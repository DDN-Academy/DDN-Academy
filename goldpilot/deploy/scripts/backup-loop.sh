#!/bin/sh
# Sauvegarde automatique de la base GoldPilot (exécuté par le service « backup » de docker-compose.yml).
#
# Toutes les 10 minutes, le script vérifie s'il existe une sauvegarde de moins de BACKUP_INTERVAL_HOURS
# heures (24 par défaut) ; sinon il en crée une. Ce fonctionnement résiste aux redémarrages : après un
# arrêt du serveur, la sauvegarde manquante est faite dès le retour.
# Fichiers : /backups/goldpilot-AAAAMMJJ-HHMMSSZ.dump (format pg_dump « custom », compressé), droits 600.
# Les sauvegardes de plus de BACKUP_RETENTION_DAYS jours (14 par défaut) sont supprimées.
# « backup-loop.sh once » : une seule sauvegarde immédiate, puis fin.
# Connexion : variables PGHOST, PGUSER, PGPASSWORD, PGDATABASE (fournies par docker-compose.yml).
set -u
umask 077

RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-14}"
INTERVAL_HOURS="${BACKUP_INTERVAL_HOURS:-24}"
DIR=/backups

log() { echo "$(date -u '+%Y-%m-%dT%H:%M:%SZ') backup: $*"; }

do_backup() {
	name="goldpilot-$(date -u '+%Y%m%d-%H%M%SZ').dump"
	tmp="$DIR/.$name.partiel"
	if pg_dump --format=custom --compress=6 --no-owner --file="$tmp"; then
		# Contrôle : l'archive doit être lisible par pg_restore avant d'être considérée comme valide.
		if pg_restore --list "$tmp" > /dev/null 2>&1; then
			mv "$tmp" "$DIR/$name"
			log "sauvegarde OK : $name ($(du -h "$DIR/$name" | cut -f1))"
		else
			rm -f "$tmp"
			log "ERREUR : archive illisible, sauvegarde rejetée"
			return 1
		fi
	else
		rm -f "$tmp"
		log "ERREUR : pg_dump a échoué"
		return 1
	fi
	# Rotation : suppression des sauvegardes plus anciennes que la durée de conservation.
	find "$DIR" -maxdepth 1 -name 'goldpilot-*.dump' -type f -mtime +"$RETENTION_DAYS" -print -delete | while read -r f; do
		log "supprimée (plus de $RETENTION_DAYS jours) : $(basename "$f")"
	done
}

mkdir -p "$DIR"
if [ "${1:-}" = "once" ]; then  # sauvegarde immédiate (scripts/backup-now.sh)
	do_backup
	exit $?
fi
log "démarrage : une sauvegarde toutes les $INTERVAL_HOURS h, conservation $RETENTION_DAYS jours"
while true; do
	recent=$(find "$DIR" -maxdepth 1 -name 'goldpilot-*.dump' -type f -mmin -$((INTERVAL_HOURS * 60)) | head -n 1)
	if [ -z "$recent" ]; then
		do_backup || true
	fi
	sleep 600
done
