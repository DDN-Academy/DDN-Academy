"""Robustesse du moteur : source primaire, barres en retard, mode sécurisé, perte latente, échéances à l'horloge,
erreur pendant un passage, reprise après arrêt, gouvernance des versions, revue périodique, jours du compte simulé."""
from __future__ import annotations

from datetime import datetime, timedelta, timezone

import numpy as np
import pandas as pd
import pytest
from sqlalchemy import func, select

from goldpilot import db
from goldpilot.engine import runner
from goldpilot.engine import strategy_config
from goldpilot.engine.runner import Engine
from goldpilot.marketdata.contracts import active_contract, next_contract
from goldpilot.notify.telegram import deliver_pending
from goldpilot.risk.account import Account
from goldpilot.risk.rules import DEFAULT_PROGRAM, get_program
from goldpilot.strategy.base import Evaluation, Setup
from goldpilot.timeutil import msess, trading_date

from .conftest import utc
from .test_api import _signal

T0 = utc(2026, 10, 7, 14, 0)  # mercredi 10:00 New York, marché ouvert
SYM = active_contract(trading_date(T0)).code
NS = 1_000_000_000


def bar(ts, px=4000.0, source="tradingview", symbol=SYM, processed=False, received=None, low=None, high=None, close=None):
    return db.Bar(source=source, symbol=symbol, ts=ts, minutes=1, open=px, high=high if high is not None else px + 0.3,
                  low=low if low is not None else px - 0.3, close=close if close is not None else px, volume=10.0,
                  received_at=received or ts + timedelta(minutes=1, seconds=2), processed=processed)


def add(*rows):
    with db.session() as s:
        for r in rows:
            s.add(r)


def notes():
    with db.session() as s:
        return {n.key: n for n in s.execute(select(db.Notification)).scalars()}


def sig_get(sid):
    with db.session() as s:
        x = s.get(db.Signal, sid)
        s.expunge(x)
        return x


def history(end: datetime, minutes: int, source="tradingview", processed=True):
    """Barres d'une minute régulières (légère oscillation) jusqu'à `end` exclu."""
    rows = []
    for k in range(minutes, 0, -1):
        ts = end - timedelta(minutes=k)
        px = 4000.0 + 2.0 * np.sin(k / 7.0)
        rows.append(bar(ts, px, source=source, processed=processed))
    add(*rows)


class StubStrategy:
    """Stratégie factice : un setup d'achat à chaque barre de décision (teste la chaîne, pas la stratégie)."""
    needs_daily_history = False

    def __init__(self, setups=True):
        self.setups = setups

    def prepare(self, F15, daily_history=None):
        F = F15.copy()
        F["atr"] = 4.0
        F["td"] = [(trading_date(t.to_pydatetime()) - runner.EPOCH).days for t in F.index]
        return F

    def evaluate(self, i, F, st):
        ts = F.index[i]
        close = float(F["close"].iloc[i])
        su = Setup(strategy="S1", config_id="stub", side=1, entry_type="market", entry=None, stop=close - 8, target=None,
                   trail_atr=3.0, atr=4.0, ref_price=close, decision_bar_ts=int(ts.value),
                   decision_ts=int(ts.value) + 15 * 60 * NS, valid_until_ts=int(ts.value) + 45 * 60 * NS, exit_msess=1290,
                   td=int(F["td"].iloc[i]), tag="stub", rationale="r", invalidation="i",
                   meta={"niveaux": {"plus_haut_veille": 4010.0, "distances_atr": {"plus_haut_veille": -2.5}}})
        return Evaluation(bar_ts=int(ts.value), regime="test", context={"z": 1.0}, setups=[su] if self.setups else [],
                          no_trade_reasons=[] if self.setups else ["aucun"])


def engine(now_box, **kw):
    e = Engine(clock=lambda: now_box["now"], **kw)
    e.macro_async = False
    e._calendar = lambda s, now: None  # pas de réseau dans les tests
    return e


# ---------------------------------------------------------------- #1 source primaire, barres en retard, contrats
def test_databento_primary_ignores_tradingview_for_decisions_and_cross_checks_prices(env):
    box = {"now": T0 + timedelta(seconds=5)}
    eng = engine(box, source_filter="databento")
    eng.startup()
    t = T0 - timedelta(minutes=2)
    # TradingView en retard de 10 min (compte gratuit) : ne doit ni piloter ni compter dans le retard mesuré
    add(bar(t, 4000.0, source="databento", received=t + timedelta(minutes=1, seconds=1)),
        bar(t + timedelta(minutes=1), 4001.0, source="databento", received=t + timedelta(minutes=2, seconds=1)),
        bar(t, 4005.0, source="tradingview", received=t + timedelta(minutes=11)))
    eng.tick()
    assert set(eng.bars["close"]) == {4000.0, 4001.0}
    assert max(eng.delays) < 5
    with db.session() as s:
        tv = s.execute(select(db.Bar).where(db.Bar.source == "tradingview")).scalars().one()
        assert tv.processed  # comparée
        inc = s.execute(select(db.Incident).where(db.Incident.component == "controle_croise", db.Incident.code == "prix")).scalars().all()
    assert len(inc) == 1 and "5.00 $" in inc[0].message
    assert any(k.startswith("xsrc:") for k in notes())


def test_tradingview_primary_by_default_ignores_other_sources(env):
    box = {"now": T0 + timedelta(seconds=5)}
    eng = engine(box)
    eng.startup()
    add(bar(T0 - timedelta(minutes=1), 4000.0, source="databento"))
    eng.tick()
    assert eng.primary_source == "tradingview" and len(eng.bars) == 0


def test_late_bar_never_moves_bucket_back_nor_reaches_tracking(env):
    box = {"now": T0 + timedelta(minutes=16)}
    eng = engine(box)
    eng.startup()
    add(bar(T0 + timedelta(minutes=15), 4000.0))
    eng.tick()
    assert eng.current_bucket == pd.Timestamp(T0 + timedelta(minutes=15))
    sid = _signal(created_at=T0 + timedelta(minutes=16), sim_entry=4000.0, sim_entry_ts=T0 + timedelta(minutes=15), sim_stop=3990.0,
                  stop=3990.0, valid_until=T0 + timedelta(minutes=45), exit_deadline=T0 + timedelta(hours=5),
                  meta={"decision_bar_ts": 0, "td": (trading_date(T0) - runner.EPOCH).days, "exit_msess": 1290, "tag": "x"})
    # barre plus ancienne renvoyée en retard, dont le bas toucherait le stop
    add(bar(T0 + timedelta(minutes=3), 3995.0, low=3985.0, received=T0 + timedelta(minutes=16, seconds=30)))
    eng.tick()
    assert eng.current_bucket == pd.Timestamp(T0 + timedelta(minutes=15))
    assert sig_get(sid).status == "ACTIF"
    assert pd.Timestamp(T0 + timedelta(minutes=3)) not in eng.bars.index  # créneau déjà dépassé : pas en mémoire


def test_two_contracts_same_minute_keep_active_contract(env):
    box = {"now": T0 + timedelta(seconds=5)}
    eng = engine(box)
    eng.startup()
    other = next_contract(active_contract(trading_date(T0))).code
    t = T0 - timedelta(minutes=1)
    add(bar(t, 4000.0), bar(t, 4030.0, symbol=other))
    eng.tick()
    assert eng.bars.loc[pd.Timestamp(t), "symbol"] == SYM and eng.bars.loc[pd.Timestamp(t), "close"] == 4000.0
    # au redémarrage aussi
    eng2 = engine(box)
    eng2.startup()
    assert eng2.bars.loc[pd.Timestamp(t), "symbol"] == SYM


# ---------------------------------------------------------------- #9 / #22 mode sécurisé
def test_safe_mode_cancels_unentered_warns_entered_and_stales_queued_alert(env):
    box = {"now": T0}
    eng = engine(box)
    eng.startup()
    history(T0, 60)
    eng2 = engine(box)
    eng2.startup()
    eng2.tick()
    assert eng2.mode in ("actif", "prechauffage")
    td = (trading_date(T0) - runner.EPOCH).days
    meta = {"decision_bar_ts": 0, "td": td, "exit_msess": 1290, "tag": "x"}
    unentered = _signal(key="a", created_at=T0, valid_until=T0 + timedelta(minutes=30), meta=meta)
    entered = _signal(key="b", created_at=T0, valid_until=T0 + timedelta(minutes=30), sim_entry=4000.0, sim_entry_ts=T0,
                      sim_stop=3990.0, exit_deadline=T0 + timedelta(hours=5), meta=meta)
    with db.session() as s:
        from goldpilot.notify.telegram import enqueue
        enqueue(s, f"new:{entered}", "signal", "nouveau signal", entered, True)
    box["now"] = T0 + timedelta(minutes=10)  # plus aucune barre : données périmées
    eng2.tick()
    assert eng2.mode == "securise"
    assert sig_get(unentered).status == "ANNULE"
    e = sig_get(entered)
    assert e.status == "ACTIF" and e.meta.get("entree_interdite")
    n = notes()
    assert f"cancel:{unentered}" in n and f"noentry:{entered}" in n
    assert any(k.startswith(f"safe-open:{entered}") for k in n)

    class FakeTG:
        configured = True
        sent: list = []

        def send_now(self, text):
            self.sent.append(text)
            return True, ""

    deliver_pending(FakeTG(), now=box["now"])
    assert notes()[f"new:{entered}"].status == "perime"


def test_queued_signal_alert_stale_when_engine_paused_or_safe(env):
    sid = _signal(valid_until=utc(2030, 1, 1))
    with db.session() as s:
        from goldpilot.notify.telegram import enqueue
        enqueue(s, f"new:{sid}", "signal", "nouveau", sid, True)
        db.kv_set(s, "engine_mode", {"mode": "pause"})

    class FakeTG:
        configured = True

        def send_now(self, text):
            raise AssertionError("ne doit pas être envoyée")

    deliver_pending(FakeTG(), now=utc(2026, 10, 9, 13, 1))
    n = notes()[f"new:{sid}"]
    assert n.status == "perime" and "pause" in n.error


def test_clock_expiry_and_time_exit_without_bars(env):
    box = {"now": T0}
    eng = engine(box)
    eng.startup()
    with db.session() as s:  # pause : isole les échéances à l'horloge du mode sécurisé (aucune donnée ici)
        db.kv_set(s, "user_mode", "pause")
    meta = {"decision_bar_ts": 0, "td": 1, "exit_msess": 1290, "tag": "x"}
    pend = _signal(key="p", created_at=T0, valid_until=T0 + timedelta(minutes=30), exit_deadline=T0 + timedelta(hours=2), meta=meta)
    pos = _signal(key="q", created_at=T0, valid_until=T0 + timedelta(minutes=30), sim_entry=4000.0, sim_entry_ts=T0, sim_stop=3990.0,
                  exit_deadline=T0 + timedelta(hours=2), meta=meta)
    box["now"] = T0 + timedelta(minutes=31)  # dans le délai de grâce : rien
    eng.tick()
    assert sig_get(pend).status == "ACTIF"
    box["now"] = T0 + timedelta(minutes=34)
    eng.tick()
    assert sig_get(pend).status == "EXPIRE" and sig_get(pos).status == "ACTIF"
    box["now"] = T0 + timedelta(hours=2, minutes=4)
    eng.tick()
    p = sig_get(pos)
    assert p.status == "CLOTURE" and p.sim_exit_reason == "sortie temporelle (sans données)"
    assert p.sim_exit is None and p.sim_r is None and p.sim_pnl_usd is None  # aucun résultat inventé
    n = notes()
    assert "Fermer la position maintenant" in n[f"exit:{pos}"].text and f"expire:{pend}" in n
    with db.session() as s:
        assert db.kv_get(s, "paper_account")["balance"] == get_program(DEFAULT_PROGRAM).account_size


# ---------------------------------------------------------------- #12 perte latente
def test_floating_loss_breach_on_paper_account(env):
    box = {"now": T0 + timedelta(minutes=2)}
    eng = engine(box)
    eng.startup()
    with db.session() as s:
        acct = Account.start(get_program(DEFAULT_PROGRAM))
        acct.floor = acct.balance - 250.0
        eng._save_paper(s, acct, trading_date(T0))
    td = (trading_date(T0) - runner.EPOCH).days
    sid = _signal(created_at=T0, sim_entry=4000.0, sim_entry_ts=T0, sim_stop=3980.0, stop=3980.0, contracts=2,
                  valid_until=T0 + timedelta(minutes=30), exit_deadline=T0 + timedelta(hours=5),
                  meta={"decision_bar_ts": 0, "td": td, "exit_msess": 1290, "tag": "x"})
    add(bar(T0 + timedelta(minutes=1), 4000.0, low=3985.0, high=4001.0, close=4000.5))  # -15 $/oz × 10 × 2 = -300 $
    eng.tick()
    assert sig_get(sid).status == "ACTIF"
    with db.session() as s:
        pa = db.kv_get(s, "paper_account")
    assert pa["breached"] and "latente" in pa["breach_reason"]
    assert f"paper-breach:{sid}" in notes()


# ---------------------------------------------------------------- #13 mode à jour avant la décision ; C4 niveaux
def test_restart_decision_uses_real_mode_and_copies_levels(env):
    end = T0  # créneau 09:45-10:00 NY clôturé par des barres en attente au redémarrage
    history(end - timedelta(minutes=15), 60 * 15)
    history_rows = [bar(end - timedelta(minutes=k), 4000.0, received=end - timedelta(minutes=k - 1, seconds=-2)) for k in range(15, 0, -1)]
    add(*history_rows)
    box = {"now": end + timedelta(seconds=5)}
    eng = engine(box)
    eng.strategy = StubStrategy()
    eng.startup()
    assert eng.mode == "demarrage"
    eng.tick()
    with db.session() as s:
        d = s.execute(select(db.Decision).where(db.Decision.bar_ts == end - timedelta(minutes=15))).scalars().one()
        sys_check = next(c for c in d.risk_checks if c["controle"] == "Système")
        assert sys_check["ok"], d.risk_checks
        assert "anomalie" not in sys_check["detail"]
        if d.signal_id:
            sig = s.get(db.Signal, d.signal_id)
            assert sig.meta["niveaux"]["plus_haut_veille"] == 4010.0


def test_levels_copied_into_signal_meta(env, monkeypatch):
    from goldpilot.risk import engine as risk

    end = T0
    history(end, 60 * 15)
    box = {"now": end + timedelta(seconds=80)}  # créneau clos par l'horloge (délai de grâce écoulé)
    eng = engine(box)
    eng.strategy = StubStrategy()
    eng.startup()

    real = risk.evaluate

    def accept(su, ctx, rs):
        d = real(su, ctx, rs)
        d.accepted, d.contracts, d.risk_usd = True, 1, 80.0
        return d

    monkeypatch.setattr(runner.risk, "evaluate", accept)
    eng.tick()
    with db.session() as s:
        sig = s.execute(select(db.Signal)).scalars().first()
        assert sig is not None and sig.meta["niveaux"]["distances_atr"]["plus_haut_veille"] == -2.5


# ---------------------------------------------------------------- #24 erreur pendant un passage
def test_tick_exception_does_not_lose_decision(env):
    end = T0
    history(end - timedelta(minutes=1), 60 * 15 - 1)
    box = {"now": end + timedelta(seconds=3)}
    eng = engine(box)
    eng.strategy = StubStrategy(setups=False)
    eng.startup()
    add(bar(end - timedelta(minutes=1), 4000.0, received=end + timedelta(seconds=2)))  # clôture le créneau
    calls = {"n": 0}
    orig = eng._end_of_day

    def boom(s, now):
        calls["n"] += 1
        if calls["n"] == 1:
            raise RuntimeError("panne simulée")
        return orig(s, now)

    eng._end_of_day = boom
    with pytest.raises(RuntimeError):
        eng.tick()
    eng.tick()
    with db.session() as s:
        n = s.execute(select(func.count()).select_from(db.Decision).where(db.Decision.bar_ts == end - timedelta(minutes=15))).scalar()
    assert n == 1


# ---------------------------------------------------------------- #16 / C1 reprise après arrêt
def _closed(r, exit_ts, key):
    return _signal(key=key, status="CLOTURE", strategy_version=VERSION, sim_r=r, sim_exit_ts=exit_ts, sim_pnl_usd=r * 100,
                   created_at=exit_ts - timedelta(minutes=30))


VERSION = "v-test"


def test_resume_after_halt_counts_only_trades_after_reset(env):
    box = {"now": T0}
    eng = engine(box)
    eng.version = VERSION
    eng.conf = {"seuils_suspension": {"drawdown_R": -27.27, "serie_pertes": 3}}
    for k in range(4):
        _closed(-1.0, T0 - timedelta(days=2, hours=k), f"l{k}")
    with db.session() as s:
        eng._performance_guard(s, True)
        h = db.kv_get(s, "halt")
        assert h and h["type"] == "performance"
        # reprise (écrit par l'API, contrat C1)
        db.kv_set(s, "halt", None)
        db.kv_set(s, "halt_reset", {"depuis": (T0 - timedelta(days=1)).isoformat(), "version": VERSION})
    _closed(1.5, T0 - timedelta(hours=1), "w1")
    with db.session() as s:
        eng._performance_guard(s, True)
        assert db.kv_get(s, "halt") is None


# ---------------------------------------------------------------- #15 / C2 gouvernance des versions
def test_governance_initialises_then_halts_on_unapproved_version(env):
    box = {"now": T0}
    eng = engine(box)
    if eng.strategy is None:
        pytest.skip("production.json absent")
    eng.startup()
    with db.session() as s:
        a = db.kv_get(s, "approved_version")
        assert a["version"] == eng.version and a["par"] == "initialisation"
        assert s.execute(select(db.Audit).where(db.Audit.action == "version_approuvee")).scalars().first() is not None
        db.kv_set(s, "approved_version", {"version": "ancienne", "approuve_le": T0.isoformat(), "par": "utilisateur"})
    eng2 = engine(box)
    eng2.startup()
    with db.session() as s:
        h = db.kv_get(s, "halt")
    assert h["type"] == "version"
    assert h["raison"] == f"nouvelle version de stratégie non approuvée : {eng2.version} (version approuvée : ancienne)"
    eng2.tick()
    assert eng2.mode == "arret"
    # approbation (API, contrat C2) : la version approuvée = courante, l'arrêt « version » est levé
    with db.session() as s:
        db.kv_set(s, "approved_version", {"version": eng2.version, "approuve_le": T0.isoformat(), "par": "utilisateur"})
        db.kv_set(s, "halt", None)
    eng2.tick()
    assert eng2.mode != "arret"


# ---------------------------------------------------------------- C3 revue périodique
def test_periodic_review_on_saturday_once(env):
    sat = utc(2026, 10, 10, 15, 0)  # samedi
    box = {"now": sat - timedelta(days=1)}
    eng = engine(box)
    if eng.strategy is None:
        pytest.skip("production.json absent")
    eng.startup()
    eng.tick()
    with db.session() as s:
        assert db.kv_get(s, "revue_periodique") is None  # vendredi : rien
    box["now"] = sat
    eng.tick()
    eng.tick()
    with db.session() as s:
        r = db.kv_get(s, "revue_periodique")
        audits = s.execute(select(db.Audit).where(db.Audit.action == "revue_periodique")).scalars().all()
    assert r["date"] == "2026-10-10" and r["version"] == eng.version and r["n"] == 0 and r["esperance_R"] is None
    ref = strategy_config.research_reference()
    assert r["reference"] == ref and r["reference"]["source"] == "research/output/selection,final"
    if (strategy_config.settings().research_dir / "final" / "final.json").exists():
        assert ref["esperance_R_walk_forward"] == 0.081 and ref["esperance_R_2022_2025"] == 0.061
    assert r["seuils"] == eng.conf["seuils_suspension"] and "Aucune modification" in r["conclusion"]
    assert len(audits) == 1 and "review:2026-10-10" in notes()


# ---------------------------------------------------------------- compte simulé : jours de trading seulement
def test_paper_account_days_skip_weekend(env):
    fri = utc(2026, 10, 9, 15, 0)  # vendredi 11:00 NY
    box = {"now": fri}
    eng = engine(box)
    eng.startup()
    for now in (utc(2026, 10, 9, 22, 30), utc(2026, 10, 10, 22, 30), utc(2026, 10, 11, 22, 30)):  # 18:30 NY ven., sam., dim.
        with db.session() as s:
            eng._end_of_day(s, now)
    with db.session() as s:
        pa = db.kv_get(s, "paper_account")
    assert pa["days"] == 1 and pa["day"] == "2026-10-12"
