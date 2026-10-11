"""Corrections de la revue (api-site) : entrée fermée, glissement déclaré, état des notifications, gouvernance de la
stratégie (C2/C3), point de reprise après arrêt (C1), niveaux (C4) et durcissement du webhook TradingView."""
from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone

import pytest
from sqlalchemy import select

from goldpilot import db
from goldpilot.api import security
from goldpilot.engine import strategy_config
from goldpilot.marketdata import tradingview as tv

from .conftest import TV_TOKEN, utc

URL = "/api/webhooks/tradingview"


@pytest.fixture(autouse=True)
def _clear_fail_limiter():
    security.webhook_fail_limiter.hits.clear()
    yield
    security.webhook_fail_limiter.hits.clear()


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


def _signal(**kw) -> str:
    now = datetime.now(tz=timezone.utc)
    base = dict(key=f"h:{db.uid()}", created_at=now - timedelta(minutes=2), mode="simulation", validated=False, strategy_version="v",
                symbol="MGCZ2026", side=1, entry_type="market", entry_ref=4000.0, entry_max_drift=2.0, stop=3990.0, target=None,
                trail_atr=3.0, atr=4.0, contracts=2, risk_usd=210.0, reward_risk=None, valid_until=now + timedelta(minutes=10),
                exit_deadline=now + timedelta(hours=3), rationale="r", invalidation="i", calendar_note="c", price_source="TradingView",
                price_ts=now, status="ACTIF", meta={"decision_bar_ts": 0})
    base.update(kw)
    with db.session() as s:
        sig = db.Signal(**base)
        s.add(sig)
        s.flush()
        return sig.id


# ------------------------------------------------------------------ #10 entrée fermée / C4 niveaux
def test_entry_open_only_inside_validity_and_range(auth):
    now = datetime.now(tz=timezone.utc)
    ok = _signal()
    expired = _signal(valid_until=now - timedelta(minutes=1), sim_entry=4000.2, sim_entry_ts=now - timedelta(minutes=5))
    band = _signal(meta={"decision_bar_ts": 0, "band_exceeded": True})
    forbidden = _signal(meta={"decision_bar_ts": 0, "entree_interdite": "Mode sécurisé : données périmées"})
    closed = _signal(status="CLOTURE")
    sig = lambda sid: auth.get(f"/api/signals/{sid}").json()["signal"]  # noqa: E731
    assert sig(ok)["entree_ouverte"] is True
    assert sig(expired)["entree_ouverte"] is False and sig(expired)["statut"] == "ACTIF"
    assert sig(band)["entree_ouverte"] is False and sig(band)["plage_depassee"] is True
    assert sig(forbidden)["entree_ouverte"] is False and "sécurisé" in sig(forbidden)["entree_interdite"]
    assert sig(closed)["entree_ouverte"] is False


def test_levels_exposed_in_signal_json(auth):
    niv = {"plus_haut_veille": 4010.0, "plus_bas_veille": 3980.0, "plus_haut_seance": None, "plus_bas_seance": None,
           "swing_haut_15m": 4005.0, "swing_bas_15m": None, "distances_atr": {"plus_haut_veille": -2.5}}
    sid = _signal(meta={"decision_bar_ts": 0, "niveaux": niv})
    assert auth.get(f"/api/signals/{sid}").json()["signal"]["niveaux"] == niv
    assert auth.get("/api/signals").json()["signaux"][0]["niveaux"] == niv
    assert auth.get("/api/dashboard").json()["trading"]["signal_en_cours"]["niveaux"] == niv


# ------------------------------------------------------------------ #14 glissement déclaré
def test_stats_declared_slippage_against_assumption(auth):
    _signal(user_executed=True, user_entry=4000.5, user_exit=4010.0, user_contracts=1, sim_exit=4010.2, sim_entry=4000.2,
            sim_pnl_usd=200.0, user_pnl_usd=95.0, status="CLOTURE")
    _signal(side=-1, entry_ref=4000.0, user_executed=True, user_entry=3999.9, user_contracts=2, status="CLOTURE")
    _signal(user_executed=False, user_entry=4100.0)  # « non exécuté » : ignoré
    ex = auth.get("/api/stats").json()["execution"]["execution_declaree"]
    assert ex["source"] == "déclaré par toi — non confirmé par le courtier"
    assert ex["n_entrees"] == 2 and ex["glissement_entree_max_oz"] == pytest.approx(0.5)
    assert ex["glissement_sortie_median_oz"] == pytest.approx(0.2)
    assert ex["hypothese_glissement_oz"] == pytest.approx(0.3)
    assert ex["dans_hypothese"] is False  # médiane (haute) 0,5 $/once > 0,30 $/once supposé
    empty = auth.get("/api/stats")  # toujours 200 même sans déclaration
    assert empty.status_code == 200


def test_stats_declared_slippage_empty(auth):
    ex = auth.get("/api/stats").json()["execution"]["execution_declaree"]
    assert ex["n_entrees"] == 0 and ex["glissement_entree_median_oz"] is None and ex["dans_hypothese"] is None


# ------------------------------------------------------------------ #17 notifications
@pytest.fixture
def telegram_env(monkeypatch):
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123:faux")
    monkeypatch.setenv("TELEGRAM_CHAT_ID", "42")
    from goldpilot.config import settings

    settings.cache_clear()
    yield
    settings.cache_clear()


def _notif(auth):
    return auth.get("/api/dashboard").json()["statut"]["notifications"]


def test_notifications_never_verified_is_not_green(auth, telegram_env):
    n = _notif(auth)
    assert n["configure"] is True and n["ok"] is False and n["verifiees"] is False and "Jamais vérifiées" in n["texte"]


def test_failed_test_notification_turns_tile_red_and_success_green(auth, telegram_env, monkeypatch):
    from goldpilot.notify import telegram as tgmod

    monkeypatch.setattr(tgmod.Telegram, "send_now", lambda self, text: (False, "HTTP 401 Unauthorized"))
    assert auth.post("/api/notifications/test").status_code == 502
    n = _notif(auth)
    assert n["ok"] is False and "Dernier envoi en échec" in n["texte"] and "401" in n["texte"]
    monkeypatch.setattr(tgmod.Telegram, "send_now", lambda self, text: (True, ""))
    assert auth.post("/api/notifications/test").status_code == 200
    n = _notif(auth)
    assert n["ok"] is True and n["derniere"] is not None and n["derniere_tentative"]["type"] == "test"
    with db.session() as s:
        rows = s.execute(select(db.Notification).where(db.Notification.kind == "test")).scalars().all()
    assert [r.status for r in rows] == ["echec", "envoye"]


def test_old_failure_without_later_success_stays_red(auth, telegram_env):
    with db.session() as s:
        s.add(db.Notification(key="vieux", kind="systeme", text="x", status="echec", attempts=5, error="HTTP 403 Forbidden",
                              created_at=datetime.now(tz=timezone.utc) - timedelta(days=3)))
    n = _notif(auth)
    assert n["ok"] is False and n["echecs_24h"] == 0 and "403" in n["texte"]


def test_retry_in_progress_is_not_green(auth, telegram_env):
    with db.session() as s:
        s.add(db.Notification(key="ok", kind="systeme", text="x", status="envoye", attempts=1, sent_at=db.now()))
        s.add(db.Notification(key="retry", kind="signal", text="x", status="a_envoyer", attempts=2, error="erreur réseau : ConnectError"))
    n = _notif(auth)
    assert n["ok"] is False and "nouvel essai" in n["texte"]


# ------------------------------------------------------------------ C1 reprise après arrêt
def test_resume_after_performance_halt_records_reset_point(auth):
    version = strategy_config.load_production()["version"]
    with db.session() as s:
        db.kv_set(s, "halt", {"raison": "drawdown", "depuis": "2026-10-01T00:00:00+00:00", "type": "performance"})
    r = auth.post("/api/engine/resume-after-halt")
    assert r.status_code == 200
    with db.session() as s:
        assert db.kv_get(s, "halt") is None
        reset = db.kv_get(s, "halt_reset")
    assert reset["version"] == version and datetime.fromisoformat(reset["depuis"]) <= datetime.now(tz=timezone.utc)


def test_resume_refused_for_version_halt(auth):
    with db.session() as s:
        db.kv_set(s, "halt", {"raison": "nouvelle version", "depuis": "2026-10-01T00:00:00+00:00", "type": "version"})
    r = auth.post("/api/engine/resume-after-halt")
    assert r.status_code == 409 and "approuve" in r.json()["detail"]
    with db.session() as s:
        assert db.kv_get(s, "halt")["type"] == "version" and db.kv_get(s, "halt_reset") is None


# ------------------------------------------------------------------ C2/C3 gouvernance
def test_governance_and_approval(auth):
    version = strategy_config.load_production()["version"]
    with db.session() as s:
        db.kv_set(s, "approved_version", {"version": "ancienne", "approuve_le": "2026-01-01T00:00:00+00:00", "par": "initialisation"})
        db.kv_set(s, "halt", {"raison": f"nouvelle version de stratégie non approuvée : {version}", "depuis": "x", "type": "version"})
        db.kv_set(s, "revue_periodique", {"date": "2026-10-10", "version": version, "n": 0, "conclusion": "échantillon trop petit"})
    g = auth.get("/api/strategy/governance").json()
    assert g["version_courante"] == version and g["en_attente"] is True and g["version_approuvee"]["version"] == "ancienne"
    assert g["revue_periodique"]["date"] == "2026-10-10" and "comparaison" in g
    assert auth.post("/api/strategy/approve", json={"version": "autre", "confirmation": "J'APPROUVE CETTE VERSION"}).status_code == 409
    assert auth.post("/api/strategy/approve", json={"version": version, "confirmation": "oui"}).status_code == 422
    assert auth.post("/api/strategy/approve", json={"version": version, "confirmation": "J'APPROUVE CETTE VERSION"}).status_code == 200
    g = auth.get("/api/strategy/governance").json()
    assert g["en_attente"] is False and g["version_approuvee"]["par"] == "utilisateur"
    with db.session() as s:
        assert db.kv_get(s, "halt") is None
        assert s.execute(select(db.Audit).where(db.Audit.action == "version_approuvee")).scalars().first() is not None


def test_approval_keeps_performance_halt(auth):
    version = strategy_config.load_production()["version"]
    with db.session() as s:
        db.kv_set(s, "halt", {"raison": "drawdown", "depuis": "x", "type": "performance"})
    assert auth.post("/api/strategy/approve", json={"version": version, "confirmation": "J'APPROUVE CETTE VERSION"}).status_code == 200
    with db.session() as s:
        assert db.kv_get(s, "halt")["type"] == "performance"


def test_governance_requires_login(client):
    assert client.get("/api/strategy/governance").status_code == 401


# ------------------------------------------------------------------ journal : dates New York complètes
def test_cross_check_journal_has_date(auth):
    with db.session() as s:
        s.add(db.MirrorSignal(symbol="MGCZ2026", bar_ts=utc(2026, 10, 9, 13, 0), side=1, price=4000.0))
    row = auth.get("/api/journal?type=controle").json()["lignes"][0]
    assert row["heure"] == "09/10/2026 09:15 New York"


# ------------------------------------------------------------------ #19 webhook : NaN, kind, journal
@pytest.mark.parametrize("raw", [
    '{"kind":"zz","x":NaN}', '{"kind":"bar","token":"bad","x":Infinity}', '{"kind":"bar","o":-Infinity}',
])
def test_non_finite_json_rejected_and_logged(client, raw):
    r = post(client, raw)
    assert r.status_code == 400 and r.json()["raison"] == "JSON invalide"
    with db.session() as s:
        log = s.execute(select(db.WebhookLog)).scalars().one()
    assert log.accepted is False and log.payload == {}


def test_long_kind_is_not_stored_verbatim(client):
    r = post(client, {"kind": "a" * 40, "token": "x"})
    assert r.status_code == 400
    with db.session() as s:
        log = s.execute(select(db.WebhookLog)).scalars().one()
    assert log.kind == "?" and len(log.kind) <= 16


def test_unhashable_kind_is_rejected_cleanly(client):
    assert post(client, {"kind": ["bar"]}).status_code == 400


def test_volume_must_be_finite_and_non_negative(client):
    assert post(client, bar(vol=-1)).status_code == 400
    assert post(client, bar(vol=1e300)).status_code == 400
    with db.session() as s:
        assert not s.execute(select(db.Bar)).scalars().all()


def test_log_write_failure_never_returns_500(client, monkeypatch):
    real = db.WebhookLog

    def boom(**kw):
        raise RuntimeError("base indisponible")

    monkeypatch.setattr(db, "WebhookLog", boom)
    assert post(client, bar(token="faux")).status_code == 401
    assert post(client, bar()).json() == {"ok": True}  # barre stockée malgré l'échec du journal
    monkeypatch.setattr(db, "WebhookLog", real)
    with db.session() as s:
        assert len(s.execute(select(db.Bar)).scalars().all()) == 1


# ------------------------------------------------------------------ #20 limitation : les refus ne bloquent pas les vraies barres
def test_wrong_token_flood_does_not_block_real_bars(client):
    for _ in range(200):
        post(client, bar(token="mauvais"))
    r = post(client, bar())
    assert r.status_code == 200 and r.json() == {"ok": True}
    with db.session() as s:
        assert len(s.execute(select(db.Bar)).scalars().all()) == 1
        logs = s.execute(select(db.WebhookLog).where(db.WebhookLog.accepted.is_(False))).scalars().all()
    assert len(logs) == security.webhook_fail_limiter.max  # au-delà du budget de refus : plus aucune écriture


def test_failed_attempts_over_budget_get_429(client):
    for _ in range(security.webhook_fail_limiter.max):
        post(client, b"pas du json")
    assert post(client, b"pas du json").status_code == 429


# ------------------------------------------------------------------ #21 horodatages et prix miroir
def test_timestamp_bounds_and_too_old(client):
    assert post(client, bar(t=0, tnow=0)).status_code == 400
    assert post(client, bar(t=-10 ** 17)).status_code == 400
    assert post(client, bar(t=10 ** 17)).status_code == 400
    old = minute_ms(datetime.now(tz=timezone.utc) - timedelta(days=4))
    r = post(client, bar(t=old, tnow=old + 61_000))
    assert r.status_code == 422 and "trop ancien" in r.json()["raison"]
    with db.session() as s:
        assert not s.execute(select(db.Bar)).scalars().all()


def test_daily_extreme_timestamp_rejected(client):
    t = minute_ms(datetime.now(tz=timezone.utc))
    msg = {"v": 1, "kind": "daily", "token": TV_TOKEN, "ticker": "COMEX:MGC1!", "t": t, "days": [[1e20, 3, 1, 2]]}
    assert post(client, msg).status_code == 400


@pytest.mark.parametrize("price", [-5, 0, 1e9])
def test_mirror_price_validated(client, price):
    t = minute_ms(datetime.now(tz=timezone.utc) - timedelta(minutes=20))
    m = {"v": 1, "kind": "mirror", "token": TV_TOKEN, "ticker": "MGCZ2026", "t": t, "side": 1, "price": price}
    assert post(client, m).status_code == 400
    with db.session() as s:
        assert not s.execute(select(db.MirrorSignal)).scalars().all()


def test_mirror_too_old_rejected(client):
    t = minute_ms(datetime.now(tz=timezone.utc) - timedelta(days=5))
    m = {"v": 1, "kind": "mirror", "token": TV_TOKEN, "ticker": "MGCZ2026", "t": t, "side": 1, "price": 4000.0}
    assert post(client, m).status_code == 422


def test_parse_bounds_unit():
    now = datetime.now(tz=timezone.utc)
    with pytest.raises(tv.Rejected):
        tv.parse(bar(t=tv.T_MAX_MS + 60_000), TV_TOKEN, now)
