# DDN's Program 🏴

A 3-page, print-ready cut-then-recomposition plan (A4, French). Built to be scanned, not read:
every number is findable in a couple of seconds.

**Deliverable:** [`DDNs-Program.pdf`](./DDNs-Program.pdf)

## Contents

| Page | Sections |
|---|---|
| 1 | **01 · Alimentation** — fixed breakfast, fixed afternoon snack, the 7-day table (midi / soir), daily totals, why the calories are where they are |
| 2 | **02 · Courses** — tickable shopping list by aisle with prices and weekly total · **03 · Programme physique** — daily non-negotiables, weekly training grid, and the rules that make it build volume |
| 3 | **04 · Objectifs** — two phases (cut to 86–88 kg, then recomposition at that weight), the 86 kg floor · **05 · Suivi** — 16-week log |

## The plan in numbers

- Target: **86–88 kg and no lower**, at roughly **10 % body fat** — lean with real volume.
- Estimated maintenance ~3,200–3,400 kcal. Phase 1 runs at **~2,500 kcal with 185–200 g protein**
  (≈ −0.7 kg/week), phase 2 at **~2,900 kcal** with weight held steady.
- Phase 1: months 1–4, 97 → 86–88 kg, ~23 % → ~14 % body fat.
- Phase 2: months 5–9, weight unchanged, ~14 % → ~10 % body fat.

## Notes

- The lifting programme itself is deliberately not detailed — the user already has it. The document
  only fixes the split (2 upper + **1 mandatory leg day**) and the loading rules.
- Prices are Auchan estimates (Q3 2026); halal chicken varies by shop.
- Projections carry the disclaimer requested: constant-deficit estimates from an assumed ~23 %
  starting body fat; real loss varies with metabolic adaptation, adherence, sleep and genetics.

## Rebuilding the PDF

```bash
cd src
npm i playwright-core
node render.js          # writes DDNs-Program.pdf and prints a per-page fit report
```

Fonts (Inter + JetBrains Mono) are base64-embedded in `src/fonts-embedded.css`, so the
build is fully offline and the output is reproducible.
