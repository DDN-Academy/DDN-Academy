"""Absence de fuite d'information : ajouter des barres futures ne change ni les indicateurs passés ni les décisions passées."""
import numpy as np
import pandas as pd
import pytest

from goldpilot.strategy.base import StrategyState
from goldpilot.strategy.candidates import S1SessionExtension, S2LondonToNewYork
from goldpilot.strategy.indicators import time_columns


def synthetic(n=12000, seed=5):
    rng = np.random.default_rng(seed)
    idx = pd.date_range("2024-01-07 23:00", periods=int(n * 1.5), freq="15min", tz="UTC")
    ny = idx.tz_convert("America/New_York")
    m = ny.hour * 60 + ny.minute
    wd = ny.weekday
    keep = ~((m >= 17 * 60) & (m < 18 * 60)) & ~((wd == 4) & (m >= 17 * 60)) & (wd != 5) & ~((wd == 6) & (m < 18 * 60))
    idx = idx[keep][:n]
    # dérive intraday pour créer des extensions
    drift = np.where((ny[keep][:n].hour >= 8) & (ny[keep][:n].hour < 12), rng.choice([-1, 1]) * 0.0004, 0.0)
    r = rng.normal(0, 0.0012, n) + drift
    c = 2000 * np.exp(np.cumsum(r))
    o = np.r_[c[0], c[:-1]]
    sp = np.abs(rng.normal(0, 0.0008, n)) * c
    return pd.DataFrame({"open": o, "high": np.maximum(o, c) + sp, "low": np.minimum(o, c) - sp, "close": c}, index=idx)


def test_time_columns():
    idx = pd.DatetimeIndex(["2025-01-15 13:30", "2025-07-15 12:30", "2025-01-15 23:00"], tz="UTC")
    tc = time_columns(idx)
    assert list(tc["msess"]) == [870, 870, 0]
    assert tc["td"].iloc[2] == tc["td"].iloc[0] + 1


@pytest.mark.parametrize("strat", [
    S1SessionExtension(k=2.0, s=2.5, t=3.0, F=False),
    S1SessionExtension(k=2.0, s=1.5, t=2.0, F=True),
    S2LondonToNewYork(q=1.0, s=2.0, E="12:00"),
])
def test_decisions_identical_with_and_without_future(strat):
    df = synthetic(30000)
    cut = 27000
    full, part = strat.prepare(df), strat.prepare(df.iloc[:cut])
    st = StrategyState()
    n = 0
    for i in range(cut - 3000, cut):
        a, b = strat.evaluate(i, full, st), strat.evaluate(i, part, st)
        assert len(a.setups) == len(b.setups)
        assert a.no_trade_reasons == b.no_trade_reasons
        for x, y in zip(a.setups, b.setups):
            assert x.side == y.side and x.stop == pytest.approx(y.stop)
            n += 1
    assert n > 0, "le test doit porter sur de vraies décisions"


def test_feature_columns_stable():
    df = synthetic(30000)
    s = S1SessionExtension(F=True)
    full, part = s.prepare(df), s.prepare(df.iloc[:25000])
    for col in ("atr", "sm", "z", "rr_rank"):
        a, b = full[col].to_numpy()[:25000], part[col].to_numpy()
        m = np.isfinite(a) & np.isfinite(b)
        assert m.sum() > 100
        np.testing.assert_allclose(a[m], b[m], rtol=1e-10)
