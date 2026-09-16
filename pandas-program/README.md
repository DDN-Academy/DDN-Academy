# PANDA's Program 🐼

A 15-page, print-ready plan (A4, English). No recipes — ingredient categories with
recommended amounts, and she cooks whatever she likes from them.

**Deliverable:** [`PANDAs-Program.pdf`](./PANDAs-Program.pdf)

## Contents

| Page | Section |
|---|---|
| 1–2 | Cover · how this works, contents, first three days |
| 3–4 | Why she's stuck · 8 weeks vs 16 weeks, and the numbers |
| 5 | The one-page cheat sheet (made to be a lock screen) |
| 6 | Breakfast (zero cooking) and the two snacks |
| 7–8 | Build your lunch · build your dinner |
| 9 | Shopping list, with Spanish supermarket names |
| 10–11 | The weekly Pilates + steps plan · building glutes and legs |
| 12 | Supplements, sleep, cycle and health notes |
| 13 | The 16-week roadmap and milestones |
| 14 | The 30-day chart and the 16-week measurement log |
| 15 | Read this on the bad days |

## Design notes

- **No recipes.** Every meal is a builder: pick one protein, one carb, vegetables,
  one fat, plus free flavour — each with the exact amount. One-line meal ideas only.
- **No morning cooking.** Breakfast is assembled in two minutes from the fridge.
- **Nothing savoury to carry to class.** At 10:00 it's a fruit or a protein drink.
- **Calorie ramp:** 1,800 in week 1, 1,700 in week 2, then 1,600 from week 3 to the
  end, at 130 g of protein throughout. Page 4 states exactly which three amounts
  change and by how much.
- **Pilates:** she attends whatever slots the studio runs and, for the first month,
  takes the class exactly as taught. The page covers what she controls inside any
  class — spring choice, tempo, variation, effort — rather than asking her to have
  the class changed for her.

## Rebuilding the PDF

Sources live in `src/`. The PDF is rendered from `src/index.html` with headless
Chromium via Playwright; `src/render.js` also reports any page whose content
overflows its A4 frame.

```bash
cd src
npm i playwright-core
node render.js          # writes PANDAs-Program.pdf and prints a per-page fit report
```

Fonts (Fraunces + Inter) are base64-embedded in `src/fonts-embedded.css`, so the
build is fully offline and the output is reproducible.
