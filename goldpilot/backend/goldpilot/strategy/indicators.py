"""Indicateurs strictement causaux (la valeur à la barre i n'utilise que les barres ≤ i).

Utilisés à l'identique par la recherche (historique complet) et par le moteur temps réel (fenêtre des
dernières barres). Les tests `test_causality.py` vérifient qu'ajouter des barres futures ne change
aucune valeur passée.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

ATR_LEN = 40


def time_columns(index_utc: pd.DatetimeIndex) -> pd.DataFrame:
    """msess (minute de séance depuis 18:00 New York) et td (journée de trading, jours depuis 1970)."""
    idx = index_utc.as_unit("ns")
    ny = idx.tz_convert("America/New_York")
    nymin = ny.hour * 60 + ny.minute
    msess = (nymin - 18 * 60) % 1440
    td = ((ny + pd.Timedelta(hours=6)).tz_localize(None).normalize().as_unit("ns").asi8 // 86_400_000_000_000)
    return pd.DataFrame({"msess": np.asarray(msess, dtype=np.int64), "td": np.asarray(td, dtype=np.int64)}, index=idx)


def true_range(h: pd.Series, l: pd.Series, c: pd.Series) -> pd.Series:
    pc = c.shift(1)
    return pd.concat([h - l, (h - pc).abs(), (l - pc).abs()], axis=1).max(axis=1)


def atr(h: pd.Series, l: pd.Series, c: pd.Series, n: int = ATR_LEN) -> pd.Series:
    return true_range(h, l, c).rolling(n, min_periods=n).mean()


def session_mean(h: pd.Series, l: pd.Series, c: pd.Series, td: pd.Series) -> pd.Series:
    """Moyenne des prix typiques depuis le début de la journée de trading, barre courante incluse."""
    tp = (h + l + c) / 3.0
    return tp.groupby(td.to_numpy()).cumsum() / (tp.groupby(td.to_numpy()).cumcount() + 1)


def prev_day_range_rank(h: pd.Series, l: pd.Series, c: pd.Series, td: pd.Series, lookback: int = 250) -> pd.Series:
    """Rang centile (0-1) de l'amplitude relative de la VEILLE parmi les `lookback` journées précédentes.

    Calculé uniquement avec des journées complètes antérieures à la journée courante.
    """
    df = pd.DataFrame({"h": h.to_numpy(), "l": l.to_numpy(), "c": c.to_numpy(), "td": td.to_numpy()})
    daily = df.groupby("td").agg(h=("h", "max"), l=("l", "min"), c=("c", "last"))
    rr = (daily["h"] - daily["l"]) / daily["c"]
    prev = rr.shift(1)
    hist = rr.shift(2)  # journées antérieures à la veille
    ranks = []
    vals_prev = prev.to_numpy()
    vals_hist = hist.to_numpy()
    for i in range(len(daily)):
        lo = max(0, i - lookback + 1)
        window = vals_hist[lo:i + 1]
        window = window[np.isfinite(window)]
        if len(window) < lookback // 2 or not np.isfinite(vals_prev[i]):
            ranks.append(np.nan)
        else:
            ranks.append(float((window < vals_prev[i]).mean()))
    r = pd.Series(ranks, index=daily.index)
    return pd.Series(r.reindex(df["td"]).to_numpy(), index=h.index)


def price_at_msess(c: pd.Series, msess: pd.Series, td: pd.Series, end_msess: int, bar_minutes: int) -> pd.Series:
    """Clôture de la barre qui se termine exactement à end_msess, propagée aux barres suivantes du même jour."""
    hit = (msess + bar_minutes) == end_msess
    s = pd.Series(np.where(hit, c, np.nan), index=c.index)
    later = (msess + bar_minutes) >= end_msess
    out = s.groupby(td.to_numpy()).ffill()
    return out.where(later)
