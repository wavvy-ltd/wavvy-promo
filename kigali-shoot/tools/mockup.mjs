// Drop shoot photos into the live wavvywallet.com (desktop 1440 px) and screenshot each section.
// Nothing on the live site changes: the photos are injected into a local headless browser only.
//
//   node tools/mockup.mjs <photos-dir> [out-dir] [--no-tags]
//
// Photos are picked by file-name prefix (the shot-list slot letters); any slot without a photo
// keeps the sample from samples/:
//   A-*        hero (first file)            B-*  How it works, in order (up to 4)
//   C-*        Who it's for portraits (4)   D-*  Financial Freedom card background
//   E-*        Featured Story portrait
// Needs: puppeteer-core (set PUPPETEER_CORE=/path/to/puppeteer-core, default: the one bundled
// with the global hyperframes CLI) and Chrome (CHROME=..., default: hyperframes' headless shell).
import fs from 'node:fs';
import path from 'node:path';
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';

const here = path.dirname(new URL(import.meta.url).pathname);
const root = path.dirname(here);
const args = process.argv.slice(2).filter(a => !a.startsWith('--'));
const tags = !process.argv.includes('--no-tags');
const photosDir = path.resolve(args[0] || path.join(root, 'samples'));
const outDir = path.resolve(args[1] || path.join(root, 'mockup'));
fs.mkdirSync(outDir, { recursive: true });

const PC = process.env.PUPPETEER_CORE ||
  execSync('ls -d $(npm root -g)/hyperframes/node_modules/puppeteer-core').toString().trim();
const puppeteer = createRequire(import.meta.url)(PC);
const CHROME = process.env.CHROME || execSync(
  'ls -d $HOME/.cache/hyperframes/chrome/chrome-headless-shell/*/chrome-headless-shell-linux64/chrome-headless-shell | tail -1'
).toString().trim();

const isImg = f => /\.(jpe?g|png|webp)$/i.test(f);
const list = (dir, prefix) => fs.existsSync(dir)
  ? fs.readdirSync(dir).filter(f => isImg(f) && f.toUpperCase().startsWith(prefix)).sort().map(f => path.join(dir, f))
  : [];
const pick = (prefix, n) => {
  const mine = list(photosDir, prefix), samples = list(path.join(root, 'samples'), prefix);
  return Array.from({ length: n }, (_, i) => mine[i] || samples[i] || null);
};
const dataUrl = f => {
  if (!f) return null;
  const ext = path.extname(f).slice(1).toLowerCase().replace('jpg', 'jpeg');
  return `data:image/${ext};base64,${fs.readFileSync(f).toString('base64')}`;
};
const slots = { A: pick('A-', 1), B: pick('B-', 4), C: pick('C-', 4), D: pick('D-', 1), E: pick('E-', 1) };
const I = Object.fromEntries(Object.entries(slots).map(([k, v]) => [k, v.map(dataUrl)]));
const isSample = Object.fromEntries(Object.entries(slots).map(([k, v]) => [k, v.map(f => !!f && f.includes(`${path.sep}samples${path.sep}`))]));
console.log('slots:', Object.fromEntries(Object.entries(slots).map(([k, v]) => [k, v.map(f => f ? path.basename(f) : '-')])));

const browser = await puppeteer.launch({ executablePath: CHROME, headless: true, args: ['--no-sandbox', '--disable-gpu', '--hide-scrollbars'] });
const page = await browser.newPage();
await page.setViewport({ width: 1440, height: 900, deviceScaleFactor: 1 });
await page.goto('https://wavvywallet.com', { waitUntil: 'networkidle2', timeout: 90000 });
await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 700) { scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } scrollTo(0, 0); });

await page.evaluate((I, S, tags) => {
  const tag = (el, sample) => { if (!tags) return; const t = document.createElement('span'); t.textContent = sample ? 'SAMPLE' : 'KIGALI SHOOT'; t.style.cssText = `position:absolute;left:12px;top:12px;z-index:5;background:${sample ? '#E4572E' : '#376C50'};color:#fff;font:800 11px Nunito,sans-serif;padding:4px 9px;border-radius:99px;letter-spacing:.04em`; el.appendChild(t); };
  if (I.A[0]) {
    const hb = document.querySelector('.ln-hero-bg');
    hb.style.backgroundImage = getComputedStyle(hb).backgroundImage.replace(/url\([^)]*\)\s*$/, `url("${I.A[0]}")`);
    hb.style.backgroundPosition = '62% 50%';
    const hs = document.querySelector('.ln-hero'); if (getComputedStyle(hs).position === 'static') hs.style.position = 'relative';
    const ht = document.createElement('div'); ht.style.cssText = 'position:absolute;left:40px;bottom:40px;width:1px;height:1px'; hs.appendChild(ht); tag(ht, S.A[0]);
  }
  document.querySelectorAll('.ln-hsteps-visual').forEach((v, i) => {
    if (!I.B[i]) return;
    v.style.position = 'relative';
    [...v.children].forEach(c => { if (getComputedStyle(c).position === 'static') c.style.position = 'relative'; c.style.zIndex = 1; });
    const im = document.createElement('img'); im.src = I.B[i];
    im.style.cssText = 'position:absolute;left:0;top:40px;width:330px;height:340px;object-fit:cover;border-radius:28px;box-shadow:0 18px 40px rgba(17,17,17,.18);z-index:0';
    v.prepend(im);
    const w = document.createElement('div'); w.style.cssText = 'position:absolute;left:0;top:40px;width:330px;height:340px;z-index:2;pointer-events:none'; v.appendChild(w); tag(w, S.B[i]);
  });
  document.querySelectorAll('.ln-audience-ico').forEach((s, i) => {
    if (!I.C[i]) return;
    s.innerHTML = '';
    s.style.cssText = `display:inline-block;width:56px;height:56px;min-width:56px;border-radius:50%;background:url(${I.C[i]}) center 30%/cover;box-shadow:0 0 0 3px #fff,0 0 0 5px rgba(55,108,80,.35)`;
  });
  const al = document.querySelector('.ln-impact-audience'); al.style.position = 'relative'; tag(al, S.C.some(Boolean));
  if (I.D[0]) {
    const fc = document.querySelector('.ln-impact-freedom-card');
    fc.style.backgroundImage = `linear-gradient(90deg, rgba(250,250,250,.97) 0%, rgba(250,250,250,.92) 45%, rgba(250,250,250,.3) 75%, rgba(250,250,250,0) 100%), url(${I.D[0]})`;
    fc.style.backgroundSize = 'cover'; fc.style.backgroundPosition = 'center'; fc.style.position = 'relative'; tag(fc, S.D[0]);
  }
  if (I.E[0]) {
    const st = document.querySelector('.ln-testimonial-image'); st.removeAttribute('srcset'); st.src = I.E[0]; st.style.objectFit = 'cover';
    const m = document.querySelector('.ln-testimonial-media'); m.style.position = 'relative'; tag(m, S.E[0]);
  }
}, I, isSample, tags);
await new Promise(r => setTimeout(r, 2500));

const sections = [['1-hero', '.ln-hero'], ['2-steps', '.ln-hsteps'], ['3-impact', '.ln-impact'], ['4-story', '.ln-testimonial-overview']];
for (const [name, sel] of sections) {
  const y = await page.evaluate(s => Math.round(document.querySelector(s).getBoundingClientRect().top + scrollY), sel);
  await page.evaluate(y => scrollTo(0, y), y);
  await new Promise(r => setTimeout(r, 1500));
  await page.screenshot({ path: path.join(outDir, `${name}.png`) });
  console.log('wrote', path.join(outDir, `${name}.png`));
}
await browser.close();
try {
  const o = outDir;
  execSync(`ffmpeg -v error -y -i ${o}/1-hero.png -i ${o}/2-steps.png -i ${o}/3-impact.png -i ${o}/4-story.png -filter_complex "[0][1]hstack[a];[2][3]hstack[b];[a][b]vstack,scale=1600:-1" ${o}/sheet.png`);
  console.log('wrote', path.join(outDir, 'sheet.png'));
} catch { console.log('ffmpeg not found: section PNGs only'); }
