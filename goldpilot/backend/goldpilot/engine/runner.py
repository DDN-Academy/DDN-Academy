"""Moteur temps réel GoldPilot (processus « engine »).

Boucle (toutes les 2 s) :
1. nouvelles barres de base reçues (webhook TradingView, Databento ou rejeu) → suivi des signaux ouverts ;
2. clôture des barres de décision de 15 min → stop suiveur, analyse de la stratégie, moteur de risque,
   création éventuelle d'un signal ; CHAQUE analyse est journalisée (signal, refus ou absence de setup) ;
3. modes : pause (toi), arrêt de sécurité (anomalie grave), mode sécurisé (données), préchauffage ;
4. calendrier officiel, avertissements d'annonces, rappel de changement d'échéance ;
5. fin de journée : plancher trailing du compte simulé ; seuils de suspension automatique ;
6. envoi des notifications en attente ; battement de cœur pour le site.
"""
from __future__ import annotations

import logging
import time
from collections import deque
from datetime import datetime, timedelta, timezone
from typing import Callable

import pandas as pd
from sqlalchemy import func, select

from .. import db
from ..calendar.events import Event, next_event, parse_ics, seed_events
from ..config import settings
from ..marketdata import quality as dq
from ..marketdata.contracts import active_contract, add_bdays, next_contract
from ..notify import messages
from ..notify.telegram import Telegram, deliver_pending, enqueue
from ..research.data import resample
from ..risk import engine as risk
from ..risk.account import Account
from ..risk.rules import DEFAULT_PROGRAM, get_program
from ..risk.sizing import RiskSettings
from ..signals import manager as sm
from ..strategy.base import StrategyState
from ..strategy.candidates import arrays
from ..timeutil import fmt_ny, fmt_paris, is_open, msess, trading_date, utcnow
from . import strategy_config

log = logging.getLogger("goldpilot.engine")
BUCKET = timedelta(minutes=15)
GRACE = timedelta(seconds=75)
KEEP = timedelta(days=8)
MIN_DECISION_BARS = 45
EPOCH = datetime(1970, 1, 1).date()


def td_int(dt: datetime) -> int:
    """Journée de trading en jours depuis 1970 (même convention que strategy.indicators.time_columns)."""
    return (trading_date(dt) - EPOCH).days


def risk_settings(s) -> RiskSettings:
    raw = db.kv_get(s, "risk_settings")
    if not raw:
        conf = strategy_config.load_production() or {}
        return RiskSettings(**conf.get("risk_settings_default", {}))
    return RiskSettings(**raw)


class Engine:
    def __init__(self, clock: Callable[[], datetime] = utcnow, telegram: Telegram | None = None, source_filter: str | None = None):
        st = settings()
        self.clock = clock
        self.conf = strategy_config.load_production()
        self.strategy = strategy_config.build_strategy(self.conf) if self.conf else None
        self.version = self.conf["version"] if self.conf else "aucune"
        self.tg = telegram or Telegram(st.telegram_bot_token, st.telegram_chat_id)
        self.bars = pd.DataFrame(columns=["open", "high", "low", "close", "volume", "minutes", "symbol"])
        self.delays: deque[float] = deque(maxlen=60)
        self.events: list[Event] = []
        self.last_quality: dq.Quality | None = None
        self.mode = "demarrage"
        self.last_beat = None
        self.last_cal = None
        self.source_filter = source_filter
        self.decided: set[int] = set()
        self.current_bucket: pd.Timestamp | None = None

    # ------------------------------------------------------------------ démarrage
    def startup(self) -> None:
        now = self.clock()
        with db.session() as s:
            for e in seed_events():
                self._upsert_event(s, e)
            if db.kv_get(s, "user_mode") is None:
                db.kv_set(s, "user_mode", "actif")
            if db.kv_get(s, "notifications") is None:
                db.kv_set(s, "notifications", True)
            if db.kv_get(s, "program") is None:
                db.kv_set(s, "program", DEFAULT_PROGRAM)
            if db.kv_get(s, "trading_mode") is None:
                db.kv_set(s, "trading_mode", "simulation")
            if db.kv_get(s, "paper_account") is None:
                self._save_paper(s, Account.start(get_program(db.kv_get(s, "program"))), trading_date(now))
            since = now - KEEP
            rows = s.execute(select(db.Bar).where(db.Bar.ts >= since, db.Bar.processed.is_(True)).order_by(db.Bar.ts)).scalars().all()
            if rows:
                self.bars = pd.DataFrame.from_records(
                    [(b.open, b.high, b.low, b.close, b.volume, b.minutes, b.symbol) for b in rows],
                    columns=["open", "high", "low", "close", "volume", "minutes", "symbol"],
                    index=pd.DatetimeIndex([b.ts for b in rows]).as_unit("ns"))
                self.bars = self.bars[~self.bars.index.duplicated(keep="last")]
                self.current_bucket = self.bars.index[-1].floor("15min")
            for (bt,) in s.execute(select(db.Decision.bar_ts).where(db.Decision.bar_ts >= since)).all():
                self.decided.add(int(bt.timestamp()))
            db.beat(s, "engine", "demarrage", {"version": self.version})
            enqueue(s, f"engine-start:{now:%Y%m%d%H%M}", "systeme",
                    messages.system_alert("Moteur GoldPilot démarré", f"Stratégie : {self.version}.", now),
                    enabled=bool(db.kv_get(s, "notifications", True)))
        self._load_events()

    # ------------------------------------------------------------------ données
    def _append(self, b: db.Bar) -> None:
        self.bars.loc[pd.Timestamp(b.ts).as_unit("ns")] = [b.open, b.high, b.low, b.close, b.volume, b.minutes, b.symbol]

    def _fetch_new(self, s) -> list[db.Bar]:
        q = select(db.Bar).where(db.Bar.processed.is_(False)).order_by(db.Bar.ts).limit(2000)
        if self.source_filter:
            q = q.where(db.Bar.source == self.source_filter)
        return s.execute(q).scalars().all()

    def _symbol_bars(self, symbol: str) -> pd.DataFrame:
        b = self.bars[self.bars["symbol"] == symbol]
        return b.sort_index()

    def decision_frame(self, symbol: str, upto_bucket: pd.Timestamp) -> pd.DataFrame:
        b = self._symbol_bars(symbol)
        b = b[b.index < upto_bucket + BUCKET]
        if b.empty:
            return b
        r = resample(b[["open", "high", "low", "close", "volume"]].astype(float), 15)
        return r[r.index <= upto_bucket]

    # ------------------------------------------------------------------ boucle
    def tick(self) -> None:
        now = self.clock()
        with db.session() as s:
            notify = bool(db.kv_get(s, "notifications", True))
            expected = active_contract(trading_date(now)).code
            new = self._fetch_new(s)
            for b in new:
                b.processed = True
                self._append(b)
                if b.source == "tradingview":
                    self.delays.append((b.received_at - (b.ts + timedelta(minutes=b.minutes))).total_seconds())
                if b.symbol != expected:
                    continue
                bucket = pd.Timestamp(b.ts).floor("15min")
                # Un créneau précédent non clôturé (dernière minute manquante) est décidé AVANT de suivre
                # la nouvelle barre : même ordre que le backtest.
                if self.current_bucket is not None and self.current_bucket < bucket:
                    self._decide(s, self.current_bucket, now, notify)
                self.current_bucket = bucket
                self._track_signals(s, b, notify)
                if b.ts + timedelta(minutes=b.minutes) >= (bucket + BUCKET).to_pydatetime():
                    self._decide(s, bucket, now, notify)
            # Créneau terminé sans barre suivante (marché calme ou dernière minute manquante)
            if self.current_bucket is not None and now >= (self.current_bucket + BUCKET).to_pydatetime() + GRACE:
                self._decide(s, self.current_bucket, now, notify)
            self._update_mode(s, now, expected, notify)
            self._calendar(s, now)
            self._news_warning(s, now, notify)
            self._roll_reminder(s, now, notify)
            self._end_of_day(s, now)
            cutoff = pd.Timestamp(now - KEEP)
            if len(self.bars) and self.bars.index[0] < cutoff:
                self.bars = self.bars[self.bars.index >= cutoff]
            if self.last_beat is None or (now - self.last_beat).total_seconds() >= 10:
                q = self.last_quality
                db.beat(s, "engine", self.mode, {"version": self.version, "quality": q.level if q else None,
                                                  "problems": q.problems if q else [], "last_price": q.last_price if q else None,
                                                  "last_bar_end": q.last_bar_end.isoformat() if q and q.last_bar_end else None,
                                                  "expected_symbol": expected, "bars_in_memory": len(self.bars)})
                self.last_beat = now
        if self.tg.configured:
            deliver_pending(self.tg)

    # ------------------------------------------------------------------ signaux ouverts
    def _track_signals(self, s, b: db.Bar, notify: bool) -> None:
        opens = sm.open_signals(s)
        if not opens:
            return
        a = self._last_atr(b.symbol)
        for sig in opens:
            before = sig.status
            sm.on_base_bar(s, sig, b.ts, b.open, b.high, b.low, b.close, a, td_int(b.ts), msess(b.ts), notify)
            if before != "CLOTURE" and sig.status == "CLOTURE":
                self._on_closed(s, sig, notify)

    def _last_atr(self, symbol: str) -> float:
        b = self._symbol_bars(symbol)
        if b.empty:
            return float("nan")
        r = resample(b[["open", "high", "low", "close", "volume"]].astype(float), 15).iloc[-41:]
        tr = pd.concat([r["high"] - r["low"], (r["high"] - r["close"].shift()).abs(), (r["low"] - r["close"].shift()).abs()], axis=1).max(axis=1)
        return float(tr.iloc[-40:].mean()) if len(tr) >= 40 else float("nan")

    def _on_closed(self, s, sig: db.Signal, notify: bool) -> None:
        acct = self._load_paper(s)
        if sig.mode == "simulation" and sig.sim_pnl_usd is not None:
            acct.close_trade(sig.sim_pnl_usd)
            self._save_paper(s, acct, db.kv_get(s, "paper_account")["day"])
        self._performance_guard(s, notify)

    # ------------------------------------------------------------------ décision
    def _decide(self, s, bucket: pd.Timestamp, now: datetime, notify: bool) -> None:
        key = int(bucket.timestamp())
        if key in self.decided:
            return
        self.decided.add(key)
        bar_ts = bucket.to_pydatetime()
        expected = active_contract(trading_date(bar_ts)).code
        F15 = self.decision_frame(expected, bucket)

        def record(outcome: str, summary: str, reasons: list, context: dict, checks=None, signal_id=None):
            s.add(db.Decision(bar_ts=bar_ts, strategy_version=self.version, outcome=outcome, summary=summary,
                              reasons=reasons, context=context, risk_checks=checks or [], signal_id=signal_id))

        if self.strategy is None:
            record("suspendu", "Aucune stratégie configurée", ["research/output/final/production.json absent"], {})
            return
        if F15.empty or F15.index[-1] != bucket or len(F15) < MIN_DECISION_BARS:
            record("suspendu", "Préchauffage : historique insuffisant",
                   [f"{len(F15)} barres de 15 min disponibles, {MIN_DECISION_BARS} nécessaires"], {})
            return
        daily = self._daily_history(s) if getattr(self.strategy, "needs_daily_history", False) else None
        F = self.strategy.prepare(F15, daily_history=daily)
        A = arrays(F)
        i = len(F) - 1
        for sig in sm.open_signals(s):
            sm.on_decision_bar_close(s, sig, float(A["high"][i]), float(A["low"][i]), float(A["atr"][i]), float(A["close"][i]), notify)
        opens = sm.open_signals(s)
        stats = sm.today_stats(s, bar_ts + BUCKET)
        tags_today = {r.meta.get("tag") for r in s.execute(select(db.Signal).where(
            db.Signal.created_at >= bar_ts - timedelta(hours=24))).scalars().all()
            if r.meta and int(r.meta.get("td", -1)) == int(A["td"][i]) and r.status != "ANNULE"}
        st = StrategyState(has_position=bool(opens), pending_tags={o.meta.get("tag") for o in opens if o.status == "EN_ATTENTE"},
                           tags_today=tags_today, trades_today=stats["trades"])
        ev = self.strategy.evaluate(i, F, st)
        ctx_info = {"regime": ev.regime, **ev.context, "prix": float(A["close"][i]), "contrat": expected}
        if not ev.setups:
            record("aucun_setup", "Aucun trade : les conditions ne sont pas réunies", ev.no_trade_reasons, ctx_info)
            return
        program_key = db.kv_get(s, "program", DEFAULT_PROGRAM)
        trading_mode = db.kv_get(s, "trading_mode", "simulation")
        acct, known, note = self._account_for_risk(s, trading_mode, now)
        q = self.last_quality or dq.assess(self._symbol_bars(expected).iloc[-300:], now, list(self.delays))
        for su in ev.setups:
            skey = f"{self.version}:{key}:{su.side}"
            dup = s.execute(select(db.Signal.id).where(db.Signal.key == skey)).first() is not None
            rctx = risk.RiskContext(
                now=now, system_mode=self.mode if self.mode in ("actif", "pause", "securise", "arret") else "securise",
                data_ok=q.ok, data_problems=q.problems, last_price=q.last_price, account=acct, account_state_known=known,
                account_note=note, trades_today=stats["trades"], losses_today=stats["losses"],
                realized_loss_today=stats["realized_loss"], open_or_pending_signals=len(opens), duplicate=dup,
                events=self.events)
            rs = risk_settings(s)
            rd = risk.evaluate(su, rctx, rs)
            checks = [{"controle": c.name, "ok": c.ok, "detail": c.detail, "bloquant": c.blocking} for c in rd.checks]
            if not rd.accepted:
                record("refuse", "Setup détecté mais refusé par le moteur de risque", rd.refusals, ctx_info, checks)
                continue
            validated = bool(self.conf.get("validated")) if self.conf else False
            mode = "reel" if (trading_mode == "reel" and validated) else "simulation"
            nxt = next_event(self.events, now)
            sig = db.Signal(
                key=skey, mode=mode, validated=validated, strategy_version=self.version, symbol=expected, side=su.side,
                entry_type=su.entry_type, entry_ref=su.planned_entry, entry_max_drift=su.max_price_drift_atr * su.atr,
                stop=su.stop, target=su.target, trail_atr=su.trail_atr, atr=su.atr, contracts=rd.contracts,
                risk_usd=rd.risk_usd, reward_risk=su.reward_risk,
                valid_until=datetime.fromtimestamp(su.valid_until_ts / 1e9, tz=timezone.utc),
                exit_deadline=self._exit_deadline(bar_ts, su.exit_msess),
                rationale=su.rationale, invalidation=su.invalidation,
                calendar_note=(f"Aucune restriction en cours. Prochaine annonce majeure : {nxt.title}, {fmt_paris(nxt.ts)}"
                               if nxt else "Aucune restriction en cours ; aucune annonce majeure connue à venir"),
                price_source=f"{ {'tradingview': 'TradingView', 'databento': 'Databento', 'replay': 'REJEU HISTORIQUE (simulation)'}.get(settings().data_source, settings().data_source)} — {expected}",
                price_ts=q.last_bar_end or now, status="EN_ATTENTE" if su.entry_type != "market" else "ACTIF",
                meta={"strategy": su.strategy, "config_id": su.config_id, "td": su.td, "tag": su.tag,
                      "exit_msess": su.exit_msess, "decision_bar_ts": su.decision_bar_ts},
            )
            s.add(sig)
            s.flush()
            s.add(db.SignalEvent(signal_id=sig.id, kind="cree", detail={"contrats": rd.contracts, "risque": rd.risk_usd}))
            label = active_contract(trading_date(bar_ts)).label()
            enqueue(s, f"new:{sig.id}", "signal", messages.new_signal(sig, label, (self.conf or {}).get("rapport_gain_perte_historique"),
                                                                       sig.calendar_note), sig.id, notify)
            record("signal", f"Signal {'LONG' if su.side > 0 else 'SHORT'} émis ({mode})", [su.rationale], ctx_info, checks, sig.id)

    @staticmethod
    def _daily_history(s) -> pd.DataFrame | None:
        rows = s.execute(select(db.DailyBar).order_by(db.DailyBar.td.desc()).limit(300)).scalars().all()
        if not rows:
            return None
        return pd.DataFrame({"h": [r.high for r in rows], "l": [r.low for r in rows], "c": [r.close for r in rows]},
                            index=[r.td for r in rows]).sort_index()

    @staticmethod
    def _exit_deadline(bar_ts: datetime, exit_msess: int) -> datetime:
        start = bar_ts - timedelta(minutes=msess(bar_ts))
        return start + timedelta(minutes=exit_msess)

    # ------------------------------------------------------------------ comptes
    def _load_paper(self, s) -> Account:
        d = db.kv_get(s, "paper_account")
        a = Account.start(get_program(db.kv_get(s, "program", DEFAULT_PROGRAM)), d["balance"], d["hwm_eod"], d["floor"], d["best_day"])
        a.day_pnl, a.days, a.breached, a.breach_reason = d.get("day_pnl", 0.0), d.get("days", 0), d.get("breached", False), d.get("breach_reason", "")
        a.day_start_balance = d.get("day_start_balance", a.balance)
        return a

    def _save_paper(self, s, a: Account, day) -> None:
        db.kv_set(s, "paper_account", {"balance": a.balance, "hwm_eod": a.hwm_eod, "floor": a.floor, "best_day": a.best_day,
                                       "day_pnl": a.day_pnl, "days": a.days, "breached": a.breached, "breach_reason": a.breach_reason,
                                       "day_start_balance": a.day_start_balance, "day": str(day), "passed": a.passed,
                                       "target": a.target()})

    def _account_for_risk(self, s, trading_mode: str, now: datetime) -> tuple[Account, bool, str]:
        if trading_mode != "reel":
            return self._load_paper(s), True, "compte simulé (suivi papier des signaux)"
        prog = get_program(db.kv_get(s, "program", DEFAULT_PROGRAM))
        upd = s.execute(select(db.AccountUpdate).order_by(db.AccountUpdate.created_at.desc())).scalars().first()
        if upd is None:
            return Account.start(prog, prog.initial_floor + 300.0), False, "état du compte jamais renseigné : hypothèse prudente (coussin 300 $)"
        a = Account.start(prog, upd.balance, upd.hwm_eod or max(upd.balance, prog.account_size), None, upd.best_day or 0.0)
        stale = trading_date(now) > trading_date(upd.created_at)
        if stale:
            risked = s.execute(select(func.coalesce(func.sum(db.Signal.risk_usd), 0.0)).where(
                db.Signal.created_at > upd.created_at, db.Signal.mode == "reel")).scalar() or 0.0
            a.balance -= float(risked)
            return a, False, f"solde déclaré le {upd.created_at:%d/%m} : hypothèse prudente, signaux depuis supposés perdants ({risked:.0f} $)"
        return a, True, f"solde déclaré aujourd'hui : {upd.balance:,.0f} $".replace(",", " ")

    def _end_of_day(self, s, now: datetime) -> None:
        d = db.kv_get(s, "paper_account")
        today = trading_date(now)
        if d and d.get("day") != str(today):
            a = self._load_paper(s)
            a.end_day()
            self._save_paper(s, a, today)

    def _performance_guard(self, s, notify: bool) -> None:
        lim = (self.conf or {}).get("seuils_suspension")
        if not lim:
            return
        rs = [r for (r,) in s.execute(select(db.Signal.sim_r).where(db.Signal.status == "CLOTURE", db.Signal.strategy_version == self.version,
                                                                      db.Signal.sim_r.is_not(None)).order_by(db.Signal.created_at)).all()]
        if not rs:
            return
        eq = pd.Series(rs).cumsum()
        dd = float((eq - eq.cummax().clip(lower=0)).min())
        streak = cur = 0
        for r in rs:
            cur = cur + 1 if r <= 0 else 0
            streak = max(streak, cur)
        reason = None
        if dd <= lim["drawdown_R"]:
            reason = f"drawdown de {dd:.1f} R au-delà du seuil pré-établi ({lim['drawdown_R']:.1f} R)"
        elif streak >= lim["serie_pertes"]:
            reason = f"série de {streak} pertes au-delà du seuil pré-établi ({lim['serie_pertes']})"
        if reason and not db.kv_get(s, "halt"):
            db.kv_set(s, "halt", {"raison": reason, "depuis": db.now().isoformat()})
            db.open_incident(s, "critique", "performance", "degradation", reason)
            enqueue(s, f"halt:{reason}", "systeme", messages.system_alert("Arrêt de sécurité", reason + ". Reprise manuelle requise après analyse.", db.now()), enabled=notify)

    # ------------------------------------------------------------------ modes
    def _update_mode(self, s, now: datetime, expected: str, notify: bool) -> None:
        q = dq.assess(self.bars.sort_index().iloc[-300:], now, list(self.delays))
        self.last_quality = q
        user = db.kv_get(s, "user_mode", "actif")
        halt = db.kv_get(s, "halt")
        if halt:
            mode = "arret"
        elif user == "pause":
            mode = "pause"
        elif self.strategy is None:
            mode = "arret"
        elif q.level == "bloquant" and (is_open(now) or not len(self.bars)):
            mode = "securise"
        elif len(self.decision_frame(expected, pd.Timestamp(now).floor("15min"))) < MIN_DECISION_BARS:
            mode = "prechauffage"
        else:
            mode = "actif"
        if mode != self.mode:
            if mode == "securise":
                n = sm.cancel_open(s, "Mode sécurisé : " + "; ".join(q.problems), notify, only_pending=True)
                if db.open_incident(s, "alerte", "donnees", "qualite", "; ".join(q.problems)):
                    enqueue(s, f"safe:{now:%Y%m%d%H%M}", "systeme", messages.system_alert(
                        "Mode sécurisé : aucun signal", "; ".join(q.problems) + (f" ({n} signal(aux) en attente annulé(s))" if n else ""), now), enabled=notify)
            elif self.mode == "securise" and mode in ("actif", "prechauffage"):
                if db.resolve_incident(s, "donnees", "qualite"):
                    enqueue(s, f"recover:{now:%Y%m%d%H%M}", "systeme", messages.system_alert("Données rétablies", "Le moteur reprend l'analyse.", now), enabled=notify)
            db.audit(s, "moteur", "changement_de_mode", {"de": self.mode, "vers": mode, "problemes": q.problems})
            self.mode = mode
        db.kv_set(s, "engine_mode", {"mode": mode, "problemes": q.problems, "qualite": q.level, "maj": now.isoformat()})

    # ------------------------------------------------------------------ calendrier
    def _upsert_event(self, s, e: Event) -> None:
        if s.execute(select(db.EconomicEvent.id).where(db.EconomicEvent.source == e.source, db.EconomicEvent.uid == e.uid)).first():
            return
        s.add(db.EconomicEvent(source=e.source, uid=e.uid, title=e.title, impact=e.impact, ts=e.ts, source_url=e.source_url))

    def _load_events(self) -> None:
        with db.session() as s:
            rows = s.execute(select(db.EconomicEvent)).scalars().all()
            self.events = [Event(r.source, r.uid, r.title, r.impact, r.ts, r.source_url) for r in rows]

    def _calendar(self, s, now: datetime) -> None:
        st = settings()
        if self.last_cal is not None and (now - self.last_cal) < timedelta(minutes=st.calendar_refresh_min):
            return
        self.last_cal = now
        if st.data_source == "replay":
            return
        try:
            import httpx

            from ..calendar.events import BLS_ICS

            r = httpx.get(BLS_ICS, timeout=20, headers={"User-Agent": "GoldPilot/1.0 (calendrier personnel)"})
            r.raise_for_status()
            for e in parse_ics(r.text):
                self._upsert_event(s, e)
            db.resolve_incident(s, "calendrier", "bls")
            db.kv_set(s, "calendar_status", {"ok": True, "maj": now.isoformat(), "source": "BLS iCalendar + dates officielles FOMC/BEA"})
        except Exception as e:  # réseau, format
            db.open_incident(s, "alerte", "calendrier", "bls", f"Calendrier BLS indisponible ({type(e).__name__}) : dates intégrées utilisées")
            db.kv_set(s, "calendar_status", {"ok": False, "maj": now.isoformat(), "source": "dates officielles intégrées uniquement"})
        s.flush()
        rows = s.execute(select(db.EconomicEvent)).scalars().all()
        self.events = [Event(r.source, r.uid, r.title, r.impact, r.ts, r.source_url) for r in rows]

    def _news_warning(self, s, now: datetime, notify: bool) -> None:
        opens = [o for o in sm.open_signals(s) if o.status == "ACTIF"]
        if not opens:
            return
        for e in self.events:
            if e.impact == "fort" and now <= e.ts <= now + timedelta(minutes=15):
                for o in opens:
                    enqueue(s, f"news:{o.id}:{e.uid}", "annonce", messages.status_change(
                        o, "Annonce imminente", f"{e.title} à {fmt_ny(e.ts)} : forte volatilité possible, vérifie ton stop."), o.id, notify)

    def _roll_reminder(self, s, now: datetime, notify: bool) -> None:
        c = active_contract(trading_date(now))
        if trading_date(now) >= add_bdays(c.roll_date, -3):
            n = next_contract(c)
            enqueue(s, f"roll:{c.code}", "roll", messages.system_alert(
                "Changement d'échéance à venir", f"À partir du {c.roll_date:%d/%m/%Y}, le contrat à trader devient {n.label()}. "
                f"Mets à jour le graphique TradingView (alerte GoldPilot Bridge) et Tradovate.", now), enabled=notify)


def main() -> None:  # pragma: no cover - point d'entrée du processus
    logging.basicConfig(level=settings().log_level, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    st = settings()
    probs = st.startup_problems()
    if probs:
        raise SystemExit("Configuration refusée :\n- " + "\n- ".join(probs))
    db.init()
    if st.data_source == "replay":
        from ..marketdata.replay import ReplayFeeder

        feeder = ReplayFeeder(st.replay_from, st.replay_speed)
        eng = Engine(clock=feeder.now, source_filter="replay")
        eng.startup()
        while feeder.step():
            eng.tick()
        log.info("rejeu terminé")
        return
    if st.data_source == "databento":
        from ..marketdata.databento_feed import start_databento_thread

        start_databento_thread(st.databento_api_key)
    eng = Engine()
    eng.startup()
    while True:
        try:
            eng.tick()
        except Exception as e:
            log.exception("erreur du moteur")
            with db.session() as s:
                db.open_incident(s, "critique", "moteur", "exception", f"{type(e).__name__}: {e}"[:500])
        time.sleep(2)


if __name__ == "__main__":  # pragma: no cover
    main()
