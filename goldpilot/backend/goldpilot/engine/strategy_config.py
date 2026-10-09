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
