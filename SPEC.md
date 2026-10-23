# SPEC — Wavvy Wallet 30 s vertical promo

GOAL:    A Kenyan M-Pesa user who watches muted on Reels/TikTok understands in 30 s that
         Wavvy Wallet reads their M-Pesa SMS for them and shows where the money went, and
         taps "Get it on Google Play".
OUTPUT:  HyperFrames, 1080 x 1920, 30 fps, voiceover (Kokoro af_heart) + music bed (MusicGen, ~115 bpm)
TIME:    30 s x 30 = 900 frames. 115 bpm -> 15.65 frames/beat; cuts land on VO lines, not drums.

LOOK:    Three worlds, one type system.
         World A "the inbox" (hook): ground #F3F2F8 flat, ink #15151B; M-Pesa SMS bubbles
           #43B02A (M-Pesa green) with white 34 px text, radius 28 px, 0 shadow.
         World B "the app" (proof): ground = the app's own #0F0F13 (the brand ships dark);
           the phone fills >= 62% of the frame height so nothing floats; a 1 px #2A2A33 edge
           and a 0 30px 80px rgba(0,0,0,.55) contact shadow under the phone.
         World C "the claim" (end card): ground #7986CB (app primary, sampled from the UI),
           ink #FFFFFF, the red/green W wallet mark on a white 40 px-radius tile.
         Accent: #7986CB on dark, #43B02A in the inbox, one highlighted word per shot.
         Type: Montserrat from the app's own TTFs (assets/fonts). Hero lines Black 900 at
           112 px, -3% tracking, max 4 words a line. Captions SemiBold 600 at 56 px,
           white, 0.12 s per-word blur-in, bottom of the 168–1330 safe band (y ~ 1180).
         Phone: CSS device at 760 x 1646 (crop of the 1440 x 3120 screenshots without the
           status/nav bars), bezel 14 px #1C1C22, radius 64 px; punch-ins to 1.6x on the panel
           the beat is about; app body text reads >= 26 px after scaling.

OBJECTS: M-Pesa SMS bubble (green, "MPESA" sender line, the real confirmation text);
         the phone with the real screens (empty home, import progress, home with balance,
         transactions list, Insights chart, Budgets, Chat with Aisha);
         the W wallet mark (assets/brand/wavvy-wallet-logo.png); the Google Play badge.

MOTION:  enter expo.out 0.45 s; camera moves power2.inOut 0.5 s; exits power3.in 0.25 s;
         bubble pile: back.out(1.4) 0.35 s each, 80 ms apart; counters linear;
         transitions with a cause: bubble grows into the phone (object becomes world, 0.65 s);
         whip-up 0.25 s between app screens; zoom-through the Insights tab icon (0.6 s);
         colour flood #0F0F13 -> #7986CB in 0.4 s for the end card. No fade+slide-up anywhere.

SHOTS (VO line numbers from the script; VO files assets/audio/vo_0N.wav):
 1  f0–105   (0–3.5 s)  Inbox. Frame 0 already has two green SMS on screen. Bubbles pile in on
             each "another"; at 2.0 s "Where did your money go?" slams in as the hero line over
             the pile. VO1. Sound: music enters at 0, soft key tick per bubble.
 2  f105–210 (3.5–7 s)  The bottom bubble grows past the frame (0.65 s) and its green becomes the
             dark app ground; the phone rises from below holding the onboarding screen
             "Know where your money is going"; the W mark and "Wavvy Wallet" land at 4.6 s.
             VO2 ("Meet Wavvy Wallet") + VO3 starts at 5.6 s. Whoosh once.
 3  f210–375 (7–12.5 s) Phone whips to the empty home; a green SMS slides in from the top edge
             and drops into the phone; the screen cuts to "Organizing Your Money" (progress bar
             fills) then to the home with balance + transactions. Caption "Reads your M-Pesa SMS.
             Zero typing." VO3 continues.
 4  f375–510 (12.5–17 s) Zoom through the Insights tab icon into the Insights screen; punch-in
             1.6x on the Money Flow chart; the top-expense number counts up. Caption
             "See exactly where it goes". VO4.
 5  f510–630 (17–21 s)  Whip to Budgets: bars fill; a budget alert notification card drops in from
             the top (real app copy). Caption "Alerts before you overspend". VO5.
 6  f630–750 (21–25 s)  Whip to Chat: the question types in letter by letter (key ticks), the
             answer bubble appears with the amount. Caption "Ask your money anything". VO6.
 7  f750–900 (25–30 s)  Colour flood to #7986CB; the W tile scales in with back.out; "Know where
             your money is going" lands at 26.2 s; Google Play badge at 27.4 s; hold to the end.
             VO7. Music fades over the last 1.5 s.

BANNED:  dark void with small floating UI (the phone is >= 62% tall); glow/bloom/particles; blue or
         purple mesh gradients (the brand's flat lavender only); cream paper + serif; every element
         fading and sliding up; three cards in a row; a title over a dimmed screenshot; the logo
         docked in a corner; titles that drift after landing; "unlock", "seamless", "effortless".

QA:      f0 (two bubbles visible, no logo), f60 (hero line readable), f140 (phone >= 62% tall),
         f300 (home with balance, text >= 26 px), f440 (chart punch-in sharp), f570 (alert card
         inside the safe band), f690 (answer bubble readable), f820 (end card: mark, line, badge),
         phone sheet at 360 px: every caption legible.
