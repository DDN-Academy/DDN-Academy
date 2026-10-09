"""Contrôle de qualité des données de marché, appliqué avant toute décision.

Un problème « bloquant » fait passer le système en mode sécurisé (aucun signal, signaux en attente
annulés). Seuils volontairement prudents.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta

import numpy as np
import pandas as pd

from ..timeutil import is_open, trading_date
from .contracts import active_contract, parse_tv_symbol

STALE_AFTER = timedelta(minutes=3)
MAX_DELAY = timedelta(minutes=3)


@dataclass
class Quality:
    level: str  # ok | degrade | bloquant
    problems: list[str] = field(default_factory=list)
    last_bar_end: datetime | None = None
    last_price: float | None = None
    age_s: float | None = None
    median_delay_s: float | None = None
    symbol: str | None = None
    expected_symbol: str | None = None

    @property
    def ok(self) -> bool:
        return self.level == "ok"


def assess(bars: pd.DataFrame, now: datetime, delays_s: list[float] | None = None) -> Quality:
    """bars : barres d'une minute récentes (index UTC = début), colonnes open/high/low/close/symbol."""
    expected = active_contract(trading_date(now)).code
    q = Quality("ok", expected_symbol=expected)
    if bars.empty:
        q.level, q.problems = "bloquant", ["aucune donnée de marché reçue"]
        return q
    last = bars.index[-1].to_pydatetime() + timedelta(minutes=1)
    q.last_bar_end, q.last_price, q.symbol = last, float(bars["close"].iloc[-1]), str(bars["symbol"].iloc[-1])
    q.age_s = (now - last).total_seconds()
    blocking: list[str] = []
    degraded: list[str] = []
    if is_open(now) and now - last > STALE_AFTER:
        blocking.append(f"données périmées : dernière barre il y a {int(q.age_s // 60)} min")
    if parse_tv_symbol(q.symbol) is None or q.symbol != expected:
        blocking.append(f"contrat reçu {q.symbol} différent du contrat actif {expected} : changer le graphique TradingView")
    if delays_s:
        med = float(np.median(delays_s[-20:]))
        q.median_delay_s = med
        if med > MAX_DELAY.total_seconds():
            blocking.append(f"données en retard d'environ {int(med // 60)} min (forfait temps réel COMEX absent ?)")
    recent = bars[bars.index >= bars.index[-1] - pd.Timedelta(minutes=60)]
    if is_open(now) and len(recent) < 45 and len(bars) >= 60:
        degraded.append(f"données incomplètes : {len(recent)} barres sur la dernière heure (60 attendues)")
    if len(bars) >= 30:
        rng = (bars["high"] - bars["low"]).iloc[-200:]
        med_rng = float(rng[rng > 0].median()) if (rng > 0).any() else 0.0
        jumps = (bars["open"] - bars["close"].shift()).abs().iloc[-30:]
        if med_rng > 0 and float(jumps.max()) > 15 * med_rng:
            blocking.append(f"saut de prix anormal de {float(jumps.max()):.2f} $ entre deux barres")
    if blocking:
        q.level, q.problems = "bloquant", blocking + degraded
    elif degraded:
        q.level, q.problems = "degrade", degraded
    return q
