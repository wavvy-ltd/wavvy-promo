# Making a product video with this starter

The film is data. You edit `storyboard.json`; `scripts/build.py` writes the HyperFrames composition
(`index.html`, `compositions/*.html`, `cue-sheet.md`); HyperFrames renders it. Nothing in the film
is drawn from memory: every screen is a capture of the real app, every number is the app's own.

## 1. Decide the story (before any capture)
- One line per feature, in the words a viewer would use. Each line is a shot: *what real screen
  proves it?* If you can't name the screen, cut the line.
- Pace: about 10 s per feature; 60 s for four features. Fast cuts are for launch films, not demos —
  a stranger needs time to read the screen.
- Order: hook (the pain) → reveal (the name) → features → end card (name, claim, store badges).

## 2. Capture the real screens
- Seed the app with believable data first (the Wavvy video injected 25 M-Pesa SMS into the emulator
  with `adb emu sms send`, created budgets, asked the AI a real question). Anything you'd be
  embarrassed to see on camera — test rows, placeholder names — is on camera.
- `scripts/capture.sh <name>` saves the full screen; the phone mockup hides the status bar and nav.
- Real notifications: background the app, trigger the event, `adb shell cmd statusbar
  expand-notifications`, capture, collapse.
- For a scroll in the film, capture the screen at each scroll position (`insights.png`,
  `insights_total.png`); the `scroll` move swaps them with motion.

## 3. Voice (optional)
- Put the lines in `voice[]` with a `start`; run `scripts/tts.sh` (Kokoro, local). It records each
  line and writes the measured `duration` back.
- Place each **phrase** on its picture: the caption and the move that proves a phrase start when the
  phrase is spoken, not when the scene starts. Read `cue-sheet.md` top to bottom and check it.
- Captions are short claims (≤ 5 words), not the voice verbatim; `*word*` highlights one word.

## 4. Music (optional)
- `python3 scripts/music.py assets/audio/take.wav 30 nofade` (MusicGen-small, ~30 s per take).
  Listen or measure; keep a clean take, never gain-fix a bad one.
- `python3 scripts/music_bed.py assets/audio/take.wav assets/audio/music.wav 62` loops it to length
  with equal-power crossfades and a steady level. Set `video.music.src`.
- Music sits at 0.5 under voice (2.2); with no voice raise it to ~0.8.

## 5. Moves (the `feature` scene)
| kind | what it does |
|---|---|
| `card-drop` | a card (SMS, message) arrives at the top and drops into the phone at `drop_at` |
| `show` | cut to `screens[n]`; `rise: true` lifts it in, `settle: true` scales it in with a pop |
| `progress` | a progress bar fills over the current screen (`top`, `width`, `duration`) |
| `scroll` | scroll down to `screens[n]` (image swap with motion) — use before a punch-in on a value |
| `punch` | camera punch-in (`scale`, `x`, `y`): frame the *whole* card/row the voice is about |
| `reset` | camera back to 1× |
| `overlay` / `overlay-out` | drop an image (a real notification shade) over the screen and remove it |
| `zoom-through` | zoom into a point (a tab icon) so the next scene arrives "through" it |
| `hide` | hide `screens[n]` (e.g. the empty state behind a crossfade) |

Transitions: `cut`, `settle` (arrives slightly large and sharpens — after a zoom-through),
`whip-over` (slides in over the previous scene; `from: bottom|top|left|right`), `flood` (end card).
A scene that whips/floods in should **start 0.2 s before the previous one ends**.

## 6. Sounds
Auto cues from the moves (whoosh on whips/scrolls, click on punch-ins and the zoom-through tap, pop
when cards/badges land, notification on overlays, one impact under the end-card mark), each placed
so its peak lands one frame after the picture, on two lanes so they never overlap. `sfx.auto:false`
turns them off; `sfx.extra[]` adds `{t, name, volume}` cues (`click|pop|whoosh|notification|impact`).

## 7. Build, check, look, deliver
```bash
python3 scripts/build.py && npm run check          # 0 errors, 0 warnings before you look
npx hyperframes snapshot --review                    # read the beat sheet and the seams
npm run dev                                          # Studio preview
scripts/deliver.sh promo                             # raw render + loudness-normalised social file
scripts/deliver.sh promo-sfx variants/sfx-only.html raw   # effects-only alternative (no normalise)
```
Review as a stranger: does each frame show what the voice says? Does every punch-in frame the
whole thing? Is any caption covering the thing it names? Snapshot every phrase start, not just
scene midpoints. Sound is measured, not heard — listen once before posting.
