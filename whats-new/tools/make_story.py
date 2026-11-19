#!/usr/bin/env python3
"""Chaptered, beginner-friendly "What's new" film -> storyboard.json.

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
    {"name": "Bank SMS import", "sub": "Bank wallet messages, read for you", "icon": "bank"},
    {"name": "More ways to import", "sub": "Mobile money SMS and PDF statements", "icon": "phone"},
    {"name": "Faster tagging", "sub": "Know right away if you're offline", "icon": "tag"},
    {"name": "Fee tracking", "sub": "See what your transfers cost", "icon": "receipt"},
    {"name": "Bill reminders", "sub": "Rent, internet, subscriptions", "icon": "bell"},
    {"name": "Clearer money flow", "sub": "Money in, money out, more currencies", "icon": "swap"},
]

# ---- the film: list of scenes; feature moves anchored to ("line", offset) ----
FILM = [
    {"id": "intro", "type": "menu", "mode": "build", "lines": ["i1", "i2"], "rows": ROWS},
    {"id": "popup", "type": "feature", "lines": ["i3"], "screens": ["whatsnew_dialog.png"], "transition": "whip-over", "from": "bottom",
     "moves": [
         ("i3", 0.5, punch(440, 1000, 1.5, 0.7)),
         ("i3", 1.3, {"kind": "mark", "box": [110, 610, 800, 1400], "hold": 2.6, "duration": 0.9}),
     ]},
    {"id": "pick", "type": "menu", "mode": "pick", "pick": 1, "lines": ["i4"], "rows": ROWS},
    {"id": "ch1", "type": "chapter", "n": 1, "steady": True, "title": "KCB M-Pesa messages", "question": "Do you use KCB M-Pesa?", "lines": ["c1q"]},
    {"id": "kcb", "type": "feature", "lines": ["c1a", "c1n", "c1b", "c1c"], "label": {"n": "1", "text": "KCB M-Pesa"},
     "screens": ["n_kcb.png", "k_auto_list.png", "g_home.png", "kcb_0_empty.png", "kcb_1_pasted.png", "kcb_2_parsed.png", "g_list2.png"],
     "moves": [
         ("c1a", 2.6, punch(450, 1130, 1.45, 0.7)),
         ("c1a", 3.4, punch(450, 1130, 1.62, 3.4)),
         ("c1a", 3.0, {"kind": "mark", "box": [40, 1000, 860, 1260], "hold": 3.8}),
         ("c1n", -0.3, {"kind": "reset", "duration": 0.3}),
         ("c1n", 0.1, {"kind": "show", "screen": "k_auto_list.png", "rise": True}),
         ("c1n", 0.6, punch(450, 1365, 1.45)),
         ("c1n", 1.0, {"kind": "mark", "box": [40, 1270, 870, 1450], "hold": 2.3}),
         ("c1b", -0.3, {"kind": "reset", "duration": 0.3}),
         ("c1b", 0.0, {"kind": "show", "screen": "g_home.png"}),
         ("c1b", 2.3, {"kind": "tap", "x": 670, "y": 1690, "lead": 0.9}),
         ("c1b", 2.6, {"kind": "show", "screen": "kcb_0_empty.png", "rise": True}),
         ("c1b", 3.7, {"kind": "tap", "x": 100, "y": 320, "lead": 0.6}),
         ("c1b", 4.2, {"kind": "show", "screen": "kcb_1_pasted.png"}),
         ("c1b", 4.4, punch(450, 860, 1.3, 0.5)),
         ("c1b", 5.9, {"kind": "reset", "duration": 0.3}),
         ("c1b", 6.6, {"kind": "tap", "x": 240, "y": 1176, "lead": 0.5}),
         ("c1c", -0.1, {"kind": "show", "screen": "kcb_2_parsed.png", "settle": True}),
         ("c1c", 0.2, punch(450, 560, 1.5, 0.4)),
         ("c1c", 0.3, {"kind": "mark", "box": [30, 455, 880, 640], "hold": 0.9}),
         ("c1c", 1.1, {"kind": "reset", "duration": 0.3}),
         ("c1c", 1.7, {"kind": "tap", "x": 480, "y": 304, "lead": 0.5}),
         ("c1c", 2.1, {"kind": "show", "screen": "g_list2.png", "rise": True}),
         ("c1c", 2.4, punch(450, 764, 1.4, 0.5)),
     ]},

    {"id": "ch2", "type": "chapter", "n": 2, "title": "MTN MoMo on iPhone", "question": "On iPhone in Rwanda?", "lines": ["c2q"]},
    {"id": "momo", "type": "hook-cards", "lines": ["c2a", "c2b"], "preloaded": 0, "label": {"n": "2", "text": "iPhone · MTN MoMo", "top": 110},
     "cards": [
         {"title": "15,000 RWF transferred to Aline Uwase", "meta": "MTN MOMO · SMS", "icon": "assets/brand/momo.jpg"},
         {"title": "Payment of 6,500 RWF to SIMBA SUPERMARKET", "meta": "MTN MOMO · SMS", "icon": "assets/brand/momo.jpg"},
         {"title": "Received 50,000 RWF from Eric Habimana", "meta": "MTN MOMO · SMS", "icon": "assets/brand/momo.jpg"},
         {"title": "MoMo statement, November 2026", "meta": "PDF STATEMENT", "icon": "assets/brand/momo.jpg"},
     ],
     "pops_at": [("c2a", 0.6), ("c2a", 1.6), ("c2a", 2.6), ("c2a", 3.8)],
     "hero_at": ("c2b", 0.2), "hero_text": "Sorted / *for* *you*"},

    {"id": "ch3", "type": "chapter", "n": 3, "title": "A faster tag screen", "question": "What was that payment for?", "lines": ["c3q"]},
    {"id": "tag", "type": "feature", "lines": ["c3a", "c3b", "c3c", "c3d"], "label": {"n": "3", "text": "Tagging"},
     "screens": ["inout_list.png", "tag_offline.png", "tag_online.png", "tag_search.png", "tag_done.png"],
     "moves": [
         ("c3a", 0.1, punch(450, 1230, 1.3, 0.5)),
         ("c3a", 2.0, {"kind": "tap", "x": 748, "y": 1208, "lead": 0.9}),
         ("c3a", 2.4, {"kind": "reset", "duration": 0.3}),
         ("c3b", -0.2, {"kind": "show", "screen": "tag_offline.png", "settle": True}),
         ("c3b", 0.6, punch(450, 820, 1.5)),
         ("c3b", 0.9, {"kind": "mark", "box": [50, 850, 860, 960], "hold": 5.0}),
         ("c3b", 4.3, {"kind": "reset", "duration": 0.4}),
         ("c3c", -0.1, {"kind": "show", "screen": "tag_online.png", "settle": True}),
         ("c3c", 1.4, {"kind": "tap", "x": 448, "y": 988, "lead": 0.8}),
         ("c3c", 1.9, {"kind": "show", "screen": "tag_search.png"}),
         ("c3c", 3.4, {"kind": "tap", "x": 300, "y": 1040, "lead": 0.8}),
         ("c3d", -0.1, {"kind": "show", "screen": "tag_done.png", "settle": True}),
         ("c3d", 0.2, punch(450, 1180, 1.3, 0.5)),
         ("c3d", 0.4, {"kind": "mark", "box": [40, 1150, 870, 1310], "hold": 2.0}),
     ]},

    {"id": "ch4", "type": "chapter", "n": 4, "title": "Transaction charges", "question": "How much do fees cost you?", "lines": ["c4q"]},
    {"id": "charges", "type": "feature", "lines": ["c4a", "c4b"], "label": {"n": "4", "text": "Transaction charges"},
     "screens": ["g_home.png", "ins_total.png"],
     "moves": [
         ("c4a", 0.9, {"kind": "tap", "x": 340, "y": 1890, "lead": 0.8}),
         ("c4a", 1.3, {"kind": "show", "screen": "ins_total.png", "rise": True}),
         ("c4a", 1.6, punch(450, 1310, 1.4, 0.5)),
         ("c4a", 2.0, {"kind": "mark", "box": [90, 1230, 800, 1400], "hold": 0.8}),
         ("c4b", 0.7, {"kind": "swipe-h", "from": "ins_total.png", "to": "ins_charges.png", "box": [0, 1090, 900, 1530], "duration": 0.6, "lead": 0.7}),
         ("c4b", 1.7, punch(420, 1290, 1.7, 0.6)),
         ("c4b", 2.2, {"kind": "mark", "box": [90, 1220, 820, 1400], "hold": 2.0}),
     ]},

    {"id": "ch5", "type": "chapter", "n": 5, "title": "Bill reminders", "question": "Ever forgotten a bill?", "lines": ["c5q"]},
    {"id": "bills", "type": "feature", "lines": ["c5a", "c5b", "c5c", "c5d"], "label": {"n": "5", "text": "Bill reminders"},
     "screens": ["g_home.png", "g_drawer.png", "rem_form.png", "rem_list.png", "notif_1.png"],
     "moves": [
         ("c5a", 0.9, {"kind": "tap", "x": 60, "y": 190, "lead": 0.8}),
         ("c5a", 1.2, {"kind": "show", "screen": "g_drawer.png"}),
         ("c5a", 2.5, {"kind": "tap", "x": 260, "y": 532, "lead": 0.8}),
         ("c5b", -0.1, {"kind": "show", "screen": "rem_form.png", "rise": True}),
         ("c5b", 0.4, punch(450, 1150, 1.3)),
         ("c5b", 3.0, {"kind": "reset", "duration": 0.35}),
         ("c5b", 3.6, {"kind": "tap", "x": 448, "y": 1820, "lead": 0.6}),
         ("c5c", -0.1, {"kind": "show", "screen": "rem_list.png", "settle": True}),
         ("c5c", 0.3, punch(450, 1230, 1.35)),
         ("c5c", 0.6, {"kind": "mark", "box": [30, 800, 870, 1200], "hold": 2.0}),
         ("c5d", -0.3, {"kind": "reset", "duration": 0.3}),
         ("c5d", 0.0, {"kind": "show", "screen": "notif_1.png", "rise": True}),
         ("c5d", 0.5, punch(450, 1200, 1.45)),
         ("c5d", 1.2, {"kind": "mark", "box": [50, 1120, 860, 1240], "hold": 2.5}),
         ("c5d", 2.4, punch(450, 1250, 1.55, 1.6)),
     ]},

    {"id": "ch6", "type": "chapter", "n": 6, "title": "Money in, money out, and RWF", "question": "Money in, or money out?", "lines": ["c6q"]},
    {"id": "inout", "type": "feature", "lines": ["c6a", "c6b", "c6c"], "label": {"n": "6", "text": "In, out, and RWF"},
     "screens": ["g_list2.png", "g_tag_out.png", "g_tag_in.png", "n_rwf.png"],
     "moves": [
         ("c6a", 1.1, {"kind": "tap", "x": 750, "y": 1484, "lead": 0.9}),
         ("c6a", 1.4, {"kind": "show", "screen": "g_tag_out.png", "rise": True}),
         ("c6a", 1.9, punch(450, 484, 1.6)),
         ("c6a", 2.4, {"kind": "mark", "box": [60, 410, 880, 510], "hold": 1.3}),
         ("c6b", -0.4, {"kind": "reset", "duration": 0.3}),
         ("c6b", -0.1, {"kind": "show", "screen": "g_list2.png"}),
         ("c6b", 0.6, {"kind": "tap", "x": 750, "y": 962, "lead": 0.6}),
         ("c6b", 0.9, {"kind": "show", "screen": "g_tag_in.png", "settle": True}),
         ("c6b", 1.2, punch(450, 484, 1.6)),
         ("c6b", 1.6, {"kind": "mark", "box": [60, 410, 880, 510], "hold": 1.8}),
         ("c6c", -0.3, {"kind": "reset", "duration": 0.3}),
         ("c6c", 0.0, {"kind": "show", "screen": "n_rwf.png", "rise": True}),
         ("c6c", 1.0, punch(450, 1065, 1.45)),
         ("c6c", 1.4, {"kind": "mark", "box": [40, 935, 860, 1150], "hold": 3.0}),
         ("c6c", 3.6, punch(450, 1065, 1.65, 1.5)),
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
    "title": "Wavvy Wallet — What's new (step by step)",
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
