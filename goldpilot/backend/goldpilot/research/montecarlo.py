"""Monte-Carlo FundedNext : réussite du challenge, violation, durée, survie et retraits en compte financé.

Méthode : tirage avec remise de journées de trading entières (jours sans trade compris), rejouées avec
les règles du programme (risk/account.py) et le dimensionnement de production (risk/sizing.py) en
contrats MGC entiers. Le risque par once de chaque trade est converti en fraction du prix puis appliqué
au prix de référence (volatilité relative plus stable que la volatilité en dollars) ; le résultat en R
est conservé.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass

import numpy as np
import pandas as pd

from ..risk.account import Account
from ..risk.rules import Program
from ..risk.sizing import MGC_OZ, RiskSettings, size


@dataclass
class MCResult:
    risk_per_trade_usd: float
    trajectoires: int
    horizon_jours: int
    p_reussite: float
    p_violation: float
    p_en_cours: float
    jours_median_reussite: float | None
    jours_p75_reussite: float | None
    p_objectif_releve: float
    profit_median: float
    profit_p05: float
    trades_moyens: float
    survie: dict
    retraits: dict

    def to_dict(self) -> dict:
        return asdict(self)


def _days(trades: pd.DataFrame, all_days: np.ndarray) -> list[list[tuple[float, float]]]:
    t = trades.sort_values("entry_ts")
    by: dict[int, list] = {}
    for td, r, risk, px in zip(t["td"], t["r"], t["planned_risk"], t["planned_entry"]):
        by.setdefault(int(td), []).append((float(r), float(risk) / float(px)))
    return [by.get(int(d), []) for d in all_days]


def simulate(trades: pd.DataFrame, all_days: np.ndarray, program: Program, settings: RiskSettings,
             price: float = 4000.0, n_paths: int = 10_000, horizon: int = 120, seed: int = 21,
             checkpoints=(21, 63, 126, 252)) -> MCResult:
    days = _days(trades, all_days)
    rng = np.random.default_rng(seed)
    nd = len(days)
    passed_at, breached_at, raised, profits, taken, paid_all = [], [], 0, [], [], []
    alive = {c: 0 for c in checkpoints}
    funded = program.phase == "funded"
    for _ in range(n_paths):
        a = Account.start(program)
        p_day = b_day = None
        n_tr = 0
        bench = 0
        cycle_start = a.balance
        paid = 0.0
        withdrawals = 0
        for k, di in enumerate(rng.integers(0, nd, size=horizon)):
            n_today = losses = 0
            loss_usd = 0.0
            cap = program.consistency_cap
            for r, risk_pct in days[di]:
                if a.breached or n_today >= settings.max_trades_per_day or losses >= settings.max_losses_per_day:
                    break
                if loss_usd >= settings.daily_loss_stop_usd:
                    break
                if cap is not None and a.day_pnl >= settings.consistency_lock_fraction * cap:
                    break
                risk_oz = risk_pct * price
                sz = size(price, price - risk_oz, a, settings, loss_usd)
                if sz.contracts < 1:
                    continue
                pnl = r * risk_oz * MGC_OZ * sz.contracts
                a.close_trade(pnl)
                n_tr += 1
                n_today += 1
                if pnl < 0:
                    losses += 1
                    loss_usd -= pnl
            day = a.day_pnl
            a.end_day()
            if funded and not a.breached:
                if day >= (program.benchmark_min_profit or 0):
                    bench += 1
                avail = a.balance - (program.lock_balance or program.account_size)
                if (bench >= (program.min_benchmark_days or 0) and a.balance - cycle_start >= (program.min_cycle_profit or 0)
                        and avail >= (program.min_withdrawal or 0)):
                    w = min(program.max_withdrawal or avail, avail)
                    a.balance -= w
                    a.day_start_balance = a.balance
                    paid += w * (program.reward_share or 1.0)
                    withdrawals += 1
                    bench = 0
                    cycle_start = a.balance
                    if program.lock_balance is not None:
                        a.floor = max(a.floor, program.lock_balance)
            if a.breached:
                b_day = k + 1
                break
            if not funded and a.passed:
                p_day = k + 1
                break
        if not funded and program.profit_target and a.target() and a.target() > program.profit_target + 1e-9:
            raised += 1
        passed_at.append(p_day)
        breached_at.append(b_day)
        profits.append(a.profit + (paid / (program.reward_share or 1.0)))
        taken.append(n_tr)
        paid_all.append(paid)
        for c in checkpoints:
            if b_day is None or b_day > c:
                alive[c] += 1
    ok = np.array([p is not None for p in passed_at])
    br = np.array([b is not None for b in breached_at])
    pdays = np.array([p for p in passed_at if p is not None], dtype=float)
    pr = np.array(profits)
    paid_arr = np.array(paid_all)
    return MCResult(
        risk_per_trade_usd=settings.risk_per_trade_usd, trajectoires=n_paths, horizon_jours=horizon,
        p_reussite=float(ok.mean()), p_violation=float(br.mean()), p_en_cours=float((~ok & ~br).mean()),
        jours_median_reussite=float(np.median(pdays)) if len(pdays) else None,
        jours_p75_reussite=float(np.quantile(pdays, 0.75)) if len(pdays) else None,
        p_objectif_releve=raised / n_paths, profit_median=float(np.median(pr)), profit_p05=float(np.quantile(pr, 0.05)),
        trades_moyens=float(np.mean(taken)),
        survie={str(c): alive[c] / n_paths for c in checkpoints if c <= horizon},
        retraits=({"moyenne_payee": float(paid_arr.mean()), "mediane_payee": float(np.median(paid_arr)),
                   "p_au_moins_un": float((paid_arr > 0).mean())} if funded else {}),
    )


def drawdown_distribution(r: np.ndarray, n_trades: int, n_paths: int = 5000, seed: int = 4) -> dict:
    """Distribution du drawdown max (R) et de la plus longue série de pertes pour n_trades trades."""
    rng = np.random.default_rng(seed)
    dds, sts = [], []
    for _ in range(n_paths):
        x = rng.choice(r, size=n_trades, replace=True)
        eq = np.concatenate([[0.0], np.cumsum(x)])
        dds.append(float((eq - np.maximum.accumulate(eq)).min()))
        b = c = 0
        for v in x:
            c = c + 1 if v <= 0 else 0
            b = max(b, c)
        sts.append(b)
    dds, sts = np.array(dds), np.array(sts)
    return {"n_trades": n_trades, "dd_median": float(np.median(dds)), "dd_p05": float(np.quantile(dds, 0.05)),
            "dd_p01": float(np.quantile(dds, 0.01)), "serie_pertes_p95": float(np.quantile(sts, 0.95)),
            "serie_pertes_p99": float(np.quantile(sts, 0.99))}
