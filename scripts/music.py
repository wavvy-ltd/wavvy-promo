"""Generate a ~30s instrumental music bed with MusicGen (facebook/musicgen-small).

Usage: python scripts/music.py <out.wav> [seconds]
"""
import sys

import numpy as np
import soundfile as sf
import torch
from transformers import AutoProcessor, MusicgenForConditionalGeneration

out = sys.argv[1]
seconds = float(sys.argv[2]) if len(sys.argv) > 2 else 30.0

PROMPT = (
    "upbeat modern afrobeat pop, warm bright synth chords, light shaker and percussion, "
    "optimistic, 115 bpm, clean instrumental for a mobile app advert"
)

device = "mps" if torch.backends.mps.is_available() else "cpu"
torch.manual_seed(7)

processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small").to(device)

inputs = processor(text=[PROMPT], padding=True, return_tensors="pt").to(device)
tokens = int(seconds * 50)  # 50 tokens per second
audio = model.generate(**inputs, do_sample=True, guidance_scale=3.0, max_new_tokens=tokens)

sr = model.config.audio_encoder.sampling_rate
wav = audio[0, 0].cpu().numpy().astype(np.float32)

# normalise to -1 dBTP; fade in 0.5 s and out over the last 1.5 s unless "nofade" is passed
wav = wav / max(1e-6, np.abs(wav).max()) * 0.89
if "nofade" not in sys.argv[3:]:
    fi, fo = int(sr * 0.5), int(sr * 1.5)
    wav[:fi] *= np.linspace(0, 1, fi)
    wav[-fo:] *= np.linspace(1, 0, fo)

sf.write(out, wav, sr)
print(f"wrote {out} {len(wav)/sr:.1f}s @ {sr}Hz on {device}")
