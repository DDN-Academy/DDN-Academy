"""Envoi Telegram idempotent avec réessais.

Chaque notification est d'abord enregistrée en base avec une clé unique (pas de doublon possible, même
en cas de redémarrage), puis envoyée ; en cas d'échec réseau elle est réessayée (jusqu'à 5 fois) et
l'échec est visible sur le site. Le jeton du bot n'est jamais écrit dans les journaux.
API : https://core.telegram.org/bots/api (sendMessage, parse_mode HTML, texte ≤ 4 096 caractères ;
environ 1 message par seconde et par conversation).
"""
from __future__ import annotations

import logging
import time

import httpx
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from .. import db

log = logging.getLogger("goldpilot.telegram")
API = "https://api.telegram.org"
MAX_ATTEMPTS = 5


class Telegram:
    def __init__(self, token: str, chat_id: str, client: httpx.Client | None = None, base_url: str = API):
        self.token, self.chat_id = token, chat_id
        self.client = client or httpx.Client(timeout=10)
        self.base = base_url
        self._last = 0.0

    @property
    def configured(self) -> bool:
        return bool(self.token and self.chat_id)

    def send_now(self, text: str) -> tuple[bool, str]:
        if not self.configured:
            return False, "Telegram non configuré (TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID)"
        wait = 1.05 - (time.monotonic() - self._last)
        if wait > 0:
            time.sleep(wait)
        try:
            r = self.client.post(f"{self.base}/bot{self.token}/sendMessage",
                                 json={"chat_id": self.chat_id, "text": text[:4096], "parse_mode": "HTML",
                                       "disable_web_page_preview": True})
            self._last = time.monotonic()
            if r.status_code == 200 and r.json().get("ok"):
                return True, ""
            desc = r.json().get("description", "") if r.headers.get("content-type", "").startswith("application/json") else ""
            return False, f"HTTP {r.status_code} {desc}"[:300]
        except httpx.HTTPError as e:
            return False, f"erreur réseau : {type(e).__name__}"

    def detect_chat_id(self) -> list[dict]:
        """Lit les derniers messages reçus par le bot pour trouver ton identifiant de conversation."""
        r = self.client.get(f"{self.base}/bot{self.token}/getUpdates", params={"limit": 20})
        out = []
        for u in r.json().get("result", []):
            chat = (u.get("message") or {}).get("chat") or {}
            if chat:
                out.append({"chat_id": str(chat.get("id")), "nom": chat.get("first_name") or chat.get("title") or ""})
        return out


def enqueue(s, key: str, kind: str, text: str, signal_id: str | None = None, enabled: bool = True) -> bool:
    """Enregistre une notification ; renvoie False si elle existait déjà (idempotence)."""
    if s.execute(select(db.Notification.id).where(db.Notification.key == key)).first():
        return False
    n = db.Notification(key=key, kind=kind, text=text, signal_id=signal_id, status="a_envoyer" if enabled else "desactive")
    try:
        with s.begin_nested():  # point de sauvegarde : un doublon concurrent n'annule pas le reste de la transaction
            s.add(n)
    except IntegrityError:
        return False
    return True


STOPPED_MODES = {"securise": "sécurisé", "arret": "arrêt de sécurité", "pause": "pause"}  # aucune nouvelle entrée
BACKOFF_S = (0, 5, 15, 45, 135)  # attente avant chaque essai : ~3 min au total avant de déclarer l'échec
_next_try: dict[int, float] = {}


def deliver_pending(tg: Telegram, limit: int = 20, now=None) -> int:
    """Envoie les notifications en attente (ordre chronologique). Renvoie le nombre envoyé.

    Une alerte de signal (ou de déplacement de stop) n'est jamais envoyée si, au moment de l'envoi, le signal
    n'est plus exploitable (clôturé, annulé, expiré, validité dépassée, prix sorti de la plage, « ne plus entrer »)
    ou si le moteur est en mode sécurisé, arrêt de sécurité ou pause (alerte de nouveau signal) : elle est
    marquée « périmée » et visible dans le journal. `now` = horloge du moteur (virtuelle en rejeu)."""
    now = now or db.now()
    sent = 0
    with db.session() as s:
        mode = (db.kv_get(s, "engine_mode") or {}).get("mode")
        rows = s.execute(select(db.Notification).where(db.Notification.status == "a_envoyer")
                         .order_by(db.Notification.id).limit(limit)).scalars().all()
        for n in rows:
            if n.kind in ("signal", "stop") and n.signal_id:
                sig = s.get(db.Signal, n.signal_id)
                m = (sig.meta or {}) if sig is not None else {}
                stale = (sig is None or sig.status not in ("EN_ATTENTE", "ACTIF")
                         or (n.kind == "signal" and (now >= sig.valid_until or m.get("band_exceeded") or m.get("entree_interdite"))))
                if not stale and n.kind == "signal" and mode in STOPPED_MODES:
                    n.status, n.error = "perime", f"non envoyée : moteur en mode {STOPPED_MODES[mode]} au moment de l'envoi"
                    continue
                if stale:
                    n.status, n.error = "perime", "non envoyée : signal plus exploitable au moment de l'envoi"
                    continue
            if time.monotonic() < _next_try.get(n.id, 0.0):
                continue
            ok, err = tg.send_now(n.text)
            n.attempts += 1
            if ok:
                n.status, n.sent_at, n.error = "envoye", db.now(), ""
                _next_try.pop(n.id, None)
                sent += 1
            else:
                n.error = err
                if n.attempts >= MAX_ATTEMPTS or "non configuré" in err:
                    n.status = "echec"
                    _next_try.pop(n.id, None)
                    log.warning("notification %s en échec : %s", n.id, err)
                else:
                    _next_try[n.id] = time.monotonic() + BACKOFF_S[min(n.attempts, len(BACKOFF_S) - 1)]
                break  # Telegram en erreur : on n'insiste pas sur les suivantes pendant ce passage
    return sent
