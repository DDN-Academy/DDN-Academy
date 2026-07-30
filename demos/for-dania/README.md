# For Dania

A single page, seven chapters, one answer at the end.

## How it is put together

| File | What it is |
| --- | --- |
| `_template.html` | The whole page: markup, styles, animation. Photos and audio are placeholders. |
| `build.py` | Inlines the photos (resized, base64) and optionally the song, and writes `index.html`. |
| `index.html` | The built page. Not committed, because it embeds private photographs. |

Everything is self contained: no fonts, scripts, or images are fetched over the
network, so the page works offline and from a plain file path.

## Building it

```bash
python3 build.py                                   # photos only, silent page
python3 build.py --audio ~/nassini-el-donya.mp3    # with the soundtrack
```

`--photos DIR` points at the folder holding the source images. The five
filenames it expects are listed at the top of `build.py`.

## The way through

The page opens on a date lock. The right day and month opens it; the year is
ignored, and a hint appears after the first wrong answer, so nobody ends up
locked outside.

Then seven chapters, each with its own colour temperature, and two moments that
need her rather than a click: a light she has to hold for six seconds, and a
button she has to press to ask one more time. Pressing it takes the screen to
full black, builds a heart out of roughly two thousand particles in 3D, and
blows it apart into the last page.

## Notes

- Built mobile first. It is meant to be read at night, alone, on a phone.
- The starfield, the golden dust and the heart are hand written canvas, no
  libraries.
- The page holds no analytics, no storage, and makes no requests.
