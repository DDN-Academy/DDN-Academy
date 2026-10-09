"""Configuration du programme FundedNext — profil confirmé par l'utilisateur : Futures Flex 50K.

Chaque règle porte sa source officielle, sa date de vérification et son statut :
* « confirmée »      : page officielle, sans contradiction trouvée ;
* « contradictoire » : pages officielles divergentes → la valeur la plus prudente est appliquée ;
* « inconnue »       : non publiée → valeur prudente appliquée et signalée dans l'interface.
Aucune règle n'est inventée. Vérification : 9 octobre 2026 (recherche web sur les domaines officiels ;
accès direct bloqué par l'environnement de développement). À reconfirmer dans ton tableau de bord.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field

CHECKED_ON = "2026-10-09"

S = {
    "flex_rules": "https://helpfutures.fundednext.com/en/articles/17229829-fundednext-futures-flex-challenge-all-rules",
    "flex_page": "https://fundednext.com/futures/flex",
    "flex_funded": "https://helpfutures.fundednext.com/en/articles/17229848-fundednext-futures-flex-fundednext-account-all-rules",
    "legacy_rules": "https://helpfutures.fundednext.com/en/articles/17229536-fundednext-futures-legacy-challenge-all-rules",
    "legacy_page": "https://fundednext.com/futures/legacy",
    "objectives": "https://fundednext.com/general-rules/futures/trading-objectives",
    "overnight": "https://helpfutures.fundednext.com/en/articles/14268506-does-fundednext-futures-allow-overnight-and-weekend-trade-holding",
    "platforms": "https://fundednext.com/general-rules/futures/trading-platforms",
    "news": "https://fundednext.com/general-rules/futures/what-is-allowed",
    "prohibited": "https://helpfutures.fundednext.com/en/articles/14298337-what-are-the-prohibited-trading-strategies-of-fundednext-futures",
    "bots": "https://helpfutures.fundednext.com/en/articles/14298560-is-the-usage-of-automated-trading-systems-eas-and-bots-allowed-in-fundednext-futures",
    "commissions": "https://helpfutures.fundednext.com/en/articles/17230203-how-do-commissions-work-in-futures-trading",
}


@dataclass(frozen=True)
class Rule:
    name: str
    value: str
    status: str
    source: str


@dataclass
class Program:
    key: str
    label: str
    phase: str  # challenge | funded
    account_size: float
    profit_target: float | None
    max_loss: float
    trailing_eod: bool
    lock_balance: float | None
    daily_loss_limit: float | None
    consistency_pct: float | None
    max_micros: int
    flat_by_ny: str
    min_benchmark_days: int | None = None
    benchmark_min_profit: float | None = None
    min_cycle_profit: float | None = None
    min_withdrawal: float | None = None
    max_withdrawal: float | None = None
    reward_share: float | None = None
    rules: list[Rule] = field(default_factory=list)
    user_confirmed: bool = False

    @property
    def initial_floor(self) -> float:
        return self.account_size - self.max_loss

    @property
    def consistency_cap(self) -> float | None:
        if self.consistency_pct and self.profit_target:
            return self.consistency_pct * self.profit_target
        return None

    def unresolved(self) -> list[Rule]:
        return [r for r in self.rules if r.status != "confirmée"]

    def to_dict(self) -> dict:
        d = asdict(self)
        d["checked_on"] = CHECKED_ON
        d["initial_floor"] = self.initial_floor
        d["consistency_cap"] = self.consistency_cap
        return d


COMMON_RULES = [
    Rule("Clôture obligatoire", "toutes les positions fermées avant 15:10 CT (16:10 New York), sinon fermeture automatique ; pas d'overnight ni de week-end", "confirmée", S["overnight"]),
    Rule("Annonces économiques", "trading autorisé (NFP, CPI, FOMC inclus) ; le système bloque quand même les entrées autour des annonces majeures par prudence", "confirmée", S["news"]),
    Rule("Bots / IA", "autorisés hors abus (latence, HFT, tick scalping, micro-scalping < 10 s)", "confirmée", S["bots"]),
    Rule("Signaux externes", "interdit de s'abonner à un service de signaux ou d'utiliser des signaux externes ; outil personnel non confirmé par écrit", "contradictoire", S["prohibited"]),
    Rule("Interdits divers", "spoofing, layering, grille, wash trading, couverture corrélée, marchés gappés/illiquides, < 2 % des limites CME", "confirmée", S["prohibited"]),
    Rule("Commission MGC", "taux tout compris par contrat non publié ; hypothèse 2 $ aller-retour", "inconnue", S["commissions"]),
]

PROGRAMS: dict[str, Program] = {
    "flex_50k_challenge": Program(
        key="flex_50k_challenge", label="FundedNext Futures Flex 50K — Challenge", phase="challenge",
        account_size=50_000, profit_target=2_500, max_loss=1_500, trailing_eod=True, lock_balance=50_100,
        daily_loss_limit=None, consistency_pct=0.40, max_micros=30, flat_by_ny="16:10", user_confirmed=True,
        rules=[
            Rule("Objectif de profit", "2 500 $", "confirmée", S["flex_rules"]),
            Rule("Perte maximale", "1 500 $ sous le plus haut solde de fin de journée, mis à jour en fin de journée", "confirmée", S["flex_rules"]),
            Rule("Verrouillage", "le plancher cesse de monter à 50 100 $", "confirmée", S["flex_page"]),
            Rule("Perte latente", "une perte flottante qui atteint le plancher viole le compte immédiatement", "confirmée", S["objectives"]),
            Rule("Limite journalière", "aucune", "confirmée", S["flex_rules"]),
            Rule("Consistance", "aucun jour > 40 % de l'objectif (1 000 $) ; sinon objectif = meilleur jour ÷ 0,40", "confirmée", S["flex_rules"]),
            Rule("Contrats", "3 mini ou 30 micros", "confirmée", S["flex_rules"]),
        ] + COMMON_RULES),
    "flex_50k_funded": Program(
        key="flex_50k_funded", label="FundedNext Futures Flex 50K — Compte financé", phase="funded",
        account_size=50_000, profit_target=None, max_loss=1_500, trailing_eod=True, lock_balance=50_100,
        daily_loss_limit=None, consistency_pct=None, max_micros=30, flat_by_ny="16:10",
        min_benchmark_days=5, benchmark_min_profit=200, min_cycle_profit=500, min_withdrawal=250,
        max_withdrawal=1_500, reward_share=0.95, user_confirmed=True,
        rules=[
            Rule("Perte maximale", "1 500 $ trailing fin de journée, verrouillée à 50 100 $", "confirmée", S["flex_funded"]),
            Rule("Consistance", "aucune en compte financé", "confirmée", S["flex_funded"]),
            Rule("Retraits", "5 jours ≥ 200 $ et ≥ 500 $ de profit dans le cycle ; 250 $ à 1 500 $ par cycle ; part 95 % ; le premier retrait ramène le plancher à 50 100 $", "confirmée", S["flex_funded"]),
            Rule("Contrats", "3 mini ou 30 micros", "confirmée", S["flex_funded"]),
        ] + COMMON_RULES),
    "legacy_50k_challenge": Program(
        key="legacy_50k_challenge", label="FundedNext Futures Legacy 50K — Challenge (alternative)", phase="challenge",
        account_size=50_000, profit_target=3_000, max_loss=2_000, trailing_eod=True, lock_balance=50_100,
        daily_loss_limit=None, consistency_pct=0.40, max_micros=30, flat_by_ny="16:10",
        rules=[
            Rule("Objectif / perte max", "3 000 $ / 2 000 $ trailing fin de journée", "confirmée", S["legacy_rules"]),
            Rule("Verrouillage", "« au solde initial » ou « solde initial + 100 $ » selon les pages : 50 100 $ appliqué (prudent)", "contradictoire", S["legacy_rules"]),
            Rule("Consistance", "40 % de l'objectif, challenge seulement", "confirmée", S["legacy_page"]),
            Rule("Contrats", "3 mini ou 30 micros", "confirmée", S["legacy_page"]),
        ] + COMMON_RULES),
}

DEFAULT_PROGRAM = "flex_50k_challenge"


def get_program(key: str) -> Program:
    return PROGRAMS[key]
