"""Test de bout en bout : le moteur temps réel (base de données, agrégation, stratégie, risque, simulateur,
cycle de vie des signaux) rejoue 3 semaines de juin 2025 et doit reproduire EXACTEMENT le backtest :
mêmes indicateurs à chaque barre de décision, mêmes signaux, mêmes résultats par trade.
"""
import math

import pandas as pd
import pytest
from sqlalchemy import select

from goldpilot import db
from goldpilot.config import settings
from goldpilot.engine import strategy_config
from goldpilot.engine.runner import Engine
from goldpilot.marketdata.replay import ReplayFeeder
from goldpilot.research.backtest import run
from goldpilot.research.data import load_15m, load_5m
from goldpilot.research.execution import BASE_COSTS

START, END = "2025-06-01T22:00:00Z", "2025-06-21T00:00:00Z"  # dimanche 18:00 New York → samedi


@pytest.fixture(scope="module")
def replayed(tmp_path_factory):
    path = tmp_path_factory.mktemp("e2e") / "e2e.db"
    mp = pytest.MonkeyPatch()
    mp.setenv("DATABASE_URL", f"sqlite:///{path}")
    mp.setenv("DATA_SOURCE", "replay")
    settings.cache_clear()
    strategy_config.load_production.cache_clear()
    db.init(create=True)
    feeder = ReplayFeeder(START, speed=0, end=END)
    n_daily = feeder.seed_daily_history()
    eng = Engine(clock=feeder.now, source_filter="replay")
    eng.startup()
    with db.session() as s:  # paramètres permissifs : on teste la parité de la chaîne, pas les limites
        db.kv_set(s, "risk_settings", {"risk_per_trade_usd": 500, "max_cushion_fraction": 0.35, "daily_loss_stop_usd": 2000,
                                        "max_trades_per_day": 6, "max_losses_per_day": 6, "consistency_lock_fraction": 1.0})
    while feeder.step():
        eng.tick()
    yield eng, n_daily
    mp.undo()
    settings.cache_clear()


def test_daily_history_seeded(replayed):
    _, n = replayed
    assert n == 300


def test_every_bucket_analysed_and_logged(replayed):
    with db.session() as s:
        dec = s.execute(select(db.Decision)).scalars().all()
    outcomes = pd.Series([d.outcome for d in dec]).value_counts().to_dict()
    assert len(dec) > 1000
    assert outcomes.get("aucun_setup", 0) > 900
    assert all(d.reasons for d in dec if d.outcome != "signal"), "chaque absence de trade doit être expliquée"


def test_indicators_identical_to_backtest(replayed):
    strat = strategy_config.build_strategy()
    F = strat.prepare(load_15m())
    with db.session() as s:
        dec = s.execute(select(db.Decision).where(db.Decision.outcome.in_(["aucun_setup", "refuse", "signal"]))).scalars().all()
    checked = 0
    for d in dec:
        z = (d.context or {}).get("z")
        ts = pd.Timestamp(d.bar_ts).tz_convert("UTC")
        if z is None or ts < pd.Timestamp("2025-06-03", tz="UTC") or ts not in F.index:
            continue
        assert z == pytest.approx(round(float(F.loc[ts, "z"]), 2), abs=0.011)
        checked += 1
    assert checked > 800


def test_signals_and_outcomes_identical_to_backtest(replayed):
    strat = strategy_config.build_strategy()
    F = strat.prepare(load_15m())
    five = load_5m()
    bt = run(strat, F, BASE_COSTS, start=pd.Timestamp("2025-06-03", tz="UTC"), end=pd.Timestamp(END), exec_bars=five)
    with db.session() as s:
        sigs = s.execute(select(db.Signal).order_by(db.Signal.created_at)).scalars().all()
        refused = s.execute(select(db.Decision).where(db.Decision.outcome == "refuse")).scalars().all()
    sigs = [x for x in sigs if pd.Timestamp(x.meta["decision_bar_ts"], unit="ns", tz="UTC") >= pd.Timestamp("2025-06-03", tz="UTC")]
    assert len(sigs) >= 1, "la période doit contenir au moins un signal"
    assert not refused, [r.reasons for r in refused]
    by_decision = {int(t.decision_ts): t for t in bt.itertuples()}
    for sg in sigs:
        key = int(sg.meta["decision_bar_ts"]) + 15 * 60 * 1_000_000_000
        assert key in by_decision, "signal du moteur absent du backtest"
        t = by_decision[key]
        assert (1 if sg.side > 0 else -1) == t.side
        assert sg.status == "CLOTURE"
        assert sg.sim_entry == pytest.approx(t.entry_px, abs=1e-9)
        assert sg.sim_exit == pytest.approx(t.exit_px, abs=1e-9)
        assert sg.sim_r == pytest.approx(t.r, abs=1e-9)
        assert sg.sim_exit_reason == t.exit_reason
    assert len(sigs) == len(bt), f"moteur {len(sigs)} signaux, backtest {len(bt)} trades"


def test_notifications_queued_for_each_signal(replayed):
    with db.session() as s:
        n = s.execute(select(db.Notification).where(db.Notification.kind == "signal")).scalars().all()
        sig = s.execute(select(db.Signal)).scalars().all()
    assert len(n) == len(sig)
    t = n[0].text
    for must in ("Instrument", "Sens", "Entrée", "Stop-loss", "Take-profit", "Rendement/risque", "Taille", "Risque estimé",
                 "Validité", "Annulation", "Pourquoi", "Calendrier", "Prix", "SIMULATION"):
        assert must in t, must
    assert not math.isnan(sig[0].risk_usd)
