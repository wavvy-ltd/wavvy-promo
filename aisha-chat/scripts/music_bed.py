#!/usr/bin/env python3
"""Turn one clean music take into a bed of any length: loop with equal-power crossfades, hold the
level steady (gain capped ±4 dB), roll off hiss above 7 kHz, land at −1 dBTP.

    python3 scripts/music_bed.py <take.wav> <out.wav> <seconds> [loop_seconds]

Generate the take first:  python3 scripts/music.py assets/audio/take.wav 30 nofade
(MusicGen-small; ~30 s per generation; keep the cleanest take — don't gain-fix a bad one).
"""
import sys
import numpy as np
import soundfile as sf

take, out, target = sys.argv[1], sys.argv[2], float(sys.argv[3])
loop_s = float(sys.argv[4]) if len(sys.argv) > 4 else None

y, sr = sf.read(take, dtype="float32")
if y.ndim > 1:
    y = y.mean(axis=1)
seg = y[: int((loop_s or (len(y) / sr - 2.0)) * sr)]   # drop the take's natural tail
xf = int(3.0 * sr)
r = np.linspace(0, 1, xf, dtype=np.float32)
a, b = np.sqrt(1 - r), np.sqrt(r)
bed = seg.copy()
while len(bed) < int(target * sr) + xf:
    bed = np.concatenate([bed[:-xf], bed[-xf:] * a + seg[:xf] * b, seg[xf:]])
bed = bed[: int(target * sr)]

# steady level: 1 s RMS envelope, gain within ±4 dB, 2.5 s smoothing
win, hop = int(1.0 * sr), int(0.25 * sr)
c = np.arange(0, len(bed), hop)
rms = np.array([np.sqrt(np.mean(bed[max(0, i - win // 2): i + win // 2] ** 2)) + 1e-6 for i in c])
g = np.clip(np.median(rms) / rms, 10 ** (-4 / 20), 10 ** (4 / 20))
k = 11
g = np.convolve(np.pad(g, (k // 2, k // 2), mode="edge"), np.ones(k) / k, mode="valid")
bed *= np.interp(np.arange(len(bed)), c, g).astype(np.float32)

# gentle high shelf (−6 dB above ~7 kHz) via a one-pole split
alpha = np.exp(-2 * np.pi * 7000 / sr)
low = np.zeros_like(bed); acc = 0.0
for i, v in enumerate(bed):
    acc = alpha * acc + (1 - alpha) * v
    low[i] = acc
bed = low + (bed - low) * 0.5

bed = bed / max(1e-6, np.abs(bed).max()) * 0.89
sf.write(out, bed, sr)
print(f"wrote {out}: {len(bed)/sr:.1f}s from a {len(seg)/sr:.1f}s loop, gain {20*np.log10(g.min()):+.1f}..{20*np.log10(g.max()):+.1f} dB")
