# SIHEME's Program

A 4-page, print-ready **lean-bulk** plan (A4, French). Same design system as
`../ddns-program` and `../billals-program`, raspberry accent.

**Deliverable:** [`SIHEMEs-Program.pdf`](./SIHEMEs-Program.pdf)

## Profile

22 years old · 1 m 80 · 71 kg · gym 3–4 ×/week · sleeps 6 h/night · cooks very little and
very simply · does not care about the number on the scale.
Stated goals: **big glutes, big thighs, abs** — thin frame, nothing to cut.

**Goal: gain mass, with as little fat as possible.** She has no fat to lose; what she is
missing is muscle, in the glutes and quads first.

A Visbody bioimpedance scan was supplied (BMI 22,2 · 30,3 % body fat · 11,29 kg trunk fat ·
waist-to-hip 0,94 · **muscle mass only average**). The only line that drives this program is
the last one. The 30,3 % reading is treated as what it is — a bioimpedance estimate accurate
to ±3–5 % that reads high on an under-muscled body — and the document says so rather than
steering by it.

## Contents

| Page | Sections |
|---|---|
| 1 | **01 · Alimentation** — fixed no-cook breakfast, fixed 4 p.m. feed, the rule that applies to every meal, the 7-day table (10-minute lunch / 10-minute dinner), daily totals, what to do on days with no appetite |
| 2 | **02 · Courses** — tickable shopping list with prices and weekly total · **03 · Semaine type** — weekly grid, sleep, the skipped-meal risk, no extra cardio |
| 3 | **04 · Les quatre séances** — A/B/C/D exercise by exercise, warm-up and load-selection cards |
| 4 | **05 · Objectifs et pilotage** — 71 → 75 kg over 16 weeks, month by month, the +0,25 kg/week steering rule, 16-week log |

## The plan in numbers

- Mifflin-St Jeor BMR ~1,565 kcal, activity factor ~1,45 → maintenance ~2,270–2,350 kcal.
- **~2,600 kcal/day, 150 g protein** (~75 g fat, ~340 g carbs) — a deliberately small
  surplus of ~+250 to 300 kcal.
- Target rate **+0,2 to 0,3 kg/week** → **71 → 75 kg in 16 weeks**, of which ~2 to 2,5 kg
  is muscle.
- **~102 €/week** of groceries, plus ~10 €/week of whey.

## Training design

Four sessions: **glutes three times a week**, quads twice, upper body once.
The hip thrust is exercise #1 in both session A and session D, because it is the one
movement that loads the glutes in their shortened position. Session D is explicitly the
expendable one on a busy week — session A never is. Progressive overload on the first three
exercises of every session is stated as the whole point of the program.

Loaded obliques (side bends, weighted rotations) are excluded on purpose: a thicker waist
flattens the contrast the glutes are being built for. Abs are trained (cable crunch, hanging
leg raise) but the document is explicit that they will show after a later cut, not during a
bulk. No running, HIIT or classes for these four months — they burn the surplus and fatigue
the legs.

## Notes

- Nutrition is written as instructions, not options — she said she would follow a plan only
  if told exactly what to do. Everything is quantified and the weekly menu is fixed, with
  Saturday dinner as a planned free meal.
- Zero cooking in the morning, zero cooking for two meals a week, one pan for ten minutes
  otherwise.
- The honest note on page 4: muscle grows at **0,5–0,7 kg/month** for a beginner and less
  afterwards, so eating more than planned adds fat, not muscle. +4 kg in 16 weeks with
  ~2,5 kg of it muscle is the realistic ceiling. The single anti-fat guardrail is the waist
  measurement, not a deficit.
- Prices are supermarket estimates (Q4 2026).

## Rebuilding the PDF

```bash
cd src
npm i playwright-core
node render.js          # writes SIHEMEs-Program.pdf and prints a per-page fit report
```

Fonts (Inter + JetBrains Mono) are base64-embedded in `src/fonts-embedded.css`.
