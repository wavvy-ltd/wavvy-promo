"""Measure the held card in the reference screenshot: white-pixel extent per row -> corner estimates."""
import numpy as np
from PIL import Image
S = '/root/videos/wavvy-whatsnew-poster/assets/ref/hanga.png'
a = np.asarray(Image.open(S).convert('RGB')).astype(float) / 255
r, g, b = a[..., 0], a[..., 1], a[..., 2]
mx, mn = a.max(-1), a.min(-1)
white = (mn > 0.9) & (mx - mn < 0.08)
white[:, :430] = False
white[:440] = False
ys = np.where(white.sum(1) > 40)[0]
print('card y range', ys.min(), ys.max())
for y in list(range(ys.min(), ys.min() + 40, 8)) + list(range(ys.min() + 100, ys.max(), 100)) + list(range(ys.max() - 40, ys.max() + 1, 8)):
    xs = np.where(white[y])[0]
    if len(xs):
        print(y, xs.min(), xs.max())
# leftmost / rightmost white columns and their rows
cols = np.where(white.any(0))[0]
for x in (cols.min(), cols.min() + 5, cols.max() - 5, cols.max()):
    yy = np.where(white[:, x])[0]
    print('x', x, 'y', yy.min(), yy.max())
