#!/bin/sh
# Restauration de la base GoldPilot à partir d'une sauvegarde (fichier .dump produit par le service backup).
#
# Usage, depuis le dossier goldpilot/deploy :
#   sh scripts/restore.sh backups/goldpilot-20261010-033000Z.dump
#
# Étapes : 1) arrêt du site et du moteur ; 2) sauvegarde de sécurité de la base actuelle (si possible) ;
# 3) effacement du contenu actuel ; 4) restauration ; 5) redémarrage (les migrations sont réappliquées
# si la sauvegarde est plus ancienne que le code).
# Effet : la base revient EXACTEMENT à l'état de la sauvegarde (signaux, journal, réglages).
set -eu
cd "$(dirname "$0")/.."

FILE="${1:-}"
if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
	echo "Usage : sh scripts/restore.sh backups/goldpilot-AAAAMMJJ-HHMMSSZ.dump" >&2
	echo "Sauvegardes disponibles :" >&2
	ls -1t backups/*.dump 2>/dev/null | head -n 20 >&2 || echo "  (aucune)" >&2
	exit 1
fi

# Le fichier doit être dans backups/ (dossier partagé avec le conteneur backup).
case "$(cd "$(dirname "$FILE")" && pwd)" in
	"$(pwd)/backups") ;;
	*) cp "$FILE" backups/ && chmod 600 "backups/$(basename "$FILE")" ;;
esac
NAME="$(basename "$FILE")"

if [ "${GOLDPILOT_RESTORE_CONFIRM:-}" != "OUI" ]; then
	printf "La base actuelle va être REMPLACÉE par %s. Tape OUI pour continuer : " "$NAME"
	read -r answer
	[ "$answer" = "OUI" ] || { echo "Annulé."; exit 1; }
fi

echo "1/5 Arrêt du site et du moteur…"
docker compose stop web engine

echo "2/5 Démarrage de la base et du service de sauvegarde…"
docker compose up -d postgres backup
i=0
until docker compose exec -T postgres pg_isready -U goldpilot -d goldpilot > /dev/null 2>&1; do
	i=$((i + 1)); [ $i -gt 30 ] && { echo "La base ne répond pas." >&2; exit 1; }; sleep 2
done

echo "3/5 Sauvegarde de sécurité de l'état actuel (avant restauration)…"
docker compose exec -T backup /bin/sh /scripts/backup-loop.sh once || echo "   (impossible : base vide ou endommagée — on continue)"

echo "4/5 Restauration de $NAME…"
docker compose exec -T backup psql -v ON_ERROR_STOP=1 -q -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"
docker compose exec -T backup pg_restore --no-owner --exit-on-error --single-transaction -d goldpilot "/backups/$NAME"

echo "5/5 Redémarrage (migrations, site, moteur)…"
docker compose up -d
echo "Restauration terminée. Vérifie : sh scripts/status.sh"
