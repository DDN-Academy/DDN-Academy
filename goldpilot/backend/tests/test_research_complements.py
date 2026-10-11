"""Compléments de recherche a posteriori : métriques (durée des drawdowns, dollars, régime de volatilité
causal), délai d'exécution simulé, et boucle de backtest du script research/05_complements.py."""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from goldpilot.research.backtest import run
from goldpilot.research.data import load_15m
from goldpilot.research.execution import BASE_COSTS, ZERO_COSTS, ExecutionSimulator
from goldpilot.research.metrics import drawdown_durations, in_dollars, volatility_tercile_by_day
from goldpilot.strategy.base import NS_MIN, Setup
from goldpilot.strategy.candidates import S1SessionExtension

B5 = 5 * NS_MIN
SCRIPT = Path(__file__).resolve().parents[2] / "research" / "05_complements.py"


def _script():
    spec = importlib.util.spec_from_file_location("complements_05", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


# ------------------------------------------------------------- métriques
def test_drawdown_durations_in_trading_days_including_flat_days():
    days = np.arange(1, 8)
    t = pd.DataFrame({"td": [1, 2, 3, 4, 5], "r": [1.0, -1.0, -1.0, 3.0, -1.0]})  # jours 6 et 7 sans trade
    d = drawdown_durations(t, days)
    # équité : 1, 0, -1, 2, 1, 1, 1 → sous le sommet aux jours 2-3 (2 j, résorbé) puis 5-7 (3 j, en cours)
    assert d["nb_drawdowns"] == 2 and d["duree_max_jours"] == 3 and d["duree_mediane_jours"] == 2.5
    assert d["drawdown_en_cours_fin"] and d["duree_en_cours_jours"] == 3 and d["jours_de_trading"] == 7


def test_drawdown_durations_no_drawdown():
    d = drawdown_durations(pd.DataFrame({"td": [1, 2], "r": [0.5, 0.5]}), np.array([1, 2]))
    assert d["duree_max_jours"] == 0 and d["nb_drawdowns"] == 0 and not d["drawdown_en_cours_fin"]


def test_in_dollars_uses_risk_per_trade():
    u = in_dollars({"esperance_R": 0.08, "drawdown_max_R": -19.2, "ic95_bas": -0.02, "ic95_haut": float("nan")}, 250)
    assert u["esperance_usd"] == pytest.approx(20.0) and u["drawdown_max_usd"] == pytest.approx(-4800.0)
    assert u["ic95_bas_usd"] == pytest.approx(-5.0) and "ic95_haut_usd" not in u


def _daily_bars(n_days: int, seed: int = 1) -> tuple[pd.DataFrame, np.ndarray]:
    rng = np.random.default_rng(seed)
    c = 100 + np.cumsum(rng.normal(0, 1, n_days))
    rngs = np.abs(rng.normal(1, 0.5, n_days)) * (1 + (np.arange(n_days) % 97 > 60))
    bars = pd.DataFrame({"high": c + rngs, "low": c - rngs, "close": c})
    return bars, np.arange(n_days)


def test_volatility_tercile_is_causal_and_labelled():
    bars, td = _daily_bars(600)
    full = volatility_tercile_by_day(bars, td)
    part = volatility_tercile_by_day(bars.iloc[:450], td[:450])
    pd.testing.assert_series_equal(full.iloc[:450], part)  # ajouter des journées futures ne change rien au passé
    assert set(full.dropna().unique()) <= {"faible", "moyenne", "forte"}
    assert full.iloc[:145].isna().all() and full.iloc[200:].notna().all()


# ------------------------------------------------------------- délai d'exécution
def _setup(side=1, stop=95.0):
    # décision à t = 0 ; valable 30 min
    return Setup("T", "T", side, "market", None, stop, None, None, 1.0, 100.0, -15 * NS_MIN, 0, 30 * NS_MIN, 1290, 1, "t", "", "")


def _bars(sim):
    sim.on_bar(0, 100.0, 101.0, 99.0, 100.5, 1.0, 1, 900)
    sim.on_bar(B5, 102.0, 102.5, 101.5, 102.2, 1.0, 1, 905)


def test_no_delay_is_unchanged_behaviour():
    sim = ExecutionSimulator(ZERO_COSTS)
    sim.submit(_setup())
    _bars(sim)
    assert sim.position.entry_px == pytest.approx(100.0) and sim.position.entry_ts == 0


def test_delay_5_min_enters_at_next_5min_open():
    sim = ExecutionSimulator(BASE_COSTS, entry_delay_ns=5 * NS_MIN, exec_bar_ns=B5)
    sim.submit(_setup())
    _bars(sim)
    assert sim.position.entry_ts == B5
    assert sim.position.entry_px == pytest.approx(102.0 + BASE_COSTS.amount("half_spread", 102.0))


@pytest.mark.parametrize("mode,side,expected", [("interpole", 1, 100.0 + 0.5 * 1 / 5), ("pire", 1, 101.0), ("pire", -1, 99.0)])
def test_delay_inside_bar_estimates_price(mode, side, expected):
    sim = ExecutionSimulator(ZERO_COSTS, entry_delay_ns=NS_MIN, exec_bar_ns=B5, delay_price=mode)
    sim.submit(_setup(side=side, stop=90.0 if side > 0 else 110.0))
    sim.on_bar(0, 100.0, 101.0, 99.0, 100.5, 1.0, 1, 900)
    assert sim.position.entry_ts == 0 and sim.position.entry_px == pytest.approx(expected)


def test_delay_requires_bar_length():
    with pytest.raises(ValueError):
        ExecutionSimulator(BASE_COSTS, entry_delay_ns=NS_MIN)


# ------------------------------------------------------------- script 05
def test_script_loop_identical_to_backtest_run():
    mod = _script()
    df = load_15m()
    bars = df[(df.index >= pd.Timestamp("2018-01-01", tz="UTC")) & (df.index < pd.Timestamp("2019-07-01", tz="UTC"))]
    cand = S1SessionExtension(k=5.0, s=2.5, t=3.0, F=False)
    F = cand.prepare(bars)
    a = run(cand, F, BASE_COSTS)
    b = mod.run_with(cand, F, ExecutionSimulator(BASE_COSTS))
    assert len(a) > 10
    pd.testing.assert_frame_equal(a.reset_index(drop=True), b.reset_index(drop=True))


def test_trend_1h_uses_only_completed_hours():
    mod = _script()
    df = load_15m()
    bars = df[(df.index >= pd.Timestamp("2020-03-02", tz="UTC")) & (df.index < pd.Timestamp("2020-03-20", tz="UTC"))]
    full = mod.trend_1h(bars)
    cut = bars.index[700]
    part = mod.trend_1h(bars[bars.index <= cut])
    pd.testing.assert_series_equal(full[full.index <= cut], part)  # barres futures sans effet
    assert set(np.unique(full)) <= {-1.0, 0.0, 1.0} and (full != 0).sum() > 500


def test_decision_minutes_restores_bar_length():
    mod = _script()
    from goldpilot.strategy import candidates
    with mod.decision_minutes(30):
        assert candidates.BAR_MIN == 30
    assert candidates.BAR_MIN == 15
