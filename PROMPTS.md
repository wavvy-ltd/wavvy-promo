# Prompts and briefs

Everything used to generate the Wavvy Wallet promo material in this repo: the requests that shaped each
variant (quoted as written), the voice, music and image-generation settings, and the chat questions put to Aisha.
Renders are attached to the GitHub Release `media-2026-11` (see README).

## 1. Requests (as written, in order)

### What's New video (`whats-new/`)
- "using the emulator could you create a video for the whsts new section, make sure to use the app theme colors get them from https://wavvywallet.com"
- "website-promo-video skill and use the kenya_female voice"
- "could you tell it as a section based story for each item, also make it more friendly even for someone not soo experienced in wavvy"
- "remember add transaction is for manual, those who allow SMS permission the message will be parsed automatically"
- "when saying swipe left the animation is swiping vertically"
- "for the easier money going in and money going out is in reference to the tagging sheet and for the support for rwf is in the notification we get on new payments"
- "nice I would like when talking about a transaction or a specific part of the screen highlight using the pencil like illustration with it's FX sound and also saying tagging offline is misleading since a user cannot tag offline they just are notified they are offline"
- "the pencil drawing should not blink" · "and don't circle a highlighted touch area" · "also no need for the pencil, the drawing is enough"
- "I would like to improve the intro, make a plan"
- "the circling is blinking and I had asked earlier ot to do that"
- "convert the list to a more general list not too specific to wavvy"
- "could you split them to 6 videos each per part"

### Aisha chat video (`aisha-chat/`)
- "could you create a video on the capabilities of the wavvy wallet chat features" (format chosen: mobile 1080x1920)

### Aisha reminders video (`aisha-reminders/`)
- "pull latest wavvy wallet and branch getting-stared-2 is theates and update the capabilities of Aisha for reminders video and export"
- Built from `getting-started-2` at 13eb129 ("Let Aisha set tagging and bill reminders for the user."), loaded into the dev app with `flutter attach` + hot restart.

### "Your Money, Your Move" posters (`posters/money-move/`)
- "I would like to recreate this image and use wavvy wallet font and colors and for the messages use realistic examples and for the image select one from [shared Google Photos album] and remove the background from those images, use html to design and create a hd image of it plan first"
- "have one for rwanda"
- "make a third poster with her for comibne kenya and Franc" (East Africa poster)
- "the cut out has a black edge remove it from the girl image"
- "nice, the image looks alittle over exposed" / "not the render the girl image cutout only"

### What's New poster with hands (`posters/whats-new/`)
- Reference: the Hanga Pitchfest '26 "Apply for Hanga Pitchfest if you are…" poster (not included; only the hands cut out of it are kept).
- "create a what's new for wavvy wallet make sure to use wavvy wallet font and theme keep the hands"
- "do everything and send use your suggestions for anything"

### Kigali social posts (`kigali-social/`)
- "could you create social media posts from the shared images" — 26 photos (Sony DSC01545–01569, 18 Nov 2026): Africa Fintech Summit + a man on his phone in front of the Kigali Convention Centre.
- Picks: DSC01567 (feed), 01568 (story), 01559 (wide), 01553 (square), 01551/01545/01547 (carousel). `tools/prep.py` crops and grades them (deep-shadow lift on the backlit portraits, slight warmth in the darks, sky kept); `tools/build.py` renders the posts. Original photos are not committed (public repo).

### Kigali landing-page photo shoot (`kigali-shoot/`)
- "checkout wavvy wallet landing from a desktop view, I would like to take images for the Landing page in Kigali, come up with ideas for framing and locations for wavvy wallet"
- "yeah do that" (one-page shot list with crop guides, and a mock-up with sample Kigali photos) · "all your suggestions"
- Slots measured on wavvywallet.com at 1440 px: hero background (16:10), How it works visuals (≈1:1, right 40 % under the phone), audience icons (56 px circles), Financial Freedom card (≈2.3:1), Featured Story image (649×678).
- Sample photos: Wikimedia Commons search (Unsplash and Pexels block automated access); credits in `kigali-shoot/CREDITS.txt`.

## 2. Theme
From wavvywallet.com (repo wavvy-ltd/wavvy-landing, `landing-next` CSS vars): primary #376C50, secondary #4FC385,
grounds #F4F7F6 / #FFFFFF / #FAFAFA, ink #111111, muted #5C5C5C, deep green #113629. Font: Nunito (200–1000).
App filmed with Settings → Switch Theme → Green. The original 60 s promo (repo root) uses the app's dark theme
(#0F0F13, lavender #7986CB, Montserrat).

## 3. Voice (MOSS-TTS on the LAN server)
`POST /v1/audio/speech` with `model: moss-tts`, `voice: kenyan_female`, `language: English`, `temperature: 1.0`,
`emotion: happy`, `seed: 7` (re-rolled per line when a take garbled a word; seed stored in `assets/audio/story/meta.json`).
"MTN MoMo" is sent as "M T N MoMo".

- Story videos (What's New story, Aisha), `tools/story_vo.py`, instructions:
  > A warm, friendly guide explaining a money app to a first-time user. Clear, patient and encouraging, natural Kenyan English, unhurried.
- What's New short cut, `tools/vo_moss.py`, instructions:
  > A warm, upbeat product announcer for a mobile money app. Clear, confident, natural Kenyan English, lively but unhurried.
- Each take is trimmed (lead/tail, pauses capped at 0.5 s) and checked with faster-whisper small.en (`tools/story_check.py`).
- Original 60 s promo: Kokoro `af_heart` (`npx hyperframes tts "<line>" -v af_heart`).

### What's New story lines (`whats-new/tools/story_lines.py`)
| id | Voice line | Caption |
|---|---|---|
| i1 | Wavvy Wallet just got better. | — |
| i2 | Here are six new updates, explained step by step. | — |
| i3 | You'll find them in the What's New popup, after you update. | — |
| i4 | Let's start with number one. | — |
| c1q | Do you save or borrow with KCB M-Pesa? Now those messages can go into Wavvy too. | — |
| c1a | If you've allowed SMS access, there's nothing to do. Your KCB M-Pesa messages come in by themselves. | Comes in automatically |
| c1n | You get a notification, and the payment is already in your list. | Notified, and already in |
| c1b | No SMS access? Tap Add Transaction, choose SMS, paste the message, and tap Next. | No SMS access? Add by hand |
| c1c | Wavvy reads it. Tap Import, and it's saved. | Tap Import |
| c2q | Number two is for iPhone users with MTN MoMo. | — |
| c2a | You can now bring in your MoMo messages, and even your PDF statements. | MoMo SMS + PDF statements |
| c2b | Wavvy sorts them into the right categories for you. | Sorted for you |
| c3q | Number three. Tagging simply means saying what a payment was for, like food, rent, or family. | — |
| c3a | Tap any transaction that says, tap to tag. | Look for Tap to tag |
| c3b | If your internet drops, the tag screen tells you straight away. Tagging needs internet, so just reconnect, and carry on. | Offline? It tells you |
| c3c | Once you're back online, type what it was for, and pick a tag. | Type, then pick a tag |
| c3d | Done. The payment is now tagged. | Done! |
| c4q | Number four. Every time you send money, there's a small fee. Do you know how much they add up to? | — |
| c4a | Open Insights, and find Total Expenses. | Insights, Total Expenses |
| c4b | Swipe that card to the left, and there are your transaction charges for the month. | Swipe left for charges |
| c5q | Number five. Never forget rent, internet, or Netflix again. | — |
| c5a | Open the menu. Then choose, Bill Reminders. | Menu, then Bill Reminders |
| c5b | Add the bill's name, the due date, and how often it repeats. | Name, date, repeat |
| c5c | Wavvy reminds you the day before, and on the day. | Alerts the day before |
| c5d | You choose which alerts you get in Settings, under Notifications. | Settings, Notifications |
| c6q | And number six. Money in and money out are now easier to tell apart, and Rwandan francs are supported. | — |
| c6a | When you tag a payment, money going out shows a minus, and an up arrow. | Minus and up: money out |
| c6b | Money coming in shows a plus, and a down arrow. | Plus and down: money in |
| c6c | And when a new MTN MoMo payment comes in, the notification shows it in Rwandan francs. | MoMo alerts in RWF |
| o1 | That's what's new. Update Wavvy Wallet today, and know where your money is going. | — |

### Aisha chat lines (`aisha-chat/tools/story_lines.py`)
| id | Voice line | Caption |
|---|---|---|
| i1 | Meet Aisha, the money assistant inside Wavvy Wallet. | — |
| i2 | Ask her anything, in plain words. Here are six things she can do for you. | — |
| h1 | To find her, open Wavvy Wallet, and tap Chat at the bottom. | Tap Chat |
| h2 | The first time, read the short note, then tap, Continue to chat. | Tap Continue to chat |
| i4 | Let's start with number one. | — |
| c1q | Number one. Ask Aisha about your spending. | — |
| c1a | Type a question, like, how much did I spend this month? Then tap send. | Type, then tap send |
| c1b | Aisha adds it all up in seconds, and shows how much is still untagged. | Totals in seconds |
| c1c | Ask where most of your money goes, and she names your biggest costs. | Your biggest costs |
| c2q | Number two. Find any payment, fast. | — |
| c2a | Ask about anyone you pay. Show me my payments to Mary Wanjiku. | Ask about anyone |
| c2b | She finds every payment, with the dates and fees, and even spots a pattern. | Dates, fees, patterns |
| c3q | Number three. Tag payments, just by chatting. | — |
| c3a | Tell her what a payment was for. Tag the Kings Court payment as rent. | Say what it was for |
| c3b | Aisha always asks before she changes anything. Tap, Allow Once. | She asks first |
| c3c | Done. Your rent is tagged, and she offers to do it every month. | Tagged! |
| c4q | Number four. Cash spending counts too. | — |
| c4a | Paid with cash? Just tell her. I paid two hundred and fifty shillings cash for lunch. | Just tell her |
| c4b | Allow it, and the cash payment is added to your list. | Cash payment added |
| c5q | Number five. Plan ahead with Aisha. | — |
| c5a | Ask her to plan a weekend trip to Diani, with twenty thousand shillings. | Plan a trip |
| c5b | She splits it into transport, a place to stay, food, activities, and a little extra, and checks it against your usual spending. | Split into a plan |
| c5c | Say yes, and she creates a trip category, so you can track every shilling. | Every shilling tracked |
| c6q | And number six. Aisha can change the app, and listen too. | — |
| c6a | Ask for a purple theme, and the whole app changes colour. | Ask for a new colour |
| c6b | Ask for green again, and it's back. | Back to green |
| c6c | Rather talk than type? Tap the microphone, and just speak. | Tap the mic and speak |
| o1 | Aisha is in beta, so double check anything important. Open Wavvy Wallet, tap Chat, and say hello. | — |

### Aisha reminders lines (`aisha-reminders/tools/story_lines.py`)
| id | Voice line | Caption |
|---|---|---|
| i1 | Aisha can now set your reminders for you. | — |
| i2 | Here are four ways she helps you stay on top of your money. | — |
| i4 | Let's start with number one. | — |
| c1q | A weekly reminder to tag your payments. | — |
| c1a | Untagged payments pile up. On your home screen, a new card offers a tagging reminder. | A new home card |
| c1b | Or just ask Aisha. Remind me to tag my transactions every Friday at six p.m. | Just ask Aisha |
| c1c | Done. Every Friday at six, Wavvy reminds you to tag. | Fridays at 6 PM |
| c2q | Number two. Never miss a bill. | — |
| c2a | Tell Aisha about the bill. Remind me to pay rent of eighteen thousand shillings on the fifth of every month. | Tell her the bill |
| c2b | She doesn't guess. She asks when you'd like to be alerted. | She asks first |
| c3q | Number three. You choose the alerts. | — |
| c3a | Answer, two days before, and one day before. | Pick your alerts |
| c3b | Your rent reminder is saved, with an alert on the due date too. | Rent reminder saved |
| c4q | And number four. Check and tidy your reminders. | — |
| c4a | Ask, what bill reminders do I have? Aisha lists them all. | See them all |
| c4b | She even spots a duplicate rent reminder, and deletes it when you say yes. | Duplicates removed |
| c4c | Change a time just by asking. Move my Netflix reminder to eight p.m. | Change it by asking |
| c4d | Everything shows up in Bill Reminders. Your tagging reminder is in Settings, under Notifications. | All in one place |
| o1 | Open Wavvy Wallet, tap Chat, and let Aisha remind you. | — |

## 4. Music (MusicGen)
`scripts/music.py`: `facebook/musicgen-small`, `torch.manual_seed(7)`, ~30 s take, run on CPU (`CUDA_VISIBLE_DEVICES=`) when the GPU is busy;
`scripts/music_bed.py` loops/crossfades it to the film length (`assets/audio/music_story.wav`). Prompt:
> upbeat modern afrobeat pop, warm bright synth chords, light shaker and percussion, optimistic, 115 bpm, clean instrumental for a mobile app advert

Sound effects: bundled HyperFrames UI library (CC0) plus a synthesized pencil scribble (`whats-new/tools/pencil_sfx.py`).

## 5. Aisha chat footage
Real chats with Aisha 2.0 on the dev build (emulator, dev account), typed with `aisha-chat/tools/ask.sh` / `act.sh`.
Every write action was approved on the "Permission Required" sheet with *Allow Once*.

| Chapter | Question typed | Aisha's reply (abridged) |
|---|---|---|
| 1 | How much did I spend this month? | KES 37,550 across 12 transactions (plus RWF 21,500); KES 25,200 uncategorized |
| 1 | Where does most of my money go? | Kings Court Apartments KES 18,000 (rent), then Shopping and Household |
| 2 | Show me my payments to Mary Wanjiku | KES 2,500 in two transfers (13 and 15 Nov) plus KES 36 fees; spots the pattern |
| 3 | Yes, tag the Kings Court payment as Rent | Permission: Tag Transaction → tagged |
| 4 | I paid KES 250 cash for lunch today, add it | Permission: Add Transaction → added |
| 5 | Help me plan a weekend trip to Diani with KES 20,000 | Transport / accommodation / food / activities / buffer split, compared with usual spending |
| 5 | Yes, just create the category for now | Permission: Create Category → Diani Trip created |
| 6 | Change the theme to purple · Switch it back to green | Permission: Change Theme → theme switched |
| 6 | (mic button) | "Listening…" bar |

### Aisha reminders chat (new chat, build 13eb129)
| Question typed | Aisha's reply (abridged) |
|---|---|
| Remind me to tag my transactions every Friday at 6pm | Reminder set for every Friday at 6:00 PM |
| Remind me to pay rent of KES 18,000 on the 5th of every month | Asks which early alerts you want |
| 2 days before and 1 day before | Rent reminder saved: 5th monthly, 9:00 AM, alerts 2 days and 1 day before (plus due time) |
| What bill reminders do I have? | Lists 3, spots two rent reminders and offers to delete the older one |
| Yes, delete the old one | Deleted; 2 left (Rent on the 5th, Netflix on the 28th) |
| Move my Netflix reminder to 8pm | Netflix now 8:00 PM, alerts unchanged |

Typed-question frames: Marionette screenshots leave the keyboard area blank, so the real Gboard keyboard from an
`adb screencap` is pasted into it (`aisha-reminders/tools/add_keyboard.py`). The home screenshot's "PRO PLUS (EXPIRED)"
badge (a dev-account artefact) was painted out with the header colour.

## 6. Images
- Poster photo cut-outs: `rembg` with `birefnet-general`, `post_process_mask=True` (`posters/money-move/tools/cutout.py`).
- Dark fringe removal: `tools/defringe.py` (alpha eroded 2 px, soft-edge pixels recoloured from the nearest solid foreground).
- Exposure fix on the East Africa cut-out: `tools/grade.py` strength 1.0 (−0.35 stop, highlight knee 0.72, +10 % midtone contrast, +8 % saturation).
- Hands for the What's New poster: chroma-keyed off the reference's navy, on-card parts keyed by darkness against the white card (`posters/whats-new/tools/hands.py`).
- Poster copy and messages: `posters/money-move/PLAN.md` and the `ROWS` list in `posters/whats-new/tools/build.py`.
- Album photos and cut-outs of people are not committed (public repo); place them in `posters/money-move/assets/{album,cutout}/` to rebuild.

## 7. Demo data
16 M-PESA and MTN MoMo (RWF) messages injected into the emulator: `whats-new/tools/seed_sms.json`. Names are fictional.
