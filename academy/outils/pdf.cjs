#!/usr/bin/env node
/* ---------------------------------------------------------------------------
   pdf.cjs — transforme le HTML d'un chapitre en PDF A4 paginé.

       node academy/outils/pdf.cjs <fichier.html> [<fichier.pdf>]

   Utilise Playwright (navigateur sans interface) pour obtenir un pied de page
   répété sur chaque feuille : matière à gauche, titre au centre, page n/N à droite.
   Si Playwright est absent, academy/outils/make.sh bascule automatiquement sur
   l'impression directe de Chromium (sans numérotation).
--------------------------------------------------------------------------- */
const path = require('path');
const fs = require('fs');
const { chromium } = require('playwright');

const PIED = (gauche, centre) => `
<div style="width:100%;box-sizing:border-box;padding:0 18mm;
            font-family:-apple-system,'Segoe UI',Helvetica,Arial,sans-serif;
            font-size:7.5pt;color:#8c929c;display:flex;justify-content:space-between;align-items:center;">
  <span style="flex:1;text-align:left;">${gauche}</span>
  <span style="flex:2;text-align:center;">${centre}</span>
  <span style="flex:1;text-align:right;"><span class="pageNumber"></span>&nbsp;/&nbsp;<span class="totalPages"></span></span>
</div>`;

(async () => {
  const [source, cible] = process.argv.slice(2);
  if (!source) {
    console.error('usage : node pdf.cjs <fichier.html> [<fichier.pdf>]');
    process.exit(1);
  }
  const html = path.resolve(source);
  if (!fs.existsSync(html)) {
    console.error('Fichier introuvable : ' + html);
    process.exit(1);
  }
  const pdf = path.resolve(cible || html.replace(/\.html?$/i, '') + '.pdf');

  const navigateur = await chromium.launch({ args: ['--no-sandbox', '--disable-dev-shm-usage'] });
  const page = await navigateur.newPage();
  await page.goto('file://' + html, { waitUntil: 'load' });

  const titre = (await page.title()) || '';
  let matiere = '';
  try {
    matiere = await page.$eval('.couverture .matiere', (el) => el.textContent.trim());
  } catch (_) { /* couverture absente : pied de page sans matière */ }

  const echappe = (s) => s.replace(/[&<>]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;' }[c]));

  await page.pdf({
    path: pdf,
    format: 'A4',
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: PIED(echappe(matiere), echappe(titre)),
    margin: { top: '18mm', bottom: '18mm', left: '18mm', right: '18mm' },
  });

  await navigateur.close();
  console.log(pdf);
})().catch((e) => {
  console.error(String((e && e.message) || e));
  process.exit(1);
});
