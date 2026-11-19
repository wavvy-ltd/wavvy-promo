# Wavvy Wallet poster ("Your Money, Your Move!"): plan

Source: Micha's screenshot (1300x1626, 4:5). Rebuild it in HTML using the Wavvy Wallet theme, then export a high-resolution PNG.

## Layout (same as the screenshot)
- Canvas 1080x1350 (4:5), exported at 2x as **2160x2700 PNG**. A 3x export (3240x4050) is available on request.
- Top bar: the Wavvy Wallet logo top-left; the App Store and Google Play badges top-right (official badge PNGs already in the project).
- Headline in two lines, centred: "YOUR MONEY" / "YOUR MOVE!"
- Centre: the person cut-out from the Google Photos album, background removed, standing on white with a soft green glow behind.
- Four notification cards floating around the person: two on the left, two on the right, white with a soft shadow. Each card has the Wavvy app icon, a title, a time and a 2-line message.
- Footer band, light grey #F4F7F6: "Know Your Spending. Make Every Shilling Count." / "Download **Wavvy Wallet** Today." with "Wavvy Wallet" in brand green.

## Theme (from the wavvy-ltd/wavvy-landing repo, the live landing page `landing-next`)
- Font: Nunito (Google Fonts, weights 200–1000), the site's only brand font. The site uses 800 for headings, 700/600 for sub-heads and 500 for body. Poster: headline 900, card titles 800, card text 600, footer 700.
- Colours, from the landing page's CSS variables: background #FFFFFF, surface #FAFAFA, text #111111, muted #5C5C5C, accent #376C50, accent-soft rgba(55,108,80,.12), borders rgba(17,17,17,.08). The secondary green #4fc385 and deep green #113629 are used elsewhere on the site.
- Card style copied from the site: white, 1px border rgba(17,17,17,.08), soft shadow rgba(17,17,17,.06–.1), green glow rgba(55,108,80,.28–.35).
- Headline: line 1 in #111111 and line 2 in #376C50, the landing page's dark-text-plus-accent pairing. This replaces the red line, since Wavvy has no red. Footer band in the site surface colour #FAFAFA.

## Realistic messages (Kenya, Ksh, M-Pesa style)
The screenshot mixes Ksh with Nigerian names and companies (IKEDC, MTN line, Kunle John). These Kenyan versions replace them:
1. **Money sent** · 4:12 PM: "You sent Ksh 2,500 to Wanjiku Kamau. Tagged: Family"
2. **Bill payment** · 2:33 PM: "Ksh 1,000 paid to KPLC Prepaid. Token: 4821-0937-5512…"
3. **Money received** · 1:08 PM: "You received Ksh 15,000 from Brian Otieno"
4. **Airtime** · 11:25 AM: "Ksh 100 airtime bought for your Safaricom line"

## Rwanda version (second poster, same layout)
- Output: `renders/wavvy-poster-rw.png` alongside the Kenya `renders/wavvy-poster-ke.png`.
- Same headline. Footer reads "Know Your Spending. Make Every Franc Count." / "Download **Wavvy Wallet** Today."
- MTN MoMo-style messages in RWF, with Rwandan names and companies:
  1. **Money sent** · 4:12 PM: "You sent 15,000 RWF to Aline Uwase. Tagged: Family"
  2. **Bill payment** · 2:33 PM: "5,000 RWF paid to EUCL Cash Power. Token: 3920-1147-8805…"
  3. **Money received** · 1:08 PM: "You received 50,000 RWF from Eric Habimana"
  4. **Groceries** · 11:25 AM: "6,500 RWF paid to Simba Supermarket. Tagged: Food"
- Same photo as Kenya by default, or a different one from the album if Micha prefers.

## Photo + background removal
- Album "WavvyHighlits" (shared Google Photos link) has 2 photos, both 3072x4080 from a Pixel 7 Pro, downloaded to `assets/album/`:
  - **photo1: family.** A man, a small girl and a smiling woman in glasses looking at a phone she holds (lilac case) at a table, indoors. Warm, happy and the phone is central. The cut-out keeps the three people and drops the room and table; the bottom edge (arms and phone) fades into the white card area.
  - **photo2: woman outdoors.** A woman in a peach T-shirt sits and holds a black phone up beside her face, in front of leaves and a rusty iron fence. A clear single hero, but a neutral expression, and the busy leaves make the hair edge harder.
- Recommendation: **photo1 (family) for Kenya, photo2 (woman) for Rwanda**, so the two posters differ. Alternative: photo1 for both.
- Crop: upper body, top of head about 30 px below the headline, centred.
- Background removal runs locally with rembg (BiRefNet / isnet model) on the CPU, because the GPU is nearly full. I'll check the hair and hand edges at full size before using the cut-out.

## Build + checks
- Project at `/root/videos/wavvy-poster/`: `poster.html` (layout and CSS, local Nunito font), `assets/` (logo, badges, cut-out PNG).
- Export with headless Chrome (Playwright) at deviceScaleFactor 2 → `renders/wavvy-poster.png`.
- Checks: no text clipped or overlapping the person's face or phone, cards readable at phone size (smallest text ≥ 28 px at 1080 width), and a side-by-side with the screenshot.

## Decisions for Micha
1. Headline colours: dark green + light green (recommended), or dark green + ink black.
2. Notification icon: the Wavvy Wallet app icon (recommended), or a generic green tag icon as in the screenshot.
