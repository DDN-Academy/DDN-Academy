#!/bin/sh
# Rotation du mot de passe PostgreSQL (POSTGRES_PASSWORD) sans perte de données.
# Usage, sur le serveur, depuis le dossier goldpilot/deploy :   sh scripts/rotate-postgres-password.sh
#
# Pourquoi un script : PostgreSQL ne lit POSTGRES_PASSWORD qu'à la toute première création de la base.
# Changer seulement la ligne du fichier .env casserait la connexion (« password authentication failed »).
# Étapes : 1) génération d'un nouveau mot de passe aléatoire ; 2) changement dans PostgreSQL ;
# 3) écriture dans .env ; 4) redémarrage des services qui l'utilisent. Le mot de passe n'est jamais affiché.
set -eu
cd "$(dirname "$0")/.."
IMAGE="goldpilot:${GOLDPILOT_TAG:-latest}"
[ -f .env ] || { echo "Fichier .env introuvable." >&2; exit 1; }

NEW=$(docker run --rm --network none "$IMAGE" python -m goldpilot.cli secret)
[ ${#NEW} -ge 32 ] || { echo "Génération du mot de passe impossible." >&2; exit 1; }

echo "1/3 Changement du mot de passe dans PostgreSQL…"
# Le mot de passe passe par l'entrée standard de psql (ni argument de commande, ni historique).
# Valeur sans apostrophe (lettres, chiffres, « - », « _ ») : insertion sûre dans la requête.
printf "ALTER ROLE goldpilot WITH PASSWORD '%s';\n" "$NEW" \
	| docker compose exec -T postgres psql -v ON_ERROR_STOP=1 -q -U goldpilot -d goldpilot

echo "2/3 Écriture dans .env…"
N=POSTGRES_PASSWORD V="$NEW" awk 'BEGIN { n = ENVIRON["N"]; v = ENVIRON["V"] }
	index($0, n "=") == 1 { if (!done) print n "=" v; done = 1; next }
	{ print }
	END { if (!done) print n "=" v }' .env > .env.tmp
chmod 600 .env.tmp
mv .env.tmp .env
NEW=""

echo "3/3 Redémarrage des services (migrations, site, moteur, sauvegardes)…"
docker compose up -d --force-recreate migrate web engine backup
echo "Terminé. Vérifie : sh scripts/status.sh"
