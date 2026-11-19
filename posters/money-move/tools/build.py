"""Wavvy Wallet "Your Money, Your Move!" poster -> poster-<cc>.html, then renders/wavvy-poster-<cc>.png.
Theme from wavvy-ltd/wavvy-landing (landing-next): Nunito, #111111 text, #376C50 accent, #FAFAFA surface.
    python3 tools/build.py [ke|rw ...]
"""
import html, json, os, subprocess, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

POSTERS = {
    "ke": {
        "photo": "assets/cutout/photo1.png",
        "count": "Shilling",
        "cards": [
            ("Money sent", "4:12 PM", "You sent <b>Ksh 2,500</b> to Wanjiku Kamau. Tagged: Family"),
            ("Bill payment", "2:33 PM", "<b>Ksh 1,000</b> paid to KPLC Prepaid for 34.6&nbsp;kWh"),
            ("Money received", "1:08 PM", "You received <b>Ksh 15,000</b> from Brian Otieno"),
            ("Airtime", "11:25 AM", "<b>Ksh 100</b> airtime bought for your Safaricom line"),
        ],
    },
    "ea": {
        "photo": "assets/cutout/photo3.clean.graded.png",
        "count": "Shilling and Franc",
        "cards": [
            ("Money sent", "4:12 PM", "You sent <b>Ksh 2,500</b> to Wanjiku Kamau. Tagged: Family"),
            ("Money received", "2:33 PM", "You received <b>50,000 RWF</b> from Eric Habimana"),
            ("Bill payment", "1:08 PM", "<b>Ksh 1,000</b> paid to KPLC Prepaid for 34.6&nbsp;kWh"),
            ("Groceries", "11:25 AM", "<b>6,500 RWF</b> paid to Simba Supermarket. Tagged: Food"),
        ],
    },
    "rw": {
        "photo": "assets/cutout/photo2.png",
        "count": "Franc",
        "cards": [
            ("Money sent", "4:12 PM", "You sent <b>15,000 RWF</b> to Aline Uwase. Tagged: Family"),
            ("Bill payment", "2:33 PM", "<b>5,000 RWF</b> paid to EUCL Cash Power for 28.4&nbsp;kWh"),
            ("Money received", "1:08 PM", "You received <b>50,000 RWF</b> from Eric Habimana"),
            ("Groceries", "11:25 AM", "<b>6,500 RWF</b> paid to Simba Supermarket. Tagged: Food"),
        ],
    },
}

# layout knobs per poster (photo box + card slots); overridable from tools/layout.json
LAYOUT = {
    # family: faces fill the top of the cut-out, so the cards sit lower, over shirts and arms
    "ke": {"photo": {"left": 140, "top": 425, "width": 687, "height": 790, "pos": "50% 0%", "fade_l": True, "fade_r": True},
           "slots": [(20, 742), (752, 742), (20, 952), (752, 952)]},
    "ea": {"photo": {"left": -95, "top": 430, "width": 1010, "height": 878, "pos": "50% 0%", "fade_l": False, "fade_r": False},
           "slots": [(20, 430), (752, 430), (20, 905), (752, 930)], "foot": 33},
    "rw": {"photo": {"left": 228, "top": 425, "width": 624, "height": 790, "pos": "50% 0%", "fade_l": False, "fade_r": True},
           "slots": [(20, 420), (752, 520), (20, 880), (752, 935)]},
}
if os.path.exists("tools/layout.json"):
    for k, v in json.load(open("tools/layout.json")).items():
        LAYOUT[k].update(v)

CSS = """
@font-face { font-family: 'Nunito'; src: url('assets/fonts/Nunito.ttf') format('truetype'); font-weight: 200 1000; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 1080px; height: 1350px; overflow: hidden; }
body { font-family: 'Nunito', sans-serif; background: #FFFFFF; color: #111111; position: relative; -webkit-font-smoothing: antialiased; }
.top { position: absolute; left: 48px; right: 48px; top: 40px; height: 96px; display: flex; align-items: center; justify-content: space-between; }
.brand { display: flex; align-items: center; gap: 16px; }
.brand img { width: 92px; height: 92px; }
.brand span { font-weight: 900; font-size: 40px; letter-spacing: -.01em; }
.brand span em { font-style: normal; color: #376C50; }
.badges { display: flex; gap: 14px; align-items: center; }
.badges img { height: 62px; }
.head { position: absolute; left: 0; right: 0; top: 168px; text-align: center; font-weight: 1000; font-size: 128px; line-height: .98; letter-spacing: -.035em; text-transform: uppercase; }
.head .l2 { color: #376C50; }
.glow { position: absolute; left: 540px; top: 860px; width: 1100px; height: 1000px; margin: -500px 0 0 -550px; border-radius: 50%;
        background: radial-gradient(closest-side, rgba(55,108,80,.22), rgba(55,108,80,.10) 55%, rgba(55,108,80,0) 100%); }
.ring { position: absolute; left: 540px; top: 900px; width: 640px; height: 640px; margin: -320px 0 0 -320px; border-radius: 50%;
        background: rgba(55,108,80,.12); }
.photo { position: absolute; object-fit: contain; }
.card { position: absolute; width: 310px; background: #FFFFFF; border: 1px solid rgba(17,17,17,.08); border-radius: 26px; padding: 16px 20px 18px;
        box-shadow: 0 18px 40px rgba(17,17,17,.10), 0 4px 10px rgba(17,17,17,.06); }
.card .row { display: flex; align-items: center; gap: 12px; margin-bottom: 8px; }
.card .ic { width: 48px; height: 48px; border-radius: 13px; background: #fff; border: 1px solid rgba(17,17,17,.08); display: flex; align-items: center; justify-content: center; flex: none; }
.card .ic img { width: 40px; height: 40px; }
.card .t { font-weight: 800; font-size: 28px; line-height: 1.1; }
.card .tm { font-weight: 700; font-size: 21px; color: #5C5C5C; margin-top: 2px; }
.card .m { font-weight: 600; font-size: 25px; line-height: 1.3; color: #333333; }
.card .m b { font-weight: 900; color: #376C50; }
.foot { position: absolute; left: 0; right: 0; bottom: 0; height: 200px; background: #FAFAFA; border-top: 1px solid rgba(17,17,17,.06);
        display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 8px; text-align: center; }
.foot .a { font-weight: 700; font-size: 38px; color: #5C5C5C; }
.foot .b { font-weight: 900; font-size: 54px; letter-spacing: -.01em; }
.foot .b em { font-style: normal; color: #376C50; }
"""


def mask(ph):
    m = ["linear-gradient(to bottom, #000 80%, transparent 97%)"]
    if ph.get("fade_l"):
        m.append("linear-gradient(to right, transparent 0%, #000 9%)")
    if ph.get("fade_r"):
        m.append("linear-gradient(to left, transparent 0%, #000 9%)")
    return "-webkit-mask-image:%s;-webkit-mask-composite:source-in;mask-composite:intersect" % ", ".join(m)


def page(cc):
    p, L = POSTERS[cc], LAYOUT[cc]
    ph = L["photo"]
    cards = []
    for (title, tm, msg), (x, y) in zip(p["cards"], L["slots"]):
        cards.append(
            '<div class="card" style="left:%dpx;top:%dpx"><div class="row"><div class="ic"><img src="assets/brand/wallet-mark.png" alt=""></div>'
            '<div><div class="t">%s</div><div class="tm">%s</div></div></div><div class="m">%s</div></div>' % (x, y, html.escape(title), tm, msg))
    return """<!doctype html><html><head><meta charset="utf-8"><title>Wavvy poster %s</title><style>%s</style></head><body>
<div class="glow"></div><div class="ring"></div>
<img class="photo" src="%s" style="left:%dpx;top:%dpx;width:%dpx;height:%dpx;object-position:%s;%s" alt="">
<div class="top"><div class="brand"><img src="assets/brand/wallet-mark.png" alt=""><span>Wavvy <em>Wallet</em></span></div>
<div class="badges"><img src="assets/brand/app-store.png" alt="App Store"><img src="assets/brand/google-play.png" alt="Google Play"></div></div>
<div class="head"><div>Your Money</div><div class="l2">Your Move!</div></div>
%s
<div class="foot"><div class="a" style="font-size:%dpx">Know Your Spending. Make Every %s Count.</div><div class="b">Download <em>Wavvy Wallet</em> Today.</div></div>
</body></html>""" % (cc, CSS, p["photo"], ph["left"], ph["top"], ph["width"], ph["height"], ph["pos"], mask(ph), "\n".join(cards), L.get("foot", 38), p["count"])


CHROME = subprocess.check_output("ls -d /root/.cache/hyperframes/chrome/chrome-headless-shell/*/chrome-headless-shell-linux64/chrome-headless-shell 2>/dev/null | tail -1 || true",
                                 shell=True).decode().strip()
os.makedirs("renders", exist_ok=True)
for cc in (sys.argv[1:] or ["ke", "rw", "ea"]):
    f = "poster-%s.html" % cc
    open(f, "w").write(page(cc))
    out = os.path.join(ROOT, "renders/wavvy-poster-%s.png" % cc)
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=2",
                    "--window-size=1080,1350", "--virtual-time-budget=4000", "--allow-file-access-from-files",
                    "--screenshot=" + out, "file://" + os.path.join(ROOT, f)], check=True, capture_output=True)
    print(cc, out)
