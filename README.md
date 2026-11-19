# wavvy-promo

Wavvy Wallet promo videos and posters, built with [HyperFrames](https://hyperframes.heygen.com) and HTML.
Every app screen is the real app captured on an emulator; voice and music are generated locally.
**`PROMPTS.md`** lists the briefs, voice/music/image settings and chat questions behind every variant.

## Variants

| Variant | Source | Format | Render |
|---|---|---|---|
| 60 s promo (dark app theme, Kokoro voice) | repo root (`index.html`) | 1080×1920, 60 s | release: `wavvy-promo-60s-social.mp4` |
| 60 s promo, effects only | `variants/sfx-only.html` | 1080×1920, 60 s | release: `wavvy-promo-60s-sfx.mp4` |
| What's New, short cut | `whats-new/` (`tools/make_storyboard.py`) | 1080×1920 | release: `wavvy-whats-new-social.mp4`, `wavvy-whats-new-kenyan-social.mp4` · [contact sheet](gallery/wavvy-whats-new-social.jpg) |
| What's New, step-by-step story v1–v6 (v6 = latest) | `whats-new/` (`tools/make_story.py`) | 1080×1920, 2:48 | release: `wavvy-whats-new-story[-vN]-social.mp4` · [contact sheet](gallery/wavvy-whats-new-story-v6-social.jpg) |
| What's New, one video per update (6 parts) | cut from the story | 1080×1920 | release: `wavvy-whats-new-N-*.mp4` |
| Meet Aisha: chat capabilities | `aisha-chat/` | 1080×1920, 2:31 | release: `wavvy-aisha-chat-social.mp4` · [contact sheet](gallery/wavvy-aisha-chat-social.jpg) |
| "Your Money, Your Move" poster: Kenya / Rwanda / East Africa | `posters/money-move/` | 2160×2700 PNG | [ke](gallery/wavvy-poster-ke.png) · [rw](gallery/wavvy-poster-rw.png) · [ea](gallery/wavvy-poster-ea.png) |
| What's New poster (hands holding a card) | `posters/whats-new/` | 2640×3260 PNG | [png](gallery/wavvy-whats-new-poster.png) |

Videos are attached to the GitHub Release **media-2026-11** (too large for git); posters and contact sheets are in `gallery/`.

## 60 s promo (repo root)
- `index.html` — root composition · `variants/sfx-only.html` — same film, effects only
- `compositions/` — one scene per file · `assets/` — sfx (CC0), screens, brand, Montserrat, audio
- `scripts/` — `seed_sms.sh`, `music.py` / `music_long.py`, `deliver.sh` · `SPEC.md`, `REVIEW.md`

```bash
scripts/deliver.sh                                                   # → wavvy-promo-60s-social.mp4 (−15 LUFS / −1 dBTP)
scripts/deliver.sh wavvy-promo-60s-sfx variants/sfx-only.html raw    # effects only
```
Needs Node 22+, FFmpeg, and network for the GSAP CDN script. `npm run dev` (Studio), `npm run check`, `npm run render`.

## What's New and Aisha films (`whats-new/`, `aisha-chat/`)
Website theme (#376C50 / #4FC385, Nunito), MOSS `kenyan_female` voice, MusicGen bed. Rebuild loop, inside the folder:
```bash
python3 tools/story_vo.py          # voice lines (only changed text is re-recorded)
python3 tools/story_check.py       # whisper check of every take
python3 tools/make_story.py        # storyboard.json from line timings
python3 scripts/build.py           # compositions + index.html
bash scripts/deliver.sh renders/<name>   # render + −15 LUFS social copy
```
Emulator helpers: `tools/m.sh` (Marionette), `tools/login.sh` (reads the app repo's `.patrol.env`, prints nothing),
`aisha-chat/tools/ask.sh` / `act.sh` (type a question, wait for Aisha, approve permissions).

## Posters (`posters/`)
`python3 tools/build.py [ke|rw|ea]` renders the HTML to PNG with headless Chrome.
Album photos and cut-outs of people are not committed; see `PROMPTS.md` §6 to recreate them.
