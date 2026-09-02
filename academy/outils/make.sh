#!/usr/bin/env bash
# ---------------------------------------------------------------------------
# make.sh — un chapitre Markdown -> HTML autonome + PDF A4 paginé.
#
#     academy/outils/make.sh academy/chapitres/micro-ch1.md
#
# Produit academy/export/micro-ch1.html et academy/export/micro-ch1.pdf
# ---------------------------------------------------------------------------
set -euo pipefail

ici="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source_md="${1:-}"

if [ -z "$source_md" ]; then
  echo "usage : academy/outils/make.sh <chapitre.md> [sortie.html]" >&2
  exit 1
fi

html="$(python3 "$ici/build.py" "$source_md" ${2:+-o "$2"})"
echo "HTML : $html"

pdf="${html%.html}.pdf"

# 1) voie principale : Playwright (pied de page numéroté)
if command -v node >/dev/null 2>&1; then
  export NODE_PATH="${NODE_PATH:-$(npm root -g 2>/dev/null || echo '')}"
  if node "$ici/pdf.cjs" "$html" "$pdf" >/dev/null 2>&1; then
    echo "PDF  : $pdf"
    exit 0
  fi
fi

# 2) repli : impression directe par Chromium (sans numérotation de page)
for c in "${PLAYWRIGHT_BROWSERS_PATH:-/opt/pw-browsers}/chromium" \
         /opt/pw-browsers/chromium \
         "$(command -v chromium || true)" \
         "$(command -v chromium-browser || true)" \
         "$(command -v google-chrome || true)"; do
  if [ -n "$c" ] && [ -x "$c" ]; then
    if "$c" --headless --disable-gpu --no-sandbox --no-pdf-header-footer \
            --print-to-pdf="$pdf" "$html" >/dev/null 2>&1; then
      echo "PDF  : $pdf  (repli Chromium : pas de numérotation de page)"
      exit 0
    fi
  fi
done

echo "PDF non généré. Ouvrez $html dans un navigateur puis Ctrl/Cmd + P → « Enregistrer en PDF »." >&2
