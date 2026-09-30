#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# publier.sh — publie un document du semestre.
#
#     Semestre1/outils/publier.sh Semestre1/Economie/Cours/Economie_Ch01_Introduction_generale.md
#
# Pour tout fichier .md : produit le PDF A4 paginé à côté du .md.
# Pour un cours (dossier Cours/) : produit en plus, par extraction
#   - Anki/<cours>.csv                  cartes Anki — seulement pour les cours au format avec cartes
#                                       (jusqu'au 29 septembre 2026 ; décision 13 : plus de cartes)
#   - Fiches/<cours>_Fiche.md + .pdf    fiche de synthèse + questions pour la marche
#   - Fiches/<Matiere>_Formulaire.md + .pdf   formulaire cumulatif de la matière
#   - GLOSSAIRE.md + .pdf               glossaire cumulatif, toutes matières
# Une seule source de vérité : le cours. Tout le reste en est dérivé.
# ---------------------------------------------------------------------------
set -euo pipefail
ici="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source_md="${1:-}"
[ -n "$source_md" ] || { echo "usage : publier.sh <fichier.md>" >&2; exit 1; }

pdf_de() {                                   # $1 = .md  -> .pdf à côté
  local md="$1" tmp html pdf
  tmp="$(mktemp -d)"
  html="$tmp/$(basename "${md%.md}").html"
  pdf="${md%.md}.pdf"
  python3 "$ici/build.py" "$md" -o "$html" >/dev/null
  export NODE_PATH="${NODE_PATH:-$(npm root -g 2>/dev/null || echo '')}"
  if node "$ici/pdf.cjs" "$html" "$pdf" >/dev/null 2>&1; then
    echo "PDF  : $pdf"
  else
    "${PLAYWRIGHT_BROWSERS_PATH:-/opt/pw-browsers}/chromium" --headless --disable-gpu --no-sandbox \
      --no-pdf-header-footer --print-to-pdf="$pdf" "$html" >/dev/null 2>&1 \
      && echo "PDF  : $pdf  (repli Chromium, sans numérotation)" \
      || { echo "PDF non généré pour $md" >&2; return 1; }
  fi
  rm -rf "$tmp"
}

python3 "$ici/verifier.py" "$source_md"
pdf_de "$source_md"

case "$source_md" in
  */Cours/*.md)
    python3 "$ici/extraire.py" "$source_md" | while read -r derive; do
      echo "Dérivé : $derive"
      case "$derive" in *.md) pdf_de "$derive" ;; esac
    done
    ;;
esac
