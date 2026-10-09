"""État du compte FundedNext : même code pour le Monte-Carlo et le suivi en production.

* Plancher « trailing fin de journée » : plus haut solde de fin de journée − perte maximale, mis à jour
  en fin de journée seulement, plafonné au niveau de verrouillage ; ne redescend jamais.
* Toute perte, même latente, qui amène le solde au plancher viole le compte immédiatement.
* Consistance (challenge) : objectif effectif = max(objectif, meilleur jour ÷ 40 %).
"""
from __future__ import annotations

from dataclasses import dataclass, field

from .rules import Program


@dataclass
class Account:
    program: Program
    balance: float
    hwm_eod: float
    floor: float
    day_start_balance: float
    day_pnl: float = 0.0
    best_day: float = 0.0
    days: int = 0
    breached: bool = False
    breach_reason: str = ""
    passed: bool = False
    history: list = field(default_factory=list)

    @classmethod
    def start(cls, program: Program, balance: float | None = None, hwm_eod: float | None = None,
              floor: float | None = None, best_day: float = 0.0) -> "Account":
        b = program.account_size if balance is None else balance
        h = max(b, program.account_size) if hwm_eod is None else hwm_eod
        f = cls.floor_for(program, h) if floor is None else floor
        return cls(program, b, h, f, b, best_day=best_day)

    @staticmethod
    def floor_for(program: Program, hwm: float) -> float:
        f = hwm - program.max_loss
        if program.lock_balance is not None:
            f = min(f, program.lock_balance)
        return max(f, program.initial_floor)

    @property
    def profit(self) -> float:
        return self.balance - self.program.account_size

    def target(self) -> float | None:
        t = self.program.profit_target
        if t is None:
            return None
        if self.program.consistency_pct:
            return max(t, self.best_day / self.program.consistency_pct)
        return t

    def cushion(self) -> float:
        """Distance entre le solde et le plancher de perte maximale."""
        return self.balance - self.floor

    def would_breach(self, loss: float) -> bool:
        return self.balance - loss <= self.floor

    def check_equity(self, floating_pnl: float) -> bool:
        if not self.breached and self.balance + floating_pnl <= self.floor:
            self.breached, self.breach_reason = True, "perte maximale atteinte (latente)"
        return self.breached

    def close_trade(self, pnl: float) -> None:
        self.balance += pnl
        self.day_pnl += pnl
        if not self.breached and self.balance <= self.floor:
            self.breached, self.breach_reason = True, "perte maximale atteinte"

    def end_day(self) -> None:
        self.history.append(self.day_pnl)
        self.days += 1
        self.best_day = max(self.best_day, self.day_pnl)
        self.hwm_eod = max(self.hwm_eod, self.balance)
        if self.program.trailing_eod:
            self.floor = max(self.floor, self.floor_for(self.program, self.hwm_eod))
        tgt = self.target()
        if tgt is not None and not self.breached and self.profit >= tgt:
            self.passed = True
        self.day_start_balance = self.balance
        self.day_pnl = 0.0
