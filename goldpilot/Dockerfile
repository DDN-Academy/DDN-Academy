# syntax=docker/dockerfile:1.7
# ---------------------------------------------------------------------------------------------------
# Image unique GoldPilot : le même fichier sert aux services « web » (FastAPI + site compilé),
# « engine » (moteur temps réel) et « migrate » (migrations de la base). Voir deploy/docker-compose.yml.
#
# Construction (depuis le dossier goldpilot/) :   docker build -t goldpilot:latest .
# Aucun secret n'est copié dans l'image : toute la configuration arrive au démarrage par variables
# d'environnement (fichier deploy/.env, jamais dans Git ni dans l'image — voir .dockerignore).
#
# Option réseau d'entreprise : si la construction passe par un proxy TLS qui remplace les certificats,
# fournir son certificat racine sans l'inscrire dans l'image :
#   docker build --secret id=extra_ca,src=/chemin/ca.crt -t goldpilot:latest .
# (le fichier n'est monté que pendant les « RUN » concernés et n'apparaît dans aucune couche).
# ---------------------------------------------------------------------------------------------------

# ---------- étape 1 : compilation du site (React + TypeScript + Vite) -> fichiers statiques ----------
FROM node:22-slim AS frontend
WORKDIR /src
COPY frontend/package.json frontend/package-lock.json ./
RUN --mount=type=secret,id=extra_ca,required=false \
    if [ -s /run/secrets/extra_ca ]; then export NODE_EXTRA_CA_CERTS=/run/secrets/extra_ca npm_config_cafile=/run/secrets/extra_ca; fi; \
    npm ci --no-audit --no-fund
COPY frontend/ ./
RUN npm run build && test -f dist/index.html

# ---------- étape 2 : image d'exécution Python ----------
FROM python:3.12-slim AS runtime

# Paquets Python supplémentaires (Databento, flux temps réel optionnel DATA_SOURCE=databento) : 0 ou 1.
ARG WITH_DATABENTO=0

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    APP_ENV=production \
    FRONTEND_DIR=/app/frontend/dist \
    RESEARCH_DIR=/app/research/output

# Utilisateur sans privilèges (aucun processus ne tourne en root dans le conteneur).
RUN groupadd --system --gid 10001 goldpilot \
 && useradd --system --uid 10001 --gid goldpilot --home-dir /app --no-create-home --shell /usr/sbin/nologin goldpilot

WORKDIR /app

# Dépendances d'abord (couche mise en cache tant que pyproject.toml ne change pas).
COPY backend/pyproject.toml /app/backend/pyproject.toml
RUN python - <<'EOF' > /tmp/requirements.txt
import os, tomllib
d = tomllib.load(open("/app/backend/pyproject.toml", "rb"))["project"]
deps = list(d["dependencies"])
if os.environ.get("WITH_DATABENTO", "0") == "1":
    deps += d["optional-dependencies"]["databento"]
print("\n".join(deps))
EOF
RUN --mount=type=secret,id=extra_ca,required=false \
    if [ -s /run/secrets/extra_ca ]; then export PIP_CERT=/run/secrets/extra_ca; fi; \
    pip install -r /tmp/requirements.txt && rm /tmp/requirements.txt

# Code du backend, utilisé « en place » (PYTHONPATH) : le code calcule ses chemins (pine/,
# research/output/, migrations/) à partir de son propre emplacement, il doit donc rester dans /app/backend.
COPY backend/ /app/backend/
ENV PYTHONPATH=/app/backend

# Fichiers lus à l'exécution :
#  - pine/goldpilot_bridge.pine            -> /api/setup/pine (copie du script depuis le site)
#  - research/output/**.json / **.md       -> configuration de production (final/production.json) et /api/stats
#  - frontend/dist                         -> le site
COPY pine/ /app/pine/
COPY research/output/ /app/research/output/
COPY --from=frontend /src/dist/ /app/frontend/dist/
COPY deploy/healthcheck.py /app/deploy/healthcheck.py

# Vérification à la construction : les fichiers indispensables sont présents (échec immédiat sinon).
RUN test -f /app/research/output/final/production.json \
 && test -f /app/pine/goldpilot_bridge.pine \
 && test -f /app/frontend/dist/index.html \
 && python -c "import goldpilot.api.app, goldpilot.engine.runner, goldpilot.cli"

USER goldpilot
EXPOSE 8000

# Contrôle de santé par défaut (service web). Le service engine le remplace dans docker-compose.yml.
HEALTHCHECK --interval=30s --timeout=5s --start-period=30s --retries=3 \
    CMD ["python", "/app/deploy/healthcheck.py", "web"]

# Un seul processus uvicorn (voir docs/05_deploiement_et_exploitation.md : les limites anti-abus sont
# tenues en mémoire par processus). --factory : la configuration est vérifiée avant d'accepter du trafic.
CMD ["python", "-m", "uvicorn", "--factory", "goldpilot.api.app:create_app", "--host", "0.0.0.0", "--port", "8000", \
     "--workers", "1", "--no-server-header", "--timeout-graceful-shutdown", "20"]
