"""Métriques de performance, en R (1 R = risque prévu du trade) et nettes de coûts, avec incertitude.

Les intervalles de confiance sont obtenus par bootstrap de journées entières (préserve la dépendance
entre trades d'une même journée).
"""
from __future__ import annotations

import math

import numpy as np
import pandas as pd
from scipy import stats

EULER = 0.5772156649015329


def streak(wins: np.ndarray, value: bool) -> int:
    best = cur = 0
    for w in wins:
        cur = cur + 1 if w == value else 0
        best = max(best, cur)
    return best


def max_drawdown(r: np.ndarray) -> float:
    if len(r) == 0:
        return 0.0
    eq = np.concatenate([[0.0], np.cumsum(r)])
    return float((eq - np.maximum.accumulate(eq)).min())


def bootstrap_ci(trades: pd.DataFrame, n_boot: int = 3000, seed: int = 3) -> dict:
    if trades.empty:
        return {}
    g = trades.groupby("td")["r"].agg(["sum", "count"])
    s, c = g["sum"].to_numpy(), g["count"].to_numpy()
    rng = np.random.default_rng(seed)
    pick = rng.integers(0, len(s), size=(n_boot, len(s)))
    means = s[pick].sum(1) / c[pick].sum(1)
    return {"ic95_bas": float(np.quantile(means, 0.025)), "ic95_haut": float(np.quantile(means, 0.975)),
            "ic_unilateral95_bas": float(np.quantile(means, 0.05))}


def daily_series(trades: pd.DataFrame, all_days: np.ndarray) -> np.ndarray:
    d = trades.groupby("td")["r"].sum() if not trades.empty else pd.Series(dtype=float)
    return pd.Series(0.0, index=all_days).add(d, fill_value=0.0).reindex(all_days).fillna(0.0).to_numpy()


def deflated_sharpe(sr: float, sr_trials: np.ndarray, T: int, skew: float, kurt: float) -> float:
    """Bailey & López de Prado (2014) : probabilité que le Sharpe dépasse le maximum attendu par hasard."""
    N = len(sr_trials)
    if N < 2 or T < 3 or not np.isfinite(sr):
        return math.nan
    v = max(float(np.var(sr_trials, ddof=1)), 1e-12)
    sr0 = math.sqrt(v) * ((1 - EULER) * stats.norm.ppf(1 - 1 / N) + EULER * stats.norm.ppf(1 - 1 / (N * math.e)))
    den = 1 - skew * sr + (kurt - 1) / 4 * sr * sr
    if den <= 0:
        return math.nan
    return float(stats.norm.cdf((sr - sr0) * math.sqrt(T - 1) / math.sqrt(den)))


def summary(trades: pd.DataFrame, ci: bool = True) -> dict:
    if trades is None or trades.empty:
        return {"n": 0}
    t = trades.sort_values("entry_ts")
    r = t["r"].to_numpy(dtype=float)
    w, lo = r[r > 0], r[r <= 0]
    gl = -lo.sum()
    months = max(1.0, (t["entry_time"].max() - t["entry_time"].min()).days / 30.44)
    out = {
        "n": int(len(r)),
        "taux_de_gain": float((r > 0).mean()),
        "gain_moyen_R": float(w.mean()) if len(w) else 0.0,
        "perte_moyenne_R": float(lo.mean()) if len(lo) else 0.0,
        "esperance_R": float(r.mean()),
        "ecart_type_R": float(r.std(ddof=1)) if len(r) > 1 else math.nan,
        "t": float(r.mean() / r.std(ddof=1) * math.sqrt(len(r))) if len(r) > 1 and r.std(ddof=1) > 0 else math.nan,
        "profit_factor": float(w.sum() / gl) if gl > 0 else math.inf,
        "total_R": float(r.sum()),
        "drawdown_max_R": max_drawdown(r),
        "serie_pertes_max": streak(r > 0, False),
        "serie_gains_max": streak(r > 0, True),
        "trades_par_mois": float(len(r) / months),
        "duree_moyenne_barres": float(t["bars"].mean()),
        "glissement_entree_moyen_oz": float(t["entry_slip"].mean()),
        "sorties": t["exit_reason"].value_counts().to_dict(),
    }
    if ci:
        out.update(bootstrap_ci(t))
    return out


def by_group(trades: pd.DataFrame, key: pd.Series) -> pd.DataFrame:
    if trades.empty:
        return pd.DataFrame()
    g = trades["r"].groupby(key)
    return pd.DataFrame({"n": g.size(), "esperance_R": g.mean(), "total_R": g.sum(),
                         "taux_de_gain": g.apply(lambda x: (x > 0).mean())}).round(4)


def session_of(trades: pd.DataFrame) -> pd.Series:
    ny = trades["entry_time"].dt.tz_convert("America/New_York")
    m = ny.dt.hour * 60 + ny.dt.minute
    return pd.Series(np.select([(m >= 18 * 60) | (m < 3 * 60), m < 8 * 60, m < 12 * 60],
                               ["Asie", "Londres", "New York matin"], "New York après-midi"), index=trades.index)


# ---------------------------------------------------------------- compléments (ajouts rétro-compatibles)
def drawdown_durations(trades: pd.DataFrame, all_days: np.ndarray) -> dict:
    """Durées des drawdowns en JOURS DE TRADING (journées sans trade comprises).

    Équité = somme cumulée des R par journée de trading (`daily_series`), sommet initial = 0. Un drawdown
    commence le premier jour où l'équité passe sous le dernier sommet et dure jusqu'à la veille du jour où
    ce sommet est retrouvé ; durée = nombre de jours passés sous le sommet. Un drawdown non résorbé à la
    fin de la période est compté avec sa durée observée et signalé (`drawdown_en_cours_fin`).
    """
    d = daily_series(trades, all_days)
    eq = np.cumsum(d)
    peak, start, durs = 0.0, None, []
    for k, e in enumerate(eq):
        if e < peak - 1e-12:
            if start is None:
                start = k
        else:
            if start is not None:
                durs.append(k - start)
                start = None
            peak = max(peak, float(e))
    ongoing = start is not None
    if ongoing:
        durs.append(len(eq) - start)
    return {"duree_max_jours": int(max(durs)) if durs else 0,
            "duree_mediane_jours": float(np.median(durs)) if durs else 0.0,
            "nb_drawdowns": len(durs), "drawdown_en_cours_fin": bool(ongoing),
            "duree_en_cours_jours": int(durs[-1]) if ongoing else 0, "jours_de_trading": int(len(eq))}


def in_dollars(s: dict, risk_usd: float) -> dict:
    """Conversion en dollars d'un `summary` en R, au risque exact `risk_usd` par trade (1 R = risk_usd, coûts
    inclus car R est net). Ignore l'arrondi au nombre entier de contrats MGC."""
    out = {"risque_par_trade_usd": float(risk_usd)}
    names = {"esperance_R": "esperance_usd", "ic95_bas": "ic95_bas_usd", "ic95_haut": "ic95_haut_usd",
             "ic_unilateral95_bas": "ic_unilateral95_bas_usd", "drawdown_max_R": "drawdown_max_usd", "total_R": "total_usd"}
    for k, name in names.items():
        v = s.get(k)
        if v is not None and np.isfinite(v):
            out[name] = round(float(v) * risk_usd, 2)
    return out


def volatility_tercile_by_day(bars: pd.DataFrame, td: np.ndarray, window: int = 20, lookback: int = 250) -> pd.Series:
    """Régime de volatilité par journée de trading, calculé de façon CAUSALE.

    Mesure = moyenne sur `window` journées complètes de l'amplitude relative (H−L)/C, connue la veille
    (journées strictement antérieures). Régime = tercile de cette mesure parmi celles des `lookback`
    journées précédentes : « faible », « moyenne », « forte » ; NaN si moins de lookback/2 journées d'historique.
    """
    df = pd.DataFrame({"h": bars["high"].to_numpy(float), "l": bars["low"].to_numpy(float), "c": bars["close"].to_numpy(float), "td": td})
    daily = df.groupby("td").agg(h=("h", "max"), l=("l", "min"), c=("c", "last"))
    known = ((daily["h"] - daily["l"]) / daily["c"]).rolling(window, min_periods=window).mean().shift(1).to_numpy()
    lab = []
    for i in range(len(known)):
        hist = known[max(0, i - lookback):i]
        hist = hist[np.isfinite(hist)]
        x = known[i]
        if not np.isfinite(x) or len(hist) < lookback // 2:
            lab.append(np.nan)
            continue
        q = float((hist < x).mean())
        lab.append("faible" if q < 1 / 3 else "moyenne" if q < 2 / 3 else "forte")
    return pd.Series(lab, index=daily.index, dtype=object)
