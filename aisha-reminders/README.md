# hyperframes-app-promo-template

A starter for vertical (1080×1920) product promos built with [HyperFrames](https://hyperframes.heygen.com):
real app screens in a phone mockup, scroll/punch-in moves, bottom captions timed to speech, UI sounds,
local voice (Kokoro) and music (MusicGen), and a reproducible render. The whole film is described in
one `storyboard.json`; `scripts/build.py` turns it into the composition.

Grew out of the Wavvy Wallet promo (`examples/wavvy-promo.storyboard.json` is that 60 s film in this format).

## New video in six steps
```bash
# 0. use this template on GitHub, clone it, then:
python3 scripts/placeholders.py      # placeholder screens + logo so it renders right away
python3 scripts/build.py && npm run check && npm run dev   # see the starter in Studio

# 1. edit storyboard.json: brand, colours, logo, badges, scenes, captions, voice lines
# 2. capture real screens:    scripts/capture.sh home   (see GUIDE.md §2)
# 3. voice (optional):        scripts/tts.sh            (writes durations back)
# 4. music (optional):        python3 scripts/music.py assets/audio/take.wav 30 nofade
#                             python3 scripts/music_bed.py assets/audio/take.wav assets/audio/music.wav 62
# 5. build + check + look:    python3 scripts/build.py && npm run check && npx hyperframes snapshot --review
# 6. deliver:                 scripts/deliver.sh promo        → promo.mp4 + promo-social.mp4 (−15 LUFS / −1 dBTP)
```

## What's here
- `storyboard.json` — the film: brand, video, voice, captions, scenes (hook-cards · reveal · feature · endcard), sfx
- `scripts/build.py` — storyboard → `index.html`, `compositions/*.html`, `cue-sheet.md` (generated files are committed so Studio can edit them; rebuild overwrites)
- `templates/` — the HTML skeletons the build fills
- `scripts/` — `capture.sh`, `tts.sh`, `music.py`, `music_bed.py`, `placeholders.py`, `deliver.sh`
- `assets/sfx/` — click, pop, whoosh, notification, impact (HyperFrames bundled library, CC0)
- `assets/brand/` — store badges; your `logo.png`
- `GUIDE.md` — how to plan, capture, time and review a cut (the rules that produced the Wavvy film)

## Requirements
Node 22+, FFmpeg, Python 3; network for the GSAP CDN script at render time. Voice: `pip install
kokoro-onnx soundfile`. Music: `pip install transformers torch soundfile numpy`. Screens: `adb`.
