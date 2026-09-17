# DDN's Program 🏴

A 3-page, print-ready cut plan (A4, French). Built to be scanned, not read:
every number is findable in a couple of seconds.

**Deliverable:** [`DDNs-Program.pdf`](./DDNs-Program.pdf)

## Contents

| Page | Sections |
|---|---|
| 1 | **01 · Alimentation** — fixed breakfast, day rhythm, the 7-day table (midi / soir / snack), daily totals, cooking rules |
| 2 | **02 · Courses** — tickable shopping list by aisle with prices and weekly total · **03 · Programme physique** — daily non-negotiables and the weekly training grid |
| 3 | **04 · Objectifs** — projection bar and month-by-month targets · **05 · Suivi** — 12-week log |

## Notes

- The upper-body lifting programme is deliberately not detailed — the user already has it.
- Prices are Auchan estimates (Q3 2026); halal chicken varies by shop.
- Projections carry the disclaimer requested: constant-deficit estimates, real loss
  varies with metabolic adaptation, adherence and individual factors.

## Rebuilding the PDF

```bash
cd src
npm i playwright-core
node render.js          # writes DDNs-Program.pdf and prints a per-page fit report
```

Fonts (Inter + JetBrains Mono) are base64-embedded in `src/fonts-embedded.css`, so the
build is fully offline and the output is reproducible.
