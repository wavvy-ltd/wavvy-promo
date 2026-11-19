"""Remove the background from the album photos -> assets/cutout/photoN.png (RGBA, trimmed).
    /root/.venvs/rembg/bin/python -I tools/cutout.py [model]
"""
import os, sys
from PIL import Image
from rembg import new_session, remove

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model = sys.argv[1] if len(sys.argv) > 1 else "birefnet-general"
s = new_session(model)
os.makedirs(os.path.join(ROOT, "assets/cutout"), exist_ok=True)
for n in ("photo1", "photo2"):
    im = Image.open(os.path.join(ROOT, "assets/album", n + ".jpg")).convert("RGB")
    out = remove(im, session=s, post_process_mask=True)
    out = out.crop(out.getbbox())
    p = os.path.join(ROOT, "assets/cutout", n + ".png")
    out.save(p)
    print(n, model, out.size, flush=True)
