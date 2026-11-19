#!/usr/bin/env python3
"""Write storyboard.json for the Wavvy Wallet "What's new" film (vertical, ~55 s).

Punch-ins are given in screenshot pixels (900x2000 captures) and converted to camera x/y here,
so each punch centres the thing the voice is talking about.
Re-run after tts (keeps measured voice durations): python3 tools/make_storyboard.py
"""
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SB = os.path.join(ROOT, "storyboard.json")

PH = dict(left=160, top=330, width=760, height=1528, radius=64, bezel=14, crop_top=66)
IMG_W = PH["width"] - 2 * PH["bezel"]          # 732
K = IMG_W / 900.0                               # screenshot px -> frame px
W, H = 1080, 1920


def punch(t, ix, iy, scale, dur=0.6):
    fx = PH["left"] + PH["bezel"] + ix * K
    fy = PH["top"] + PH["bezel"] - PH["crop_top"] + iy * K
    x = round(-(fx - W / 2) * scale)
    y = round(-(fy - H / 2) * scale)
    return {"t": t, "kind": "punch", "scale": scale, "x": x, "y": y, "duration": dur}


C = {
    "ground": "#F4F7F6",      # site light section
    "surface": "#FFFFFF",
    "ink": "#111111",
    "accent": "#376C50",      # site --bs-primary
    "highlight": "#376C50",
    "flood": "#376C50",
    "ink_on_flood": "#FFFFFF",
    "bezel": "#111111",
    "bezel_edge": "#2A2F2C",
}

old_voice = {}
if os.path.exists(SB):
    try:
        for v in json.load(open(SB)).get("voice", []):
            old_voice[v["id"]] = v
    except Exception:
        pass

voice = [
    ("vo1", "Here's what's new in Wavvy Wallet.", 4.6),
    ("vo2", "Got a KCB M-Pesa message? Paste it in, and it becomes a transaction.", 8.6),
    ("vo3", "On iPhone, import MTN MoMo texts and PDF statements, with smarter auto-tagging.", 16.2),
    ("vo4", "On Android, the tag screen reacts instantly when the internet drops, and comes right back when it returns.", 23.3),
    ("vo5", "Transaction charges now sit one swipe from your total expenses.", 32.1),
    ("vo6", "Set reminders for bills and subscriptions, and pick your alerts on the new notifications page.", 38.0),
    ("vo7", "Money in and money out are clearer, with Rwandan francs fully supported.", 45.9),
    ("vo8", "Update Wavvy Wallet today.", 53.0),
]
voice_list = []
for vid, text, start in voice:
    v = {"id": vid, "text": text, "start": start, "src": "assets/audio/%s.wav" % vid, "volume": 1.4}
    ov = old_voice.get(vid)
    if ov and ov.get("text") == text and ov.get("duration"):
        v["duration"] = ov["duration"]
        v["src"] = ov.get("src", v["src"])
    voice_list.append(v)

scenes = [
    {"id": "hook", "type": "hook-cards", "start": 0, "duration": 4.4, "preloaded": 2,
     "cards": [
         {"title": "KCB M-Pesa: paste a message", "meta": "NEW · IMPORT"},
         {"title": "iPhone: MTN MoMo SMS + PDF statements", "meta": "NEW · IPHONE"},
         {"title": "Tag screen reacts instantly", "meta": "NEW · ANDROID"},
         {"title": "Charges, easier to see", "meta": "NEW · INSIGHTS"},
         {"title": "Bill + subscription reminders", "meta": "NEW · REMINDERS"},
         {"title": "In vs out, plus RWF", "meta": "NEW · RWF"},
     ],
     "pops": [0.25, 0.5, 0.75, 1.0], "hero": {"text": "What's / *new?*", "at": 2.6}, "flood_at": 3.95},
    {"id": "reveal", "type": "reveal", "start": 4.4, "duration": 4.0, "screens": ["whatsnew_dialog.png"],
     "brand_at": 0.15, "drain": True, "push": 1.12},
    {"id": "kcb", "type": "feature", "start": 8.4, "duration": 7.6, "transition": "cut",
     "label": {"n": "1", "text": "KCB M-Pesa import", "at": 2.6},
     "screens": ["kcb_0_empty.png", "kcb_1_pasted.png", "kcb_2_parsed.png", "home_list.png"],
     "moves": [
         {"t": 0.2, "kind": "card-drop", "title": "Ksh5,000 from your KCB M-PESA account",
          "meta": "SMS · KCB M-PESA", "icon": "assets/brand/mpesa.png", "drop_at": 2.2},
         {"t": 2.45, "kind": "show", "screen": 1, "rise": True},
         punch(2.8, 450, 860, 1.45),
         {"t": 4.1, "kind": "reset", "duration": 0.4},
         {"t": 4.3, "kind": "show", "screen": 2, "settle": True},
         punch(4.6, 450, 570, 1.6),
         {"t": 6.0, "kind": "reset", "duration": 0.4},
         {"t": 6.2, "kind": "show", "screen": 3, "rise": True},
         punch(6.45, 450, 820, 1.4, 0.5),
     ]},
    {"id": "momo", "type": "hook-cards", "start": 16.0, "duration": 7.2, "preloaded": 0,
     "label": {"n": "2", "text": "iPhone · MTN MoMo", "top": 110, "at": 0.1},
     "cards": [
         {"title": "15,000 RWF transferred to Aline Uwase", "meta": "M-MONEY · SMS", "icon": "assets/brand/momo.jpg"},
         {"title": "Your payment of 6,500 RWF to SIMBA SUPERMARKET", "meta": "M-MONEY · SMS", "icon": "assets/brand/momo.jpg"},
         {"title": "You have received 50,000 RWF from Eric Habimana", "meta": "M-MONEY · SMS", "icon": "assets/brand/momo.jpg"},
         {"title": "MoMo statement · November 2026.pdf", "meta": "PDF STATEMENT", "icon": "assets/brand/momo.jpg"},
     ],
     "pops": [0.3, 0.7, 1.1, 1.5], "hero": {"text": "Now on / *iPhone*", "at": 3.6}},
    {"id": "offline", "type": "feature", "start": 23.0, "duration": 9.0, "transition": "whip-over", "from": "bottom",
     "label": {"n": "3", "text": "Instant tag screen", "at": 0.3},
     "screens": ["tag_offline.png", "tag_online.png", "tag_search.png", "tag_done.png"],
     "moves": [
         punch(0.9, 450, 700, 1.45),
         {"t": 3.3, "kind": "reset", "duration": 0.4},
         {"t": 3.6, "kind": "show", "screen": 1, "settle": True},
         {"t": 5.4, "kind": "show", "screen": 2},
         {"t": 6.6, "kind": "show", "screen": 3, "settle": True},
         punch(6.9, 450, 700, 1.2, 0.5),
     ]},
    {"id": "charges", "type": "feature", "start": 31.8, "duration": 6.0, "transition": "whip-over", "from": "right",
     "label": {"n": "4", "text": "Transaction charges", "at": 0.3},
     "screens": ["ins_total.png", "ins_charges.png"],
     "moves": [
         punch(0.6, 450, 1250, 1.45),
         {"t": 2.0, "kind": "scroll", "screen": 1},
         punch(2.6, 400, 1290, 1.75),
     ]},
    {"id": "reminders", "type": "feature", "start": 37.6, "duration": 8.2, "transition": "whip-over", "from": "bottom",
     "label": {"n": "5", "text": "Bill reminders", "at": 0.3},
     "screens": ["rem_form.png", "rem_list.png", "notif_1.png"],
     "moves": [
         {"t": 1.3, "kind": "show", "screen": 1, "rise": True},
         punch(1.7, 450, 1260, 1.4),
         {"t": 4.3, "kind": "reset", "duration": 0.4},
         {"t": 4.6, "kind": "show", "screen": 2, "settle": True},
         punch(5.0, 450, 1050, 1.3),
     ]},
    {"id": "inout", "type": "feature", "start": 45.6, "duration": 7.2, "transition": "whip-over", "from": "right",
     "label": {"n": "6", "text": "In vs out · RWF", "at": 0.3},
     "screens": ["inout_list.png", "inout_rwf.png", "ins_top.png"],
     "moves": [
         punch(0.7, 600, 1110, 1.5),
         {"t": 2.6, "kind": "scroll", "screen": 1},
         punch(3.0, 600, 1300, 1.5),
         {"t": 4.6, "kind": "reset", "duration": 0.4},
         {"t": 4.9, "kind": "show", "screen": 2, "settle": True},
         punch(5.2, 450, 900, 1.3),
     ]},
    {"id": "endcard", "type": "endcard", "start": 52.6, "duration": 4.4, "transition": "flood",
     "tile_at": 0.35, "name_at": 0.7, "claim_at": 1.3,
     "badges": [{"src": "assets/brand/app-store.png", "at": 1.9}, {"src": "assets/brand/google-play.png", "at": 2.3}]},
]

captions = [
    {"text": "Paste a *KCB* M-Pesa SMS", "start": 8.7, "end": 12.3},
    {"text": "It becomes a *transaction*", "start": 12.4, "end": 15.6},
    {"text": "MTN MoMo SMS + *PDF* statements", "start": 16.3, "end": 20.0},
    {"text": "Smarter *auto-tagging*", "start": 20.2, "end": 22.8},
    {"text": "Internet *drops?* It tells you", "start": 23.4, "end": 26.8},
    {"text": "Back online, *instantly*", "start": 26.9, "end": 31.4},
    {"text": "Charges, *one swipe* away", "start": 32.2, "end": 37.3},
    {"text": "Bills and *subscriptions*", "start": 38.0, "end": 41.9},
    {"text": "Pick your *alerts*", "start": 42.2, "end": 45.3},
    {"text": "Money in *+* money out *−*", "start": 46.0, "end": 49.3},
    {"text": "Rwandan franc *(RWF)* support", "start": 49.4, "end": 52.4},
]

sb = {
    "title": "Wavvy Wallet — What's new",
    "brand": {
        "name": "Wavvy Wallet",
        "claim": "Know where your money is going.",
        "font": "Nunito",
        "font_files": {"200 1000": "assets/fonts/Nunito.ttf"},
        "colors": C,
        "logo": "assets/brand/logo.png",
        "badges": [],
        "phone": PH,
    },
    "video": {
        "width": W, "height": H, "fps": 30, "duration": 57,
        "music": {"src": "assets/audio/music.wav", "volume": 0.33, "fade_in": 0.5, "fade_out": 2.5},
        "captions": {"top": 1700, "size": 52, "pill": "rgba(255,255,255,.96)"},
    },
    "voice": voice_list,
    "captions": captions,
    "scenes": scenes,
    "sfx": {"auto": True, "scale": 0.6},
}
json.dump(sb, open(SB, "w"), indent=2, ensure_ascii=False)
print("wrote", SB)
