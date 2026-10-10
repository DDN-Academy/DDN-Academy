"""Cycle de vie des signaux et suivi des positions simulées (même simulateur que le backtest).

Statuts affichés :
* EN_ATTENTE : entrée conditionnelle (ordre stop/limite) pas encore déclenchée ;
* ACTIF      : entrée immédiate signalée, ou entrée conditionnelle déclenchée ; position simulée suivie ;
* ANNULE     : invalidé avant exécution (prix sorti de la plage, mode sécurisé, annonce, action de l'utilisateur) ;
* EXPIRE     : validité écoulée sans déclenchement ;
* CLOTURE    : position simulée sortie (stop, stop suiveur, objectif, fermeture horaire).
La « position réellement exécutée » n'existe que si tu la déclares (aucune connexion au courtier).
"""
from __future__ import annotations

import json
import logging
from datetime import datetime, timedelta, timezone

from sqlalchemy import select

from .. import db
from ..notify import messages
from ..notify.telegram import enqueue
from ..research.execution import BASE_COSTS, ExecutionSimulator, OpenPosition
from ..risk.sizing import MGC_OZ
from ..strategy.base import Setup
from ..timeutil import ny_time_on, trading_date

log = logging.getLogger("goldpilot.signals")
OPEN_STATUSES = ("EN_ATTENTE", "ACTIF")


def ns(dt: datetime) -> int:
    return int(dt.timestamp() * 1_000_000_000)


def dt_ns(x: int) -> datetime:
    return datetime.fromtimestamp(x / 1_000_000_000, tz=timezone.utc)


def setup_from_signal(sig: db.Signal) -> Setup:
    m = sig.meta or {}
    return Setup(
        strategy=m.get("strategy", "?"), config_id=m.get("config_id", "?"), side=sig.side, entry_type=sig.entry_type,
        entry=None if sig.entry_type == "market" else sig.entry_ref, stop=sig.stop, target=sig.target,
        trail_atr=sig.trail_atr, atr=sig.atr, ref_price=sig.entry_ref, decision_bar_ts=int(m.get("decision_bar_ts", 0)),
        decision_ts=ns(sig.created_at), valid_until_ts=ns(sig.valid_until), exit_msess=int(m["exit_msess"]),
        td=int(m["td"]), tag=m.get("tag", ""), rationale=sig.rationale, invalidation=sig.invalidation,
    )


def simulator_for(sig: db.Signal) -> ExecutionSimulator:
    sim = ExecutionSimulator(BASE_COSTS)
    su = setup_from_signal(sig)
    m = sig.meta or {}
    if sig.sim_entry is None:
        sim.pending = [su]
    else:
        sim.position = OpenPosition(su, sig.side, sig.sim_entry, ns(sig.sim_entry_ts), sig.sim_stop, sig.stop, sig.target,
                                    float(m.get("extreme", sig.sim_entry)), int(m.get("bars", 0)))
    return sim


def _event(s, sig: db.Signal, kind: str, **detail) -> None:
    s.add(db.SignalEvent(signal_id=sig.id, kind=kind, detail=detail))


def _persist_position(sig: db.Signal, sim: ExecutionSimulator) -> None:
    p = sim.position
    m = dict(sig.meta or {})
    if p is not None:
        sig.sim_stop = p.stop
        m["extreme"], m["bars"] = p.extreme, p.bars
    sig.meta = m


def on_base_bar(s, sig: db.Signal, ts: datetime, o: float, h: float, l: float, c: float, atr: float, td: int, msess_: int,
                notify: bool) -> None:
    """Applique une barre de base (1 min en direct) à un signal ouvert.

    Seules les barres commençant à ou après la clôture de la barre de décision sont prises en compte
    (la barre suivante commence avant l'instant où le moteur crée le signal)."""
    decision_close = dt_ns(int((sig.meta or {}).get("decision_bar_ts", 0)) + 15 * 60 * 1_000_000_000)
    if sig.status not in OPEN_STATUSES or ts < decision_close:
        return
    m = dict(sig.meta or {})
    # Fenêtre d'entrée manuelle : prévenir une fois si le prix sort de la plage annoncée
    if ts < sig.valid_until and not m.get("band_exceeded") and abs(c - sig.entry_ref) > sig.entry_max_drift:
        m["band_exceeded"] = True
        sig.meta = m
        _event(s, sig, "plage_depassee", prix=c)
        enqueue(s, f"band:{sig.id}", "plage", messages.status_change(
            sig, "Ne plus entrer", f"Le prix ({c:.1f}) est sorti de la plage d'entrée prévue. Si tu n'es pas déjà entré, laisse passer."),
            sig.id, notify)
    sim = simulator_for(sig)
    for ev in sim.on_bar(ns(ts), o, h, l, c, atr, td, msess_):
        if ev.kind == "fill":
            sig.sim_entry, sig.sim_entry_ts, sig.sim_stop = ev.price, ts, sig.stop
            if sig.status == "EN_ATTENTE":
                sig.status = "ACTIF"
                enqueue(s, f"fill:{sig.id}", "declenche", messages.status_change(
                    sig, "Entrée déclenchée", f"Prix d'entrée simulé {ev.price:.1f}. Stop {sig.stop:.1f}."), sig.id, notify)
            _event(s, sig, "entree_simulee", prix=ev.price)
        elif ev.kind == "exit":
            t = ev.trade
            sig.status, sig.sim_exit, sig.sim_exit_ts, sig.sim_exit_reason = "CLOTURE", t.exit_px, ts, t.exit_reason
            sig.sim_r = t.r
            sig.sim_pnl_usd = t.pnl_oz * MGC_OZ * sig.contracts
            sig.status_reason = t.exit_reason
            _event(s, sig, "sortie_simulee", prix=t.exit_px, raison=t.exit_reason, r=t.r)
            verb = "Fermer la position maintenant" if t.exit_reason == "sortie temporelle" else "Position sortie"
            enqueue(s, f"exit:{sig.id}", "sortie", messages.status_change(
                sig, verb, f"Sortie simulée {t.exit_px:.1f} ({t.exit_reason}) : {t.r:+.2f} R, {sig.sim_pnl_usd:+.0f} $ "
                f"pour {sig.contracts} contrat(s)."), sig.id, notify)
        elif ev.kind == "expire":
            sig.status, sig.status_reason = "EXPIRE", "validité écoulée sans déclenchement"
            _event(s, sig, "expire")
            enqueue(s, f"expire:{sig.id}", "expire", messages.status_change(sig, "Signal expiré", "Aucune entrée : la validité est écoulée."), sig.id, notify)
    if sig.status in OPEN_STATUSES:
        _persist_position(sig, sim)


def on_decision_bar_close(s, sig: db.Signal, h: float, l: float, atr: float, price: float, notify: bool) -> None:
    """Clôture d'une barre de décision : mise à jour du stop suiveur (effective dès la barre suivante)."""
    if sig.status != "ACTIF" or sig.sim_entry is None:
        return
    sim = simulator_for(sig)
    before = sim.position.stop
    sim.end_of_decision_bar(h, l, atr)
    after = sim.position.stop
    _persist_position(sig, sim)
    if abs(after - before) >= 0.1 - 1e-9:
        _event(s, sig, "stop_deplace", avant=before, apres=after)
        enqueue(s, f"stop:{sig.id}:{after:.1f}", "stop", messages.stop_update(sig, after, price), sig.id, notify)


def cancel_open(s, reason: str, notify: bool, only_pending: bool = False) -> int:
    rows = s.execute(select(db.Signal).where(db.Signal.status.in_(OPEN_STATUSES))).scalars().all()
    n = 0
    for sig in rows:
        if sig.status == "ACTIF" and (only_pending or sig.sim_entry is not None):
            continue
        sig.status, sig.status_reason = "ANNULE", reason
        _event(s, sig, "annule", raison=reason)
        enqueue(s, f"cancel:{sig.id}", "annule", messages.status_change(sig, "Signal annulé", reason), sig.id, notify)
        n += 1
    return n


def open_signals(s) -> list[db.Signal]:
    return s.execute(select(db.Signal).where(db.Signal.status.in_(OPEN_STATUSES)).order_by(db.Signal.created_at)).scalars().all()


def today_stats(s, now: datetime) -> dict:
    start = ny_time_on(trading_date(now), "18:00")  # début de la journée de trading (18:00 New York la veille)
    rows = s.execute(select(db.Signal).where(db.Signal.created_at >= start, db.Signal.status != "ANNULE")).scalars().all()
    closed = [r for r in rows if r.status == "CLOTURE" and r.sim_pnl_usd is not None]
    losses = [r for r in closed if r.sim_pnl_usd < 0]
    return {"trades": len([r for r in rows if r.sim_entry is not None or r.status == "ACTIF"]),
            "losses": len(losses), "realized_loss": float(-sum(r.sim_pnl_usd for r in losses)),
            "pnl": float(sum(r.sim_pnl_usd for r in closed))}


def dumps(o) -> str:
    return json.dumps(o, default=str, ensure_ascii=False)
