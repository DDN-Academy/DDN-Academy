"""Alertes téléphone (Telegram) : contenu exigé, échappement HTML, envoi, réessais, idempotence, signaux périmés."""
from __future__ import annotations

import json
from datetime import timedelta

import httpx
import pytest
from sqlalchemy import select

from goldpilot import db
from goldpilot.notify import messages, telegram
from goldpilot.notify.telegram import Telegram, deliver_pending, enqueue

from .conftest import utc
from .test_api import _signal


class FakeTelegram:
    """Serveur Telegram simulé (httpx.MockTransport) : aucune requête réseau réelle."""

    def __init__(self, fail: int = 0, status: int = 200):
        self.fail, self.status, self.sent = fail, status, []

    def __call__(self, request: httpx.Request) -> httpx.Response:
        if request.url.path.endswith("/getUpdates"):
            return httpx.Response(200, json={"ok": True, "result": [{"message": {"chat": {"id": 123456, "first_name": "Moi"}}}]})
        if self.fail:
            self.fail -= 1
            return httpx.Response(self.status, json={"ok": False, "description": "Too Many Requests"})
        self.sent.append(json.loads(request.content))
        return httpx.Response(200, json={"ok": True, "result": {}})


def tg(fake: FakeTelegram) -> Telegram:
    t = Telegram("123:ABC", "42", client=httpx.Client(transport=httpx.MockTransport(fake)), base_url="https://telegram.test")
    t._last = -10.0
    return t


@pytest.fixture(autouse=True)
def no_wait(monkeypatch):
    monkeypatch.setattr(telegram.time, "sleep", lambda s: None)
    telegram._next_try.clear()


def test_signal_alert_contains_every_required_field(env):
    sid = _signal(rationale="Prix < moyenne & <script>", calendar_note="Aucune restriction en cours")
    with db.session() as s:
        sig = s.get(db.Signal, sid)
        txt = messages.new_signal(sig, "Micro Gold décembre 2026 (MGCZ6 sur Tradovate, COMEX:MGCZ2026 sur TradingView)", 1.9, "")
    for must in ("SIMULATION — NE PAS EXÉCUTER", "SIGNAL LONG", "Instrument :", "MGCZ6", "COMEX:MGCZ2026", "(heure de Paris)", "New York",
                 "Sens :", "Entrée :", "immédiate (au marché)", "plage acceptable 3 998.0 – 4 002.0", "Stop-loss :</b> 3 990.0",
                 "Take-profit :", "stop suiveur", "Rendement/risque :", "1.90", "Taille :</b> 2 contrat(s) MGC", "Risque estimé :</b> 210 $",
                 "Validité :", "Annulation :", "Pourquoi :", "Calendrier :", "Prix :", "TradingView"):
        assert must in txt, must
    assert "<script>" not in txt and "&lt;script&gt;" in txt and "&amp;" in txt


def test_real_validated_signal_has_no_simulation_banner(env):
    sid = _signal(mode="reel", validated=True)
    with db.session() as s:
        txt = messages.new_signal(s.get(db.Signal, sid), "MGC", None, "")
    assert "SIMULATION" not in txt


def test_conditional_entry_and_fixed_target_wording(env):
    sid = _signal(entry_type="stop", target=4020.0, reward_risk=2.0, status="EN_ATTENTE")
    with db.session() as s:
        txt = messages.new_signal(s.get(db.Signal, sid), "MGC", None, "")
    assert "conditionnelle (ordre stop à 4 000.0)" in txt and "Take-profit :</b> 4 020.0" in txt and "2.00" in txt


def test_send_ok_and_message_truncated():
    fake = FakeTelegram()
    ok, err = tg(fake).send_now("x" * 5000)
    assert ok and err == "" and len(fake.sent[0]["text"]) == 4096 and fake.sent[0]["parse_mode"] == "HTML"


def test_send_error_reported_without_token():
    ok, err = tg(FakeTelegram(fail=1, status=429)).send_now("x")
    assert not ok and "429" in err and "123:ABC" not in err


def test_network_error():
    def boom(request):
        raise httpx.ConnectError("down")

    t = Telegram("123:ABC", "42", client=httpx.Client(transport=httpx.MockTransport(boom)), base_url="https://telegram.test")
    ok, err = t.send_now("x")
    assert not ok and err == "erreur réseau : ConnectError"


def test_not_configured():
    assert Telegram("", "").send_now("x") == (False, "Telegram non configuré (TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID)")


def test_detect_chat_id():
    assert tg(FakeTelegram()).detect_chat_id() == [{"chat_id": "123456", "nom": "Moi"}]


def test_enqueue_is_idempotent_and_keeps_transaction(env):
    with db.session() as s:
        db.kv_set(s, "marqueur", 1)  # écriture concurrente dans la même transaction
        assert enqueue(s, "k1", "systeme", "a")
        assert not enqueue(s, "k1", "systeme", "b")
    with db.session() as s:
        assert db.kv_get(s, "marqueur") == 1
        assert len(s.execute(select(db.Notification)).scalars().all()) == 1


def test_disabled_notifications_are_recorded_not_sent(env):
    fake = FakeTelegram()
    with db.session() as s:
        enqueue(s, "k", "systeme", "a", enabled=False)
    assert deliver_pending(tg(fake)) == 0 and fake.sent == []
    with db.session() as s:
        assert s.execute(select(db.Notification)).scalars().one().status == "desactive"


def test_retry_with_backoff_then_failure(env, monkeypatch):
    clock = [1000.0]
    monkeypatch.setattr(telegram.time, "monotonic", lambda: clock[0])
    fake = FakeTelegram(fail=10, status=502)
    t = tg(fake)
    with db.session() as s:
        enqueue(s, "k", "systeme", "a")
    deliver_pending(t)
    deliver_pending(t)  # pendant l'attente : pas de nouvel essai
    with db.session() as s:
        n = s.execute(select(db.Notification)).scalars().one()
    assert n.attempts == 1 and n.status == "a_envoyer"
    for _ in range(10):
        clock[0] += 200
        deliver_pending(t)
    with db.session() as s:
        n = s.execute(select(db.Notification)).scalars().one()
    assert n.status == "echec" and n.attempts == telegram.MAX_ATTEMPTS and "502" in n.error


def test_retry_succeeds(env, monkeypatch):
    clock = [1000.0]
    monkeypatch.setattr(telegram.time, "monotonic", lambda: clock[0])
    fake = FakeTelegram(fail=1, status=502)
    t = tg(fake)
    with db.session() as s:
        enqueue(s, "k", "systeme", "a")
    deliver_pending(t)
    clock[0] += 10
    assert deliver_pending(t) == 1
    with db.session() as s:
        n = s.execute(select(db.Notification)).scalars().one()
    assert n.status == "envoye" and n.attempts == 2 and n.sent_at is not None


def test_stale_signal_alert_never_sent(env):
    fake = FakeTelegram()
    expired = _signal(key="a", valid_until=utc(2026, 10, 9, 13, 30))
    cancelled = _signal(key="b", status="ANNULE")
    band = _signal(key="c", meta={"decision_bar_ts": 0, "td": 1, "exit_msess": 1290, "band_exceeded": True})
    fresh = _signal(key="d")
    with db.session() as s:
        for sid in (expired, cancelled, band, fresh):
            enqueue(s, f"new:{sid}", "signal", f"signal {sid}", sid)
    now = utc(2026, 10, 9, 13, 31)  # validité du premier signal dépassée
    with db.session() as s:
        s.get(db.Signal, fresh).valid_until = now + timedelta(minutes=10)
    assert deliver_pending(tg(fake), now=now) == 1
    assert [m["text"] for m in fake.sent] == [f"signal {fresh}"]
    with db.session() as s:
        st = {n.signal_id: n.status for n in s.execute(select(db.Notification)).scalars()}
    assert st[expired] == st[cancelled] == st[band] == "perime" and st[fresh] == "envoye"


def test_logging_never_leaks_urls(caplog):
    """httpx journalise l'URL complète au niveau INFO ; l'URL Telegram contient le jeton du bot."""
    import logging

    from goldpilot.engine.runner import configure_logging

    logging.getLogger("httpx").setLevel(logging.NOTSET)
    configure_logging("INFO")
    with caplog.at_level(logging.INFO):  # niveau racine INFO, comme en production avec LOG_LEVEL=INFO
        assert tg(FakeTelegram()).send_now("x")[0]
    assert "123:ABC" not in caplog.text
