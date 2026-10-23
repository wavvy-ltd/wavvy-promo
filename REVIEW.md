# REVIEW — Wavvy Wallet 30 s promo

## Creative calls
- Storyline built: **"Life before and after"** — the M-Pesa inbox piling up (light world) → the app
  organising it (dark world, the phone ≥ 80% of the frame) → flat lavender end card. The storyboard
  was approved in plan mode, so the three-storyline stop was skipped. Not built: "A number lands"
  (one KES figure travelling through every scene) and "Type carries the argument" (kinetic type only).
- Every screen is the real app on the emulator after a fresh account + 25 injected M-Pesa SMS:
  onboarding, empty home, import progress, "52 transactions imported & categorized", home,
  Insights (KES), Budgets (Restaurant 2.13K of 2.5K, 85.2 % Caution), Aisha chat (real answer:
  Food & Dining KES 4,120). Nothing is mocked; the one drawn object is the SMS bubble (real text).
- Voice: Kokoro `af_heart`, 7 lines; music: MusicGen (afrobeat-pop prompt), 0.3 under voice at 2.2.
- Captions are short claims, not the VO verbatim; cap 5 sits in the top band so it never covers
  Aisha's answer.
- Brand colours as the app ships them: ground #0f0f13, accent #7986cb (end card #5c6bc0 for AA
  contrast), M-Pesa green darkened to #2f8f1c for white text.

## Measured vs looked at
- `hyperframes check`: 0 errors, 0 warnings (lint, runtime, layout, motion, contrast, craft).
- Snapshots read: review beats, all six seams, phone sheet at 360 px, plus targeted frames at
  12.2/12.45/12.6/17.1/21.1/25.25/27.5 s after the seam fixes.
- Sound was measured (`hyperframes audio`), not heard: VO ≈ −22 LUFS per file (raised +6.8 dB),
  music −19.2 LUFS (lowered −10.5 dB). Check the rendered file's loudness before posting.

## Weakest shot
- Hook bubbles 5–6 pop in late (0.97 s / 0.63 s on screen) — they are texture, not copy, but a
  stranger may try to read them. With more time: fewer, bigger bubbles and a 0.5 s longer hook.
- The home balance is hidden (• • • • •) because a Ksh 10 test SMS pinned the balance card; the
  hidden state is the app's own privacy toggle, so it reads as real.

## Warnings kept on purpose
- None open after the fixes; `line_unread` on the SMS pile was removed by shortening each bubble to
  ≤ 6 words.
