# wavvy-promo

60-second vertical (1080×1920) promo for Wavvy Wallet, built with [HyperFrames](https://hyperframes.heygen.com).
Every screen is the real app captured on an emulator; voiceover is Kokoro, music is MusicGen — both generated locally.

## Layout
- `index.html` — root composition (timeline, voice/music/sfx clips) · `variants/sfx-only.html` — same film, effects only
- `compositions/` — one scene per file: hook, reveal, track, insights, budgets, chat, endcard, captions
- `assets/sfx/` — UI sounds (bundled HyperFrames library, CC0) · `assets/screens/` — app screenshots · `assets/brand/` — logo and store badges · `assets/fonts/` — Montserrat (the app font) · `assets/audio/` — voice lines and the music bed
- `scripts/` — `seed_sms.sh` (inject M-Pesa SMS into the emulator), `music.py` / `music_long.py` (MusicGen beds)
- `SPEC.md`, `REVIEW.md` — the director's brief and the review note

Renders are not tracked; they are reproducible from this repo.

## Build the video
```bash
scripts/deliver.sh                                        # voiced cut → wavvy-promo-60s-social.mp4 (−15 LUFS / −1 dBTP)
scripts/deliver.sh wavvy-promo-60s-sfx variants/sfx-only.html raw   # effects only: no voice, no music
```
Needs Node 22+, FFmpeg, and network for the GSAP CDN script. Other commands:
```bash
npm run dev      # Studio preview
npm run check    # lint + runtime + layout + motion + contrast
npm run render   # raw render only
```
Voice lines: `npx hyperframes tts "<line>" -v af_heart -o assets/audio/vo_NN.wav` (needs `pip install kokoro-onnx soundfile`).
