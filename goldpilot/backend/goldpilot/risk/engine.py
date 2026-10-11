"""Moteur de risque : contrôle obligatoire de chaque signal avant émission. Il est prioritaire sur la
stratégie et sur tout autre module : un seul contrôle « bloquant » en échec suffit à refuser le signal.

Chaque contrôle est enregistré (nom, résultat, explication) dans le journal des décisions.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timedelta

from ..calendar.events import Blackout, Event, blocking_event
from ..strategy.base import Setup
from ..timeutil import HOLIDAY_SAFETY_MIN, fmt_ny, msess, msess_of, session_close_ny, trading_date
from .account import Account
from .sizing import RiskSettings, Sizing, size

LATEST_EXIT = msess_of("15:45")  # FundedNext ferme à 16:10 New York ; marge de 25 minutes


@dataclass
class Check:
    name: str
    ok: bool
    detail: str
    blocking: bool = True


@dataclass
class RiskDecision:
    accepted: bool
    contracts: int
    risk_usd: float
    checks: list[Check] = field(default_factory=list)
    sizing: Sizing | None = None

    @property
    def refusals(self) -> list[str]:
        return [f"{c.name} : {c.detail}" for c in self.checks if not c.ok and c.blocking]


@dataclass
class RiskContext:
    now: datetime
    system_mode: str  # actif | pause | securise | arret
    data_ok: bool
    data_problems: list[str]
    last_price: float | None
    account: Account
    account_state_known: bool
    account_note: str
    trades_today: int
    losses_today: int
    realized_loss_today: float
    open_or_pending_signals: int
    duplicate: bool
    events: list[Event]
    blackout: Blackout = field(default_factory=Blackout)
    real_mode: bool = False  # signal destiné au compte réel (sinon : simulation)
    rules_confirmed_in_writing: bool = False  # confirmation écrite de FundedNext déclarée (règle « signaux externes »)


def evaluate(setup: Setup, ctx: RiskContext, settings: RiskSettings) -> RiskDecision:
    C: list[Check] = []
    add = C.append
    add(Check("Système", ctx.system_mode == "actif", {"actif": "moteur actif", "pause": "génération de signaux suspendue par toi",
                                                     "securise": "mode sécurisé (anomalie détectée)", "arret": "arrêt de sécurité"}.get(ctx.system_mode, ctx.system_mode)))
    add(Check("Données de marché", ctx.data_ok, "fraîches et cohérentes" if ctx.data_ok else "; ".join(ctx.data_problems) or "indisponibles"))
    errs = settings.validate()
    add(Check("Paramètres de risque", not errs, "valides" if not errs else " ; ".join(errs)))
    a = ctx.account
    add(Check("Programme FundedNext", a.program.user_confirmed, a.program.label if a.program.user_confirmed else "programme non confirmé"))
    # Règle contradictoire = incertitude sur la conformité : bloquant en réel (cahier des charges §8). Les règles
    # « inconnues » (ex. commission) sont couvertes par une hypothèse prudente dans les paramètres de risque.
    uncertain = [r.name for r in a.program.rules if r.status == "contradictoire"]
    if not uncertain:
        add(Check("Règles incertaines", True, "aucune"))
    elif ctx.rules_confirmed_in_writing:
        add(Check("Règles incertaines", True, "levées par la confirmation écrite de FundedNext que tu as déclarée"))
    elif ctx.real_mode:
        add(Check("Règles incertaines", False, "bloquant tant que FundedNext n'a pas confirmé par écrit : " + ", ".join(uncertain)))
    else:
        add(Check("Règles incertaines", True, "non bloquant en simulation ; bloquant en réel sans confirmation écrite de FundedNext : "
                  + ", ".join(uncertain), blocking=False))
    add(Check("État du compte", ctx.account_state_known, ctx.account_note, blocking=False))
    add(Check("Compte non violé", not a.breached, "aucune violation" if not a.breached else a.breach_reason))
    add(Check("Une seule position à la fois", ctx.open_or_pending_signals == 0,
              "aucun signal en cours" if ctx.open_or_pending_signals == 0 else "un signal est déjà en cours"))
    add(Check("Pas de doublon", not ctx.duplicate, "signal inédit" if not ctx.duplicate else "signal déjà émis pour cette barre"))
    add(Check("Trades du jour", ctx.trades_today < settings.max_trades_per_day, f"{ctx.trades_today}/{settings.max_trades_per_day}"))
    add(Check("Pertes du jour", ctx.losses_today < settings.max_losses_per_day, f"{ctx.losses_today}/{settings.max_losses_per_day}"))
    add(Check("Perte journalière interne", ctx.realized_loss_today < settings.daily_loss_stop_usd,
              f"{ctx.realized_loss_today:.0f} $ / {settings.daily_loss_stop_usd:.0f} $"))
    cap = a.program.consistency_cap
    if cap is not None:
        lock = settings.consistency_lock_fraction * cap
        add(Check("Consistance 40 %", a.day_pnl < lock, f"profit du jour {a.day_pnl:.0f} $ (arrêt à {lock:.0f} $ pour ne pas relever l'objectif)"))
    # Sortie au plus tard à min(15:45 New York, clôture réelle du CME − 25 min) : jours fériés et clôtures anticipées.
    close = session_close_ny(trading_date(ctx.now))
    if close is None:
        add(Check("Horaires FundedNext", False, "marché fermé (jour férié CME)"))
    else:
        latest = min(LATEST_EXIT, msess(close) - HOLIDAY_SAFETY_MIN)
        early = latest < LATEST_EXIT
        exit_ok = setup.exit_msess <= latest
        limit_txt = fmt_ny(close - timedelta(minutes=HOLIDAY_SAFETY_MIN)) if early else "15:45 New York"
        why = f"clôture anticipée du CME à {fmt_ny(close)}" if early else "clôture FundedNext 16:10"
        add(Check("Horaires FundedNext", exit_ok and msess(ctx.now) < setup.exit_msess,
                  f"sortie prévue avant {limit_txt} ({why})" if exit_ok
                  else f"sortie prévue trop tardive : limite {limit_txt} ({why})"))
    horizon = timedelta(minutes=30)
    ev = blocking_event(ctx.events, ctx.now, horizon, ctx.blackout)
    add(Check("Annonces économiques", ev is None,
              "aucune annonce majeure dans la fenêtre de prudence" if ev is None else f"{ev.title} à {fmt_ny(ev.ts)}"))
    if ctx.last_price is not None:
        drift = abs(ctx.last_price - setup.planned_entry)
        lim = setup.max_price_drift_atr * setup.atr
        add(Check("Prix encore exploitable", drift <= lim, f"écart {drift:.2f} $ (max {lim:.2f} $)"))
    else:
        add(Check("Prix encore exploitable", False, "prix actuel inconnu"))
    # Taille calculée sur la pire entrée de la plage acceptable (entrée prévue ± écart toléré, côté opposé au stop) :
    # le risque réel ne dépasse jamais le budget, même en entrant au bord de la plage annoncée.
    worst_entry = setup.planned_entry + setup.side * setup.max_price_drift_atr * setup.atr
    sz = size(worst_entry, setup.stop, a, settings, ctx.realized_loss_today)
    add(Check("Taille de position", sz.contracts >= 1,
              f"{sz.contracts} contrat(s), risque {sz.risk_usd:.0f} $ (contrainte : {sz.binding})" if sz.contracts else sz.refusal))
    if sz.contracts >= 1:
        add(Check("Coussin de perte maximale", not a.would_breach(sz.risk_usd + settings.safety_margin_usd),
                  f"coussin {a.cushion():.0f} $, risque {sz.risk_usd:.0f} $ + marge {settings.safety_margin_usd:.0f} $"))
    accepted = all(c.ok for c in C if c.blocking)
    return RiskDecision(accepted, sz.contracts if accepted else 0, sz.risk_usd if accepted else 0.0, C, sz)
