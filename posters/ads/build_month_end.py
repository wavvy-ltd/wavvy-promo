"""'25th of the month has entered the chat…' rebuilt in Wavvy styling (2160x2700).
Theme: wavvy-landing (Nunito, #111111 / #376C50 / #FAFAFA), transparent wallet mark only.
    python3 tools/build_month_end.py   -> renders/wavvy-month-end.png
"""
import os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

CSS = """
@font-face { font-family: 'Nunito'; src: url('assets/fonts/Nunito.ttf') format('truetype'); font-weight: 200 1000; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 1080px; height: 1350px; overflow: hidden; }
body { font-family: 'Nunito', 'Noto Color Emoji', sans-serif; background: #FFFFFF; color: #111111; position: relative; -webkit-font-smoothing: antialiased; }
.mark { position: absolute; left: 48px; top: 44px; width: 84px; height: 84px; }
.badges { position: absolute; right: 48px; top: 56px; display: flex; gap: 12px; }
.badges img { height: 56px; display: block; }
.head { position: absolute; left: 0; right: 0; top: 160px; text-align: center; font-weight: 1000; font-size: 84px; line-height: 1.02; letter-spacing: -.035em; }
.head em { font-style: normal; color: #376C50; }
.sub { position: absolute; left: 0; right: 0; top: 345px; text-align: center; font-weight: 700; font-size: 38px; color: #5C5C5C; }
.glow { position: absolute; left: 540px; top: 760px; width: 1000px; height: 900px; margin: -450px 0 0 -500px; border-radius: 50%;
        background: radial-gradient(closest-side, rgba(55,108,80,.16), rgba(55,108,80,.06) 60%, rgba(55,108,80,0)); }
.photo { position: absolute; left: 40px; top: 410px; width: 1000px; height: 690px; object-fit: contain; object-position: 50% 100%;
         -webkit-mask-image: linear-gradient(to bottom, #000 88%, transparent 100%); }
.foot { position: absolute; left: 0; right: 0; bottom: 0; height: 250px; background: #FAFAFA; border-top: 1px solid rgba(17,17,17,.06);
        display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 12px; text-align: center; }
.foot .a { font-weight: 900; font-size: 44px; letter-spacing: -.01em; line-height: 1.15; }
.foot .a em { font-style: normal; color: #376C50; }
.foot .b { font-weight: 700; font-size: 32px; color: #5C5C5C; }
.foot .b em { font-style: normal; color: #376C50; font-weight: 900; }
"""

page = """<!doctype html><html><head><meta charset="utf-8"><style>%s</style></head><body>
<img class="mark" src="assets/brand/wallet-mark.png" alt="Wavvy Wallet">
<div class="badges"><img src="assets/brand/app-store.png" alt="App Store"><img src="assets/brand/google-play.png" alt="Google Play"></div>
<div class="head">25th of the month has<br>entered <em>the chat…</em></div>
<div class="sub">Salary imeisha kabla mwezi ianze! 😂</div>
<div class="glow"></div>
<img class="photo" src="assets/cutout/month-end-man.clean.png" alt="">
<div class="foot"><div class="a">Be honest… salary yako hukaa<br>kwa account <em>for how long?</em></div>
<div class="b">Download <em>Wavvy Wallet</em> today.</div></div>
</body></html>""" % CSS

open("poster-month-end.html", "w").write(page)
chrome = subprocess.check_output("ls -d /root/.cache/hyperframes/chrome/chrome-headless-shell/*/chrome-headless-shell-linux64/chrome-headless-shell | tail -1", shell=True).decode().strip()
out = os.path.join(ROOT, "renders/wavvy-month-end.png")
subprocess.run([chrome, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2", "--window-size=1080,1350",
                "--virtual-time-budget=4000", "--allow-file-access-from-files", "--screenshot=" + out,
                "file://" + os.path.join(ROOT, "poster-month-end.html")], check=True, capture_output=True)
print(out)
