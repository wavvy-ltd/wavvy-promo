"""Remove the dark fringe a cut-out keeps from a dark background (trees, hair shadow).
Shrinks the alpha by ERODE px, then replaces the colour of every soft-edge pixel with the
colour of the nearest solid foreground, so no background colour bleeds into the edge.
    /root/.venvs/rembg/bin/python -I tools/defringe.py assets/cutout/photo3.png [erode=2]
Writes <name>.clean.png next to the input.
"""
import sys
import cv2
import numpy as np

src = sys.argv[1]
erode = int(sys.argv[2]) if len(sys.argv) > 2 else 2
im = cv2.imread(src, cv2.IMREAD_UNCHANGED).astype(np.float32)
rgb, a = im[..., :3], im[..., 3] / 255.0

k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * erode + 1, 2 * erode + 1))
a2 = cv2.erode(a, k)
a2 = cv2.GaussianBlur(a2, (0, 0), 0.7)

# solid interior = well inside the original matte
solid = (cv2.erode(a, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * erode + 5, 2 * erode + 5))) > 0.98).astype(np.float32)
fill = rgb.copy()
acc = np.zeros_like(rgb); w = np.zeros_like(a)
for s in (2, 4, 8, 16, 32):          # multi-scale normalised blur = colour of nearby solid pixels
    b = cv2.GaussianBlur(rgb * solid[..., None], (0, 0), s)
    m = cv2.GaussianBlur(solid, (0, 0), s)
    take = (w < 1e-3) & (m > 1e-3)
    acc[take] = b[take] / m[take][:, None]
    w[take] = 1
edge = (solid < 0.5) & (w > 0)
fill[edge] = acc[edge]

out = np.dstack([fill, a2 * 255]).clip(0, 255).astype(np.uint8)
dst = src.rsplit(".", 1)[0] + ".clean.png"
cv2.imwrite(dst, out)
print(dst, out.shape)
