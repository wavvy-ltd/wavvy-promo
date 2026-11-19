#!/usr/bin/env python3
"""Chaptered, beginner-friendly "Meet Aisha" chat capabilities film -> storyboard.json.

Each update is a section: chapter card (number, title, the everyday question) then the app
walkthrough with tap rings on the exact control, punch-ins on the result, one caption per step.
Times come from the measured voice lines (assets/audio/story/meta.json), so re-recording a line
re-flows the whole film. Coordinates are in 900x2000 screenshot pixels.
    python3 tools/make_story.py
"""
import json, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from story_lines import LINES
os.chdir(ROOT)
META = json.load(open("assets/audio/story/meta.json"))
TEXT = {l: t for l, t, _ in LINES}
CAP = {l: c for l, _, c in LINES}
DUR = {l: META[l]["duration"] for l in TEXT}

PH = dict(left=160, top=330, width=760, height=1528, radius=64, bezel=14, crop_top=66)
K = (PH["width"] - 2 * PH["bezel"]) / 900.0
W, H = 1080, 1920
GAP, LEAD, TAIL = 0.45, 0.45, 0.7

C = {"ground": "#F4F7F6", "surface": "#FFFFFF", "ink": "#111111", "accent": "#376C50", "highlight": "#376C50",
     "flood": "#376C50", "ink_on_flood": "#FFFFFF", "bezel": "#111111", "bezel_edge": "#2A2F2C", "tap_glow": "#4fc385", "pencil": "#E4572E"}


def punch(ix, iy, scale, dur=0.6):
    fx = PH["left"] + PH["bezel"] + ix * K
    fy = PH["top"] + PH["bezel"] - PH["crop_top"] + iy * K
    return {"kind": "punch", "scale": scale, "x": round(-(fx - W / 2) * scale), "y": round(-(fy - H / 2) * scale), "duration": dur}


ROWS = [
    {"name": "Ask about spending", "sub": "Totals and top costs in seconds", "icon": "chart"},
    {"name": "Find any payment", "sub": "By name, with dates and fees", "icon": "search"},
    {"name": "Tag by chatting", "sub": "Say what a payment was for", "icon": "tag"},
    {"name": "Add cash spending", "sub": "Cash counts too", "icon": "add"},
    {"name": "Plan a trip", "sub": "Split it, track every shilling", "icon": "flight"},
    {"name": "Themes and voice", "sub": "Change colours, or just speak", "icon": "mic"},
]
A = "assets/screens/aisha/"
INPUT = [70, 1806, 792, 1930]     # chat input box
SEND = (850, 1868)                 # send / mic button
ALLOW = (448, 1684)                # permission sheet: Allow Once
PERM = [44, 1410, 856, 1576]       # permission sheet: what Aisha wants to do


def ask(q_line, q_off, send_off, screen_after):
    """input punch + mark, then tap send and show the reply screen"""
    return [
        (q_line, q_off, punch(430, 1760, 1.35, 0.5)),
        (q_line, q_off + 0.4, {"kind": "mark", "box": INPUT, "hold": max(0.8, send_off - q_off - 1.2)}),
        (q_line, send_off, {"kind": "tap", "x": SEND[0], "y": SEND[1], "lead": 0.6}),
        (q_line, send_off + 0.35, {"kind": "show", "screen": screen_after, "settle": True}),
        (q_line, send_off + 0.45, {"kind": "reset", "duration": 0.35}),
    ]


def reply(line, off, box, hold=2.4, scale=1.3):
    cy = (box[1] + box[3]) / 2
    return [
        (line, off, punch(410, min(cy, 1560), scale, 0.55)),
        (line, off + 0.5, {"kind": "mark", "box": box, "hold": hold}),
    ]


FILM = [
    {"id": "intro", "type": "menu", "mode": "build", "lines": ["i1", "i2"], "rows": ROWS,
     "kicker": "Meet", "headline": "Aisha", "tile": "assets/brand/aisha.png", "tile_round": True},
    {"id": "open", "type": "feature", "lines": ["h1", "h2"], "transition": "whip-over", "from": "bottom",
     "screens": [A + "home0.png", A + "chat0.png", A + "chat1.png"],
     "moves": [
         ("h1", 1.6, punch(700, 1800, 1.5, 0.6)),
         ("h1", 2.5, {"kind": "tap", "x": 788, "y": 1860, "lead": 0.8}),
         ("h1", 2.9, {"kind": "reset", "duration": 0.3}),
         ("h1", 3.0, {"kind": "show", "screen": A + "chat0.png", "rise": True}),
         ("h2", 0.3, punch(450, 980, 1.3, 0.5)),
         ("h2", 0.6, {"kind": "mark", "box": [80, 780, 860, 1140], "hold": 1.6}),
         ("h2", 2.4, {"kind": "reset", "duration": 0.3}),
         ("h2", 3.0, {"kind": "tap", "x": 448, "y": 1220, "lead": 0.7}),
         ("h2", 3.4, {"kind": "show", "screen": A + "chat1.png", "settle": True}),
         ("h2", 3.8, punch(400, 1400, 1.25, 0.5)),
     ]},
    {"id": "pick", "type": "menu", "mode": "pick", "pick": 1, "lines": ["i4"], "rows": ROWS,
     "kicker": "Meet", "headline": "Aisha", "tile": "assets/brand/aisha.png", "tile_round": True},

    {"id": "ch1", "type": "chapter", "n": 1, "kicker": "AISHA", "steady": True, "title": "Ask about your spending", "question": "Where did my money go?", "lines": ["c1q"]},
    {"id": "spend", "type": "feature", "lines": ["c1a", "c1b", "c1c"], "label": {"n": "1", "text": "Ask about spending"},
     "screens": [A + "c01_q.png", A + "c01_a.png", A + "c02_a.png"],
     "moves": ask("c1a", 0.3, 4.6, A + "c01_a.png") + reply("c1b", 0.0, [79, 1458, 709, 1788], 3.2) + [
         ("c1c", -0.3, {"kind": "reset", "duration": 0.3}),
         ("c1c", 0.1, {"kind": "show", "screen": A + "c02_a.png", "rise": True}),
     ] + reply("c1c", 0.9, [79, 1327, 709, 1788], 2.8)},

    {"id": "ch2", "type": "chapter", "n": 2, "kicker": "AISHA", "title": "Find any payment", "question": "Who did I pay, and when?", "lines": ["c2q"]},
    {"id": "find", "type": "feature", "lines": ["c2a", "c2b"], "label": {"n": "2", "text": "Find any payment"},
     "screens": [A + "c03_q.png", A + "c03_a.png"],
     "moves": ask("c2a", 0.5, 3.9, A + "c03_a.png") + reply("c2b", 0.0, [79, 1327, 709, 1788], 3.6)},

    {"id": "ch3", "type": "chapter", "n": 3, "kicker": "AISHA", "title": "Tag by chatting", "question": "What was that payment for?", "lines": ["c3q"]},
    {"id": "tagc", "type": "feature", "lines": ["c3a", "c3b", "c3c"], "label": {"n": "3", "text": "Tag by chatting"},
     "screens": [A + "c04_q.png", A + "c04_perm.png", A + "c04_done.png"],
     "moves": ask("c3a", 1.8, 4.4, A + "c04_perm.png") + [
         ("c3b", 0.1, punch(450, 1560, 1.3, 0.5)),
         ("c3b", 0.5, {"kind": "mark", "box": PERM, "hold": 1.8}),
         ("c3b", 2.6, {"kind": "tap", "x": ALLOW[0], "y": ALLOW[1], "lead": 0.7}),
         ("c3b", 3.0, {"kind": "reset", "duration": 0.3}),
         ("c3c", -0.2, {"kind": "show", "screen": A + "c04_done.png", "settle": True}),
     ] + reply("c3c", 0.2, [79, 1414, 709, 1788], 2.6)},

    {"id": "ch4", "type": "chapter", "n": 4, "kicker": "AISHA", "title": "Add cash spending", "question": "Paid with cash?", "lines": ["c4q"]},
    {"id": "cash", "type": "feature", "lines": ["c4a", "c4b"], "label": {"n": "4", "text": "Add cash spending"},
     "screens": [A + "m07_q.png", A + "m07_perm.png", A + "m07_done.png"],
     "moves": ask("c4a", 1.4, 5.4, A + "m07_perm.png") + [
         ("c4b", 0.0, {"kind": "tap", "x": ALLOW[0], "y": ALLOW[1], "lead": 0.6}),
         ("c4b", 0.4, {"kind": "show", "screen": A + "m07_done.png", "settle": True}),
     ] + reply("c4b", 0.8, [79, 1502, 709, 1788], 2.0)},

    {"id": "ch5", "type": "chapter", "n": 5, "kicker": "AISHA", "title": "Plan a trip", "question": "Going away for the weekend?", "lines": ["c5q"]},
    {"id": "trip", "type": "feature", "lines": ["c5a", "c5b", "c5c"], "label": {"n": "5", "text": "Plan a trip"},
     "screens": [A + "m09_q.png", A + "m09_a.png", A + "m10_done.png"],
     "moves": ask("c5a", 0.6, 4.4, A + "m09_a.png") + [
         ("c5b", 0.0, punch(410, 1180, 1.25, 0.55)),
         ("c5b", 0.5, {"kind": "mark", "box": [100, 1000, 700, 1400], "hold": 3.0}),
         ("c5b", 4.6, punch(410, 1520, 1.25, 0.6)),
         ("c5b", 5.0, {"kind": "mark", "box": [100, 1380, 700, 1620], "hold": 2.6}),
         ("c5c", -0.3, {"kind": "reset", "duration": 0.3}),
         ("c5c", 0.2, {"kind": "show", "screen": A + "m10_done.png", "rise": True}),
     ] + reply("c5c", 0.9, [79, 1458, 709, 1788], 2.6)},

    {"id": "ch6", "type": "chapter", "n": 6, "kicker": "AISHA", "title": "Themes and voice", "question": "Rather talk than type?", "lines": ["c6q"]},
    {"id": "theme", "type": "feature", "lines": ["c6a", "c6b", "c6c"], "label": {"n": "6", "text": "Themes and voice"},
     "screens": [A + "m11_q.png", A + "m11_perm.png", A + "m11_done.png", A + "m12_done.png", A + "m13_mic.png"],
     "moves": ask("c6a", 0.2, 1.4, A + "m11_perm.png") + [
         ("c6a", 2.0, {"kind": "tap", "x": ALLOW[0], "y": ALLOW[1], "lead": 0.5}),
         ("c6a", 2.4, {"kind": "show", "screen": A + "m11_done.png", "settle": True}),
         ("c6a", 2.7, {"kind": "mark", "box": [79, 1458, 709, 1788], "hold": 1.4}),
         ("c6b", 0.2, {"kind": "show", "screen": A + "m12_done.png", "settle": True}),
         ("c6b", 0.5, {"kind": "mark", "box": [79, 1650, 709, 1788], "hold": 1.4}),
         ("c6c", 1.6, punch(450, 1760, 1.3, 0.5)),
         ("c6c", 2.0, {"kind": "tap", "x": SEND[0], "y": SEND[1], "lead": 0.6}),
         ("c6c", 2.4, {"kind": "show", "screen": A + "m13_mic.png", "settle": True}),
         ("c6c", 2.7, {"kind": "mark", "box": [20, 1688, 860, 1784], "hold": 1.8}),
     ]},

    {"id": "endcard", "type": "endcard", "lines": ["o1"], "tile_at": 0.35, "name_at": 0.7, "claim_at": 1.3,
     "badges": [{"src": "assets/brand/app-store.png", "at": 1.9}, {"src": "assets/brand/google-play.png", "at": 2.3}]},
]

t = 0.0
scenes, voice, captions = [], [], []
for sc in FILM:
    s = {k: v for k, v in sc.items() if k not in ("lines", "fixed", "moves", "pops_at", "hero_at", "hero_text")}
    s["start"] = round(t, 2)
    rel, cur = {}, LEAD
    for l in sc["lines"]:
        rel[l] = cur
        voice.append({"id": l, "text": TEXT[l], "start": round(t + cur, 2), "duration": DUR[l],
                      "src": "assets/audio/story/%s.wav" % l, "volume": 1.4})
        if CAP[l]:
            captions.append({"text": CAP[l], "start": round(t + cur + 0.05, 2), "end": round(t + cur + DUR[l] + 0.15, 2)})
        cur += DUR[l] + GAP
    dur = sc.get("fixed") or round(cur - GAP + TAIL, 2)
    if sc["type"] == "endcard":
        dur = round(cur - GAP + 1.6, 2)
    s["duration"] = round(dur, 2)
    if "moves" in sc:
        mv = []
        for (l, off, m) in sc["moves"]:
            m = dict(m); m["t"] = round(rel[l] + off, 2)
            if "screen" in m and isinstance(m["screen"], str):
                m["screen"] = sc["screens"].index(m["screen"])
            mv.append(m)
        s["moves"] = mv
    if "pops_at" in sc:
        s["pops"] = [round(rel[l] + o, 2) for l, o in sc["pops_at"]]
        s["hero"] = {"text": sc["hero_text"], "at": round(rel[sc["hero_at"][0]] + sc["hero_at"][1], 2)}
    if sc["type"] == "menu" and sc["mode"] == "build":
        a, d2 = rel["i2"], DUR["i2"]
        s["shrink_at"] = round(a - 0.35, 2)
        s["row_times"] = [round(a + 0.25 + k * min(0.5, (d2 - 0.4) / 6), 2) for k in range(6)]
    if sc["type"] == "menu" and sc["mode"] == "pick":
        s["pick_at"] = round(rel["i4"] + 0.9, 2)
        s["fly_at"] = round(rel["i4"] + DUR["i4"] + 0.3, 2)
        s["duration"] = round(s["fly_at"] + 0.62, 2)
        dur = s["duration"]
    if s.get("label"):
        s["label"].setdefault("at", 0.15)
    scenes.append(s)
    t += dur

total = round(t, 2)
sb = {
    "title": "Wavvy Wallet — Meet Aisha, your money assistant",
    "brand": {"name": "Wavvy Wallet", "claim": "Know where your money is going.", "font": "Nunito",
              "font_files": {"200 1000": "assets/fonts/Nunito.ttf"}, "colors": C, "logo": "assets/brand/logo.png",
              "badges": [], "phone": PH},
    "video": {"width": W, "height": H, "fps": 30, "duration": total,
              "music": {"src": "assets/audio/music_story.wav", "volume": 0.3, "fade_in": 0.5, "fade_out": 3},
              "captions": {"top": 1700, "size": 52, "pill": "rgba(255,255,255,.96)"}},
    "voice": voice, "captions": captions, "scenes": scenes, "sfx": {"auto": True, "scale": 0.55},
}
json.dump(sb, open("storyboard.json", "w"), indent=2, ensure_ascii=False)
print("total %.1fs, %d scenes, %d voice, %d captions" % (total, len(scenes), len(voice), len(captions)))
for s in scenes:
    print("  %6.2f  %-8s %5.2fs" % (s["start"], s["id"], s["duration"]))
