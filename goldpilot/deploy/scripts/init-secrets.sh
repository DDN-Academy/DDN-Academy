#!/bin/sh
# Prépare le fichier deploy/.env de production : crée le fichier s'il n'existe pas, génère les secrets
# aléatoires manquants et enregistre le hachage de ton mot de passe de connexion au site.
#
# Usage (sur le serveur, depuis le dossier goldpilot/deploy, APRÈS « docker build -t goldpilot:latest .. ») :
#   sh scripts/init-secrets.sh
#
# - POSTGRES_PASSWORD, SECRET_KEY, TV_WEBHOOK_TOKEN : générés seulement s'ils sont VIDES (jamais écrasés ;
#   pour changer un secret existant, suivre la procédure de rotation de docs/05).
# - ADMIN_PASSWORD_HASH : si la valeur d'exemple est encore là, le mot de passe t'est demandé deux fois
#   (rien ne s'affiche pendant la saisie) ; seul son hachage est écrit dans .env.
# Aucun secret n'est affiché à l'écran. Le fichier .env reçoit les droits 600 (lisible par toi seul).
set -eu
cd "$(dirname "$0")/.."
IMAGE="goldpilot:${GOLDPILOT_TAG:-latest}"

docker image inspect "$IMAGE" > /dev/null 2>&1 || {
	echo "Image $IMAGE introuvable : lance d'abord « docker build -t $IMAGE .. » depuis goldpilot/deploy." >&2
	exit 1
}

if [ ! -f .env ]; then
	cp .env.example .env
	echo "Fichier .env créé à partir de .env.example."
fi
chmod 600 .env

get_var() { sed -n "s/^$1=//p" .env | tail -n 1; }

# Remplace (ou ajoute) la ligne NOM=valeur sans interpréter les caractères spéciaux de la valeur.
set_var() {
	N="$1" V="$2" awk 'BEGIN { n = ENVIRON["N"]; v = ENVIRON["V"] }
		index($0, n "=") == 1 { if (!done) print n "=" v; done = 1; next }
		{ print }
		END { if (!done) print n "=" v }' .env > .env.tmp
	chmod 600 .env.tmp
	mv .env.tmp .env
}

for name in POSTGRES_PASSWORD SECRET_KEY TV_WEBHOOK_TOKEN; do
	if [ -z "$(get_var "$name")" ]; then
		set_var "$name" "$(docker run --rm --network none "$IMAGE" python -m goldpilot.cli secret)"
		echo "$name : généré."
	else
		echo "$name : déjà défini, conservé."
	fi
done

case "$(get_var ADMIN_PASSWORD_HASH)" in
	*REMPLACER*|"")
		echo "Choisis le mot de passe de connexion au site (12 caractères minimum ; rien ne s'affiche pendant la frappe)."
		stty -echo 2> /dev/null || true
		printf "Mot de passe : "; IFS= read -r pw1; echo
		printf "Confirmer    : "; IFS= read -r pw2; echo
		stty echo 2> /dev/null || true
		# Le mot de passe passe par un tube vers le conteneur (jamais en argument de commande, jamais écrit).
		h=$(printf '%s\n%s\n' "$pw1" "$pw2" | docker run --rm -i --network none "$IMAGE" python -m goldpilot.cli hash-password 2> /dev/null | tail -n 1) || h=""
		pw1=""; pw2=""
		case "$h" in
			scrypt\$*) set_var ADMIN_PASSWORD_HASH "'$h'"; echo "ADMIN_PASSWORD_HASH : enregistré." ;;
			*) echo "Échec : mots de passe différents ou trop courts (12 caractères minimum). Relance le script." >&2; exit 1 ;;
		esac
		;;
	*) echo "ADMIN_PASSWORD_HASH : déjà défini, conservé." ;;
esac

echo
echo "Reste à remplir à la main dans .env (nano .env) : GOLDPILOT_DOMAIN, ACME_EMAIL"
echo "et, si tu les as, TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, FRED_API_KEY."
echo "Le jeton TradingView à recopier dans le script Pine s'affiche avec :  grep TV_WEBHOOK_TOKEN .env"
