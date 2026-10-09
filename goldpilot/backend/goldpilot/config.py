"""Configuration lue uniquement dans les variables d'environnement. Aucun secret dans le code ni dans Git.

La liste complète, commentée, est dans `deploy/.env.example`.
"""
from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TV_IPS = ("52.89.214.238", "34.212.75.30", "54.218.53.128", "52.32.178.7")


def _b(name: str, default: bool) -> bool:
    v = os.environ.get(name, "")
    return default if v == "" else v.strip().lower() in ("1", "true", "yes", "oui", "on")


@dataclass(frozen=True)
class Settings:
    app_env: str
    database_url: str
    secret_key: str
    admin_password_hash: str
    public_base_url: str
    trust_proxy: bool
    session_hours: int
    telegram_bot_token: str
    telegram_chat_id: str
    tv_webhook_token: str
    tv_ip_allowlist: tuple[str, ...]
    tv_enforce_ip: bool
    data_source: str  # tradingview | databento | replay
    databento_api_key: str
    replay_speed: float
    replay_from: str
    fred_api_key: str
    calendar_refresh_min: int
    frontend_dir: Path
    research_dir: Path
    log_level: str

    @property
    def production(self) -> bool:
        return self.app_env == "production"

    def startup_problems(self) -> list[str]:
        """En production, toute configuration dangereuse empêche le démarrage (message explicite)."""
        p = []
        if self.production:
            if len(self.secret_key) < 32:
                p.append("SECRET_KEY : au moins 32 caractères aléatoires (python -m goldpilot.cli secret).")
            if not self.admin_password_hash.startswith("scrypt$"):
                p.append("ADMIN_PASSWORD_HASH absent (python -m goldpilot.cli hash-password).")
            if not self.public_base_url.startswith("https://"):
                p.append("PUBLIC_BASE_URL doit commencer par https://")
            if not self.database_url.startswith("postgresql"):
                p.append("DATABASE_URL doit pointer vers PostgreSQL en production.")
            if self.data_source == "tradingview" and len(self.tv_webhook_token) < 24:
                p.append("TV_WEBHOOK_TOKEN : au moins 24 caractères aléatoires (python -m goldpilot.cli secret).")
            if self.data_source == "replay":
                p.append("DATA_SOURCE=replay (rejeu historique) est interdit en production.")
        return p


@lru_cache(maxsize=1)
def settings() -> Settings:
    e = os.environ.get
    ips = e("TV_IP_ALLOWLIST")
    return Settings(
        app_env=e("APP_ENV", "development"),
        database_url=e("DATABASE_URL", f"sqlite:///{ROOT / 'var' / 'goldpilot.db'}"),
        secret_key=e("SECRET_KEY", ""),
        admin_password_hash=e("ADMIN_PASSWORD_HASH", ""),
        public_base_url=e("PUBLIC_BASE_URL", "http://localhost:8000").rstrip("/"),
        trust_proxy=_b("TRUST_PROXY", False),
        session_hours=int(e("SESSION_HOURS", "12")),
        telegram_bot_token=e("TELEGRAM_BOT_TOKEN", ""),
        telegram_chat_id=e("TELEGRAM_CHAT_ID", ""),
        tv_webhook_token=e("TV_WEBHOOK_TOKEN", ""),
        tv_ip_allowlist=tuple(x.strip() for x in ips.split(",") if x.strip()) if ips else TV_IPS,
        tv_enforce_ip=_b("TV_ENFORCE_IP", True),
        data_source=e("DATA_SOURCE", "tradingview").lower(),
        databento_api_key=e("DATABENTO_API_KEY", ""),
        replay_speed=float(e("REPLAY_SPEED", "120")),
        replay_from=e("REPLAY_FROM", "2025-06-02"),
        fred_api_key=e("FRED_API_KEY", ""),
        calendar_refresh_min=int(e("CALENDAR_REFRESH_MIN", "360")),
        frontend_dir=Path(e("FRONTEND_DIR", str(ROOT / "frontend" / "dist"))),
        research_dir=Path(e("RESEARCH_DIR", str(ROOT / "research" / "output"))),
        log_level=e("LOG_LEVEL", "INFO"),
    )
