// 逐幀出片：多個無頭 Chrome 並行截圖 → ffmpeg 編碼 + 合音軌
//   node render.mjs film1                         全片（可續傳）
//   node render.mjs film1 --stills 3,20.5,44      單幀預覽 → out/stills/
//   node render.mjs film1 --workers 6 --audio audio/out/film1.wav
//   node render.mjs film1 --encode-only
import http from 'node:http';
import fs from 'node:fs';
import path from 'node:path';
import { spawnSync } from 'node:child_process';
import { chromium } from 'playwright-core';

const ROOT = path.dirname(new URL(import.meta.url).pathname.replace(/^\/([A-Za-z]:)/, '$1'));
const WEB = path.join(ROOT, 'web');
const args = process.argv.slice(2);
const film = args.find(a => !a.startsWith('--')) || 'film1';
const opt = (k, d) => { const i = args.indexOf('--' + k); return i >= 0 ? args[i + 1] : d; };
const has = k => args.includes('--' + k);
const FPS = +opt('fps', 30);
const WORKERS = +opt('workers', 6);
const CHROME = process.env.CHROME || 'C:/Program Files/Google/Chrome/Application/chrome.exe';

const MIME = { '.html': 'text/html', '.js': 'text/javascript', '.json': 'application/json', '.webp': 'image/webp',
  '.jpg': 'image/jpeg', '.png': 'image/png', '.ttf': 'font/ttf', '.otf': 'font/otf' };
const server = http.createServer((req, res) => {
  const p = path.join(WEB, decodeURIComponent(req.url.split('?')[0]));
  if (!p.startsWith(WEB) || !fs.existsSync(p) || fs.statSync(p).isDirectory()) { res.writeHead(404); return res.end(); }
  res.writeHead(200, { 'Content-Type': MIME[path.extname(p)] || 'application/octet-stream', 'Cache-Control': 'max-age=3600' });
  fs.createReadStream(p).pipe(res);
});
await new Promise(r => server.listen(0, r));
const URL0 = `http://127.0.0.1:${server.address().port}/player.html?film=${film}`;

const browser = await chromium.launch({
  executablePath: CHROME, headless: true,
  args: ['--use-angle=d3d11', '--enable-gpu', '--ignore-gpu-blocklist', '--enable-unsafe-swiftshader', '--disable-background-timer-throttling'],
});
async function page() {
  const ctx = await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: 1 });
  const p = await ctx.newPage();
  p.on('console', m => { if (m.type() === 'error') console.error('[page]', m.text()); });
  p.on('pageerror', e => console.error('[pageerror]', e.message));
  await p.goto(URL0);
  await p.waitForFunction(() => window.__ready === true, null, { timeout: 120000 });
  return p;
}
const shot = async (p, t, file) => {
  await p.evaluate(t => window.__seek(t), t);
  await p.screenshot({ path: file, type: 'jpeg', quality: 95, clip: { x: 0, y: 0, width: 1920, height: 1080 } });
};

const OUT = path.join(ROOT, 'out');
if (has('stills')) {
  const p = await page();
  const dir = path.join(OUT, 'stills'); fs.mkdirSync(dir, { recursive: true });
  for (const t of opt('stills').split(',').map(Number)) {
    const f = path.join(dir, `${film}_${t.toFixed(2)}.jpg`);
    const t0 = Date.now(); await shot(p, t, f); console.log(f, Date.now() - t0, 'ms');
  }
} else if (!has('encode-only')) {
  const p0 = await page();
  const dur = +opt('dur', await p0.evaluate(() => window.__meta.dur));
  await p0.context().close();
  const N = Math.round(dur * FPS);
  const dir = path.join(OUT, 'frames', film); fs.mkdirSync(dir, { recursive: true });
  const todo = [];
  for (let i = 0; i < N; i++) if (!fs.existsSync(path.join(dir, `${String(i).padStart(5, '0')}.jpg`))) todo.push(i);
  console.log(`${film}: ${N} frames, ${todo.length} to render, ${WORKERS} workers`);
  const t0 = Date.now(); let done = 0;
  const chunk = Math.ceil(todo.length / WORKERS);
  await Promise.all([...Array(WORKERS)].map(async (_, w) => {
    const mine = todo.slice(w * chunk, (w + 1) * chunk);
    if (!mine.length) return;
    const p = await page();
    for (const i of mine) {
      await shot(p, i / FPS, path.join(dir, `${String(i).padStart(5, '0')}.jpg`));
      if (++done % 100 === 0) {
        const el = (Date.now() - t0) / 1000;
        console.log(`  ${done}/${todo.length}  ${(done / el).toFixed(1)} fps  eta ${((todo.length - done) / (done / el) / 60).toFixed(1)} min`);
      }
    }
    await p.context().close();
  }));
  console.log(`frames done in ${((Date.now() - t0) / 60000).toFixed(1)} min`);
}
await browser.close(); server.close();

if (!has('stills') && !has('frames-only')) {
  const dir = path.join(OUT, 'frames', film);
  const audio = opt('audio', path.join(ROOT, 'audio', 'out', `${film}.wav`));
  const out = opt('out', path.join(OUT, `${film}.mp4`));
  const a = ['-y', '-framerate', String(FPS), '-i', path.join(dir, '%05d.jpg')];
  if (fs.existsSync(audio)) a.push('-i', audio);
  a.push('-c:v', 'libx264', '-preset', 'slow', '-crf', '17', '-tune', 'grain', '-pix_fmt', 'yuv420p', '-movflags', '+faststart');
  if (fs.existsSync(audio)) a.push('-c:a', 'aac', '-b:a', '256k', '-shortest');
  a.push(out);
  console.log('ffmpeg', a.join(' '));
  const r = spawnSync('ffmpeg', a, { stdio: 'inherit' });
  process.exit(r.status ?? 0);
}
