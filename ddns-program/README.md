# DDN's Program 🏴

A 4-page, print-ready cut plan (A4, French). Built to be scanned, not read:
every number is findable in a couple of seconds.

**Deliverable:** [`DDNs-Program.pdf`](./DDNs-Program.pdf)

## Contents

| Page | Sections |
|---|---|
| 1 | **01 · Alimentation** — fixed breakfast, day rhythm, the 7-day table (midi / soir / snack), daily totals, cooking rules, whey countdown |
| 2 | **02 · Courses** — tickable shopping list by aisle with prices and weekly total · **03 · Semaine type** — daily non-negotiables and the weekly grid |
| 3 | **04 · Les trois séances** — the full upper-body programme, exercise by exercise, with sets, reps and rest |
| 4 | **05 · Objectifs et pilotage** — target band, month-by-month projection, the 90 kg steering rule, 12-week log |

## The plan in numbers

- Target: **86–88 kg in 2–3 months**, not below, not above. Very lean, maximum muscle
  retained in a deficit — between athletic and muscular.
- **~1,400–1,500 kcal/day, 150–170 g protein.** Same week repeated, no variants to choose.
- **~56 €/week** of groceries (whey already owned: 900 g = exactly 30 days at 1 scoop).
- Training: 3 upper-body sessions (Mon / Thu / Sat), boxing Wednesday, 5,000–10,000 steps daily.

## Notes

- The three sessions are the user's own, transcribed as given. Values he left unspecified
  are filled in as suggestions and marked with a `°`, with a legend at the foot of page 3.
- Prices are Auchan estimates (Q3 2026); halal chicken varies by shop.
- Page 4 carries the steering rule verbatim: from 90 kg, weigh weekly and raise portions
  if the trend threatens to undershoot 86 kg — plus the honest note on the limits of
  building muscle during an aggressive natural deficit.

## Rebuilding the PDF

```bash
cd src
npm i playwright-core
node render.js          # writes DDNs-Program.pdf and prints a per-page fit report
```

Fonts (Inter + JetBrains Mono) are base64-embedded in `src/fonts-embedded.css`, so the
build is fully offline and the output is reproducible.
