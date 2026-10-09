"""Calendrier économique officiel et fenêtres de restriction autour des annonces.

Sources (vérifiées le 9 octobre 2026) :
* FOMC : https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm — communiqué 14:00, conférence 14:30 (New York).
* BLS (emploi, inflation) : fichier iCalendar officiel https://www.bls.gov/schedule/news_release/bls.ics
  (synchronisé automatiquement en production) ; dates d'octobre à décembre 2026 vérifiées sur
  https://www.bls.gov/schedule/2026/home.htm et intégrées ci-dessous en base de secours.
* BEA (PIB, PCE) : https://www.bea.gov/news/schedule (dates intégrées ; à compléter chaque trimestre).

Une annonce ne constitue jamais un signal : elle sert uniquement à bloquer les nouvelles entrées
pendant une fenêtre de prudence et à prévenir si une position simulée est ouverte.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from datetime import date, datetime, time, timedelta, timezone

from ..timeutil import NY

FOMC_URL = "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm"
BLS_URL = "https://www.bls.gov/schedule/2026/home.htm"
BLS_ICS = "https://www.bls.gov/schedule/news_release/bls.ics"
BEA_URL = "https://www.bea.gov/news/schedule"

FOMC_DECISION_DAYS = [
    "2026-01-28", "2026-03-18", "2026-04-29", "2026-06-17", "2026-07-29", "2026-09-16", "2026-10-28", "2026-12-09",
    "2027-01-27", "2027-03-17", "2027-04-28", "2027-06-09", "2027-07-28", "2027-09-15", "2027-10-27", "2027-12-08",
]
BLS_SEED = [
    ("2026-10-02", "Emploi américain (NFP) — septembre 2026"),
    ("2026-10-14", "Inflation CPI — septembre 2026"),
    ("2026-11-06", "Emploi américain (NFP) — octobre 2026"),
    ("2026-11-10", "Inflation CPI — octobre 2026"),
    ("2026-12-04", "Emploi américain (NFP) — novembre 2026"),
    ("2026-12-10", "Inflation CPI — novembre 2026"),
]
BEA_SEED = [
    ("2026-10-29", "PIB T3 2026 (estimation avancée) et dépenses PCE de septembre"),
    ("2026-11-25", "PIB T3 2026 (2e estimation) et dépenses PCE d'octobre"),
    ("2026-12-23", "Dépenses et inflation PCE de novembre"),
]

HIGH = ("employment situation", "consumer price index", "nfp", "cpi", "fomc", "pib", "gdp", "pce", "personal income")
MEDIUM = ("producer price index", "job openings", "employment cost index", "jolts", "retail")


@dataclass(frozen=True)
class Event:
    source: str
    uid: str
    title: str
    impact: str  # fort | moyen | faible
    ts: datetime
    source_url: str


def ny(d: str, hh: int, mm: int) -> datetime:
    y, m, dd = map(int, d.split("-"))
    return datetime.combine(date(y, m, dd), time(hh, mm), tzinfo=NY).astimezone(timezone.utc)


def impact_of(title: str) -> str:
    t = title.lower()
    if any(k in t for k in HIGH):
        return "fort"
    if any(k in t for k in MEDIUM):
        return "moyen"
    return "faible"


def seed_events() -> list[Event]:
    ev = []
    for d in FOMC_DECISION_DAYS:
        ev.append(Event("fed", f"fomc-{d}", "Décision de taux FOMC (communiqué)", "fort", ny(d, 14, 0), FOMC_URL))
        ev.append(Event("fed", f"fomc-pc-{d}", "Conférence de presse du président de la Fed", "fort", ny(d, 14, 30), FOMC_URL))
    for d, t in BLS_SEED:
        ev.append(Event("bls", f"seed-{d}", t, "fort", ny(d, 8, 30), BLS_URL))
    for d, t in BEA_SEED:
        ev.append(Event("bea", f"seed-{d}", t, "fort", ny(d, 8, 30), BEA_URL))
    return ev


_DT = re.compile(r"^DTSTART(?:;TZID=([^:;]+))?(?:;VALUE=DATE)?:(\d{8})(?:T(\d{4,6}))?(Z)?", re.M)


def parse_ics(text: str) -> list[Event]:
    """Analyse minimale d'un fichier iCalendar BLS (VEVENT : DTSTART, SUMMARY, UID)."""
    out = []
    for block in text.split("BEGIN:VEVENT")[1:]:
        block = block.split("END:VEVENT")[0].replace("\r\n ", "").replace("\n ", "")
        m = _DT.search(block)
        s = re.search(r"^SUMMARY[^:]*:(.+)$", block, re.M)
        u = re.search(r"^UID[^:]*:(.+)$", block, re.M)
        if not m or not s:
            continue
        tzid, d, hm, z = m.groups()
        title = s.group(1).strip().replace("\\,", ",")
        if hm is None:
            hh, mm = 8, 30  # événement « journée » : heure de publication BLS standard
        else:
            hh, mm = int(hm[:2]), int(hm[2:4])
        day = date(int(d[:4]), int(d[4:6]), int(d[6:8]))
        tz = timezone.utc if z else NY
        ts = datetime.combine(day, time(hh, mm), tzinfo=tz).astimezone(timezone.utc)
        out.append(Event("bls", (u.group(1).strip() if u else f"{d}-{title}")[:200], title[:300], impact_of(title), ts, BLS_ICS))
    return out


@dataclass(frozen=True)
class Blackout:
    before: timedelta = timedelta(minutes=10)
    after: timedelta = timedelta(minutes=15)


def blocking_event(events: list[Event], at: datetime, horizon: timedelta, bo: Blackout = Blackout()) -> Event | None:
    """Premier événement à fort impact dont la fenêtre [t − avant, t + après] chevauche [at, at + horizon]."""
    for e in sorted(events, key=lambda x: x.ts):
        if e.impact != "fort":
            continue
        if e.ts - bo.before <= at + horizon and at <= e.ts + bo.after:
            return e
    return None


def next_event(events: list[Event], at: datetime, min_impact: str = "fort") -> Event | None:
    order = {"fort": 2, "moyen": 1, "faible": 0}
    nxt = [e for e in events if e.ts >= at and order[e.impact] >= order[min_impact]]
    return min(nxt, key=lambda e: e.ts) if nxt else None
