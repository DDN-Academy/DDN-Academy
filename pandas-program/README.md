# PANDA's Program 🐼

A 33-page, print-ready lifestyle & nutrition plan (A4, English).

**Deliverable:** [`PANDAs-Program.pdf`](./PANDAs-Program.pdf)

## Contents

Colour-coded sections, with a generated table of contents on page 2.

| Pages | Section |
|---|---|
| 1–2 | Cover, contents |
| 3–4 | How to use this book · your first three days |
| 5–7 | Why this works · your numbers · your seven promises |
| 8–10 | The one-page cheat sheet · the weekday hour by hour · how a day adds up |
| 11–21 | Menus: 6 breakfasts, 6 snacks, 8 lunches, 8 dinners, sweet fixes, 3 sample days |
| 22 | Protein cheat sheet |
| 23–25 | Shopping list (Spanish names) · flavour kit · halal sourcing in Madrid |
| 26–27 | Pilates · steps |
| 28–30 | Supplements · energy, sleep & water · health notes |
| 31–33 | The 16-week roadmap · tracking · milestones and rewards |
| 34–36 | Troubleshooting · eating out in Madrid |
| 37–39 | 30-day starter chart · weekly tracker · read this on the bad days |

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
