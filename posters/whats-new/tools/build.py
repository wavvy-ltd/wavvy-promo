"""Wavvy Wallet "What's new" poster in the Hanga Pitchfest layout (hands holding a card).
Theme from wavvywallet.com: Nunito, #376C50 primary, #4FC385 secondary, #111111 ink, dark green ground.
The B&W hands are the reference's own, cut out by tools/hands.py, layered over the new card.
    python3 tools/build.py   -> poster.html, renders/wavvy-whats-new-poster.png
"""
import html, os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
W, H = 1320, 1630

ROWS = [
    ("KCB M-Pesa messages,", "imported for you"),
    ("MTN MoMo SMS &amp; PDF", "statements on iPhone"),
    ("A faster tag screen that", "tells you when you're offline"),
    ("Transaction charges, one", "swipe from your expenses"),
    ("Reminders for bills", "&amp; subscriptions"),
    ("Clearer money in &amp; out,", "plus RWF support"),
]
# card geometry measured from the reference (centre, size, rotation) — grown 6 px to cover the old edge
CARD = dict(cx=859, cy=1040.5, w=700, h=1084, rot=5.9)

ARROW = ('<svg class="arrow" viewBox="0 0 200 140"><g fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">'
         '<path d="M14 20 C 20 70, 70 100, 150 104"/><path d="M22 14 C 30 64, 76 92, 150 96"/>'
         '<path d="M126 78 L 168 101 L 128 124"/></g></svg>')
SEARCH = ('<svg viewBox="0 0 24 24" width="30" height="30"><circle cx="10.5" cy="10.5" r="6.5" fill="none" stroke="#111" stroke-width="2.6"/>'
          '<path d="M15.5 15.5 L 21 21" stroke="#111" stroke-width="2.6" stroke-linecap="round"/></svg>')

CSS = """
@font-face { font-family: 'Nunito'; src: url('assets/fonts/Nunito.ttf') format('truetype'); font-weight: 200 1000; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: %(W)dpx; height: %(H)dpx; overflow: hidden; font-family: 'Nunito', sans-serif; }
body { position: relative; background:
  radial-gradient(ellipse 900px 700px at 15%% 18%%, rgba(79,195,133,.22), rgba(79,195,133,0) 70%%),
  radial-gradient(ellipse 900px 900px at 95%% 95%%, rgba(55,108,80,.45), rgba(55,108,80,0) 70%%),
  linear-gradient(165deg, #1E3D2D 0%%, #142A1F 55%%, #0E1F17 100%%); }
.brand { position: absolute; left: 92px; top: 86px; display: flex; align-items: center; gap: 22px; }
.brand .tile { width: 104px; height: 104px; border-radius: 28px; background: #fff; display: flex; align-items: center; justify-content: center; box-shadow: 0 12px 30px rgba(0,0,0,.3); }
.brand .tile img { width: 92px; height: 92px; }
.brand .wm { color: #fff; font-weight: 900; font-size: 50px; line-height: .95; letter-spacing: -.01em; }
.brand .wm span { display: block; color: #B7EBC8; font-weight: 700; font-size: 30px; letter-spacing: .02em; margin-top: 6px; }
.ver { position: absolute; right: 92px; top: 112px; color: #0E1F17; background: #B7EBC8; font-weight: 900; font-size: 30px; padding: 14px 28px; border-radius: 999px; letter-spacing: .02em; }
.title { position: absolute; left: 62px; top: 268px; transform: rotate(-11deg); transform-origin: 0 0; color: #fff; font-weight: 900; text-transform: uppercase; }
.title .l1 { font-size: 78px; letter-spacing: .01em; margin-left: 112px; }
.title .tag { display: inline-block; margin-top: 10px; background: #4FC385; color: #0E1F17; font-size: 70px; padding: 6px 34px 10px; clip-path: polygon(3%% 0, 100%% 0, 97%% 100%%, 0 100%%); letter-spacing: .005em; }
.title .l3 { font-size: 60px; margin-top: 12px; margin-left: 6px; letter-spacing: .01em; }
.arrow { position: absolute; left: 300px; top: 610px; width: 170px; transform: rotate(18deg); }
.card { position: absolute; left: %(cl)dpx; top: %(ct)dpx; width: %(cw)dpx; height: %(ch)dpx; transform: rotate(%(rot)sdeg);
        background: #FAFAFA; border-radius: 46px; box-shadow: 0 30px 70px rgba(0,0,0,.45); padding: 58px 46px 0 70px; }
.row { position: relative; display: flex; align-items: center; gap: 22px; height: 112px; margin-bottom: 20px; padding: 0 22px 0 18px; border-radius: 18px; }
.row .n { flex: none; width: 58px; height: 58px; border-radius: 50%%; font-weight: 900; font-size: 34px; line-height: 58px; text-align: center; }
.row .t { font-weight: 800; font-size: 30px; line-height: 1.12; letter-spacing: -.005em; }
.row.fill { background: #376C50; color: #fff; box-shadow: 0 8px 18px rgba(55,108,80,.28); }
.row.fill .n { background: #fff; color: #376C50; }
.row.line { border: 3px dashed #376C50; color: #111; background: #fff; }
.row.line .n { background: #376C50; color: #fff; }
.cta { position: absolute; left: 70px; bottom: 54px; width: 470px; text-align: center; }
.cta .k { color: #111; font-weight: 800; font-size: 36px; letter-spacing: .14em; }
.cta .pill { margin: 14px auto 0; display: flex; align-items: center; justify-content: space-between; gap: 16px; border: 3px solid #376C50; border-radius: 999px; padding: 12px 22px 12px 32px; width: 450px; }
.cta .pill b { color: #111; font-weight: 800; font-size: 32px; }
.cta .pill i { width: 3px; height: 34px; background: #376C50; margin-left: auto; }
.hands { position: absolute; left: 0; top: 0; width: %(W)dpx; height: %(H)dpx; pointer-events: none; }
.foot { position: absolute; left: 60px; top: 1420px; color: #fff; }
.foot .k { font-weight: 900; font-size: 38px; letter-spacing: .04em; }
.foot .k span { color: #4FC385; }
.foot .b { display: flex; gap: 14px; margin-top: 18px; }
.foot .b img { height: 54px; width: auto; display: block; }
"""


def page():
    rows = []
    tilts = [-1.2, 1.0, -0.8, 1.3, -1.0, 0.9]
    for i, (a, b) in enumerate(ROWS):
        cls = "line" if i % 2 == 0 else "fill"
        style = "transform: rotate(%sdeg);" % tilts[i]
        if i == 5:
            style += " width: 560px;"
        rows.append('<div class="row %s" style="%s"><div class="n">%d</div><div class="t">%s<br>%s</div></div>' % (cls, style, i + 1, a, b))
    c = CARD
    css = CSS % dict(W=W, H=H, cl=round(c["cx"] - c["w"] / 2), ct=round(c["cy"] - c["h"] / 2), cw=c["w"], ch=c["h"], rot=c["rot"])
    return """<!doctype html><html><head><meta charset="utf-8"><style>%s</style></head><body>
<div class="brand"><div class="tile"><img src="assets/brand/logo.png" alt=""></div><div class="wm">Wavvy Wallet<span>What's new</span></div></div>
<div class="ver">NEW UPDATE</div>
<div class="title"><div class="l1">What's new in</div><div class="tag">Wavvy Wallet</div><div class="l3">this update...</div></div>
%s
<div class="card">%s
  <div class="cta"><div class="k">UPDATE NOW</div><div class="pill"><b>wavvywallet.com</b><i></i>%s</div></div>
</div>
<img class="hands" src="assets/hands.png" alt="">
<div class="foot"><div class="k">AVAILABLE <span>NOW</span></div><div class="b"><img src="assets/brand/google-play.png" alt=""><img src="assets/brand/app-store.png" alt=""></div></div>
</body></html>""" % (css, ARROW, "\n  ".join(rows), SEARCH)


CHROME = subprocess.check_output("ls -d /root/.cache/hyperframes/chrome/chrome-headless-shell/*/chrome-headless-shell-linux64/chrome-headless-shell | tail -1",
                                 shell=True).decode().strip()
open("poster.html", "w").write(page())
out = os.path.join(ROOT, "renders/wavvy-whats-new-poster.png")
subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                "--window-size=%d,%d" % (W, H), "--virtual-time-budget=4000", "--allow-file-access-from-files",
                "--screenshot=" + out, "file://" + os.path.join(ROOT, "poster.html")], check=True, capture_output=True)
print(out)
