#!/usr/bin/env bash
# ---------------------------------------------------------------------------------------------------
# GoldPilot — installation automatique sur un serveur neuf (Ubuntu 22.04 / 24.04 ou Debian 12), en UNE commande :
#
#   curl -fsSL https://raw.githubusercontent.com/DDN-Academy/DDN-Academy/claude/goldpilot/goldpilot/deploy/installer.sh | sudo bash
#
# Avant de la lancer : le nom de domaine (ex. goldpilot.mondomaine.fr) doit pointer vers l'adresse IPv4 du serveur
# (enregistrement DNS de type A, voir docs/05 § 2).
#
# Ce que fait le script (rien n'est acheté, aucun compte n'est créé) :
#   1. installe Docker s'il est absent (paquets officiels de la distribution, sinon script officiel get.docker.com) ;
#   2. télécharge GoldPilot (branche claude/goldpilot) dans /opt/goldpilot ;
#   3. construit l'image, génère les secrets et te demande le mot de passe du site (seul son hachage est gardé) ;
#   4. te demande le domaine, une adresse e-mail (certificat HTTPS) et, si tu veux, le bot Telegram ;
#   5. démarre le site, le moteur, la base, HTTPS et les sauvegardes, puis vérifie que tout répond.
# Aucun secret n'est envoyé ailleurs que sur ton serveur. Le fichier de configuration est /opt/goldpilot/goldpilot/deploy/.env
# (droits 600). Non testé sur un vrai VPS par son auteur : les étapes reprennent la procédure de docs/05, elle-même
# exécutée avec succès dans Docker le 10/10/2026 (voir le début de docs/05).
# ---------------------------------------------------------------------------------------------------
set -euo pipefail

BRANCHE="claude/goldpilot"
ARCHIVE="https://github.com/DDN-Academy/DDN-Academy/archive/refs/heads/${BRANCHE}.tar.gz"
DEST="/opt/goldpilot"
DEPLOY="$DEST/goldpilot/deploy"

say() { printf '\n\033[1m==> %s\033[0m\n' "$*"; }
die() { printf '\n\033[31mERREUR : %s\033[0m\n' "$*" >&2; exit 1; }
ask() { local q="$1" v; printf '%s' "$q" > /dev/tty; IFS= read -r v < /dev/tty; printf '%s' "$v"; }

[ "$(id -u)" -eq 0 ] || die "lance la commande avec sudo (droits administrateur nécessaires)."
[ -r /dev/tty ] || die "le script doit être lancé depuis un terminal (il pose des questions)."
command -v apt-get > /dev/null || die "système non pris en charge : Ubuntu 22.04/24.04 ou Debian 12 requis."
[ -f "$DEPLOY/.env" ] && die "GoldPilot est déjà installé ($DEPLOY/.env existe). Pour une mise à jour, suis docs/05 § 11."

# ------------------------------------------------------------------------------------------------- 1. Docker
say "1/5 Docker"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq ca-certificates curl tar > /dev/null
if ! docker compose version > /dev/null 2>&1; then
	if ! apt-get install -y -qq docker.io docker-compose-v2 > /dev/null 2>&1; then
		echo "Paquets de la distribution indisponibles : installation par le script officiel https://get.docker.com"
		curl -fsSL https://get.docker.com | sh
	fi
fi
systemctl enable --now docker > /dev/null 2>&1 || true
docker compose version > /dev/null 2>&1 || die "Docker Compose n'a pas pu être installé."
echo "Docker prêt : $(docker --version)"

# ------------------------------------------------------------------------------------------------- 2. Code
say "2/5 Téléchargement de GoldPilot ($BRANCHE)"
TMP=$(mktemp -d)
curl -fsSL "$ARCHIVE" -o "$TMP/goldpilot.tar.gz" || die "téléchargement impossible ($ARCHIVE)."
mkdir -p "$DEST"
tar -xzf "$TMP/goldpilot.tar.gz" -C "$TMP"
SRC=$(find "$TMP" -maxdepth 1 -mindepth 1 -type d | head -n 1)
[ -d "$SRC/goldpilot/deploy" ] || die "archive inattendue : dossier goldpilot/deploy absent."
rm -rf "$DEST/goldpilot"
cp -a "$SRC/goldpilot" "$DEST/goldpilot"
rm -rf "$TMP"
echo "Installé dans $DEST/goldpilot"

# ------------------------------------------------------------------------------------------------- 3. Image + secrets
say "3/5 Construction de l'image (quelques minutes) et secrets"
cd "$DEPLOY"
docker build -q -t goldpilot:latest .. > /dev/null
sh scripts/init-secrets.sh < /dev/tty

set_var() { # remplace (ou ajoute) NOM=valeur dans .env sans interpréter la valeur
	N="$1" V="$2" awk 'BEGIN { n = ENVIRON["N"]; v = ENVIRON["V"] }
		index($0, n "=") == 1 { if (!done) print n "=" v; done = 1; next }
		{ print }
		END { if (!done) print n "=" v }' .env > .env.tmp
	chmod 600 .env.tmp && mv .env.tmp .env
}

# ------------------------------------------------------------------------------------------------- 4. Questions
say "4/5 Configuration"
DOMAINE=""
while [ -z "$DOMAINE" ]; do
	DOMAINE=$(ask "Nom de domaine du site (ex. goldpilot.mondomaine.fr, sans https://) : " | tr -d ' ' | sed 's#^https\?://##; s#/.*$##')
done
IP_SERVEUR=$(curl -fsS -4 https://api.ipify.org 2> /dev/null || true)
IP_DNS=$(getent ahostsv4 "$DOMAINE" 2> /dev/null | awk 'NR==1{print $1}' || true)
if [ -n "$IP_SERVEUR" ] && [ "$IP_DNS" != "$IP_SERVEUR" ]; then
	echo "ATTENTION : $DOMAINE pointe vers « ${IP_DNS:-rien} » alors que ce serveur est $IP_SERVEUR."
	echo "Le certificat HTTPS ne pourra pas être obtenu tant que l'enregistrement DNS A n'est pas corrigé (docs/05 § 2)."
	[ "$(ask "Continuer quand même ? (oui/non) : ")" = "oui" ] || die "installation interrompue : corrige le DNS puis relance (supprime d'abord $DEST)."
fi
EMAIL=""
while ! printf '%s' "$EMAIL" | grep -q '^[^@ ]\+@[^@ ]\+\.[^@ ]\+$'; do
	EMAIL=$(ask "Adresse e-mail pour le certificat HTTPS (Let's Encrypt) : " | tr -d ' ')
done
set_var GOLDPILOT_DOMAIN "$DOMAINE"
set_var ACME_EMAIL "$EMAIL"

if [ "$(ask "Configurer maintenant les alertes Telegram ? (oui/non) : ")" = "oui" ]; then
	echo "Sur ton téléphone : ouvre Telegram, écris à @BotFather, envoie /newbot et suis les questions ;"
	echo "il te donne un jeton du type 123456789:AA...  (garde-le secret)."
	stty -echo < /dev/tty 2> /dev/null || true
	TG=$(ask "Colle le jeton du bot (rien ne s'affiche) : ")
	stty echo < /dev/tty 2> /dev/null || true
	echo
	ask "Envoie maintenant un message (par ex. « bonjour ») à TON bot dans Telegram, puis appuie sur Entrée... " > /dev/null
	CHAT=$(docker run --rm --network bridge -e TG="$TG" goldpilot:latest python -c '
import os
from goldpilot.notify.telegram import Telegram
r = Telegram(os.environ["TG"], "").detect_chat_id()
print(r[-1]["chat_id"] if r else "")' 2> /dev/null || true)
	if [ -n "$CHAT" ]; then
		set_var TELEGRAM_BOT_TOKEN "$TG"
		set_var TELEGRAM_CHAT_ID "$CHAT"
		echo "Telegram configuré (conversation $CHAT)."
	else
		echo "Conversation introuvable : tu pourras finir plus tard depuis le site (Réglages › Telegram) et docs/06."
		set_var TELEGRAM_BOT_TOKEN "$TG"
	fi
	TG=""
fi

if command -v ufw > /dev/null && ufw status 2> /dev/null | grep -q "Status: active"; then
	ufw allow 80/tcp > /dev/null && ufw allow 443/tcp > /dev/null && echo "Pare-feu : ports 80 et 443 ouverts."
fi

# ------------------------------------------------------------------------------------------------- 5. Démarrage
say "5/5 Démarrage"
docker compose up -d
echo "Attente du site (certificat HTTPS compris, jusqu'à 3 minutes)..."
OK=""
for _ in $(seq 1 36); do
	if curl -fsS --max-time 5 "https://$DOMAINE/api/health" > /dev/null 2>&1; then OK=1; break; fi
	sleep 5
done
sh scripts/status.sh || true

JETON=$(sed -n 's/^TV_WEBHOOK_TOKEN=//p' .env | tail -n 1)
cat << FIN

==========================================================================================================
$( [ -n "$OK" ] && echo "GoldPilot est EN LIGNE." || echo "Les services tournent mais https://$DOMAINE ne répond pas encore (DNS ou certificat) : relance « sh $DEPLOY/scripts/status.sh » dans quelques minutes." )

  Ton site               : https://$DOMAINE   (mot de passe choisi à l'étape 3)
  Adresse du webhook     : https://$DOMAINE/api/webhooks/tradingview
  Jeton pour TradingView : $JETON
                           (à coller dans le champ « Jeton secret » du script GoldPilot Bridge ; ne le partage pas)

Dernière étape, dans TradingView (abonnement payant + double authentification + données temps réel COMEX) :
  suis Réglages › TradingView sur ton site (ou docs/06 § « Première mise en service »).
Tant que TradingView n'envoie pas les prix, le site affiche « Données indisponibles » : c'est normal.
Rappel : la stratégie n'est PAS validée, les signaux restent en SIMULATION.
==========================================================================================================
FIN
