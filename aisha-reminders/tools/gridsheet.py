"""Contact sheet with a 100px grid (900x2000 space) for picking tap/mark coordinates.
    python3 tools/gridsheet.py out.png a.png b.png ...
"""
import sys
from PIL import Image, ImageDraw
out, fs = sys.argv[1], sys.argv[2:]
tiles = []
for f in fs:
    im = Image.open(f).convert("RGB").resize((900, 2000))
    d = ImageDraw.Draw(im)
    for y in range(0, 2000, 100):
        d.line([(0, y), (900, y)], fill=(255, 0, 0) if y % 500 == 0 else (255, 120, 120), width=2)
        d.text((4, y + 2), str(y), fill=(255, 255, 0))
    for x in range(0, 900, 100):
        d.line([(x, 0), (x, 2000)], fill=(0, 200, 255), width=1)
        d.text((x + 3, 30), str(x), fill=(0, 255, 255))
    d.text((300, 4), f.split("/")[-1], fill=(255, 255, 255))
    tiles.append(im.resize((450, 1000)))
W = Image.new("RGB", (450 * len(tiles), 1000))
for i, t in enumerate(tiles):
    W.paste(t, (450 * i, 0))
W.save(out)
