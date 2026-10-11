"""Données de test DÉTERMINISTES et FICTIVES pour les tests de bout en bout (Playwright).

Écrit directement dans la base via les modèles GoldPilot (aucun point d'accès d'aide côté serveur).
Aucune de ces valeurs ne provient du marché : prix, signaux et séries macro sont inventés pour les tests.

Usage (avec DATABASE_URL défini et le dossier goldpilot/backend dans PYTHONPATH) :
    python seed.py init            # crée le schéma et insère le jeu de test complet
    python seed.py heartbeat-on    # signe de vie récent du moteur + qualité des données « ok »
    python seed.py heartbeat-off   # supprime le signe de vie (moteur considéré arrêté)
    python seed.py pending         # crée un nouveau signal EN_ATTENTE sans position simulée, affiche son id
    python seed.py version-pending # version approuvée ≠ version en service + arrêt de sécurité « version » (gouvernance)
"""
from __future__ import annotations

import sys
import uuid
from datetime import datetime, timedelta, timezone

from sqlalchemy import delete

from goldpilot import db

NOTE = "Données de test E2E (fictives)"
CONTRAT = "MGCZ2026"


def now() -> datetime:
    return datetime.now(timezone.utc).replace(microsecond=0)


def checks(bloque: bool = False) -> list[dict]:
    return [
        {"controle": "Données de marché", "ok": True, "detail": "qualité ok (test)", "bloquant": True},
        {"controle": "Calendrier économique", "ok": True, "detail": "aucune annonce à fort impact dans la fenêtre (test)", "bloquant": True},
        {"controle": "Taille de position", "ok": not bloque, "detail": "2 contrat(s), risque 236 $ ≤ 250 $ (test)", "bloquant": True},
        {"controle": "Règles incertaines", "ok": True, "detail": "non bloquant en simulation (test)", "bloquant": False},
    ]


def make_signal(s, sid: str, statut: str, created: datetime, side: int, entry: float, *, sim_entry=None, sim_exit=None,
                sim_r=None, reason: str = "", user=None) -> db.Signal:
    atr = 4.2
    stop = entry - side * 2.5 * atr
    sig = db.Signal(
        id=sid, key=f"e2e-{sid}", created_at=created, mode="simulation", validated=False,
        strategy_version="S1-test-e2e", symbol=CONTRAT, side=side, entry_type="market", entry_ref=entry,
        entry_max_drift=0.5 * atr, stop=round(stop, 2), target=None, trail_atr=3.0, atr=atr, contracts=2, risk_usd=236.0,
        reward_risk=None, valid_until=created + timedelta(minutes=15), exit_deadline=created + timedelta(hours=8),
        rationale=f"{NOTE} : franchissement du seuil d'extension de séance.",
        invalidation="Annulé si le prix sort de la plage d'entrée ou après 15 minutes.",
        calendar_note="Aucune annonce à fort impact dans les 30 minutes (test).", price_source="TradingView (webhook) — test",
        price_ts=created - timedelta(seconds=20), status=statut, status_reason=reason,
        meta={"decision_bar_ts": int((created - timedelta(seconds=30) - timedelta(minutes=15)).timestamp() * 1e9)},
    )
    if sim_entry is not None:
        sig.sim_entry, sig.sim_entry_ts, sig.sim_stop = sim_entry, created + timedelta(minutes=1), sig.stop
    if sim_exit is not None:
        sig.sim_exit, sig.sim_exit_ts, sig.sim_exit_reason = sim_exit, created + timedelta(hours=3), "stop suiveur"
        sig.sim_r, sig.sim_pnl_usd = sim_r, round((sim_r or 0) * 236.0, 2)
    if user is not None:
        sig.user_executed, sig.user_entry, sig.user_exit, sig.user_contracts, sig.user_pnl_usd = user
    s.add(sig)
    s.flush()
    s.add(db.SignalEvent(signal_id=sid, ts=created, kind="cree", detail={"contrats": 2, "risque": 236.0}))
    if sim_entry is not None:
        s.add(db.SignalEvent(signal_id=sid, ts=created + timedelta(minutes=1), kind="entree_simulee", detail={"prix": sim_entry}))
    if sim_exit is not None:
        s.add(db.SignalEvent(signal_id=sid, ts=created + timedelta(hours=3), kind="sortie_simulee",
                             detail={"prix": sim_exit, "raison": "stop suiveur", "r": sim_r}))
    if statut == "EXPIRE":
        s.add(db.SignalEvent(signal_id=sid, ts=created + timedelta(minutes=15), kind="expire", detail={}))
    if statut == "ANNULE":
        s.add(db.SignalEvent(signal_id=sid, ts=created + timedelta(minutes=4), kind="annule", detail={"raison": "prix hors plage d'entrée"}))
    s.add(db.Decision(bar_ts=created - timedelta(minutes=15, seconds=30), strategy_version="S1-test-e2e", outcome="signal",
                      summary=f"Signal {'LONG' if side > 0 else 'SHORT'} émis ({NOTE.lower()})", reasons=["tous les contrôles satisfaits"],
                      context={"regime": "tendance haussière (test)", "z": 2.61, "atr": atr, "franchissement": side, "prix": entry,
                               "contrat": CONTRAT}, risk_checks=checks(), signal_id=sid))
    s.add(db.Notification(created_at=created, key=f"e2e-notif-{sid}", kind="signal", signal_id=sid, text=f"<b>GOLD — SIGNAL</b> {NOTE}",
                          status="envoye", attempts=1, sent_at=created + timedelta(seconds=3)))
    return sig


def init() -> None:
    db.init(create=True)
    t = now()
    with db.session() as s:
        db.kv_set(s, "engine_mode", {"mode": "actif", "qualite": "ok", "problemes": []})
        db.kv_set(s, "user_mode", "actif")
        db.kv_set(s, "notifications", True)
        db.kv_set(s, "paper_account", {"balance": 50_472.0, "hwm_eod": 50_472.0, "floor": 48_972.0, "best_day": 472.0, "day_pnl": 0.0,
                                       "days": 3, "breached": False, "breach_reason": "", "day_start_balance": 50_472.0,
                                       "day": t.date().isoformat(), "passed": False, "target": 3000.0})
        db.kv_set(s, "macro_context", {
            "disponible": True, "maj": (t - timedelta(hours=2)).isoformat(),
            "probleme": "Série(s) indisponible(s) : DGS10 (test : réponse invalide)",
            "series": [
                {"id": "DFII10", "nom": "Taux réel américain 10 ans (TIPS)", "valeur": 1.85, "unite": "%", "date": (t - timedelta(days=1)).date().isoformat(),
                 "variation_5j": -0.07, "url": "https://fred.stlouisfed.org/series/DFII10"},
                {"id": "DTWEXBGS", "nom": "Dollar américain — indice large nominal (Fed)", "valeur": 121.3456, "unite": "indice (janv. 2006 = 100)",
                 "date": (t - timedelta(days=6)).date().isoformat(), "variation_5j": None, "url": "https://fred.stlouisfed.org/series/DTWEXBGS"},
            ]})
        make_signal(s, "e2ecloture", "CLOTURE", t - timedelta(days=3), 1, 3990.0, sim_entry=3990.4, sim_exit=4002.1, sim_r=1.18,
                    reason="sortie par stop suiveur", user=(True, 3990.6, 4001.8, 2, 224.0))
        make_signal(s, "e2eexpire", "EXPIRE", t - timedelta(days=2), -1, 4010.0, reason="validité dépassée sans déclenchement")
        make_signal(s, "e2eannule", "ANNULE", t - timedelta(days=1), 1, 4021.0, reason="prix hors plage d'entrée")
        make_signal(s, "e2eattente", "EN_ATTENTE", t - timedelta(hours=2), -1, 4030.0)
        actif = make_signal(s, "e2eactif", "ACTIF", t - timedelta(minutes=5), 1, 4035.5, sim_entry=4035.8)
        actif.meta = dict(actif.meta, niveaux={  # niveaux fictifs (test)
            "plus_haut_veille": 4041.2, "plus_bas_veille": 4002.4, "plus_haut_seance": 4036.0, "plus_bas_seance": 4012.3,
            "swing_haut_15m": None, "swing_bas_15m": 4020.1,
            "distances_atr": {"plus_haut_veille": -1.36, "plus_bas_veille": 7.88, "plus_haut_seance": -0.12, "plus_bas_seance": 5.5,
                              "swing_haut_15m": None, "swing_bas_15m": 3.69}})
        db.kv_set(s, "revue_periodique", {
            "date": (t - timedelta(days=1)).date().isoformat(), "version": "S1-test-e2e", "n": 3, "esperance_R": 0.12,
            "borne_basse_95_R": None, "drawdown_max_R": -1.0, "serie_pertes_max": 1, "taux_de_gain": 0.667,
            "reference": {"esperance_R_walk_forward": None, "esperance_R_2022_2025": None, "source": "research/output/selection,final"},
            "seuils": {"drawdown_R": -27.27, "serie_pertes": 17},
            "conclusion": f"3 trade(s) simulé(s) : échantillon trop petit pour conclure ({NOTE.lower()})."})
        s.add(db.Decision(bar_ts=t - timedelta(minutes=30), strategy_version="S1-test-e2e", outcome="aucun_setup",
                          summary="Aucun setup valide : les conditions ne sont pas réunies (test)", reasons=["pas de franchissement du seuil"],
                          context={"regime": "range (test)", "z": 0.4}, risk_checks=[]))
        s.add(db.Decision(bar_ts=t - timedelta(minutes=45), strategy_version="S1-test-e2e", outcome="refuse",
                          summary="Setup refusé par le risque (test)", reasons=["taille de position nulle"], context={"z": 2.7},
                          risk_checks=checks(bloque=True)))
        s.add(db.Incident(created_at=t - timedelta(minutes=50), severity="alerte", component="donnees", code="e2e_retard",
                          message="Données en retard de 4 minutes (test)"))
        s.add(db.Incident(created_at=t - timedelta(days=1), severity="critique", component="moteur", code="e2e_resolu",
                          message="Moteur silencieux (test, résolu)", resolved_at=t - timedelta(hours=20)))
        s.add(db.Incident(created_at=t - timedelta(minutes=40), severity="avertissement", component="contexte", code="fred",
                          message="Contexte macro FRED partiellement indisponible (test)"))
        for i, (st, err) in enumerate([("echec", "HTTP 502 (test)"), ("perime", "signal périmé avant l'envoi (test)"), ("desactive", "")]):
            s.add(db.Notification(created_at=t - timedelta(minutes=20 + i), key=f"e2e-n-{st}", kind="systeme", text=f"Alerte système ({NOTE})",
                                  status=st, attempts=3 if st == "echec" else 0, error=err))
        s.add(db.WebhookLog(received_at=t - timedelta(hours=1), ip="52.89.214.238", kind="bar", accepted=True, reason="retard 2 s",
                            payload={"kind": "bar", "test": True}))
        s.add(db.WebhookLog(received_at=t - timedelta(minutes=59), ip="203.0.113.9", kind="?", accepted=False, reason="jeton invalide",
                            payload={}))
        s.add(db.MirrorSignal(received_at=t - timedelta(days=3), symbol=CONTRAT, bar_ts=t - timedelta(days=3, minutes=16), side=1, price=3990.0,
                              matched_signal_id="e2ecloture", verdict="concordant", checked_at=t - timedelta(days=3)))
        s.add(db.MirrorSignal(received_at=t - timedelta(days=1), symbol=CONTRAT, bar_ts=t - timedelta(days=1, minutes=16), side=-1, price=4015.0,
                              verdict="decision_absente", checked_at=t - timedelta(days=1)))
        s.add(db.EconomicEvent(source="manuel", uid="e2e-cpi", title="Indice des prix à la consommation (CPI, États-Unis) — test", impact="fort",
                               ts=t + timedelta(days=3), source_url="saisi manuellement"))
        db.audit(s, "systeme", "initialisation_e2e", {"note": NOTE})


def heartbeat(on: bool) -> None:
    db.init()
    t = now()
    with db.session() as s:
        s.execute(delete(db.Heartbeat).where(db.Heartbeat.component == "engine"))
        if on:
            bar_ts = t.replace(second=0) - timedelta(minutes=1)
            s.add(db.Heartbeat(component="engine", ts=t, status="ok",
                               detail={"last_price": 4036.2, "last_bar_end": (bar_ts + timedelta(minutes=1)).isoformat()}))
            s.execute(delete(db.Bar).where(db.Bar.symbol == CONTRAT))
            s.add(db.Bar(source="tradingview", symbol=CONTRAT, ts=bar_ts, minutes=1,
                         open=4036.0, high=4036.5, low=4035.8, close=4036.2, volume=12, processed=True))
            db.kv_set(s, "engine_mode", {"mode": "actif", "qualite": "ok", "problemes": []})


def version_pending() -> None:
    db.init()
    t = now()
    with db.session() as s:
        db.kv_set(s, "approved_version", {"version": "S0-ancienne-version-e2e", "approuve_le": (t - timedelta(days=30)).isoformat(),
                                          "par": "initialisation"})
        db.kv_set(s, "halt", {"raison": "nouvelle version de stratégie non approuvée (test E2E)", "depuis": t.isoformat(), "type": "version"})


def pending() -> str:
    db.init()
    sid = "e2e" + uuid.uuid4().hex[:20]
    with db.session() as s:
        make_signal(s, sid, "EN_ATTENTE", now() - timedelta(days=30), 1, 3900.0)
    return sid


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    if cmd == "init":
        init()
    elif cmd == "heartbeat-on":
        heartbeat(True)
    elif cmd == "heartbeat-off":
        heartbeat(False)
    elif cmd == "version-pending":
        version_pending()
    elif cmd == "pending":
        print(pending())
    else:
        sys.exit(__doc__)
