"""Cut the two B&W hands out of the reference poster -> assets/hands.png (RGBA, same size as the ref).

Outside the card the background is saturated navy and the hands are greyscale, so alpha comes from
saturation (chroma key) and the colour is replaced by luminance (kills the navy fringe). Over the card
(the left thumb, the right fingers) alpha comes from darkness against the white card, with holes
filled so bright nails stay opaque. Only the two big hand blobs are kept.
"""
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

ROOT = '/root/videos/wavvy-whatsnew-poster/'
a = np.asarray(Image.open(ROOT + 'assets/ref/hanga.png').convert('RGB')).astype(np.float32) / 255
H, W = a.shape[:2]
mx, mn = a.max(-1), a.min(-1)
sat = (mx - mn) / np.maximum(mx, 1e-4)
lum = 0.2126 * a[..., 0] + 0.7152 * a[..., 1] + 0.0722 * a[..., 2]

card = np.array([(570, 469), (1260, 540), (1148, 1612), (458, 1541)], np.float32)
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
in_card = np.ones((H, W), bool)
for i in range(4):
    (x1, y1), (x2, y2) = card[i], card[(i + 1) % 4]
    in_card &= ((x2 - x1) * (yy - y1) - (y2 - y1) * (xx - x1)) >= 0

key = np.clip((0.42 - sat) / 0.30, 0, 1)
left = (xx < 640) & (yy > 820) & (yy < 1345)
right = (xx > 990) & (yy > 1310)
zone_thumb = left & in_card & (xx < 620) & (yy < 1060)
zone_fing = right & in_card & (xx > 1030)

# on-card parts: binary darker-than-card mask, holes filled (nails), then soft edge from luminance
oncard = (zone_thumb | zone_fing) & (lum < 0.86) & (sat < 0.25)
oncard = ndi.binary_opening(oncard, iterations=2)
oncard = ndi.binary_fill_holes(oncard)
soft = np.clip((0.97 - lum) / 0.15, 0, 1)
oncard_a = np.where(ndi.binary_erosion(oncard, iterations=2), 1.0, oncard * soft)
oncard_a = np.maximum(oncard_a, ndi.binary_dilation(oncard, iterations=1) * soft * (zone_thumb | zone_fing))

alpha = np.where((left | right) & ~in_card, key, 0.0)
# the card's own light edge/shadow just outside the polygon is not hand
ring = ndi.binary_dilation(in_card, iterations=12) & ~in_card
alpha = np.where(ring & (lum > 0.5), 0.0, alpha)
alpha = np.maximum(alpha, oncard_a)
# fill holes in the whole hand too (bright knuckle highlights), then keep only the big blobs
solid = ndi.binary_fill_holes(alpha > 0.5)
alpha = np.where(solid & (alpha < 0.5) & ndi.binary_erosion(solid, iterations=3), 1.0, alpha)
lab, n = ndi.label(alpha > 0.35)
sizes = ndi.sum(np.ones_like(lab), lab, range(1, n + 1))
keep = np.isin(lab, [i + 1 for i, s in enumerate(sizes) if s > 15000])
keep = ndi.binary_dilation(keep, iterations=3)
alpha = alpha * keep
# fade the cropped bottom of the left hand into the background
fade = np.clip((1345 - yy) / 60, 0, 1)
alpha = np.where(left & ~in_card, alpha * fade, alpha)

alpha = np.where((yy > 1596) & (xx < 1185), 0.0, alpha)   # screenshot's bottom bar
g = np.clip(lum, 0, 1)
out = np.dstack([g, g, g, alpha])
Image.fromarray((out * 255 + 0.5).astype(np.uint8), 'RGBA').save(ROOT + 'assets/hands.png')
print('blobs kept', int((sizes > 15000).sum()), 'of', n)
