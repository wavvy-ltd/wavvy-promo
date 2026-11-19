"""Tone down an over-exposed cut-out: pull highlights back, restore midtone contrast and a little
saturation, keep alpha untouched. Writes <in>.graded.png next to the input.
    /root/.venvs/audio/bin/python -I tools/grade.py assets/cutout/photo3.clean.png [strength=1.0]
"""
import sys
import numpy as np
from PIL import Image

src = sys.argv[1]
k = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
im = Image.open(src).convert("RGBA")
a = np.asarray(im).astype(np.float32) / 255.0
rgb, alpha = a[..., :3], a[..., 3:]
m = alpha[..., 0] > 0.5
lum = (0.2126 * rgb[..., 0] + 0.7152 * rgb[..., 1] + 0.0722 * rgb[..., 2])
print("before: mean %.3f p50 %.3f p95 %.3f clipped(>0.97) %.1f%%" % (
    lum[m].mean(), np.percentile(lum[m], 50), np.percentile(lum[m], 95), 100 * (lum[m] > 0.97).mean()))

# 1) exposure down ~0.35 stop, 2) highlight shoulder (compress the top end), 3) mild S-curve, 4) +8% saturation
x = rgb * (2 ** (-0.35 * k))
knee = 0.72
over = np.clip(x - knee, 0, None)
x = np.where(x > knee, knee + (1 - knee) * (1 - np.exp(-over / (1 - knee) * 1.4)) / (1 - np.exp(-1.4)), x)
x = np.clip(x, 0, 1)
x = x + 0.10 * k * (x - 0.5) * (1 - np.abs(2 * x - 1))      # midtone contrast
g = (0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2])[..., None]
x = np.clip(g + (x - g) * (1 + 0.08 * k), 0, 1)
l2 = 0.2126 * x[..., 0] + 0.7152 * x[..., 1] + 0.0722 * x[..., 2]
print("after:  mean %.3f p50 %.3f p95 %.3f clipped(>0.97) %.1f%%" % (
    l2[m].mean(), np.percentile(l2[m], 50), np.percentile(l2[m], 95), 100 * (l2[m] > 0.97).mean()))
out = src.replace(".png", ".graded.png")
Image.fromarray((np.concatenate([x, alpha], -1) * 255 + 0.5).astype(np.uint8), "RGBA").save(out)
print("wrote", out)
