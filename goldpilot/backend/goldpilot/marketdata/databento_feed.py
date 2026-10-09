"""Flux temps réel indépendant Databento (optionnel, DATA_SOURCE=databento) : barres d'une minute du MGC.

Supprime la dépendance unique à TradingView. Nécessite un abonnement Databento CME (199 $/mois au
9 octobre 2026, à souscrire par toi) et DATABENTO_API_KEY.
Implémenté d'après le client officiel `databento` (Live, jeu GLBX.MDP3, schéma ohlcv-1m, symboles bruts
« MGCZ6 ») ; NON testé contre le service réel (pas de clé ni d'accès réseau dans l'environnement de
développement). Les prix Databento sont des entiers en 1e-9 $ ; ts_event = début de l'intervalle.
"""
from __future__ import annotations

import logging
import threading
import time
from datetime import datetime, timezone

from .. import db
from ..timeutil import trading_date, utcnow
from .contracts import active_contract

log = logging.getLogger("goldpilot.databento")
SCALE = 1e-9


def record_to_bar(rec, symbol_long: str):
    """Convertit un OHLCVMsg Databento en ligne Bar (testé avec un objet simulé)."""
    ts = datetime.fromtimestamp(rec.ts_event / 1e9, tz=timezone.utc)
    return db.Bar(source="databento", symbol=symbol_long, ts=ts, minutes=1, open=rec.open * SCALE, high=rec.high * SCALE,
                  low=rec.low * SCALE, close=rec.close * SCALE, volume=float(rec.volume), processed=False, received_at=utcnow())


def _run(api_key: str) -> None:  # pragma: no cover - nécessite le service réel
    import databento as dbn

    while True:
        c = active_contract(trading_date(utcnow()))
        try:
            client = dbn.Live(key=api_key, reconnect_policy="reconnect")
            client.subscribe(dataset="GLBX.MDP3", schema="ohlcv-1m", stype_in="raw_symbol", symbols=[c.short_code])
            for rec in client:
                if isinstance(rec, dbn.OHLCVMsg):
                    with db.session() as s:
                        s.add(record_to_bar(rec, c.code))
                if active_contract(trading_date(utcnow())) != c:
                    client.stop()
                    break
        except Exception as e:
            log.error("flux Databento interrompu : %s", type(e).__name__)
            with db.session() as s:
                db.open_incident(s, "alerte", "donnees", "databento", f"Flux Databento interrompu ({type(e).__name__}), reconnexion")
            time.sleep(10)


def start_databento_thread(api_key: str) -> threading.Thread:
    if not api_key:
        raise SystemExit("DATA_SOURCE=databento exige DATABENTO_API_KEY")
    t = threading.Thread(target=_run, args=(api_key,), daemon=True, name="databento")
    t.start()
    return t
