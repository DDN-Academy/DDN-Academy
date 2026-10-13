# SIHEME's Program

A 4-page, print-ready **body-recomposition** plan (A4, French). Same design system as
`../ddns-program` and `../billals-program`, raspberry accent.

**Deliverable:** [`SIHEMEs-Program.pdf`](./SIHEMEs-Program.pdf)

## Profile

22 years old · 1 m 80 · 71 kg · gym 3–4 ×/week · sleeps 6 h/night · cooks very little and
very simply · does not care about the number on the scale.
Stated goals: **abs, thighs, big glutes.**

A Visbody bioimpedance scan was supplied. It is the backbone of the whole document:

| Marker | Value | Reading |
|---|---|---|
| BMI | 22,2 | normal — weight is not the problem |
| Body fat | **30,3 %** (21,5 kg) | the actual problem |
| Trunk fat | **11,29 kg** | more than half the fat mass sits on the trunk |
| Waist-to-hip ratio | **0,94** | fat stored at the waist, not the hips |
| Muscle mass | average | nothing to lose, something to build |

Normal weight with 30 % body fat and an average muscle mass is a **composition** problem,
not a weight problem — so the plan is a recomposition (lose fat, build muscle at the same
time), and page 4 tracks **waist / hips / thigh / body fat**, never kilograms.

## Contents

| Page | Sections |
|---|---|
| 1 | **01 · Alimentation** — fixed no-cook breakfast, fixed 4 p.m. feed, the one rule that applies to every meal, the 7-day table (10-minute lunch / 10-minute dinner), daily totals |
| 2 | **02 · Courses** — tickable shopping list with prices and weekly total · **03 · Semaine type** — weekly grid, the 6 h → 7 h sleep card, slip-ups, why walking and not cardio |
| 3 | **04 · Les quatre séances** — A/B/C/D exercise by exercise, warm-up and load-selection cards |
| 4 | **05 · Objectifs et pilotage** — 30,3 % → 22 % over 16 weeks, month by month, the tape-measure steering rule, 16-week log |

## The plan in numbers

- Mifflin-St Jeor BMR ~1,565 kcal, activity factor ~1,45 → maintenance ~2,270 kcal.
- **~1,900 kcal/day, 135 g protein** (~60 g fat, ~205 g carbs) — a ~370 kcal deficit,
  about **0,4 kg/week**, slow enough to keep (and build) muscle.
- 16 weeks → **−6 kg of fat, +1,5 kg of muscle**, i.e. ~30,3 % → ~22 % body fat.
- **~78 €/week** of groceries, plus ~10 €/week of whey.

## Training design

Four sessions: **glutes three times a week**, quads twice, upper body once.
The hip thrust is exercise #1 in both session A and session D, because it is the one
movement that loads the glutes in their shortened position. Session D is explicitly the
expendable one on a busy week — session A never is.

Loaded obliques (side bends, weighted rotations) are excluded on purpose: with a
waist-to-hip ratio already at 0,94, thickening the waist works against the exact silhouette
she asked for. Abs are trained with cable crunches and hanging leg raises only.

## Notes

- Nutrition is written as instructions, not options — she said she would follow a plan only
  if told exactly what to do. Everything is quantified, the menu is fixed, and Saturday
  dinner is a planned free meal.
- Zero cooking in the morning, zero cooking for two meals a week, and never more than one
  pan for ten minutes otherwise.
- The honest note on page 4 carries two caveats: bioimpedance is accurate to **±3–5 %**
  (only the trend on the same device at the same time of day means anything), and **spot
  reduction does not exist** — no ab exercise burns belly fat; abs appear in a calorie
  deficit. What *is* fully controllable is where muscle is built.
- Prices are supermarket estimates (Q4 2026).

## Rebuilding the PDF

```bash
cd src
npm i playwright-core
node render.js          # writes SIHEMEs-Program.pdf and prints a per-page fit report
```

Fonts (Inter + JetBrains Mono) are base64-embedded in `src/fonts-embedded.css`.
