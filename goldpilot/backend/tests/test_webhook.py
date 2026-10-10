"""Webhook TradingView : authentification, liste d'IP, taille, schéma, cohérence, idempotence, journal sans secret."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import select

from goldpilot import db
from goldpilot.config import TV_IPS, settings
from goldpilot.marketdata import tradingview as tv

from .conftest import TV_TOKEN

URL = "/api/webhooks/tradingview"


def minute_ms(dt: datetime) -> int:
    return int(dt.replace(second=0, microsecond=0).timestamp() * 1000)


def bar(**kw) -> dict:
    t = datetime.now(tz=timezone.utc) - timedelta(minutes=1)
    m = {"v": 1, "kind": "bar", "token": TV_TOKEN, "ticker": "MGCZ2026", "tf": "1", "t": minute_ms(t),
         "o": 4000.1, "h": 4001.5, "l": 3999.8, "c": 4000.9, "vol": 120, "tnow": minute_ms(t) + 61_000}
    m.update(kw)
    return m


def post(client, payload, **kw):
    return client.post(URL, content=payload if isinstance(payload, (bytes, str)) else json.dumps(payload),
                       headers={"content-type": "application/json", **kw.pop("headers", {})}, **kw)


def test_valid_bar_stored_once(client):
    m = bar()
    assert post(client, m).json() == {"ok": True}
    r = post(client, m)  # renvoi TradingView (5xx/timeout) : accepté sans doublon
    assert r.status_code == 200 and r.json().get("doublon") is True
    with db.session() as s:
        rows = s.execute(select(db.Bar)).scalars().all()
    assert len(rows) == 1 and rows[0].symbol == "MGCZ2026" and rows[0].minutes == 1 and rows[0].source == "tradingview"


@pytest.mark.parametrize("change,status,reason", [
    ({"token": "mauvais"}, 401, "jeton invalide"),
    ({"ticker": "MGC1!"}, 422, "symbole non accepté"),
    ({"ticker": "GCZ2026"}, 422, "symbole non accepté"),
    ({"tf": "5"}, 400, "message invalide"),
    ({"h": 3990.0}, 422, "OHLC incohérent"),
    ({"c": -1}, 400, "message invalide"),
    ({"o": float("nan")}, 400, "JSON invalide"),
    ({"extra": 1}, 400, "message invalide"),
    ({"kind": "autre"}, 400, "type de message inconnu"),
])
def test_rejections(client, change, status, reason):
    m = bar(**change)
    raw = json.dumps(m) if "o" not in change else json.dumps(m).replace("NaN", "NaN")
    r = post(client, raw)
    if reason == "JSON invalide":  # NaN accepté par json.loads → rejeté par le schéma
        assert r.status_code == 400
    else:
        assert r.status_code == status and reason in r.json()["raison"]
    with db.session() as s:
        assert not s.execute(select(db.Bar)).scalars().all()
        log = s.execute(select(db.WebhookLog)).scalars().one()
    assert log.accepted is False and "token" not in (log.payload or {})


def test_future_and_non_round_timestamps(client):
    fut = datetime.now(tz=timezone.utc) + timedelta(minutes=10)
    assert post(client, bar(t=minute_ms(fut))).status_code == 422
    assert post(client, bar(t=minute_ms(datetime.now(tz=timezone.utc)) - 30_000)).status_code == 422


def test_body_too_large_and_bad_json(client):
    assert post(client, b"{" + b" " * 5000 + b"}").status_code == 413
    assert post(client, b"pas du json").status_code == 400
    assert post(client, b"[1,2,3]").status_code == 400


def test_token_never_logged(client):
    post(client, bar())
    post(client, bar(token="faux"))
    with db.session() as s:
        logs = s.execute(select(db.WebhookLog)).scalars().all()
    assert len(logs) == 2
    for lg in logs:
        assert TV_TOKEN not in json.dumps(lg.payload) and "faux" not in json.dumps(lg.payload)


def test_ip_allowlist_enforced(client, monkeypatch):
    monkeypatch.setenv("TV_ENFORCE_IP", "true")
    settings.cache_clear()
    assert post(client, bar()).status_code == 403  # client de test hors liste TradingView
    monkeypatch.setenv("TRUST_PROXY", "true")
    settings.cache_clear()
    assert post(client, bar(), headers={"x-forwarded-for": TV_IPS[0]}).status_code == 200
    assert post(client, bar(t=bar()["t"] - 60_000), headers={"x-forwarded-for": "8.8.8.8"}).status_code == 403


def test_webhook_rate_limit(client):
    from goldpilot.api import security

    for _ in range(security.webhook_limiter.max):
        security.webhook_limiter.allow("testclient")
    assert post(client, bar()).status_code == 429


def test_daily_history_stored_by_trading_day_and_updated(client):
    # Journée de trading du jeudi 8 octobre 2026 : barre journalière horodatée 17:00 Chicago la veille (convention CME)
    t_session = int(datetime(2026, 10, 7, 22, 0, tzinfo=timezone.utc).timestamp() * 1000)
    t_midnight = int(datetime(2026, 10, 9, 0, 0, tzinfo=timezone.utc).timestamp() * 1000)  # autre convention : minuit UTC
    msg = {"v": 1, "kind": "daily", "token": TV_TOKEN, "ticker": "COMEX:MGC1!", "t": t_midnight,
           "days": [[t_session, 4010.0, 3950.0, 4000.0], [t_midnight, 4030.0, 3990.0, 4020.0]]}
    assert post(client, msg).json() == {"ok": True}
    msg["days"][1] = [t_midnight, 4031.0, 3990.0, 4021.0]
    assert post(client, msg).json() == {"ok": True}
    with db.session() as s:
        rows = {r.td: r for r in s.execute(select(db.DailyBar)).scalars()}
    epoch = datetime(1970, 1, 1).date()
    d8 = (datetime(2026, 10, 8).date() - epoch).days
    d9 = (datetime(2026, 10, 9).date() - epoch).days
    assert set(rows) == {d8, d9}
    assert rows[d9].high == 4031.0 and rows[d9].close == 4021.0


@pytest.mark.parametrize("days", [[[1, 10, 20, 15]], [[1, 20, 10]], []])
def test_daily_history_validation(client, days):
    msg = {"v": 1, "kind": "daily", "token": TV_TOKEN, "ticker": "COMEX:MGC1!", "t": 0, "days": days}
    assert post(client, msg).status_code == 400


def test_daily_history_other_symbol_rejected(client):
    msg = {"v": 1, "kind": "daily", "token": TV_TOKEN, "ticker": "OANDA:XAUUSD", "t": 0, "days": [[0, 20, 10, 15]]}
    assert post(client, msg).status_code == 422


def test_mirror_stored_once(client):
    t = minute_ms(datetime.now(tz=timezone.utc) - timedelta(minutes=20))
    m = {"v": 1, "kind": "mirror", "token": TV_TOKEN, "ticker": "MGCZ2026", "t": t, "side": -1, "price": 4001.2}
    assert post(client, m).json() == {"ok": True}
    assert post(client, m).json().get("doublon") is True
    with db.session() as s:
        assert len(s.execute(select(db.MirrorSignal)).scalars().all()) == 1


def test_delay_measurement():
    t0 = datetime(2026, 10, 9, 13, 0, tzinfo=timezone.utc)
    msg = tv.BarMsg.model_validate(bar(t=int(t0.timestamp() * 1000)))
    assert tv.delay_of(msg, t0 + timedelta(minutes=1, seconds=4)).total_seconds() == 4
    assert tv.delay_of(msg, t0 + timedelta(minutes=11)).total_seconds() == 600
