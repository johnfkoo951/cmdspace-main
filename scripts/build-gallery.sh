#!/usr/bin/env bash
# Scan /assets/gallery/ for image files, optionally import fresh ones
# from a source folder, then regenerate /data/gallery.json.
#
# Usage:
#   ./scripts/build-gallery.sh                      # rebuild manifest from current files
#   ./scripts/build-gallery.sh /path/to/new-photos  # also import new photos from source
#
# - Accepts .jpg .jpeg .png .heic (converted to JPG)
# - Resizes max dim to 1200px, quality 80 (progressive JPEG)
# - Preserves EXIF rotation
# - Generates sequential filenames: photo-NN.jpg

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
GALLERY="$ROOT/assets/gallery"
MANIFEST="$ROOT/data/gallery.json"
SRC="${1:-}"

mkdir -p "$GALLERY" "$(dirname "$MANIFEST")"

python3 - <<PYEOF
import os, json, glob, shutil, sys
from PIL import Image, ImageOps

GALLERY = "$GALLERY"
MANIFEST = "$MANIFEST"
SRC = "$SRC"
EXTS = ("jpg", "jpeg", "JPG", "JPEG", "png", "PNG", "heic", "HEIC")
MAX_DIM = 1200
QUALITY = 80

# 1. Optionally import new files from SRC into GALLERY (preserve originals there)
if SRC and os.path.isdir(SRC):
    # Number starting after current max
    existing = sorted([f for f in os.listdir(GALLERY) if f.startswith("photo-") and f.endswith(".jpg")])
    start = 0
    if existing:
        try: start = max(int(f.split("-")[1].split(".")[0]) for f in existing)
        except Exception: pass
    new_files = []
    for e in EXTS:
        new_files.extend(glob.glob(os.path.join(SRC, f"*.{e}")))
    new_files = sorted(new_files)
    for i, f in enumerate(new_files, start + 1):
        try:
            im = Image.open(f)
        except Exception as ex:
            print(f"  ⚠️ skip {f}: {ex}")
            continue
        im = ImageOps.exif_transpose(im)
        if im.mode not in ("RGB", "L"): im = im.convert("RGB")
        w, h = im.size
        scale = min(MAX_DIM / max(w, h), 1.0)
        if scale < 1.0: im = im.resize((int(w*scale), int(h*scale)), Image.LANCZOS)
        name = f"photo-{i:02d}.jpg"
        out = os.path.join(GALLERY, name)
        im.save(out, "JPEG", quality=QUALITY, optimize=True, progressive=True)
        print(f"  + imported {name}")

# 2. Scan GALLERY and rebuild manifest
files = []
for e in EXTS + ("jpg",):
    files.extend(glob.glob(os.path.join(GALLERY, f"*.{e}")))
files = sorted(set(files))

manifest = []
for f in files:
    try: im = Image.open(f); w, h = im.size
    except Exception: continue
    name = os.path.basename(f)
    manifest.append({"src": f"/assets/gallery/{name}", "w": w, "h": h, "caption": ""})

with open(MANIFEST, "w") as fh:
    json.dump(manifest, fh, ensure_ascii=False, indent=2)

print(f"✅ {len(manifest)} items → {MANIFEST}")
PYEOF

echo ""
echo "Next: vercel deploy --prod --yes"
