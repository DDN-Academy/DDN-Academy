"""Séances CME (jours fériés, clôtures anticipées, réouverture de 18:00), dimensionnement sur la pire entrée de la plage,
mois actifs MGC (octobre) et niveaux de contexte des signaux (contrat C4)."""
from __future__ import annotations

from datetime import date, timedelta
from types import SimpleNamespace

import numpy as np
import pandas as pd
import pytest
from sqlalchemy import select

from goldpilot import db
from goldpilot.marketdata import quality as dq
from goldpilot.marketdata.contracts import ACTIVE_MONTHS, active_contract
from goldpilot.notify import messages
from goldpilot.risk import engine as risk
from goldpilot.risk.sizing import RiskSettings, risk_per_contract
from goldpilot.strategy.base import StrategyState
from goldpilot.strategy.candidates import LEVEL_KEYS, S1SessionExtension
from goldpilot.timeutil import NY, UTC, is_open, last_open_time, market_phase, msess_of, session_close_ny

from .conftest import utc
from .test_causality import synthetic
from .test_risk import S, ctx, refused_by, setup


def ny(y, mo, d, h, mi=0, s=0):
    from datetime import datetime
    return datetime(y, mo, d, h, mi, s, tzinfo=NY)


# ------------------------------------------------------------------------------------------- jours fériés (#0)
@pytest.mark.parametrize("dt,phase", [
    (ny(2026, 12, 25, 10, 0), "fermé (jour férié)"),  # Noël
    (ny(2026, 12, 24, 19, 0), "fermé (jour férié)"),  # séance du soir rattachée au 25/12
    (ny(2026, 12, 24, 14, 30), "fermé (clôture anticipée)"),  # veille de Noël : clôture 13:45
    (ny(2026, 12, 24, 13, 0), "New York (après-midi)"),
    (ny(2026, 11, 27, 14, 0), "fermé (clôture anticipée)"),  # lendemain de Thanksgiving
    (ny(2026, 11, 26, 13, 30), "fermé (clôture anticipée)"),  # Thanksgiving : arrêt 13:00
    (ny(2026, 11, 26, 18, 30), "Asie"),  # réouverture le soir pour le vendredi
    (ny(2027, 3, 26, 10, 0), "fermé (jour férié)"),  # Vendredi saint
    (ny(2027, 1, 1, 10, 0), "fermé (jour férié)"),
    (ny(2026, 12, 27, 18, 30), "Asie"),  # réouverture du dimanche après Noël
])
def test_holiday_phases(dt, phase):
    assert market_phase(dt) == phase
    assert is_open(dt) == (not phase.startswith("fermé"))


def test_session_close_helper():
    assert session_close_ny(date(2026, 12, 25)) is None
    assert session_close_ny(date(2026, 11, 27)) == ny(2026, 11, 27, 13, 45)
    assert session_close_ny(date(2026, 12, 24)) == ny(2026, 12, 24, 13, 45)
    assert session_close_ny(date(2026, 10, 14)) == ny(2026, 10, 14, 17, 0)


@pytest.mark.parametrize("now,opened", [
    (ny(2026, 10, 13, 18, 0, 10), ny(2026, 10, 13, 18, 0)),  # réouverture quotidienne
    (ny(2026, 10, 14, 10, 0), ny(2026, 10, 13, 18, 0)),
    (ny(2026, 10, 11, 18, 30), ny(2026, 10, 11, 18, 0)),  # dimanche soir
    (ny(2026, 12, 27, 18, 5), ny(2026, 12, 27, 18, 0)),  # après Noël
    (ny(2026, 12, 25, 10, 0), ny(2026, 12, 23, 18, 0)),  # jour férié : dernière ouverture = séance du 24
])
def test_last_open_time(now, opened):
    assert last_open_time(now) == opened


def bars_until(end, n=120, minutes=1, symbol="MGCZ2026"):
    idx = pd.date_range(end=(end - timedelta(minutes=minutes)).astimezone(UTC), periods=n, freq=f"{minutes}min", tz="UTC")
    c = 4000 + np.arange(n) * 0.1
    return pd.DataFrame({"open": c, "high": c + 0.5, "low": c - 0.5, "close": c, "volume": 10.0, "minutes": minutes,
                         "symbol": symbol}, index=idx)


def test_no_stale_safe_mode_on_holiday_or_after_early_close():
    q = dq.assess(bars_until(ny(2026, 12, 24, 13, 45), symbol="MGCG2027"), ny(2026, 12, 25, 10, 0))
    assert q.level == "ok", q.problems
    q = dq.assess(bars_until(ny(2026, 11, 27, 13, 45), symbol="MGCG2027"), ny(2026, 11, 27, 14, 30))
    assert q.level == "ok", q.problems


def test_risk_refuses_exit_after_early_close():
    d = risk.evaluate(setup(), ctx(now=ny(2026, 11, 27, 10, 0)), S)  # sortie 15:30 > 13:45 − 25 min
    assert not d.accepted and "Horaires FundedNext" in refused_by(d)
    assert "clôture anticipée" in next(c.detail for c in d.checks if c.name == "Horaires FundedNext")
    d = risk.evaluate(setup(), ctx(now=ny(2026, 12, 24, 10, 0)), S)
    assert "Horaires FundedNext" in refused_by(d)
    d = risk.evaluate(setup(exit_msess=msess_of("13:20")), ctx(now=ny(2026, 12, 24, 10, 0)), S)
    assert "Horaires FundedNext" not in refused_by(d)
    d = risk.evaluate(setup(exit_msess=msess_of("13:25")), ctx(now=ny(2026, 12, 24, 10, 0)), S)
    assert "Horaires FundedNext" in refused_by(d)


def test_risk_refuses_on_full_holiday():
    d = risk.evaluate(setup(), ctx(now=ny(2026, 12, 25, 10, 0)), S)
    assert "Horaires FundedNext" in refused_by(d)


def test_regular_day_keeps_1545_limit():
    assert "Horaires FundedNext" not in refused_by(risk.evaluate(setup(exit_msess=msess_of("15:45")), ctx(), S))
    assert "Horaires FundedNext" in refused_by(risk.evaluate(setup(exit_msess=msess_of("15:50")), ctx(), S))


# ------------------------------------------------------------------------------------------- réouverture 18:00 (#23)
def test_no_false_stale_at_daily_reopen():
    b = bars_until(ny(2026, 10, 13, 17, 0))
    assert dq.assess(b, ny(2026, 10, 13, 18, 0, 10)).level == "ok"
    q = dq.assess(b, ny(2026, 10, 13, 18, 4))  # 4 min après la réouverture sans nouvelle barre : bien périmé
    assert q.level == "bloquant" and "périmées" in q.problems[0]


def test_no_false_stale_at_sunday_reopen():
    b = bars_until(ny(2026, 10, 9, 17, 0))
    assert dq.assess(b, ny(2026, 10, 11, 18, 0, 30)).level == "ok"
    assert dq.assess(b, ny(2026, 10, 11, 18, 5)).level == "bloquant"


def test_incomplete_hour_measured_from_reopen():
    before = bars_until(ny(2026, 10, 13, 17, 0), n=120)
    after = bars_until(ny(2026, 10, 13, 18, 10), n=10)  # 10 barres depuis 18:00 : complet
    q = dq.assess(pd.concat([before, after]), ny(2026, 10, 13, 18, 10, 30))
    assert q.level == "ok", q.problems
    holes = pd.concat([before, after.iloc[:2], after.iloc[-1:]])  # 3 barres sur 10 minutes : incomplet
    q = dq.assess(holes, ny(2026, 10, 13, 18, 10, 30))
    assert q.level == "degrade" and "incomplètes" in q.problems[0]


def test_engine_no_safe_mode_alert_at_reopen(env):
    from goldpilot.engine.runner import Engine

    clock = {"t": utc(2026, 10, 13, 20, 0, 5)}  # 16:00:05 New York
    e = Engine(clock=lambda: clock["t"])
    e.startup()
    with db.session() as s:
        t0 = utc(2026, 10, 13, 20, 0)
        for i in range(60):  # 16:00 → 16:59 New York
            ts = t0 + timedelta(minutes=i)
            s.add(db.Bar(source="tradingview", symbol="MGCZ2026", ts=ts, minutes=1, open=4000, high=4001, low=3999, close=4000,
                         volume=1, received_at=ts + timedelta(minutes=1, seconds=2), processed=False))
    for t in (utc(2026, 10, 13, 21, 0, 5), utc(2026, 10, 13, 21, 30), utc(2026, 10, 13, 22, 0, 10)):
        clock["t"] = t
        e.tick()
    assert e.mode != "securise"
    with db.session() as s:
        keys = [n.key for n in s.execute(select(db.Notification)).scalars()]
    assert not [k for k in keys if k.startswith(("safe:", "recover:"))], keys
    clock["t"] = utc(2026, 10, 13, 22, 4, 30)  # toujours aucune barre 4 min après la réouverture
    e.tick()
    assert e.mode == "securise"


# ------------------------------------------------------------------------------------------- taille (#8)
@pytest.mark.parametrize("side", [1, -1])
def test_size_uses_worst_entry_of_band(side):
    su = setup(side=side, atr=3.0, ref_price=4000.0, stop=4000.0 - side * 7.5)
    settings = RiskSettings(risk_per_trade_usd=250, daily_loss_stop_usd=500)
    d = risk.evaluate(su, ctx(last_price=4000.0), settings)
    assert d.accepted, d.refusals
    edge = 4000.0 + side * 0.5 * 3.0  # bord défavorable de la plage acceptable
    real = d.contracts * risk_per_contract(edge, su.stop, settings)
    assert real <= settings.risk_per_trade_usd + 1e-9
    assert d.contracts == 2 and d.risk_usd == pytest.approx(real)  # avant correction : 3 contrats, 285 $ au bord


def test_telegram_risk_text_mentions_worst_entry():
    sig = fake_signal()
    assert "pire bord de la plage" in messages.new_signal(sig, "Micro Gold", None, "")


# ------------------------------------------------------------------------------------------- mois actifs (#7)
def test_october_is_an_active_month_and_2027_roll_sequence():
    assert 10 in ACTIVE_MONTHS
    assert active_contract(date(2027, 7, 20)).code == "MGCQ2027"
    assert active_contract(date(2027, 7, 26)).code == "MGCV2027"
    assert active_contract(date(2027, 9, 24)).code == "MGCZ2027"
    assert active_contract(date(2026, 10, 11)).code == "MGCZ2026"


# ------------------------------------------------------------------------------------------- niveaux (C4)
@pytest.fixture(scope="module")
def s1_frames():
    df = synthetic(30000)
    s = S1SessionExtension(k=2.0, s=2.5, t=3.0, F=False)
    return s, df, s.prepare(df), s.prepare(df.iloc[:27000])


def test_s1_context_has_levels_and_setup_meta(s1_frames):
    s, df, full, _ = s1_frames
    st = StrategyState()
    found = 0
    for i in range(26000, 27000):
        ev = s.evaluate(i, full, st)
        niv = ev.context["niveaux"]
        assert set(LEVEL_KEYS) <= set(niv) and set(niv["distances_atr"]) == set(LEVEL_KEYS)
        for su in ev.setups:
            assert su.meta["niveaux"] == niv
            found += 1
    assert found > 0


def test_levels_values_and_causality(s1_frames):
    s, df, full, part = s1_frames
    st = StrategyState()
    td = full["td"].to_numpy()
    for i in (26010, 26500, 26999):
        a, b = s.evaluate(i, full, st).context["niveaux"], s.evaluate(i, part, st).context["niveaux"]
        assert a == b  # aucune donnée future
        same = td == td[i]
        assert a["plus_haut_seance"] == round(float(df["high"].to_numpy()[: i + 1][same[: i + 1]].max()), 2)
        prev = td < td[i]
        prev_td = td[prev].max()
        assert a["plus_bas_veille"] == round(float(df["low"].to_numpy()[td == prev_td].min()), 2)
        c, atr = float(full["close"].iloc[i]), float(full["atr"].iloc[i])
        assert a["distances_atr"]["plus_haut_seance"] == round((c - float(full["lv_sh"].iloc[i])) / atr, 2)
        h = df["high"].to_numpy()
        j = max(k for k in range(2, i - 1) if h[k] >= h[k - 2:k + 3].max())  # dernier sommet confirmé (2 barres après)
        assert a["swing_haut_15m"] == round(float(h[j]), 2)


def test_levels_do_not_change_decisions(s1_frames):
    s, df, full, _ = s1_frames
    bare = full.drop(columns=[c for c in full.columns if c.startswith("lv_")]).copy()
    bare.attrs = {}
    st = StrategyState()
    for i in range(26000, 27000):
        a, b = s.evaluate(i, full, st), s.evaluate(i, bare, st)
        assert a.no_trade_reasons == b.no_trade_reasons and len(a.setups) == len(b.setups)
        assert "niveaux" not in b.context


def fake_signal(meta=None):
    return SimpleNamespace(side=1, entry_ref=4000.0, entry_max_drift=2.0, target=None, reward_risk=None, trail_atr=3.0, atr=4.0,
                           exit_deadline=utc(2026, 10, 9, 19, 30), entry_type="market", mode="simulation", validated=False,
                           created_at=utc(2026, 10, 9, 13, 0, 5), stop=3990.0, contracts=2, risk_usd=250.0,
                           valid_until=utc(2026, 10, 9, 13, 30), invalidation="i", rationale="r", calendar_note="c",
                           price_source="TradingView", price_ts=utc(2026, 10, 9, 13, 0), id="abcdef123456", strategy_version="v",
                           meta=meta or {})


def test_telegram_levels_line():
    niv = {"plus_haut_veille": 4012.3, "plus_bas_veille": 3980.0, "plus_haut_seance": 4005.0, "plus_bas_seance": 3990.5,
           "swing_haut_15m": None, "swing_bas_15m": 3995.0,
           "distances_atr": {"plus_haut_veille": -3.08, "plus_bas_veille": 5.0, "plus_haut_seance": -1.25,
                             "plus_bas_seance": 2.38, "swing_haut_15m": None, "swing_bas_15m": 1.25}}
    txt = messages.new_signal(fake_signal({"niveaux": niv}), "Micro Gold", None, "")
    line = next(x for x in txt.split("\n") if x.startswith("<b>Niveaux :</b>"))
    assert "plus haut de la veille 4 012.3 (-3.1 ATR)" in line and "dernier creux 15 min 3 995.0 (+1.2 ATR)" in line
    assert "dernier sommet 15 min" not in line
    assert txt.index("Pourquoi :") < txt.index("Niveaux :") < txt.index("Calendrier :")
    assert "Niveaux :" not in messages.new_signal(fake_signal(), "Micro Gold", None, "")
