#!/usr/bin/env python3
"""Write labelled placeholder screens and a placeholder logo so the starter renders before you
have real captures. Pure Python (no Pillow). Replace every file it writes with real captures.

    python3 scripts/placeholders.py            # 1440x3120 phone screens listed in storyboard.json
"""
import json, os, struct, sys, zlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def png(path, w, h, paint):
    rows = bytearray()
    for y in range(h):
        rows.append(0)
        for x in range(w):
            rows += bytes(paint(x, y))
    def chunk(t, d):
        return struct.pack(">I", len(d)) + t + d + struct.pack(">I", zlib.crc32(t + d) & 0xFFFFFFFF)
    data = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 8, 2, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(bytes(rows), 6)) + chunk(b"IEND", b"")
    with open(path, "wb") as f:
        f.write(data)


def hexrgb(s):
    s = s.lstrip("#"); return tuple(int(s[i:i + 2], 16) for i in (0, 2, 4))


def screen(path, ground, surface, accent, seed):
    W, H = 1440, 3120
    g, s, a = hexrgb(ground), hexrgb(surface), hexrgb(accent)
    # a status bar, an app bar, a hero card, and a column of list cards — enough to look like an app
    cards = [(120, 520 + i * 420, 1320, 520 + i * 420 + 330) for i in range(5)]
    def paint(x, y):
        if y < 130: return g
        if 130 <= y < 330: return s
        if 400 <= y < 440 and 90 <= x < 90 + 400 + (seed * 90) % 500: return a
        for i, (x0, y0, x1, y1) in enumerate(cards):
            if x0 <= x < x1 and y0 <= y < y1:
                if x0 + 40 <= x < x0 + 160 and y0 + 100 <= y < y0 + 220: return a
                if x0 + 200 <= x < x0 + 200 + 300 + ((seed + i) * 137) % 500 and y0 + 110 <= y < y0 + 150: return (120, 120, 130)
                return s
        if y >= H - 230: return s
        return g
    png(path, W, H, paint)


def logo(path, accent):
    a = hexrgb(accent)
    def paint(x, y):
        r = ((x - 256) ** 2 + (y - 256) ** 2) ** 0.5
        if r < 200: return a if abs(x - 256) < 60 or abs(y - 256) < 60 else (255, 255, 255)
        return (255, 255, 255)
    png(path, 512, 512, paint)


if __name__ == "__main__":
    sb = json.load(open(os.path.join(ROOT, "storyboard.json")))
    c = sb["brand"]["colors"]
    names = set()
    for sc in sb["scenes"]:
        for s in sc.get("screens", []): names.add(s)
        for m in sc.get("moves", []):
            if m.get("kind") == "overlay": names.add(m["src"])
    os.makedirs(os.path.join(ROOT, "assets/screens"), exist_ok=True)
    for i, n in enumerate(sorted(names)):
        p = os.path.join(ROOT, "assets/screens", n)
        if os.path.exists(p):
            print("keep   ", n); continue
        screen(p, c["ground"], c["surface"], c["accent"], i); print("wrote  ", n)
    lp = os.path.join(ROOT, sb["brand"]["logo"])
    if not os.path.exists(lp):
        logo(lp, c["accent"]); print("wrote  ", sb["brand"]["logo"])
