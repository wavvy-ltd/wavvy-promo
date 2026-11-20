"""'Murakoze Kigali' post: night photo of the Kigali Convention Centre (1920x1080 landscape, exported 2x).
    python3 tools/murakoze.py -> posts/07-murakoze-kigali.png
"""
import os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
V = "/root/videos/wavvy-whats-new/assets"

page = """<!doctype html><html><head><meta charset="utf-8"><style>
@font-face { font-family: 'Nunito'; src: url('%s/fonts/Nunito.ttf') format('truetype'); font-weight: 200 1000; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 1920px; height: 1080px; overflow: hidden; font-family: 'Nunito', sans-serif; background: #020203 url('../assets/murakoze.jpg') center/cover; color: #fff; }
.tile { position: absolute; left: 48px; top: 97px; width: 96px; height: 96px; border-radius: 26px; background: #fff;
        display: flex; align-items: center; justify-content: center; }
.tile img { width: 74px; height: 74px; }
.txt { position: absolute; right: 70px; top: 30px; width: 640px; text-align: right; }
.txt h1 { font-weight: 1000; font-size: 112px; line-height: .96; letter-spacing: -.035em; }
.txt h1 em { font-style: normal; color: #4FC385; }
.txt p { margin-top: 16px; font-weight: 700; font-size: 30px; color: rgba(255,255,255,.8); }
.brand { position: absolute; left: 164px; top: 104px;  font-weight: 900; font-size: 36px; letter-spacing: -.01em; }
.brand em { font-style: normal; color: #4FC385; }
.brand small { display: block; margin-top: 0; font-weight: 600; font-size: 24px; color: rgba(255,255,255,.7); }
</style></head><body>
<div class="tile"><img src="%s/brand/wallet-mark.png" alt=""></div>
<div class="txt"><h1>Murakoze,<br><em>Kigali!</em></h1><p>Thank you for an amazing week.</p>
</div>
<div class="brand">Wavvy <em>Wallet</em><small>Know where your money is going.</small></div>
</body></html>""" % (V, V)

os.makedirs("html", exist_ok=True)
open("html/07-murakoze-kigali.html", "w").write(page)
chrome = subprocess.check_output("ls -d /root/.cache/hyperframes/chrome/chrome-headless-shell/*/chrome-headless-shell-linux64/chrome-headless-shell | tail -1", shell=True).decode().strip()
out = os.path.join(ROOT, "posts/07-murakoze-kigali.png")
subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2", "--window-size=1920,1080",
                "--virtual-time-budget=4000", "--allow-file-access-from-files", "--screenshot=" + out,
                "file://" + os.path.join(ROOT, "html/07-murakoze-kigali.html")], check=True, capture_output=True)
print(out)
