"""Échéances du Micro Gold (MGC) : contrat actif à trader et dates de roll.

Règles CME (sources : spécifications MGC et règlement COMEX chapitre 113, vérifiés le 9 octobre 2026) :
* mois cotés : février, avril, juin, août, octobre, décembre ;
* mois actifs (liquidité) : février, avril, juin, août, octobre, décembre — octobre est un mois « lead » de l'or COMEX
  depuis la date de négociation du 12 janvier 2026 (CME Group, Special Executive Report SER#9637 du 9 décembre 2025,
  rappelé par SER#9637R du 9 juin 2026 : https://www.cmegroup.com/content/dam/cmegroup/notices/ser/2025/12/ser-9637.pdf).
  Le SER porte sur le Gold (GC) ; le règlement quotidien du Micro Gold (MGC) dérive de celui du GC, on applique donc la
  même séquence au MGC (vérifié par recherche web le 11 octobre 2026, PDF officiel non consultable depuis l'environnement) ;
* fin de négociation : 3e dernier jour ouvré du mois de livraison ;
* premier jour d'avis (or COMEX) : dernier jour ouvré du mois précédant le mois de livraison.
Le volume migre vers l'échéance suivante avant le premier jour d'avis : on roule 5 jours ouvrés avant
(paramétrable). Le calendrier des jours fériés est une approximation du calendrier CME (une erreur d'un
jour est sans effet puisque le roll a lieu plusieurs jours avant le premier jour d'avis).
"""
from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from functools import lru_cache

CODES = "FGHJKMNQUVXZ"
ACTIVE_MONTHS = (2, 4, 6, 8, 10, 12)
ROLL_BDAYS = 5


def _easter(y: int) -> date:
    a, b, c = y % 19, y // 100, y % 100
    d, e = b // 4, b % 4
    f = (b + 8) // 25
    g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l_ = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l_) // 451
    return date(y, (h + l_ - 7 * m + 114) // 31, (h + l_ - 7 * m + 114) % 31 + 1)


def _nth(y: int, mo: int, wd: int, n: int) -> date:
    d = date(y, mo, 1)
    d += timedelta(days=(wd - d.weekday()) % 7)
    return d + timedelta(weeks=n - 1)


def _last(y: int, mo: int, wd: int) -> date:
    d = date(y + mo // 12, mo % 12 + 1, 1) - timedelta(days=1)
    return d - timedelta(days=(d.weekday() - wd) % 7)


def _obs(d: date) -> date:
    return d - timedelta(days=1) if d.weekday() == 5 else d + timedelta(days=1) if d.weekday() == 6 else d


@lru_cache(maxsize=32)
def holidays(y: int) -> frozenset[date]:
    return frozenset({_obs(date(y, 1, 1)), _nth(y, 1, 0, 3), _nth(y, 2, 0, 3), _easter(y) - timedelta(days=2),
                      _last(y, 5, 0), _obs(date(y, 6, 19)), _obs(date(y, 7, 4)), _nth(y, 9, 0, 1), _nth(y, 11, 3, 4),
                      _obs(date(y, 12, 25))})


def business_day(d: date) -> bool:
    return d.weekday() < 5 and d not in holidays(d.year)


def add_bdays(d: date, n: int) -> date:
    step = 1 if n > 0 else -1
    for _ in range(abs(n)):
        d += timedelta(days=step)
        while not business_day(d):
            d += timedelta(days=step)
    return d


def last_bday(y: int, mo: int) -> date:
    d = date(y + mo // 12, mo % 12 + 1, 1) - timedelta(days=1)
    while not business_day(d):
        d -= timedelta(days=1)
    return d


@dataclass(frozen=True)
class Contract:
    year: int
    month: int
    root: str = "MGC"

    @property
    def code(self) -> str:
        """Ex. MGCZ2026 (TradingView : COMEX:MGCZ2026)."""
        return f"{self.root}{CODES[self.month - 1]}{self.year}"

    @property
    def short_code(self) -> str:
        """Ex. MGCZ6 (Tradovate)."""
        return f"{self.root}{CODES[self.month - 1]}{self.year % 10}"

    @property
    def tradingview(self) -> str:
        return f"COMEX:{self.code}"

    @property
    def first_notice(self) -> date:
        y, mo = (self.year, self.month - 1) if self.month > 1 else (self.year - 1, 12)
        return last_bday(y, mo)

    @property
    def last_trade(self) -> date:
        return add_bdays(last_bday(self.year, self.month), -2)

    @property
    def roll_date(self) -> date:
        return add_bdays(self.first_notice, -ROLL_BDAYS)

    def label(self) -> str:
        mois = ["janvier", "février", "mars", "avril", "mai", "juin", "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
        return f"Micro Gold {mois[self.month - 1]} {self.year} ({self.short_code} sur Tradovate, {self.tradingview} sur TradingView)"


def active_contract(on: date) -> Contract:
    """Contrat à trader à la date `on` : premier mois actif dont la date de roll n'est pas atteinte."""
    for k in range(0, 24):
        y, mo = on.year + (on.month - 1 + k) // 12, (on.month - 1 + k) % 12 + 1
        if mo in ACTIVE_MONTHS:
            c = Contract(y, mo)
            if on < c.roll_date:
                return c
    raise RuntimeError("aucun contrat actif")


def next_contract(c: Contract) -> Contract:
    return active_contract(c.roll_date)


def parse_tv_symbol(sym: str) -> Contract | None:
    """'COMEX:MGCZ2026' ou 'MGCZ2026' → Contract ; None si ce n'est pas un contrat MGC daté."""
    s = sym.split(":")[-1].strip().upper()
    if not s.startswith("MGC") or len(s) != 8 or s[3] not in CODES or not s[4:].isdigit():
        return None
    return Contract(int(s[4:]), CODES.index(s[3]) + 1)
