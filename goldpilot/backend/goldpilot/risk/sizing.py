"""Paramètres de risque (modifiables sans toucher au code) et dimensionnement en contrats MGC entiers.

Budget d'un trade = minimum de :
* risque par trade configuré ;
* fraction du coussin restant au-dessus du plancher (on ne joue jamais tout le coussin) ;
* perte journalière interne restante ;
La consistance 40 % (challenge) n'entre pas dans la taille : elle est gérée par le verrouillage du moteur de risque
(arrêt des signaux du jour quand le profit du jour atteint consistency_lock_fraction × plafond de consistance).
Risque par contrat = (distance au stop + provision de glissement) × 10 onces + commission ; le moteur de risque passe
la pire entrée de la plage acceptable (entrée prévue ± 0,5 ATR, côté opposé au stop).
"""
from __future__ import annotations

import math
from dataclasses import asdict, dataclass

from .account import Account

MGC_OZ = 10.0


@dataclass
class RiskSettings:
    risk_per_trade_usd: float = 150.0
    max_cushion_fraction: float = 0.20
    daily_loss_stop_usd: float = 300.0
    max_trades_per_day: int = 3
    max_losses_per_day: int = 2
    consistency_lock_fraction: float = 0.8  # arrêt du jour quand le profit du jour ≥ 80 % de 1 000 $
    safety_margin_usd: float = 100.0
    slippage_allowance_oz: float = 0.30
    commission_per_contract_rt: float = 2.0
    max_contracts_personal: int = 30

    def validate(self) -> list[str]:
        e = []
        if not 25 <= self.risk_per_trade_usd <= 500:
            e.append("Risque par trade : entre 25 $ et 500 $ (perte maximale du compte : 1 500 $).")
        if not 0.05 <= self.max_cushion_fraction <= 0.35:
            e.append("Fraction du coussin : entre 0,05 et 0,35.")
        if self.daily_loss_stop_usd < self.risk_per_trade_usd:
            e.append("La perte journalière interne doit être au moins égale au risque par trade.")
        if not 1 <= self.max_trades_per_day <= 6:
            e.append("Trades par jour : entre 1 et 6.")
        if not 1 <= self.max_losses_per_day <= self.max_trades_per_day:
            e.append("Pertes par jour : entre 1 et le nombre maximal de trades.")
        if not 0.3 <= self.consistency_lock_fraction <= 1.0:
            e.append("Verrouillage de consistance : entre 0,3 et 1.")
        if self.safety_margin_usd < 0 or self.slippage_allowance_oz < 0 or self.commission_per_contract_rt < 0:
            e.append("Marge, glissement et commission ne peuvent pas être négatifs.")
        if not 1 <= self.max_contracts_personal <= 30:
            e.append("Plafond personnel de contrats : entre 1 et 30 (limite Flex 50K).")
        return e

    def to_dict(self) -> dict:
        return asdict(self)


@dataclass
class Sizing:
    contracts: int
    risk_per_contract: float
    budget: float
    risk_usd: float
    binding: str
    refusal: str = ""


def risk_per_contract(entry: float, stop: float, s: RiskSettings) -> float:
    return (abs(entry - stop) + s.slippage_allowance_oz) * MGC_OZ + s.commission_per_contract_rt


def size(entry: float, stop: float, acct: Account, s: RiskSettings, realized_loss_today: float = 0.0) -> Sizing:
    rpc = risk_per_contract(entry, stop, s)
    if not math.isfinite(rpc) or rpc <= 0 or entry == stop:
        return Sizing(0, rpc, 0, 0, "données", "stop invalide")
    caps = {
        "risque par trade": s.risk_per_trade_usd,
        "coussin au-dessus du plancher": s.max_cushion_fraction * max(0.0, acct.cushion() - s.safety_margin_usd),
        "perte journalière interne": s.daily_loss_stop_usd - max(0.0, realized_loss_today),
    }
    binding = min(caps, key=caps.get)
    budget = max(0.0, caps[binding])
    n = int(math.floor(budget / rpc + 1e-9))
    cap = min(acct.program.max_micros, s.max_contracts_personal)
    if n > cap:
        n, binding = cap, "plafond de contrats"
    if n < 1:
        return Sizing(0, rpc, budget, 0, binding,
                      f"budget {budget:.0f} $ (contrainte : {binding}) inférieur au risque d'un contrat ({rpc:.0f} $)")
    return Sizing(n, rpc, budget, n * rpc, binding)
