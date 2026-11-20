# Kigali landing-page photo shoot

Shot list and mock-up for new wavvywallet.com photos taken in Kigali.

- `wavvy-kigali-shotlist.pdf` (source `shotlist.html`): crop guide per landing-page slot (A–F), locations, brand rules, permissions, one-day plan.
- `mockup/sheet.png`: the live site (desktop 1440 px) with photos dropped into every slot.
- `samples/`: stand-in Kigali photos from Wikimedia Commons (location and mood only; credits in `CREDITS.txt`).

## Put the real shoot photos into the mock-up
Name the selects by slot (as in the shot list) and run:
```bash
node tools/mockup.mjs <photos-dir> <out-dir>      # add --no-tags for clean screenshots
```
`A-*` hero · `B-*` How it works (4, in order) · `C-*` Who it's for portraits (4) · `D-*` Financial Freedom card · `E-*` Featured Story.
Missing slots keep the sample (orange "SAMPLE" tag); shoot photos get a green "KIGALI SHOOT" tag.
Needs Node, `puppeteer-core` and Chrome (defaults to the copies bundled with the global `hyperframes` CLI; override with `PUPPETEER_CORE` / `CHROME`). The live site is never modified.

## Rebuild the PDF
```bash
chrome-headless-shell --headless --no-sandbox --allow-file-access-from-files --no-pdf-header-footer \
  --print-to-pdf=wavvy-kigali-shotlist.pdf file://$PWD/shotlist.html
```
