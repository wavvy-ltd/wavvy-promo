# wavvy-promo

60-second vertical (1080×1920) promo for Wavvy Wallet, built with [HyperFrames](https://hyperframes.heygen.com).
Every screen is the real app captured on an emulator; voiceover is Kokoro, music is MusicGen — both generated locally.

## Layout
- `index.html` — root composition (timeline, voice/music clips)
- `compositions/` — one scene per file: hook, reveal, track, insights, budgets, chat, endcard, captions
- `assets/screens/` — app screenshots · `assets/brand/` — logo and store badges · `assets/fonts/` — Montserrat (the app font) · `assets/audio/` — voice lines and the music bed
- `scripts/` — `seed_sms.sh` (inject M-Pesa SMS into the emulator), `music.py` / `music_long.py` (MusicGen beds)
- `SPEC.md`, `REVIEW.md` — the director's brief and the review note
- `wavvy-promo-60s-social.mp4` — the delivered render (−15 LUFS / −1 dBTP)

## Work on it
```bash
npm run dev      # Studio preview
npm run check    # lint + runtime + layout + motion + contrast
npm run render   # render to MP4
```
Voice lines: `npx hyperframes tts "<line>" -v af_heart -o assets/audio/vo_NN.wav` (needs `pip install kokoro-onnx soundfile`).
