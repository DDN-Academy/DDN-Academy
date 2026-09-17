# BILLAL's Program

A 4-page, print-ready **lean-bulk** plan (A4, French). Same design system as
`../ddns-program`, blue accent, built for the opposite goal.

**Deliverable:** [`BILLALs-Program.pdf`](./BILLALs-Program.pdf)

## Profile

20 years old · 1 m 88 · **74 kg → 80 kg** · nothing to cut · 3 gym sessions + 1 football
per week · 100 daily push-ups · whey + creatine available.
Weak points: back (no V-taper, "taille tout droit") and general lack of mass.
He barely cooks, so every meal is **one pan, ten minutes**: starch in the microwave or a pot,
diced meat in the pan, frozen vegetables thrown into the same pan. Nothing else.

## Contents

| Page | Sections |
|---|---|
| 1 | **01 · Alimentation** — fixed breakfast (a bowl), three fixed no-cook feeds, the 7-day table (10-minute lunch / 10-minute dinner), the method, the Sunday rice batch |
| 2 | **02 · Courses** — tickable shopping list with prices and weekly total · **03 · Semaine type** — daily non-negotiables, weekly grid, push-up rules |
| 3 | **04 · Les trois séances** — full-body ×3 with back priority in all three, exercise by exercise · the V-taper note |
| 4 | **05 · Objectifs et pilotage** — +6 kg over 4 months, month-by-month, the ±0.5 kg/week steering rule, 16-week log |

## The plan in numbers

- Maintenance estimated ~3,000 kcal → **~3,900 kcal/day, 200–210 g protein**
  (~120 g fat, ~500 g carbs). Surplus of ~+900 kcal — the fast mode he asked for.
- Target rate **+0.7 to 0.8 kg/week** → 80 kg in **8–9 weeks**.
- **~131 €/week** of groceries, plus ~13 €/week for whey (2 scoops/day) and creatine (5 g/day).

## Training design

Full body three times a week rather than a split, because he is a near-beginner and needs
frequency everywhere. **Back appears in all three sessions**, split between width work
(pull-ups, wide pulldowns, straight-arm pull-over) and thickness work (barbell row).
Lateral raises twice a week. Heavy shrugs, loaded obliques and side bends are explicitly
excluded — they thicken the waist and work against the V-taper he is missing.

## Notes

- Projections carry the honest note: at +0.75 kg/week, roughly 2.5–3 kg of the 6 kg is muscle
  and 3–3.5 kg is fat and water. The same +6 kg spread over 4 months would be 4–5 kg of muscle —
  speed costs ratio, and the page says so. Starting at BMI 20.9, the extra fat is not a problem.
- Prices are supermarket estimates (Q3 2026).

## Rebuilding the PDF

```bash
cd src
npm i playwright-core
node render.js          # writes BILLALs-Program.pdf and prints a per-page fit report
```

Fonts (Inter + JetBrains Mono) are base64-embedded in `src/fonts-embedded.css`.
