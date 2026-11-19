# Intro improvement plan — Wavvy "What's new" story (v4)

## What the current intro does (0–11 s)
- 0–3 s: six small text cards pile up in the top third of the frame and the bottom two-thirds is empty. The text is tiny on a phone and there are no icons.
- 3–4 s: the cards blur and a small "What's new?" appears, but only from 3 s, so the thumbnail (frame 0) shows tiny cards.
- 4.0–4.5 s: a flat green frame with nothing on it.
- 4.5–11 s: a small logo, then a phone with the dark What's New popup that sits still for about 6.5 s apart from a slow push-in. The popup text is too small to read.
- The voice only starts at 4.65 s, so the first 4.6 s is music alone.
- 11 s: a hard cut to the "1" chapter card.

## New intro (~10 s, light theme, brand green #376C50, Nunito)
1. **0–2.2 s · Title (frame 0 is the thumbnail)**
   - Logo tile and "What's new in Wavvy Wallet" are on screen from the first frame. The title scales in rather than fading in, with a soft green radial glow and a light impact hit.
   - Voice from 0.3 s: "Wavvy Wallet just got better."
2. **2.2–6.0 s · The six updates as a numbered menu**
   - Six large rows fill the frame (about 64 px text). Each has its number badge, an icon (M-Pesa logo, MoMo logo, tag, receipt, bell, in/out arrows) and a short name.
   - The rows pop in one after another in time with the voice, with a soft click each: "Here are six new updates, explained step by step."
   - This row list is the map the chapters come back to.
3. **6.0–9.0 s · Where you'll see them**
   - The phone rises with the real What's New popup and the camera punches in so its list is readable.
   - A red hand-drawn loop goes around the list (same drawing and sound as the rest of the video).
   - Voice: "You'll find them in the What's New popup after you update."
4. **9.0–10.2 s · Into chapter 1**
   - Back on the numbered menu, row 1 highlights and its number badge grows into the chapter 1 card. This replaces the hard cut and connects the intro to the chapter layout.
   - Voice: "Let's start with number one."
   - Chapter 1's line then starts with "Do you save or borrow with KCB M-Pesa?". I'll drop the "Number one." it currently opens with so it isn't said twice.

## Small consistency changes
- Each chapter card keeps its 1-of-6 dots, and the chapter number badge uses the same style as the menu rows.
- Remove the flat green flood frame.
- The new voice lines use the same MOSS kenyan_female voice and get checked by transcription. Only the intro lines and chapter 1's opening line get re-recorded.

## Checks and delivery
hyperframes check with 0 errors, frames every 0.5 s over 0–12 s, a blink check on the new animations, render, −15 LUFS, and a transcription of the first 20 s. Then I'll send v5. The total length stays about 2:45.

## Decisions for Micha
1. Open on the brand title ("What's new in Wavvy Wallet", recommended), or on a relatable question hook ("Missed what changed?")?
2. Keep the real in-app What's New popup beat (recommended, it shows people where to find it), or cut it for a shorter ~7 s intro?
