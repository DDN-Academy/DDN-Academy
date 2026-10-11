"""Contrats MGC (échéances, roll), fuseaux horaires et heures d'été, calendrier économique, qualité des données."""
from __future__ import annotations

from datetime import date, datetime, timedelta, timezone

import pandas as pd
import pytest

from goldpilot.calendar.events import Blackout, Event, blocking_event, next_event, parse_ics, seed_events
from goldpilot.marketdata import quality as dq
from goldpilot.marketdata.contracts import active_contract, add_bdays, business_day, next_contract, parse_tv_symbol
from goldpilot.timeutil import fmt_ny, fmt_paris, is_open, market_phase, msess, ny_time_on, trading_date

from .conftest import utc


# ------------------------------------------------------------------------------------------- contrats
def test_active_contract_and_roll_dates():
    c = active_contract(date(2026, 10, 10))
    assert c.code == "MGCZ2026" and c.short_code == "MGCZ6" and c.tradingview == "COMEX:MGCZ2026"
    assert c.first_notice == date(2026, 11, 30)  # dernier jour ouvré du mois précédent l'échéance
    assert c.roll_date == date(2026, 11, 20)  # 5 jours ouvrés avant (Thanksgiving 26/11 exclu)
    assert active_contract(date(2026, 11, 19)).code == "MGCZ2026"
    assert active_contract(date(2026, 11, 20)).code == "MGCG2027"
    assert next_contract(c).code == "MGCG2027"


def test_only_active_months_are_traded():
    seen = {active_contract(date(2026, m, 15)).month for m in range(1, 13)}
    assert seen <= {2, 4, 6, 8, 10, 12}


def test_business_days_skip_holidays_and_weekends():
    assert not business_day(date(2026, 11, 26))  # Thanksgiving
    assert not business_day(date(2026, 12, 25)) and not business_day(date(2026, 10, 10))
    assert add_bdays(date(2026, 11, 25), 1) == date(2026, 11, 27)


@pytest.mark.parametrize("sym,code", [("COMEX:MGCZ2026", "MGCZ2026"), ("mgcg2027", "MGCG2027"), ("MGC1!", None), ("GCZ2026", None),
                                      ("MGCZ26", None), ("MGCA2026", None)])
def test_parse_tradingview_symbol(sym, code):
    c = parse_tv_symbol(sym)
    assert (c.code if c else None) == code


# ------------------------------------------------------------------------------------------- temps
def test_trading_day_starts_at_18h_new_york():
    assert trading_date(utc(2026, 10, 11, 22, 30)) == date(2026, 10, 12)  # dimanche 18:30 NY → lundi
    assert trading_date(utc(2026, 10, 12, 21, 59)) == date(2026, 10, 12)  # lundi 17:59 NY
    assert trading_date(utc(2026, 1, 12, 23, 0)) == date(2026, 1, 13)  # hiver : 18:00 NY = 23:00 UTC


def test_session_minutes_identical_across_daylight_saving():
    # 09:00 New York en heure d'hiver (UTC-5) et en heure d'été (UTC-4) : même minute de séance
    assert msess(utc(2026, 1, 15, 14, 0)) == msess(utc(2026, 7, 15, 13, 0)) == 15 * 60
    # semaine de décalage USA/Europe (mars 2026) : Paris n'a pas encore changé d'heure
    assert msess(utc(2026, 3, 10, 13, 0)) == 15 * 60
    assert fmt_paris(utc(2026, 3, 10, 13, 0)).startswith("10/03/2026 14:00")
    assert fmt_ny(utc(2026, 3, 10, 13, 0)) == "09:00 New York"


def test_ny_time_on_handles_previous_evening():
    assert ny_time_on(date(2026, 10, 12), "18:00") == utc(2026, 10, 11, 22, 0)
    assert ny_time_on(date(2026, 10, 12), "15:30") == utc(2026, 10, 12, 19, 30)


@pytest.mark.parametrize("dt,phase", [(utc(2026, 10, 10, 15, 0), "fermé (week-end)"), (utc(2026, 10, 11, 21, 0), "fermé (week-end)"),
                                      (utc(2026, 10, 11, 22, 30), "Asie"), (utc(2026, 10, 12, 21, 30), "pause quotidienne"),
                                      (utc(2026, 10, 12, 9, 0), "Londres"), (utc(2026, 10, 12, 14, 0), "New York (matin)"),
                                      (utc(2026, 10, 12, 17, 0), "New York (après-midi)"), (utc(2026, 10, 9, 21, 30), "fermé (week-end)")])
def test_market_phase(dt, phase):
    assert market_phase(dt) == phase


def test_naive_datetimes_rejected():
    with pytest.raises(ValueError):
        msess(datetime(2026, 10, 12, 14, 0))


# ------------------------------------------------------------------------------------------- calendrier
CPI = Event("bls", "cpi", "Consumer Price Index", "fort", utc(2026, 10, 14, 12, 30), "https://www.bls.gov")


@pytest.mark.parametrize("at,blocked", [(utc(2026, 10, 14, 11, 49), False), (utc(2026, 10, 14, 11, 51), True),
                                        (utc(2026, 10, 14, 12, 15), True), (utc(2026, 10, 14, 12, 45), True),
                                        (utc(2026, 10, 14, 12, 46), False)])
def test_blackout_window(at, blocked):
    # fenêtre de prudence 12:20–12:45 UTC (10 min avant, 15 min après) ; horizon de 30 min après l'instant du signal
    assert (blocking_event([CPI], at, timedelta(minutes=30), Blackout()) is not None) == blocked


def test_seeded_official_dates():
    ev = seed_events()
    titles = " ".join(e.title for e in ev)
    assert "FOMC" in titles and any(e.ts == utc(2026, 11, 6, 13, 30) for e in ev)  # NFP 6 novembre 08:30 NY (heure d'hiver)
    assert all(e.source_url.startswith("https://") for e in ev)
    assert next_event(ev, utc(2026, 10, 10)).ts >= utc(2026, 10, 10)


def test_parse_bls_ics():
    ics = ("BEGIN:VCALENDAR\nBEGIN:VEVENT\nUID:abc@bls.gov\nDTSTART;TZID=America/New_York:20261106T083000\n"
           "SUMMARY:Employment Situation for October 2026\nEND:VEVENT\nBEGIN:VEVENT\nUID:def@bls.gov\n"
           "DTSTART;TZID=America/New_York:20261112T100000\nSUMMARY:Job Openings and Labor Turnover Survey\nEND:VEVENT\nEND:VCALENDAR\n")
    ev = {e.uid: e for e in parse_ics(ics)}
    assert ev["abc@bls.gov"].ts == utc(2026, 11, 6, 13, 30) and ev["abc@bls.gov"].impact == "fort"
    assert ev["def@bls.gov"].impact == "moyen"


# ------------------------------------------------------------------------------------------- qualité
NOW_Q = utc(2026, 10, 7, 14, 0, 30)  # mercredi 10:00:30 New York, marché ouvert


def bars(n=120, end=NOW_Q - timedelta(seconds=30), symbol="MGCZ2026", minutes=1, jump_at=None):
    idx = pd.date_range(end=end - timedelta(minutes=minutes), periods=n, freq=f"{minutes}min", tz="UTC")
    c = 4000 + pd.Series(range(n), dtype=float).to_numpy() * 0.1
    df = pd.DataFrame({"open": c, "high": c + 0.5, "low": c - 0.5, "close": c, "volume": 10.0, "minutes": minutes, "symbol": symbol}, index=idx)
    if jump_at is not None:
        df.iloc[jump_at:, :4] += 100
    return df


def test_quality_ok():
    q = dq.assess(bars(), NOW_Q, [2.0] * 10)
    assert q.level == "ok" and q.ok and q.last_price == pytest.approx(4011.9)


def test_quality_no_data():
    assert dq.assess(bars().iloc[:0], NOW_Q).level == "bloquant"


def test_quality_stale():
    q = dq.assess(bars(end=NOW_Q - timedelta(minutes=10)), NOW_Q)
    assert q.level == "bloquant" and "périmées" in q.problems[0]


def test_quality_stale_ignored_when_market_closed():
    sat = utc(2026, 10, 10, 15, 0)
    assert dq.assess(bars(end=utc(2026, 10, 9, 21, 0)), sat).level == "ok"


def test_quality_wrong_contract():
    q = dq.assess(bars(symbol="MGCV2026"), NOW_Q)
    assert q.level == "bloquant" and "différent du contrat actif" in q.problems[0]


def test_quality_delayed_feed():
    q = dq.assess(bars(), NOW_Q, [600.0] * 10)  # 10 min : compte TradingView sans temps réel COMEX
    assert q.level == "bloquant" and "retard" in " ".join(q.problems)


def test_quality_incomplete_hour_is_degraded():
    b = bars(n=180)
    b = pd.concat([b.iloc[:120], b.iloc[-30:]])  # 30 barres sur la dernière heure au lieu de 60
    q = dq.assess(b, NOW_Q)
    assert q.level == "degrade" and "incomplètes" in q.problems[0]


def test_quality_abnormal_jump():
    q = dq.assess(bars(jump_at=110), NOW_Q)
    assert q.level == "bloquant" and "saut de prix" in " ".join(q.problems)


def test_quality_five_minute_bars_not_flagged_stale_or_incomplete():
    q = dq.assess(bars(n=60, minutes=5, end=NOW_Q - timedelta(minutes=2)), NOW_Q)
    assert q.level == "ok", q.problems
