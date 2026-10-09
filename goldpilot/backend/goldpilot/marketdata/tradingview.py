"""Réception des webhooks TradingView (script Pine « GoldPilot Bridge »).

Format accepté (JSON, ≤ 4 Ko) :
  barre : {"v":1,"kind":"bar","token":"…","ticker":"MGCZ2026","tf":"1","t":<ms début de barre>,
           "o":…,"h":…,"l":…,"c":…,"vol":…,"tnow":<ms heure d'envoi>}
  miroir : {"v":1,"kind":"mirror","token":"…","ticker":"MGCZ2026","t":<ms barre 15 min>,"side":1|-1,"price":…}

Contrôles : jeton secret (comparaison à temps constant), liste d'IP TradingView (optionnelle),
schéma strict, contrat MGC daté, cohérence OHLC, horodatage plausible, détection des données
différées (une barre reçue plus de 3 minutes après sa clôture indique un flux en retard, par exemple
un compte TradingView sans le forfait temps réel COMEX).
TradingView coupe la requête après 3 s et la renvoie jusqu'à 3 fois en cas d'erreur 5xx : le traitement
est donc minimal (validation + insertion idempotente) et toute répétition est ignorée sans erreur.
"""
from __future__ import annotations

import hmac
import math
from datetime import datetime, timedelta, timezone
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from .contracts import parse_tv_symbol

MAX_BODY = 4096
DELAY_LIMIT = timedelta(minutes=3)


class BarMsg(BaseModel):
    model_config = ConfigDict(extra="forbid")
    v: Literal[1]
    kind: Literal["bar"]
    token: str = Field(min_length=1, max_length=200)
    ticker: str = Field(min_length=3, max_length=40)
    tf: Literal["1"]
    t: int
    o: float
    h: float
    l: float  # noqa: E741
    c: float
    vol: float = 0.0
    tnow: int

    @field_validator("o", "h", "l", "c")
    @classmethod
    def finite_positive(cls, x: float) -> float:
        if not math.isfinite(x) or x <= 0 or x > 100_000:
            raise ValueError("prix invalide")
        return x


class MirrorMsg(BaseModel):
    model_config = ConfigDict(extra="forbid")
    v: Literal[1]
    kind: Literal["mirror"]
    token: str = Field(min_length=1, max_length=200)
    ticker: str = Field(min_length=3, max_length=40)
    t: int
    side: Literal[1, -1]
    price: float


class DailyMsg(BaseModel):
    """Historique journalier du MGC continu (amplitudes des journées passées) : [[t_ms, haut, bas, clôture], ...]."""

    model_config = ConfigDict(extra="forbid")
    v: Literal[1]
    kind: Literal["daily"]
    token: str = Field(min_length=1, max_length=200)
    ticker: str = Field(min_length=3, max_length=40)
    t: int
    days: list[list[float]] = Field(min_length=1, max_length=80)

    @field_validator("days")
    @classmethod
    def check_days(cls, v: list[list[float]]) -> list[list[float]]:
        for row in v:
            if len(row) != 4 or not all(math.isfinite(x) for x in row):
                raise ValueError("ligne journalière invalide")
            _, h, l, c = row
            if not (0 < l <= c <= h < 100_000):
                raise ValueError("haut/bas/clôture incohérents")
        return v


class Rejected(Exception):
    def __init__(self, status: int, reason: str):
        super().__init__(reason)
        self.status, self.reason = status, reason


def token_ok(given: str, expected: str) -> bool:
    return bool(expected) and hmac.compare_digest(given.encode(), expected.encode())


def ms_to_dt(ms: int) -> datetime:
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc)


def parse(payload: dict, expected_token: str, now: datetime) -> BarMsg | MirrorMsg | DailyMsg:
    kind = payload.get("kind") if isinstance(payload, dict) else None
    models = {"bar": BarMsg, "mirror": MirrorMsg, "daily": DailyMsg}
    try:
        msg = models[kind].model_validate(payload) if kind in models else None
    except ValidationError as e:
        raise Rejected(400, f"message invalide : {e.errors()[0].get('msg', 'schéma')}") from None
    if msg is None:
        raise Rejected(400, "type de message inconnu")
    if not token_ok(msg.token, expected_token):
        raise Rejected(401, "jeton invalide")
    if isinstance(msg, DailyMsg):
        if not msg.ticker.split(":")[-1].upper().startswith("MGC"):
            raise Rejected(422, f"historique journalier : symbole MGC attendu, reçu {msg.ticker}")
        return msg
    if parse_tv_symbol(msg.ticker) is None:
        raise Rejected(422, f"symbole non accepté : {msg.ticker} (attendu : contrat MGC daté, ex. MGCZ2026)")
    t = ms_to_dt(msg.t)
    if t > now + timedelta(minutes=2):
        raise Rejected(422, "horodatage dans le futur")
    if isinstance(msg, BarMsg):
        if msg.t % 60_000 != 0:
            raise Rejected(422, "la barre ne commence pas sur une minute ronde")
        if msg.h < max(msg.o, msg.c) or msg.l > min(msg.o, msg.c) or msg.h < msg.l:
            raise Rejected(422, "OHLC incohérent")
    return msg


def delay_of(msg: BarMsg, received: datetime) -> timedelta:
    """Retard entre la clôture de la barre et sa réception par le serveur."""
    return received - (ms_to_dt(msg.t) + timedelta(minutes=1))
