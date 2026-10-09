"""Chargement des données historiques du dépôt, converties en UTC selon la convention établie par l'audit.

La convention (décalage entre l'heure du fichier et l'heure de New York, par période) est lue dans
`conventions.json`, produit par `research/01_audit_donnees.py`. Aucune valeur n'est codée en dur ici.
Index retourné : DatetimeIndex UTC en nanosecondes = DÉBUT de chaque barre.
"""
from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path

import pandas as pd

PKG = Path(__file__).resolve().parent
REPO = PKG.parents[3]
CONVENTIONS = PKG / "conventions.json"
F15 = REPO / "data" / "xau_15m_2004_2025.csv"
F5 = REPO / "data" / "xauusd_5m_2025.csv"

PRIMARY_START = pd.Timestamp("2011-05-01", tz="UTC")


def _conv() -> dict:
    return json.loads(CONVENTIONS.read_text())


def _to_utc(file_time: pd.Series, offset_h: int) -> pd.Series:
    ny = file_time - pd.Timedelta(hours=offset_h)
    return ny.dt.tz_localize("America/New_York", ambiguous="NaT", nonexistent="NaT").dt.tz_convert("UTC")


def _frame(d: pd.DataFrame, source: str) -> pd.DataFrame:
    d = d.dropna(subset=["ts"]).sort_values("ts").drop_duplicates("ts")
    out = d.set_index("ts")[["open", "high", "low", "close", "volume"]].astype(float)
    out.index = pd.DatetimeIndex(out.index).as_unit("ns")
    out["source"] = source
    return out


def resample(df: pd.DataFrame, minutes: int) -> pd.DataFrame:
    """Ré-agrégation alignée sur l'horloge (les décalages UTC/New York sont des heures entières)."""
    r = df[["open", "high", "low", "close", "volume"]].resample(f"{minutes}min", label="left", closed="left").agg(
        {"open": "first", "high": "max", "low": "min", "close": "last", "volume": "sum"}).dropna(subset=["open"])
    r.index = r.index.as_unit("ns")
    if "source" in df.columns:
        r["source"] = df["source"].resample(f"{minutes}min", label="left", closed="left").first().reindex(r.index)
    return r


@lru_cache(maxsize=2)
def load_15m(include_secondary: bool = False) -> pd.DataFrame:
    """Barres 15 min en UTC.

    Période principale : 01/05/2011 → 28/10/2025 (fichier 15 min jusqu'au 13/02/2025 22:30 heure
    fichier, puis fichier 5 min ré-agrégé, car le fichier 15 min a des trous de plusieurs semaines en 2025).
    include_secondary=True ajoute 2004 → mars 2011 (décalage 6 h), réservé aux contrôles de robustesse.
    """
    conv = _conv()
    raw = pd.read_csv(F15, sep=";")
    raw.columns = [c.strip().lower() for c in raw.columns]
    raw["t"] = pd.to_datetime(raw["date"], format="%Y.%m.%d %H:%M")
    switch = pd.Timestamp(conv["bascule_15m_vers_5m"])
    excluded = {pd.Period(m, "M") for m in conv["mois_exclus"]}
    parts = []
    for seg in conv["segments_15m"]:
        lo = pd.Period(seg["debut"], "M").start_time
        hi = pd.Period(seg["fin"], "M").end_time
        part = raw[(raw["t"] >= lo) & (raw["t"] <= hi) & (raw["t"] < switch)].copy()
        part = part[~part["t"].dt.to_period("M").isin(excluded)]
        if part.empty:
            continue
        part["ts"] = _to_utc(part["t"], seg["decalage_h"])
        parts.append(_frame(part, f"xau15m_decalage{seg['decalage_h']}h"))
    five = load_5m()
    parts.append(resample(five[five.index >= _to_utc(pd.Series([switch]), conv["fichier_5m_decalage_h"]).iloc[0]], 15).assign(source="xau5m_reagrege"))
    out = pd.concat(parts).sort_index()
    out = out[~out.index.duplicated(keep="first")]
    if not include_secondary:
        out = out[out.index >= PRIMARY_START]
    return out


@lru_cache(maxsize=1)
def load_5m() -> pd.DataFrame:
    conv = _conv()
    raw = pd.read_csv(F5)
    raw.columns = [c.strip().lower() for c in raw.columns]
    raw["t"] = pd.to_datetime(raw["date"])
    raw["ts"] = _to_utc(raw["t"], conv["fichier_5m_decalage_h"])
    return _frame(raw, "xau5m")
