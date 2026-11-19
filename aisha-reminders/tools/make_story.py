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
    {"name": "Tagging reminder", "sub": "A weekly nudge to tag", "icon": "tag"},
    {"name": "Bill reminders", "sub": "Rent, Wi-Fi, subscriptions", "icon": "bell"},
    {"name": "Your alerts", "sub": "Days or hours before", "icon": "receipt"},
    {"name": "Check and tidy", "sub": "List, change, delete", "icon": "search"},
]
A = "assets/screens/rem/"
INPUT = [70, 1806, 792, 1930]     # chat input box
SEND = (850, 1868)                 # send / mic button
ALLOW = (448, 1684)                # permission sheet: Allow Once
PERM = [44, 1410, 856, 1576]       # permission sheet: what Aisha wants to do


def ask(q_line, q_off, send_off, screen_after, top=1806, bottom=1930):
    """input punch + mark, then tap send and show the reply screen. top/bottom: input box rows
    (the typed-question screens have the keyboard up, so the input sits higher)."""
    box = [70, top, 792, bottom]
    cy = (top + bottom) / 2
    return [
        (q_line, q_off, punch(430, cy, 1.35, 0.5)),
        (q_line, q_off + 0.4, {"kind": "mark", "box": box, "hold": max(0.8, send_off - q_off - 1.2)}),
        (q_line, send_off, {"kind": "tap", "x": SEND[0], "y": cy, "lead": 0.6}),
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
     "kicker": "Aisha can now set", "headline": "Reminders", "tile": "assets/brand/aisha.png", "tile_round": True},
    {"id": "pick", "type": "menu", "mode": "pick", "pick": 1, "lines": ["i4"], "rows": ROWS,
     "kicker": "Aisha can now set", "headline": "Reminders", "tile": "assets/brand/aisha.png", "tile_round": True},

    {"id": "ch1", "type": "chapter", "n": 1, "of": 4, "kicker": "REMINDERS", "steady": True, "title": "Tagging reminder", "question": "Payments piling up untagged?", "lines": ["c1q"]},
    {"id": "tagrem", "type": "feature", "lines": ["c1a", "c1b", "c1c"], "label": {"n": "1", "text": "Tagging reminder"},
     "screens": [A + "r_home.png", A + "r01_q.png", A + "r01_a.png"],
     "moves": [
         ("c1a", 1.6, punch(450, 470, 1.55, 0.6)),
         ("c1a", 2.3, {"kind": "mark", "box": [34, 300, 866, 562], "hold": 2.6}),
         ("c1b", -0.3, {"kind": "reset", "duration": 0.3}),
         ("c1b", 0.0, {"kind": "show", "screen": A + "r01_q.png", "rise": True}),
     ] + ask("c1b", 1.2, 5.2, A + "r01_a.png", 1028, 1236) + reply("c1c", 0.1, [79, 1607, 709, 1788], 2.8)},

    {"id": "ch2", "type": "chapter", "n": 2, "of": 4, "kicker": "REMINDERS", "title": "Bill reminders", "question": "Ever paid rent late?", "lines": ["c2q"]},
    {"id": "bill", "type": "feature", "lines": ["c2a", "c2b"], "label": {"n": "2", "text": "Bill reminders"},
     "screens": [A + "r02_q.png", A + "r02_a.png"],
     "moves": ask("c2a", 1.6, 6.4, A + "r02_a.png", 1028, 1236) + reply("c2b", 0.0, [79, 1563, 709, 1788], 3.2)},

    {"id": "ch3", "type": "chapter", "n": 3, "of": 4, "kicker": "REMINDERS", "title": "You choose the alerts", "question": "A day before? Two?", "lines": ["c3q"]},
    {"id": "alerts", "type": "feature", "lines": ["c3a", "c3b"], "label": {"n": "3", "text": "Your alerts"},
     "screens": [A + "r03_q.png", A + "r03_a.png"],
     "moves": ask("c3a", 0.3, 2.6, A + "r03_a.png", 1133, 1236) + reply("c3b", 0.0, [79, 1563, 709, 1788], 3.4)},

    {"id": "ch4", "type": "chapter", "n": 4, "of": 4, "kicker": "REMINDERS", "title": "Check and tidy", "question": "What's coming up?", "lines": ["c4q"]},
    {"id": "tidy", "type": "feature", "lines": ["c4a", "c4b", "c4c", "c4d"], "label": {"n": "4", "text": "Check and tidy"},
     "screens": [A + "r04_q.png", A + "r04_a.png", A + "r05_a.png", A + "r06_q.png", A + "r06_a.png", A + "r_bills.png", A + "r_notif.png"],
     "moves": ask("c4a", 0.3, 2.4, A + "r04_a.png", 1133, 1236) + [
         ("c4a", 2.9, punch(410, 1440, 1.2, 0.5)),
         ("c4a", 3.2, {"kind": "mark", "box": [79, 1099, 709, 1788], "hold": 1.4}),
         ("c4b", -0.3, {"kind": "reset", "duration": 0.3}),
         ("c4b", 0.1, {"kind": "show", "screen": A + "r05_a.png", "rise": True}),
     ] + reply("c4b", 1.6, [79, 1607, 709, 1788], 2.6) + [
         ("c4c", -0.3, {"kind": "reset", "duration": 0.3}),
         ("c4c", 0.0, {"kind": "show", "screen": A + "r06_q.png"}),
     ] + ask("c4c", 1.4, 4.4, A + "r06_a.png", 1081, 1236) + [
         ("c4c", 4.9, {"kind": "mark", "box": [79, 1607, 709, 1788], "hold": 1.2}),
         ("c4d", -0.2, {"kind": "reset", "duration": 0.3}),
         ("c4d", 0.1, {"kind": "show", "screen": A + "r_bills.png", "rise": True}),
         ("c4d", 0.6, punch(450, 760, 1.3, 0.5)),
         ("c4d", 0.9, {"kind": "mark", "box": [40, 380, 860, 1110], "hold": 2.2}),
         ("c4d", 3.3, {"kind": "reset", "duration": 0.3}),
         ("c4d", 3.6, {"kind": "show", "screen": A + "r_notif.png", "settle": True}),
         ("c4d", 4.0, punch(450, 1660, 1.35, 0.5)),
         ("c4d", 4.3, {"kind": "mark", "box": [40, 1610, 860, 1720], "hold": 2.2}),
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
        s["row_times"] = [round(a + 0.25 + k * min(0.5, (d2 - 0.4) / len(sc["rows"])), 2) for k in range(len(sc["rows"]))]
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
    "title": "Wavvy Wallet — Aisha sets your reminders",
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
