// 第十一部《霉菌》— 宗教與秩序
import { keys, ease, easeOut, easeIn, prog, clamp, lerp, hash } from '../lib/engine.js';
import * as fx from '../lib/fx.js';

const W = 2304, H = 1296, TR = 2, lin = x => x;
const TW = '劉仲敬 Twitter', YD = '《文明更迭的源代碼》', SJ = '《數卷殘編》', WX = '劉仲敬微信言論';
const chap = (num, text, t0, t1, o = {}) => ({ style: 'chapter', num, text, t0, t1, ...o });

export default {
  title: '霉菌',
  fadeIn: 1.5, fadeOut: 2.5,
  scenes: [
    { id: 's1_candles', dur: 15, trans: TR, grade: { warm: 0.2 },
      cam: t => keys([[0, { x: W * 0.46, y: H * 0.6, z: 1.18 }], [15, { x: W * 0.5, y: H * 0.56, z: 1.08 }]], t, lin),
      fx: [{ draw: c => { fx.stars(c, { n: 160, k: 0.7 });
        fx.lamps(c, c.meta.candles, 0.45, { t0: 3, t1: 12, order: (i, n) => i / n, warm: '255,200,120' });
        fx.lamps(c, c.meta.wins, 0.45, { t0: 9, t1: 13, seed: 4 });
        fx.flame(c, c.meta.hand, 0.45, { size: 0.5 }); } }],
      caps: [
        { t0: 1.4, t1: 6.6, style: 'title', text: '霉菌', pos: 'center', y: 400, color: 'paper' },
        { t0: 2.5, t1: 6.6, style: 'sub', text: '劉仲敬思想 · 水彩短片 其十一 —— 宗教與秩序', pos: 'center', y: 540, wash: false, color: 'paper' },
        chap('一', '秩序的生產者', 7, 14.4, { color: 'paper' }),
        { t0: 7.4, t1: 14.4, style: 'quote', text: '原教旨主義者是*秩序的生產者*，\n霉菌繁榮的地方就沒有細菌。', src: TW, color: 'paper', pos: 'top', y: 290, opt: { size: 58 } },
      ] },
    { id: 's2_dish', dur: 16, trans: TR, grade: { expo: 1.02 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.53, z: 1.0 }], [16, { x: W * 0.48, y: H * 0.55, z: 1.08 }]], t, lin),
      layers: {
        bact: t => ({ grow: lerp(-0.02, 1.05, ease(prog(t, 0.3, 4.5))), soft: 0.1 }),
        bact_in: t => ({ grow: lerp(-0.02, 1.02, ease(prog(t, 5, 12))), conceal: true, soft: 0.06, alpha: ease(prog(t, 0.3, 2.5)) }),
        mould: t => ({ grow: lerp(-0.02, 1.1, ease(prog(t, 3, 12))), soft: 0.08 }),
      },
      caps: [
        chap('二', '青霉素', 0.6, 15.6, { color: 'paper' }),
        { t0: 1.4, t1: 7.6, style: 'quote', text: '伊斯蘭教組織發達的地方，\n恰好是伊斯蘭國*最難滲入*的地方。', src: TW, color: 'paper', pos: 'top', y: 150, opt: { size: 44 } },
        { t0: 8, t1: 15.6, style: 'quote', text: '青霉素產生於霉菌繁榮的地方，\n因為細菌害怕的對手*不是人類而是霉菌*。', src: TW, color: 'paper', pos: 'top', y: 150, opt: { size: 44 } },
        { t0: 9, t1: 15, style: 'note', text: '抑菌圈', x: 1620, y: 860, at: [W * 0.5 - 70 + 200, H * 0.59 + 24 + 150, 0.4], opt: { size: 34 }, color: 'paper' },
      ] },
    { id: 's3_wipe', dur: 15, trans: TR, grade: t => ({ sat: lerp(1, 0.85, prog(t, 4, 12)), warm: -0.05 }),
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.53, z: 1.06 }], [15, { x: W * 0.5, y: H * 0.52, z: 1.0 }]], t, lin),
      layers: {
        mould: t => ({ grow: lerp(-0.02, 1.04, ease(prog(t, 1.5, 6))), conceal: true, soft: 0.05 }),
        flood: t => ({ grow: lerp(-0.02, 1.3, ease(prog(t, 2.5, 9))), soft: 0.08 }),
        hard: t => ({ grow: lerp(-0.02, 1.05, ease(prog(t, 8.5, 13.5))), soft: 0.1 }),
      },
      sprites: (t, c) => { const [cx, cy, R] = c.meta.dish, k = ease(prog(t, 1.5, 6)); if (t < 1 || t > 6.6) return [];
        return [{ name: 'cloth', x: lerp(cx - R - 120, cx + R + 120, k), y: cy + Math.sin(k * 18) * 180, d: 0.4, rot: Math.sin(k * 18) * 0.2, alpha: ease(prog(t, 1, 1.5)) * (1 - ease(prog(t, 6, 6.6))) }]; },
      caps: [
        chap('三', '抗生素', 0.6, 14.6, { color: 'paper' }),
        { t0: 1.4, t1: 8, style: 'quote', text: '伊斯蘭國容易扎根的地方，都是列寧黨國或社會工程國家。\n這些世俗主義政權通過反對傳統伊斯蘭，*嚴重降低了社會組織復雜度*。', src: TW, color: 'paper', pos: 'top', y: 150, opt: { size: 36, max: 1450 } },
        { t0: 8.4, t1: 14.6, style: 'quote', text: '制造原子化對組織力量最強的宗教有利，盡管她是最大攻擊對象。\n抗生素對*耐葯性最強的細菌*最有利，對益生菌最有害。', src: SJ, color: 'paper', pos: 'top', y: 150, opt: { size: 36, max: 1450 } },
      ] },
    { id: 's4_cell', dur: 14, trans: TR, grade: { warm: 0.2 },
      cam: t => keys([[0, { x: W * 0.42, y: H * 0.56, z: 1.12 }], [14, { x: W * 0.56, y: H * 0.6, z: 1.16 }]], t, lin),
      layers: { books: t => ({ dx: Math.sin(t * 1.4) * 10 * prog(t, 2, 6), alpha: lerp(1, 0.35, ease(prog(t, 7, 12))) }) },
      fx: [{ after: 'fig', draw: c => { fx.flame(c, c.meta.flame, 0.45, { size: 0.9 }); fx.motes(c, c.meta.flame, 0.45, { n: 30, k: 0.6 }); } }],
      caps: [
        chap('四', '虔誠與學問', 0.6, 13.6, { color: 'paper' }),
        { t0: 1.4, t1: 7.2, style: 'quote', text: '任何思想都不是秩序的生產或秩序的來源，只是秩序的解釋。\n虔誠和狂熱的信仰是秩序的來源，但*並不需要任何知識*。', src: TW, color: 'paper', pos: 'top', y: 200, opt: { size: 42, max: 1800 } },
        { t0: 7.6, t1: 13.6, style: 'quote', text: '每十個神學家就起碼有八個人有動機說，\n耶穌本人的話其實很淺陋，*都是些比喻和故事*', src: YD, color: 'paper', pos: 'top', y: 200, opt: { size: 46 } },
      ] },
    { id: 's5_rose', dur: 12, trans: TR, grade: { expo: 1.04 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.5, z: 1.2 }], [12, { x: W * 0.5, y: H * 0.5, z: 1.04 }]], t, lin),
      layers: { rose: t => ({ grow: lerp(-0.02, 1.04, ease(prog(t, 0.5, 6))), soft: 0.06 }) },
      fx: [{ draw: c => { fx.stars(c, { n: 200, k: 0.9 }); const [x, y, R] = c.meta.rose; fx.glowAt(c, [x, y], 0.3, R * 1.4, '255,220,160', 0.25 * ease(prog(c.t, 5, 8)));
        const v = c.view(0.3), k = ease(prog(c.t, 6, 9)); if (k <= 0) return; const S = c.meta.stars;
        c.a.strokeStyle = `rgba(230,220,255,${0.4 * k})`; c.a.lineWidth = 1.5; c.a.beginPath();
        S.forEach((p, i) => { const [a, b] = v.P(p[0], p[1]); i ? c.a.lineTo(a, b) : c.a.moveTo(a, b); }); c.a.closePath(); c.a.stroke();
        S.forEach(p => { const [a, b] = v.P(p[0], p[1]); fx.glow(c.a, a, b, 18, '240,236,255', 0.8 * k); }); } }],
      caps: [
        chap('五', '神意', 0.6, 11.6, { color: 'paper' }),
        { t0: 1.4, t1: 11.4, style: 'quote', text: '中世紀思想有一基本前提：*神意構成一切秩序本原*，\n包括政治秩序與自然秩序。', src: SJ, color: 'paper', pos: 'bottom', y: 1010, opt: { size: 46 } },
      ] },
    { id: 's6_ship', dur: 14, trans: TR, grade: { warm: 0.2 },
      cam: t => keys([[0, { x: 1100, y: H * 0.56, z: 1.12 }], [14, { x: 1900, y: H * 0.56, z: 1.12 }]], t, lin),
      sprites: (t, c) => [{ name: 'ship', x: lerp(700, 2350, ease(prog(t, 0, 13))), y: c.meta.sea_y + Math.sin(t * 1.3) * 10, rot: Math.sin(t * 1.1) * 0.03, d: 0.4, after: 'sea' }],
      caps: [
        chap('六', '種子', 0.6, 13.6),
        { t0: 1.4, t1: 7, style: 'quote', text: '清教徒卻是*種子*，你的子孫終將仰仗他們的仁慈。', src: SJ, pos: 'top', y: 290, opt: { size: 54 } },
        { t0: 7.4, t1: 13.6, style: 'quote', text: '殉道者的家屬是老幹部遺孀級包養的，\n勞動隱居團體的產品是*無條件包買包銷*的。', src: TW, pos: 'top', y: 280 },
      ] },
    { id: 's7_granary', dur: 16, trans: TR, grade: t => ({ sat: lerp(1, 0.55, ease(prog(t, 8.5, 11))), warm: lerp(0.2, -0.1, prog(t, 8.5, 11)) }),
      cam: t => keys([[0, { x: 1150, y: H * 0.58, z: 1.12 }], [16, { x: 1500, y: H * 0.6, z: 1.12 }]], t, lin),
      layers: { boards: t => (t < 9 ? { hide: true } : { alpha: ease(prog(t, 9, 9.6)) }) },
      sprites: (t, c) => t < 10 ? [] : [0, 1, 2].map(i => ({ name: `wander_${Math.floor(t * 3 + i) % 4}`, x: 1300 + i * 260 + (t - 10) * 120, y: c.meta.road_y + i * 10, d: 0.45, scale: 0.8, alpha: ease(prog(t, 10 + i * 0.5, 11 + i * 0.5)), after: 'mid' })),
      fx: [{ after: 'mid', draw: c => { const k = 1 - ease(prog(c.t, 8, 9));
        if (k > 0) c.meta.bowls.forEach((b, i) => fx.flow(c, [c.meta.door, [(c.meta.door[0] + b[0]) / 2, c.meta.door[1] - 120], b], 0.45, { n: 10, col: '232,196,110', k: k * ease(prog(c.t, 1 + i * 0.3, 2 + i * 0.3)), size: 3.5, seed: 50 + i, speed: 0.25 })); } }],
      caps: [
        chap('七', '福利之源', 0.6, 15.6),
        { t0: 1.4, t1: 8.4, style: 'quote', text: '原始教會素為共產主義之首，*福利體系之源*，\n趙宋救荒賑災，僧居其七，官府儻乎其後。', src: SJ, pos: 'top', y: 280 },
        { t0: 9, t1: 15.6, style: 'quote', text: '新教興，教產沒，貧民無所得食，\n*流為盜寇佣兵者眾*', src: SJ, pos: 'top', y: 290, opt: { size: 56 } },
      ] },
    { id: 's8_statue', dur: 15, trans: TR, grade: { sat: 0.9 },
      cam: t => keys([[0, { x: W * 0.36, y: H * 0.54, z: 1.14 }], [15, { x: W * 0.62, y: H * 0.58, z: 1.14 }]], t, lin),
      sprites: (t, c) => { const [sx, sy] = c.meta.sapling, [cx, cy] = c.meta.circle, k = ease(prog(t, 8, 14));
        return [{ name: t < 5.5 ? 'sap_0' : 'sap_1', x: sx, y: sy, d: 0.45 },
          { name: `leaver_${Math.floor(t * 3) % 4}`, x: cx + 300 + k * 420, y: cy + 60, d: 0.45, scale: 0.8, alpha: 1 - 0.85 * k }]; },
      fx: [{ draw: c => fx.glowAt(c, c.meta.lamp, 0.45, 300, '255,214,140', 0.45) }],
      caps: [
        chap('八', '大與小', 0.6, 14.6),
        { t0: 1.4, t1: 7.6, style: 'quote', text: '國家是大共同體，*大共同體無法用政策手段把小共同體扶起來*，\n就像是國家沒有辦法用補貼消滅掉私營企業一樣', src: '《劉仲敬訪談 029 論小共同體》', pos: 'top', y: 260, opt: { size: 42, max: 1800 } },
        { t0: 8, t1: 14.6, style: 'quote', text: '部落巫師的詛咒和教會的破門都能在生物學意義上致命，\n因為切斷社會關系的人和*得不到愛撫的嬰兒*一樣非死不可', src: WX, pos: 'top', y: 260, opt: { size: 42, max: 1800 } },
      ] },
    { id: 's9_summer', dur: 15, trans: TR, grade: { warm: 0.2, sat: 1.05 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.36, z: 1.3 }], [5, { x: W * 0.5, y: H * 0.38, z: 1.26 }], [15, { x: W * 0.5, y: H * 0.56, z: 1.04 }]], t, ease),
      layers: { roots: t => ({ grow: lerp(-0.02, 1.05, ease(prog(t, 5, 14))), soft: 0.05 }) },
      fx: [{ draw: c => fx.petals(c, { n: 30, wind: 60, k: 1 - prog(c.t, 6, 9) }) }],
      caps: [
        chap('九', '花朵之下', 0.6, 14.6),
        { t0: 1.4, t1: 7.4, style: 'quote', text: '教會反而顯得像是古舊過時的、行將滅亡的、應該被淘汰的東西。\n其實它不是，它只是*隱退在了花朵和枝葉之下*而已', src: YD, pos: 'bottom', y: 1000, opt: { size: 44, max: 1800 }, color: 'paper' },
        { t0: 8, t1: 14.6, style: 'quote', text: '聰明的士大夫即使個人缺乏宗教意義的靈性，也會像休謨和孔子一樣維護教會\n（也就是維護*文明大樹的地下部分*）。', src: '劉仲敬人人網言論', pos: 'bottom', y: 1000, opt: { size: 40, max: 1850 }, color: 'paper' },
      ] },
    { id: 's10_candle', dur: 13, trans: TR, grade: { warm: 0.25 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.4, z: 1.14 }], [13, { x: W * 0.5, y: H * 0.56, z: 1.06 }]], t, lin),
      layers: { wax: t => ({ grow: lerp(-0.02, 0.72, easeIn(prog(t, 0.5, 12.5))), conceal: true, soft: 0.01 }) },
      fx: [{ after: 'wax', draw: c => { const g = lerp(-0.02, 0.72, easeIn(prog(c.t, 0.5, 12.5))), y = lerp(c.meta.top, c.meta.bot, Math.max(0, g));
        const big = 1 + 1.4 * Math.sin(Math.PI * clamp(c.t / 9));   // 火焰在中段最旺：釋放
        fx.flame(c, [c.meta.cx, y - 6], 0.4, { size: big }); fx.motes(c, [c.meta.cx, y - 60], 0.4, { n: 50, k: 0.5 * big }); } }],
      caps: [
        chap('十', '釋放', 0.6, 12.6, { color: 'paper' }),
        { t0: 1.4, t1: 7, style: 'quote', text: '虔誠信仰給歐洲帶來的巨大能量，大概是在文藝復興之前的某個時期達到頂峰，\n而文藝復興就屬於*釋放階段*了。', src: YD, color: 'paper', pos: 'bottom', y: 1010, opt: { size: 40, max: 1850 } },
        { t0: 7.4, t1: 12.6, style: 'quote', text: '一切秩序都是*德性的展開或消耗*，在窮盡其內在可能性以後滅亡。', src: WX, color: 'paper', pos: 'bottom', y: 1020, opt: { size: 46 } },
      ] },
    { id: 's11_moon', dur: 11, trans: TR, grade: { expo: 1.0 },
      cam: t => keys([[0, { x: W * 0.55, y: H * 0.46, z: 1.12 }], [11, { x: W * 0.5, y: H * 0.52, z: 1.04 }]], t, lin),
      fx: [{ draw: c => { fx.stars(c, { n: 120, k: 0.6 }); fx.glowAt(c, c.meta.moon, 0.05, 520, '220,226,255', 0.35); fx.lamps(c, c.meta.wins, 0.35, { t0: 0, t1: 3 }); } }],
      caps: [
        chap('十一', '反射的光', 0.6, 10.6, { color: 'paper' }),
        { t0: 1.4, t1: 10.6, style: 'quote', text: '這些資源就像*月亮反射太陽的光線*一樣，\n它們的力量實際上都是來自基督教的', src: YD, color: 'paper', pos: 'top', y: 560, opt: { size: 50 } },
      ] },
    { id: 's12_match', dur: 15, trans: TR, grade: { warm: -0.05 },
      cam: t => keys([[0, { x: 1100, y: H * 0.56, z: 1.12 }], [15, { x: 1550, y: H * 0.56, z: 1.12 }]], t, lin),
      sprites: (t, c) => { const [hx] = c.meta.hall, k = ease(prog(t, 8.5, 14.5)), walk = t > 8.5 && k < 1;
        return [{ name: walk ? `girl_${1 + Math.floor(t * 3) % 3}` : 'girl_0', x: lerp(1150, hx - 60, k), y: c.meta.street_y, d: 0.4, alpha: 1 - ease(prog(t, 13.8, 14.6)) }]; },
      fx: [{ draw: c => { fx.snow(c, { n: 260, wind: 30 }); const k = ease(prog(c.t, 8.5, 14.5));
        if (c.t < 8.5) [1, 3.6, 6.2].forEach(td => { const e = c.t - td; if (e > 0 && e < 1.8) fx.glowAt(c, [1185, c.meta.street_y - 110], 0.4, 160, '255,190,100', 0.7 * (1 - e / 1.8)); });
        fx.lamps(c, c.meta.wins, 0.4, { t0: 7.5, t1: 9.5, k: 1.3 }); } }],
      caps: [
        chap('十二', '教會真空', 0.6, 14.6, { color: 'paper' }),
        { t0: 1.4, t1: 8, style: 'quote', text: '像安徒生描繪的賣火柴的小女孩那種事情，其實就是城市化和工業化的過程中間\n傳統的教區跟不上、城市出現了*教會真空*的結果。', src: '《劉仲敬訪談 022 論委內瑞拉的歷史與憲制》', color: 'paper', pos: 'top', y: 240, opt: { size: 40, max: 1850 } },
        { t0: 8.4, t1: 14.6, style: 'quote', text: '無神論教會所占領的生態位，\n*恰好就是基督教會拋棄的*。', src: WX, color: 'paper', pos: 'top', y: 250, opt: { size: 54 } },
      ] },
    { id: 's13_winter', dur: 19, grade: t => ({ warm: 0.25, expo: lerp(1.0, 0.92, prog(t, 10, 18)) }),
      cam: t => keys([[0, { x: 1150, y: H * 0.7, z: 1.25 }], [6, { x: 1200, y: H * 0.66, z: 1.2 }], [19, { x: 1350, y: H * 0.5, z: 1.06 }]], t, ease),
      fx: [{ draw: c => { fx.snow(c, { n: 200, wind: 20, k: 1 - 0.5 * prog(c.t, 10, 16) });
        c.meta.seeds.forEach((p, i) => fx.glowAt(c, p, 0.5, 60, '255,210,130', 0.4 * ease(prog(c.t, 1 + i * 0.2, 2 + i * 0.2)) * (0.7 + 0.3 * Math.sin(c.t * 2 + i))));
        fx.lamps(c, c.meta.wins, 0.4, { t0: 9, t1: 14 });
        [10, 12, 14].forEach(td => { const e = c.t - td; if (e > 0 && e < 2) fx.glowAt(c, c.meta.bell, 0.4, 200 + e * 300, '255,236,200', 0.35 * (1 - e / 2)); }); } }],
      caps: [
        chap('十三', '嚴冬', 0.6, 16.4),
        { t0: 1.4, t1: 8.4, style: 'quote', text: '當嚴冬來臨的時候人們就會發現，跟初期的情況一樣，\n又是*只有種子能夠存活下來*，負責保護文明基因。', src: YD, pos: 'top', y: 260, opt: { size: 46 } },
        { t0: 8.8, t1: 16.4, style: 'quote', text: '教會如果能夠*保護家庭和小區*，其他都是多余的，\n如果不能保護家庭和小區，要教會何用。', src: TW, pos: 'top', y: 260, opt: { size: 46 } },
        { t0: 16.6, t1: 19, style: 'sub', text: '劉仲敬思想 · 其十一《霉菌》', pos: 'center', wash: false },
      ] },
  ],
};
