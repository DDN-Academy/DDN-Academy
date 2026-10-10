#!/bin/sh
# Sauvegarde immédiate de la base (par exemple avant une mise à jour).
# Usage, depuis le dossier goldpilot/deploy :   sh scripts/backup-now.sh
# Le fichier est écrit dans goldpilot/deploy/backups/ (même format que les sauvegardes quotidiennes).
set -eu
cd "$(dirname "$0")/.."
docker compose exec -T backup /bin/sh /scripts/backup-loop.sh once
ls -lh backups | tail -n 3
