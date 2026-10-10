"""Contrôle de santé Docker des conteneurs GoldPilot (copié dans l'image : /app/deploy/healthcheck.py).

  python /app/deploy/healthcheck.py web     -> le processus web répond-il ? (code 0 = sain)
  python /app/deploy/healthcheck.py engine  -> le moteur a-t-il écrit son battement de cœur récemment ?

Le contrôle « web » accepte la réponse 503 de /api/health : elle signifie « site en ligne mais moteur
silencieux ». Le site doit rester joignable dans ce cas pour AFFICHER la panne du moteur ; c'est le
contrôle « engine » (et la surveillance externe, voir docs/05) qui signale la panne du moteur.
Aucun secret n'est lu ni affiché.
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request
from datetime import datetime, timezone

ENGINE_MAX_AGE_S = 90  # le moteur écrit un battement toutes les ~10 s ; 90 s laisse une marge


def check_web() -> int:
    try:
        with urllib.request.urlopen("http://127.0.0.1:8000/api/health", timeout=4) as r:
            body = json.loads(r.read() or b"{}")
    except urllib.error.HTTPError as e:  # 503 = moteur silencieux, le site lui-même fonctionne
        try:
            body = json.loads(e.read() or b"{}")
        except ValueError:
            body = {}
    except Exception as e:  # connexion refusée, délai dépassé…
        print(f"web injoignable : {type(e).__name__}")
        return 1
    ok = body.get("web") == "ok"
    print("web ok" if ok else f"réponse inattendue : {body}")
    return 0 if ok else 1


def check_engine() -> int:
    from goldpilot import db

    try:
        with db.session() as s:
            hb = s.get(db.Heartbeat, "engine")
    except Exception as e:
        print(f"base de données injoignable : {type(e).__name__}")
        return 1
    if hb is None:
        print("aucun battement de cœur du moteur")
        return 1
    ts = hb.ts if hb.ts.tzinfo else hb.ts.replace(tzinfo=timezone.utc)
    age = (datetime.now(tz=timezone.utc) - ts).total_seconds()
    print(f"moteur : dernier battement il y a {age:.0f} s (état {hb.status})")
    return 0 if age < ENGINE_MAX_AGE_S else 1


if __name__ == "__main__":
    what = sys.argv[1] if len(sys.argv) > 1 else "web"
    sys.exit(check_engine() if what == "engine" else check_web())
