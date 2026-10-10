"""Fixtures communes : base SQLite temporaire, configuration de test, client HTTP de l'API."""
from __future__ import annotations

from datetime import datetime, timezone

import pytest

from goldpilot import db
from goldpilot.api import security
from goldpilot.config import settings
from goldpilot.engine import strategy_config

PASSWORD = "mot-de-passe-de-test"
_HASH = security.hash_password(PASSWORD)
TV_TOKEN = "jeton-webhook-de-test-0123456789abcdef"


@pytest.fixture
def env(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_ENV", "test")
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'test.db'}")
    monkeypatch.setenv("ADMIN_PASSWORD_HASH", _HASH)
    monkeypatch.setenv("TV_WEBHOOK_TOKEN", TV_TOKEN)
    monkeypatch.setenv("TV_ENFORCE_IP", "false")
    monkeypatch.setenv("DATA_SOURCE", "tradingview")
    monkeypatch.delenv("TELEGRAM_BOT_TOKEN", raising=False)
    monkeypatch.delenv("TELEGRAM_CHAT_ID", raising=False)
    monkeypatch.delenv("TRUST_PROXY", raising=False)
    settings.cache_clear()
    strategy_config.load_production.cache_clear()
    db.init(create=True)
    for lim in (security.login_limiter, security.webhook_limiter, security.api_limiter):
        lim.hits.clear()
    yield
    settings.cache_clear()
    getattr(strategy_config.load_production, "cache_clear", lambda: None)()  # peut être remplacée par un test


@pytest.fixture
def client(env):
    from fastapi.testclient import TestClient

    from goldpilot.api.app import app

    return TestClient(app)


@pytest.fixture
def auth(client):
    r = client.post("/api/auth/login", json={"password": PASSWORD})
    assert r.status_code == 200, r.text
    client.headers.update({"X-GoldPilot": "1"})
    return client


def utc(*a) -> datetime:
    return datetime(*a, tzinfo=timezone.utc)
