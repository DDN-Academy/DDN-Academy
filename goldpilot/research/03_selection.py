"""Sélection (protocole sections 5) — AUCUNE donnée postérieure au 31/12/2021 n'est chargée.

Pour chaque famille (S1, S2) :
* trades de toutes les configurations (coûts de base, ×2, fixes) sur 2011-05 → 2021 ;
* walk-forward 2014-2021 (re-sélection annuelle par t-stat sur 3 ans) ;
* configuration de production (t-stat max 2011-2021) et critères 1 à 6.
Sorties : research/output/selection/
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from goldpilot.research.backtest import run  # noqa: E402
from goldpilot.research.data import load_15m  # noqa: E402
from goldpilot.research.execution import BASE_COSTS, FIXED_COSTS  # noqa: E402
from goldpilot.research.metrics import daily_series, deflated_sharpe, summary  # noqa: E402
from goldpilot.strategy.candidates import grid  # noqa: E402
from goldpilot.strategy.indicators import time_columns  # noqa: E402

OUT = ROOT / "research" / "output" / "selection"
OUT.mkdir(parents=True, exist_ok=True)
SEL_END = pd.Timestamp("2022-01-01", tz="UTC")
TRAIN_END = pd.Timestamp("2019-01-01", tz="UTC")
N_TRIALS_DSR = 200  # 32 essais de cette session + 168 de la session abandonnée (protocole section 0)


def tstat(r) -> float:
    r = np.asarray(r, dtype=float)
    if len(r) < 30 or r.std(ddof=1) == 0:
        return -math.inf
    return float(r.mean() / r.std(ddof=1) * math.sqrt(len(r)))


def between(t: pd.DataFrame, a=None, b=None) -> pd.DataFrame:
    m = pd.Series(True, index=t.index)
    if a is not None:
        m &= t["entry_time"] >= a
    if b is not None:
        m &= t["entry_time"] < b
    return t[m]


def params_of(cid: str) -> dict:
    return dict(kv.split("=") for kv in cid.split("|")[1].split(","))


def neighbours(cid: str, ids: list[str]) -> list[str]:
    p = params_of(cid)
    vals: dict[str, list[str]] = {}
    for c in ids:
        for k, v in params_of(c).items():
            vals.setdefault(k, [])
            if v not in vals[k]:
                vals[k].append(v)

    def key(v):
        try:
            return (0, float(v.replace(":", ".")))
        except ValueError:
            return (1, v)

    for k in vals:
        vals[k].sort(key=key)
    out = []
    for c in ids:
        q = params_of(c)
        diff = [k for k in p if p[k] != q[k]]
        if len(diff) == 1:
            k = diff[0]
            numeric = all(key(v)[0] == 0 for v in vals[k])
            if not numeric or abs(vals[k].index(p[k]) - vals[k].index(q[k])) == 1:
                out.append(c)
    return out


def main() -> int:
    df = load_15m()
    df = df[df.index < SEL_END]
    assert df.index.max() < SEL_END, "garde-fou : aucune donnée du test final"
    days = np.unique(time_columns(df.index)["td"].to_numpy())
    variants = {"base": BASE_COSTS, "x2": BASE_COSTS.scaled(2.0), "fixe": FIXED_COSTS}
    res = {v: [] for v in variants}
    g = grid()
    for fam, strats in g.items():
        for s in strats:
            F = s.prepare(df)
            for v, cm in variants.items():
                t = run(s, F, cm)
                t["family"] = fam
                res[v].append(t)
            print(s.config_id, flush=True)
    T = {v: pd.concat(x, ignore_index=True) for v, x in res.items()}
    for v, t in T.items():
        t.to_parquet(OUT / f"trades_{v}.parquet")
    base = T["base"]
    first_day = int(base["td"].min())
    days = days[days >= first_day]

    all_ids = [s.config_id for v in g.values() for s in v]
    srs = []
    for cid in all_ids:
        x = daily_series(base[base["config_id"] == cid], days)
        srs.append(x.mean() / x.std(ddof=1) if x.std(ddof=1) > 0 else 0.0)
    srs = np.array(srs)
    # DSR avec N = 200 essais : la dispersion des Sharpe est estimée sur les 32 essais disponibles
    sr_trials_200 = np.resize(srs, N_TRIALS_DSR)

    report = {"genere_utc": pd.Timestamp.now(tz="UTC").isoformat(), "essais_cette_session": len(all_ids),
              "essais_comptes_pour_DSR": N_TRIALS_DSR, "familles": {}}
    for fam, strats in g.items():
        ids = [s.config_id for s in strats]
        ft = base[base["family"] == fam]
        # Walk-forward
        picks, oos = [], []
        for y in range(2014, 2022):
            w0, w1, w2 = (pd.Timestamp(f"{y - 3}-01-01", tz="UTC"), pd.Timestamp(f"{y}-01-01", tz="UTC"),
                          pd.Timestamp(f"{y + 1}-01-01", tz="UTC"))
            sc = between(ft, w0, w1).groupby("config_id")["r"].apply(tstat)
            best = sc.idxmax()
            tt = between(ft[ft["config_id"] == best], w1, w2)
            picks.append({"annee": y, "config": best, "t_fenetre": round(float(sc.max()), 2), "n": int(len(tt)),
                          "esperance_R": round(float(tt["r"].mean()), 3) if len(tt) else None})
            oos.append(tt)
        wf = summary(pd.concat(oos, ignore_index=True))
        # Configuration de production
        sc_all = ft.groupby("config_id")["r"].apply(tstat)
        prod = sc_all.idxmax()
        pt = ft[ft["config_id"] == prod]
        tr, va = summary(between(pt, None, TRAIN_END)), summary(between(pt, TRAIN_END, SEL_END))
        yearly = pt.groupby("year")["r"].agg(["count", "mean", "sum"]).round(4)
        frac_years = float((yearly["mean"] > 0).mean())
        nb = neighbours(prod, ids)
        nb_pos = {c: bool(between(ft[ft["config_id"] == c], None, TRAIN_END)["r"].mean() > 0) for c in nb}
        frac_nb = float(np.mean(list(nb_pos.values()))) if nb_pos else 0.0
        x2v = between(T["x2"][T["x2"]["config_id"] == prod], TRAIN_END, SEL_END)["r"]
        fxa = summary(T["fixe"][T["fixe"]["config_id"] == prod], ci=False)
        ds = daily_series(pt, days)
        sr = ds.mean() / ds.std(ddof=1) if ds.std(ddof=1) > 0 else 0.0
        sk, ku = float(stats.skew(ds)), float(stats.kurtosis(ds, fisher=False))
        dsr200 = deflated_sharpe(sr, sr_trials_200, len(ds), sk, ku)
        dsr32 = deflated_sharpe(sr, srs, len(ds), sk, ku)
        crit = {
            "1_walk_forward_esperance_et_IC_unilateral_bas_>0": bool(wf.get("n", 0) and wf["esperance_R"] > 0 and wf["ic_unilateral95_bas"] > 0),
            "2_validation_esperance_>0_et_PF_>=1.10": bool(va.get("n", 0) and va["esperance_R"] > 0 and va["profit_factor"] >= 1.10),
            "3_couts_x2_validation_>=0": bool(len(x2v) and x2v.mean() >= 0),
            "4_annees_positives_>=60%": bool(frac_years >= 0.60),
            "5_voisins_positifs_>=70%": bool(frac_nb >= 0.70),
            "6_DSR_200_essais_>=0.90": bool(np.isfinite(dsr200) and dsr200 >= 0.90),
        }
        rows = []
        for c in ids:
            q = ft[ft["config_id"] == c]
            a, b = between(q, None, TRAIN_END)["r"], between(q, TRAIN_END, SEL_END)["r"]
            rows.append({"config": c, "n_entr": int(len(a)), "esp_entr": round(float(a.mean()), 4) if len(a) else None,
                         "n_val": int(len(b)), "esp_val": round(float(b.mean()), 4) if len(b) else None,
                         "t_2011_2021": round(float(sc_all.get(c, math.nan)), 2)})
        report["familles"][fam] = {
            "walk_forward": {"choix": picks, "resume": wf}, "production": prod, "entrainement": tr, "validation": va,
            "validation_couts_x2_esperance_R": float(x2v.mean()) if len(x2v) else None,
            "couts_fixes_2011_2021": fxa, "par_annee": yearly.reset_index().to_dict(orient="records"),
            "fraction_annees_positives": frac_years, "voisins": nb_pos, "fraction_voisins_positifs": frac_nb,
            "sharpe_journalier": float(sr), "DSR_200": dsr200, "DSR_32": dsr32, "criteres": crit,
            "eligible": bool(all(crit.values())), "toutes_configurations": rows,
        }
    (OUT / "selection.json").write_text(json.dumps(report, indent=2, ensure_ascii=False, default=str))
    L = ["# Sélection (données ≤ 31/12/2021)", ""]
    for fam, r in report["familles"].items():
        w, v = r["walk_forward"]["resume"], r["validation"]
        L += [f"## {fam} — production : `{r['production']}` — **{'ÉLIGIBLE' if r['eligible'] else 'NON ÉLIGIBLE'}**", "",
              f"- Walk-forward 2014-2021 : n={w.get('n')}, espérance={w.get('esperance_R', float('nan')):.3f} R, IC95 [{w.get('ic95_bas', float('nan')):.3f} ; {w.get('ic95_haut', float('nan')):.3f}], unilatéral bas {w.get('ic_unilateral95_bas', float('nan')):.3f}, PF={w.get('profit_factor', float('nan')):.2f}",
              f"- Entraînement : n={r['entrainement'].get('n')}, espérance={r['entrainement'].get('esperance_R', float('nan')):.3f} R ; validation : n={v.get('n')}, espérance={v.get('esperance_R', float('nan')):.3f} R, PF={v.get('profit_factor', float('nan')):.2f}",
              f"- Validation coûts ×2 : {r['validation_couts_x2_esperance_R']:.3f} R ; coûts fixes 2011-2021 : {r['couts_fixes_2011_2021'].get('esperance_R', float('nan')):.3f} R",
              f"- Années positives : {r['fraction_annees_positives']:.0%} ; voisins positifs : {r['fraction_voisins_positifs']:.0%} ; DSR(200)={r['DSR_200']:.3f} ; DSR(32)={r['DSR_32']:.3f}", ""]
        L += [f"- {k} : {'✔' if ok else '✘'}" for k, ok in r["criteres"].items()] + [""]
        L += ["| Configuration | n entr. | esp. entr. | n val. | esp. val. | t 2011-21 |", "|---|---|---|---|---|---|"]
        for row in sorted(r["toutes_configurations"], key=lambda z: -z["t_2011_2021"] if np.isfinite(z["t_2011_2021"]) else 99):
            L.append(f"| `{row['config']}` | {row['n_entr']} | {row['esp_entr']} | {row['n_val']} | {row['esp_val']} | {row['t_2011_2021']} |")
        L += ["", "| Année WF | Config. choisie | t fenêtre | n | esp. |", "|---|---|---|---|---|"]
        for p in r["walk_forward"]["choix"]:
            L.append(f"| {p['annee']} | `{p['config']}` | {p['t_fenetre']} | {p['n']} | {p['esperance_R']} |")
        L.append("")
    (OUT / "selection.md").write_text("\n".join(L))
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    sys.exit(main())
