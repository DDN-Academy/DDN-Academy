"""Base de données (PostgreSQL en production, SQLite pour les tests). Horodatages toujours en UTC.

Le moteur et le site communiquent uniquement par ces tables. Les contraintes d'unicité garantissent
l'idempotence : une barre, un signal, une notification ne peuvent pas être enregistrés deux fois.
"""
from __future__ import annotations

import json
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from typing import Any, Iterator

from sqlalchemy import (
    JSON, Boolean, DateTime, Float, ForeignKey, Index, Integer, String, Text, UniqueConstraint, create_engine, select,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, sessionmaker
from sqlalchemy.types import TypeDecorator

from .config import settings


def now() -> datetime:
    return datetime.now(tz=timezone.utc)


def uid() -> str:
    return uuid.uuid4().hex


class UTC(TypeDecorator):
    impl = DateTime(timezone=True)
    cache_ok = True

    def process_bind_param(self, v, dialect):
        if v is None:
            return None
        if v.tzinfo is None:
            raise ValueError("datetime sans fuseau refusé")
        return v.astimezone(timezone.utc)

    def process_result_value(self, v, dialect):
        if v is None:
            return None
        return v.replace(tzinfo=timezone.utc) if v.tzinfo is None else v.astimezone(timezone.utc)


class Base(DeclarativeBase):
    pass


class KV(Base):
    """Paramètres et état persistants (mode du moteur, réglages de risque, programme, état du compte…)."""

    __tablename__ = "kv"
    key: Mapped[str] = mapped_column(String(64), primary_key=True)
    value: Mapped[Any] = mapped_column(JSON)
    updated_at: Mapped[datetime] = mapped_column(UTC(), default=now, onupdate=now)


class Bar(Base):
    __tablename__ = "bars"
    __table_args__ = (UniqueConstraint("source", "symbol", "ts", name="uq_bar"), Index("ix_bars_symbol_ts", "symbol", "ts"))
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String(24))
    symbol: Mapped[str] = mapped_column(String(32))  # ex. MGCZ2026
    ts: Mapped[datetime] = mapped_column(UTC())  # début de la barre
    minutes: Mapped[int] = mapped_column(Integer, default=1)  # durée de la barre (1 en direct, 5 en rejeu)
    open: Mapped[float] = mapped_column(Float)
    high: Mapped[float] = mapped_column(Float)
    low: Mapped[float] = mapped_column(Float)
    close: Mapped[float] = mapped_column(Float)
    volume: Mapped[float] = mapped_column(Float, default=0.0)
    received_at: Mapped[datetime] = mapped_column(UTC(), default=now)
    processed: Mapped[bool] = mapped_column(Boolean, default=False, index=True)


class DailyBar(Base):
    """Historique journalier (amplitude des journées passées), envoyé par TradingView (MGC continu)."""

    __tablename__ = "daily_bars"
    __table_args__ = (UniqueConstraint("source", "td", name="uq_daily"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String(24))
    symbol: Mapped[str] = mapped_column(String(32))
    td: Mapped[int] = mapped_column(Integer, index=True)  # journée de trading, jours depuis 1970
    high: Mapped[float] = mapped_column(Float)
    low: Mapped[float] = mapped_column(Float)
    close: Mapped[float] = mapped_column(Float)
    received_at: Mapped[datetime] = mapped_column(UTC(), default=now)


class Decision(Base):
    """Chaque analyse à la clôture d'une barre de décision : trade ou absence de trade, avec les raisons."""

    __tablename__ = "decisions"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(UTC(), default=now, index=True)
    bar_ts: Mapped[datetime] = mapped_column(UTC(), index=True)
    strategy_version: Mapped[str] = mapped_column(String(80))
    outcome: Mapped[str] = mapped_column(String(16))  # aucun_setup | refuse | signal | suspendu
    summary: Mapped[str] = mapped_column(Text)
    reasons: Mapped[Any] = mapped_column(JSON, default=list)
    context: Mapped[Any] = mapped_column(JSON, default=dict)
    risk_checks: Mapped[Any] = mapped_column(JSON, default=list)
    signal_id: Mapped[str | None] = mapped_column(String(32), nullable=True)


class Signal(Base):
    __tablename__ = "signals"
    id: Mapped[str] = mapped_column(String(32), primary_key=True, default=uid)
    key: Mapped[str] = mapped_column(String(160), unique=True)  # clé d'idempotence
    created_at: Mapped[datetime] = mapped_column(UTC(), default=now, index=True)
    mode: Mapped[str] = mapped_column(String(12))  # simulation | reel
    validated: Mapped[bool] = mapped_column(Boolean, default=False)
    strategy_version: Mapped[str] = mapped_column(String(80))
    symbol: Mapped[str] = mapped_column(String(32))
    side: Mapped[int] = mapped_column(Integer)
    entry_type: Mapped[str] = mapped_column(String(12))
    entry_ref: Mapped[float] = mapped_column(Float)
    entry_max_drift: Mapped[float] = mapped_column(Float)
    stop: Mapped[float] = mapped_column(Float)
    target: Mapped[float | None] = mapped_column(Float, nullable=True)
    trail_atr: Mapped[float | None] = mapped_column(Float, nullable=True)
    atr: Mapped[float] = mapped_column(Float)
    contracts: Mapped[int] = mapped_column(Integer)
    risk_usd: Mapped[float] = mapped_column(Float)
    reward_risk: Mapped[float | None] = mapped_column(Float, nullable=True)
    valid_until: Mapped[datetime] = mapped_column(UTC())
    exit_deadline: Mapped[datetime] = mapped_column(UTC())
    rationale: Mapped[str] = mapped_column(Text)
    invalidation: Mapped[str] = mapped_column(Text)
    calendar_note: Mapped[str] = mapped_column(Text, default="")
    price_source: Mapped[str] = mapped_column(String(40))
    price_ts: Mapped[datetime] = mapped_column(UTC())
    status: Mapped[str] = mapped_column(String(12), index=True)  # EN_ATTENTE | ACTIF | ANNULE | EXPIRE | CLOTURE
    status_reason: Mapped[str] = mapped_column(Text, default="")
    sim_entry_ts: Mapped[datetime | None] = mapped_column(UTC(), nullable=True)
    sim_entry: Mapped[float | None] = mapped_column(Float, nullable=True)
    sim_stop: Mapped[float | None] = mapped_column(Float, nullable=True)
    sim_exit_ts: Mapped[datetime | None] = mapped_column(UTC(), nullable=True)
    sim_exit: Mapped[float | None] = mapped_column(Float, nullable=True)
    sim_exit_reason: Mapped[str | None] = mapped_column(String(40), nullable=True)
    sim_r: Mapped[float | None] = mapped_column(Float, nullable=True)
    sim_pnl_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    user_executed: Mapped[bool | None] = mapped_column(Boolean, nullable=True)
    user_entry: Mapped[float | None] = mapped_column(Float, nullable=True)
    user_exit: Mapped[float | None] = mapped_column(Float, nullable=True)
    user_contracts: Mapped[int | None] = mapped_column(Integer, nullable=True)
    user_pnl_usd: Mapped[float | None] = mapped_column(Float, nullable=True)
    user_note: Mapped[str] = mapped_column(Text, default="")
    meta: Mapped[Any] = mapped_column(JSON, default=dict)


class SignalEvent(Base):
    __tablename__ = "signal_events"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    signal_id: Mapped[str] = mapped_column(String(32), ForeignKey("signals.id"), index=True)
    ts: Mapped[datetime] = mapped_column(UTC(), default=now)
    kind: Mapped[str] = mapped_column(String(32))
    detail: Mapped[Any] = mapped_column(JSON, default=dict)


class Notification(Base):
    __tablename__ = "notifications"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(UTC(), default=now, index=True)
    key: Mapped[str] = mapped_column(String(200), unique=True)
    kind: Mapped[str] = mapped_column(String(32))
    signal_id: Mapped[str | None] = mapped_column(String(32), nullable=True)
    text: Mapped[str] = mapped_column(Text)
    status: Mapped[str] = mapped_column(String(12))  # a_envoyer | envoye | echec | desactive
    attempts: Mapped[int] = mapped_column(Integer, default=0)
    error: Mapped[str] = mapped_column(Text, default="")
    sent_at: Mapped[datetime | None] = mapped_column(UTC(), nullable=True)


class Incident(Base):
    __tablename__ = "incidents"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(UTC(), default=now, index=True)
    severity: Mapped[str] = mapped_column(String(12))  # info | alerte | critique
    component: Mapped[str] = mapped_column(String(24))
    code: Mapped[str] = mapped_column(String(48))
    message: Mapped[str] = mapped_column(Text)
    resolved_at: Mapped[datetime | None] = mapped_column(UTC(), nullable=True)


class EconomicEvent(Base):
    __tablename__ = "economic_events"
    __table_args__ = (UniqueConstraint("source", "uid", name="uq_econ"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    source: Mapped[str] = mapped_column(String(24))
    uid: Mapped[str] = mapped_column(String(200))
    title: Mapped[str] = mapped_column(String(300))
    impact: Mapped[str] = mapped_column(String(8))  # fort | moyen | faible
    ts: Mapped[datetime] = mapped_column(UTC(), index=True)
    source_url: Mapped[str] = mapped_column(String(300), default="")
    fetched_at: Mapped[datetime] = mapped_column(UTC(), default=now)


class WebhookLog(Base):
    __tablename__ = "webhook_log"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    received_at: Mapped[datetime] = mapped_column(UTC(), default=now, index=True)
    ip: Mapped[str] = mapped_column(String(64))
    kind: Mapped[str] = mapped_column(String(16))
    accepted: Mapped[bool] = mapped_column(Boolean)
    reason: Mapped[str] = mapped_column(Text, default="")
    payload: Mapped[Any] = mapped_column(JSON, default=dict)


class MirrorSignal(Base):
    """Signal calculé côté TradingView par le script Pine (contrôle croisé, jamais décisionnel)."""

    __tablename__ = "mirror_signals"
    __table_args__ = (UniqueConstraint("symbol", "bar_ts", "side", name="uq_mirror"),)
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    received_at: Mapped[datetime] = mapped_column(UTC(), default=now)
    symbol: Mapped[str] = mapped_column(String(32))
    bar_ts: Mapped[datetime] = mapped_column(UTC())
    side: Mapped[int] = mapped_column(Integer)
    price: Mapped[float] = mapped_column(Float)
    matched_signal_id: Mapped[str | None] = mapped_column(String(32), nullable=True)
    verdict: Mapped[str | None] = mapped_column(String(40), nullable=True)  # concordant | discordant | decision_absente
    checked_at: Mapped[datetime | None] = mapped_column(UTC(), nullable=True)


class AccountUpdate(Base):
    __tablename__ = "account_updates"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(UTC(), default=now, index=True)
    balance: Mapped[float] = mapped_column(Float)
    hwm_eod: Mapped[float | None] = mapped_column(Float, nullable=True)
    best_day: Mapped[float | None] = mapped_column(Float, nullable=True)
    note: Mapped[str] = mapped_column(Text, default="")


class Audit(Base):
    __tablename__ = "audit"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    ts: Mapped[datetime] = mapped_column(UTC(), default=now, index=True)
    actor: Mapped[str] = mapped_column(String(24))
    action: Mapped[str] = mapped_column(String(64))
    detail: Mapped[Any] = mapped_column(JSON, default=dict)


class LoginSession(Base):
    __tablename__ = "login_sessions"
    token_hash: Mapped[str] = mapped_column(String(64), primary_key=True)
    created_at: Mapped[datetime] = mapped_column(UTC(), default=now)
    expires_at: Mapped[datetime] = mapped_column(UTC())
    ip: Mapped[str] = mapped_column(String(64), default="")


class Heartbeat(Base):
    __tablename__ = "heartbeats"
    component: Mapped[str] = mapped_column(String(24), primary_key=True)
    ts: Mapped[datetime] = mapped_column(UTC(), default=now)
    status: Mapped[str] = mapped_column(String(16))
    detail: Mapped[Any] = mapped_column(JSON, default=dict)


_engine = None
_Session = None


def init(url: str | None = None, create: bool = False):
    """Initialise la connexion. En production, le schéma est créé par les migrations Alembic."""
    global _engine, _Session
    url = url or settings().database_url
    kw: dict = {"pool_pre_ping": True, "json_serializer": lambda o: json.dumps(o, default=str, ensure_ascii=False)}
    if url.startswith("sqlite"):
        from pathlib import Path

        p = url.replace("sqlite:///", "")
        if p and p != ":memory:":
            Path(p).parent.mkdir(parents=True, exist_ok=True)
        kw["connect_args"] = {"check_same_thread": False}
    _engine = create_engine(url, **kw)
    _Session = sessionmaker(bind=_engine, expire_on_commit=False)
    if create:
        Base.metadata.create_all(_engine)
    return _engine


def engine():
    if _engine is None:
        init()
    return _engine


@contextmanager
def session() -> Iterator[Session]:
    if _Session is None:
        init()
    s = _Session()
    try:
        yield s
        s.commit()
    except Exception:
        s.rollback()
        raise
    finally:
        s.close()


def kv_get(s: Session, key: str, default: Any = None) -> Any:
    r = s.get(KV, key)
    return default if r is None else r.value


def kv_set(s: Session, key: str, value: Any) -> None:
    r = s.get(KV, key)
    if r is None:
        s.add(KV(key=key, value=value))
    else:
        r.value = value
        r.updated_at = now()


def audit(s: Session, actor: str, action: str, detail: dict | None = None) -> None:
    s.add(Audit(actor=actor, action=action, detail=detail or {}))


def open_incident(s: Session, severity: str, component: str, code: str, message: str) -> bool:
    """Ouvre un incident s'il n'en existe pas déjà un identique non résolu. Renvoie True si nouveau."""
    ex = s.execute(select(Incident).where(Incident.component == component, Incident.code == code,
                                          Incident.resolved_at.is_(None))).scalars().first()
    if ex is not None:
        return False
    s.add(Incident(severity=severity, component=component, code=code, message=message))
    return True


def resolve_incident(s: Session, component: str, code: str) -> bool:
    rows = s.execute(select(Incident).where(Incident.component == component, Incident.code == code,
                                            Incident.resolved_at.is_(None))).scalars().all()
    for r in rows:
        r.resolved_at = now()
    return bool(rows)


def beat(s: Session, component: str, status: str, detail: dict | None = None) -> None:
    r = s.get(Heartbeat, component)
    if r is None:
        s.add(Heartbeat(component=component, status=status, detail=detail or {}, ts=now()))
    else:
        r.status, r.detail, r.ts = status, detail or {}, now()
