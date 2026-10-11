"""Compléments A POSTERIORI (non pré-enregistrés, ne changent pas le verdict « NON VALIDÉE »).

Ajoutés après la revue de conformité au cahier des charges ; ils n'alimentent ni la sélection, ni la
configuration de production (`production.json` n'est ni lu pour décider ni réécrit ici).

A. Métriques du § 4 pour le candidat S1 (walk-forward 2014-2021 et exploratoire 2022-2025) : durée des
   drawdowns en jours de trading, résultats par séance et par régime de volatilité (terciles causaux),
   espérance en dollars au risque par défaut.
B. Test de sensibilité au délai d'exécution manuelle : entrée 0, 1, 3, 5 minutes après la décision,
   exécution sur barres de 5 minutes (février → octobre 2025).
C. Combinaisons d'unités de temps (§ 5 du cahier des charges), contrôle de robustesse sur 2011-2021
   UNIQUEMENT : décision 15 min + filtre journalier (référence), sans filtre journalier, avec filtre de
   tendance 1 h en plus, décision sur 30 min.
Sorties : research/output/complements/
"""
from __future__ import annotations

import json
import sys
from contextlib import contextmanager
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "backend"))

from goldpilot.research.backtest import trades_frame  # noqa: E402
from goldpilot.research.data import load_15m, load_5m, resample  # noqa: E402
from goldpilot.research.execution import BASE_COSTS, ExecutionSimulator  # noqa: E402
from goldpilot.research.metrics import (by_group, drawdown_durations, in_dollars, session_of, summary,  # noqa: E402
                                        volatility_tercile_by_day)
from goldpilot.strategy import candidates  # noqa: E402
from goldpilot.strategy.base import Evaluation, StrategyState  # noqa: E402
from goldpilot.strategy.candidates import S1SessionExtension  # noqa: E402
from goldpilot.strategy.indicators import time_columns  # noqa: E402

SEL = ROOT / "research" / "output" / "selection"
FIN = ROOT / "research" / "output" / "final"
OUT = ROOT / "research" / "output" / "complements"
LABEL = "complément a posteriori (non pré-enregistré, ne change pas le verdict)"
CANDIDATE = dict(k=5.0, s=2.5, t=3.0, F=True)
NS_MIN = 60 * 1_000_000_000
HOLD = pd.Timestamp("2022-01-01", tz="UTC")
TRAIN_END = pd.Timestamp("2019-01-01", tz="UTC")
DELAYS_MIN = (0, 1, 3, 5)


# ------------------------------------------------------------------ outils
def run_with(strategy, F: pd.DataFrame, sim: ExecutionSimulator, start=None, end=None, exec_bars: pd.DataFrame | None = None,
             bar_ns: int = 15 * NS_MIN) -> pd.DataFrame:
    """Même boucle que `goldpilot.research.backtest.run`, avec un simulateur fourni et une durée de barre de
    décision paramétrable (vérifié identique à `run` par backend/tests/test_research_complements.py)."""
    idx = F.index.asi8
    i0 = max(int(np.searchsorted(idx, pd.Timestamp(start).value)) if start is not None else 0, strategy.warmup_bars)
    i1 = int(np.searchsorted(idx, pd.Timestamp(end).value)) if end is not None else len(F)
    o, h, l, c = (F[k].to_numpy() for k in ("open", "high", "low", "close"))
    a, td, ms = F["atr"].to_numpy(), F["td"].to_numpy(), F["msess"].to_numpy()
    if exec_bars is not None:
        ex_idx = exec_bars.index.as_unit("ns")
        ets, etc = ex_idx.asi8, time_columns(ex_idx)
        eo, eh, el, ec = (exec_bars[k].to_numpy(dtype=float) for k in ("open", "high", "low", "close"))
        etd, ems = etc["td"].to_numpy(), etc["msess"].to_numpy()
    for i in range(i0, i1):
        atr_known = a[i - 1] if i > 0 else a[i]
        if exec_bars is None:
            sim.on_bar(int(idx[i]), o[i], h[i], l[i], c[i], atr_known, int(td[i]), int(ms[i]))
        else:
            j0, j1 = np.searchsorted(ets, idx[i]), np.searchsorted(ets, idx[i] + bar_ns)
            for j in range(j0, j1):
                sim.on_bar(int(ets[j]), eo[j], eh[j], el[j], ec[j], atr_known, int(etd[j]), int(ems[j]))
        sim.end_of_decision_bar(h[i], l[i], a[i])
        d = int(td[i])
        st = StrategyState(has_position=sim.position is not None,
                           pending_tags={s.tag for s in sim.pending if s.valid_until_ts > idx[i] + bar_ns},
                           tags_today=sim.tags_by_td.get(d, set()), trades_today=sim.entries_by_td.get(d, 0))
        for s in strategy.evaluate(i, F, st).setups:
            sim.submit(s)
    return trades_frame(sim.trades)


def trend_1h(bars15: pd.DataFrame, span: int = 20) -> pd.Series:
    """+1 / −1 / 0 pour chaque barre de 15 min : clôture de la DERNIÈRE barre 1 h TERMINÉE au moment de la
    clôture de la barre de 15 min, au-dessus (+1) ou en dessous (−1) de sa moyenne exponentielle 20 périodes 1 h."""
    h1 = resample(bars15, 60)
    ema = h1["close"].ewm(span=span, adjust=False, min_periods=span).mean()
    sign = np.sign(h1["close"] - ema).where(ema.notna(), 0.0)
    avail = pd.DataFrame({"t": h1.index + pd.Timedelta(minutes=60), "trend": sign.to_numpy()})
    close_t = pd.DataFrame({"t": bars15.index + pd.Timedelta(minutes=15)})
    m = pd.merge_asof(close_t, avail, on="t", direction="backward")
    return pd.Series(m["trend"].fillna(0.0).to_numpy(), index=bars15.index)


class S1Trend1h(S1SessionExtension):
    """Variante de robustesse : S1 + filtre de contexte 1 h (achat seulement si tendance 1 h haussière, vente
    seulement si baissière). Jamais utilisée en production."""

    def prepare(self, bars: pd.DataFrame, daily_history=None) -> pd.DataFrame:
        F = super().prepare(bars, daily_history)
        F["trend1h"] = trend_1h(bars).to_numpy()
        return F

    def evaluate(self, i: int, F: pd.DataFrame, st: StrategyState) -> Evaluation:
        ev = super().evaluate(i, F, st)
        if ev.setups:
            tr = candidates.arrays(F)["trend1h"][i]
            if tr != ev.setups[0].side:
                return Evaluation(ev.bar_ts, ev.regime, ev.context, [], ["contexte 1 h contraire (variante de robustesse)"])
        return ev


@contextmanager
def decision_minutes(m: int):
    """La stratégie lit la durée de barre dans `candidates.BAR_MIN` (15) : réglée temporairement pour la variante 30 min."""
    old = candidates.BAR_MIN
    candidates.BAR_MIN = m
    try:
        yield
    finally:
        candidates.BAR_MIN = old


def wf_trades() -> pd.DataFrame:
    sel = json.loads((SEL / "selection.json").read_text())
    base = pd.read_parquet(SEL / "trades_base.parquet")
    return pd.concat([base[(base["config_id"] == p["config"]) & (base["year"] == p["annee"])]
                      for p in sel["familles"]["S1"]["walk_forward"]["choix"]], ignore_index=True)


def days_between(df: pd.DataFrame, a: str, b: str) -> np.ndarray:
    d = df[(df.index >= pd.Timestamp(a, tz="UTC")) & (df.index < pd.Timestamp(b, tz="UTC"))]
    return np.unique(time_columns(d.index)["td"].to_numpy())


def groups(t: pd.DataFrame, key: pd.Series, risk: float) -> list[dict]:
    g = by_group(t, key)
    g["esperance_usd"] = (g["esperance_R"] * risk).round(2)
    return g.reset_index(names="groupe").to_dict(orient="records")


def short(s: dict) -> dict:
    keys = ("n", "esperance_R", "ic95_bas", "ic95_haut", "profit_factor", "taux_de_gain", "drawdown_max_R", "ecart_type_R",
            "serie_pertes_max", "glissement_entree_moyen_oz")
    return {k: s.get(k) for k in keys if k in s}


# ------------------------------------------------------------------ sections
def section_metrics(df: pd.DataFrame, risk: float) -> dict:
    regime_by_td = volatility_tercile_by_day(df, time_columns(df.index)["td"].to_numpy())
    hold = pd.read_parquet(FIN / "candidat_trades_base.parquet")
    hold = hold[hold["entry_time"] >= HOLD]
    out = {}
    for name, t, a, b in (("walk_forward_2014_2021", wf_trades(), "2014-01-01", "2022-01-01"),
                          ("exploratoire_2022_2025", hold, "2022-01-01", "2025-10-29")):
        s = summary(t)
        reg = t["td"].map(regime_by_td).fillna("indéterminé (historique < 125 j)")
        out[name] = {"resume": short(s), "en_dollars": in_dollars(s, risk),
                     "durees_drawdown": drawdown_durations(t, days_between(df, a, b)),
                     "par_seance": groups(t, session_of(t), risk), "par_regime_volatilite": groups(t, reg, risk)}
    out["definition_regime"] = ("tercile de la moyenne sur 20 journées de l'amplitude relative (H−L)/C, connue la veille, "
                                "parmi les 250 journées précédentes (calcul causal)")
    return out


def section_delay(df: pd.DataFrame) -> dict:
    five = load_5m()
    start = five.index.min()
    cand = S1SessionExtension(**CANDIDATE)
    F = cand.prepare(df)
    rows = []
    for d in DELAYS_MIN:
        modes = ["exact"] if d % 5 == 0 else ["interpole", "pire"]
        for mode in modes:
            sim = (ExecutionSimulator(BASE_COSTS) if d == 0 else
                   ExecutionSimulator(BASE_COSTS, entry_delay_ns=d * NS_MIN, exec_bar_ns=5 * NS_MIN,
                                      delay_price="interpole" if mode == "exact" else mode))
            t = run_with(cand, F, sim, start=start, exec_bars=five)
            rows.append({"delai_min": d, "prix_entree": mode, **short(summary(t))})
            print("délai", d, mode, rows[-1]["n"], rows[-1].get("esperance_R"), flush=True)
    return {"periode": f"{start} → {five.index.max()}", "resultats": rows,
            "note": ("1 et 3 min tombent à l'intérieur d'une barre de 5 min : prix d'entrée inconnu, encadré par une estimation "
                     "interpolée (ouverture → clôture) et une borne prudente (extrême défavorable de la barre). "
                     "0 et 5 min : ouverture exacte d'une barre de 5 min.")}


def section_timeframes(df: pd.DataFrame) -> dict:
    d = df[df.index < HOLD]
    assert d.index.max() < HOLD, "garde-fou : aucune donnée postérieure au 31/12/2021"
    variants = [
        ("reference_15min_filtre_journalier", "décision 15 min + filtre de volatilité journalière (configuration de production)",
         S1SessionExtension(**CANDIDATE), d, 15),
        ("15min_sans_filtre_journalier", "décision 15 min, sans contexte journalier",
         S1SessionExtension(**{**CANDIDATE, "F": False}), d, 15),
        ("15min_filtre_journalier_tendance_1h", "décision 15 min + filtre journalier + contexte de tendance 1 h (EMA 20)",
         S1Trend1h(**CANDIDATE), d, 15),
        ("30min_filtre_journalier", "décision 30 min (mêmes paramètres en nombre de barres) + filtre journalier",
         S1SessionExtension(**CANDIDATE), resample(d, 30), 30),
    ]
    out = {}
    for key, desc, strat, bars, m in variants:
        with decision_minutes(m):
            F = strat.prepare(bars)
            t = run_with(strat, F, ExecutionSimulator(BASE_COSTS), bar_ns=m * NS_MIN)
        tr, va = t[t["entry_time"] < TRAIN_END], t[t["entry_time"] >= TRAIN_END]
        out[key] = {"description": desc, "entrainement_2011_2018": short(summary(tr)), "validation_2019_2021": short(summary(va)),
                    "total_2011_2021": short(summary(t))}
        print(key, out[key]["total_2011_2021"], flush=True)
    return out


def fmt(x, nd=3, sign=True):
    if x is None or (isinstance(x, float) and not np.isfinite(x)):
        return "—"
    return f"{x:+.{nd}f}" if sign else f"{x:.{nd}f}"


def markdown(res: dict) -> str:
    L = ["# Compléments de recherche", "", f"> **{LABEL}.** Calculés après coup ; ils ne servent ni à choisir ni à modifier la stratégie.",
         "", f"Candidat : `S1|F=True,k=5.0,s=2.5,t=3.0`, coûts de base. Risque par trade pour les montants : {res['risque_usd']:.0f} $ "
         "(profil par défaut, `production.json`), 1 R = ce risque exactement (arrondi au contrat entier ignoré).", "",
         "## A. Métriques complémentaires (§ 4)", ""]
    A = res["A_metriques"]
    L += ["| Période | n | espérance R | espérance $ | IC95 $ | drawdown max R | durée max DD (j) | durée médiane DD (j) | nb DD | DD en cours à la fin |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    for k in ("walk_forward_2014_2021", "exploratoire_2022_2025"):
        x, u, dd = A[k]["resume"], A[k]["en_dollars"], A[k]["durees_drawdown"]
        L.append(f"| {k} | {x['n']} | {fmt(x['esperance_R'])} | {fmt(u.get('esperance_usd'), 2)} | "
                 f"[{fmt(u.get('ic95_bas_usd'), 2)} ; {fmt(u.get('ic95_haut_usd'), 2)}] | {fmt(x['drawdown_max_R'], 1)} | "
                 f"{dd['duree_max_jours']} | {dd['duree_mediane_jours']:g} | {dd['nb_drawdowns']} | "
                 f"{'oui (' + str(dd['duree_en_cours_jours']) + ' j)' if dd['drawdown_en_cours_fin'] else 'non'} |")
    L += ["", "Durée d'un drawdown = jours de trading passés sous le précédent sommet d'équité (journées sans trade comprises).", ""]
    for k in ("walk_forward_2014_2021", "exploratoire_2022_2025"):
        for g, title in (("par_seance", "par séance (heure d'entrée, New York)"), ("par_regime_volatilite", "par régime de volatilité")):
            L += [f"**{k} — {title}**", "", "| Groupe | n | espérance R | espérance $ | taux de gain |", "|---|---|---|---|---|"]
            L += [f"| {r['groupe']} | {r['n']} | {fmt(r['esperance_R'])} | {fmt(r['esperance_usd'], 2)} | {r['taux_de_gain']:.0%} |" for r in A[k][g]]
            L.append("")
    L += [f"Régime : {A['definition_regime']}.", "", "## B. Délai d'exécution manuelle (§ 3.7)", "",
          f"Période : {res['B_delai']['periode']} ; exécution sur barres de 5 minutes. {res['B_delai']['note']}", "",
          "| Délai | Prix d'entrée | n | espérance R | IC95 R | drawdown max R | glissement d'entrée moyen ($/oz) |", "|---|---|---|---|---|---|---|"]
    for r in res["B_delai"]["resultats"]:
        L.append(f"| {r['delai_min']} min | {r['prix_entree']} | {r['n']} | {fmt(r.get('esperance_R'))} | "
                 f"[{fmt(r.get('ic95_bas'))} ; {fmt(r.get('ic95_haut'))}] | {fmt(r.get('drawdown_max_R'), 1)} | {fmt(r.get('glissement_entree_moyen_oz'), 3)} |")
    L += ["", "## C. Combinaisons d'unités de temps (§ 5) — 2011-2021 uniquement", "",
          "| Variante | entraînement 2011-18 : n / espérance R | validation 2019-21 : n / espérance R / PF | total 2011-21 : espérance R [IC95] |",
          "|---|---|---|---|"]
    for k, v in res["C_unites_de_temps"].items():
        tr, va, to = v["entrainement_2011_2018"], v["validation_2019_2021"], v["total_2011_2021"]
        L.append(f"| {v['description']} | {tr['n']} / {fmt(tr.get('esperance_R'))} | {va['n']} / {fmt(va.get('esperance_R'))} / "
                 f"{fmt(va.get('profit_factor'), 2, False)} | {fmt(to.get('esperance_R'))} [{fmt(to.get('ic95_bas'))} ; {fmt(to.get('ic95_haut'))}] |")
    L += ["", "Aucune variante n'est adoptée : la production reste inchangée (pas de modification silencieuse, § 17)."]
    return "\n".join(L)


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    df = load_15m()
    risk = float(json.loads((FIN / "production.json").read_text())["risk_settings_default"]["risk_per_trade_usd"])
    res = {"statut": LABEL, "genere_utc": pd.Timestamp.now(tz="UTC").isoformat(), "candidat": "S1|F=True,k=5.0,s=2.5,t=3.0",
           "risque_usd": risk}
    res["A_metriques"] = section_metrics(df, risk)
    res["B_delai"] = section_delay(df)
    res["C_unites_de_temps"] = section_timeframes(df)
    (OUT / "complements.json").write_text(json.dumps(res, indent=2, ensure_ascii=False, default=str))
    md = markdown(res)
    (OUT / "complements.md").write_text(md)
    print(md)
    return 0


if __name__ == "__main__":
    sys.exit(main())
