"""Temps : stockage en UTC, règles de marché exprimées en heure de New York (changements d'heure inclus).

Repères :
* journée de trading CME : 18:00 New York (veille) → 17:00 New York ; pause 17:00-18:00 ;
* FundedNext Futures : positions fermées au plus tard à 15:10 CT = 16:10 New York ;
* « minute de séance » (msess) : minutes écoulées depuis 18:00 New York (0 → 1379) ;
* jours fériés CME (métaux) : fermeture complète ou clôture anticipée, voir `metals_session_close`.
"""
from __future__ import annotations

from datetime import date, datetime, time, timedelta, timezone
from functools import lru_cache
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


# ------------------------------------------------------------------ jours fériés CME (métaux, CME Globex)
# Sources consultées le 11 octobre 2026 (le site cmegroup.com n'était pas joignable depuis l'environnement de
# développement ; recherche web uniquement) :
# * CME Group, « Holiday and Trading Hours » : https://www.cmegroup.com/trading-hours.html (calendriers 2026 et 2027) ;
# * CME Group, horaires de Thanksgiving 2023 (métaux : clôture 12:45 CT le lendemain de Thanksgiving) :
#   https://www.cmegroup.com/trading-hours/files/thanksgiving-day-2023.pdf ;
# * récapitulatifs tiers 2026 (non officiels, en partie contradictoires) : https://crosstrade.io/blog/cme-trading-hours-2026,
#   https://www.metrotrade.com/cme-holiday-trading-hours/ (Vendredi saint 3 avril 2026 : métaux fermés ; Juneteenth :
#   arrêt 12:00 CT).
# Règle appliquée (prudente) :
# * fermeture complète : Jour de l'an, Vendredi saint, Noël (dates observées) ;
# * arrêt anticipé à 12:00 CT = 13:00 New York : MLK, Presidents' Day, Memorial Day, Juneteenth, Independence Day,
#   Labor Day, Thanksgiving ;
# * clôture anticipée à 12:45 CT = 13:45 New York : lendemain de Thanksgiving et veille de Noël (si jour ouvré).
# À VÉRIFIER chaque année sur le calendrier officiel CME (publié environ deux semaines avant chaque fête) : les horaires
# exacts 2026-2027 n'ont pas pu être confirmés sur la page officielle ; un récapitulatif tiers indique une clôture
# anticipée le 1er janvier 2027 au lieu d'une fermeture (on retient la fermeture, plus prudente) ; quand Noël tombe un
# samedi (2027), le vendredi 24 est traité comme fermé et le jeudi 23 comme une séance normale (à vérifier).
EARLY_HALT_HOLIDAY = time(13, 0)  # 12:00 CT
EARLY_CLOSE_EVE = time(13, 45)  # 12:45 CT
REGULAR_CLOSE = time(17, 0)
HOLIDAY_SAFETY_MIN = 25  # aucune sortie prévue moins de 25 min avant la clôture réelle


def _cme_metals_calendar(y: int) -> dict[date, time | None]:
    """{journée de trading : heure de clôture New York (None = fermé toute la journée)} pour l'année y."""
    from .marketdata.contracts import _easter, _last, _nth, _obs  # import local : évite un cycle d'import

    cal: dict[date, time | None] = {}
    for d in (_nth(y, 1, 0, 3), _nth(y, 2, 0, 3), _last(y, 5, 0), _obs(date(y, 6, 19)), _obs(date(y, 7, 4)),
              _nth(y, 9, 0, 1), _nth(y, 11, 3, 4)):
        cal[d] = EARLY_HALT_HOLIDAY
    thanksgiving = _nth(y, 11, 3, 4)
    cal[thanksgiving + timedelta(days=1)] = EARLY_CLOSE_EVE
    xmas = _obs(date(y, 12, 25))
    eve = date(y, 12, 24)
    if eve.weekday() < 5 and eve != xmas:
        cal[eve] = EARLY_CLOSE_EVE
    new_year = _obs(date(y, 1, 1))
    for d in ((new_year,) if new_year.year == y else ()) + (_easter(y) - timedelta(days=2), xmas):
        # 1er janvier un samedi : pas de report au 31 décembre (séance normale supposée, à vérifier)
        cal[d] = None
    return cal


@lru_cache(maxsize=16)
def _calendar_cached(y: int) -> dict[date, time | None]:
    return _cme_metals_calendar(y)


def metals_session_close(td: date) -> time | None:
    """Heure de clôture New York de la journée de trading td : 17:00, clôture anticipée, ou None si fermée."""
    return _calendar_cached(td.year).get(td, REGULAR_CLOSE)


def session_close_ny(td: date) -> datetime | None:
    """Instant UTC de la clôture réelle (clôture anticipée ou 17:00 New York) ; None si la journée est fériée (fermée)."""
    t = metals_session_close(td)
    return None if t is None else datetime.combine(td, t, tzinfo=NY).astimezone(UTC)


def last_open_time(now: datetime) -> datetime:
    """Dernière ouverture du marché (18:00 New York, après la pause, le week-end ou un jour férié) au plus tard à now."""
    td = trading_date(require_aware(now))
    for k in range(0, 15):
        d = td - timedelta(days=k)
        if d.weekday() >= 5 or metals_session_close(d) is None:
            continue
        start = session_bounds_utc(d)[0]
        if start <= now:
            return start
    return session_bounds_utc(td)[0]


def market_phase(dt: datetime) -> str:
    """Phase du marché CME de l'or (heure de New York), jours fériés et clôtures anticipées compris."""
    n = require_aware(dt).astimezone(NY)
    m = n.hour * 60 + n.minute
    wd = n.weekday()
    if wd == 5 or (wd == 6 and m < 18 * 60) or (wd == 4 and m >= 17 * 60):
        return "fermé (week-end)"
    close = metals_session_close(trading_date(dt))
    if close is None:
        return "fermé (jour férié)"
    if close != REGULAR_CLOSE and close.hour * 60 + close.minute <= m < 17 * 60:
        return "fermé (clôture anticipée)"
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
    ph = market_phase(dt)
    return not ph.startswith("fermé") and ph != "pause quotidienne"


def fmt_paris(dt: datetime) -> str:
    return require_aware(dt).astimezone(PARIS).strftime("%d/%m/%Y %H:%M") + " (heure de Paris)"


def fmt_ny(dt: datetime) -> str:
    return require_aware(dt).astimezone(NY).strftime("%H:%M") + " New York"
