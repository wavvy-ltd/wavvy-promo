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
| Aisha reminders: tagging + bill reminders by chat (build 13eb129) | `aisha-reminders/` | 1080×1920, 1:38 | release: `wavvy-aisha-reminders-social.mp4` · [contact sheet](gallery/wavvy-aisha-reminders-social.jpg) |
| Kigali social posts: feed, story, wide, square, 3-slide Summit carousel, "Thank you, Africa Fintech Summit" (founders), "Murakoze, Kigali!" (landscape + Instagram) + captions | `kigali-social/` | 1080×1350 · 1080×1920 · 1200×675 · 1080×1080 · 1920×1080 | [posts](kigali-social/posts/) · [captions](kigali-social/CAPTIONS.md) |
| Kigali landing-page photo shoot: shot list, crop guides, mock-up | `kigali-shoot/` | A4 PDF + 1440 px mock-up | [shot list](kigali-shoot/wavvy-kigali-shotlist.pdf) · [mock-up](gallery/kigali-shoot-mockup.png) |
| Ads rebuilt in Wavvy styling: "Small daily expenses" and "25th of the month" | `posters/ads/` | 2160×2700 PNG | [small spends](gallery/wavvy-small-spends.png) · [month end](gallery/wavvy-month-end.png) |
| Aisha voice-over scripts (reminders + chat films), with timings and captions | `aisha-scripts/` | DOCX · MD | [md](aisha-scripts/aisha-voiceover-scripts.md) |
| "Your Money, Your Move" poster: Kenya / Rwanda / East Africa | `posters/money-move/` | 2160×2700 PNG | [ke](gallery/wavvy-poster-ke.png) · [rw](gallery/wavvy-poster-rw.png) · [ea](gallery/wavvy-poster-ea.png) |
| What's New poster (hands holding a card) | `posters/whats-new/` | 2640×3260 PNG | [png](gallery/wavvy-whats-new-poster.png) |
| Partner blog images: Wavvy Wallet × ASU Edson E+I (side by side + stacked), Wavvy Wallet × Plug In Ventures | `partner-logos/` | 1080×1350 PNG | [ASU](partner-logos/posts/wavvy-x-asu-edson.png) · [ASU stacked](partner-logos/posts/wavvy-x-asu-edson-stacked.png) · [Plug In Ventures](partner-logos/posts/wavvy-x-plug-in-ventures.png) |

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

## Partner blog images (`partner-logos/`)
Wavvy Wallet on the left, a grey "×", the partner on the right, on a white 1080×1350 canvas.
`python3 partner-logos/tools/build.py` rebuilds every image in `posts/` from `sources/` (needs Pillow and `rsvg-convert`).
- Wavvy Wallet logo: cut from the blog's existing `wavvy-x-nvidia-2.png`, so partner posts match.
- ASU Edson E+I: cut from the institute's funding-page image, without the "Pay it Forward" box. The source is only 564 px wide, so swap in an official high-res file if ASU sends one.
- Plug In Ventures: the official logo SVG from pluginventures.co.
