#!/usr/bin/env bash
# Démarre un backend GoldPilot ISOLÉ pour les tests de bout en bout :
# base SQLite temporaire, jeu de données de test déterministe (fictif), site compilé (dist) servi par uvicorn.
# Aucun secret réel : mot de passe et jeton de webhook de test uniquement.
set -euo pipefail

ICI="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND="$(cd "$ICI/../../backend" && pwd)"
DIR="${GOLDPILOT_E2E_DIR:?GOLDPILOT_E2E_DIR non défini (voir playwright.config.ts)}"
PORT="${GOLDPILOT_E2E_PORT:-8102}"
PY="${PYTHON:-python3}"

mkdir -p "$DIR"
rm -f "$DIR/e2e.db"

export APP_ENV=development
export DATABASE_URL="sqlite:///$DIR/e2e.db"
export DATA_SOURCE=tradingview
export TV_ENFORCE_IP=false
export TV_WEBHOOK_TOKEN=e2e-jeton-de-test-0123456789abcdef
export PUBLIC_BASE_URL="http://127.0.0.1:$PORT"
# Chaque test envoie son propre X-Forwarded-For : les limites de débit (5 connexions / 15 min par IP) restent actives
# mais ne s'appliquent qu'à l'intérieur d'un test.
export TRUST_PROXY=true
export TELEGRAM_BOT_TOKEN=
export TELEGRAM_CHAT_ID=
export FRED_API_KEY=
export PYTHONPATH="$BACKEND${PYTHONPATH:+:$PYTHONPATH}"
export ADMIN_PASSWORD_HASH="$("$PY" -c 'from goldpilot.api.security import hash_password; print(hash_password("e2e-mot-de-passe-123"))')"

cd "$BACKEND"
"$PY" "$ICI/seed.py" init
exec "$PY" -m uvicorn goldpilot.api.app:app --host 127.0.0.1 --port "$PORT" --log-level warning
