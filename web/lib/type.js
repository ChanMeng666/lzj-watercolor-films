// 字幕排版：墨跡逐字暈開（模糊 → 清晰），可橫排／直排
const VW = 1920, VH = 1080;
const cl = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
const sm = t => { t = cl(t); return t * t * (3 - 2 * t); };

const STY = {
  quote:   { font: 'Kai', size: 58, lh: 1.55, cps: 0.075, max: 1640 },
  concept: { font: 'Serif', size: 46, lh: 1.5, cps: 0.06, max: 1400, track: 0.18 },
  title:   { font: 'Serif', size: 150, lh: 1.3, cps: 0.16, max: 1700, track: 0.35 },
  sub:     { font: 'Kai', size: 40, lh: 1.5, cps: 0.05, max: 1500, track: 0.1 },
  vquote:  { font: 'Kai', size: 60, lh: 1.08, cps: 0.085, col: 12 },
  chapter: { font: 'Serif', size: 46, lh: 1.3, cps: 0.09, max: 1400, track: 0.2 },
  note:    { font: 'Kai', size: 40, lh: 1.4, cps: 0.05, max: 640, track: 0.02 },
};
const VERM = [176, 46, 32];

// *重點* 標記 → 朱色
function parseEm(text) {
  let out = '', em = [], on = false;
  for (const ch of text) { if (ch === '*') { on = !on; continue; } out += ch; if (ch !== '\n') em.push(on); }
  return { text: out, em };
}

function chapterCard(ctx, c, T, ink, fin, out) {
  // 朱印：方形印章 + 白字序號
  const x = c.x ?? 110, y = c.y ?? 92, s = 66;
  const k = sm((T - c.t0) / 0.5) * out;
  ctx.save();
  ctx.translate(x + s / 2, y); ctx.rotate(-0.04); ctx.scale(0.8 + 0.2 * k, 0.8 + 0.2 * k);
  ctx.fillStyle = `rgba(${VERM},${0.88 * k})`;
  ctx.beginPath();
  for (let i = 0; i < 24; i++) {     // 略帶毛邊的方形
    const a = i / 24 * Math.PI * 2, r = s / 2 * (1 / Math.max(Math.abs(Math.cos(a)), Math.abs(Math.sin(a))));
    const j = 1 + 0.03 * Math.sin(i * 7.3);
    i ? ctx.lineTo(Math.cos(a) * r * j, Math.sin(a) * r * j) : ctx.moveTo(Math.cos(a) * r * j, Math.sin(a) * r * j);
  }
  ctx.closePath(); ctx.fill();
  ctx.fillStyle = `rgba(248,240,226,${k})`; ctx.font = `${Math.round(s * ((c.num || '').length > 1 ? 0.42 : 0.62))}px Serif`;
  ctx.textAlign = 'center'; ctx.textBaseline = 'middle'; ctx.fillText(c.num || '一', 0, 3);
  ctx.restore();
  const sub = c.sub ? 1 : 0;
  drawCaption(ctx, { ...c, style: '_chap', x: undefined }, T, { x0: x + s + 34, y });
}

function wrap(ctx, text, max, track, size) {
  const lines = [];
  for (const para of text.split('\n')) {
    let cur = '';
    for (const ch of para) {
      const w = ctx.measureText(cur + ch).width + (cur.length + 1) * track * size;
      if (w > max && cur) {
        // 避頭點：標點不放行首
        if ('，。、；：」』）！？'.includes(ch)) { cur += ch; continue; }
        lines.push(cur); cur = ch;
      } else cur += ch;
    }
    lines.push(cur);
  }
  return lines;
}

export function drawCaption(ctx, c, T, left = null) {
  const style = c.style === '_chap' ? 'chapter' : (c.style || 'quote');
  const st = { ...STY[style], ...(c.opt || {}) };
  const dark = c.color === 'paper';
  const ink = dark ? [244, 238, 226] : [40, 33, 29];
  const out = 1 - sm((T - (c.t1 - 0.7)) / 0.7);
  const fin = sm((T - c.t0) / 0.4);
  if (out <= 0) return;
  if (c.style === 'chapter') return chapterCard(ctx, c, T, ink, fin, out);
  const P = parseEm(c.text); const EM = P.em;
  st.cps = Math.min(st.cps, 3.6 / Math.max(1, P.em.length));   // 長句加快顯現
  c = { ...c, text: P.text };
  if (c.style === 'note' && c.to) {   // 墨線箭頭指向畫面中的物件
    const k = sm((T - c.t0 - 0.2) / 0.9) * out;
    const [x0, y0] = c.from || [c.x, c.y + 40], [x1, y1] = c.to;
    const mx = (x0 + x1) / 2 + (y1 - y0) * 0.25, my = (y0 + y1) / 2 - (x1 - x0) * 0.25;
    ctx.save(); ctx.strokeStyle = `rgba(${dark ? '244,238,226' : '60,40,32'},${0.8 * out})`; ctx.lineWidth = 2.4; ctx.lineCap = 'round';
    ctx.beginPath(); const N = 30;
    let px = x0, py = y0;
    ctx.moveTo(x0, y0);
    for (let i = 1; i <= N * k; i++) { const t = i / N; px = (1 - t) ** 2 * x0 + 2 * (1 - t) * t * mx + t * t * x1; py = (1 - t) ** 2 * y0 + 2 * (1 - t) * t * my + t * t * y1; ctx.lineTo(px, py); }
    ctx.stroke();
    if (k > 0.97) { const a = Math.atan2(y1 - my, x1 - mx); ctx.beginPath();
      ctx.moveTo(x1 - Math.cos(a - 0.45) * 18, y1 - Math.sin(a - 0.45) * 18); ctx.lineTo(x1, y1);
      ctx.lineTo(x1 - Math.cos(a + 0.45) * 18, y1 - Math.sin(a + 0.45) * 18); ctx.stroke(); }
    ctx.restore();
  }
  const track = st.track ?? 0.04;
  ctx.save();
  ctx.font = `${st.size}px ${st.font}`;
  ctx.textBaseline = 'middle';
  const chars = [];   // {ch, x, y}
  let box;
  if (c.style === 'vquote') {
    // 直排：右起向左
    const cols = [];
    for (const para of c.text.split('\n')) for (let i = 0; i < para.length; i += st.col) cols.push(para.slice(i, i + st.col));
    const colW = st.size * 1.6, step = st.size * st.lh;
    const x0 = c.x ?? VW * 0.82, y0 = c.y ?? VH * 0.16;
    cols.forEach((col, j) => [...col].forEach((ch, i) => chars.push({ ch, i: chars.length, x: x0 - j * colW, y: y0 + i * step + step / 2 })));
    const hgt = Math.max(...cols.map(s => s.length)) * step;
    box = { x: x0 - (cols.length - 0.5) * colW, y: y0, w: cols.length * colW, h: hgt };
  } else {
    const lines = wrap(ctx, c.text, st.max, track, st.size);
    const lh = st.size * st.lh;
    const cy = left ? left.y : c.y ?? (c.pos === 'center' ? VH * 0.5 : c.pos === 'top' ? VH * 0.18 : VH * 0.8);
    const y0 = cy - (lines.length - 1) * lh / 2;
    let wmax = 0;
    lines.forEach((ln, j) => {
      const arr = [...ln];
      const widths = arr.map(ch => ctx.measureText(ch).width + track * st.size);
      const tw = widths.reduce((a, b) => a + b, 0) - track * st.size;
      wmax = Math.max(wmax, tw);
      let x = left ? left.x0 : (c.x ?? VW / 2) - tw / 2;
      arr.forEach((ch, i) => { chars.push({ ch, i: chars.length, x: x + widths[i] / 2 - track * st.size / 2, y: y0 + j * lh }); x += widths[i]; });
    });
    box = { x: left ? left.x0 : (c.x ?? VW / 2) - wmax / 2, y: y0 - lh / 2, w: wmax, h: lines.length * lh };
  }
  // 襯底：一抹淡彩，保證可讀
  if (c.wash !== false) {
    const cx = box.x + box.w / 2, cy = box.y + box.h / 2;
    const rx = box.w / 2 + st.size * 1.6, ry = box.h / 2 + st.size * 0.9;
    ctx.save(); ctx.translate(cx, cy); ctx.scale(rx, ry);
    const g = ctx.createRadialGradient(0, 0, 0, 0, 0, 1);
    const bc = dark ? '20,18,30' : '248,244,234';
    const a = (dark ? 0.42 : 0.62) * fin * out;
    g.addColorStop(0, `rgba(${bc},${a})`); g.addColorStop(0.6, `rgba(${bc},${a * 0.75})`); g.addColorStop(1, `rgba(${bc},0)`);
    ctx.fillStyle = g; ctx.beginPath(); ctx.arc(0, 0, 1, 0, Math.PI * 2); ctx.fill(); ctx.restore();
  }
  ctx.textAlign = 'center';
  chars.forEach((o, i) => {
    const k = sm((T - c.t0 - i * st.cps) / 0.55);
    if (k <= 0) return;
    const a = k * out;
    const b = (1 - k) * 7;
    ctx.filter = b > 0.3 ? `blur(${b.toFixed(1)}px)` : 'none';
    const col = EM[o.i] ? (dark ? [255, 150, 120] : VERM) : ink;
    ctx.fillStyle = `rgba(${col[0]},${col[1]},${col[2]},${a.toFixed(3)})`;
    ctx.fillText(o.ch, o.x, o.y + (1 - k) * 6);
    if (EM[o.i] && !EM[o.i + 1] && c.style !== 'vquote') {   // 重點詞下的朱筆短線
      ctx.strokeStyle = `rgba(${col[0]},${col[1]},${col[2]},${(0.7 * a).toFixed(3)})`; ctx.lineWidth = 2.5;
      let j = o.i; while (j > 0 && EM[j - 1] && chars[j - 1]) j--;
      ctx.beginPath(); ctx.moveTo(chars[j].x - st.size * 0.45, o.y + st.size * 0.62); ctx.lineTo(o.x + st.size * 0.45, o.y + st.size * 0.66); ctx.stroke();
    }
  });
  ctx.filter = 'none';
  // 出處
  if (c.src) {
    const k = sm((T - c.t0 - chars.length * st.cps - 0.2) / 0.8) * out;
    ctx.font = `${Math.round(st.size * 0.52)}px Serif`;
    ctx.fillStyle = `rgba(${ink[0]},${ink[1]},${ink[2]},${(0.8 * k).toFixed(3)})`;
    if (c.style === 'vquote') {
      ctx.textAlign = 'center';
      const x = box.x - st.size * 1.0;
      [...('——' + c.src)].forEach((ch, i) => ctx.fillText(ch, x, box.y + box.h * 0.35 + i * st.size * 0.6));
    } else {
      ctx.textAlign = 'right';
      ctx.fillText('——' + c.src, box.x + box.w, box.y + box.h + st.size * 0.55);
    }
  }
  // 標題下的細線
  if (c.style === 'title' || c.style === 'concept' || c.style === '_chap') {
    const k = sm((T - c.t0 - 0.3) / 1.2) * out;
    const y = box.y + box.h + st.size * 0.25;
    const w = box.w * 0.6 * k;
    ctx.strokeStyle = `rgba(${ink[0]},${ink[1]},${ink[2]},${(0.55 * k).toFixed(3)})`;
    ctx.lineWidth = c.style === 'title' ? 2.2 : 1.4;
    ctx.beginPath(); ctx.moveTo(box.x + box.w / 2 - w / 2, y); ctx.lineTo(box.x + box.w / 2 + w / 2, y); ctx.stroke();
  }
  ctx.restore();
}
