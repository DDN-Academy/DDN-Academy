"""Backtest événementiel : même séquence que le moteur temps réel.

Pour chaque barre de décision i :
1. barres d'exécution de la période de i (la barre i elle-même, ou ses barres plus fines) → simulateur ;
2. clôture de i : mise à jour du stop suiveur ;
3. la stratégie évalue la barre i avec les seules données ≤ i ; ses ordres valent à partir de i+1.
"""
from __future__ import annotations

from dataclasses import asdict

import numpy as np
import pandas as pd

from ..strategy.base import StrategyState
from ..strategy.indicators import time_columns
from .execution import BASE_COSTS, CostModel, ExecutionSimulator, Trade

BAR_NS = 15 * 60 * 1_000_000_000


def run(strategy, F: pd.DataFrame, costs: CostModel = BASE_COSTS, start=None, end=None,
        exec_bars: pd.DataFrame | None = None) -> pd.DataFrame:
    idx = F.index.asi8
    i0 = max(int(np.searchsorted(idx, pd.Timestamp(start).value)) if start is not None else 0, strategy.warmup_bars)
    i1 = int(np.searchsorted(idx, pd.Timestamp(end).value)) if end is not None else len(F)
    o, h, l, c = (F[k].to_numpy() for k in ("open", "high", "low", "close"))
    a, td, ms = F["atr"].to_numpy(), F["td"].to_numpy(), F["msess"].to_numpy()
    if exec_bars is not None:
        ex_idx = exec_bars.index.as_unit("ns")
        ets = ex_idx.asi8
        etc = time_columns(ex_idx)
        eo, eh, el, ec = (exec_bars[k].to_numpy(dtype=float) for k in ("open", "high", "low", "close"))
        etd, ems = etc["td"].to_numpy(), etc["msess"].to_numpy()
    sim = ExecutionSimulator(costs)
    for i in range(i0, i1):
        atr_known = a[i - 1] if i > 0 else a[i]  # ATR connu au début de la barre (glissement « marché rapide »)
        if exec_bars is None:
            sim.on_bar(int(idx[i]), o[i], h[i], l[i], c[i], atr_known, int(td[i]), int(ms[i]))
        else:
            j0, j1 = np.searchsorted(ets, idx[i]), np.searchsorted(ets, idx[i] + BAR_NS)
            for j in range(j0, j1):
                sim.on_bar(int(ets[j]), eo[j], eh[j], el[j], ec[j], atr_known, int(etd[j]), int(ems[j]))
        sim.end_of_decision_bar(h[i], l[i], a[i])
        d = int(td[i])
        st = StrategyState(
            has_position=sim.position is not None,
            pending_tags={s.tag for s in sim.pending if s.valid_until_ts > idx[i] + BAR_NS},
            tags_today=sim.tags_by_td.get(d, set()),
            trades_today=sim.entries_by_td.get(d, 0),
        )
        for s in strategy.evaluate(i, F, st).setups:
            sim.submit(s)
    return trades_frame(sim.trades)


def trades_frame(trades: list[Trade]) -> pd.DataFrame:
    cols = list(Trade.__dataclass_fields__.keys())
    if not trades:
        return pd.DataFrame(columns=cols + ["entry_time", "year"])
    d = pd.DataFrame([{k: v for k, v in asdict(t).items()} for t in trades])
    d["entry_time"] = pd.to_datetime(d["entry_ts"], utc=True, unit="ns")
    d["year"] = d["entry_time"].dt.year
    return d
