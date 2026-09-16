# PANDA's Program 🐼

A 33-page, print-ready lifestyle & nutrition plan (A4, English).

**Deliverable:** [`PANDAs-Program.pdf`](./PANDAs-Program.pdf)

## Contents

| Pages | Section |
|---|---|
| 1 | Cover |
| 2–4 | Diagnosis, targets, the seven rules |
| 5–6 | Daily timeline, how a day adds up, Phase 1 → Phase 2 |
| 7–17 | Menus: 6 breakfasts, 6 mid-morning snacks, 8 lunches, 8 dinners, snacks, 3 sample days |
| 18 | Protein cheat sheet |
| 19–21 | Shopping list (Spanish supermarket names), flavour kit, halal sourcing in Madrid |
| 22–23 | Pilates and steps |
| 24–26 | Supplements, energy & sleep, health notes |
| 27–28 | 16-week roadmap, progress tracking |
| 29–31 | Troubleshooting, eating out in Madrid |
| 32–33 | Printable weekly tracker, closing note |

## Rebuilding the PDF

Sources live in `src/`. The PDF is rendered from `src/index.html` with headless Chromium
via Playwright; `src/render.js` also reports any page whose content overflows its A4 frame.

```bash
cd src
npm i playwright-core
node render.js          # writes PANDAs-Program.pdf and prints a per-page fit report
```

Fonts (Fraunces + Inter) are base64-embedded in `src/fonts-embedded.css`, so the build
is fully offline and the output is reproducible.
