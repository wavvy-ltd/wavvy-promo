"""Find chat bubbles in 900x2000 screenshots: Aisha's grey bubbles and the user's green ones.
    python3 tools/bubbles.py assets/screens/aisha/*.png
"""
import sys
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

for f in sys.argv[1:]:
    a = np.asarray(Image.open(f).convert("RGB")).astype(int)
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    grey = (abs(r - g) < 6) & (abs(g - b) < 8) & (r > 36) & (r < 56)
    green = (g > 180) & (r > 90) & (r < 160) & (b < 150) & (g - r > 60)
    purple = (b > 170) & (r > 150) & (g < 190) & (b - g > 20)
    out = []
    for name, m in (("aisha", grey), ("user", green | purple)):
        m = m.copy(); m[:280] = False; m[1780:] = False
        m = ndi.binary_opening(m, iterations=3)
        lab, n = ndi.label(m)
        for sl in ndi.find_objects(lab):
            y0, y1, x0, x1 = sl[0].start, sl[0].stop, sl[1].start, sl[1].stop
            if (x1 - x0) > 200 and (y1 - y0) > 50:
                out.append((y0, name, [x0, y0, x1, y1]))
    print(f.split("/")[-1], " ".join("%s%s" % (n, b) for _, n, b in sorted(out)))
