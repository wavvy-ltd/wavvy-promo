#!/usr/bin/env python3
"""Build the Wavvy Wallet x partner blog images (1080x1350, white).

Run from the repo root:  python3 partner-logos/tools/build.py
Needs Pillow + numpy, and rsvg-convert for the Plug In Ventures SVG.
"""
import subprocess
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
SRC, OUT = ROOT / "sources", ROOT / "posts"
W, H = 1080, 1350
RULE, CROSS = (200, 200, 200), (140, 140, 140)


def flatten(im):
    im = im.convert("RGBA")
    bg = Image.new("RGBA", im.size, (255, 255, 255, 255))
    bg.alpha_composite(im)
    return bg.convert("RGB")


def fit(im, w):
    return im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)


def wavvy():
    # Wavvy mark + wordmark: left part of the existing blog image (wavvy-x-nvidia-2.png).
    return flatten(Image.open(SRC / "wavvy-x-nvidia-2.png").crop((-14, 155, 822, 845)))


def asu():
    # Edson E+I logo: top of the funding-page JPG, without the "Pay it Forward" box.
    return Image.open(SRC / "asu-edson-venture-devils-pay-it-forward.jpg").convert("RGB").crop((59, 66, 505, 203))


def plug_in_ventures(width):
    png = OUT / ".piv.png"
    subprocess.run(["rsvg-convert", "-w", str(width), "-b", "white",
                    str(SRC / "plug-in-ventures-logo-black.svg"), "-o", str(png)], check=True)
    im = Image.open(png).convert("RGB")
    png.unlink()
    return im


def cross(d, cx, cy, horizontal_rules, s=14):
    d.line((cx - s, cy - s, cx + s, cy + s), fill=CROSS, width=5)
    d.line((cx - s, cy + s, cx + s, cy - s), fill=CROSS, width=5)
    if horizontal_rules:
        d.line((cx - 260, cy, cx - 40, cy), fill=RULE, width=3)
        d.line((cx + 40, cy, cx + 260, cy), fill=RULE, width=3)
    else:
        d.line((cx, cy - 150, cx, cy - 45), fill=RULE, width=3)
        d.line((cx, cy + 45, cx, cy + 150), fill=RULE, width=3)


def side_by_side(right, name, margin=40, gap=120):
    lw = W - 2 * margin - gap - right.width
    left = fit(wavvy(), lw)
    c = Image.new("RGB", (W, H), "white")
    cy = H // 2
    c.paste(left, (margin, cy - left.height // 2))
    cross(ImageDraw.Draw(c), margin + lw + gap // 2, cy, horizontal_rules=False)
    c.paste(right, (margin + lw + gap, cy - right.height // 2))
    c.save(OUT / name)
    print(OUT / name)


def stacked(bottom, name, top_width=560, gap=110):
    top = fit(wavvy(), top_width)
    c = Image.new("RGB", (W, H), "white")
    y = (H - top.height - gap - bottom.height) // 2
    c.paste(top, ((W - top.width) // 2, y))
    cross(ImageDraw.Draw(c), W // 2, y + top.height + gap // 2, horizontal_rules=True, s=16)
    c.paste(bottom, ((W - bottom.width) // 2, y + top.height + gap))
    c.save(OUT / name)
    print(OUT / name)


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    sharpen = ImageFilter.UnsharpMask(2, 60, 2)  # the ASU source is only 564 px wide
    side_by_side(fit(asu(), 560).filter(sharpen), "wavvy-x-asu-edson.png", margin=50, gap=90)
    stacked(fit(asu(), 860).filter(sharpen), "wavvy-x-asu-edson-stacked.png")
    side_by_side(plug_in_ventures(560), "wavvy-x-plug-in-ventures.png")
