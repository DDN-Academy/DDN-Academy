"""Rejeu historique (DATA_SOURCE=replay) : fait tourner le système complet sur des données passées.

Usage : démonstration et tests de bout en bout sans flux en direct. Les barres de 5 minutes XAUUSD 2025
du dépôt sont insérées une à une comme si elles venaient d'arriver, avec une horloge virtuelle.
ATTENTION : ce sont des prix SPOT XAUUSD étiquetés avec le contrat MGC actif de la date, uniquement pour
faire fonctionner la chaîne ; les signaux produits sont marqués « REJEU HISTORIQUE (simulation) ».
Interdit en production (refus au démarrage).
"""
from __future__ import annotations

import time
from datetime import datetime, timedelta, timezone

import pandas as pd

from .. import db
from ..research.data import load_15m, load_5m
from ..strategy.indicators import time_columns
from ..timeutil import trading_date
from .contracts import active_contract


class ReplayFeeder:
    def __init__(self, start: str, speed: float = 120.0, end: str | None = None, minutes: int = 5):
        d = load_5m()
        d = d[d.index >= pd.Timestamp(start, tz="UTC")]
        if end:
            d = d[d.index < pd.Timestamp(end, tz="UTC")]
        self.data = d
        self.i = 0
        self.speed = speed
        self.minutes = minutes
        self._now = d.index[0].to_pydatetime() if len(d) else datetime.now(tz=timezone.utc)

    def resume_from_db(self) -> int:
        """Après un redémarrage : reprend après la dernière barre déjà rejouée (aucun doublon). Renvoie l'index."""
        from sqlalchemy import func, select

        with db.session() as s:
            last = s.execute(select(func.max(db.Bar.ts)).where(db.Bar.source == "replay")).scalar()
        if last is not None:
            self.i = int((self.data.index <= pd.Timestamp(last)).sum())
            if self.i:
                self._now = self.data.index[self.i - 1].to_pydatetime() + timedelta(minutes=self.minutes, seconds=1)
        return self.i

    def seed_daily_history(self, days: int = 300) -> int:
        """Historique journalier antérieur au début du rejeu (équivalent du message « daily » de TradingView)."""
        if not len(self.data):
            return 0
        from sqlalchemy import select

        with db.session() as s:
            if s.execute(select(db.DailyBar.id).where(db.DailyBar.source == "replay").limit(1)).first():
                return 0  # déjà chargé (redémarrage)
        h = load_15m()
        h = h[h.index < self.data.index[0]]
        tc = time_columns(h.index)
        g = pd.DataFrame({"td": tc["td"].to_numpy(), "h": h["high"].to_numpy(), "l": h["low"].to_numpy(), "c": h["close"].to_numpy()})
        first_td = int(time_columns(self.data.index[:1])["td"].iloc[0])
        daily = g.groupby("td").agg(h=("h", "max"), l=("l", "min"), c=("c", "last"))
        daily = daily[daily.index < first_td].iloc[-days:]  # journées complètes uniquement
        with db.session() as s:
            for td, r in daily.iterrows():
                s.add(db.DailyBar(source="replay", symbol="XAUUSD-historique", td=int(td), high=float(r["h"]), low=float(r["l"]), close=float(r["c"])))
        return len(daily)

    def now(self) -> datetime:
        return self._now

    def step(self) -> bool:
        if self.i >= len(self.data):
            return False
        ts = self.data.index[self.i].to_pydatetime()
        r = self.data.iloc[self.i]
        sym = active_contract(trading_date(ts)).code
        with db.session() as s:
            s.add(db.Bar(source="replay", symbol=sym, ts=ts, minutes=self.minutes, open=float(r["open"]), high=float(r["high"]),
                         low=float(r["low"]), close=float(r["close"]), volume=float(r["volume"]), processed=False,
                         received_at=ts + timedelta(minutes=self.minutes)))
        self._now = ts + timedelta(minutes=self.minutes, seconds=1)
        self.i += 1
        if self.speed > 0:
            time.sleep(1.0 / self.speed)
        return True
