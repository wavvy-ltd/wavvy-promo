#!/usr/bin/env python3
"""MOSS-TTS kenyan_female narration for the chaptered story. Caches per line (re-records only when the
text changed or the id is named on the command line). Trims lead/tail silence and caps any internal
pause at 0.5 s. Writes assets/audio/story/meta.json {id: {text, duration}}.
    python3 tools/story_vo.py [ids...]      SEED=n to re-roll
"""
import json, os, subprocess, sys, urllib.request
import numpy as np, soundfile as sf
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from story_lines import LINES
os.chdir(ROOT)
D = "assets/audio/story"
os.makedirs(D, exist_ok=True)
MF = os.path.join(D, "meta.json")
meta = json.load(open(MF)) if os.path.exists(MF) else {}
force = set(sys.argv[1:])
seed = int(os.environ.get("SEED", 7))


def tidy(path):
    y, sr = sf.read(path)
    if y.ndim > 1:
        y = y.mean(1)
    w = int(0.02 * sr)
    n = len(y) // w
    rms = np.array([np.sqrt(np.mean(y[i * w:(i + 1) * w] ** 2)) for i in range(n)])
    loud = rms > 10 ** (-42 / 20)
    idx = np.where(loud)[0]
    a, b = max(idx[0] - 3, 0), min(idx[-1] + 8, n)
    keep, run = [], 0
    for i in range(a, b):
        run = 0 if loud[i] else run + 1
        if run <= 25:              # cap pauses at 0.5 s
            keep.append(y[i * w:(i + 1) * w])
    out = np.concatenate(keep)
    f = int(0.03 * sr)
    out[:f] *= np.linspace(0, 1, f)
    out[-f:] *= np.linspace(1, 0, f)
    sf.write(path, out, sr)
    return round(len(out) / sr, 2)


for lid, text, _ in LINES:
    out = os.path.join(D, lid + ".wav")
    if lid not in force and meta.get(lid, {}).get("text") == text and os.path.exists(out):
        continue
    body = {"model": "moss-tts", "voice": "kenyan_female", "language": "English", "seed": seed,
            "temperature": 1.0, "response_format": "wav", "emotion": "happy",
            "instructions": "A warm, friendly guide explaining a money app to a first-time user. Clear, "
                            "patient and encouraging, natural Kenyan English, unhurried.",
            "input": text.replace("MTN MoMo", "M T N MoMo")}
    req = urllib.request.Request("http://192.168.100.204:8001/v1/audio/speech",
                                 data=json.dumps(body).encode(), headers={"Content-Type": "application/json"})
    open(out, "wb").write(urllib.request.urlopen(req, timeout=300).read())
    meta[lid] = {"text": text, "duration": tidy(out), "seed": seed}
    print(f"{lid:>4} {meta[lid]['duration']:5.2f}s  {text}", flush=True)
    json.dump(meta, open(MF, "w"), indent=1)
print("total voice %.1fs" % sum(m["duration"] for m in meta.values()))
