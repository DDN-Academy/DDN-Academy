"""Temps : stockage en UTC, règles de marché exprimées en heure de New York (changements d'heure inclus).

Repères :
* journée de trading CME : 18:00 New York (veille) → 17:00 New York ; pause 17:00-18:00 ;
* FundedNext Futures : positions fermées au plus tard à 15:10 CT = 16:10 New York ;
* « minute de séance » (msess) : minutes écoulées depuis 18:00 New York (0 → 1379).
"""
from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone
from zoneinfo import ZoneInfo

UTC = timezone.utc
NY = ZoneInfo("America/New_York")
CT = ZoneInfo("America/Chicago")
PARIS = ZoneInfo("Europe/Paris")

SESSION_START_NY = 18 * 60  # 18:00
FUNDEDNEXT_FLAT_NY = time(16, 10)


def utcnow() -> datetime:
    return datetime.now(tz=UTC)


def require_aware(dt: datetime) -> datetime:
    if dt.tzinfo is None:
        raise ValueError("datetime sans fuseau horaire refusé")
    return dt


def ny_minute(dt: datetime) -> int:
    n = require_aware(dt).astimezone(NY)
    return n.hour * 60 + n.minute


def msess(dt: datetime) -> int:
    """Minute de séance : 18:00 New York → 0, 08:30 → 870, 16:10 → 1330."""
    return (ny_minute(dt) - SESSION_START_NY) % 1440


def msess_of(hhmm: str) -> int:
    h, m = hhmm.split(":")
    return (int(h) * 60 + int(m) - SESSION_START_NY) % 1440


def trading_date(dt: datetime) -> date:
    """Date de la journée de trading CME à laquelle appartient l'instant dt."""
    return (require_aware(dt).astimezone(NY) + timedelta(hours=6)).date()


def session_bounds_utc(td: date) -> tuple[datetime, datetime]:
    """Début (18:00 NY la veille) et fin (17:00 NY) de la journée de trading td, en UTC."""
    start = datetime.combine(td - timedelta(days=1), time(18, 0), tzinfo=NY).astimezone(UTC)
    end = datetime.combine(td, time(17, 0), tzinfo=NY).astimezone(UTC)
    return start, end


def ny_time_on(td: date, hhmm: str) -> datetime:
    """Instant UTC correspondant à l'heure New York hhmm de la journée de trading td."""
    h, m = map(int, hhmm.split(":"))
    day = td - timedelta(days=1) if h * 60 + m >= SESSION_START_NY else td
    return datetime.combine(day, time(h, m), tzinfo=NY).astimezone(UTC)


def market_phase(dt: datetime) -> str:
    """Phase du marché CME de l'or (heure de New York)."""
    n = require_aware(dt).astimezone(NY)
    m = n.hour * 60 + n.minute
    wd = n.weekday()
    if wd == 5 or (wd == 6 and m < 18 * 60) or (wd == 4 and m >= 17 * 60):
        return "fermé (week-end)"
    if 17 * 60 <= m < 18 * 60:
        return "pause quotidienne"
    if m >= 18 * 60 or m < 3 * 60:
        return "Asie"
    if m < 8 * 60:
        return "Londres"
    if m < 12 * 60:
        return "New York (matin)"
    return "New York (après-midi)"


def is_open(dt: datetime) -> bool:
    return market_phase(dt) not in ("fermé (week-end)", "pause quotidienne")


def fmt_paris(dt: datetime) -> str:
    return require_aware(dt).astimezone(PARIS).strftime("%d/%m/%Y %H:%M") + " (heure de Paris)"


def fmt_ny(dt: datetime) -> str:
    return require_aware(dt).astimezone(NY).strftime("%H:%M") + " New York"
