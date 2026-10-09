"""Structures communes : intentions d'ordre, évaluation d'une barre, état visible par la stratégie."""
from __future__ import annotations

from dataclasses import dataclass, field

import pandas as pd

NS_MIN = 60 * 1_000_000_000


@dataclass
class Setup:
    """Intention d'ordre décidée à la clôture d'une barre ; exécutable uniquement sur les barres suivantes."""

    strategy: str
    config_id: str
    side: int  # +1 achat, -1 vente
    entry_type: str  # "market" | "stop" | "limit"
    entry: float | None  # niveau (None si au marché : ouverture de la barre suivante)
    stop: float
    target: float | None
    trail_atr: float | None
    atr: float
    ref_price: float  # clôture de la barre de décision
    decision_bar_ts: int  # ns UTC, début de la barre de décision
    decision_ts: int  # ns UTC, clôture de la barre de décision
    valid_until_ts: int  # ns UTC (exclusif) : l'entrée doit avoir lieu avant
    exit_msess: int  # sortie forcée à la première barre dont msess >= exit_msess
    td: int
    tag: str
    rationale: str
    invalidation: str
    max_price_drift_atr: float = 0.5  # écart toléré entre le prix au moment d'agir et l'entrée prévue
    meta: dict = field(default_factory=dict)

    @property
    def planned_entry(self) -> float:
        return self.entry if self.entry is not None else self.ref_price

    @property
    def planned_risk(self) -> float:
        return abs(self.planned_entry - self.stop)

    @property
    def reward_risk(self) -> float | None:
        if self.target is None or self.planned_risk <= 0:
            return None
        return abs(self.target - self.planned_entry) / self.planned_risk


@dataclass
class Evaluation:
    """Résultat de l'analyse d'une barre : contexte, setups éventuels, et raisons de ne pas trader."""

    bar_ts: int
    regime: str
    context: dict
    setups: list[Setup]
    no_trade_reasons: list[str]

    @property
    def has_setup(self) -> bool:
        return bool(self.setups)


@dataclass
class StrategyState:
    has_position: bool = False
    pending_tags: set = field(default_factory=set)
    tags_today: set = field(default_factory=set)
    trades_today: int = 0


def fmt(p: float) -> str:
    return f"{p:,.2f}".replace(",", " ")


def ts_ns(index: pd.DatetimeIndex, i: int) -> int:
    return int(index.asi8[i])
