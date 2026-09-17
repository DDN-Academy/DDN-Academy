# BILLAL's Program

A 4-page, print-ready **lean-bulk** plan (A4, French). Same design system as
`../ddns-program`, blue accent, built for the opposite goal.

**Deliverable:** [`BILLALs-Program.pdf`](./BILLALs-Program.pdf)

## Profile

20 years old · 1 m 88 · **74 kg → 80 kg** · nothing to cut · 3 gym sessions + 1 football
per week · 100 daily push-ups · whey + creatine available.
Weak points: back (no V-taper, "taille tout droit") and general lack of mass.

## Contents

| Page | Sections |
|---|---|
| 1 | **01 · Alimentation** — fixed breakfast, two fixed snacks, the 7-day table (midi / soir), daily totals, how to actually eat 3,400 kcal |
| 2 | **02 · Courses** — tickable shopping list with prices and weekly total · **03 · Semaine type** — daily non-negotiables, weekly grid, push-up rules |
| 3 | **04 · Les trois séances** — full-body ×3 with back priority in all three, exercise by exercise · the V-taper note |
| 4 | **05 · Objectifs et pilotage** — +6 kg over 4 months, month-by-month, the ±0.5 kg/week steering rule, 16-week log |

## The plan in numbers

- Maintenance estimated ~3,000 kcal → **~3,400 kcal/day, 180–190 g protein**
  (~95 g fat, ~470 g carbs). Surplus of ~+400 kcal.
- Target rate **+0.35 to 0.5 kg/week** → 80 kg in about 4 months.
- **~94 €/week** of groceries, plus ~13 €/week for whey (2 scoops/day) and creatine (5 g/day).

## Training design

Full body three times a week rather than a split, because he is a near-beginner and needs
frequency everywhere. **Back appears in all three sessions**, split between width work
(pull-ups, wide pulldowns, straight-arm pull-over) and thickness work (barbell row).
Lateral raises twice a week. Heavy shrugs, loaded obliques and side bends are explicitly
excluded — they thicken the waist and work against the V-taper he is missing.

## Notes

- Projections carry the honest note: muscle gain caps around 0.5–1 kg/month in the first
  year, so +6 kg over 4 months is roughly 4–5 kg of muscle plus 1–2 kg of fat and water.
- Prices are supermarket estimates (Q3 2026).

## Rebuilding the PDF

```bash
cd src
npm i playwright-core
node render.js          # writes BILLALs-Program.pdf and prints a per-page fit report
```

Fonts (Inter + JetBrains Mono) are base64-embedded in `src/fonts-embedded.css`.
