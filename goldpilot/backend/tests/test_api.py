"""API : authentification, protection CSRF, en-têtes de sécurité, réglages, verrou du mode réel,
signaux (déclaration d'exécution, annulation), journal, absence de faux « vert »."""
from __future__ import annotations

from datetime import timedelta

from sqlalchemy import select

from goldpilot import db
from goldpilot.api import security
from goldpilot.engine import strategy_config

from .conftest import PASSWORD, utc


def test_health_reports_silent_engine_then_ok(client):
    r = client.get("/api/health")
    assert r.status_code == 503 and r.json()["moteur"] == "silencieux"
    with db.session() as s:
        db.beat(s, "engine", "actif")
    assert client.get("/api/health").status_code == 200


def test_everything_requires_login(client):
    for path in ("/api/dashboard", "/api/signals", "/api/journal", "/api/stats", "/api/settings", "/api/calendar", "/api/setup/pine"):
        assert client.get(path).status_code == 401, path
    assert client.post("/api/engine/mode", json={"mode": "pause"}).status_code == 401


def test_login_wrong_password_and_rate_limit(client):
    for _ in range(5):
        assert client.post("/api/auth/login", json={"password": "faux"}).status_code == 401
    assert client.post("/api/auth/login", json={"password": PASSWORD}).status_code == 429
    with db.session() as s:
        actions = [a.action for a in s.execute(select(db.Audit)).scalars()]
    assert actions.count("connexion_refusee") == 5


def test_session_cookie_flags_and_hash_only_in_db(client):
    r = client.post("/api/auth/login", json={"password": PASSWORD})
    cookie = r.headers["set-cookie"].lower()
    assert "httponly" in cookie and "samesite=strict" in cookie
    token = client.cookies.get(security.COOKIE)
    with db.session() as s:
        rows = s.execute(select(db.LoginSession)).scalars().all()
    assert len(rows) == 1 and rows[0].token_hash != token and len(rows[0].token_hash) == 64


def test_logout_invalidates_session(auth):
    assert auth.get("/api/auth/me").status_code == 200
    auth.post("/api/auth/logout")
    assert auth.get("/api/auth/me").status_code == 401


def test_writes_require_csrf_header(auth):
    del auth.headers["X-GoldPilot"]
    assert auth.post("/api/engine/mode", json={"mode": "pause"}).status_code == 403
    auth.headers["X-GoldPilot"] = "1"
    assert auth.post("/api/engine/mode", json={"mode": "pause"}).status_code == 200
    with db.session() as s:
        assert db.kv_get(s, "user_mode") == "pause"


def test_security_headers(client):
    r = client.get("/api/health")
    assert r.headers["x-frame-options"] == "DENY"
    assert "frame-ancestors 'none'" in r.headers["content-security-policy"]
    assert r.headers["cache-control"] == "no-store"
    assert r.headers["x-content-type-options"] == "nosniff"


def test_dashboard_never_green_when_components_down(auth):
    d = auth.get("/api/dashboard").json()
    st = d["statut"]
    assert st["connexion"]["ok"] is False
    assert st["donnees"]["ok"] is False
    assert st["moteur"]["ok"] is False and st["moteur"]["etat"] == "arrete"
    assert st["notifications"]["ok"] is False and st["notifications"]["texte"] == "Telegram non configuré"
    assert d["trading"]["strategie"]["validee"] is False
    assert d["marche"]["contrat"].startswith("MGC")


def test_dashboard_green_only_with_live_engine_and_fresh_data(auth):
    with db.session() as s:
        db.beat(s, "engine", "actif", {"clock": None})
        db.kv_set(s, "engine_mode", {"mode": "actif", "problemes": [], "qualite": "ok"})
    st = auth.get("/api/dashboard").json()["statut"]
    assert st["connexion"]["ok"] and st["donnees"]["ok"] and st["moteur"]["ok"]
    with db.session() as s:
        db.kv_set(s, "engine_mode", {"mode": "securise", "problemes": ["données périmées"], "qualite": "bloquant"})
    st = auth.get("/api/dashboard").json()["statut"]
    assert not st["donnees"]["ok"] and "périmées" in st["donnees"]["texte"]
    assert not st["moteur"]["ok"] and st["moteur"]["texte"].startswith("Mode sécurisé")


RISK = {"risk_per_trade_usd": 200, "max_cushion_fraction": 0.2, "daily_loss_stop_usd": 400, "max_trades_per_day": 3,
        "max_losses_per_day": 2, "consistency_lock_fraction": 0.8, "safety_margin_usd": 100, "slippage_allowance_oz": 0.3,
        "commission_per_contract_rt": 2.0, "max_contracts_personal": 10}


def test_risk_settings_validation(auth):
    assert auth.put("/api/settings/risk", json=RISK).status_code == 200
    assert auth.get("/api/settings").json()["risque"]["risk_per_trade_usd"] == 200
    bad = dict(RISK, risk_per_trade_usd=5000)
    r = auth.put("/api/settings/risk", json=bad)
    assert r.status_code == 422 and "Risque par trade" in r.json()["detail"]
    assert auth.put("/api/settings/risk", json=dict(RISK, inconnu=1)).status_code == 422
    assert auth.put("/api/settings/risk", json=dict(RISK, max_trades_per_day="beaucoup")).status_code == 422
    assert auth.put("/api/settings/risk", json=dict(RISK, max_contracts_personal=31)).status_code == 422
    with db.session() as s:
        audits = [a for a in s.execute(select(db.Audit).where(db.Audit.action == "parametres_risque")).scalars()]
    assert len(audits) == 1


def test_program_must_exist(auth):
    assert auth.put("/api/settings/program", json={"programme": "inexistant"}).status_code == 422
    assert auth.put("/api/settings/program", json={"programme": "flex_50k_funded"}).status_code == 200


def test_real_mode_locked_while_strategy_not_validated(auth):
    r = auth.put("/api/settings/trading-mode", json={"mode": "reel", "confirmation": "JE CONFIRME LE PASSAGE EN REEL"})
    assert r.status_code == 409 and "critères de validation" in r.json()["detail"]
    with db.session() as s:
        assert db.kv_get(s, "trading_mode", "simulation") == "simulation"


def test_real_mode_requires_fundednext_confirmation_and_exact_phrase(auth, monkeypatch):
    conf = dict(strategy_config.load_production(), validated=True)
    monkeypatch.setattr(strategy_config, "load_production", lambda: conf)
    r = auth.put("/api/settings/trading-mode", json={"mode": "reel", "confirmation": "JE CONFIRME LE PASSAGE EN REEL"})
    assert r.status_code == 409 and "FundedNext" in r.json()["detail"]
    assert auth.put("/api/settings/fundednext-confirmation", json={"confirme": True}).status_code == 422
    assert auth.put("/api/settings/fundednext-confirmation", json={"confirme": True, "reference": "ticket 12345"}).status_code == 200
    assert auth.put("/api/settings/trading-mode", json={"mode": "reel", "confirmation": "oui"}).status_code == 422
    assert auth.put("/api/settings/trading-mode", json={"mode": "reel", "confirmation": "JE CONFIRME LE PASSAGE EN REEL"}).status_code == 200
    # retirer la confirmation ramène immédiatement en simulation
    assert auth.put("/api/settings/fundednext-confirmation", json={"confirme": False}).status_code == 200
    with db.session() as s:
        assert db.kv_get(s, "trading_mode") == "simulation"


def _signal(**kw) -> str:
    base = dict(key="v:1:1", created_at=utc(2026, 10, 9, 13, 0, 5), mode="simulation", validated=False, strategy_version="v",
                symbol="MGCZ2026", side=1, entry_type="market", entry_ref=4000.0, entry_max_drift=2.0, stop=3990.0, target=None,
                trail_atr=3.0, atr=4.0, contracts=2, risk_usd=210.0, reward_risk=None, valid_until=utc(2026, 10, 9, 13, 30),
                exit_deadline=utc(2026, 10, 9, 19, 30), rationale="r", invalidation="i", calendar_note="c", price_source="TradingView",
                price_ts=utc(2026, 10, 9, 13, 0), status="ACTIF", meta={"decision_bar_ts": 0, "td": 1, "exit_msess": 1290, "tag": "ext_long"})
    base.update(kw)
    with db.session() as s:
        sig = db.Signal(**base)
        s.add(sig)
        s.flush()
        return sig.id


def test_declared_execution_is_labelled_and_pnl_computed(auth):
    sid = _signal()
    r = auth.post(f"/api/signals/{sid}/execution", json={"executee": True, "entree": 4001.0, "sortie": 4011.0, "contrats": 2})
    assert r.status_code == 200
    d = auth.get(f"/api/signals/{sid}").json()
    assert d["signal"]["execution_declaree"]["pnl_usd"] == 200.0  # 10 $ × 10 onces × 2 contrats
    assert any(e["type"] == "execution_declaree" for e in d["evenements"])
    assert auth.post(f"/api/signals/{sid}/execution", json={"executee": True, "contrats": 31}).status_code == 422
    assert auth.post("/api/signals/inconnu/execution", json={"executee": False}).status_code == 404


def test_cancel_only_before_simulated_entry(auth):
    sid = _signal(key="v:2:1", status="EN_ATTENTE", entry_type="stop")
    assert auth.post(f"/api/signals/{sid}/cancel").status_code == 200
    assert auth.get(f"/api/signals/{sid}").json()["signal"]["statut"] == "ANNULE"
    assert auth.post(f"/api/signals/{sid}/cancel").status_code == 400
    sid2 = _signal(key="v:3:1", sim_entry=4000.5, sim_entry_ts=utc(2026, 10, 9, 13, 15))
    r = auth.post(f"/api/signals/{sid2}/cancel")
    assert r.status_code == 400 and "déjà ouverte" in r.json()["detail"]


def test_signal_list_filter(auth):
    _signal(key="a", status="CLOTURE")
    _signal(key="b", status="ACTIF")
    assert len(auth.get("/api/signals").json()["signaux"]) == 2
    assert [x["statut"] for x in auth.get("/api/signals?statut=ACTIF").json()["signaux"]] == ["ACTIF"]


def test_journal_types(auth):
    for t in ("decisions", "incidents", "notifications", "webhooks", "controle", "audit"):
        assert auth.get(f"/api/journal?type={t}").status_code == 200, t
    assert auth.get("/api/journal?type=secret").status_code == 422


def test_stats_contains_research_and_execution_quality(auth):
    d = auth.get("/api/stats").json()
    assert d["production"]["validated"] is False
    assert d["selection"] is not None and d["test_final"] is not None and d["monte_carlo"] is not None
    assert d["execution"]["signaux"] == 0 and d["paper"] is None


def test_manual_calendar_event_requires_timezone(auth):
    assert auth.post("/api/calendar", json={"titre": "Discours Fed", "quand": "2026-10-20T14:00:00"}).status_code == 422
    assert auth.post("/api/calendar", json={"titre": "Discours Fed", "quand": "2026-10-20T14:00:00-04:00"}).status_code == 200
    with db.session() as s:
        e = s.execute(select(db.EconomicEvent).where(db.EconomicEvent.source == "manuel")).scalars().one()
    assert e.ts == utc(2026, 10, 20, 18, 0) and e.impact == "fort"


def test_account_declaration_validated(auth):
    assert auth.post("/api/account", json={"solde": -5}).status_code == 422
    assert auth.post("/api/account", json={"solde": 50250, "plus_haut_fin_de_jour": 50400}).status_code == 200


def test_pine_script_served(auth):
    r = auth.get("/api/setup/pine")
    assert r.status_code == 200 and "GoldPilot Bridge" in r.text and "//@version=6" in r.text


def test_test_notification_reports_missing_configuration(auth):
    r = auth.post("/api/notifications/test")
    assert r.status_code == 502 and "non configuré" in r.json()["detail"]


def test_settings_expose_no_secret(auth):
    txt = auth.get("/api/settings").text
    from .conftest import TV_TOKEN

    assert TV_TOKEN not in txt
    d = auth.get("/api/settings").json()
    assert d["tradingview"]["jeton_defini"] is True and d["tradingview"]["url_webhook"].endswith("/api/webhooks/tradingview")


def test_session_expiry(auth):
    with db.session() as s:
        for row in s.execute(select(db.LoginSession)).scalars():
            row.expires_at = db.now() - timedelta(seconds=1)
    assert auth.get("/api/auth/me").status_code == 401
