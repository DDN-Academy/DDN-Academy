"""Suite pré-enregistrée (protocole section 10) :
1. évaluation EXPLORATOIRE du candidat de simulation sur 2022-01-01 → 2025-10-28 (non confirmatoire) ;
2. contrôle de résolution : février → octobre 2025, exécution sur barres de 5 minutes ;
3. Monte-Carlo FundedNext Flex 50K (challenge + compte financé) sur les trades hors échantillon du
   walk-forward S1 2014-2021 → profil de risque par défaut et seuils de suspension ;
4. écriture de research/output/final/production.json (lu par le moteur et le site).
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from goldpilot.research.backtest import run  # noqa: E402
from goldpilot.research.data import load_15m, load_5m  # noqa: E402
from goldpilot.research.execution import BASE_COSTS, FIXED_COSTS  # noqa: E402
from goldpilot.research.metrics import by_group, session_of, summary  # noqa: E402
from goldpilot.research.montecarlo import drawdown_distribution, simulate  # noqa: E402
from goldpilot.risk.rules import get_program  # noqa: E402
from goldpilot.risk.sizing import RiskSettings  # noqa: E402
from goldpilot.strategy.candidates import S1SessionExtension  # noqa: E402
from goldpilot.strategy.indicators import time_columns  # noqa: E402

SEL = ROOT / "research" / "output" / "selection"
OUT = ROOT / "research" / "output" / "final"
OUT.mkdir(parents=True, exist_ok=True)
HOLD = pd.Timestamp("2022-01-01", tz="UTC")
CANDIDATE = dict(k=5.0, s=2.5, t=3.0, F=True)
RISK_GRID = [75, 100, 125, 150, 200, 250]
PRICE_REF = 4000.0


def wf_trades() -> pd.DataFrame:
    sel = json.loads((SEL / "selection.json").read_text())
    base = pd.read_parquet(SEL / "trades_base.parquet")
    parts = []
    for p in sel["familles"]["S1"]["walk_forward"]["choix"]:
        y = p["annee"]
        t = base[(base["config_id"] == p["config"]) & (base["year"] == y)]
        parts.append(t)
    return pd.concat(parts, ignore_index=True)


def days_between(df: pd.DataFrame, a: str, b: str) -> np.ndarray:
    d = df[(df.index >= pd.Timestamp(a, tz="UTC")) & (df.index < pd.Timestamp(b, tz="UTC"))]
    return np.unique(time_columns(d.index)["td"].to_numpy())


def settings_for(risk: float) -> RiskSettings:
    return RiskSettings(risk_per_trade_usd=float(risk), daily_loss_stop_usd=float(2 * risk))


def main() -> int:
    df = load_15m()
    cand = S1SessionExtension(**CANDIDATE)
    F = cand.prepare(df)
    res: dict = {"candidat": cand.config_id, "statut": "exploratoire — non confirmatoire"}

    # 1. Évaluation exploratoire 2022-2025
    for name, cm in (("base", BASE_COSTS), ("couts_x2", BASE_COSTS.scaled(2.0)), ("couts_fixes", FIXED_COSTS)):
        t = run(cand, F, cm)
        t.to_parquet(OUT / f"candidat_trades_{name}.parquet")
        h = t[t["entry_time"] >= HOLD]
        res[f"exploratoire_{name}"] = summary(h, ci=(name == "base"))
        if name == "base":
            res["exploratoire_par_annee"] = by_group(h, h["year"]).reset_index().to_dict(orient="records")
            res["exploratoire_par_seance"] = by_group(h, session_of(h)).reset_index().to_dict(orient="records")
            res["exploratoire_par_sens"] = by_group(h, h["side"].map({1: "achat", -1: "vente"})).reset_index().to_dict(orient="records")
            hold_trades = h
    # 2. Contrôle de résolution 5 minutes
    five = load_5m()
    start = five.index.min()
    a = run(cand, F, BASE_COSTS, start=start)
    b = run(cand, F, BASE_COSTS, start=start, exec_bars=five)
    res["controle_resolution_2025"] = {"periode": f"{start} → {five.index.max()}", "barres_15min": summary(a, ci=False),
                                       "execution_5min": summary(b, ci=False)}

    # 3. Monte-Carlo
    wf = wf_trades()
    wf_days = days_between(df, "2014-01-01", "2022-01-01")
    hold_days = days_between(df, "2022-01-01", "2025-10-29")
    mc = {"prix_reference": PRICE_REF, "trades_wf": len(wf), "jours_wf": len(wf_days), "challenge_wf": [], "challenge_2022_2025": [],
          "challenge_wf_prix_4500": []}
    prog_c, prog_f = get_program("flex_50k_challenge"), get_program("flex_50k_funded")
    for risk in RISK_GRID:
        st = settings_for(risk)
        mc["challenge_wf"].append(simulate(wf, wf_days, prog_c, st, PRICE_REF, n_paths=10_000, horizon=120, seed=11).to_dict())
        mc["challenge_2022_2025"].append(simulate(hold_trades, hold_days, prog_c, st, PRICE_REF, n_paths=10_000, horizon=120, seed=12).to_dict())
        mc["challenge_wf_prix_4500"].append(simulate(wf, wf_days, prog_c, st, 4500.0, n_paths=5_000, horizon=120, seed=13).to_dict())
        print("MC risque", risk, flush=True)
    eligible = [m for m in mc["challenge_wf"] if m["p_violation"] <= 0.20]
    chosen = max(eligible, key=lambda m: (m["p_reussite"], -m["risk_per_trade_usd"])) if eligible else min(mc["challenge_wf"], key=lambda m: m["risk_per_trade_usd"])
    risk_default = chosen["risk_per_trade_usd"]
    mc["profil_retenu"] = {"risque_par_trade_usd": risk_default, "regle": "P(réussite) maximale sous P(violation) ≤ 20 % (trades walk-forward)",
                           "contrainte_respectee": bool(eligible)}
    mc["finance_wf"] = simulate(wf, wf_days, prog_f, settings_for(risk_default), PRICE_REF, n_paths=5_000, horizon=252, seed=14).to_dict()
    r = wf["r"].to_numpy()
    mc["suspension"] = drawdown_distribution(r, 100)
    (OUT / "montecarlo.json").write_text(json.dumps(mc, indent=2, ensure_ascii=False))

    # 4. Configuration de production
    wins, losses = r[r > 0], r[r <= 0]
    s_wf = summary(wf)
    prod = {
        "strategy": "S1", "params": {k: str(v) for k, v in CANDIDATE.items()},
        "version": "S1-extension-seance-k5-s2.5-t3-F (2026-10-09)",
        "validated": False,
        "verdict": ("NON VALIDÉE. Sur 2011-2021, aucune famille n'a satisfait les critères pré-enregistrés : espérance "
                    f"walk-forward S1 {s_wf['esperance_R']:+.3f} R par trade (IC95 {s_wf['ic95_bas']:+.3f} ; {s_wf['ic95_haut']:+.3f}), "
                    "non distinguable de zéro après correction des tests multiples, et négative si les coûts doublent. "
                    "Le système fonctionne en SIMULATION uniquement ; le passage au réel exige une validation prospective."),
        "rapport_gain_perte_historique": float(wins.mean() / abs(losses.mean())) if len(losses) else None,
        "trades_par_mois_attendus": s_wf["trades_par_mois"],
        "risk_settings_default": settings_for(risk_default).to_dict(),
        "seuils_suspension": {"drawdown_R": round(mc["suspension"]["dd_p01"], 2), "serie_pertes": int(np.ceil(mc["suspension"]["serie_pertes_p99"]))},
        "historique_journalier_requis": 250,
        "references": {"selection": "research/output/selection/selection.md", "final": "research/output/final/final.md",
                       "protocole": "docs/03_protocole_de_recherche.md"},
    }
    (OUT / "production.json").write_text(json.dumps(prod, indent=2, ensure_ascii=False))
    res["walk_forward_S1"] = s_wf
    (OUT / "final.json").write_text(json.dumps(res, indent=2, ensure_ascii=False, default=str))

    def f(x, nd=3):
        return "—" if x is None or (isinstance(x, float) and not np.isfinite(x)) else (f"{x:+.{nd}f}" if isinstance(x, float) else str(x))

    e = res["exploratoire_base"]
    L = ["# Évaluation finale (exploratoire) et Monte-Carlo", "", f"Candidat de simulation : `{cand.config_id}` — **{prod['verdict']}**", "",
         "## 2022-01-01 → 2025-10-28 (exploratoire, non confirmatoire)", "",
         "| Coûts | n | espérance R | PF | taux de gain | drawdown max R |", "|---|---|---|---|---|---|"]
    for k in ("base", "couts_x2", "couts_fixes"):
        x = res[f"exploratoire_{k}"]
        L.append(f"| {k} | {x.get('n')} | {f(x.get('esperance_R'))} | {f(x.get('profit_factor'), 2)} | {f(x.get('taux_de_gain'), 2)} | {f(x.get('drawdown_max_R'), 1)} |")
    L += ["", f"IC95 de l'espérance (base) : [{f(e.get('ic95_bas'))} ; {f(e.get('ic95_haut'))}] ; borne unilatérale basse {f(e.get('ic_unilateral95_bas'))}", "",
          "Par année :", ""] + [f"- {int(r_['year'])} : n={int(r_['n'])}, espérance {r_['esperance_R']:+.3f} R" for r_ in res["exploratoire_par_annee"]]
    rc = res["controle_resolution_2025"]
    L += ["", f"Contrôle de résolution ({rc['periode']}) : barres 15 min n={rc['barres_15min'].get('n')}, espérance {f(rc['barres_15min'].get('esperance_R'))} R ; "
          f"exécution 5 min n={rc['execution_5min'].get('n')}, espérance {f(rc['execution_5min'].get('esperance_R'))} R", "",
          "## Monte-Carlo Flex 50K (challenge, 120 jours, trades walk-forward 2014-2021, or à 4 000 $)", "",
          "| Risque/trade | P(réussite) | P(violation) | P(en cours) | jours médians | objectif relevé | trades moyens |", "|---|---|---|---|---|---|---|"]
    for m in mc["challenge_wf"]:
        L.append(f"| {m['risk_per_trade_usd']:.0f} $ | {m['p_reussite']:.1%} | {m['p_violation']:.1%} | {m['p_en_cours']:.1%} | {m['jours_median_reussite']} | {m['p_objectif_releve']:.1%} | {m['trades_moyens']:.0f} |")
    L += ["", "Même chose avec les trades 2022-2025 (exploratoire) :", "", "| Risque/trade | P(réussite) | P(violation) |", "|---|---|---|"]
    for m in mc["challenge_2022_2025"]:
        L.append(f"| {m['risk_per_trade_usd']:.0f} $ | {m['p_reussite']:.1%} | {m['p_violation']:.1%} |")
    fm = mc["finance_wf"]
    L += ["", f"Profil retenu : **{risk_default:.0f} $ par trade** ({mc['profil_retenu']['regle']}).",
          f"Compte financé (252 jours) : survie {fm['survie']}, probabilité d'au moins un retrait {fm['retraits'].get('p_au_moins_un', 0):.1%}, "
          f"retraits moyens {fm['retraits'].get('moyenne_payee', 0):.0f} $.",
          f"Seuils de suspension automatique : drawdown ≤ {prod['seuils_suspension']['drawdown_R']} R ou série de {prod['seuils_suspension']['serie_pertes']} pertes."]
    (OUT / "final.md").write_text("\n".join(L))
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    sys.exit(main())
