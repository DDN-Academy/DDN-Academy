#!/bin/sh
# État de GoldPilot en une commande (à lancer sur le serveur, depuis le dossier goldpilot/deploy) :
#   sh scripts/status.sh
# Affiche : l'état de chaque service, la réponse publique de /api/health, la dernière sauvegarde,
# l'espace disque. N'affiche aucun secret.
set -u
cd "$(dirname "$0")/.."

echo "== Services (STATUS doit indiquer « Up » et « healthy » pour web et engine)"
docker compose ps --format 'table {{.Service}}\t{{.Status}}'

DOMAIN=$(sed -n 's/^GOLDPILOT_DOMAIN=//p' .env 2>/dev/null | tail -n 1 | tr -d '"' | tr -d "'")
echo
echo "== Santé publique : https://$DOMAIN/api/health"
if [ -n "$DOMAIN" ]; then
	curl -sS -m 10 -w '  (code HTTP %{http_code})\n' "https://$DOMAIN/api/health" || echo "  injoignable"
else
	echo "  GOLDPILOT_DOMAIN absent de .env"
fi

echo
echo "== Dernières sauvegardes (deploy/backups)"
ls -1t backups/*.dump 2>/dev/null | head -n 3 | while read -r f; do
	echo "  $(basename "$f")  $(du -h "$f" | cut -f1)"
done
[ -n "$(find backups -maxdepth 1 -name '*.dump' -mmin -1560 2>/dev/null | head -n 1)" ] \
	&& echo "  OK : sauvegarde de moins de 26 h" || echo "  ATTENTION : aucune sauvegarde de moins de 26 h (voir : docker compose logs backup)"

echo
echo "== Espace disque"
df -h . | tail -n 1 | awk '{print "  utilisé " $5 " — libre " $4}'
