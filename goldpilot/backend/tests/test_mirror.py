"""Contrôle croisé TradingView ↔ moteur : un désaccord (données contradictoires) est détecté, journalisé et signalé."""
from __future__ import annotations

from datetime import timedelta

from sqlalchemy import select

from goldpilot import db
from goldpilot.engine.runner import Engine

from .conftest import utc
from .test_api import _signal

NOW = utc(2026, 10, 7, 14, 20)
BAR = utc(2026, 10, 7, 14, 0)  # barre de 15 min 10:00–10:15 New York


def decision(bar_ts=BAR, cross=1, outcome="aucun_setup", signal_id=None):
    with db.session() as s:
        s.add(db.Decision(bar_ts=bar_ts, strategy_version="v", outcome=outcome, summary="", reasons=[],
                          context={"franchissement": cross, "z": 5.3 if cross else 1.2}, signal_id=signal_id))


def mirror(side=1, bar_ts=BAR, received=NOW - timedelta(minutes=3)):
    with db.session() as s:
        m = db.MirrorSignal(symbol="MGCZ2026", bar_ts=bar_ts, side=side, price=4000.0, received_at=received)
        s.add(m)
        s.flush()
        return m.id


def run_check(now=NOW):
    eng = Engine(clock=lambda: now)
    with db.session() as s:
        eng._check_mirrors(s, now, True)


def state(mid):
    with db.session() as s:
        m = s.get(db.MirrorSignal, mid)
        inc = s.execute(select(db.Incident).where(db.Incident.component == "controle_croise", db.Incident.resolved_at.is_(None))).scalars().all()
        notes = [n.key for n in s.execute(select(db.Notification)).scalars()]
        return m.verdict, inc, notes


def test_concordant(env):
    decision(cross=1)
    mid = mirror(side=1)
    run_check()
    verdict, inc, notes = state(mid)
    assert verdict == "concordant" and not inc and not [k for k in notes if k.startswith("mirror")]


def test_discordant_opens_incident_and_alert(env):
    decision(cross=0)
    mid = mirror(side=1)
    run_check()
    verdict, inc, notes = state(mid)
    assert verdict == "discordant" and len(inc) == 1 and f"mirror:{mid}" in notes
    assert "franchissement haussier" in inc[0].message and "10:15 New York" in inc[0].message


def test_concordant_after_discordant_resolves_incident(env):
    decision(cross=0)
    mirror(side=1)
    run_check()
    later = BAR + timedelta(minutes=45)
    decision(bar_ts=later, cross=-1)
    mid2 = mirror(side=-1, bar_ts=later, received=NOW + timedelta(minutes=44))
    run_check(NOW + timedelta(minutes=46))
    verdict, inc, _ = state(mid2)
    assert verdict == "concordant" and not inc


def test_missing_decision_waits_then_flags(env):
    mid = mirror(side=-1, received=NOW - timedelta(minutes=1))
    run_check()
    assert state(mid)[0] is None  # le moteur a encore le temps de décider
    run_check(NOW + timedelta(minutes=6))
    verdict, inc, _ = state(mid)
    assert verdict == "decision_absente" and len(inc) == 1


def test_engine_signal_not_confirmed_by_tradingview(env):
    old = BAR - timedelta(minutes=45)
    mirror(side=1, bar_ts=old - timedelta(hours=1), received=NOW - timedelta(hours=1))  # le miroir fonctionne
    sid = _signal(key="x", created_at=old + timedelta(minutes=15, seconds=5))
    decision(bar_ts=old, cross=1, outcome="signal", signal_id=sid)
    run_check()
    with db.session() as s:
        keys = [n.key for n in s.execute(select(db.Notification)).scalars()]
        evs = [e.kind for e in s.execute(select(db.SignalEvent).where(db.SignalEvent.signal_id == sid)).scalars()]
    assert f"mirror-missing:{sid}" in keys and "controle_croise" in evs
    run_check(NOW + timedelta(minutes=1))  # idempotent
    with db.session() as s:
        assert len([n for n in s.execute(select(db.Notification)).scalars() if n.key.startswith("mirror-missing")]) == 1
