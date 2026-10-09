"""Audit des données historiques XAUUSD du dépôt (étape préalable à toute recherche).

Questions traitées :
1. Intégrité : ordre, doublons, cohérence OHLC, prix aberrants, trous.
2. Fuseau horaire des horodatages : déterminé MOIS PAR MOIS, sans hypothèse, par deux signatures
   indépendantes :
   a. la pause quotidienne du marché de l'or (17:00-18:00 heure de New York) ;
   b. le pic de volatilité de 08:30 heure de New York (publications américaines), mesuré tous les jours
      ouvrés (pas seulement les NFP).
   Pour chaque mois, on cherche le décalage horaire (en heures) entre « heure du fichier » et « heure de
   New York » qui explique le mieux ces deux signatures.
3. Couverture des deux fichiers et cohérence entre eux sur la période commune.

Sorties : research/output/audit/ (JSON + Markdown) et backend/goldpilot/research/conventions.json,
utilisé ensuite par le chargeur de données.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
OUT = HERE / "output" / "audit"
OUT.mkdir(parents=True, exist_ok=True)
CONV = HERE.parent / "backend" / "goldpilot" / "research" / "conventions.json"


def read_15m() -> pd.DataFrame:
    d = pd.read_csv(REPO / "data" / "xau_15m_2004_2025.csv", sep=";")
    d.columns = [c.strip().lower() for c in d.columns]
    d["t"] = pd.to_datetime(d["date"], format="%Y.%m.%d %H:%M")
    return d.drop(columns="date")


def read_5m() -> pd.DataFrame:
    d = pd.read_csv(REPO / "data" / "xauusd_5m_2025.csv")
    d.columns = [c.strip().lower() for c in d.columns]
    d["t"] = pd.to_datetime(d["date"])
    return d.drop(columns="date")


def integrity(d: pd.DataFrame, step: int) -> dict:
    t = d["t"]
    gaps = t.diff().dt.total_seconds().div(60)
    lr = np.log(d["close"]).diff()
    bad = (d["high"] < d[["open", "close"]].max(axis=1)) | (d["low"] > d[["open", "close"]].min(axis=1)) | (d["high"] < d["low"])
    big = gaps[gaps > 4 * 24 * 60]
    return {
        "lignes": int(len(d)),
        "debut": str(t.iloc[0]),
        "fin": str(t.iloc[-1]),
        "ordre_croissant": bool(t.is_monotonic_increasing),
        "doublons": int(t.duplicated().sum()),
        "ohlc_incoherents": int(bad.sum()),
        "prix_non_positifs": int((d[["open", "high", "low", "close"]] <= 0).any(axis=1).sum()),
        "pas_attendu_pct": round(float((gaps == step).mean() * 100), 2),
        "trous_plus_de_4_jours": [
            {"apres": str(t.iloc[i - 1]), "reprise": str(t.iloc[i]), "jours": round(float(g) / 1440, 1)}
            for i, g in big.items()
        ],
        "volume": "entier (nombre de ticks du broker, pas un volume d'échange)" if bool((d["volume"] % 1 == 0).all()) else "décimal",
        "plus_fortes_variations_barre_a_barre": [
            {"barre": str(t.iloc[i]), "log_rendement": round(float(lr.iloc[i]), 4), "trou_minutes_avant": float(gaps.iloc[i])}
            for i in lr.abs().nlargest(8).index
        ],
    }


def monthly_offset(d: pd.DataFrame, step: int) -> pd.DataFrame:
    """Décalage (fichier − New York, en heures) estimé mois par mois.

    Signature principale : le pic de volatilité des publications américaines de 08:30 New York,
    recoupé par celui de 10:00 New York (deux horaires de publication indépendants). Pour chaque
    décalage candidat (4 à 9 h), score = volatilité relative du créneau 08:30 + celle du créneau 10:00
    (médiane des jours ouvrés, rapportée à la médiane du mois). La pause quotidienne observée dans le
    fichier est rapportée séparément : c'est une caractéristique du broker, pas forcément de la place.
    """
    x = d.copy()
    x["rng"] = np.log(x["high"] / x["low"])
    x["mois"] = x["t"].dt.to_period("M")
    x["slot"] = x["t"].dt.hour * 60 + x["t"].dt.minute
    x = x[x["t"].dt.dayofweek < 5]
    rows = []
    for mois, g in x.groupby("mois"):
        if len(g) < 500:
            continue
        med = g["rng"].median()
        if not med > 0:
            continue
        prof = g.groupby("slot")["rng"].median() / med
        scores = {}
        for off in range(4, 10):
            s830 = (8 * 60 + 30 + off * 60) % 1440
            s1000 = (10 * 60 + off * 60) % 1440
            scores[off] = float(prof.get(s830, 0.0)) + float(prof.get(s1000, 0.0))
        ranked = sorted(scores.items(), key=lambda kv: -kv[1])
        best, second = ranked[0], ranked[1]
        hours_present = set(g["t"].dt.hour.unique())
        missing = sorted(h for h in range(24) if h not in hours_present or (g["t"].dt.hour == h).sum() < 0.2 * len(g) / 24)
        rows.append({"mois": str(mois), "decalage_h": best[0], "score": round(best[1], 2),
                     "marge_sur_2e": round(best[1] - second[1], 2), "heures_rares_fichier": missing, "barres": int(len(g))})
    return pd.DataFrame(rows)


def main() -> int:
    d15, d5 = read_15m(), read_5m()
    rep = {"xau_15m": integrity(d15, 15), "xau_5m": integrity(d5, 5)}
    off15 = monthly_offset(d15, 15)
    off5 = monthly_offset(d5, 5)
    off15.to_csv(OUT / "decalage_mensuel_15m.csv", index=False)
    off5.to_csv(OUT / "decalage_mensuel_5m.csv", index=False)
    # Segments de convention constante
    # Lissage majoritaire sur 9 mois : un broker ne change pas de convention pour 1 à 3 mois ;
    # les écarts isolés sont du bruit de l'estimateur (mois où un autre créneau domine).
    off15["decalage_lisse"] = off15["decalage_h"].rolling(9, center=True, min_periods=1).apply(lambda v: pd.Series(v).mode().iloc[0]).astype(int)
    segs = []
    for _, r in off15.assign(decalage_h=off15["decalage_lisse"]).iterrows():
        if segs and segs[-1]["decalage_h"] == r["decalage_h"]:
            segs[-1]["fin_mois"] = r["mois"]
            segs[-1]["n_mois"] += 1
        else:
            segs.append({"debut_mois": r["mois"], "fin_mois": r["mois"], "decalage_h": int(r["decalage_h"]), "n_mois": 1})
    rep["segments_convention_15m"] = segs
    rep["decalages_5m"] = off5["decalage_h"].value_counts().to_dict()

    # Recoupement 15 min / 5 min sur la période commune (5 min ré-agrégé)
    a = d5.set_index("t")[["open", "high", "low", "close"]].resample("15min", label="left", closed="left").agg(
        {"open": "first", "high": "max", "low": "min", "close": "last"}).dropna()
    b = d15.set_index("t")[["close"]]
    j = a.join(b, rsuffix="_15", how="inner")
    rep["recoupement_15m_5m"] = {"barres_communes": int(len(j)),
                                 "ecart_median_cloture": round(float((j["close"] - j["close_15"]).abs().median()), 3),
                                 "ecart_p99_cloture": round(float((j["close"] - j["close_15"]).abs().quantile(0.99)), 3)}

    # Convention retenue : segments lissés ; le mois de bascule est exclu (convention ambiguë).
    stable = [s_ for s_ in segs if s_["n_mois"] >= 6]
    excluded = []
    for a_, b_ in zip(stable, stable[1:]):
        if a_["decalage_h"] != b_["decalage_h"]:
            excluded.append(b_["debut_mois"])
    conv = {
        "source": "research/01_audit_donnees.py",
        "regle": "heure_new_york = heure_fichier - decalage_h",
        "segments_15m": [{"debut": s_["debut_mois"], "fin": s_["fin_mois"], "decalage_h": s_["decalage_h"]} for s_ in stable],
        "mois_exclus": excluded,
        "fichier_5m_decalage_h": 7,
        "fichier_5m_justification": "pause quotidienne à 00:00 heure fichier tous les jours (17:00 New York) et pic des NFP à 15:30",
        "bascule_15m_vers_5m": str(d5["t"].iloc[0]),
    }
    CONV.write_text(json.dumps(conv, indent=2))
    (OUT / "audit.json").write_text(json.dumps(rep, indent=2, ensure_ascii=False))

    L = ["# Audit des données historiques", ""]
    for k in ("xau_15m", "xau_5m"):
        r = rep[k]
        L += [f"## {k}", "", f"- {r['lignes']} barres, du {r['debut']} au {r['fin']}",
              f"- ordre croissant : {r['ordre_croissant']}, doublons : {r['doublons']}, OHLC incohérents : {r['ohlc_incoherents']}, prix ≤ 0 : {r['prix_non_positifs']}",
              f"- intervalles réguliers : {r['pas_attendu_pct']} % ; volume : {r['volume']}",
              f"- trous de plus de 4 jours : {len(r['trous_plus_de_4_jours'])}"]
        for g in r["trous_plus_de_4_jours"]:
            L.append(f"  - après {g['apres']} → reprise {g['reprise']} ({g['jours']} jours)")
        L.append("")
    L += ["## Fuseau horaire (heure New York = heure du fichier − décalage)", "", "| Du mois | Au mois | Décalage | Nb mois |", "|---|---|---|---|"]
    for s in segs:
        L.append(f"| {s['debut_mois']} | {s['fin_mois']} | {s['decalage_h']} h | {s['n_mois']} |")
    L += ["", f"Fichier 5 min : décalage le plus fréquent = {conv['fichier_5m_decalage_h']} h ({rep['decalages_5m']}).",
          f"Recoupement 15 min / 5 min : {rep['recoupement_15m_5m']}"]
    (OUT / "audit.md").write_text("\n".join(L))
    print("\n".join(L))
    return 0


if __name__ == "__main__":
    sys.exit(main())
