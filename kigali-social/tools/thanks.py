"""'Thank you, Africa Fintech Summit' posts (1080x1350, exported 2x) from the founders' summit photos.
    /root/.venvs/rembg/bin/python -I tools/thanks.py
"""
import os, subprocess
from PIL import Image, ImageOps, ImageEnhance

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
SRC = "/root/videos/wavvy-social/assets/extra"
V = "/root/videos/wavvy-whats-new/assets"
os.makedirs("assets", exist_ok=True); os.makedirs("html", exist_ok=True); os.makedirs("posts", exist_ok=True)

# name -> (photo, crop box as fractions x1,y1,x2,y2 ; photo area is 1080x980 -> aspect 1.102)
POSTS = {
    "06-thanks-afs-a": ("MRPC9208", (0.215, 0.10, 0.827, 0.955)),
    "06-thanks-afs-b": ("MRPC9279", (0.205, 0.14, 0.817, 0.995)),
}
PH = 980

for name, (src, (x1, y1, x2, y2)) in POSTS.items():
    im = ImageOps.exif_transpose(Image.open(os.path.join(SRC, src + ".jpg"))).convert("RGB")
    W, H = im.size
    c = im.crop((int(x1 * W), int(y1 * H), int(x2 * W), int(y2 * H))).resize((2160, PH * 2), Image.LANCZOS)
    c = ImageEnhance.Color(c).enhance(0.9)          # tame the orange/purple room light a little
    c.save("assets/%s.jpg" % name, quality=92)

CSS = """
@font-face { font-family: 'Nunito'; src: url('%s/fonts/Nunito.ttf') format('truetype'); font-weight: 200 1000; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 1080px; height: 1350px; overflow: hidden; font-family: 'Nunito', sans-serif; background: #FFFFFF; color: #111111; }
.photo { position: absolute; left: 0; top: 0; width: 1080px; height: %dpx; background-size: cover; background-position: center; }
.photo::after { content: ''; position: absolute; left: 0; right: 0; bottom: 0; height: 120px; background: linear-gradient(to bottom, rgba(255,255,255,0), #fff); }
.panel { position: absolute; left: 0; right: 0; top: %dpx; bottom: 0; display: flex; flex-direction: column; align-items: center; justify-content: center; text-align: center; padding-bottom: 10px; }
h1 { font-weight: 1000; font-size: 66px; line-height: 1.02; letter-spacing: -.025em; }
h1 em { font-style: normal; color: #376C50; }
.brand { margin-top: 26px; display: flex; align-items: center; gap: 14px; }
.brand img { width: 64px; height: 64px; }
.brand b { font-weight: 900; font-size: 36px; letter-spacing: -.01em; }
.brand b em { font-style: normal; color: #376C50; }
.corner { position: absolute; left: 44px; top: 44px; display: flex; align-items: center; gap: 14px; background: rgba(255,255,255,.96); border-radius: 22px; padding: 14px; box-shadow: 0 10px 30px rgba(0,0,0,.22); }
.corner img { width: 76px; height: 76px; display: block; }
.corner b { font-weight: 900; font-size: 32px; letter-spacing: -.01em; }
.corner b em { font-style: normal; color: #376C50; }
.small { margin-top: 8px; font-weight: 600; font-size: 26px; color: #5C5C5C; }
""" % (V, PH, PH - 20)

VARIANTS = [(n, n, False) for n in POSTS] + [(n, n + "-logo", True) for n in POSTS]
for img, name, corner in VARIANTS:
    brand = '<div class="brand"><img src="%s/brand/wallet-mark.png" alt=""><b>Wavvy <em>Wallet</em></b></div>' % V
    top = ""
    if corner:
        top = '<div class="corner"><img src="%s/brand/wallet-mark.png" alt=""></div>' % V
        brand = '<div class="brand"><b>Wavvy <em>Wallet</em></b></div>'
    html = """<!doctype html><html><head><meta charset="utf-8"><style>%s</style></head><body>
<div class="photo" style="background-image:url('../assets/%s.jpg')"></div>%s
<div class="panel">
  <h1>Thank you,<br><em>Africa Fintech Summit!</em></h1>
  %s
  <div class="small">Know where your money is going.</div>
</div></body></html>""" % (CSS, img, top, brand)
    f = "html/%s.html" % name
    open(f, "w").write(html)
    chrome = subprocess.check_output("ls -d /root/.cache/hyperframes/chrome/chrome-headless-shell/*/chrome-headless-shell-linux64/chrome-headless-shell | tail -1", shell=True).decode().strip()
    out = os.path.join(ROOT, "posts/%s.png" % name)
    subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                    "--window-size=1080,1350", "--virtual-time-budget=4000", "--allow-file-access-from-files",
                    "--screenshot=" + out, "file://" + os.path.join(ROOT, f)], check=True, capture_output=True)
    print(out)
