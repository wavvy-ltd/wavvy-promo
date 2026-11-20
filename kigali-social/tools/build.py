"""Wavvy Wallet Kigali social posts (HTML -> PNG with headless Chrome, exact platform sizes).
Theme from wavvywallet.com: Nunito, #376C50 / #4FC385, ink #111111, deep green #0E1F17.
    python3 tools/build.py            -> posts/*.png
"""
import os, subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
os.makedirs("posts", exist_ok=True)
V = "/root/videos/wavvy-whats-new/assets"

BASE = """
@font-face { font-family: 'Nunito'; src: url('%s/fonts/Nunito.ttf') format('truetype'); font-weight: 200 1000; }
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: %%(W)dpx; height: %%(H)dpx; overflow: hidden; font-family: 'Nunito', sans-serif; }
body { position: relative; background: #0E1F17 url('../assets/%%(img)s.jpg') center/cover no-repeat; }
.brand { position: absolute; display: flex; align-items: center; gap: 16px; }
.tile { flex: none; width: 76px; height: 76px; border-radius: 22px; background: #fff; display: flex; align-items: center; justify-content: center; box-shadow: 0 10px 26px rgba(0,0,0,.22); }
.tile img { width: 66px; height: 66px; }
.brand b { font-weight: 900; font-size: 34px; letter-spacing: -.01em; }
.shade { position: absolute; left: 0; right: 0; }
h1 { font-weight: 900; letter-spacing: -.02em; line-height: 1.02; }
h1 em { font-style: normal; color: #4FC385; }
.sub { font-weight: 700; }
.pill { display: inline-block; border-radius: 999px; font-weight: 800; }
.badges { display: flex; gap: 14px; }
.badges img { height: 62px; display: block; }
.notif { position: absolute; background: rgba(255,255,255,.97); border-radius: 30px; box-shadow: 0 24px 60px rgba(0,0,0,.28); display: flex; gap: 20px; padding: 24px 28px; align-items: center; }
.notif .ic { flex: none; width: 70px; height: 70px; border-radius: 18px; background: #fff; border: 2px solid rgba(17,17,17,.08); display: flex; align-items: center; justify-content: center; }
.notif .ic img { width: 58px; height: 58px; }
.notif .meta { color: #5C5C5C; font-weight: 700; font-size: 24px; }
.notif .t { color: #111; font-weight: 900; font-size: 30px; margin-top: 2px; }
.notif .amt { color: #376C50; }
.dots { position: absolute; display: flex; gap: 10px; }
.dots i { width: 12px; height: 12px; border-radius: 50%%%%; background: rgba(255,255,255,.45); }
.dots i.on { background: #fff; width: 34px; border-radius: 6px; }
""" % V

LOGO = '<div class="tile"><img src="%s/brand/logo.png"></div>' % V
BADGES = '<div class="badges"><img src="%s/brand/google-play.png"><img src="%s/brand/app-store.png"></div>' % (V, V)

POSTS = {
    # Instagram / Facebook feed, 4:5
    "01-feed-know-your-money": dict(W=1080, H=1350, img="feed", body=f"""
<div class="shade" style="top:0;height:300px;background:linear-gradient(rgba(14,31,23,.55),rgba(14,31,23,0))"></div>
<div class="shade" style="bottom:0;height:640px;background:linear-gradient(rgba(14,31,23,0),rgba(14,31,23,.86) 52%,rgba(14,31,23,.95))"></div>
<div class="brand" style="left:64px;top:60px">{LOGO}<b style="color:#fff">Wavvy Wallet</b></div>
<div style="position:absolute;left:64px;right:64px;bottom:84px;color:#fff">
  <span class="pill" style="background:#4FC385;color:#0E1F17;font-size:26px;padding:8px 22px">KIGALI · RWF · MTN MOMO</span>
  <h1 style="font-size:96px;margin-top:26px">Know where<br>your money<br><em>is going.</em></h1>
  <p class="sub" style="font-size:34px;margin-top:24px;color:#E6F2EA">Every payment tracked and tagged, in francs.</p>
</div>"""),

    # Instagram / WhatsApp / Facebook story, 9:16 (keep 250px top/bottom clear of UI)
    "02-story-payment-lands": dict(W=1080, H=1920, img="story", body=f"""
<div class="shade" style="top:0;height:520px;background:linear-gradient(rgba(14,31,23,.6),rgba(14,31,23,0))"></div>
<div class="shade" style="bottom:0;height:860px;background:linear-gradient(rgba(14,31,23,0),rgba(14,31,23,.88) 45%,rgba(14,31,23,.96))"></div>
<div class="brand" style="left:72px;top:250px;display:none">{LOGO}<b style="color:#fff">Wavvy Wallet</b></div>
<div class="notif" style="left:56px;right:56px;top:270px">
  <div class="ic"><img src="{V}/brand/logo.png"></div>
  <div><div class="meta">Wavvy Wallet · now</div><div class="t">New payment <span class="amt">+RWF 25,000</span></div><div class="meta" style="font-size:25px;margin-top:2px">from Jean Mugisha · MTN MoMo</div></div>
</div>
<div style="position:absolute;left:72px;right:72px;bottom:270px;color:#fff">
  <h1 style="font-size:92px">Every payment,<br><em>sorted the moment<br>it lands.</em></h1>
  <p class="sub" style="font-size:34px;margin-top:26px;color:#E6F2EA">Download Wavvy Wallet. Free on Android and iPhone.</p>
  <div style="margin-top:34px">{BADGES}</div>
</div>"""),

    # LinkedIn / X / Facebook link post, 16:9
    "03-wide-every-franc": dict(W=1200, H=675, img="wide", body=f"""
<div class="shade" style="top:0;right:0;left:auto;width:720px;height:675px;background:linear-gradient(90deg,rgba(244,247,246,0),rgba(244,247,246,.78) 40%,rgba(244,247,246,.9))"></div>
<div style="position:absolute;right:56px;top:70px;width:520px;color:#111;text-align:right">
  <span class="pill" style="background:#376C50;color:#fff;font-size:18px;padding:6px 16px">KIGALI, RWANDA</span>
  <h1 style="font-size:66px;margin-top:20px">Every franc,<br><em style="color:#376C50">accounted for.</em></h1>
  <p class="sub" style="font-size:24px;margin-top:18px;color:#3B4A42">Wavvy Wallet reads your MTN MoMo messages and shows exactly where your money goes.</p>
</div>
<div class="brand" style="right:56px;bottom:46px"><b style="color:#111;font-size:28px">wavvywallet.com</b>{LOGO.replace('76px','60px')}</div>"""),

    # Square post, 1:1
    "04-square-muraho-kigali": dict(W=1080, H=1080, img="square", body=f"""
<div class="shade" style="top:0;height:420px;background:linear-gradient(rgba(14,31,23,.62),rgba(14,31,23,0))"></div>
<div style="position:absolute;left:64px;top:64px;color:#fff">
  <h1 style="font-size:104px">Muraho,<br><em>Kigali.</em></h1>
</div>
<div style="position:absolute;left:40px;right:40px;bottom:40px;background:#fff;border-radius:34px;padding:32px 36px;display:flex;align-items:center;gap:26px;box-shadow:0 20px 50px rgba(0,0,0,.25)">
  {LOGO}
  <div style="flex:1"><div style="font-weight:900;font-size:36px;color:#111">Wavvy Wallet speaks RWF</div>
  <div style="font-weight:700;font-size:26px;color:#5C5C5C;margin-top:4px">Track MTN MoMo payments in francs, and see where every one goes.</div></div>
</div>"""),
}

# Carousel, 4:5 x 3 (Africa Fintech Summit)
SUMMIT = [
    ("05-summit-1", "summit1", "AFRICA FINTECH SUMMIT · KIGALI", "Big conversations about<br><em>Africa's money.</em>", "Fintech builders, banks and founders, all in one room."),
    ("05-summit-2", "summit2", "AFRICA FINTECH SUMMIT · KIGALI", "Money tools that fit<br><em>how we really pay.</em>", "MoMo, M-Pesa, cash: everyday money is mobile."),
    ("05-summit-3", "summit3", "THANK YOU, KIGALI", "Know where your money<br><em>is going.</em>", "Try Wavvy Wallet free: wavvywallet.com"),
]
for i, (name, img, kick, head, sub) in enumerate(SUMMIT):
    dots = "".join('<i class="on"></i>' if j == i else "<i></i>" for j in range(3))
    extra = f'<div style="margin-top:30px">{BADGES}</div>' if i == 2 else ""
    POSTS[name] = dict(W=1080, H=1350, img=img, body=f"""
<div class="shade" style="top:0;height:300px;background:linear-gradient(rgba(14,31,23,.6),rgba(14,31,23,0))"></div>
<div class="shade" style="bottom:0;height:720px;background:linear-gradient(rgba(14,31,23,0),rgba(14,31,23,.9) 50%,rgba(14,31,23,.96))"></div>
<div class="brand" style="left:64px;top:60px">{LOGO}<b style="color:#fff">Wavvy Wallet</b></div>
<div class="dots" style="right:64px;top:92px">{dots}</div>
<div style="position:absolute;left:64px;right:64px;bottom:84px;color:#fff">
  <span class="pill" style="background:#4FC385;color:#0E1F17;font-size:24px;padding:8px 22px">{kick}</span>
  <h1 style="font-size:80px;margin-top:24px">{head}</h1>
  <p class="sub" style="font-size:32px;margin-top:22px;color:#E6F2EA">{sub}</p>{extra}
</div>""")

CHROME = subprocess.check_output("ls -d /root/.cache/hyperframes/chrome/chrome-headless-shell/*/chrome-headless-shell-linux64/chrome-headless-shell | tail -1", shell=True).decode().strip()
os.makedirs("html", exist_ok=True)
for name, p in POSTS.items():
    html = '<!doctype html><html><head><meta charset="utf-8"><style>%s</style></head><body>%s</body></html>' % (BASE % p, p["body"])
    f = os.path.join(ROOT, "html", name + ".html")
    open(f, "w").write(html)
    out = os.path.join(ROOT, "posts", name + ".png")
    subprocess.run([CHROME, "--headless", "--no-sandbox", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    "--window-size=%d,%d" % (p["W"], p["H"]), "--virtual-time-budget=4000", "--allow-file-access-from-files",
                    "--screenshot=" + out, "file://" + f], check=True, capture_output=True)
    print(out)
