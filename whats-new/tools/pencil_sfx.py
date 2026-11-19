#!/usr/bin/env python3
"""Synthesise a pencil-on-paper scribble (graphite grain = band-passed noise + grit impulses,
loudness following the stroke speed). Deterministic (fixed seed). Writes assets/sfx/pencil.wav.
    /root/.venvs/audio/bin/python tools/pencil_sfx.py [seconds]
"""
import os, sys
import numpy as np, soundfile as sf
from scipy.signal import butter, sosfilt

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
dur = float(sys.argv[1]) if len(sys.argv) > 1 else 0.75
sr = 44100
n = int(dur * sr)
rng = np.random.default_rng(11)
t = np.arange(n) / sr

noise = rng.standard_normal(n)
grain = sosfilt(butter(4, [1800, 7500], btype="band", fs=sr, output="sos"), noise)
grit = np.zeros(n)
idx = rng.integers(0, n, int(dur * 900))
grit[idx] = rng.standard_normal(len(idx)) * 3.0
grit = sosfilt(butter(2, [2500, 9000], btype="band", fs=sr, output="sos"), grit)
body = sosfilt(butter(2, [300, 1200], btype="band", fs=sr, output="sos"), noise) * 0.35

# stroke speed: a loop drawn in ~2.3 strokes (speeds up mid-stroke, eases at the turns)
speed = 0.55 + 0.45 * np.abs(np.sin(np.pi * 2.3 * t / dur))
speed *= 1 + 0.25 * np.sin(2 * np.pi * 23 * t + rng.uniform(0, 6))   # hand tremor
env = np.minimum(1, t / 0.03) * np.minimum(1, (dur - t) / 0.12)
y = (grain + grit * 0.6 + body) * speed * env
y = y / np.max(np.abs(y)) * 0.7
os.makedirs(os.path.join(ROOT, "assets/sfx"), exist_ok=True)
out = os.path.join(ROOT, "assets/sfx/pencil.wav")
sf.write(out, y.astype(np.float32), sr)
print("wrote", out, dur, "s")
