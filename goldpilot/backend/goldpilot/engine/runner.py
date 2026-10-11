"""Moteur temps réel GoldPilot (processus « engine »).

Boucle (toutes les 2 s) :
1. nouvelles barres de base reçues (webhook TradingView, Databento ou rejeu) → suivi des signaux ouverts ;
2. clôture des barres de décision de 15 min → stop suiveur, analyse de la stratégie, moteur de risque,
   création éventuelle d'un signal ; CHAQUE analyse est journalisée (signal, refus ou absence de setup) ;
3. modes : pause (toi), arrêt de sécurité (anomalie grave), mode sécurisé (données), préchauffage ;
4. calendrier officiel, avertissements d'annonces, rappel de changement d'échéance ;
   contexte macro FRED (taux réels, dollar) toutes les 6 h, information seulement, jamais lu par la décision ;
5. fin de journée : plancher trailing du compte simulé ; seuils de suspension automatique ;
6. envoi des notifications en attente ; battement de cœur pour le site.
"""
from __future__ import annotations

import logging
import math
import threading
import time
from collections import deque
from datetime import datetime, timedelta, timezone
from typing import Callable

import pandas as pd
from sqlalchemy import desc, func, select

from .. import db
from ..calendar.events import Event, next_event, parse_ics, seed_events
from ..config import settings
from ..context import fred as macro
from ..marketdata import quality as dq
from ..marketdata.contracts import active_contract, add_bdays, business_day, next_contract
from ..notify import messages
from ..notify.telegram import Telegram, deliver_pending, enqueue
from ..research.data import resample
from ..risk import engine as risk
from ..risk.account import Account
from ..risk.rules import DEFAULT_PROGRAM, get_program
from ..risk.sizing import MGC_OZ, RiskSettings
from ..signals import manager as sm
from ..strategy.base import StrategyState
from ..strategy.candidates import arrays
from ..timeutil import NY, fmt_ny, fmt_paris, is_open, msess, trading_date, utcnow
from . import strategy_config

log = logging.getLogger("goldpilot.engine")
BUCKET = timedelta(minutes=15)
GRACE = timedelta(seconds=75)
KEEP = timedelta(days=8)
MIN_DECISION_BARS = 45
MIRROR_WAIT = timedelta(minutes=5)  # délai laissé au moteur pour décider avant de juger un signal miroir
EPOCH = datetime(1970, 1, 1).date()
MACRO_EVERY = timedelta(hours=6)  # contexte macro FRED : rafraîchissement normal
MACRO_RETRY = timedelta(minutes=30)  # nouvel essai après un échec (3 requêtes, très loin de la limite FRED)
CLOCK_GRACE_MIN = timedelta(minutes=3)  # échéance à l'horloge : délai laissé à la barre attendue (= seuil « données périmées »)
# Contrôle croisé des prix (DATA_SOURCE=databento) : écart de clôture toléré entre Databento et TradingView sur la même
# minute. Seuil de prudence (10 ticks MGC), hypothèse NON validée : il sert à signaler des données contradictoires.
CROSS_CHECK_TOL = 1.0
MODE_LABELS = {"demarrage": "démarrage du moteur (état des données pas encore évalué)",
               "prechauffage": "préchauffage (historique insuffisant)"}


def td_int(dt: datetime) -> int:
    """Journée de trading en jours depuis 1970 (même convention que strategy.indicators.time_columns)."""
    return (trading_date(dt) - EPOCH).days


def _parse_utc(x: str) -> datetime:
    d = datetime.fromisoformat(x)
    return d.replace(tzinfo=timezone.utc) if d.tzinfo is None else d


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
        self.last_mirror_check = None
        self.source_filter = source_filter
        self.primary_source = source_filter or "tradingview"  # source des décisions ; les autres : contrôle croisé
        self.last_bar_ts: dict[str, datetime] = {}  # dernière barre appliquée par contrat (jamais de retour en arrière)
        self.decided: set[int] = set()
        self.current_bucket: pd.Timestamp | None = None
        self.last_decision_atr = float("nan")  # ATR de la dernière barre de décision clôturée (comme le backtest)
        self.last_macro: datetime | None = None
        self.macro_ok = True
        self.macro_async = True  # False uniquement dans les tests (appel synchrone)
        self.macro_thread: threading.Thread | None = None
        self.macro_result: tuple[dict, bool] | None = None

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
            rows = s.execute(select(db.Bar).where(db.Bar.ts >= since, db.Bar.processed.is_(True), db.Bar.source == self.primary_source)
                             .order_by(db.Bar.ts)).scalars().all()
            if rows:
                self.bars = pd.DataFrame.from_records(
                    [(b.open, b.high, b.low, b.close, b.volume, b.minutes, b.symbol) for b in rows],
                    columns=["open", "high", "low", "close", "volume", "minutes", "symbol"],
                    index=pd.DatetimeIndex([b.ts for b in rows]).as_unit("ns"))
                self.bars = self._dedupe(self.bars)
                self.current_bucket = self.bars.index[-1].floor("15min")
                for b in rows:
                    if b.source == self.primary_source:
                        self.last_bar_ts[b.symbol] = max(self.last_bar_ts.get(b.symbol, b.ts), b.ts)
            for (bt,) in s.execute(select(db.Decision.bar_ts).where(db.Decision.bar_ts >= since)).all():
                self.decided.add(int(bt.timestamp()))
            self._governance(s, now)
            db.beat(s, "engine", "demarrage", {"version": self.version})
            enqueue(s, f"engine-start:{now:%Y%m%d%H%M}", "systeme",
                    messages.system_alert("Moteur GoldPilot démarré", f"Stratégie : {self.version}.", now),
                    enabled=bool(db.kv_get(s, "notifications", True)))
        self._load_events()

    # ------------------------------------------------------------------ données
    def _append(self, b: db.Bar) -> None:
        """Barres en mémoire indexées par minute : si deux contrats arrivent pour la même minute (autour du changement
        d'échéance, deux alertes TradingView actives), la barre du contrat actif n'est jamais écrasée par l'autre."""
        ts = pd.Timestamp(b.ts).as_unit("ns")
        if ts in self.bars.index:
            cur = self.bars.at[ts, "symbol"]
            if cur != b.symbol and cur == active_contract(trading_date(b.ts)).code:
                return
        self.bars.loc[ts] = [b.open, b.high, b.low, b.close, b.volume, b.minutes, b.symbol]

    @staticmethod
    def _dedupe(bars: pd.DataFrame) -> pd.DataFrame:
        """Une ligne par minute ; en cas de doublon, celle du contrat actif de la journée l'emporte."""
        if not bars.index.duplicated().any():
            return bars
        active: dict = {}

        def code(ts: pd.Timestamp) -> str:
            td = trading_date(ts.to_pydatetime())
            if td not in active:
                active[td] = active_contract(td).code
            return active[td]

        pref = [sym == code(ts) for ts, sym in zip(bars.index, bars["symbol"])]
        tmp = bars.assign(_pref=pref, _ts=bars.index)
        tmp = tmp.sort_values(["_ts", "_pref"], kind="stable")
        tmp = tmp[~tmp.index.duplicated(keep="last")]
        return tmp.drop(columns=["_pref", "_ts"])

    def _fetch_new(self, s) -> list[db.Bar]:
        q = (select(db.Bar).where(db.Bar.processed.is_(False), db.Bar.source == self.primary_source)
             .order_by(db.Bar.ts).limit(2000))
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
    def _snapshot(self) -> tuple:
        return (set(self.decided), self.current_bucket, self.last_decision_atr, self.bars, deque(self.delays, maxlen=self.delays.maxlen),
                dict(self.last_bar_ts), self.mode, self.last_mirror_check, self.last_cal, self.last_beat)

    def _restore(self, snap: tuple) -> None:
        (self.decided, self.current_bucket, self.last_decision_atr, self.bars, self.delays, self.last_bar_ts, self.mode,
         self.last_mirror_check, self.last_cal, self.last_beat) = snap

    def tick(self) -> None:
        """Un passage de la boucle. Si une erreur survient, la transaction est annulée (décisions, signaux, barres
        marquées traitées) : l'état en mémoire est alors restauré pour que les mêmes barres soient retraitées et que
        chaque créneau de 15 min soit bien décidé au passage suivant (aucune analyse perdue)."""
        now = self.clock()
        snap = self._snapshot()
        try:
            with db.session() as s:
                self._tick(s, now)
        except Exception:
            self._restore(snap)
            raise
        if self.tg.configured:
            deliver_pending(self.tg, now=now)

    def _tick(self, s, now: datetime) -> None:
        notify = bool(db.kv_get(s, "notifications", True))
        expected = active_contract(trading_date(now)).code
        new = self._fetch_new(s)
        if new:
            self.bars = self.bars.copy()  # la copie de l'instantané reste intacte en cas d'annulation
        for b in new:
            b.processed = True
            self.delays.append((b.received_at - (b.ts + timedelta(minutes=b.minutes))).total_seconds())
            last = self.last_bar_ts.get(b.symbol)
            if last is not None and b.ts <= last:
                # Barre arrivée en retard (renvoi) : jamais appliquée au suivi ni au créneau courant après une plus
                # récente. Elle complète seulement le créneau de 15 min encore ouvert (pas encore décidé).
                bucket = pd.Timestamp(b.ts).floor("15min")
                if (b.symbol == expected and self.current_bucket is not None and bucket >= self.current_bucket
                        and int(bucket.timestamp()) not in self.decided):
                    self._append(b)
                log.warning("barre %s %s reçue après une barre plus récente : ignorée pour le suivi", b.symbol, b.ts)
                continue
            self.last_bar_ts[b.symbol] = b.ts
            self._append(b)
            if b.symbol != expected:
                continue
            bucket = pd.Timestamp(b.ts).floor("15min")
            # Un créneau précédent non clôturé (dernière minute manquante) est décidé AVANT de suivre
            # la nouvelle barre : même ordre que le backtest.
            if self.current_bucket is not None and self.current_bucket < bucket:
                self._decide(s, self.current_bucket, now, notify)
            if self.current_bucket is None or bucket > self.current_bucket:
                self.current_bucket = bucket
            self._track_signals(s, b, notify)
            if b.ts + timedelta(minutes=b.minutes) >= (bucket + BUCKET).to_pydatetime():
                self._decide(s, bucket, now, notify)
        # Créneau terminé sans barre suivante (marché calme ou dernière minute manquante)
        if self.current_bucket is not None and now >= (self.current_bucket + BUCKET).to_pydatetime() + GRACE:
            self._decide(s, self.current_bucket, now, notify)
        self._clock_deadlines(s, now, notify)
        self._update_mode(s, now, expected, notify)
        self._cross_check_sources(s, now, notify)
        self._calendar(s, now)
        self._macro_context(s, now)
        self._news_warning(s, now, notify)
        self._roll_reminder(s, now, notify)
        self._check_mirrors(s, now, notify)
        self._end_of_day(s, now)
        self._periodic_review(s, now, notify)
        cutoff = pd.Timestamp(now - KEEP)
        if len(self.bars) and self.bars.index[0] < cutoff:
            self.bars = self.bars[self.bars.index >= cutoff]
        if self.last_beat is None or (now - self.last_beat).total_seconds() >= 10:
            q = self.last_quality
            db.beat(s, "engine", self.mode, {"version": self.version, "quality": q.level if q else None,
                                              "problems": q.problems if q else [], "last_price": q.last_price if q else None,
                                              "last_bar_end": q.last_bar_end.isoformat() if q and q.last_bar_end else None,
                                              "expected_symbol": expected, "bars_in_memory": len(self.bars),
                                              "source": self.primary_source, "clock": now.isoformat()})
            self.last_beat = now

    def _clock_deadlines(self, s, now: datetime, notify: bool) -> None:
        """Validité et heure limite de sortie vérifiées à l'horloge (barres interrompues : voir sm.on_clock)."""
        bar_min = int(self.bars["minutes"].iloc[-1]) if len(self.bars) else 1
        grace = max(CLOCK_GRACE_MIN, timedelta(minutes=2 * bar_min + 1))
        for sig in sm.open_signals(s):
            sm.on_clock(s, sig, now, grace, notify)

    def _cross_check_sources(self, s, now: datetime, notify: bool) -> None:
        """DATA_SOURCE=databento : les barres TradingView ne pilotent ni les décisions ni le suivi ; chaque minute reçue
        des deux sources est comparée (clôture). Un écart > CROSS_CHECK_TOL ouvre un incident « données contradictoires »."""
        if self.primary_source != "databento" or not self.last_bar_ts:
            return
        upto = max(self.last_bar_ts.values())
        rows = s.execute(select(db.Bar).where(db.Bar.processed.is_(False), db.Bar.source == "tradingview", db.Bar.ts <= upto)
                         .order_by(db.Bar.ts).limit(2000)).scalars().all()
        worst, compared = None, 0
        for b in rows:
            b.processed = True
            ts = pd.Timestamp(b.ts).as_unit("ns")
            if ts not in self.bars.index or self.bars.at[ts, "symbol"] != b.symbol:
                continue
            compared += 1
            gap = abs(float(self.bars.at[ts, "close"]) - b.close)
            if gap > CROSS_CHECK_TOL and (worst is None or gap > worst[0]):
                worst = (gap, b)
        if worst is not None:
            gap, b = worst
            msg = (f"Prix contradictoires entre Databento et TradingView : écart de {gap:.2f} $ sur la clôture de "
                   f"{fmt_ny(b.ts + timedelta(minutes=b.minutes))} ({b.symbol}). Seuil de prudence {CROSS_CHECK_TOL:.2f} $ "
                   "(hypothèse non validée). Vérifie les deux graphiques avant de suivre un signal.")
            if db.open_incident(s, "avertissement", "controle_croise", "prix", msg):
                enqueue(s, f"xsrc:{b.ts:%Y%m%d%H%M}", "systeme", messages.system_alert("Sources de prix en désaccord", msg, now), enabled=notify)
        elif compared:
            db.resolve_incident(s, "controle_croise", "prix")

    # ------------------------------------------------------------------ signaux ouverts
    def _track_signals(self, s, b: db.Bar, notify: bool) -> None:
        opens = sm.open_signals(s)
        if not opens:
            return
        a = self.last_decision_atr
        for sig in opens:
            before = sig.status
            sm.on_base_bar(s, sig, b.ts, b.open, b.high, b.low, b.close, a, td_int(b.ts), msess(b.ts), notify)
            if before != "CLOTURE" and sig.status == "CLOTURE":
                self._on_closed(s, sig, notify)
            elif sig.status == "ACTIF" and sig.sim_entry is not None and sig.mode == "simulation":
                self._check_floating_loss(s, sig, b, notify)

    def _check_floating_loss(self, s, sig: db.Signal, b: db.Bar, notify: bool) -> None:
        """Règle FundedNext « perte latente » : la perte flottante au pire extrême de la barre (bas pour un achat,
        haut pour une vente) qui amène le solde simulé au plancher viole le compte immédiatement."""
        worst = b.low if sig.side > 0 else b.high
        floating = (worst - sig.sim_entry) * sig.side * MGC_OZ * sig.contracts
        acct = self._load_paper(s)
        if acct.breached or not acct.check_equity(floating):
            return
        self._save_paper(s, acct, db.kv_get(s, "paper_account")["day"])
        enqueue(s, f"paper-breach:{sig.id}", "systeme", messages.system_alert(
            "Compte simulé : perte maximale atteinte (latente)",
            f"Perte flottante de {-floating:,.0f} $ au pire de la barre de {fmt_ny(b.ts)} : le solde simulé touche le plancher "
            f"({acct.floor:,.0f} $). Sur un vrai compte FundedNext, le compte serait violé.".replace(",", " "), b.ts), enabled=notify)

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
        # Mode mis à jour AVANT de décider (sinon : mode du passage précédent, ou « démarrage » après un redémarrage)
        self._update_mode(s, now, active_contract(trading_date(now)).code, notify)
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
        self.last_decision_atr = float(A["atr"][i])
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
        q = dq.assess(self.bars.sort_index().iloc[-300:], now, list(self.delays))  # état des données à l'instant de la décision
        for su in ev.setups:
            skey = f"{self.version}:{key}:{su.side}"
            dup = s.execute(select(db.Signal.id).where(db.Signal.key == skey)).first() is not None
            rctx = risk.RiskContext(
                now=now, system_mode=MODE_LABELS.get(self.mode, self.mode),
                data_ok=q.ok, data_problems=q.problems, last_price=q.last_price, account=acct, account_state_known=known,
                account_note=note, trades_today=stats["trades"], losses_today=stats["losses"],
                realized_loss_today=stats["realized_loss"], open_or_pending_signals=len(opens), duplicate=dup,
                events=self.events, real_mode=trading_mode == "reel",
                rules_confirmed_in_writing=bool((db.kv_get(s, "fundednext_confirmation") or {}).get("confirme")))
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
                key=skey, created_at=now, mode=mode, validated=validated, strategy_version=self.version, symbol=expected, side=su.side,
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
                      "exit_msess": su.exit_msess, "decision_bar_ts": su.decision_bar_ts,
                      "niveaux": (getattr(su, "meta", None) or {}).get("niveaux")},
            )
            s.add(sig)
            s.flush()
            s.add(db.SignalEvent(signal_id=sig.id, ts=now, kind="cree", detail={"contrats": rd.contracts, "risque": rd.risk_usd}))
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
            try:
                prev = datetime.strptime(d.get("day"), "%Y-%m-%d").date()
            except (TypeError, ValueError):
                prev = None
            if prev is None or business_day(prev):  # samedi, dimanche, jour férié CME : pas de journée de trading close
                a.end_day()
            self._save_paper(s, a, today)

    def _performance_guard(self, s, notify: bool) -> None:
        lim = (self.conf or {}).get("seuils_suspension")
        if not lim:
            return
        q = select(db.Signal.sim_r).where(db.Signal.status == "CLOTURE", db.Signal.strategy_version == self.version, db.Signal.sim_r.is_not(None))
        reset = db.kv_get(s, "halt_reset") or {}
        if reset.get("version") == self.version and reset.get("depuis"):
            # Reprise manuelle après un arrêt : les seuils sont recomptés sur les trades clôturés depuis la reprise
            q = q.where(db.Signal.sim_exit_ts > _parse_utc(reset["depuis"]))
        rs = [r for (r,) in s.execute(q.order_by(db.Signal.created_at)).all()]
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
            db.kv_set(s, "halt", {"raison": reason, "depuis": db.now().isoformat(), "type": "performance"})
            db.open_incident(s, "critique", "performance", "degradation", reason)
            enqueue(s, f"halt:{reason}", "systeme", messages.system_alert("Arrêt de sécurité", reason + ". Reprise manuelle requise après analyse.", db.now()), enabled=notify)

    # ------------------------------------------------------------------ gouvernance des versions (cahier §17)
    def _governance(self, s, now: datetime) -> None:
        """Aucune nouvelle version de stratégie ne remplace l'ancienne sans approbation explicite (Paramètres).
        Première mise en service : la version courante est enregistrée comme approuvée (« initialisation »)."""
        if self.strategy is None:
            return
        approved = db.kv_get(s, "approved_version")
        if not approved:
            db.kv_set(s, "approved_version", {"version": self.version, "approuve_le": now.isoformat(), "par": "initialisation"})
            db.audit(s, "moteur", "version_approuvee", {"version": self.version, "par": "initialisation"})
            return
        if approved.get("version") == self.version:
            halt = db.kv_get(s, "halt")
            if halt and halt.get("type") == "version":  # retour à la version approuvée : l'arrêt « version » n'a plus d'objet
                db.kv_set(s, "halt", None)
                db.resolve_incident(s, "strategie", "version")
                db.audit(s, "moteur", "arret_version_leve", {"version": self.version})
            return
        reason = f"nouvelle version de stratégie non approuvée : {self.version} (version approuvée : {approved.get('version')})"
        halt = db.kv_get(s, "halt")
        if not halt or halt.get("type") != "version" or halt.get("raison") != reason:
            db.kv_set(s, "halt", {"raison": reason, "depuis": now.isoformat(), "type": "version"})
            db.audit(s, "moteur", "version_non_approuvee", {"version_courante": self.version, "version_approuvee": approved.get("version")})
            db.open_incident(s, "critique", "strategie", "version", reason)
            enqueue(s, f"version:{self.version}", "systeme", messages.system_alert(
                "Arrêt de sécurité : nouvelle version de stratégie", reason + ". Compare-la puis approuve-la dans Paramètres.", now),
                enabled=bool(db.kv_get(s, "notifications", True)))

    # ------------------------------------------------------------------ revue périodique (cahier §17)
    def _periodic_review(self, s, now: datetime, notify: bool) -> None:
        """Chaque samedi (date de New York), bilan des trades simulés de la version en service comparé aux résultats
        de la recherche. Information seulement : la stratégie n'est JAMAIS modifiée automatiquement."""
        ny = now.astimezone(NY).date()
        if ny.weekday() != 5 or self.strategy is None:
            return
        prev = db.kv_get(s, "revue_periodique") or {}
        if prev.get("date") == ny.isoformat():
            return
        rs = [float(r) for (r,) in s.execute(select(db.Signal.sim_r).where(
            db.Signal.status == "CLOTURE", db.Signal.strategy_version == self.version, db.Signal.mode == "simulation",
            db.Signal.sim_r.is_not(None)).order_by(db.Signal.sim_exit_ts)).all()]
        n = len(rs)
        mean = sum(rs) / n if n else None
        lb = dd = win = None
        streak = cur = 0
        if n:
            if n >= 2:
                sd = math.sqrt(sum((r - mean) ** 2 for r in rs) / (n - 1))
                lb = round(mean - 1.645 * sd / math.sqrt(n), 3)  # borne basse unilatérale à 95 %
            eq = pd.Series(rs).cumsum()
            dd = round(float((eq - eq.cummax().clip(lower=0)).min()), 2)
            win = round(sum(1 for r in rs if r > 0) / n, 3)
            for r in rs:
                cur = cur + 1 if r <= 0 else 0
                streak = max(streak, cur)
        ref = strategy_config.research_reference()
        lim = (self.conf or {}).get("seuils_suspension")
        if n < 30:
            concl = (f"{n} trade(s) simulé(s) clôturé(s) avec cette version : échantillon trop petit pour conclure. "
                     "Aucune modification de la stratégie.")
        else:
            wf = ref.get("esperance_R_walk_forward")
            cmp_txt = (f"inférieure à l'espérance walk-forward de la recherche ({wf:+.3f} R)" if wf is not None and mean < wf
                       else "conforme ou supérieure à la recherche" if wf is not None else "référence de recherche indisponible")
            concl = (f"{n} trades simulés : espérance {mean:+.3f} R par trade ({cmp_txt}), borne basse 95 % {lb:+.3f} R. "
                     + ("La borne basse est négative : aucun avantage démontré. " if lb is not None and lb <= 0 else "")
                     + "Aucune modification automatique de la stratégie.")
        review = {"date": ny.isoformat(), "version": self.version, "n": n,
                  "esperance_R": None if mean is None else round(mean, 3), "borne_basse_95_R": lb, "drawdown_max_R": dd,
                  "serie_pertes_max": streak, "taux_de_gain": win, "reference": ref, "seuils": lim, "conclusion": concl}
        db.kv_set(s, "revue_periodique", review)
        db.audit(s, "moteur", "revue_periodique", review)
        enqueue(s, f"review:{ny.isoformat()}", "systeme", messages.system_alert("Revue hebdomadaire des performances", concl, now),
                enabled=notify)

    # ------------------------------------------------------------------ modes
    def _update_mode(self, s, now: datetime, expected: str, notify: bool) -> None:
        q = dq.assess(self.bars.sort_index().iloc[-300:], now, list(self.delays))
        self.last_quality = q
        user = db.kv_get(s, "user_mode", "actif")
        halt = db.kv_get(s, "halt")
        approved = db.kv_get(s, "approved_version")
        if halt or (self.strategy is not None and approved and approved.get("version") != self.version):
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
                n = sm.cancel_open(s, "Mode sécurisé : " + "; ".join(q.problems), notify, only_pending=True, now=now)
                if db.open_incident(s, "alerte", "donnees", "qualite", "; ".join(q.problems)):
                    enqueue(s, f"safe:{now:%Y%m%d%H%M}", "systeme", messages.system_alert(
                        "Mode sécurisé : aucun signal", "; ".join(q.problems) + (f" ({n} signal(aux) non entré(s) annulé(s))" if n else ""), now), enabled=notify)
                for sig in sm.open_signals(s):  # position simulée ouverte : prévenir explicitement
                    if sig.status == "ACTIF" and sig.sim_entry is not None:
                        enqueue(s, f"safe-open:{sig.id}:{now:%Y%m%d%H%M}", "systeme", messages.status_change(
                            sig, "Position ouverte, données interrompues",
                            f"{'; '.join(q.problems)}. Surveille-la directement sur Tradovate (stop simulé {sig.sim_stop or sig.stop:.1f}). "
                            f"Fermeture au plus tard à {fmt_ny(sig.exit_deadline)}, même sans nouvelle alerte."), sig.id, notify)
            elif self.mode == "securise" and mode in ("actif", "prechauffage"):
                if db.resolve_incident(s, "donnees", "qualite"):
                    enqueue(s, f"recover:{now:%Y%m%d%H%M}", "systeme", messages.system_alert("Données rétablies", "Le moteur reprend l'analyse.", now), enabled=notify)
            db.audit(s, "moteur", "changement_de_mode", {"de": self.mode, "vers": mode, "problemes": q.problems})
            self.mode = mode
        db.kv_set(s, "engine_mode", {"mode": mode, "problemes": q.problems, "qualite": q.level, "maj": now.isoformat()})

    # ------------------------------------------------------------------ contrôle croisé TradingView
    def _check_mirrors(self, s, now: datetime, notify: bool) -> None:
        """Compare les franchissements calculés par le script Pine (signaux « miroir ») aux décisions du moteur.

        Le miroir n'est jamais décisionnel. Un désaccord signale des données contradictoires (barres perdues,
        décalées ou différentes) : incident visible sur le site et alerte téléphone."""
        if self.last_mirror_check is not None and now - self.last_mirror_check < timedelta(seconds=30):
            return
        self.last_mirror_check = now
        pending = s.execute(select(db.MirrorSignal).where(db.MirrorSignal.verdict.is_(None))
                            .order_by(db.MirrorSignal.bar_ts).limit(50)).scalars().all()
        for m in pending:
            dec = s.execute(select(db.Decision).where(db.Decision.bar_ts == m.bar_ts).order_by(desc(db.Decision.id))).scalars().first()
            if dec is None and now - m.received_at < MIRROR_WAIT:
                continue
            sens = "haussier" if m.side > 0 else "baissier"
            heure = fmt_ny(m.bar_ts + BUCKET)
            if dec is None:
                m.verdict = "decision_absente"
                why = "n'a analysé aucune barre de 15 minutes à cet instant"
            else:
                m.matched_signal_id = dec.signal_id
                m.verdict = "concordant" if (dec.context or {}).get("franchissement") == m.side else "discordant"
                why = f"ne l'a pas retrouvé (écart calculé par le moteur : {(dec.context or {}).get('z')} ATR)"
            m.checked_at = now
            if m.verdict == "concordant":
                db.resolve_incident(s, "controle_croise", "miroir")
                continue
            msg = (f"TradingView a détecté un franchissement {sens} à la clôture de {heure} ; le moteur {why}. "
                   "Causes possibles : barres d'une minute perdues ou décalées, historique journalier différent. "
                   "Vérifie Journal › Webhooks avant de suivre un signal.")
            db.open_incident(s, "avertissement", "controle_croise", "miroir", msg)
            enqueue(s, f"mirror:{m.id}", "systeme", messages.system_alert("Contrôle croisé TradingView en désaccord", msg, now), enabled=notify)
        # Sens inverse : signal du moteur que TradingView n'a pas signalé (seulement si le miroir fonctionne déjà)
        if settings().data_source != "tradingview" or not s.execute(select(db.MirrorSignal.id).limit(1)).first():
            return
        recent = s.execute(select(db.Decision).where(db.Decision.outcome == "signal", db.Decision.bar_ts >= now - timedelta(hours=3),
                                                     db.Decision.bar_ts <= now - BUCKET - MIRROR_WAIT)).scalars().all()
        for d in recent:
            sig = s.get(db.Signal, d.signal_id) if d.signal_id else None
            if sig is None:
                continue
            seen = s.execute(select(db.MirrorSignal.id).where(db.MirrorSignal.bar_ts == d.bar_ts, db.MirrorSignal.side == sig.side)).first()
            if seen:
                continue
            msg = (f"Le moteur a émis un signal {'LONG' if sig.side > 0 else 'SHORT'} à {fmt_ny(d.bar_ts + BUCKET)} que le script "
                   "TradingView n'a pas confirmé. Causes possibles : barres perdues ou décalées, filtre de volatilité calculé "
                   "différemment, signal antérieur dans le même sens côté TradingView. Prudence sur ce signal.")
            if enqueue(s, f"mirror-missing:{sig.id}", "systeme", messages.system_alert("Contrôle croisé TradingView en désaccord", msg, now),
                       sig.id, notify):
                db.open_incident(s, "avertissement", "controle_croise", "miroir", msg)
                s.add(db.SignalEvent(signal_id=sig.id, ts=now, kind="controle_croise", detail={"verdict": "non_confirme_par_tradingview"}))

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

    # ------------------------------------------------------------------ contexte macro (information seulement)
    def _macro_context(self, s, now: datetime) -> None:
        """Rafraîchit le contexte macro FRED (KV « macro_context ») ; n'influence ni la stratégie ni le risque.

        Choix : la requête réseau (3 séries, délai 10 s chacune) tourne dans un fil d'exécution séparé. Faite dans la
        boucle, elle garderait ouverte jusqu'à ~30 s la transaction de la boucle (base SQLite verrouillée pour le
        webhook TradingView) et retarderait d'autant une décision de clôture de 15 min. Le fil ne touche pas à la
        base : il dépose son résultat, que la boucle enregistre au passage suivant (toutes les 2 s). Toute erreur
        ici est journalisée et ignorée : le contexte ne doit jamais bloquer les signaux."""
        try:
            if self.macro_thread is not None:
                if self.macro_thread.is_alive():
                    return
                self.macro_thread = None
                done, self.macro_result = self.macro_result, None
                if done is not None:
                    self._store_macro(s, *done)
            due = self.last_macro is None or now - self.last_macro >= (MACRO_EVERY if self.macro_ok else MACRO_RETRY)
            if not due:
                return
            self.last_macro = now
            st = settings()
            if st.data_source == "replay":  # le contexte du jour ne correspond pas à l'horloge virtuelle
                self._store_macro(s, macro.unavailable(macro.REPLAY), False)
                return
            if not st.fred_api_key:  # configuration facultative : pas d'incident, le site affiche le problème
                self._store_macro(s, macro.unavailable(macro.KEY_MISSING), False)
                return
            key = st.fred_api_key
            if not self.macro_async:
                self._store_macro(s, *self._fetch_macro(key))
                return
            self.macro_thread = threading.Thread(target=lambda: setattr(self, "macro_result", self._fetch_macro(key)),
                                                 name="goldpilot-fred", daemon=True)
            self.macro_thread.start()
        except Exception as e:  # pragma: no cover - filet de sécurité
            log.warning("contexte macro ignoré (%s)", type(e).__name__)

    @staticmethod
    def _fetch_macro(key: str) -> tuple[dict, bool]:
        """(contexte, échec ?) — exécuté hors de la boucle ; aucune exception ne sort, la clé n'est jamais citée."""
        try:
            ctx = macro.build_context(key)
        except Exception as e:  # imprévu : seul le type est repris (le message pourrait contenir l'URL)
            ctx = macro.unavailable(f"erreur interne ({type(e).__name__})")
        return ctx, ctx["probleme"] is not None

    def _store_macro(self, s, ctx: dict, failed: bool) -> None:
        prev = db.kv_get(s, "macro_context") or {}
        if failed and not ctx["disponible"] and ctx["maj"] is None and prev.get("maj"):
            ctx = {**ctx, "maj": prev["maj"]}  # date du dernier rafraîchissement réussi
        if failed:
            db.open_incident(s, "avertissement", "contexte", "fred",
                             f"Contexte macro FRED : {ctx['probleme']}. Information de contexte uniquement : "
                             "les signaux ne sont pas affectés.")
        else:
            db.resolve_incident(s, "contexte", "fred")
        self.macro_ok = not failed
        if prev != ctx:
            db.kv_set(s, "macro_context", ctx)

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


def configure_logging(level: str) -> None:
    logging.basicConfig(level=level, format="%(asctime)s %(levelname)s %(name)s %(message)s")
    for noisy in ("httpx", "httpcore"):  # ces bibliothèques journalisent l'URL complète (jeton Telegram, clé FRED)
        logging.getLogger(noisy).setLevel(logging.WARNING)


def main() -> None:  # pragma: no cover - point d'entrée du processus
    configure_logging(settings().log_level)
    st = settings()
    probs = st.startup_problems()
    if probs:
        raise SystemExit("Configuration refusée :\n- " + "\n- ".join(probs))
    db.init()
    if st.data_source == "replay":
        from ..marketdata.replay import ReplayFeeder

        feeder = ReplayFeeder(st.replay_from, st.replay_speed)
        feeder.seed_daily_history()
        feeder.resume_from_db()
        eng = Engine(clock=feeder.now, source_filter="replay")
        eng.startup()
        while feeder.step():
            eng.tick()
        log.info("rejeu terminé : le moteur reste actif (horloge virtuelle figée) pour la consultation du site")
        with db.session() as s:
            db.kv_set(s, "replay_status", {"termine": True, "horloge": feeder.now().isoformat()})
        while True:
            eng.tick()
            time.sleep(2)
    if st.data_source == "databento":
        from ..marketdata.databento_feed import start_databento_thread

        start_databento_thread(st.databento_api_key)
    # Source primaire = celle des décisions et du suivi. Avec DATA_SOURCE=databento, les barres TradingView ne servent
    # qu'au contrôle croisé des prix ; il n'y a PAS de bascule automatique vers une source de secours.
    eng = Engine(source_filter="databento" if st.data_source == "databento" else "tradingview")
    eng.startup()
    failing = False
    while True:
        try:
            eng.tick()
            if failing:  # retour à la normale après une erreur
                with db.session() as s:
                    db.resolve_incident(s, "moteur", "exception")
                    enqueue(s, f"engine-recovered:{utcnow():%Y%m%d%H%M}", "systeme",
                            messages.system_alert("Moteur rétabli", "Le moteur fonctionne de nouveau normalement.", utcnow()))
                failing = False
        except Exception as e:
            log.exception("erreur du moteur")
            try:
                with db.session() as s:
                    if db.open_incident(s, "critique", "moteur", "exception", f"{type(e).__name__}: {e}"[:500]):
                        enqueue(s, f"engine-error:{utcnow():%Y%m%d%H%M}", "systeme", messages.system_alert(
                            "Erreur du moteur", f"{type(e).__name__} : les signaux sont suspendus jusqu'au rétablissement.", utcnow()))
                if eng.tg.configured:
                    deliver_pending(eng.tg)
            except Exception:  # base de données indisponible : le site affichera « moteur injoignable »
                log.exception("impossible d'enregistrer l'incident")
            failing = True
        time.sleep(2)


if __name__ == "__main__":  # pragma: no cover
    main()
