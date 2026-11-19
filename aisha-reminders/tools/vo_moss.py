#!/usr/bin/env python3
"""Narration with MOSS-TTS (kenyan_female) on the LAN server, one WAV per storyboard voice line.
Writes src + measured duration back into storyboard.json.
    python3 tools/vo_moss.py [vo2 vo5 ...]      (SEED=n to re-roll)
"""
import json, os, subprocess, sys, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sb = json.load(open("storyboard.json"))
only = set(sys.argv[1:])
seed = int(os.environ.get("SEED", 7))
os.makedirs("assets/audio/moss", exist_ok=True)
for vo in sb["voice"]:
    if only and vo["id"] not in only:
        continue
    text = vo["text"].replace("M-Pesa", "M-Pesa").replace("MTN MoMo", "M T N MoMo")
    body = {"model": "moss-tts", "voice": "kenyan_female", "language": "English", "seed": seed,
            "temperature": 1.0, "response_format": "wav", "emotion": "happy",
            "instructions": "A warm, upbeat product announcer for a mobile money app. Clear, confident, "
                            "natural Kenyan English, lively but unhurried.",
            "input": text}
    req = urllib.request.Request("http://192.168.100.204:8001/v1/audio/speech",
                                 data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    out = "assets/audio/moss/%s.wav" % vo["id"]
    open(out, "wb").write(urllib.request.urlopen(req, timeout=300).read())
    d = float(subprocess.check_output(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", out]).decode())
    vo["src"], vo["duration"] = out, round(d, 2)
    print(f"{vo['id']:>4} {vo['start']:5.1f} +{d:4.2f} -> {vo['start'] + d:5.1f}  {vo['text']}", flush=True)
json.dump(sb, open("storyboard.json", "w"), indent=2, ensure_ascii=False)
