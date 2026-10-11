"""Stratégie de production et statut de validation, lus dans les résultats de recherche (jamais codés en dur).

Fichier source : research/output/final/production.json, écrit par research/05_test_final.py après le
test final. S'il est absent, le moteur refuse d'émettre des signaux (« aucune stratégie configurée »).
Le champ `validated` n'est vrai que si tous les critères pré-enregistrés ont été satisfaits.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

from ..config import settings
from ..strategy.candidates import S1SessionExtension, S2LondonToNewYork

REGISTRY = {"S1": S1SessionExtension, "S2": S2LondonToNewYork}


def production_file() -> Path:
    return settings().research_dir / "final" / "production.json"


@lru_cache(maxsize=1)
def load_production() -> dict | None:
    p = production_file()
    if not p.exists():
        return None
    return json.loads(p.read_text())


def build_strategy(conf: dict | None = None):
    conf = conf or load_production()
    if not conf:
        return None
    cls = REGISTRY[conf["strategy"]]
    params = dict(conf["params"])
    if conf["strategy"] == "S1":
        params = {"k": float(params["k"]), "s": float(params["s"]), "t": float(params["t"]), "F": str(params["F"]) in ("True", "true", "1")}
    elif conf["strategy"] == "S2":
        params = {"q": float(params["q"]), "s": float(params["s"]), "E": params["E"]}
    return cls(**params)


def version() -> str:
    c = load_production()
    return c["version"] if c else "aucune"


def validation_status() -> str:
    c = load_production()
    if not c:
        return "Aucune stratégie configurée : la recherche n'a pas encore produit research/output/final/production.json."
    return (f"Stratégie {c['version']} — {'VALIDÉE' if c['validated'] else 'NON VALIDÉE (simulation uniquement)'}\n"
            f"{c.get('verdict', '')}")


def _read_json(p: Path) -> dict | None:
    try:
        return json.loads(p.read_text())
    except (OSError, ValueError):
        return None


def _dig(d: dict | None, *keys):
    for k in keys:
        if not isinstance(d, dict) or k not in d:
            return None
        d = d[k]
    return float(d) if isinstance(d, (int, float)) else None


def research_reference() -> dict:
    """Espérances de référence de la recherche, lues dans les fichiers produits (jamais codées en dur) :
    walk-forward 2011-2021 (selection.json, famille S1) et période exploratoire 2022-2025 (final.json).
    Une valeur absente vaut None (fichier manquant ou structure différente)."""
    out = settings().research_dir
    sel = _read_json(out / "selection" / "selection.json")
    fin = _read_json(out / "final" / "final.json")
    wf = _dig(sel, "familles", "S1", "walk_forward", "resume", "esperance_R")
    if wf is None:
        wf = _dig(fin, "walk_forward_S1", "esperance_R")
    return {"esperance_R_walk_forward": None if wf is None else round(wf, 3),
            "esperance_R_2022_2025": None if (x := _dig(fin, "exploratoire_base", "esperance_R")) is None else round(x, 3),
            "source": "research/output/selection,final"}
