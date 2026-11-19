#!/usr/bin/env python3
"""Transcribe each story line with local faster-whisper and flag word mismatches."""
import json, os, re, sys, difflib
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
from story_lines import LINES
from faster_whisper import WhisperModel
os.chdir(ROOT)
m = WhisperModel("small.en", device="cpu", compute_type="int8")
only = set(sys.argv[1:])
norm = lambda s: re.sub(r"[^a-z0-9 ]", " ", s.lower().replace("-", " ").replace("wavy", "wavvy")).split()
for lid, text, _ in LINES:
    if only and lid not in only:
        continue
    t = " ".join(s.text for s in m.transcribe("assets/audio/story/%s.wav" % lid, language="en",
                 initial_prompt="Wavvy Wallet, Aisha, Mary Wanjiku, Kings Court, Naivasha, Allow Once")[0]).strip()
    r = difflib.SequenceMatcher(None, norm(text), norm(t)).ratio()
    print(f"{'OK ' if r > 0.85 else 'BAD'} {r:.2f} {lid}: {t}")
