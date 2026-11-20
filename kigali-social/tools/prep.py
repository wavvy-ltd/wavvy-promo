"""Grade + crop the picked Kigali photos for each post.
Grade: lift shadows (the subject is backlit), slight warmth to offset the blue cast, mild contrast.
    /root/.venvs/audio/bin/python -I tools/prep.py
"""
import os
import numpy as np
from PIL import Image, ImageOps

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
os.makedirs("assets", exist_ok=True)

# name: (source, out W, out H, focus x 0-1, focus y 0-1, shadow lift, warmth)
JOBS = {
    "feed":     ("DSC01567", 1080, 1350, 0.45, 0.53, 0.85, 0.07),
    "story":    ("DSC01568", 1080, 1920, 0.45, 0.50, 0.85, 0.07),
    "wide":     ("DSC01559", 1200, 675, 0.50, 0.50, 0.85, 0.07),
    "square":   ("DSC01553", 1080, 1080, 0.43, 0.48, 0.12, 0.03),
    "summit1":  ("DSC01551", 1080, 1350, 0.42, 0.50, 0.18, 0.00),
    "summit2":  ("DSC01545", 1080, 1350, 0.45, 0.50, 0.18, 0.00),
    "summit3":  ("DSC01547", 1080, 1350, 0.55, 0.55, 0.18, 0.00),
}


def grade(a, lift, warm):
    lum = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]
    gain = 1 + lift * (1 - np.clip(lum / 0.32, 0, 1)) ** 1.5        # brighten deep shadows only
    a = np.clip(a * gain[..., None], 0, 1)
    w = warm * (1 - lum)[..., None]                                   # warm the darks, keep the sky
    a = a * (1 + w * np.array([1.0, 0.35, -0.6]))
    a = np.clip(a, 0, 1)
    a = a + 0.06 * (a - 0.5) * (1 - np.abs(2 * a - 1))               # gentle midtone contrast
    return np.clip(a, 0, 1)


for name, (src, W, H, fx, fy, lift, warm) in JOBS.items():
    im = ImageOps.exif_transpose(Image.open("src/%s.JPG" % src)).convert("RGB")
    r = W / H
    iw, ih = im.size
    cw, ch = (ih * r, ih) if iw / ih > r else (iw, iw / r)
    x0 = min(max(fx * iw - cw / 2, 0), iw - cw)
    y0 = min(max(fy * ih - ch / 2, 0), ih - ch)
    im = im.crop((round(x0), round(y0), round(x0 + cw), round(y0 + ch))).resize((W * 2, H * 2), Image.LANCZOS)
    a = grade(np.asarray(im).astype(np.float32) / 255, lift, warm)
    Image.fromarray((a * 255 + 0.5).astype(np.uint8)).save("assets/%s.jpg" % name, quality=90)
    print(name, src, im.size)
