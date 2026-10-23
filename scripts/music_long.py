"""Generate a continuous music bed longer than MusicGen's ~30 s window by chaining
audio-prompted continuations: each new segment is conditioned on the last few
seconds of what came before, so there is no loop seam.

Usage: python scripts/music_long.py <out.wav> [seconds]
"""
import sys

import numpy as np
import soundfile as sf
import torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration

out = sys.argv[1]
target = float(sys.argv[2]) if len(sys.argv) > 2 else 62.0

PROMPT = (
    "upbeat modern afrobeat pop, warm bright synth chords, light shaker and percussion, "
    "optimistic, 115 bpm, clean instrumental for a mobile app advert"
)
FIRST_S = 28.0      # first free generation
PROMPT_S = 8.0      # audio context carried into each continuation
STEP_S = 20.0       # new audio per continuation

device = "mps" if torch.backends.mps.is_available() else "cpu"
torch.manual_seed(7)

processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small").to(device)
sr = model.config.audio_encoder.sampling_rate
tps = 50  # tokens per second

inputs = processor(text=[PROMPT], padding=True, return_tensors="pt").to(device)
audio = model.generate(**inputs, do_sample=True, guidance_scale=3.0, max_new_tokens=int(FIRST_S * tps))
wav = audio[0, 0].cpu().numpy().astype(np.float32)
print(f"segment 1: {len(wav)/sr:.1f}s")

seg = 2
while len(wav) / sr < target:
    tail = wav[-int(PROMPT_S * sr):]
    cont_in = processor(audio=tail, sampling_rate=sr, text=[PROMPT], padding=True, return_tensors="pt").to(device)
    cont = model.generate(**cont_in, do_sample=True, guidance_scale=3.0, max_new_tokens=int((PROMPT_S + STEP_S) * tps))
    cont_wav = cont[0, 0].cpu().numpy().astype(np.float32)
    new = cont_wav[len(tail):]  # drop the re-emitted prompt, keep only the continuation
    # tiny equal-power blend over 40 ms at the join
    n = int(0.04 * sr)
    ramp = np.linspace(0, 1, n, dtype=np.float32)
    wav[-n:] = wav[-n:] * (1 - ramp) + new[:n] * ramp
    wav = np.concatenate([wav, new[n:]])
    print(f"segment {seg}: +{len(new)/sr:.1f}s → {len(wav)/sr:.1f}s")
    seg += 1

wav = wav[: int(target * sr)]
wav = wav / max(1e-6, np.abs(wav).max()) * 0.89  # -1 dBTP
sf.write(out, wav, sr)
print(f"wrote {out} {len(wav)/sr:.1f}s @ {sr}Hz on {device}")
