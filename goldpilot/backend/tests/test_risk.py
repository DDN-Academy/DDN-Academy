"""Règles FundedNext Flex 50K (compte), dimensionnement et moteur de risque : chaque contrôle bloquant est vérifié."""
from __future__ import annotations

from dataclasses import replace
from datetime import timedelta

import pytest

from goldpilot.calendar.events import Event
from goldpilot.risk import engine as risk
from goldpilot.risk.account import Account
from goldpilot.risk.rules import PROGRAMS, get_program
from goldpilot.risk.sizing import RiskSettings, risk_per_contract, size
from goldpilot.strategy.base import Setup
from goldpilot.timeutil import msess_of

from .conftest import utc

FLEX = get_program("flex_50k_challenge")
FUNDED = get_program("flex_50k_funded")


# ------------------------------------------------------------------------------------------- compte
def test_flex_initial_state():
    a = Account.start(FLEX)
    assert a.balance == 50_000 and a.floor == 48_500 and a.cushion() == 1_500 and a.target() == 2_500


def test_trailing_floor_moves_only_at_end_of_day_and_locks():
    a = Account.start(FLEX)
    a.close_trade(+800)
    assert a.floor == 48_500  # pas de mouvement en cours de journée
    a.end_day()
    assert a.floor == 49_300
    a.close_trade(+1_200)
    a.end_day()
    assert a.floor == 50_100  # verrouillé à 50 100 $ (et non 50 500 $)
    a.close_trade(+500)
    a.end_day()
    assert a.floor == 50_100
    a.close_trade(-600)
    a.end_day()
    assert a.floor == 50_100  # ne redescend jamais


def test_intraday_floating_loss_breaches_immediately():
    a = Account.start(FLEX)
    assert not a.check_equity(-1_499)
    assert a.check_equity(-1_500) and "latente" in a.breach_reason


def test_realized_loss_to_floor_breaches():
    a = Account.start(FLEX)
    a.close_trade(-1_500)
    assert a.breached


def test_consistency_raises_effective_target():
    a = Account.start(FLEX)
    a.close_trade(+1_200)
    a.end_day()
    assert a.best_day == 1_200 and a.target() == pytest.approx(3_000)  # 1 200 / 0,40
    a.close_trade(+1_300)
    a.end_day()
    assert a.profit == 2_500 and not a.passed  # objectif effectif 3 250 $ (meilleur jour 1 300 $)
    a.close_trade(+800)
    a.end_day()
    assert a.passed


def test_funded_has_no_target_nor_consistency():
    a = Account.start(FUNDED)
    a.close_trade(+2_000)
    a.end_day()
    assert a.target() is None and FUNDED.consistency_cap is None


def test_every_rule_has_source_and_status():
    for p in PROGRAMS.values():
        for r in p.rules:
            assert r.source.startswith("https://") and r.status in ("confirmée", "contradictoire", "inconnue")


# ------------------------------------------------------------------------------------------- taille
def test_risk_per_contract_uses_real_mgc_value():
    s = RiskSettings(slippage_allowance_oz=0.3, commission_per_contract_rt=2.0)
    assert risk_per_contract(4000.0, 3990.0, s) == pytest.approx((10 + 0.3) * 10 + 2)  # 1 $ par 0,10 = 10 $ par point


def test_size_floor_and_binding_constraint():
    a = Account.start(FLEX)
    s = RiskSettings(risk_per_trade_usd=250, max_cushion_fraction=0.20, daily_loss_stop_usd=500, safety_margin_usd=100)
    z = size(4000, 3990, a, s)  # 105 $ par contrat ; plafonds : 250 / 0,2 × 1 400 = 280 / 500
    assert z.contracts == 2 and z.binding == "risque par trade" and z.risk_usd == pytest.approx(210)


def test_size_limited_by_cushion():
    a = Account.start(FLEX, balance=48_900)  # coussin 400 $
    s = RiskSettings(risk_per_trade_usd=250, max_cushion_fraction=0.20, safety_margin_usd=100)
    z = size(4000, 3998, a, s)  # budget = 0,2 × 300 = 60 $ ; 25 $ par contrat
    assert z.binding == "coussin au-dessus du plancher" and z.contracts == 2


def test_size_capped_by_contract_limit():
    a = Account.start(FLEX)
    s = RiskSettings(risk_per_trade_usd=500, max_cushion_fraction=0.35, daily_loss_stop_usd=500, slippage_allowance_oz=0,
                     commission_per_contract_rt=0, max_contracts_personal=5)
    z = size(4000, 3999.9, a, s)
    assert z.contracts == 5 and z.binding == "plafond de contrats"


def test_size_refuses_when_one_contract_is_too_risky():
    a = Account.start(FLEX)
    z = size(4000, 3950, a, RiskSettings(risk_per_trade_usd=150))
    assert z.contracts == 0 and "inférieur au risque d'un contrat" in z.refusal


def test_size_refuses_invalid_stop():
    assert size(4000, 4000, Account.start(FLEX), RiskSettings()).contracts == 0


def test_daily_loss_reduces_budget():
    a = Account.start(FLEX)
    s = RiskSettings(risk_per_trade_usd=250, daily_loss_stop_usd=300)
    assert size(4000, 3990, a, s, realized_loss_today=200).binding == "perte journalière interne"


@pytest.mark.parametrize("field,value", [("risk_per_trade_usd", 10), ("risk_per_trade_usd", 501), ("max_cushion_fraction", 0.5),
                                         ("daily_loss_stop_usd", 100), ("max_trades_per_day", 7), ("max_losses_per_day", 4),
                                         ("consistency_lock_fraction", 0.1), ("commission_per_contract_rt", -1),
                                         ("max_contracts_personal", 31)])
def test_risk_settings_bounds(field, value):
    assert RiskSettings(**{field: value}).validate()


def test_default_settings_valid():
    assert not RiskSettings().validate()


# ------------------------------------------------------------------------------------------- moteur de risque
NOW = utc(2026, 10, 7, 14, 0, 5)  # mercredi 10:00:05 New York


def setup(**kw) -> Setup:
    s = Setup(strategy="S1", config_id="S1|t", side=1, entry_type="market", entry=None, stop=3990.0, target=None, trail_atr=3.0,
              atr=4.0, ref_price=4000.0, decision_bar_ts=0, decision_ts=0, valid_until_ts=0, exit_msess=msess_of("15:30"), td=1,
              tag="ext_long", rationale="", invalidation="")
    return replace(s, **kw)


def ctx(**kw) -> risk.RiskContext:
    c = risk.RiskContext(now=NOW, system_mode="actif", data_ok=True, data_problems=[], last_price=4000.5, account=Account.start(FLEX),
                         account_state_known=True, account_note="compte simulé", trades_today=0, losses_today=0, realized_loss_today=0.0,
                         open_or_pending_signals=0, duplicate=False, events=[])
    return replace(c, **kw)


S = RiskSettings(risk_per_trade_usd=250, daily_loss_stop_usd=500)


def refused_by(d: risk.RiskDecision) -> set[str]:
    return {c.name for c in d.checks if c.blocking and not c.ok}


def test_nominal_signal_accepted():
    d = risk.evaluate(setup(), ctx(), S)
    # taille calculée sur la pire entrée de la plage (4 000 + 0,5 × 4 ATR = 4 002) : (12 + 0,3) × 10 + 2 = 125 $ par contrat
    assert d.accepted and d.contracts == 2 and d.risk_usd == pytest.approx(250), d.refusals


@pytest.mark.parametrize("kw,name", [
    ({"system_mode": "pause"}, "Système"),
    ({"system_mode": "securise"}, "Système"),
    ({"data_ok": False, "data_problems": ["données périmées"]}, "Données de marché"),
    ({"duplicate": True}, "Pas de doublon"),
    ({"open_or_pending_signals": 1}, "Une seule position à la fois"),
    ({"trades_today": 3}, "Trades du jour"),
    ({"losses_today": 2}, "Pertes du jour"),
    ({"realized_loss_today": 500.0}, "Perte journalière interne"),
    ({"last_price": 4003.0}, "Prix encore exploitable"),  # 3 $ > 0,5 ATR = 2 $
    ({"last_price": None}, "Prix encore exploitable"),
])
def test_each_blocking_check(kw, name):
    d = risk.evaluate(setup(), ctx(**kw), S)
    assert not d.accepted and d.contracts == 0 and name in refused_by(d)


def test_breached_account_blocks():
    a = Account.start(FLEX)
    a.close_trade(-1_500)
    assert "Compte non violé" in refused_by(risk.evaluate(setup(), ctx(account=a), S))


def test_consistency_lock_blocks_after_big_day():
    a = Account.start(FLEX)
    a.close_trade(+850)  # 0,8 × 1 000 $ = 800 $
    assert "Consistance 40 %" in refused_by(risk.evaluate(setup(), ctx(account=a), S))


def test_exit_after_fundednext_cutoff_blocks():
    assert "Horaires FundedNext" in refused_by(risk.evaluate(setup(exit_msess=msess_of("16:00")), ctx(), S))
    late = ctx(now=utc(2026, 10, 7, 19, 31))  # 15:31 New York, après la sortie prévue
    assert "Horaires FundedNext" in refused_by(risk.evaluate(setup(), late, S))


def test_news_blackout_blocks():
    ev = Event("bls", "x", "Consumer Price Index", "fort", NOW + timedelta(minutes=25), "https://www.bls.gov")
    assert "Annonces économiques" in refused_by(risk.evaluate(setup(), ctx(events=[ev]), S))
    far = replace(ev, ts=NOW + timedelta(minutes=45))
    assert risk.evaluate(setup(), ctx(events=[far]), S).accepted
    medium = replace(ev, impact="moyen")
    assert risk.evaluate(setup(), ctx(events=[medium]), S).accepted


def test_cushion_check_blocks_when_risk_plus_margin_reaches_floor():
    a = Account.start(FLEX, balance=48_700)  # coussin 200 $
    s = RiskSettings(risk_per_trade_usd=250, max_cushion_fraction=0.35, safety_margin_usd=100)
    d = risk.evaluate(setup(stop=3999.0), ctx(account=a), s)  # 15 $ par contrat
    assert d.accepted and d.risk_usd + 100 < 200
    s2 = RiskSettings(risk_per_trade_usd=250, max_cushion_fraction=0.35, safety_margin_usd=190)
    assert not risk.evaluate(setup(stop=3999.0), ctx(account=a), s2).accepted


def test_invalid_settings_block():
    assert "Paramètres de risque" in refused_by(risk.evaluate(setup(), ctx(), RiskSettings(risk_per_trade_usd=5)))


def test_unconfirmed_program_blocks():
    assert "Programme FundedNext" in refused_by(risk.evaluate(setup(), ctx(account=Account.start(get_program("legacy_50k_challenge"))), S))


def test_uncertain_rule_blocks_only_in_real_mode_without_written_confirmation():
    sim = risk.evaluate(setup(), ctx(), S)
    chk = next(c for c in sim.checks if c.name == "Règles incertaines")
    assert sim.accepted and not chk.blocking and "Signaux externes" in chk.detail
    real = risk.evaluate(setup(), ctx(real_mode=True), S)
    assert "Règles incertaines" in refused_by(real)
    assert risk.evaluate(setup(), ctx(real_mode=True, rules_confirmed_in_writing=True), S).accepted


def test_unknown_account_state_is_reported_not_hidden():
    d = risk.evaluate(setup(), ctx(account_state_known=False, account_note="solde jamais renseigné"), S)
    c = next(c for c in d.checks if c.name == "État du compte")
    assert not c.ok and not c.blocking and d.accepted


def test_short_side_symmetry():
    d = risk.evaluate(setup(side=-1, stop=4010.0, tag="ext_short"), ctx(last_price=3999.5), S)
    assert d.accepted and d.contracts == 2
