"""Chaque règle d'exécution prudente du protocole est vérifiée."""
import pytest

from goldpilot.research.execution import BASE_COSTS, ZERO_COSTS, CostModel, ExecutionSimulator
from goldpilot.strategy.base import NS_MIN, Setup

B = 15 * NS_MIN


def setup(side=1, et="market", entry=None, stop=99.0, target=None, trail=None, valid_bars=1, exit_m=1290, td=1, ref=100.0):
    return Setup("T", "T", side, et, entry, stop, target, trail, 1.0, ref, 0, B, B * (1 + valid_bars), exit_m, td, "t", "", "")


def bar(sim, k, o, h, l, c, atr=1.0, td=1, m=900):
    return sim.on_bar(k * B, o, h, l, c, atr, td, m)


def test_market_entry_at_next_open_with_half_spread():
    sim = ExecutionSimulator(BASE_COSTS)
    sim.submit(setup())
    bar(sim, 1, 100.0, 100.5, 99.5, 100.2)
    assert sim.position.entry_px == pytest.approx(100.0 + 0.05 / 4000 * 100.0)


def test_entry_bar_entirely_after_market_entry_stop_hit():
    sim = ExecutionSimulator(ZERO_COSTS)
    sim.submit(setup(stop=99.0))
    ev = bar(sim, 1, 100.0, 100.4, 98.9, 100.1)
    assert [e.kind for e in ev] == ["fill", "exit"]
    assert sim.trades[0].r == pytest.approx(-1.0)


def test_stop_entry_gap_fills_at_open():
    sim = ExecutionSimulator(ZERO_COSTS)
    sim.submit(setup(et="stop", entry=100.5, stop=99.5))
    bar(sim, 1, 101.0, 101.2, 100.9, 101.1)
    assert sim.position.entry_px == pytest.approx(101.0)


def test_expiry():
    sim = ExecutionSimulator(ZERO_COSTS)
    sim.submit(setup(et="stop", entry=101.0, valid_bars=1))
    bar(sim, 1, 100.0, 100.5, 99.8, 100.2)
    ev = bar(sim, 2, 100.2, 101.5, 100.1, 101.4)
    assert [e.kind for e in ev] == ["expire"] and sim.position is None


def test_same_bar_stop_and_target_stop_first():
    sim = ExecutionSimulator(ZERO_COSTS)
    sim.submit(setup(stop=99.0, target=102.0))
    bar(sim, 1, 100.0, 100.3, 99.6, 100.1)
    ev = bar(sim, 2, 100.1, 102.5, 98.8, 100.0)
    assert ev[0].reason == "stop" and sim.trades[0].r == pytest.approx(-1.0)


def test_gap_through_stop_exits_at_open():
    sim = ExecutionSimulator(ZERO_COSTS)
    sim.submit(setup(stop=99.0))
    bar(sim, 1, 100.0, 100.3, 99.6, 100.1)
    bar(sim, 2, 97.5, 98.0, 97.0, 97.8)
    assert sim.trades[0].exit_px == pytest.approx(97.5) and sim.trades[0].r == pytest.approx(-2.5)


def test_time_exit_and_day_change():
    sim = ExecutionSimulator(ZERO_COSTS)
    sim.submit(setup(exit_m=1000))
    bar(sim, 1, 100.0, 100.3, 99.6, 100.1, m=985)
    ev = bar(sim, 2, 100.4, 100.6, 100.3, 100.5, m=1000)
    assert ev[0].reason == "sortie temporelle" and sim.trades[0].exit_px == pytest.approx(100.4)
    sim2 = ExecutionSimulator(ZERO_COSTS)
    sim2.submit(setup())
    bar(sim2, 1, 100.0, 100.3, 99.6, 100.1)
    ev = bar(sim2, 2, 100.2, 100.3, 100.1, 100.2, td=2, m=0)
    assert ev[0].reason == "sortie temporelle"


def test_trailing_stop_ratchets_only():
    sim = ExecutionSimulator(ZERO_COSTS)
    sim.submit(setup(stop=98.0, trail=1.0))
    bar(sim, 1, 100.0, 100.5, 99.5, 100.4)
    sim.end_of_decision_bar(100.5, 99.5, 1.0)
    assert sim.position.stop == pytest.approx(99.5)
    bar(sim, 2, 100.4, 102.0, 100.3, 101.8)
    sim.end_of_decision_bar(102.0, 100.3, 1.0)
    assert sim.position.stop == pytest.approx(101.0)
    bar(sim, 3, 101.8, 101.9, 101.2, 101.5)
    sim.end_of_decision_bar(101.9, 101.2, 1.0)
    assert sim.position.stop == pytest.approx(101.0)
    ev = bar(sim, 4, 101.5, 101.6, 100.8, 100.9)
    assert ev[0].reason == "stop suiveur" and sim.trades[0].exit_px == pytest.approx(101.0)


def test_short_symmetry():
    sim = ExecutionSimulator(ZERO_COSTS)
    sim.submit(setup(side=-1, stop=101.0, trail=1.0))
    bar(sim, 1, 100.0, 100.2, 99.0, 99.1)
    sim.end_of_decision_bar(100.2, 99.0, 1.0)
    assert sim.position.stop == pytest.approx(100.0)
    ev = bar(sim, 2, 99.1, 100.1, 99.0, 100.0)
    assert ev[0].reason == "stop suiveur" and sim.trades[0].r == pytest.approx(0.0)


def test_one_position_at_a_time_and_no_fill_on_exit_bar():
    sim = ExecutionSimulator(ZERO_COSTS)
    sim.submit(setup(stop=99.0))
    bar(sim, 1, 100.0, 100.3, 99.6, 100.1)
    sim.submit(setup(side=-1, stop=101.0, valid_bars=3))
    ev = bar(sim, 2, 99.5, 99.6, 98.5, 98.7)  # stop de l'achat touché
    assert [e.kind for e in ev] == ["exit"] and sim.position is None and len(sim.pending) == 1


def test_fast_market_slippage_and_commission():
    cm = CostModel("fixed", 0.2, 0.05, 0.10, 0.30, 3.0, "t")
    sim = ExecutionSimulator(cm)
    sim.submit(setup(stop=99.0))
    bar(sim, 1, 100.0, 100.2, 95.0, 96.0, atr=1.0)  # amplitude 5,2 ATR : marché rapide
    t = sim.trades[0]
    assert t.entry_px == pytest.approx(100.05)
    assert t.exit_px == pytest.approx(99.0 - 0.05 - 0.30)
    assert t.pnl_oz == pytest.approx(t.exit_px - t.entry_px - 0.2)


def test_proportional_costs_scale_with_price():
    a = BASE_COSTS.amount("commission_rt", 4000.0)
    b = BASE_COSTS.amount("commission_rt", 2000.0)
    assert a == pytest.approx(0.20) and b == pytest.approx(0.10)
    assert BASE_COSTS.scaled(2).amount("commission_rt", 4000.0) == pytest.approx(0.40)
