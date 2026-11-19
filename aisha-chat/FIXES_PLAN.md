# Wavvy "What's new" story video — fix plan

Base: `renders/wavvy-whats-new-story-social.mp4` (2:23, 6 chapters, kenyan_female voice, wavvywallet.com green theme).
Kept as is: chapter cards, tap rings, step captions, intro + end card, chapters 2 (MoMo on iPhone), 3 (tagging), 5 (bill reminders).
Recording rules: tour skipped, real SMS sent to the emulator, dev test account, green app theme.

## 1. Chapter 1, KCB M-Pesa: automatic first, manual second
Problem: the video says KCB messages go in through Add Transaction. That's the manual route; with SMS permission the message is read automatically.
- Record: app in the background, `adb emu sms send MPESA "<new KCB M-PESA transfer SMS>"` (new code and amount, so it isn't a duplicate of the pasted one), pull down the notification shade and capture the new-transaction notification, then open the app and capture the new row at the top of Recent Transactions.
- Story:
  - c1a: "If you've allowed SMS access, there's nothing to do. Your KCB M-Pesa messages come in by themselves." (SMS lands → notification → new row, punch-in on it)
  - c1b: "No SMS access? Tap Add Transaction, choose SMS, paste the message, and tap Next." (the existing manual screens, shorter: tap rings on Add Transaction, the SMS tab, Next)
  - c1c: "Wavvy reads it. Tap Import, and it's saved."
- Captions: "Comes in *automatically*" / "Or add it *by* *hand*" / "Tap *Import*".

## 2. Chapter 4, transaction charges: sideways swipe
Problem: the voice says "swipe left" but the screen moves up and down.
- New `swipe-h` move in build.py: crop only the Total Expenses card from `ins_total.png` and the Transaction charges card from `ins_charges.png`, both clipped to the card area. The first slides out to the left while the second slides in from the right; the rest of the screen stays still.
- A finger dot drags right to left across the card at the same moment, plus a whoosh.
- Line c4b becomes: "Swipe that card to the left, and there are your transaction charges for the month."

## 3. Chapter 6: money in and out on the tagging sheet, RWF on payment notifications
Problem: "clearer in and out" means the tagging sheet, and "RWF support" means the notification for a new payment.
- New title: "Money in, money out, and RWF". Question: "Did money come in, or go out?"
- Part A, the tagging sheet (green theme, fresh captures):
  - Open a withdrawal: Mary Wanjiku, − KES 1,250, up arrow.
  - Open a deposit: Peter Otieno, + KES 3,500, down arrow.
  - Tap rings on "Tap to tag", then a punch-in on each sheet's header (sign, amount, arrow).
  - c6a: "When you tag a payment, the sheet shows a minus and an up arrow for money going out…" c6b: "…and a plus and a down arrow for money coming in."
- Part B, the RWF notification:
  - With the app in the background, send `adb emu sms send M-Money "You have received 25,000 RWF from … FT Id: …"`.
  - Capture the shade with Wavvy's new-payment notification, then punch in on the RWF amount.
  - c6c: "And when a new MTN MoMo payment comes in, the notification shows it in Rwandan francs."
- The list and Insights RWF shots come out of this chapter.
- Check before building: I'll read the notification text first. If it shows Ksh, or no notification arrives, I'll stop and report back instead of faking it.

## 4. Unchanged / follow-through
- Re-record only the changed lines (c1a–c1c, c4b, c6a–c6c, c6q) with MOSS kenyan_female, then transcribe them and re-roll any that don't match.
- Timings re-flow from the measured line lengths; the music is re-looped to the new length.
- hyperframes check must show 0 errors, then snapshots at every tap and punch-in, then render and normalise to −15 LUFS.
- Then transcribe the whole video, check a contact sheet, and send the new MP4. Expected length is about 2:30.

## Test data added to the dev account
2–3 new SMS (one KCB M-Pesa, one MTN MoMo RWF payment, possibly one more deposit). Nothing gets tagged or deleted.
