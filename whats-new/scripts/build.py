#!/usr/bin/env python3
"""Build the HyperFrames composition from storyboard.json.

    python3 scripts/build.py [storyboard.json] [--out DIR]

Writes index.html, compositions/<scene>.html, compositions/captions.html and cue-sheet.md.
Generated files are meant to be committed: Studio edits them, and re-running the build
overwrites them from the storyboard. Everything below encodes the rules HyperFrames wants
(initial hidden states via gsap.set, transforms only, fromTo in seeked scenes, transparent roots
for scenes that whip in over the previous one, every timed element with class="clip").
"""
import argparse, html, json, math, os, re, sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TPL = os.path.join(ROOT, "templates")

# bundled sounds: where each file's peak sits, so a cue lands one frame after the picture
SFX = {
    "click":        {"file": "assets/sfx/click.mp3",         "dur": 0.37, "peak": 0.073},
    "pop":          {"file": "assets/sfx/pop.mp3",           "dur": 0.72, "peak": 0.120},
    "whoosh":       {"file": "assets/sfx/whoosh.mp3",        "dur": 0.58, "peak": 0.162},
    "notification": {"file": "assets/sfx/notification.mp3",  "dur": 2.46, "peak": 0.229},
    "impact":       {"file": "assets/sfx/impact-bass-1.mp3", "dur": 2.12, "peak": 0.073},
    "pencil":       {"file": "assets/sfx/pencil.wav",         "dur": 0.75, "peak": 0.03},
}
FRAME = 1 / 30


def tpl(name):
    with open(os.path.join(TPL, name)) as f:
        return f.read()


def fill(t, **kw):
    for k, v in kw.items():
        t = t.replace("{{%s}}" % k, str(v))
    return t


def esc(s):
    return html.escape(str(s), quote=True)


def rich(text):
    """'Where did your money *go?*' → words as spans, *…* highlighted."""
    out = []
    for w in text.split():
        hi = w.startswith("*") and w.endswith("*") and len(w) > 2
        out.append('<span class="w%s">%s</span>' % (" hi" if hi else "", esc(w.strip("*"))))
    return " ".join(out)


def hero_html(text):
    parts = []
    for w in text.split():
        hi = w.startswith("*") and w.endswith("*") and len(w) > 2
        parts.append('<span class="q">%s</span>' % esc(w.strip("*")) if hi else esc(w))
    return " ".join(parts)


PENCIL_SVG = (
    '<svg width="150" height="150" viewBox="0 0 150 150" style="position:absolute; left:-6px; top:-144px; overflow:visible">'
    '<g transform="rotate(-38 6 144)">'
    '<polygon points="6,144 24,132 24,156" fill="#F2C99A"/>'
    '<polygon points="6,144 12,140 12,148" fill="{lead}"/>'
    '<rect x="24" y="132" width="96" height="24" rx="2" fill="{body}"/>'
    '<rect x="24" y="140" width="96" height="8" fill="#ffffff" opacity=".18"/>'
    '<rect x="120" y="131" width="12" height="26" fill="#C9CED6"/>'
    '<rect x="132" y="132" width="16" height="24" rx="5" fill="#F29BB0"/>'
    '</g></svg>')


def mark_points(box, shape, seed):
    """Hand-drawn loop (or underline) around box, resampled to even arc length."""
    x1, y1, x2, y2 = box
    ph = (seed * 2.399) % (2 * math.pi)
    pts = []
    if shape == "underline":
        n = 60
        for i in range(n + 1):
            u = i / n
            x = x1 + (x2 - x1) * u
            y = y2 + 10 + 6 * math.sin(u * math.pi * 1.0 + ph) * 0.6 + 4 * math.sin(u * 7 + ph)
            pts.append((x, y))
    else:
        cx, cy = (x1 + x2) / 2, (y1 + y2) / 2
        rx, ry = (x2 - x1) / 2 + 22, (y2 - y1) / 2 + 20
        n, turns, a0 = 140, 1.13, math.radians(200)
        for i in range(n + 1):
            u = i / n
            a = a0 + 2 * math.pi * turns * u
            g = 1 + 0.07 * (u - 0.5) + 0.025 * math.sin(3 * a + ph)
            pts.append((cx + rx * g * math.cos(a), cy + ry * g * math.sin(a) * (1 + 0.04 * math.sin(a + ph))))
    # resample to equal spacing
    d = [0.0]
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        d.append(d[-1] + math.hypot(bx - ax, by - ay))
    L, out, j = d[-1], [], 0
    for k in range(41):
        tgt = L * k / 40
        while j < len(d) - 2 and d[j + 1] < tgt:
            j += 1
        f = (tgt - d[j]) / max(1e-6, d[j + 1] - d[j])
        out.append((pts[j][0] + (pts[j + 1][0] - pts[j][0]) * f, pts[j][1] + (pts[j + 1][1] - pts[j][1]) * f))
    return pts, out, L


class Build:
    def __init__(self, sb, out):
        self.sb, self.out = sb, out
        self.b = sb["brand"]
        self.c = self.b["colors"]
        self.v = sb["video"]
        self.W, self.H = self.v["width"], self.v["height"]
        self.p = dict(left=160, top=330, width=760, height=1528, radius=64, bezel=14, crop_top=66)
        self.p.update(self.b.get("phone", {}))
        self.p["img_width"] = self.p["width"] - 2 * self.p["bezel"]
        self.p["screen_h"] = self.p["height"] - 2 * self.p["bezel"]
        self.sfx = []      # (time, name, volume, note)
        self.cues = []     # for cue-sheet.md
        font = self.b.get("font", "Montserrat")
        self.font_fallback = '"%s", sans-serif' % font
        faces = []
        for weight, path in (self.b.get("font_files") or {}).items():
            faces.append('    @font-face { font-family: "%s"; font-weight: %s; src: url("%s"); }' % (font, weight, path))
        self.font_faces = "\n".join(faces)

    # ---------- shared CSS ----------
    def phone_css(self, sid):
        p = self.p
        return (
            "    .phone { position: absolute; left: %dpx; top: %dpx; width: %dpx; height: %dpx; border-radius: %dpx; background: %s; padding: %dpx; box-shadow: 0 30px 80px rgba(0,0,0,.55); border: 1px solid %s; }\n"
            "    .phone .screen { width: %dpx; height: %dpx; border-radius: %dpx; overflow: hidden; background: %s; position: relative; }\n"
            "    .phone .screen img { position: absolute; left: 0; top: -%dpx; width: %dpx; height: auto; }\n"
            "    #%s-cam { position: absolute; inset: 0; }\n"
            "    #%s-zoom { position: absolute; inset: 0; }\n"
        ) % (p["left"], p["top"], p["width"], p["height"], p["radius"], self.c.get("bezel", "#1c1c22"), p["bezel"],
             self.c.get("bezel_edge", "#2a2a33"), p["img_width"], p["screen_h"], p["radius"] - 12, self.c["ground"],
             p["crop_top"], p["img_width"], sid, sid)

    def card_css(self):
        c = self.c
        return (
            "    .card { position: relative; width: 900px; background: %s; border: 1.5px solid %s33; border-radius: 16px; box-shadow: 0 4px 10px rgba(0,0,0,.05); padding: 26px 32px; display: flex; align-items: center; gap: 24px; color: %s; }\n"
            "    .card .icon { flex: none; width: 88px; height: 88px; border-radius: 44px; background: %s29; display: flex; align-items: center; justify-content: center; }\n"
            "    .card .icon img { width: 56px; height: 56px; }\n"
            "    .card .text { min-width: 0; }\n"
            "    .card .title { font-weight: 600; font-size: 36px; line-height: 1.3; }\n"
            "    .card .meta { color: %s; font-weight: 700; font-size: 28px; letter-spacing: .04em; margin-top: 8px; }\n"
        ) % (c["surface"], c["accent"], c["ink"], c["accent"], c["highlight"])

    def card_html(self, card, cid):
        icon = '<div class="icon"><img src="%s" alt="" /></div>' % esc(card["icon"]) if card.get("icon") else ""
        meta = '<div class="meta">%s</div>' % esc(card["meta"]) if card.get("meta") else ""
        return '<div class="card" id="%s">%s<div class="text"><div class="title">%s</div>%s</div></div>' % (cid, icon, esc(card["title"]), meta)

    def screens_html(self, sid, screens):
        return "\n".join('            <img id="%s-s%d" src="%s" alt="%s" />' % (sid, i, esc(s if "/" in s else "assets/screens/" + s), esc(os.path.splitext(os.path.basename(s))[0]))
                         for i, s in enumerate(screens))

    def phone_html(self, sid, screens, extra=""):
        return ('      <div id="%s-cam">\n       <div id="%s-zoom">\n        <div class="phone" id="%s-phone"><div class="screen">\n%s\n%s        </div></div>\n       </div>\n      </div>'
                % (sid, sid, sid, self.screens_html(sid, screens), extra))

    def label(self, s):
        """Optional eyebrow chip above the phone: {"label": {"n": "1/6", "text": "KCB M-Pesa"}}."""
        lb = s.get("label")
        if not lb:
            return "", "", ""
        sid = s["id"]; c = self.c
        css = ("    #%s-label { position: absolute; left: 0; right: 0; top: %dpx; display: flex; justify-content: center; }\n"
               "    #%s-label .chip { display: inline-flex; align-items: center; gap: 18px; background: %s; color: %s; font-weight: 800; font-size: 46px; padding: 18px 36px 18px 18px; border-radius: 999px; box-shadow: 0 10px 30px rgba(0,0,0,.08); border: 2px solid %s22; }\n"
               "    #%s-label .n { background: %s; color: #fff; font-size: 34px; font-weight: 900; padding: 10px 20px; border-radius: 999px; }\n"
               ) % (sid, lb.get("top", 150), sid, c["surface"], c["ink"], c["accent"], sid, c["accent"])
        n = '<span class="n">%s</span>' % esc(lb["n"]) if lb.get("n") else ""
        html_ = '      <div id="%s-label"><div class="chip">%s<span>%s</span></div></div>\n' % (sid, n, esc(lb["text"]))
        tl = '    tl.fromTo("#%s-label .chip", { y: -40, opacity: 0, scale: 0.9 }, { y: 0, opacity: 1, scale: 1, duration: 0.4, ease: "back.out(1.6)" }, %s);' % (sid, lb.get("at", 0.1))
        return css, html_, tl

    def cue(self, t, name, vol, note):
        self.sfx.append((round(t, 3), name, vol, note))

    # ---------- scene types ----------
    def scene_hook(self, s):
        sid = s["id"]; c = self.c
        pre = s.get("preloaded", 2)
        cards = s["cards"]; pops = s.get("pops", [])
        style = self.card_css() + (
            "    #%s-pile { position: absolute; left: 90px; top: 250px; width: 900px; display: flex; flex-direction: column; gap: 24px; }\n"
            "    #%s-line { position: absolute; left: 70px; right: 70px; top: 560px; text-align: center; color: %s; font-weight: 900; font-size: 128px; line-height: 1.02; letter-spacing: -.03em; }\n"
            "    #%s-line .q { color: %s; }\n"
            "    #%s-flood { position: absolute; left: %dpx; top: %dpx; width: 200px; height: 200px; margin-left: -100px; margin-top: -100px; border-radius: 50%%; background: %s; }\n"
        ) % (sid, sid, c["ink"], sid, c["highlight"], sid, self.W // 2, int(self.H * 0.78), c["flood"])
        markup = '      <div id="%s-pile" data-layout-allow-overlap>\n%s\n      </div>\n' % (sid, "\n".join("        " + self.card_html(cd, "%s-c%d" % (sid, i)) for i, cd in enumerate(cards)))
        tlj = []
        for i in range(len(cards)):
            if i < pre:
                tlj.append('    tl.fromTo("#%s-c%d", { y: 0, opacity: 1 }, { y: 0, opacity: 1, duration: 0.01 }, 0);' % (sid, i))
            else:
                t = pops[i - pre] if i - pre < len(pops) else 0.4 * (i - pre + 1)
                tlj.append('    tl.fromTo("#%s-c%d", { y: 140, opacity: 0, scale: 0.92, transformOrigin: "50%% 100%%" }, { y: 0, opacity: 1, scale: 1, duration: 0.35, ease: "back.out(1.4)" }, %s);' % (sid, i, t))
                self.cue(s["start"] + t, "pop" if (i - pre) % 2 == 0 else "click", 1.0 if (i - pre) % 2 == 0 else 0.9, "card lands")
        hero = s.get("hero")
        if hero:
            markup += '      <div id="%s-line">%s</div>\n' % (sid, hero_html(hero["text"]).replace(" / ", "<br />"))
            tlj.append('    tl.to("#%s-pile", { filter: "blur(7px)", opacity: 0.35, duration: 0.3, ease: "power2.inOut" }, %s);' % (sid, hero["at"] - 0.05))
            tlj.append('    tl.fromTo("#%s-line", { opacity: 0, scale: 1.35, filter: "blur(10px)" }, { opacity: 1, scale: 1, filter: "blur(0px)", duration: 0.32, ease: "expo.out" }, %s);' % (sid, hero["at"]))
            self.cue(s["start"] + hero["at"], "whoosh", 0.7, "hero line")
            self.cues.append((s["start"] + hero["at"], "hero line: " + hero["text"]))
        if s.get("flood_at") is not None:
            markup += '      <div id="%s-flood"></div>\n' % sid
            tlj.append('    tl.fromTo("#%s-flood", { scale: 0 }, { scale: 14, duration: 0.42, ease: "power3.in" }, %s);' % (sid, s["flood_at"]))
            self.cue(s["start"] + s["flood_at"], "whoosh", 0.4, "flood")
        self.cues.append((s["start"], "hook: %d cards pile in" % len(cards)))
        return style, markup, "\n".join(tlj), c["ground"]

    def scene_reveal(self, s):
        sid = s["id"]; c = self.c
        screens = s.get("screens", [])
        style = self.phone_css(sid) + (
            "    #%s-drain { position: absolute; inset: 0; background: %s; }\n"
            "    #%s-brand { position: absolute; left: 0; right: 0; top: 150px; height: 140px; display: flex; align-items: center; justify-content: center; gap: 28px; }\n"
            "    #%s-tile { width: 120px; height: 120px; border-radius: 30px; background: #fff; display: flex; align-items: center; justify-content: center; }\n"
            "    #%s-tile img { width: 104px; height: 104px; }\n"
            "    #%s-word { color: %s; font-weight: 900; font-size: 84px; letter-spacing: -.03em; }\n"
        ) % (sid, c["flood"], sid, sid, sid, sid, c["ink"])
        markup = self.phone_html(sid, screens) if screens else ""
        markup += '\n      <div id="%s-brand"><div id="%s-tile"><img src="%s" alt="%s mark" /></div><div id="%s-word">%s</div></div>\n' % (sid, sid, esc(self.b["logo"]), esc(self.b["name"]), sid, esc(self.b["name"]))
        tlj = []
        if s.get("drain", True):
            markup += '      <div id="%s-drain"></div>\n' % sid
            tlj.append('    tl.fromTo("#%s-drain", { opacity: 1 }, { opacity: 0, duration: 0.3, ease: "power2.inOut" }, 0);' % sid)
        for i in range(1, len(screens)):
            tlj.append('    gsap.set("#%s-s%d", { opacity: 0, x: %d });' % (sid, i, self.p["img_width"]))
        if screens:
            tlj.append('    tl.fromTo("#%s-phone", { y: 1000, scale: 0.9, transformOrigin: "50%% 100%%" }, { y: 0, scale: 1, duration: 0.8, ease: "expo.out" }, 0.05);' % sid)
        ba = s.get("brand_at", 0.15)
        tlj.append('    tl.fromTo("#%s-tile", { scale: 0, rotate: -12 }, { scale: 1, rotate: 0, duration: 0.5, ease: "back.out(1.6)" }, %s);' % (sid, ba))
        tlj.append('    tl.fromTo("#%s-word", { opacity: 0, filter: "blur(8px)", x: -20 }, { opacity: 1, filter: "blur(0px)", x: 0, duration: 0.3, ease: "power4.out" }, %s);' % (sid, ba + 0.05))
        self.cue(s["start"] + ba, "pop", 1.0, "brand mark lands")
        if s.get("push") and screens:
            # slow push-in on the phone so a held screen keeps moving
            tlj.append('    tl.fromTo("#%s-cam", { scale: 1, transformOrigin: "50%% 45%%" }, { scale: %s, duration: %s, ease: "sine.inOut", immediateRender: false }, 0.9);' % (sid, s["push"], round(s["duration"] - 1.0, 2)))
        for i, t in enumerate(s.get("swipes", [])):
            if i + 1 >= len(screens):
                break
            tlj.append('    tl.to("#%s-s%d", { x: -%d, duration: 0.45, ease: "power2.inOut" }, %s);' % (sid, i, self.p["img_width"], t))
            tlj.append('    tl.to("#%s-s%d", { x: 0, opacity: 1, duration: 0.45, ease: "power2.inOut" }, %s);' % (sid, i + 1, t))
            self.cue(s["start"] + t, "whoosh", 0.4, "screen swipe")
        self.cues.append((s["start"], "reveal: %s mark + name" % self.b["name"]))
        return style, markup, "\n".join(tlj), c["ground"]

    ICONS = {
        "bell": "M12 22c1.1 0 2-.9 2-2h-4c0 1.1.89 2 2 2zm6-6v-5c0-3.07-1.64-5.64-4.5-6.32V4c0-.83-.67-1.5-1.5-1.5s-1.5.67-1.5 1.5v.68C7.63 5.36 6 7.92 6 11v5l-2 2v1h16v-1l-2-2z",
        "tag": "M21.41 11.58l-9-9C12.05 2.22 11.55 2 11 2H4c-1.1 0-2 .9-2 2v7c0 .55.22 1.05.59 1.42l9 9c.36.36.86.58 1.41.58.55 0 1.05-.22 1.41-.59l7-7c.37-.36.59-.86.59-1.41 0-.55-.23-1.06-.59-1.42zM5.5 7C4.67 7 4 6.33 4 5.5S4.67 4 5.5 4 7 4.67 7 5.5 6.33 7 5.5 7z",
        "receipt": "M18 17H6v-2h12v2zm0-4H6v-2h12v2zm0-4H6V7h12v2zM3 22l1.5-1.5L6 22l1.5-1.5L9 22l1.5-1.5L12 22l1.5-1.5L15 22l1.5-1.5L18 22l1.5-1.5L21 22V2l-1.5 1.5L18 2l-1.5 1.5L15 2l-1.5 1.5L12 2l-1.5 1.5L9 2 7.5 3.5 6 2 4.5 3.5 3 2v20z",
        "bank": "M4 10v7h3v-7H4zm6 0v7h3v-7h-3zM2 22h19v-3H2v3zm14-12v7h3v-7h-3zm-4.5-9L2 6v2h19V6l-9.5-5z",
        "phone": "M17 1.01L7 1c-1.1 0-2 .9-2 2v18c0 1.1.9 2 2 2h10c1.1 0 2-.9 2-2V3c0-1.1-.9-1.99-2-1.99zM17 19H7V5h10v14z",
        "swap": "M16 17.01V10h-2v7.01h-3L15 21l4-3.99h-3zM9 3L5 6.99h3V14h2V6.99h3L9 3z",
    }

    def scene_menu(self, s):
        """Intro title + numbered menu of the updates.
        mode "build": title visible at frame 0, shrinks up at shrink_at, rows pop at row_times.
        mode "pick":  title small + rows static; row `pick` highlights, its badge flies to the chapter-card badge."""
        sid = s["id"]; c = self.c; b = self.b
        rows = s["rows"]; mode = s.get("mode", "build")
        top0, rh, gap = 640, 136, 22
        style = (
            "    #%s-glow { position: absolute; left: 540px; top: 640px; width: 1500px; height: 1500px; margin: -750px 0 0 -750px; border-radius: 50%%; background: radial-gradient(circle, %s2a 0%%, %s00 60%%); }\n"
            "    #%s-title { position: absolute; left: 0; right: 0; top: 300px; display: flex; flex-direction: column; align-items: center; transform-origin: 50%% 0%%; }\n"
            "    #%s-title .tile { width: 200px; height: 200px; border-radius: 52px; background: #fff; display: flex; align-items: center; justify-content: center; box-shadow: 0 24px 60px rgba(17,17,17,.14); }\n"
            "    #%s-title .tile img { width: 176px; height: 176px; }\n"
            "    #%s-title .k { margin-top: 56px; color: %s; font-weight: 800; font-size: 64px; letter-spacing: .01em; }\n"
            "    #%s-title .n { margin-top: 4px; color: %s; font-weight: 900; font-size: 128px; letter-spacing: -.03em; line-height: 1.02; }\n"
            "    .mrow { position: absolute; left: 80px; width: 920px; height: %dpx; background: #fff; border-radius: 30px; box-shadow: 0 10px 30px rgba(17,17,17,.08); border: 2px solid %s1f; display: flex; align-items: center; gap: 26px; padding: 0 30px; box-sizing: border-box; }\n"
            "    .mrow .bd { flex: none; width: 84px; height: 84px; border-radius: 50%%; background: %s; color: #fff; font-weight: 900; font-size: 50px; line-height: 84px; text-align: center; }\n"
            "    .mrow .ic { flex: none; width: 76px; height: 76px; border-radius: 22px; background: %s14; display: flex; align-items: center; justify-content: center; overflow: hidden; }\n"
            "    .mrow .ic img { width: 76px; height: 76px; object-fit: contain; background: #fff; }\n"
            "    .mrow .ic svg { width: 46px; height: 46px; fill: %s; }\n"
            "    .mrow .tx { color: %s; font-weight: 800; font-size: 54px; white-space: nowrap; }\n"
            "    .mrow .tx small { display: block; color: #5C6670; font-weight: 700; font-size: 32px; margin-top: 2px; }\n"
        ) % (sid, c["accent"], c["accent"], sid, sid, sid, sid, c["accent"], sid, c["ink"], rh, c["accent"], c["accent"], c["accent"], c["accent"], c["ink"])
        rhtml = []
        for i, r in enumerate(rows):
            if r.get("img"):
                ic = '<img src="%s" alt="" />' % esc(r["img"])
            else:
                ic = '<svg viewBox="0 0 24 24"><path d="%s"/></svg>' % self.ICONS[r["icon"]]
            sub = "<small>%s</small>" % esc(r["sub"]) if r.get("sub") else ""
            rhtml.append('<div class="mrow" id="%s-r%d" style="top: %dpx"><div class="bd" id="%s-b%d">%d</div><div class="ic">%s</div><div class="tx">%s%s</div></div>'
                         % (sid, i, top0 + i * (rh + gap), sid, i, i + 1, ic, esc(r["name"]), sub))
        markup = ('      <div id="%s-glow"></div>\n      <div id="%s-title"><div class="tile"><img src="%s" alt="%s" /></div><div class="k">What\'s new in</div><div class="n">%s</div></div>\n      %s\n'
                  % (sid, sid, esc(b["logo"]), esc(b["name"]), esc(b["name"]), "\n      ".join(rhtml)))
        tlj = []
        small = '{ scale: 0.6, y: -170 }'
        if mode == "build":
            tlj.append('    tl.fromTo("#%s-title", { scale: 1.1 }, { scale: 1, duration: 0.7, ease: "expo.out", immediateRender: false }, 0);' % sid)
            tlj.append('    tl.fromTo("#%s-glow", { scale: 0.8 }, { scale: 1.15, duration: %s, ease: "sine.inOut", immediateRender: false }, 0);' % (sid, s["duration"]))
            self.cue(s["start"] + 0.05, "impact", 0.35, "title")
            sa = s["shrink_at"]
            tlj.append('    tl.fromTo("#%s-title", { scale: 1, y: 0 }, { scale: 0.6, y: -170, duration: 0.55, ease: "power3.inOut", immediateRender: false }, %s);' % (sid, sa))
            self.cue(s["start"] + sa, "whoosh", 0.4, "title up")
            for i, t in enumerate(s["row_times"]):
                tlj.append('    gsap.set("#%s-r%d", { opacity: 0, x: 80 });' % (sid, i))
                tlj.append('    tl.fromTo("#%s-r%d", { opacity: 0, x: 80, scale: 0.96 }, { opacity: 1, x: 0, scale: 1, duration: 0.4, ease: "back.out(1.5)", immediateRender: false }, %s);' % (sid, i, t))
                self.cue(s["start"] + t, "pop" if i % 2 == 0 else "click", 0.7, "menu row")
            if s.get("out_at") is not None:
                oa = s["out_at"]
                tlj.append('    tl.fromTo(".mrow", { opacity: 1, y: 0 }, { opacity: 0, y: -60, duration: 0.35, ease: "power2.in", stagger: 0.03, immediateRender: false }, %s);' % oa)
                tlj.append('    tl.fromTo("#%s-title", { opacity: 1 }, { opacity: 0, duration: 0.3, immediateRender: false }, %s);' % (sid, oa))
                # note: title y is relative to the shrunk state; keep scale
        else:
            tlj.append('    gsap.set("#%s-title", %s);' % (sid, small))
            tlj.append('    tl.fromTo(".mrow", { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 0.3, ease: "power3.out", stagger: 0.025, immediateRender: false }, 0);')
            n = s["pick"] - 1; pa = s["pick_at"]; fa = s["fly_at"]
            others = ", ".join("#%s-r%d" % (sid, i) for i in range(len(rows)) if i != n)
            tlj.append('    tl.fromTo("%s", { opacity: 1 }, { opacity: 0.28, duration: 0.3, immediateRender: false }, %s);' % (others, pa))
            tlj.append('    tl.fromTo("#%s-r%d", { scale: 1, boxShadow: "0 10px 30px rgba(17,17,17,.08)" }, { scale: 1.05, boxShadow: "0 0 0 8px %s55, 0 20px 50px rgba(17,17,17,.14)", duration: 0.35, ease: "back.out(2)", immediateRender: false }, %s);' % (sid, n, c["accent"], pa))
            self.cue(s["start"] + pa, "click", 0.9, "pick row")
            # badge flight: row badge centre -> chapter badge centre (540, 585), 84px -> 230px
            bx = 80 + 30 + 42; by = top0 + n * (rh + gap) + rh / 2
            dx, dy = 540 - bx, 585 - by
            tlj.append('    tl.fromTo("%s", { opacity: 0.28 }, { opacity: 0, duration: 0.3, immediateRender: false }, %s);' % (others, fa))
            tlj.append('    tl.fromTo("#%s-title, #%s-r%d .ic, #%s-r%d .tx", { opacity: 1 }, { opacity: 0, duration: 0.3, immediateRender: false }, %s);' % (sid, sid, n, sid, n, fa))
            tlj.append('    tl.fromTo("#%s-r%d", { backgroundColor: "rgba(255,255,255,1)", borderColor: "%s1f", boxShadow: "0 0 0 8px %s55, 0 20px 50px rgba(17,17,17,.14)" }, { backgroundColor: "rgba(255,255,255,0)", borderColor: "%s00", boxShadow: "0 0 0 0px %s00, 0 0px 0px rgba(17,17,17,0)", duration: 0.3, immediateRender: false }, %s);' % (sid, n, c["accent"], c["accent"], c["accent"], c["accent"], fa))
            tlj.append('    tl.fromTo("#%s-b%d", { x: 0, y: 0, scale: 1 }, { x: %.1f, y: %.1f, scale: %.3f, duration: 0.6, ease: "power3.inOut", immediateRender: false }, %s);' % (sid, n, dx / 1.05, dy / 1.05, 230 / 84 / 1.05, fa))
            self.cue(s["start"] + fa, "whoosh", 0.5, "badge flight")
        self.cues.append((s["start"], "menu (%s)" % mode))
        return style, markup, "\n".join(tlj), c["ground"]

    def scene_chapter(self, s):
        """Section card: number badge, kicker, title, question, progress dots."""
        sid = s["id"]; c = self.c
        n, total = s["n"], s.get("of", 6)
        style = (
            "    #%s-wrap { position: absolute; left: 80px; right: 80px; top: 470px; display: flex; flex-direction: column; align-items: center; text-align: center; }\n"
            "    #%s-badge { width: 230px; height: 230px; border-radius: 50%%; background: %s; color: #fff; font-weight: 900; font-size: 140px; line-height: 230px; box-shadow: 0 24px 60px %s55; }\n"
            "    #%s-kick { margin-top: 64px; color: %s; font-weight: 800; font-size: 40px; letter-spacing: .14em; }\n"
            "    #%s-title { margin-top: 22px; color: %s; font-weight: 900; font-size: 96px; line-height: 1.05; letter-spacing: -.02em; }\n"
            "    #%s-q { margin-top: 44px; color: #5C6670; font-weight: 700; font-size: 58px; line-height: 1.2; }\n"
            "    #%s-dots { position: absolute; left: 0; right: 0; top: 1520px; display: flex; justify-content: center; gap: 26px; }\n"
            "    #%s-dots .d { width: 30px; height: 30px; border-radius: 50%%; background: %s33; }\n"
            "    #%s-dots .d.on { background: %s; width: 84px; border-radius: 15px; }\n"
            "    #%s-glow { position: absolute; left: 540px; top: 700px; width: 1400px; height: 1400px; margin: -700px 0 0 -700px; border-radius: 50%%; background: radial-gradient(circle, %s22 0%%, %s00 62%%); }\n"
        ) % (sid, sid, c["accent"], c["accent"], sid, c["accent"], sid, c["ink"], sid, sid, sid, c["accent"], sid, c["accent"], sid, c["accent"], c["accent"])
        dots = "".join('<div class="d%s"></div>' % (" on" if i + 1 == n else "") for i in range(total))
        markup = ('      <div id="%s-glow"></div>\n      <div id="%s-wrap"><div id="%s-badge">%d</div><div id="%s-kick">NEW · %d OF %d</div>'
                  '<div id="%s-title">%s</div><div id="%s-q">%s</div></div>\n      <div id="%s-dots">%s</div>\n') % (
            sid, sid, sid, n, sid, n, total, sid, esc(s["title"]), sid, esc(s["question"]), sid, dots)
        tlj = [
            ('    tl.fromTo("#%s-badge", { scale: 1 }, { scale: 1.06, duration: 0.25, ease: "sine.out", yoyo: true, repeat: 1, immediateRender: false }, 0.02);' % sid) if s.get("steady") else
            '    tl.fromTo("#%s-badge", { scale: 0.4, rotate: -20 }, { scale: 1, rotate: 0, duration: 0.55, ease: "back.out(1.7)" }, 0.05);' % sid,
            '    tl.fromTo("#%s-kick", { y: 30, opacity: 0 }, { y: 0, opacity: 1, duration: 0.35, ease: "power3.out" }, 0.3);' % sid,
            '    tl.fromTo("#%s-title", { y: 50, opacity: 0, filter: "blur(8px)" }, { y: 0, opacity: 1, filter: "blur(0px)", duration: 0.45, ease: "expo.out" }, 0.4);' % sid,
            '    tl.fromTo("#%s-q", { y: 40, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "expo.out" }, %s);' % (sid, s.get("q_at", 0.9)),
            '    tl.fromTo("#%s-dots", { opacity: 0 }, { opacity: 1, duration: 0.3 }, 0.5);' % sid,
            '    tl.fromTo("#%s-glow", { scale: 0.85 }, { scale: 1.12, duration: %s, ease: "sine.inOut", immediateRender: false }, 0);' % (sid, s["duration"]),
            '    tl.fromTo("#%s-wrap", { scale: 1 }, { scale: 1.04, duration: %s, ease: "sine.inOut", immediateRender: false }, 0.9);' % (sid, round(s["duration"] - 0.9, 2)),
        ]
        if not s.get("steady"):
            self.cue(s["start"] + 0.05, "pop", 0.9, "chapter badge")
        self.cues.append((s["start"], "chapter %d: %s" % (n, s["title"])))
        return style, markup, "\n".join(tlj), c["ground"]

    def scene_feature(self, s):
        sid = s["id"]; c = self.c; p = self.p
        screens = s["screens"]
        style = self.phone_css(sid) + self.card_css() + (
            "    #%s-card { position: absolute; left: 90px; top: 120px; width: 900px; }\n"
            "    #%s-bar { position: absolute; left: 36px; height: 8px; width: 0; background: %s; border-radius: 4px; }\n"
            "    #%s-ov { position: absolute; left: 0; top: -%dpx; width: %dpx; height: auto; }\n"
        ) % (sid, sid, c["accent"], sid, p["crop_top"], p["img_width"])
        extra = ""
        overlays = [m for m in s["moves"] if m["kind"] == "overlay"]
        if overlays:
            src = overlays[0]["src"]
            extra = '            <img id="%s-ov" src="%s" alt="overlay" />\n' % (sid, esc(src if "/" in src else "assets/screens/" + src))
        swipes = [m for m in s["moves"] if m["kind"] == "swipe-h"]
        Kp = p["img_width"] / 900.0
        for i, m in enumerate(swipes):
            m["_id"] = "%s-sw%d" % (sid, i)
            x1, y1, x2, y2 = m["box"]
            bw, bh = round((x2 - x1) * Kp), round((y2 - y1) * Kp)
            def crop(src, cls):
                src = src if "/" in src else "assets/screens/" + src
                return ('<img class="%s" src="%s" alt="" style="position: absolute; left: %dpx; top: %dpx; width: %dpx; height: auto;" />'
                        % (cls, esc(src), -round(x1 * Kp), -round(y1 * Kp), p["img_width"]))
            extra += ('            <div id="%s" style="position: absolute; left: %dpx; top: %dpx; width: %dpx; height: %dpx; overflow: hidden; opacity: 0;">'
                      '<div class="a" style="position: absolute; inset: 0;">%s</div><div class="b" style="position: absolute; inset: 0;">%s</div></div>\n'
                      % (m["_id"], round(x1 * Kp), round(y1 * Kp - p["crop_top"]), bw, bh, crop(m["from"], "ia"), crop(m["to"], "ib")))
            extra += ('            <div id="%s-f" style="position: absolute; left: %dpx; top: %dpx; width: 96px; height: 96px; margin: -48px 0 0 -48px; border-radius: 50%%; background: rgba(255,255,255,.85); border: 6px solid %s; box-shadow: 0 0 30px %s; opacity: 0;"></div>\n'
                      % (m["_id"], round((x1 + (x2 - x1) * 0.82) * Kp), round(((y1 + y2) / 2) * Kp - p["crop_top"]), c["accent"], c.get("tap_glow", "#4fc385")))
            m["_bw"] = bw
        marks = [m for m in s["moves"] if m["kind"] == "mark"]
        Km = p["img_width"] / 900.0
        if marks:
            style += ("    .mk { position: absolute; left: 0; top: 0; width: %dpx; height: %dpx; overflow: visible; pointer-events: none; }\n"
                      "    .pen { position: absolute; left: 0; top: 0; width: 1px; height: 1px; filter: drop-shadow(0 6px 8px rgba(0,0,0,.35)); }\n") % (p["img_width"], p["screen_h"])
        for i, m in enumerate(marks):
            m["_id"] = "%s-mk%d" % (sid, i)
            b = m["box"]
            box = [b[0] * Km, b[1] * Km - p["crop_top"], b[2] * Km, b[3] * Km - p["crop_top"]]
            pts, keys, L = mark_points(box, m.get("shape", "circle"), i + len(sid))
            path = "M" + " L".join("%.1f %.1f" % xy for xy in pts)
            col = m.get("color", c.get("pencil", "#E4572E"))
            # no SVG filter: feTurbulence/feDisplacementMap rasterise differently per render worker -> loop blinks
            extra += ('            <svg class="mk" id="%s">'
                      '<path class="p1" d="%s" fill="none" stroke="%s" stroke-width="7" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="%.1f" stroke-dashoffset="%.1f"/>'
                      '<path class="p2" d="%s" fill="none" stroke="%s" stroke-opacity=".45" stroke-width="3" stroke-linecap="round" transform="translate(2.5 -2)" stroke-dasharray="%.1f" stroke-dashoffset="%.1f"/></svg>\n'
                      % (m["_id"], path, col, L + 2, L + 2, path, col, L + 2, L + 2))
            if m.get("pencil", False):
                extra += '            <div class="pen" id="%s-pen">%s</div>\n' % (m["_id"], PENCIL_SVG.replace("{body}", col).replace("{lead}", col))
            m["_keys"], m["_L"] = keys, L
        taps = [m for m in s["moves"] if m["kind"] == "tap"]
        K = p["img_width"] / 900.0
        for i, m in enumerate(taps):
            m["_id"] = "%s-tap%d" % (sid, i)
            extra += '            <div class="tap" id="%s" style="left: %dpx; top: %dpx"></div>\n' % (m["_id"], round(m["x"] * K), round(m["y"] * K - p["crop_top"]))
        if taps:
            style += ("    .tap { position: absolute; width: 120px; height: 120px; margin: -60px 0 0 -60px; border-radius: 50%%; border: 7px solid %s; background: %s40; box-shadow: 0 0 0 14px %s26, 0 0 40px %s; }\n"
                      % (c["accent"], c["accent"], c["accent"], c.get("tap_glow", "#4fc385")))
        bars = [m for m in s["moves"] if m["kind"] == "progress"]
        if bars:
            extra += '            <div id="%s-bar"></div>\n' % sid
        markup = self.phone_html(sid, screens, extra)
        drops = [m for m in s["moves"] if m["kind"] == "card-drop"]
        if drops:
            d = drops[0]
            markup += '\n      <div id="%s-card">%s</div>\n' % (sid, self.card_html(d, sid + "-cardel"))
        tlj = []
        for i in range(1, len(screens)):
            tlj.append('    gsap.set("#%s-s%d", { opacity: 0, y: 260 });' % (sid, i))
        if overlays:
            tlj.append('    gsap.set("#%s-ov", { opacity: 0, y: -200 });' % sid)
        tr = s.get("transition", "cut")
        if tr == "whip-over":
            frm = s.get("from", "bottom")
            start = {"bottom": "y: 900", "top": "y: -900", "right": "x: 1100", "left": "x: -1100"}[frm]
            end = "y: 0" if frm in ("bottom", "top") else "x: 0"
            tlj.append('    tl.fromTo("#%s-cam", { %s, filter: "blur(10px)" }, { %s, filter: "blur(0px)", duration: 0.4, ease: "expo.out" }, 0);' % (sid, start, end))
            self.cue(s["start"], "whoosh", 0.5, "%s whips in" % sid)
        elif tr == "settle":
            tlj.append('    tl.fromTo("#%s-cam", { scale: 1.18, x: 0, y: 0, filter: "blur(6px)", transformOrigin: "50%% 50%%" }, { scale: 1, filter: "blur(0px)", duration: 0.45, ease: "expo.out" }, 0);' % sid)
        current = 0
        for m in s["moves"]:
            t = m["t"]; k = m["kind"]; at = s["start"] + t
            if k == "card-drop":
                tlj.append('    tl.fromTo("#%s-card", { y: -420, opacity: 0 }, { y: 0, opacity: 1, duration: 0.45, ease: "expo.out" }, %s);' % (sid, t))
                tlj.append('    tl.to("#%s-card", { y: 760, scale: 0.12, opacity: 0, transformOrigin: "50%% 50%%", duration: 0.45, ease: "power3.in" }, %s);' % (sid, m["drop_at"]))
                self.cue(at, "whoosh", 0.4, "card arrives"); self.cue(s["start"] + m["drop_at"], "whoosh", 0.5, "card drops into phone")
                self.cues.append((at, "%s: card '%s' arrives, drops at %.1fs" % (sid, m["title"], s["start"] + m["drop_at"])))
            elif k == "show":
                n = m["screen"]
                if m.get("rise"):
                    tlj.append('    gsap.set("#%s-s%d", { y: 120 });' % (sid, n))
                    tlj.append('    tl.to("#%s-s%d", { opacity: 0, duration: 0.1 }, %s);' % (sid, current, t))
                    tlj.append('    tl.to("#%s-s%d", { opacity: 1, y: 0, duration: 0.3, ease: "expo.out" }, %s);' % (sid, n, t))
                elif m.get("settle"):
                    tlj.append('    gsap.set("#%s-s%d", { y: 0, scale: 1.06, transformOrigin: "50%% 30%%" });' % (sid, n))
                    tlj.append('    tl.to("#%s-s%d", { opacity: 0, duration: 0.1 }, %s);' % (sid, current, t))
                    tlj.append('    tl.to("#%s-s%d", { opacity: 1, scale: 1, duration: 0.25, ease: "expo.out" }, %s);' % (sid, n, t))
                    self.cue(at, "pop", 1.0, "screen lands")
                else:
                    tlj.append('    gsap.set("#%s-s%d", { y: 0 });' % (sid, n))
                    tlj.append('    tl.to("#%s-s%d", { opacity: 0, duration: 0.1 }, %s);' % (sid, current, t))
                    tlj.append('    tl.to("#%s-s%d", { opacity: 1, duration: 0.18, ease: "power2.out" }, %s);' % (sid, n, t))
                self.cues.append((at, "%s: show %s" % (sid, screens[n])))
                current = n
            elif k == "scroll":
                n = m["screen"]
                tlj.append('    tl.to("#%s-s%d", { y: -260, opacity: 0, duration: 0.45, ease: "power2.inOut" }, %s);' % (sid, current, t))
                tlj.append('    tl.to("#%s-s%d", { y: 0, opacity: 1, duration: 0.45, ease: "power2.inOut" }, %s);' % (sid, n, t))
                self.cue(at, "whoosh", 0.4, "scroll"); self.cues.append((at, "%s: scroll to %s" % (sid, screens[n])))
                current = n
            elif k == "punch":
                tlj.append('    tl.to("#%s-cam", { scale: %s, x: %s, y: %s, duration: %s, ease: "power2.inOut", transformOrigin: "50%% 50%%" }, %s);' % (sid, m.get("scale", 1.5), m.get("x", 0), m.get("y", 0), m.get("duration", 0.6), t))
                self.cue(at, "click", 0.9, "punch-in"); self.cues.append((at, "%s: punch-in ×%s" % (sid, m.get("scale", 1.5))))
            elif k == "reset":
                tlj.append('    tl.to("#%s-cam", { scale: 1, x: 0, y: 0, duration: %s, ease: "power2.inOut" }, %s);' % (sid, m.get("duration", 0.5), t))
            elif k == "overlay":
                tlj.append('    tl.to("#%s-ov", { opacity: 1, y: 0, duration: 0.4, ease: "expo.out" }, %s);' % (sid, t))
                self.cue(at, "notification", 0.6, "overlay drops in"); self.cues.append((at, "%s: overlay %s" % (sid, m["src"])))
            elif k == "overlay-out":
                tlj.append('    tl.to("#%s-ov", { opacity: 0, y: -200, duration: 0.35, ease: "power2.in" }, %s);' % (sid, t))
            elif k == "progress":
                tlj.append('    gsap.set("#%s-bar", { top: %d });' % (sid, m.get("top", 1140)))
                tlj.append('    tl.fromTo("#%s-bar", { width: 0, opacity: 1 }, { width: %d, duration: %s, ease: "power1.inOut" }, %s);' % (sid, m.get("width", 660), m.get("duration", 1.5), t))
                tlj.append('    tl.to("#%s-bar", { opacity: 0, duration: 0.05 }, %s);' % (sid, t + m.get("duration", 1.5) + 0.2))
            elif k == "zoom-through":
                tlj.append('    tl.fromTo("#%s-zoom", { scale: 1, transformOrigin: "%s" }, { scale: 3.4, duration: 0.5, ease: "power3.in" }, %s);' % (sid, m.get("origin", "50% 90%"), t))
                self.cue(at, "click", 1.4, "tap (zoom-through)"); self.cues.append((at, "%s: zoom through %s" % (sid, m.get("origin"))))
            elif k == "mark":
                # all tweens are fromTo with absolute values: the renderer seeks frames out of order
                # (parallel workers), and plain .to()/relative values make the loop blink between frames
                i_, keys, L = m["_id"], m["_keys"], m["_L"]; d = m.get("duration", 0.75); hold = m.get("hold", 2.4)
                seg = round(d / (len(keys) - 1), 4)
                x0, y0 = keys[0]; xe, ye = keys[-1]
                if m.get("pencil", False): tlj.append('    gsap.set("#%s-pen", { x: %.1f, y: %.1f, opacity: 0 });' % (i_, x0, y0))
                if m.get("pencil", False): tlj.append('    tl.fromTo("#%s-pen", { opacity: 0 }, { opacity: 1, duration: 0.15, immediateRender: false }, %s);' % (i_, round(t - 0.18, 3)))
                tlj.append('    tl.fromTo("#%s path", { strokeDashoffset: %.1f }, { strokeDashoffset: 0, duration: %s, ease: "none", immediateRender: false }, %s);' % (i_, L + 2, d, t))
                for q in (range(1, len(keys)) if m.get("pencil", False) else []):
                    (ax, ay), (bx, by) = keys[q - 1], keys[q]
                    if m.get("pencil", False): tlj.append('    tl.fromTo("#%s-pen", { x: %.1f, y: %.1f }, { x: %.1f, y: %.1f, duration: %s, ease: "none", immediateRender: false }, %s);'
                               % (i_, ax, ay, bx, by, seg, round(t + seg * (q - 1), 4)))
                if m.get("pencil", False): tlj.append('    tl.fromTo("#%s-pen", { opacity: 1, x: %.1f, y: %.1f }, { opacity: 0, x: %.1f, y: %.1f, duration: 0.3, ease: "power2.in", immediateRender: false }, %s);'
                           % (i_, xe, ye, xe + 40, ye - 50, round(t + d + 0.05, 3)))
                tlj.append('    tl.fromTo("#%s", { opacity: 1 }, { opacity: 0, duration: 0.25, immediateRender: false }, %s);' % (i_, round(t + d + hold, 3)))
                self.cue(at, "pencil", 0.9, "pencil highlight"); self.cues.append((at, "%s: pencil mark" % sid))
            elif k == "swipe-h":
                i_, bw = m["_id"], m["_bw"]; d = m.get("duration", 0.55); lead = m.get("lead", 0.7)
                travel = round(bw * 0.62)
                tlj.append('    gsap.set("#%s .b", { x: %d });' % (i_, bw))
                tlj.append('    tl.set("#%s", { opacity: 1 }, %s);' % (i_, round(t - lead, 3)))
                tlj.append('    tl.fromTo("#%s-f", { opacity: 0, scale: 0.5 }, { opacity: 1, scale: 1, duration: 0.25, ease: "back.out(2)", immediateRender: false }, %s);' % (i_, round(t - lead, 3)))
                tlj.append('    tl.to("#%s-f", { x: -%d, duration: %s, ease: "power2.inOut" }, %s);' % (i_, travel, d, t))
                tlj.append('    tl.to("#%s .a", { x: -%d, duration: %s, ease: "power2.inOut" }, %s);' % (i_, bw, d, t))
                tlj.append('    tl.to("#%s .b", { x: 0, duration: %s, ease: "power2.inOut" }, %s);' % (i_, d, t))
                tlj.append('    tl.to("#%s-f", { opacity: 0, scale: 0.6, duration: 0.25 }, %s);' % (i_, round(t + d, 3)))
                self.cue(at, "whoosh", 0.6, "swipe left"); self.cues.append((at, "%s: swipe left" % sid))
            elif k == "tap":
                i_ = m["_id"]; lead = m.get("lead", 0.9)
                tlj.append('    gsap.set("#%s", { opacity: 0, scale: 0.3 });' % i_)
                tlj.append('    tl.fromTo("#%s", { opacity: 0, scale: 0.3 }, { opacity: 1, scale: 1, duration: 0.3, ease: "back.out(2)", immediateRender: false }, %s);' % (i_, round(t - lead, 3)))
                half = round(max(0.05, (lead - 0.36) / 2), 3)
                tlj.append('    tl.to("#%s", { scale: 1.14, duration: %s, ease: "sine.inOut", yoyo: true, repeat: 1 }, %s);' % (i_, half, round(t - lead + 0.3, 3)))
                tlj.append('    tl.to("#%s", { scale: 0.78, duration: 0.08, ease: "power2.in" }, %s);' % (i_, t))
                tlj.append('    tl.to("#%s", { scale: 1.9, opacity: 0, duration: 0.42, ease: "power2.out" }, %s);' % (i_, round(t + 0.08, 3)))
                self.cue(at, "click", 1.0, "tap"); self.cues.append((at, "%s: tap %s,%s" % (sid, m["x"], m["y"])))
            elif k == "hide":
                tlj.append('    tl.set("#%s-s%d", { opacity: 0 }, %s);' % (sid, m["screen"], t))
            else:
                sys.exit("unknown move kind %r in scene %s" % (k, sid))
        bg = "transparent" if tr == "whip-over" else c["ground"]
        self.cues.append((s["start"], "%s: %s" % (sid, screens[0])))
        return style, markup, "\n".join(tlj), bg

    def scene_endcard(self, s):
        sid = s["id"]; c = self.c; b = self.b
        style = (
            "    #%s-flood { position: absolute; inset: 0; background: %s; }\n"
            "    #%s-tile { position: absolute; left: %dpx; top: 460px; width: 300px; height: 300px; border-radius: 72px; background: #fff; display: flex; align-items: center; justify-content: center; box-shadow: 0 30px 70px rgba(0,0,0,.25); }\n"
            "    #%s-tile img { width: 268px; height: 268px; }\n"
            "    #%s-name { position: absolute; left: 0; right: 0; top: 810px; text-align: center; color: %s; font-weight: 900; font-size: 104px; letter-spacing: -.03em; }\n"
            "    #%s-claim { position: absolute; left: 50px; right: 50px; top: 960px; text-align: center; color: %s; font-weight: 600; font-size: 54px; line-height: 1.25; white-space: nowrap; }\n"
            "    .badge { position: absolute; left: %dpx; width: 500px; }\n    .badge img { width: 500px; height: auto; display: block; }\n"
        ) % (sid, c["flood"], sid, self.W // 2 - 150, sid, sid, c.get("ink_on_flood", "#ffffff"), sid, c.get("ink_on_flood", "#ffffff"), self.W // 2 - 250)
        markup = '      <div id="%s-flood"></div>\n      <div id="%s-tile"><img src="%s" alt="%s" /></div>\n      <div id="%s-name">%s</div>\n      <div id="%s-claim" data-var-text="claim">%s</div>\n' % (
            sid, sid, esc(b["logo"]), esc(b["name"]), sid, esc(b["name"]), sid, esc(b["claim"]))
        tlj = ['    tl.fromTo("#%s-flood", { clipPath: "inset(100%% 0 0 0)" }, { clipPath: "inset(0%% 0 0 0)", duration: 0.45, ease: "power2.inOut" }, 0);' % sid]
        self.cue(s["start"], "whoosh", 0.5, "flood")
        ta, na, ca = s.get("tile_at", 0.4), s.get("name_at", 0.75), s.get("claim_at", 1.75)
        tlj.append('    tl.fromTo("#%s-tile", { scale: 0, rotate: -10 }, { scale: 1, rotate: 0, duration: 0.55, ease: "back.out(1.5)" }, %s);' % (sid, ta))
        tlj.append('    tl.fromTo("#%s-name", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.25, ease: "power4.out" }, %s);' % (sid, na))
        tlj.append('    tl.fromTo("#%s-claim", { opacity: 0, filter: "blur(8px)" }, { opacity: 1, filter: "blur(0px)", duration: 0.25, ease: "power4.out" }, %s);' % (sid, ca))
        self.cue(s["start"] + ta, "impact", 0.45, "mark lands")
        for i, bd in enumerate(s.get("badges", b.get("badges", []))):
            top = 1110 + i * 190
            markup += '      <div class="badge" id="%s-badge%d" style="top: %dpx"><img src="%s" alt="store badge" /></div>\n' % (sid, i, top, esc(bd["src"]))
            tlj.append('    tl.fromTo("#%s-badge%d", { y: 200, opacity: 0 }, { y: 0, opacity: 1, duration: 0.5, ease: "expo.out" }, %s);' % (sid, i, bd["at"]))
            self.cue(s["start"] + bd["at"], "pop", 1.0, "badge")
        self.cues.append((s["start"], "end card: mark, name, claim, badges"))
        return style, markup, "\n".join(tlj), "transparent" if s.get("transition", "flood") == "flood" else c["ground"]

    # ---------- assembly ----------
    def run(self):
        sb, v = self.sb, self.v
        os.makedirs(os.path.join(self.out, "compositions"), exist_ok=True)
        hosts, z = [], 1
        for s in sb["scenes"]:
            fn = getattr(self, "scene_" + s["type"].replace("-", "_").replace("hook_cards", "hook"))
            style, markup, timeline, bg = fn(s)
            lcss, lhtml, ltl = self.label(s)
            style, markup, timeline = style + lcss, markup + lhtml, timeline + ("\n" + ltl if ltl else "")
            page = fill(tpl("scene.html"), font_faces=self.font_faces, root_background=bg, font_fallback=self.font_fallback,
                        id=s["id"], width=self.W, height=self.H, duration=s["duration"], style=style, markup=markup, timeline=timeline)
            with open(os.path.join(self.out, "compositions", s["id"] + ".html"), "w") as f:
                f.write(page)
            lane = 1 if s.get("transition", "cut") in ("cut", "settle") else 2
            hosts.append('      <div id="%s" data-composition-id="%s" data-composition-src="compositions/%s.html" data-track-kind="graphics" data-start="%s" data-duration="%s" data-track-index="%d" data-width="%d" data-height="%d" style="z-index: %d"></div>'
                         % (s["id"], s["id"], s["id"], s["start"], s["duration"], lane, self.W, self.H, z))
            z += 1
        # captions
        caps = sb.get("captions", [])
        cap_host = ""
        if caps:
            cs = v.get("captions", {})
            divs, groups = [], []
            for i, cp in enumerate(caps, 1):
                divs.append('    <div id="cap%d" class="clip cap" data-start="%s" data-duration="%s" data-layout-allow-caption-zone><div class="pill">%s</div></div>'
                            % (i, cp["start"], round(cp["end"] - cp["start"], 3), rich(cp["text"])))
                groups.append(["#cap%d" % i, cp["start"], cp["end"]])
            page = fill(tpl("captions.html"), font_faces=self.font_faces, font_fallback=self.font_fallback, top=cs.get("top", 1620), size=cs.get("size", 56),
                        pill=cs.get("pill", "rgba(15,15,19,.78)"), ink=self.c["ink"], highlight=self.c["highlight"], width=self.W, height=self.H,
                        caption_divs="\n".join(divs), groups=json.dumps(groups))
            with open(os.path.join(self.out, "compositions", "captions.html"), "w") as f:
                f.write(page)
            cap_host = '      <div id="captions" data-composition-id="captions" data-composition-src="compositions/captions.html" data-track-kind="captions" data-start="0" data-duration="%s" data-track-index="3" data-width="%d" data-height="%d" style="z-index: 9"></div>' % (v["duration"], self.W, self.H)
        # audio
        clips = []
        m = v.get("music")
        if m and m.get("src"):
            clips.append('      <audio id="music" class="clip" src="%s" data-start="0" data-duration="%s" data-volume="%s" data-fade-in="%s" data-fade-out="%s" data-track-index="4"></audio>'
                         % (m["src"], m.get("duration", v["duration"]), m.get("volume", 0.5), m.get("fade_in", 0.5), m.get("fade_out", 2)))
        for vo in sb.get("voice", []):
            if not vo.get("duration"):
                print("warning: voice %s has no duration — run scripts/tts.sh first" % vo["id"])
            clips.append('      <audio id="%s" class="clip" src="%s" data-start="%s" data-duration="%s" data-volume="%s" data-track-index="5"></audio>'
                         % (vo["id"], vo.get("src", "assets/audio/%s.wav" % vo["id"]), vo["start"], vo.get("duration", 3), vo.get("volume", 2.2)))
        sfx_cfg = sb.get("sfx", {})
        k = sfx_cfg.get("scale", 1.0)
        cues = [(t, n, round(v * k, 3), note) for t, n, v, note in self.sfx] if sfx_cfg.get("auto", True) else []
        cues += [(x["t"], x["name"], x.get("volume", 1.0), x.get("note", "manual")) for x in sfx_cfg.get("extra", [])]
        cues.sort()
        if cues and not sfx_cfg.get("off"):
            clips.append("      <!-- UI sounds: bundled HyperFrames library (CC0); each placed so its peak lands one frame after the picture -->")
            lane_end = {}
            for i, (t, name, vol, note) in enumerate(cues, 1):
                f = SFX[name]
                st = round(t - f["peak"] + FRAME, 3)
                lane = next(l for l in range(7, 20) if lane_end.get(l, -1) <= st - 0.02)
                lane_end[lane] = st + f["dur"]
                clips.append('      <audio id="sfx%02d" class="clip" src="%s" data-start="%s" data-duration="%s" data-volume="%s" data-track-index="%d"></audio>'
                             % (i, f["file"], st, f["dur"], vol, lane))
        c = self.c
        css_vars = "\n".join("        --%s: %s;" % (k, val) for k, val in c.items()) + '\n        --font-display: %s;' % self.font_fallback
        page = fill(tpl("index.html"), resolution="portrait" if self.H > self.W else "landscape", claim=esc(self.b["claim"]), title=esc(sb.get("title", self.b["name"] + " promo")),
                    width=self.W, height=self.H, duration=v["duration"], font_faces=self.font_faces, css_vars=css_vars,
                    scene_hosts="\n".join(hosts), caption_host=cap_host, audio_clips="\n".join(clips))
        with open(os.path.join(self.out, "index.html"), "w") as f:
            f.write(page)
        # cue sheet
        rows = [(t, "SCENE  " + n) for t, n in self.cues]
        rows += [(vo["start"], "VOICE  " + vo["text"]) for vo in sb.get("voice", [])]
        rows += [(cp["start"], "CAPTION  " + cp["text"]) for cp in caps]
        rows += [(t, "SFX  %s (%s)" % (n, note)) for t, n, _, note in cues]
        rows.sort(key=lambda r: r[0])
        with open(os.path.join(self.out, "cue-sheet.md"), "w") as f:
            f.write("# Cue sheet — %s (%ss)\n\n| t | what |\n|---|---|\n" % (sb.get("title", self.b["name"]), v["duration"]))
            for t, what in rows:
                f.write("| %5.2f | %s |\n" % (t, what.replace("|", "/")))
        print("built %d scenes, %d captions, %d voice lines, %d sfx cues → %s" % (len(sb["scenes"]), len(caps), len(sb.get("voice", [])), len(cues), self.out))


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("storyboard", nargs="?", default=os.path.join(ROOT, "storyboard.json"))
    ap.add_argument("--out", default=ROOT)
    a = ap.parse_args()
    with open(a.storyboard) as f:
        Build(json.load(f), a.out).run()
