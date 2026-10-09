"""Étude exploratoire — période d'ENTRAÎNEMENT uniquement (01/05/2011 → 31/12/2018).

But : mesurer des propriétés statistiques du marché de l'or AVANT de concevoir des règles, pour que
chaque stratégie candidate repose sur une hypothèse étayée. Aucune donnée postérieure à 2018 n'est lue.

Toutes les variations sont exprimées en unités d'ATR (true range moyen sur 40 barres de 15 min, connu
à l'instant de la mesure), ce qui rend les années comparables malgré les changements de prix.
Coût de référence d'un aller-retour MGC : 0,50 $/once à 4 000 $ (1,25 point de base du prix) ; son
équivalent en ATR est indiqué pour juger si un effet est exploitable après coûts.

Tests multiples : beaucoup de mesures sont faites ; seuls les effets avec |t| ≥ 3 sont considérés
comme des pistes sérieuses (correction approximative de type Bonferroni pour ~50 tests).
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))
from goldpilot.research.data import load_15m  # noqa: E402

OUT = Path(__file__).resolve().parent / "output" / "etude_exploratoire"
OUT.mkdir(parents=True, exist_ok=True)
TRAIN_END = pd.Timestamp("2019-01-01", tz="UTC")
COST_BP = 0.50 / 4000  # coût aller-retour en fraction du prix


def prepare() -> pd.DataFrame:
    d = load_15m()
    d = d[d.index < TRAIN_END].copy()
    assert d.index.max() < TRAIN_END
    ny = d.index.tz_convert("America/New_York")
    d["nymin"] = ny.hour * 60 + ny.minute
    d["msess"] = (d["nymin"] - 18 * 60) % 1440
    d["td"] = (ny + pd.Timedelta(hours=6)).tz_localize(None).normalize()
    tr = np.maximum(d["high"] - d["low"], np.maximum((d["high"] - d["close"].shift()).abs(), (d["low"] - d["close"].shift()).abs()))
    d["atr"] = tr.rolling(40).mean()
    d["lr"] = np.log(d["close"]).diff()
    d["cost_atr"] = COST_BP * d["close"] / d["atr"]
    return d.dropna(subset=["atr"])


def tstat(x: np.ndarray) -> tuple[float, float, int]:
    x = np.asarray(x, dtype=float)
    x = x[np.isfinite(x)]
    n = len(x)
    if n < 20:
        return math.nan, math.nan, n
    return float(x.mean()), float(x.mean() / x.std(ddof=1) * math.sqrt(n)), n


def price_at(d: pd.DataFrame, msess_end: int) -> pd.Series:
    """Prix de clôture de la dernière barre se terminant au plus tard à la minute de séance msess_end, par journée."""
    sub = d[(d["msess"] + 15) <= msess_end]
    return sub.groupby("td")["close"].last()


def atr_at(d: pd.DataFrame, msess_end: int) -> pd.Series:
    sub = d[(d["msess"] + 15) <= msess_end]
    return sub.groupby("td")["atr"].last()


M = lambda hhmm: (int(hhmm[:2]) * 60 + int(hhmm[3:]) - 18 * 60) % 1440  # noqa: E731


def segment_predictability(d: pd.DataFrame) -> list[dict]:
    """La variation d'un segment de séance prédit-elle celle du segment suivant ? (momentum / retournement)"""
    pairs = [
        ("Asie 18:00→02:00", "18:00", "02:00", "Londres 02:00→08:00", "02:00", "08:00"),
        ("Londres 02:00→08:00", "02:00", "08:00", "NY matin 08:00→12:00", "08:00", "12:00"),
        ("Nuit 18:00→08:00", "18:00", "08:00", "NY matin 08:00→12:00", "08:00", "12:00"),
        ("08:00→09:30", "08:00", "09:30", "09:30→12:00", "09:30", "12:00"),
        ("08:00→10:00", "08:00", "10:00", "10:00→14:00", "10:00", "14:00"),
        ("NY matin 08:00→12:00", "08:00", "12:00", "NY après-midi 12:00→15:45", "12:00", "15:45"),
        ("Séance 18:00→15:00", "18:00", "15:00", "Fin 15:00→16:00", "15:00", "16:00"),
    ]
    out = []
    for name_a, a0, a1, name_b, b0, b1 in pairs:
        pa0 = price_at(d, M(a0)) if a0 != "18:00" else d.groupby("td")["open"].first()
        pa1, pb1 = price_at(d, M(a1)), price_at(d, M(b1))
        pb0 = price_at(d, M(b0)) if b0 != "18:00" else d.groupby("td")["open"].first()
        atr = atr_at(d, M(b0))
        df = pd.concat({"a": (pa1 - pa0) / atr, "b": (pb1 - pb0) / atr}, axis=1).dropna()
        df = df[(df["a"].abs() < 50) & (df["b"].abs() < 50)]
        if len(df) < 100:
            continue
        x, y = df["a"].to_numpy(), df["b"].to_numpy()
        beta = np.polyfit(x, y, 1)[0]
        corr = np.corrcoef(x, y)[0, 1]
        t_corr = corr * math.sqrt((len(df) - 2) / (1 - corr ** 2))
        # rendement « suivre le signe » du segment A sur le segment B
        follow = np.sign(x) * y
        m, t, n = tstat(follow)
        out.append({"segment_A": name_a, "segment_B": name_b, "jours": int(len(df)), "beta": round(beta, 4),
                    "correlation": round(corr, 4), "t_correlation": round(t_corr, 2),
                    "suivre_signe_A_moyenne_ATR": round(m, 3), "t": round(t, 2)})
    return out


def bar_autocorrelation(d: pd.DataFrame) -> list[dict]:
    """Autocorrélation des rendements consécutifs (15, 30, 60 min) par séance."""
    out = []
    for tf in (15, 30, 60):
        r = d["close"].resample(f"{tf}min", label="left", closed="left").last().dropna()
        lr = np.log(r).diff()
        ny = lr.index.tz_convert("America/New_York")
        m = ny.hour * 60 + ny.minute
        nxt = lr.shift(-1)
        gap_ok = (pd.Series(lr.index, index=lr.index).diff().shift(-1) == pd.Timedelta(minutes=tf))
        for sess, (lo, hi) in {"Asie": (18 * 60, 26 * 60), "Londres": (2 * 60, 8 * 60), "NY matin": (8 * 60, 12 * 60), "NY après-midi": (12 * 60, 16 * 60)}.items():
            mm = np.where(m < 12 * 60, m + 1440, m) if sess == "Asie" else m
            mask = (mm >= lo) & (mm < hi) & gap_ok.to_numpy()
            x, y = lr[mask].to_numpy(), nxt[mask].to_numpy()
            ok = np.isfinite(x) & np.isfinite(y)
            x, y = x[ok], y[ok]
            c = np.corrcoef(x, y)[0, 1]
            out.append({"unite": f"{tf} min", "seance": sess, "n": int(len(x)), "autocorrelation": round(c, 4),
                        "t": round(c * math.sqrt(len(x)), 2)})
    return out


def breakout_follow_through(d: pd.DataFrame) -> list[dict]:
    """Après une clôture au-delà du plus haut / bas des N dernières heures, le prix continue-t-il ?

    Rendement mesuré en ATR, de la clôture de la barre de cassure à la clôture H heures plus tard, dans
    le sens de la cassure (brut, sans coûts ; le coût moyen en ATR est indiqué à côté).
    """
    out = []
    c, h, l, atr = d["close"], d["high"], d["low"], d["atr"]
    for n_h in (2, 4, 8):
        nb = n_h * 4
        hh = h.shift(1).rolling(nb).max()
        ll = l.shift(1).rolling(nb).min()
        up = c > hh
        dn = c < ll
        for window, (lo, hi) in {"Londres 02:00-08:00": ("02:00", "08:00"), "NY 08:00-11:00": ("08:00", "11:00"), "NY 11:00-14:00": ("11:00", "14:00"), "Asie 19:00-02:00": ("19:00", "02:00")}.items():
            a, b = M(lo), M(hi)
            inwin = (d["msess"] >= a) & (d["msess"] < b)
            for H in (1, 2, 4):
                k = H * 4
                fwd = (c.shift(-k) - c) / atr
                same_day = d["td"].shift(-k) == d["td"]
                sig = pd.Series(np.where(up, 1.0, np.where(dn, -1.0, np.nan)), index=d.index)
                sel = inwin & sig.notna() & same_day
                x = (sig[sel] * fwd[sel]).to_numpy()
                m, t, n = tstat(x)
                out.append({"cassure_N_heures": n_h, "fenetre": window, "horizon_h": H, "n": n,
                            "suite_moyenne_ATR": round(m, 3), "t": round(t, 2),
                            "cout_moyen_ATR": round(float(d.loc[sel, "cost_atr"].mean()), 3)})
    return out


def opening_range(d: pd.DataFrame) -> list[dict]:
    """Range 08:30-09:30 New York : la cassure (première clôture au-delà, avant 11:30) se prolonge-t-elle ?"""
    out = []
    a, b, e = M("08:30"), M("09:30"), M("11:30")
    for H in (1, 2, 4):
        res = []
        for td, g in d.groupby("td"):
            rng = g[(g["msess"] >= a) & (g["msess"] < b)]
            if len(rng) < 4:
                continue
            rh, rl = rng["high"].max(), rng["low"].min()
            after = g[(g["msess"] >= b) & (g["msess"] < e)]
            hit = after[(after["close"] > rh) | (after["close"] < rl)]
            if hit.empty:
                continue
            i0 = hit.index[0]
            side = 1 if hit.iloc[0]["close"] > rh else -1
            pos = g.index.get_loc(i0)
            if pos + H * 4 >= len(g):
                continue
            fwd = (g["close"].iloc[pos + H * 4] - g["close"].iloc[pos]) / g["atr"].iloc[pos]
            res.append(side * fwd)
        m, t, n = tstat(np.array(res))
        out.append({"horizon_h": H, "n": n, "suite_moyenne_ATR": round(m, 3), "t": round(t, 2)})
    return out


def sweep_reversal(d: pd.DataFrame) -> list[dict]:
    """Balayage du plus haut / bas de la veille puis clôture de retour : retournement ensuite ?"""
    daily = d.groupby("td").agg(h=("high", "max"), l=("low", "min"))
    prev = daily.shift(1).rename(columns={"h": "h_veille", "l": "l_veille"})
    x = d.join(prev, on="td")
    a, b = M("03:00"), M("12:00")
    inwin = (x["msess"] >= a) & (x["msess"] < b)
    up_sweep = inwin & (x["high"] > x["h_veille"] + 0.1 * x["atr"]) & (x["close"] < x["h_veille"])
    dn_sweep = inwin & (x["low"] < x["l_veille"] - 0.1 * x["atr"]) & (x["close"] > x["l_veille"])
    out = []
    for H in (1, 2, 4):
        k = H * 4
        fwd = (x["close"].shift(-k) - x["close"]) / x["atr"]
        same = x["td"].shift(-k) == x["td"]
        r = np.concatenate([(-fwd[up_sweep & same]).to_numpy(), (fwd[dn_sweep & same]).to_numpy()])
        m, t, n = tstat(r)
        out.append({"horizon_h": H, "n": n, "retournement_moyen_ATR": round(m, 3), "t": round(t, 2)})
    return out


def session_mean_reversion(d: pd.DataFrame) -> list[dict]:
    """Écart extrême à la moyenne de séance (prix typique moyen depuis 18:00) : retour vers la moyenne ?"""
    tp = (d["high"] + d["low"] + d["close"]) / 3
    smean = tp.groupby(d["td"]).cumsum() / tp.groupby(d["td"]).cumcount().add(1)
    z = (d["close"] - smean) / d["atr"]
    a, b = M("03:00"), M("14:00")
    inwin = (d["msess"] >= a) & (d["msess"] < b)
    out = []
    for k_z in (2, 3, 4, 5):
        for H in (1, 2):
            k = H * 4
            fwd = (d["close"].shift(-k) - d["close"]) / d["atr"]
            same = d["td"].shift(-k) == d["td"]
            sel_hi = inwin & (z > k_z) & same
            sel_lo = inwin & (z < -k_z) & same
            r = np.concatenate([(-fwd[sel_hi]).to_numpy(), fwd[sel_lo].to_numpy()])
            m, t, n = tstat(r)
            out.append({"ecart_min_ATR": k_z, "horizon_h": H, "n": n, "retour_moyen_ATR": round(m, 3), "t": round(t, 2)})
    return out


def regime_conditioning(d: pd.DataFrame) -> list[dict]:
    """La suite des cassures (4 h, fenêtre NY 08:00-11:00, horizon 2 h) dépend-elle du régime ?

    Régimes mesurés avec l'information de la VEILLE : volatilité relative (ATR journalier / prix, terciles)
    et tendance (efficiency ratio journalier sur 10 jours, terciles).
    """
    daily = d.groupby("td").agg(h=("high", "max"), l=("low", "min"), c=("close", "last"))
    vol = ((daily["h"] - daily["l"]) / daily["c"]).rolling(20).mean().shift(1)
    er = ((daily["c"] - daily["c"].shift(10)).abs() / daily["c"].diff().abs().rolling(10).sum()).shift(1)
    x = d.join(vol.rename("vol"), on="td").join(er.rename("er"), on="td")
    c, h, l = x["close"], x["high"], x["low"]
    hh, ll = h.shift(1).rolling(16).max(), l.shift(1).rolling(16).min()
    sig = pd.Series(np.where(c > hh, 1.0, np.where(c < ll, -1.0, np.nan)), index=x.index)
    a, b = M("08:00"), M("11:00")
    fwd = (c.shift(-8) - c) / x["atr"]
    same = x["td"].shift(-8) == x["td"]
    base = (x["msess"] >= a) & (x["msess"] < b) & sig.notna() & same
    out = []
    for var, label in (("vol", "volatilité de la veille"), ("er", "tendance journalière (ER 10 j)")):
        q = x.loc[base, var].quantile([1 / 3, 2 / 3]).to_numpy()
        for name, sel in (("bas", x[var] <= q[0]), ("moyen", (x[var] > q[0]) & (x[var] <= q[1])), ("haut", x[var] > q[1])):
            r = (sig * fwd)[base & sel].to_numpy()
            m, t, n = tstat(r)
            out.append({"variable": label, "tercile": name, "n": n, "suite_moyenne_ATR": round(m, 3), "t": round(t, 2),
                        "cout_moyen_ATR": round(float(x.loc[base & sel, "cost_atr"].mean()), 3)})
    return out


def vol_profile(d: pd.DataFrame) -> list[dict]:
    rel = (d["high"] - d["low"]) / d["atr"]
    g = rel.groupby(d["nymin"]).mean()
    return [{"heure_new_york": f"{m // 60:02d}:{m % 60:02d}", "amplitude_relative": round(float(v), 3)} for m, v in g.items()]


def main() -> int:
    d = prepare()
    res = {
        "periode": f"{d.index.min()} → {d.index.max()} (entraînement uniquement)",
        "cout_median_aller_retour_ATR": round(float(d["cost_atr"].median()), 3),
        "profil_volatilite": vol_profile(d),
        "predictibilite_segments": segment_predictability(d),
        "autocorrelation_barres": bar_autocorrelation(d),
        "suite_des_cassures": breakout_follow_through(d),
        "range_ouverture_ny": opening_range(d),
        "balayage_veille": sweep_reversal(d),
        "retour_moyenne_seance": session_mean_reversion(d),
        "conditionnement_regime": regime_conditioning(d),
    }
    (OUT / "etude.json").write_text(json.dumps(res, indent=2, ensure_ascii=False))

    def table(rows, cols):
        L = ["| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
        for r in rows:
            L.append("| " + " | ".join(str(r[c]) for c in cols) + " |")
        return L

    L = ["# Étude exploratoire (entraînement 2011-05 → 2018-12)", "", f"Coût aller-retour médian ≈ {res['cout_median_aller_retour_ATR']} ATR de 15 min.", ""]
    L += ["## Prédictibilité d'un segment de séance par le précédent", ""] + table(res["predictibilite_segments"], ["segment_A", "segment_B", "jours", "correlation", "t_correlation", "suivre_signe_A_moyenne_ATR", "t"])
    L += ["", "## Autocorrélation des rendements consécutifs", ""] + table(res["autocorrelation_barres"], ["unite", "seance", "n", "autocorrelation", "t"])
    L += ["", "## Suite des cassures (brut, en ATR)", ""] + table(res["suite_des_cassures"], ["cassure_N_heures", "fenetre", "horizon_h", "n", "suite_moyenne_ATR", "t", "cout_moyen_ATR"])
    L += ["", "## Range d'ouverture New York 08:30-09:30", ""] + table(res["range_ouverture_ny"], ["horizon_h", "n", "suite_moyenne_ATR", "t"])
    L += ["", "## Balayage du plus haut/bas de la veille", ""] + table(res["balayage_veille"], ["horizon_h", "n", "retournement_moyen_ATR", "t"])
    L += ["", "## Retour à la moyenne de séance", ""] + table(res["retour_moyenne_seance"], ["ecart_min_ATR", "horizon_h", "n", "retour_moyen_ATR", "t"])
    L += ["", "## Suite des cassures selon le régime (NY 08:00-11:00, cassure 4 h, horizon 2 h)", ""] + table(res["conditionnement_regime"], ["variable", "tercile", "n", "suite_moyenne_ATR", "t", "cout_moyen_ATR"])
    (OUT / "etude.md").write_text("\n".join(L))
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    sys.exit(main())
