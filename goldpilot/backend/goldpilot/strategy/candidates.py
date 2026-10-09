"""Candidats S1 et S2, codés exactement selon docs/03_protocole_de_recherche.md (section 4).

Chaque candidat :
* `prepare(bars)` : colonnes causales vectorisées (DataFrame aligné sur les barres) ;
* `evaluate(i, F, state)` : analyse à la clôture de la barre i → Evaluation (contexte, setups,
  raisons explicites quand il n'y a pas de trade).
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from ..timeutil import msess_of
from .base import NS_MIN, Evaluation, Setup, StrategyState, fmt
from .indicators import atr, prev_day_range_rank, price_at_msess, session_mean, time_columns

BAR_MIN = 15


def base_features(bars: pd.DataFrame, need_range_rank: bool = False) -> pd.DataFrame:
    tc = time_columns(bars.index)
    F = pd.DataFrame(index=tc.index)
    for k in ("open", "high", "low", "close"):
        F[k] = bars[k].to_numpy(dtype=float)
    F["msess"], F["td"] = tc["msess"].to_numpy(), tc["td"].to_numpy()
    F["atr"] = atr(F["high"], F["low"], F["close"])
    F["sm"] = session_mean(F["high"], F["low"], F["close"], F["td"])
    F["z"] = (F["close"] - F["sm"]) / F["atr"]
    if need_range_rank:
        F["rr_rank"] = prev_day_range_rank(F["high"], F["low"], F["close"], F["td"])
    return F


def arrays(F: pd.DataFrame) -> dict:
    """Colonnes de F en tableaux numpy, mises en cache sur l'objet (F n'est jamais modifié après préparation)."""
    cache = F.attrs.get("_np")
    if cache is None or cache.get("_len") != len(F):
        cache = {c: F[c].to_numpy() for c in F.columns}
        cache["_ts"] = F.index.asi8
        cache["_len"] = len(F)
        F.attrs["_np"] = cache
    return cache


class _Candidate:
    name = "?"
    warmup_bars = 60

    def __init__(self, **params):
        self.params = params
        self.config_id = self.name + "|" + ",".join(f"{k}={v}" for k, v in sorted(params.items()))

    def _setup(self, F: pd.DataFrame, i: int, **kw) -> Setup:
        A = arrays(F)
        ts = int(A["_ts"][i])
        return Setup(strategy=self.name, config_id=self.config_id, atr=float(A["atr"][i]),
                     ref_price=float(A["close"][i]), decision_bar_ts=ts, decision_ts=ts + BAR_MIN * NS_MIN,
                     td=int(A["td"][i]), **kw)


class S1SessionExtension(_Candidate):
    """S1 — Extension de séance : suivre un prix qui franchit k ATR d'écart à sa moyenne de séance."""

    name = "S1"

    def __init__(self, k: float = 4.0, s: float = 2.5, t: float = 3.0, F: bool = False):
        super().__init__(k=k, s=s, t=t, F=F)
        self.k, self.s, self.t, self.use_filter = k, s, t, F
        self.w0, self.w1, self.exit = msess_of("03:00"), msess_of("13:00"), msess_of("15:30")
        self.warmup_bars = 60 if not F else 60

    def prepare(self, bars: pd.DataFrame) -> pd.DataFrame:
        return base_features(bars, need_range_rank=self.use_filter)

    def evaluate(self, i: int, F: pd.DataFrame, st: StrategyState) -> Evaluation:
        A = arrays(F)
        ts = int(A["_ts"][i])
        close_m = int(A["msess"][i]) + BAR_MIN
        a, z, sm, c = A["atr"][i], A["z"][i], A["sm"][i], A["close"][i]
        ctx = {"z": None if not np.isfinite(z) else round(float(z), 2), "session_mean": None if not np.isfinite(sm) else round(float(sm), 2),
               "atr": None if not np.isfinite(a) else round(float(a), 2)}
        regime = "indéterminé"
        if np.isfinite(z):
            regime = "extension haussière" if z > self.k else "extension baissière" if z < -self.k else (
                "tendance modérée" if abs(z) > self.k / 2 else "équilibre autour de la moyenne")
        reasons: list[str] = []
        if not (self.w0 <= close_m <= self.w1):
            reasons.append("hors de la fenêtre de décision 03:00-13:00 New York")
        if not (np.isfinite(a) and a > 0 and np.isfinite(z)):
            reasons.append("indicateurs pas encore disponibles (historique insuffisant)")
        if st.has_position:
            reasons.append("une position est déjà en cours")
        if reasons:
            return Evaluation(ts, regime, ctx, [], reasons)
        same_day_prev = i > 0 and A["td"][i - 1] == A["td"][i]
        zp = A["z"][i - 1] if same_day_prev else np.nan
        up = z > self.k and (not np.isfinite(zp) or zp <= self.k)
        dn = z < -self.k and (not np.isfinite(zp) or zp >= -self.k)
        if not (up or dn):
            reasons.append(f"pas de franchissement du seuil d'extension ±{self.k:g} ATR (écart actuel {z:+.1f} ATR)")
            return Evaluation(ts, regime, ctx, [], reasons)
        tag = "ext_long" if up else "ext_short"
        if tag in st.tags_today or tag in st.pending_tags:
            reasons.append("un signal dans ce sens a déjà été donné aujourd'hui (un seul par sens et par jour)")
            return Evaluation(ts, regime, ctx, [], reasons)
        if self.use_filter:
            rk = A["rr_rank"][i]
            ctx["rang_volatilite_veille"] = None if not np.isfinite(rk) else round(float(rk), 2)
            if not np.isfinite(rk):
                reasons.append("filtre de volatilité indisponible (moins de 125 jours d'historique)")
                return Evaluation(ts, regime, ctx, [], reasons)
            if rk > 2 / 3:
                reasons.append("veille dans le tiers le plus volatil des 250 derniers jours : prolongements moins fiables")
                return Evaluation(ts, regime, ctx, [], reasons)
        side = 1 if up else -1
        stop = c - side * self.s * a
        word = "au-dessus" if up else "en dessous"
        su = self._setup(
            F, i, side=side, entry_type="market", entry=None, stop=float(stop), target=None, trail_atr=self.t,
            valid_until_ts=ts + 2 * BAR_MIN * NS_MIN, exit_msess=self.exit, tag=tag,
            rationale=(f"Le prix ({fmt(c)}) est à {abs(z):.1f} ATR {word} de sa moyenne de séance ({fmt(sm)}) : "
                       f"mouvement directionnel de journée de tendance, historiquement suivi d'un prolongement."),
            invalidation=(f"Stop initial {fmt(stop)} ({self.s:g} ATR), puis stop suiveur à {self.t:g} ATR de l'extrême atteint. "
                          f"Sortie au plus tard à 15:30 New York. Ne pas entrer si le prix s'est écarté de plus de 0,5 ATR de {fmt(c)}."),
        )
        return Evaluation(ts, regime, ctx, [su], [])


class S2LondonToNewYork(_Candidate):
    """S2 — Continuité Londres → New York : prolonger à 08:00 la direction prise entre 02:00 et 08:00."""

    name = "S2"

    def __init__(self, q: float = 2.0, s: float = 2.0, E: str = "12:00"):
        super().__init__(q=q, s=s, E=E)
        self.q, self.s, self.E = q, s, E
        self.m02, self.m08 = msess_of("02:00"), msess_of("08:00")
        self.exit = msess_of("12:00") if E == "12:00" else msess_of("15:30")
        self.trail = None if E == "12:00" else 3.0

    def prepare(self, bars: pd.DataFrame) -> pd.DataFrame:
        F = base_features(bars)
        F["c02"] = price_at_msess(F["close"], F["msess"], F["td"], self.m02, BAR_MIN)
        return F

    def evaluate(self, i: int, F: pd.DataFrame, st: StrategyState) -> Evaluation:
        A = arrays(F)
        ts = int(A["_ts"][i])
        close_m = int(A["msess"][i]) + BAR_MIN
        a, c, c02 = A["atr"][i], A["close"][i], A["c02"][i]
        m = (c - c02) / a if (np.isfinite(c02) and np.isfinite(a) and a > 0) else np.nan
        ctx = {"mouvement_londres_ATR": None if not np.isfinite(m) else round(float(m), 2), "atr": None if not np.isfinite(a) else round(float(a), 2)}
        regime = "indéterminé" if not np.isfinite(m) else ("Londres haussière" if m > 0 else "Londres baissière")
        if close_m != self.m08:
            return Evaluation(ts, regime, ctx, [], ["décision uniquement à la clôture de 08:00 New York"])
        reasons = []
        if not np.isfinite(m):
            reasons.append("prix de 02:00 ou ATR indisponible")
        if st.has_position:
            reasons.append("une position est déjà en cours")
        if not reasons and abs(m) < self.q:
            reasons.append(f"mouvement de Londres trop faible ({m:+.1f} ATR, seuil ±{self.q:g})")
        if reasons:
            return Evaluation(ts, regime, ctx, [], reasons)
        side = 1 if m > 0 else -1
        stop = c - side * self.s * a
        sens = "hausse" if side > 0 else "baisse"
        su = self._setup(
            F, i, side=side, entry_type="market", entry=None, stop=float(stop), target=None, trail_atr=self.trail,
            valid_until_ts=ts + 2 * BAR_MIN * NS_MIN, exit_msess=self.exit, tag="london_ny",
            rationale=(f"Londres a nettement monté/baissé ({m:+.1f} ATR entre 02:00 et 08:00) : pari que la {sens} se prolonge "
                       f"pendant la matinée de New York."),
            invalidation=(f"Stop {fmt(stop)} ({self.s:g} ATR). Sortie à {'12:00' if self.E == '12:00' else '15:30 (stop suiveur 3 ATR)'} New York."),
        )
        return Evaluation(ts, regime, ctx, [su], [])


def grid() -> dict[str, list]:
    g = {"S1": [], "S2": []}
    for k in (3.0, 4.0, 5.0):
        for s in (1.5, 2.5):
            for t in (2.0, 3.0):
                for f in (False, True):
                    g["S1"].append(S1SessionExtension(k=k, s=s, t=t, F=f))
    for q in (2.0, 4.0):
        for s in (2.0, 3.0):
            for E in ("12:00", "suivi"):
                g["S2"].append(S2LondonToNewYork(q=q, s=s, E=E))
    return g
