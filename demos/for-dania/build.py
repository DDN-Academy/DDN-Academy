#!/usr/bin/env python3
"""
Builds demos/for-dania/index.html from _template.html.

Photos are resized and inlined as base64 so the page is a single self
contained file with no network dependency at all.

To add the song later:
    python3 build.py --audio /path/to/nassini-el-donya.mp3
"""
import argparse, base64, io, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
UPLOADS = "/root/.claude/uploads/42db3c04-3fad-5324-83d5-d0074762da94"

PHOTOS = {
    "beginning": "c5d42d80-IMG_8472.jpeg",
    "shelter":   "ae246ab4-A5447966D4274B39BD7D12733C04AC1E.jpeg",
    "hands":     "eb97a25d-IMG_6187.jpeg",
    "closeness": "0c004bef-IMG_8449.jpeg",
    "final":     "bf940d2f-IMG_6222.jpeg",
}

MAX_W = 1250
QUALITY = 79


def encode_photo(path):
    from PIL import Image, ImageOps
    im = ImageOps.exif_transpose(Image.open(path)).convert("RGB")
    w, h = im.size
    if w > MAX_W:
        im = im.resize((MAX_W, round(h * MAX_W / w)), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, "JPEG", quality=QUALITY, optimize=True, progressive=True)
    raw = buf.getvalue()
    print(f"  {os.path.basename(path):20s} {w}x{h} -> {im.size[0]}x{im.size[1]}  {len(raw)/1024:6.1f} KB")
    return "data:image/jpeg;base64," + base64.b64encode(raw).decode()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--photos", default=UPLOADS, help="directory holding the source photos")
    ap.add_argument("--audio", default=None, help="mp3 to embed as the soundtrack")
    args = ap.parse_args()

    with open(os.path.join(HERE, "_template.html")) as f:
        html = f.read()

    print("photos:")
    for key, fname in PHOTOS.items():
        path = os.path.join(args.photos, fname)
        if not os.path.exists(path):
            sys.exit(f"missing photo: {path}")
        html = html.replace(f"__PHOTO_{key}__", encode_photo(path))

    if args.audio:
        with open(args.audio, "rb") as f:
            raw = f.read()
        ext = os.path.splitext(args.audio)[1].lstrip(".").lower() or "mpeg"
        mime = {"mp3": "mpeg", "m4a": "mp4", "ogg": "ogg", "wav": "wav"}.get(ext, ext)
        print(f"\naudio: {os.path.basename(args.audio)}  {len(raw)/1024/1024:.2f} MB")
        html = html.replace("__AUDIO__", f"data:audio/{mime};base64," + base64.b64encode(raw).decode())
    else:
        print("\naudio: none (page stays silent)")
        html = html.replace("__AUDIO__", "")

    out = os.path.join(HERE, "index.html")
    with open(out, "w") as f:
        f.write(html)
    print(f"\nwrote {out}  {os.path.getsize(out)/1024/1024:.2f} MB")


if __name__ == "__main__":
    main()
