"""Simulateur d'exécution prudent — utilisé par le backtest ET par le suivi des positions simulées en production.

Règles (protocole, section 3) :
* entrée au marché : ouverture de la barre suivante + demi-spread ; toute la barre d'entrée est
  postérieure à l'entrée (stop touché si l'extrême défavorable l'atteint) ;
* entrée stop : au niveau (ou à l'ouverture en cas de gap) + demi-spread + glissement ; sur la barre
  d'entrée, stop supposé touché si l'extrême défavorable l'atteint (prudent) ;
* stop touché par un gap : sortie à l'ouverture ; stop et objectif dans la même barre : stop d'abord ;
* objectif (ordre limite) : le prix doit dépasser le niveau d'un tick ;
* sortie temporelle à l'ouverture de la première barre dont la minute de séance ≥ heure de sortie, ou
  dès que la journée de trading change ;
* commission déduite à la sortie.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

from ..strategy.base import Setup

TICK = 0.10


@dataclass(frozen=True)
class CostModel:
    """Coûts par once. mode « proportional » : fractions du prix ; mode « fixed » : dollars par once."""

    mode: str = "proportional"
    commission_rt: float = 0.20 / 4000
    half_spread: float = 0.05 / 4000
    stop_slip: float = 0.10 / 4000
    fast_slip: float = 0.30 / 4000
    fast_atr_mult: float = 3.0
    label: str = "base (proportionnel, calé sur MGC à 4 000 $)"

    def amount(self, component: str, price: float) -> float:
        v = getattr(self, component)
        return v * price if self.mode == "proportional" else v

    def scaled(self, k: float) -> "CostModel":
        return CostModel(self.mode, self.commission_rt * k, self.half_spread * k, self.stop_slip * k, self.fast_slip * k,
                         self.fast_atr_mult, f"{self.label} ×{k:g}")


BASE_COSTS = CostModel()
FIXED_COSTS = CostModel("fixed", 0.20, 0.05, 0.10, 0.30, 3.0, "fixes 0,50 $/oz aller-retour (stress historique)")
ZERO_COSTS = CostModel("fixed", 0, 0, 0, 0, 3.0, "sans coûts")


@dataclass
class OpenPosition:
    setup: Setup
    side: int
    entry_px: float
    entry_ts: int
    stop: float
    initial_stop: float
    target: float | None
    extreme: float
    bars: int = 0


@dataclass
class Trade:
    strategy: str
    config_id: str
    tag: str
    side: int
    td: int
    decision_ts: int
    entry_ts: int
    exit_ts: int
    planned_entry: float
    entry_px: float
    exit_px: float
    initial_stop: float
    planned_risk: float
    exit_reason: str
    pnl_oz: float  # net de tous les coûts, $ par once
    r: float  # en multiples du risque prévu
    bars: int
    entry_slip: float  # défavorable > 0
    meta: dict = field(default_factory=dict)


@dataclass
class Event:
    kind: str  # fill | exit | expire | cancel
    setup: Setup
    ts: int
    price: float | None = None
    reason: str = ""
    trade: Trade | None = None


DELAY_PRICES = ("interpole", "pire")


class ExecutionSimulator:
    def __init__(self, costs: CostModel = BASE_COSTS, entry_delay_ns: int = 0, exec_bar_ns: int | None = None,
                 delay_price: str = "interpole"):
        """`entry_delay_ns` (test de sensibilité, recherche uniquement ; 0 = comportement standard) : une entrée au
        marché n'a lieu qu'à décision + délai. Si une barre d'exécution (durée `exec_bar_ns`) commence exactement à
        cet instant ou après, entrée à son ouverture ; si l'instant tombe à l'intérieur d'une barre, le prix intrabarre
        est inconnu et estimé : « interpole » = ouverture + (clôture − ouverture) × fraction écoulée ;
        « pire » = extrême défavorable de la barre (borne prudente). Demi-spread ajouté dans les deux cas."""
        if entry_delay_ns and (not exec_bar_ns or delay_price not in DELAY_PRICES):
            raise ValueError("entry_delay_ns exige exec_bar_ns et delay_price ∈ " + str(DELAY_PRICES))
        self.entry_delay_ns = int(entry_delay_ns)
        self.exec_bar_ns = exec_bar_ns
        self.delay_price = delay_price
        self.costs = costs
        self.pending: list[Setup] = []
        self.position: OpenPosition | None = None
        self.trades: list[Trade] = []
        self.tags_by_td: dict[int, set[str]] = {}
        self.entries_by_td: dict[int, int] = {}

    def submit(self, s: Setup) -> None:
        self.pending.append(s)

    def cancel_pending(self, ts: int, reason: str) -> list[Event]:
        ev = [Event("cancel", s, ts, reason=reason) for s in self.pending]
        self.pending = []
        return ev

    # -------------------------------------------------------------- coûts
    def _slip(self, px: float, h: float, l: float, atr: float) -> float:
        fast = np.isfinite(atr) and atr > 0 and (h - l) > self.costs.fast_atr_mult * atr
        return self.costs.amount("fast_slip" if fast else "stop_slip", px)

    def _fill(self, s: Setup, o: float, h: float, l: float, atr: float, ts: int | None = None, c: float | None = None) -> float | None:
        hs = self.costs.amount("half_spread", o)
        if s.entry_type == "market" and self.entry_delay_ns and ts is not None:
            target = s.decision_ts + self.entry_delay_ns
            if ts >= target:
                return o + s.side * hs
            if ts + self.exec_bar_ns <= target:
                return None  # délai pas encore écoulé
            if self.delay_price == "pire":
                base = h if s.side > 0 else l
            else:
                base = o + (c - o) * (target - ts) / self.exec_bar_ns
            return base + s.side * self.costs.amount("half_spread", base)
        if s.entry_type == "market":
            return o + s.side * hs
        p = s.entry
        if s.entry_type == "stop":
            if s.side > 0 and (o >= p or h >= p):
                base = max(o, p)
                return base + hs + self._slip(base, h, l, atr)
            if s.side < 0 and (o <= p or l <= p):
                base = min(o, p)
                return base - hs - self._slip(base, h, l, atr)
            return None
        if s.entry_type == "limit":
            if s.side > 0 and l <= p - TICK:
                return min(o, p)
            if s.side < 0 and h >= p + TICK:
                return max(o, p)
            return None
        raise ValueError(s.entry_type)

    def _close(self, ts: int, px: float, reason: str) -> Trade:
        p = self.position
        s = p.setup
        gross = (px - p.entry_px) * p.side
        net = gross - self.costs.amount("commission_rt", p.entry_px)
        risk = s.planned_risk
        t = Trade(s.strategy, s.config_id, s.tag, p.side, s.td, s.decision_ts, p.entry_ts, ts, s.planned_entry, p.entry_px, px,
                  p.initial_stop, risk, reason, net, net / risk if risk > 0 else 0.0, p.bars,
                  (p.entry_px - s.planned_entry) * p.side, dict(s.meta))
        self.trades.append(t)
        self.position = None
        return t

    def _stop_px(self, base: float, h: float, l: float, atr: float) -> float:
        p = self.position
        adj = self.costs.amount("half_spread", base) + self._slip(base, h, l, atr)
        return base - adj if p.side > 0 else base + adj

    # -------------------------------------------------------------- barre
    def on_bar(self, ts: int, o: float, h: float, l: float, c: float, atr: float, td: int, msess: int) -> list[Event]:
        ev: list[Event] = []
        exited = False
        p = self.position
        if p is not None:
            s = p.setup
            if td != s.td or msess >= s.exit_msess:
                px = o - p.side * self.costs.amount("half_spread", o)
                ev.append(Event("exit", s, ts, px, "sortie temporelle", self._close(ts, px, "sortie temporelle")))
                exited = True
            elif (o <= p.stop) if p.side > 0 else (o >= p.stop):
                px = self._stop_px(o, h, l, atr)
                ev.append(Event("exit", s, ts, px, "stop (gap)", self._close(ts, px, "stop (gap)")))
                exited = True
            else:
                hit_stop = (l <= p.stop) if p.side > 0 else (h >= p.stop)
                hit_tgt = p.target is not None and ((h >= p.target + TICK) if p.side > 0 else (l <= p.target - TICK))
                if hit_stop:
                    reason = "stop suiveur" if p.stop != p.initial_stop else "stop"
                    px = self._stop_px(p.stop, h, l, atr)
                    ev.append(Event("exit", s, ts, px, reason, self._close(ts, px, reason)))
                    exited = True
                elif hit_tgt:
                    ev.append(Event("exit", s, ts, p.target, "objectif", self._close(ts, p.target, "objectif")))
                    exited = True
                else:
                    p.bars += 1
        if self.pending:
            keep: list[Setup] = []
            filled = False
            for s in self.pending:
                if ts >= s.valid_until_ts or td != s.td or msess >= s.exit_msess:
                    ev.append(Event("expire", s, ts, reason="validité écoulée"))
                    continue
                if filled or exited or self.position is not None:
                    keep.append(s)
                    continue
                px = self._fill(s, o, h, l, atr, ts, c) if self.entry_delay_ns else self._fill(s, o, h, l, atr)
                if px is None:
                    keep.append(s)
                    continue
                filled = True
                self.position = OpenPosition(s, s.side, px, ts, s.stop, s.stop, s.target, px)
                self.tags_by_td.setdefault(s.td, set()).add(s.tag)
                self.entries_by_td[s.td] = self.entries_by_td.get(s.td, 0) + 1
                ev.append(Event("fill", s, ts, px, "entrée"))
                # Barre d'entrée : stop touché si l'extrême défavorable l'atteint (prudent pour tous les types)
                pos = self.position
                if (l <= pos.stop) if pos.side > 0 else (h >= pos.stop):
                    spx = self._stop_px(pos.stop, h, l, atr)
                    ev.append(Event("exit", s, ts, spx, "stop (barre d'entrée)", self._close(ts, spx, "stop (barre d'entrée)")))
                elif pos.target is not None and s.entry_type == "market" and (
                        (h >= pos.target + TICK) if pos.side > 0 else (l <= pos.target - TICK)):
                    ev.append(Event("exit", s, ts, pos.target, "objectif", self._close(ts, pos.target, "objectif")))
                else:
                    pos.extreme = max(px, h) if pos.side > 0 else min(px, l)
            # un seul ordre peut être exécuté ; les autres ordres de même groupe sont annulés
            if filled:
                for s in keep:
                    ev.append(Event("cancel", s, ts, reason="une position a été ouverte"))
                keep = []
            self.pending = keep
        return ev

    def end_of_decision_bar(self, h: float, l: float, atr: float) -> None:
        """Mise à jour du stop suiveur à la clôture d'une barre de décision (effective dès la suivante)."""
        p = self.position
        if p is None or p.setup.trail_atr is None or not (np.isfinite(atr) and atr > 0):
            return
        if p.side > 0:
            p.extreme = max(p.extreme, h)
            p.stop = max(p.stop, p.extreme - p.setup.trail_atr * atr)
        else:
            p.extreme = min(p.extreme, l)
            p.stop = min(p.stop, p.extreme + p.setup.trail_atr * atr)
