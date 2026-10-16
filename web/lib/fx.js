// 確定性特效：燈、炊煙、雪、花瓣、落葉、煙花、星、火、燭光。全部是 (t) 的純函數。
import { hash, clamp, ease, lerp, VW, VH } from './engine.js';

const TAU = Math.PI * 2;

export function glow(c, x, y, r, rgb, a) {
  if (a <= 0.002) return;
  const g = c.createRadialGradient(x, y, 0, x, y, r);
  g.addColorStop(0, `rgba(${rgb},${a})`); g.addColorStop(0.35, `rgba(${rgb},${a * 0.35})`); g.addColorStop(1, `rgba(${rgb},0)`);
  c.fillStyle = g; c.fillRect(x - r, y - r, r * 2, r * 2);
}

// 燈：lamps=[[x,y,size]...]；按亂序在 [t0, t1] 間逐盞點亮；off 為熄燈時段
export function lamps(ctx, list, d, { t0 = 0, t1 = 4, off = null, seed = 1, warm = '255,196,110', k = 1, order = null } = {}) {
  const v = ctx.view(d);
  list.forEach((L, i) => {
    const r = order ? order(i, list.length) : hash(i, seed);
    let a = ease((ctx.t - lerp(t0, t1, r)) / 0.35);
    if (off) a *= 1 - ease((ctx.t - lerp(off[0], off[1], hash(i, seed + 7))) / 0.5);
    if (a <= 0) return;
    const fl = 0.85 + 0.15 * Math.sin(ctx.t * 9 + i * 3.1) * Math.sin(ctx.t * 5.3 + i);
    const [x, y] = v.P(L[0], L[1]);
    const s = v.s * (L[2] || 20);
    // 窗內暖光（正常層）
    ctx.n.fillStyle = `rgba(${warm},${0.85 * a})`;
    ctx.n.beginPath(); ctx.n.ellipse(x, y, s * 0.42, s * 0.55, 0, 0, TAU); ctx.n.fill();
    glow(ctx.a, x, y, s * 3.2 * k, warm, 0.32 * a * fl * k);
    glow(ctx.a, x, y, s * 1.1, '255,230,170', 0.4 * a * fl);
  });
}

export function smoke(ctx, pts, d, { k = 1, seed = 3 } = {}) {
  const v = ctx.view(d), c = ctx.n;
  pts.forEach((p, j) => {
    for (let i = 0; i < 14; i++) {
      const life = 6, ph = ((ctx.t + hash(i, j + seed) * life) % life) / life;
      const [x, y] = v.P(p[0] + Math.sin(ph * 5 + i) * 18 + ph * 90, p[1] - ph * 260);
      const r = v.s * (10 + ph * 46);
      const a = 0.16 * Math.sin(ph * Math.PI) * k;
      const g = c.createRadialGradient(x, y, 0, x, y, r);
      g.addColorStop(0, `rgba(200,196,206,${a})`); g.addColorStop(1, 'rgba(200,196,206,0)');
      c.fillStyle = g; c.fillRect(x - r, y - r, r * 2, r * 2);
    }
  });
}

// 雪：三個景深的雪片
export function snow(ctx, { n = 260, wind = 40, k = 1, seed = 5, col = '255,255,255', speed = 1 } = {}) {
  const c = ctx.n, t = ctx.t;
  for (let i = 0; i < n; i++) {
    const z = 0.3 + 0.7 * hash(i, seed);           // 景深
    const sp = (40 + 90 * z) * speed;
    const x0 = hash(i, seed + 1) * (VW + 400) - 200;
    const y0 = hash(i, seed + 2) * (VH + 100);
    let x = x0 + wind * z * t + Math.sin(t * (0.6 + z) + i) * 18 * z;
    let y = (y0 + sp * t) % (VH + 100) - 50;
    x = ((x + 200) % (VW + 400) + (VW + 400)) % (VW + 400) - 200;
    const r = (1.2 + 3.6 * z * z) * k;
    c.fillStyle = `rgba(${col},${(0.55 + 0.4 * z) * Math.min(1, k)})`;
    c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill();
  }
}

// 花瓣／落葉
export function petals(ctx, { n = 70, cols = ['246,190,205', '240,170,190', '252,220,226'], wind = 70, fall = 50, seed = 9, size = 1, k = 1 } = {}) {
  const c = ctx.n, t = ctx.t;
  for (let i = 0; i < n; i++) {
    const z = 0.35 + 0.65 * hash(i, seed);
    const x0 = hash(i, seed + 1) * (VW + 600) - 300, y0 = hash(i, seed + 2) * (VH + 200);
    let x = x0 + wind * z * t + Math.sin(t * 0.9 + i) * 40 * z;
    let y = (y0 + fall * z * t + Math.sin(t * 1.3 + i * 2) * 20) % (VH + 200) - 100;
    x = ((x + 300) % (VW + 600) + (VW + 600)) % (VW + 600) - 300;
    const rot = t * (1 + hash(i, seed + 3) * 2) + i;
    const s = (5 + 9 * z) * size;
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(1, 0.45 + 0.55 * Math.abs(Math.sin(rot * 1.7)));
    c.fillStyle = `rgba(${cols[i % cols.length]},${(0.7 + 0.3 * z) * k})`;
    c.beginPath(); c.ellipse(0, 0, s, s * 0.55, 0, 0, TAU); c.fill();
    c.restore();
  }
}

export function stars(ctx, { n = 220, seed = 8, k = 1, ymax = 0.6 } = {}) {
  const c = ctx.a, t = ctx.t;
  for (let i = 0; i < n; i++) {
    const x = hash(i, seed) * VW, y = hash(i, seed + 1) * VH * ymax;
    const tw = 0.55 + 0.45 * Math.sin(t * (1 + 2 * hash(i, seed + 2)) + i);
    const r = 0.6 + 1.6 * hash(i, seed + 3) ** 3;
    c.fillStyle = `rgba(255,248,230,${0.75 * tw * k})`;
    c.beginPath(); c.arc(x, y, r, 0, TAU); c.fill();
    if (r > 1.6) glow(c, x, y, r * 6, '255,240,210', 0.15 * tw * k);
  }
}

// 煙花：bursts=[[t, x, y, hueRGB], ...] 場景座標
export function fireworks(ctx, bursts, d, { seed = 11 } = {}) {
  const v = ctx.view(d), c = ctx.a, t = ctx.t;
  bursts.forEach((b, j) => {
    const [tb, bx, by, rgb] = b;
    const rise = 1.1, life = 2.6;
    const dt = t - tb;
    if (dt < 0 || dt > rise + life) return;
    const [x0, y0] = v.P(bx, ctx.man.h);
    const [x1, y1] = v.P(bx, by);
    if (dt < rise) {   // 升空
      const k = ease(dt / rise);
      const x = lerp(x0, x1, k), y = lerp(y0, y1, 1 - (1 - k) ** 2);
      glow(c, x, y, 18, '255,220,170', 0.6);
      for (let s = 1; s < 8; s++) glow(c, x, y + s * 9, 7, '255,200,140', 0.25 * (1 - s / 8));
      return;
    }
    const e = dt - rise, f = 1 - e / life;
    if (e < 0.25) glow(c, x1, y1, 260 * v.s * (1 - e / 0.25), '255,240,210', 0.5 * (1 - e / 0.25));
    const N = 90;
    for (let i = 0; i < N; i++) {
      const a = (i / N) * TAU + hash(i, j + seed) * 0.08;
      const spd = (280 + 140 * hash(i, j + seed + 1)) * v.s;
      const dist = spd * (1 - Math.exp(-e * 2.2)) / 2.2 * 2.0;
      const x = x1 + Math.cos(a) * dist, y = y1 + Math.sin(a) * dist + 60 * e * e * v.s;
      const al = f * f * (0.6 + 0.4 * Math.sin(e * 30 + i));
      c.fillStyle = `rgba(${rgb},${al})`;
      c.beginPath(); c.arc(x, y, 2.6 * v.s + 1, 0, TAU); c.fill();
      // 拖尾
      c.strokeStyle = `rgba(${rgb},${al * 0.35})`; c.lineWidth = 2;
      c.beginPath(); c.moveTo(x, y); c.lineTo(x - Math.cos(a) * 26 * f, y - Math.sin(a) * 26 * f - 6); c.stroke();
    }
  });
}

export function fire(ctx, p, d, { k = 1, size = 1 } = {}) {
  const v = ctx.view(d), t = ctx.t;
  const [x, y] = v.P(p[0], p[1]);
  const s = v.s * size;
  const fl = 0.8 + 0.2 * Math.sin(t * 13) * Math.sin(t * 7.7);
  glow(ctx.a, x, y, 520 * s * fl, '255,150,70', 0.30 * k);
  glow(ctx.a, x, y, 160 * s, '255,210,120', 0.55 * k * fl);
  const c = ctx.n;
  for (let i = 0; i < 9; i++) {
    const ph = (t * 1.6 + hash(i, 4)) % 1;
    const fx = x + Math.sin(t * 6 + i * 2) * 16 * s * (1 - ph);
    const fy = y - ph * 120 * s;
    const r = (34 - 28 * ph) * s;
    c.fillStyle = `rgba(255,${Math.round(200 - 120 * ph)},80,${0.55 * (1 - ph) * k})`;
    c.beginPath(); c.ellipse(fx, fy, r * 0.6, r, 0, 0, TAU); c.fill();
  }
}

export function flame(ctx, p, d, { k = 1, size = 1 } = {}) {
  const v = ctx.view(d), t = ctx.t;
  const [x, y] = v.P(p[0], p[1]);
  const s = v.s * size;
  const fl = 0.85 + 0.15 * Math.sin(t * 11) * Math.sin(t * 6.1 + 1);
  glow(ctx.a, x, y, 900 * s * fl, '255,170,90', 0.22 * k);
  glow(ctx.a, x, y, 120 * s, '255,220,150', 0.6 * k * fl);
  const c = ctx.n, sw = Math.sin(t * 3.1) * 3 * s;
  c.fillStyle = `rgba(255,236,170,${0.95 * k})`;
  c.beginPath(); c.moveTo(x - 9 * s, y + 10 * s);
  c.quadraticCurveTo(x - 10 * s, y - 14 * s, x + sw, y - 40 * s * fl);
  c.quadraticCurveTo(x + 10 * s, y - 14 * s, x + 9 * s, y + 10 * s); c.fill();
  c.fillStyle = `rgba(255,150,60,${0.7 * k})`;
  c.beginPath(); c.ellipse(x, y + 4 * s, 5 * s, 9 * s, 0, 0, TAU); c.fill();
}

// 燭光塵埃
export function motes(ctx, p, d, { n = 40, k = 1 } = {}) {
  const v = ctx.view(d), t = ctx.t;
  const [x0, y0] = v.P(p[0], p[1]);
  for (let i = 0; i < n; i++) {
    const a = hash(i, 21) * TAU, r = 80 + 420 * hash(i, 22);
    const x = x0 + Math.cos(a + t * 0.05) * r + Math.sin(t * 0.3 + i) * 20;
    const y = y0 + Math.sin(a) * r * 0.6 - ((t * 8 + i * 37) % 200) + 100;
    glow(ctx.a, x, y, 4 + 3 * hash(i, 23), '255,220,160', 0.5 * k * (0.5 + 0.5 * Math.sin(t + i)));
  }
}

// 水波紋（種子落地）
export function ripple(ctx, p, d, t0, { col = '60,46,36' } = {}) {
  const v = ctx.view(d), e = ctx.t - t0;
  if (e < 0 || e > 2.5) return;
  const [x, y] = v.P(p[0], p[1]);
  for (let i = 0; i < 3; i++) {
    const ee = e - i * 0.3; if (ee < 0) continue;
    const r = ee * 140 * v.s, a = 0.45 * (1 - ee / 2.2);
    if (a <= 0) continue;
    ctx.n.strokeStyle = `rgba(${col},${a})`; ctx.n.lineWidth = 2;
    ctx.n.beginPath(); ctx.n.ellipse(x, y, r, r * 0.22, 0, 0, TAU); ctx.n.stroke();
  }
}

// 光柱（神意光）
export function godrays(ctx, x, y, { k = 1, n = 7, len = 1400, rgb = '255,236,190', seed = 2 } = {}) {
  const c = ctx.a, t = ctx.t;
  for (let i = 0; i < n; i++) {
    const a = Math.PI * 0.5 + (hash(i, seed) - 0.5) * 1.1 + Math.sin(t * 0.2 + i) * 0.03;
    const w = 40 + 120 * hash(i, seed + 1);
    const g = c.createLinearGradient(x, y, x + Math.cos(a) * len, y + Math.sin(a) * len);
    g.addColorStop(0, `rgba(${rgb},${0.10 * k})`); g.addColorStop(1, `rgba(${rgb},0)`);
    c.fillStyle = g; c.beginPath(); c.moveTo(x, y);
    c.lineTo(x + Math.cos(a - w / len) * len, y + Math.sin(a - w / len) * len);
    c.lineTo(x + Math.cos(a + w / len) * len, y + Math.sin(a + w / len) * len); c.fill();
  }
}

// 雲影掠過（時間流逝）
export function cloudShadows(ctx, { k = 1, speed = 160, seed = 4 } = {}) {
  const c = ctx.n, t = ctx.t;
  for (let i = 0; i < 5; i++) {
    const x = ((hash(i, seed) * VW * 2 + t * speed * (0.7 + 0.6 * hash(i, seed + 1))) % (VW * 2)) - VW * 0.5;
    const y = VH * (0.55 + 0.4 * hash(i, seed + 2));
    const r = 500 + 400 * hash(i, seed + 3);
    c.save(); c.translate(x, y); c.scale(1, 0.3);
    const g = c.createRadialGradient(0, 0, 0, 0, 0, r);
    g.addColorStop(0, `rgba(40,40,60,${0.16 * k})`); g.addColorStop(1, 'rgba(40,40,60,0)');
    c.fillStyle = g; c.fillRect(-r, -r, r * 2, r * 2); c.restore();
  }
}

// 雨：斜線
export function rain(ctx, { n = 400, k = 1, angle = 0.25, speed = 1600, seed = 31, col = '200,210,230' } = {}) {
  const c = ctx.n, t = ctx.t;
  c.strokeStyle = `rgba(${col},${0.35 * k})`; c.lineWidth = 1.3;
  c.beginPath();
  for (let i = 0; i < n; i++) {
    const z = 0.4 + 0.6 * hash(i, seed);
    const L = 18 + 30 * z;
    let y = (hash(i, seed + 1) * (VH + 200) + speed * z * t) % (VH + 200) - 100;
    let x = (hash(i, seed + 2) * (VW + 400) + angle * speed * z * t) % (VW + 400) - 200;
    c.moveTo(x, y); c.lineTo(x - angle * L, y - L);
  }
  c.stroke();
}

// 沿折線流動的水點（場景座標）
export function flow(ctx, pts, d, { n = 26, speed = 0.18, col = '120,170,220', k = 1, size = 4, seed = 41 } = {}) {
  const v = ctx.view(d);
  const seg = []; let L = 0;
  for (let i = 0; i < pts.length - 1; i++) { const l = Math.hypot(pts[i + 1][0] - pts[i][0], pts[i + 1][1] - pts[i][1]); seg.push(l); L += l; }
  for (let j = 0; j < n; j++) {
    let u = ((ctx.t * speed + hash(j, seed)) % 1) * L, i = 0;
    while (i < seg.length - 1 && u > seg[i]) { u -= seg[i]; i++; }
    const f = u / seg[i];
    const x = pts[i][0] + (pts[i + 1][0] - pts[i][0]) * f, y = pts[i][1] + (pts[i + 1][1] - pts[i][1]) * f;
    const [sx, sy] = v.P(x, y);
    ctx.n.fillStyle = `rgba(${col},${0.8 * k})`;
    ctx.n.beginPath(); ctx.n.arc(sx, sy, size * v.s * 1.2, 0, Math.PI * 2); ctx.n.fill();
  }
}

export function flash(ctx, t0, { k = 1, dur = 0.6 } = {}) {
  const e = ctx.t - t0; if (e < 0 || e > dur) return;
  const a = (1 - e / dur) ** 2 * k * (0.7 + 0.3 * Math.sin(e * 60));
  ctx.a.fillStyle = `rgba(255,250,235,${0.55 * a})`; ctx.a.fillRect(0, 0, VW, VH);
}

// 場景座標上的暖光（燈籠／烽火）
export function glowAt(ctx, p, d, r, rgb, a) {
  const v = ctx.view(d); const [x, y] = v.P(p[0], p[1]); glow(ctx.a, x, y, r * v.s, rgb, a);
}
