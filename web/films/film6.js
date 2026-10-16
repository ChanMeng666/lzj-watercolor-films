// 第六部《發明》— 民族發明學
import { keys, ease, easeOut, easeIn, prog, clamp, lerp, hash } from '../lib/engine.js';
import * as fx from '../lib/fx.js';

const W = 2304, H = 1296, TR = 2, lin = x => x;
const F002 = '《劉仲敬訪談 002 論主權者與民族發明》', PL = '《劉仲敬論波蘭民族構建》', YD = '《文明更迭的源代碼》', BA = '《經與史 · 跋》';
const chap = (num, text, t0, t1, o = {}) => ({ style: 'chapter', num, text, t0, t1, ...o });

function bubble(c, x, y, r, a) {   // 虹彩泡泡
  if (a <= 0 || r <= 0) return;
  const g = c.n.createRadialGradient(x - r * 0.3, y - r * 0.3, r * 0.1, x, y, r);
  g.addColorStop(0, `rgba(255,255,255,${0.05 * a})`); g.addColorStop(0.8, `rgba(200,220,255,${0.12 * a})`);
  g.addColorStop(0.93, `rgba(255,190,230,${0.35 * a})`); g.addColorStop(1, `rgba(170,240,220,${0.5 * a})`);
  c.n.fillStyle = g; c.n.beginPath(); c.n.arc(x, y, r, 0, Math.PI * 2); c.n.fill();
  c.n.strokeStyle = `rgba(90,110,150,${0.45 * a})`; c.n.lineWidth = 2; c.n.stroke();
  fx.glow(c.a, x - r * 0.45, y - r * 0.45, r * 0.25, '255,255,255', 0.35 * a);
}

export default {
  title: '發明',
  fadeIn: 1.5, fadeOut: 2.5,
  scenes: [
    { id: 's1_cell', dur: 15, trans: TR, grade: { warm: 0.05 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.6, z: 1.1 }], [15, { x: W * 0.5, y: H * 0.64, z: 1.2 }]], t, lin),
      layers: { membrane: t => ({ grow: lerp(-0.02, 1.02, ease(prog(t, 6.5, 12))), soft: 0.06 }) },
      caps: [
        { t0: 1.4, t1: 6.4, style: 'title', text: '發明', pos: 'center', y: 400 },
        { t0: 2.5, t1: 6.4, style: 'sub', text: '劉仲敬思想 · 水彩短片 其六 —— 民族發明學', pos: 'center', y: 540, wash: false },
        chap('一', '細胞膜', 6.8, 14.6),
        { t0: 7.2, t1: 14.6, style: 'quote', text: '所有民族都是*發明*的，\n民族本身就是為滿足*細胞膜*需要的產生的。', src: '劉仲敬微信言論', pos: 'top', y: 290 },
      ] },
    { id: 's2_names', dur: 14, trans: TR, grade: { warm: 0.25 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.42, z: 1.16 }], [14, { x: W * 0.5, y: H * 0.5, z: 1.08 }]], t, lin),
      caps: [
        chap('二', '與血緣無關', 0.6, 13.6),
        { t0: 1.4, t1: 13.4, style: 'quote', text: '發明的必要性源於*共同體重構*的需要，\n跟真實的血緣出身一點關係都沒有。', src: '劉仲敬 Twitter', pos: 'bottom', y: 960 },
      ] },
    { id: 's3_bubble', dur: 14, trans: TR, grade: { warm: 0.1 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.56, z: 1.12 }], [14, { x: W * 0.5, y: H * 0.42, z: 1.12 }]], t, lin),
      fx: [{ draw: c => {
        const v = c.view(0.45), [bx, by] = c.meta.blow;
        const k = ease(prog(c.t, 1, 9)), pop = c.t > 10.5;
        const [x, y] = v.P(bx + k * 120, by - k * 520);
        if (!pop) bubble(c, x, y, (40 + 330 * k) * v.s, 1);
        else { const e = c.t - 10.5; for (let i = 0; i < 18; i++) { const a = i / 18 * Math.PI * 2; fx.glow(c.a, x + Math.cos(a) * (370 + e * 300) * v.s, y + Math.sin(a) * (370 + e * 300) * v.s, 14, '200,230,255', 0.5 * (1 - e)); }
          c.n.fillStyle = `rgba(110,150,210,${0.8 * (1 - prog(c.t, 11, 13))})`; c.n.beginPath(); c.n.arc(x, y + e * 200, 9, 0, Math.PI * 2); c.n.fill(); }
      } }],
      caps: [
        chap('三', '一滴水吹出的泡沫', 0.6, 13.6),
        { t0: 1.4, t1: 13.4, style: 'quote', text: '它和所有的神話一樣，都像是*一滴水吹出的泡沫*，\n其中有真實的成分，但大部分都是泡沫。', src: '《劉仲敬論近代民族的神話建構》', pos: 'bottom', y: 960 },
      ] },
    { id: 's4_crown', dur: 16, trans: TR, grade: { warm: 0.2 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.42, z: 1.18 }], [16, { x: W * 0.5, y: H * 0.5, z: 1.06 }]], t, lin),
      layers: { crown: t => ({ grow: lerp(-0.05, 1.08, ease(prog(t, 8, 13))), conceal: true, soft: 0.1 }) },
      caps: [
        chap('四', '1789：國民取代國王', 0.6, 15.6),
        { t0: 1.4, t1: 15.6, style: 'quote', text: '最初，文武百官宣誓效忠於國王和憲法；\n接下來，效忠於國王、國民和憲法；\n最後，效忠於國民和憲法，*把國王給刪掉了*。', src: F002, pos: 'top', y: 300, opt: { size: 50 } },
      ] },
    { id: 's5_delta', dur: 16, trans: TR, grade: { warm: 0.1 },
      cam: t => keys([[0, { x: W * 0.55, y: H * 0.35, z: 1.2 }], [16, { x: W * 0.5, y: H * 0.6, z: 1.08 }]], t, lin),
      fx: [{ draw: c => { c.meta.chans.forEach((p, i) => fx.flow(c, p, 0, { n: 4, speed: 0.25, col: '255,255,255', size: 3, k: 0.6, seed: i })); fx.glowAt(c, c.meta.lamp, 0.5, 300, '255,210,140', 0.4); } }],
      caps: [
        chap('五', '1848：語言劃出邊界', 0.6, 15.6),
        { t0: 1.4, t1: 8, style: 'quote', text: '國民民族主義是1789年隨著法國大革命而產生的。\n語言民族主義是隨著1848年的*反革命*而產生的。', src: PL, pos: 'top', y: 290 },
        { t0: 8.4, t1: 15.6, style: 'quote', text: '芬蘭語本來已經是一種快要滅絕的方言。\n芬蘭的商人說的是德語，法院的官員和統治階級說的是瑞典語。', src: F002, pos: 'top', y: 290, opt: { size: 50 } },
      ] },
    { id: 's6_bear', dur: 16, trans: TR, grade: { sat: 0.85, warm: -0.1 },
      cam: t => keys([[0, { x: 1300, y: H * 0.5, z: 1.1 }], [16, { x: 1500, y: H * 0.5, z: 1.14 }]], t, lin),
      layers: { bear: t => ({ dx: lerp(-200, 120, ease(prog(t, 0, 16))), dy: lerp(-60, 40, ease(prog(t, 0, 16))) }) },
      fx: [{ after: 'mid', draw: c => fx.lamps(c, c.meta.lamps, 0.45, { t0: -2, t1: -1, off: [5, 14], seed: 2 }) }],
      caps: [
        chap('六', '帝國的反擊', 0.6, 15.6),
        { t0: 1.4, t1: 8.6, style: 'quote', text: '我們要注意這兩種大型的民族主義，或我稱之為*「假民族主義」*。\n它們之所以產生，都是針對國民民族主義的一種反擊。', src: PL, pos: 'bottom', y: 960, opt: { size: 48 } },
        { t0: 9, t1: 15.6, style: 'quote', text: '沙皇就是人民，人民就是沙皇，\n沙皇和人民彼此之間是根本沒有區別的。', src: PL, pos: 'bottom', y: 960 },
      ] },
    { id: 's7_triptych', dur: 15, trans: TR, grade: { warm: 0.1 },
      cam: t => keys([[0, { x: W * 0.2, y: H * 0.48, z: 1.5 }], [5, { x: W * 0.5, y: H * 0.48, z: 1.5 }], [10, { x: W * 0.8, y: H * 0.48, z: 1.5 }], [15, { x: W * 0.5, y: H * 0.5, z: 1.04 }]], t),
      caps: [
        chap('七', '樹木、木材、雲彩', 0.6, 14.6),
        { t0: 1, t1: 14.6, style: 'quote', text: '如果說國民民族主義像蘊藏樹根的土壤長出的*樹木*，\n奧斯曼主義像斧頭砍倒的*木材*，\n文化泛民族主義就像森林和木材上空漂浮的*雲彩*', src: '《近代史的墮落》', pos: 'bottom', y: 960, opt: { size: 46 } },
      ] },
    { id: 's8_seeds', dur: 14, trans: TR, grade: { warm: 0.05 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.62, z: 1.14 }], [14, { x: W * 0.55, y: H * 0.66, z: 1.2 }]], t, lin),
      layers: { sprouts: t => ({ grow: lerp(-0.02, 1.1, ease(prog(t, 3, 12))), soft: 0.05 }) },
      caps: [
        chap('八', '大多數發明胎死腹中', 0.6, 13.6),
        { t0: 1.4, t1: 13.4, style: 'quote', text: '赫爾德的徒子徒孫發明了很多民族……\n大多數發明其實就*胎死腹中*，被我們忘掉了。', src: F002, pos: 'top', y: 290 },
      ] },
    { id: 's9_boomerang', dur: 16, trans: TR, grade: { warm: 0.1 },
      cam: t => keys([[0, { x: 1100, y: H * 0.5, z: 1.1 }], [6, { x: 1700, y: H * 0.46, z: 1.1 }], [12, { x: 1100, y: H * 0.5, z: 1.14 }], [16, { x: 1100, y: H * 0.52, z: 1.16 }]], t),
      sprites: (t, c) => {
        const [tx, ty] = c.meta.thrower, [fx_, fy] = c.meta.far;
        const out = [{ name: t < 1.5 ? 'thrower_0' : 'thrower_1', x: tx, y: ty, d: 0.45, after: 'mid' }];
        if (t > 1.5 && t < 11.6) {
          const k = (t - 1.5) / 10, a = k * Math.PI * 2;
          const x = tx + (fx_ - tx) * (0.5 - 0.5 * Math.cos(a)), y = ty - 260 + Math.sin(a) * -380 + (fy - ty) * 0.3 * Math.sin(a / 2);
          out.push({ name: 'boomerang', x, y, d: 0.45, rot: t * 14, scale: 1.2 });
        }
        return out;
      },
      fx: [{ draw: c => fx.flash(c, 11.6, { k: 0.5, dur: 0.4 }) }],
      caps: [
        chap('九', '迴力鏢', 0.6, 15.6),
        { t0: 1.4, t1: 8, style: 'quote', text: '十九世紀早期用來對付拿破崙的文化武器\n反而*落到了他們後人的頭上*。', src: YD, pos: 'top', y: 280 },
        { t0: 8.4, t1: 15.6, style: 'quote', text: '扔出去的飛鏢本來只是為了打在別人頭上，\n結果到飛鏢飛回來的時候，*你自己也剛好被打中*。', src: YD, pos: 'top', y: 280 },
      ] },
    { id: 's10_overlay', dur: 15, trans: TR, grade: { warm: 0.05 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.5, z: 1.1 }], [15, { x: W * 0.5, y: H * 0.5, z: 1.2 }]], t, lin),
      layers: {
        red: t => ({ dx: lerp(0, -260, ease(prog(t, 2, 8))), dy: lerp(0, 60, ease(prog(t, 2, 8))) }),
        blue: t => ({ dx: lerp(0, 260, ease(prog(t, 2, 8))), dy: lerp(0, -60, ease(prog(t, 2, 8))) }),
        gaps: t => ({ alpha: ease(prog(t, 7, 10)) }),
      },
      caps: [
        chap('十', '邊界不一致的地方', 0.6, 14.6),
        { t0: 1.4, t1: 14.6, style: 'quote', text: '他們按照帝國民族主義原則和泛文化民族主義原則劃分出來的邊界是不一致的，\n而*邊界不一致的地方*就會自動產生新的國民民族或語言民族。', src: PL, pos: 'bottom', y: 1000, opt: { size: 44, max: 1800 } },
        { t0: 3, t1: 9, style: 'note', text: '帝國超民族主義', x: 420, y: 330 },
        { t0: 4, t1: 9, style: 'note', text: '泛文化民族主義', x: 1520, y: 330 },
      ] },
    { id: 's11_furrow', dur: 18, trans: TR, grade: { sat: 0.9 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.5, z: 1.06 }], [18, { x: W * 0.5, y: H * 0.56, z: 1.16 }]], t, lin),
      layers: { furrow: t => ({ grow: lerp(-0.02, 1.05, ease(prog(t, 1, 8))), soft: 0.05 }) },
      caps: [
        chap('十一', '邊界先於左右', 0.6, 17.6),
        { t0: 1.4, t1: 6.4, style: 'quote', text: '共同體邊界的劃定是*極其殘酷*的過程，\n以致於人們寧願忘記它的存在。', src: BA, pos: 'top', y: 280 },
        { t0: 6.8, t1: 11.6, style: 'quote', text: '在邊界劃定以前，*左與右、溫和與激進*的差別沒有意義。', src: BA, pos: 'top', y: 280 },
        { t0: 12, t1: 17.6, style: 'quote', text: '認同政治的邏輯完全不同於共同體內部的共識政治，\n勝利屬於*邊界最清晰*（也就是認同最強）的一方。', src: BA, pos: 'top', y: 280, opt: { size: 50 } },
      ] },
    { id: 's12_butterfly', dur: 16, trans: TR, grade: { warm: 0.2 },
      cam: t => keys([[0, { x: W * 0.4, y: H * 0.6, z: 1.18 }], [16, { x: W * 0.6, y: H * 0.56, z: 1.1 }]], t, lin),
      sprites: (t, c) => {
        if (t < 4) return [];
        const k = ease(prog(t, 4, 14)), fl = Math.floor(t * 6) % 3;
        const [cx, cy] = c.meta.cat;
        return [{ name: `bfly_${t < 5 ? 0 : fl}`, x: cx + k * 700 + Math.sin(t * 2) * 60, y: cy - k * 380 + Math.sin(t * 3) * 40, d: 0.45, scale: 0.8 + 0.2 * k, alpha: ease(prog(t, 4, 5)) }];
      },
      caps: [
        chap('十二', '蝴蝶與毛蟲', 0.6, 15.6),
        { t0: 1.4, t1: 8.8, style: 'quote', text: '熱愛蝴蝶、厭惡毛蟲是人之常情，歐盟時代的英格蘭確實比克倫威爾時代更舒適，\n問題在於我們*根本就沒有生活在這樣的時代*。', src: BA, pos: 'top', y: 270, opt: { size: 44, max: 1800 } },
        { t0: 9.2, t1: 15.6, style: 'quote', text: '帝國永遠不能成為民族，\n正如*種子標本永遠不會發芽*。', src: '劉仲敬微信言論', pos: 'top', y: 280 },
        { t0: 10, t1: 15.4, style: 'note', text: '標本', x: 1500, y: 640, from: [1520, 660], at: [W * 0.8, H * 0.66, 0.45] },
      ] },
    { id: 's13_towns', dur: 18, grade: { warm: 0.15, sat: 1.05 },
      cam: t => keys([[0, { x: 1300, y: H * 0.5, z: 1.14 }], [18, { x: 1800, y: H * 0.5, z: 1.06 }]], t, lin),
      fx: [{ after: 'mid', draw: c => fx.lamps(c, c.meta.lamps, 0.45, { t0: 6, t1: 12, k: 0.7, warm: '255,214,140' }) }, { draw: c => fx.petals(c, { n: 50, seed: 4 }) }],
      caps: [
        chap('十三', '諸夏', 0.6, 15),
        { t0: 1.4, t1: 15, style: 'quote', text: '未來屬於*諸亞和諸夏*，\n多國體系才是*文明最好的朋友*。', src: '劉仲敬 Twitter', pos: 'top', y: 290, opt: { size: 62 } },
        { t0: 15.3, t1: 18, style: 'sub', text: '劉仲敬思想 · 其六《發明》', pos: 'center', wash: false },
      ] },
  ],
};
