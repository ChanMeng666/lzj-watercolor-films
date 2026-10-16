// 第十二部《梯子》— 博雅教育：先訓練，後問為什麼
import { keys, ease, easeOut, easeIn, prog, clamp, lerp, hash } from '../lib/engine.js';
import * as fx from '../lib/fx.js';

const W = 2304, H = 1296, TR = 2, lin = x => x;
const BA = '《經與史 · 跋》', XU = '《經與史 · 序言》', AY = '《阿姨，我不想努力了》', YD = '《文明更迭的源代碼》';
const chap = (num, text, t0, t1, o = {}) => ({ style: 'chapter', num, text, t0, t1, ...o });

// 沿折線畫一條逐漸亮起的金線
function goldPath(c, pts, d, t0, t1, { w = 5, rgb = '255,214,120' } = {}) {
  const k = clamp((c.t - t0) / (t1 - t0)); if (k <= 0) return;
  const v = c.view(d), P = pts.map(p => v.P(p[0], p[1]));
  const seg = []; let L = 0; for (let i = 1; i < P.length; i++) { const l = Math.hypot(P[i][0] - P[i - 1][0], P[i][1] - P[i - 1][1]); seg.push(l); L += l; }
  let rem = L * ease(k); c.a.strokeStyle = `rgba(${rgb},0.85)`; c.a.lineWidth = w * v.s; c.a.lineCap = 'round';
  c.a.beginPath(); c.a.moveTo(...P[0]);
  for (let i = 1; i < P.length && rem > 0; i++) { const f = Math.min(1, rem / seg[i - 1]); c.a.lineTo(lerp(P[i - 1][0], P[i][0], f), lerp(P[i - 1][1], P[i][1], f)); rem -= seg[i - 1]; }
  c.a.stroke();
}
function label(c, d, x, y, text, a, { size = 34, col = '60,40,30' } = {}) {
  if (a <= 0) return; const v = c.view(d), [X, Y] = v.P(x, y);
  c.n.font = `${size * v.s}px Kai`; c.n.textAlign = 'center'; c.n.fillStyle = `rgba(${col},${a})`; c.n.fillText(text, X, Y);
}

export default {
  title: '梯子',
  fadeIn: 1.5, fadeOut: 2.5,
  scenes: [
    { id: 's1_copy', dur: 18, trans: TR, grade: { warm: 0.2 },
      cam: t => keys([[0, { x: W * 0.63, y: H * 0.42, z: 1.5 }], [5.5, { x: W * 0.63, y: H * 0.42, z: 1.45 }], [12, { x: W * 0.52, y: H * 0.5, z: 1.08 }], [18, { x: W * 0.58, y: H * 0.47, z: 1.14 }]], t, ease),
      layers: { char: t => ({ grow: lerp(-0.02, 1.04, prog(t, 6.2, 14)), soft: 0.03 }) },
      caps: [
        { t0: 1.2, t1: 6, style: 'title', text: '梯子', pos: 'center', y: 400 },
        { t0: 2.2, t1: 6, style: 'sub', text: '劉仲敬思想 · 水彩短片 其十二 —— 先訓練，後問為什麼', pos: 'center', y: 540, wash: false },
        chap('一', '先掌握', 6.4, 17.6),
        { t0: 6.6, t1: 12, style: 'quote', text: '智力訓練必需首先掌握，然後才能問為什麼。\n事先就問為什麼，你就*永遠進不了布局*。', src: BA, pos: 'bottom', y: 990, opt: { size: 50 } },
        { t0: 12.4, t1: 17.6, style: 'quote', text: '我自己不知道也不在乎有什麼用處，\n無非是*搜集大偵探波洛全部作品*同類的事情。', src: '《劉仲敬文選 · 第四卷》', pos: 'bottom', y: 990, opt: { size: 50 } },
      ] },
    { id: 's2_board', dur: 15, trans: TR, grade: { warm: 0.1 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.52, z: 1.25 }], [15, { x: W * 0.5, y: H * 0.52, z: 1.05 }]], t, lin),
      layers: { stones: t => ({ alpha: lerp(1, 0.12, ease(prog(t, 6, 11))) }) },
      fx: [{ after: 'stones', draw: c => c.meta.frame.forEach((p, i) => goldPath(c, p, 0.4, 5 + i * 0.8, 8 + i * 0.8, { w: 7 })) }],
      caps: [
        chap('二', '格局感', 0.6, 14.6, { color: 'paper' }),
        { t0: 1.4, t1: 14.6, style: 'quote', text: '歷史分析和布局分析都是必需的智力訓練，通過摸索培養格局感。\n*格局感確定後，材料就會變得毫無關系*。', src: BA, color: 'paper', pos: 'bottom', y: 1000, opt: { size: 46, max: 1800 } },
      ] },
    { id: 's3_nav', dur: 15, trans: TR, grade: { sat: 0.9 },
      cam: t => keys([[0, { x: W * 0.42, y: H * 0.55, z: 1.15 }], [15, { x: W * 0.58, y: H * 0.45, z: 1.08 }]], t, lin),
      fx: [{ draw: c => {
        fx.lamps(c, c.meta.side, 0, { t0: 0.5, t1: 5, off: [5.5, 7.5], warm: '200,210,235', k: 0.6, seed: 5 });
        goldPath(c, c.meta.route, 0, 7, 12.5, { w: 6 });
        fx.lamps(c, c.meta.route, 0, { t0: 7, t1: 12.5, order: (i, n) => i / n, k: 1.1 });
      } }],
      caps: [
        chap('三', '導航系統', 0.6, 14.6),
        { t0: 1.4, t1: 7, style: 'quote', text: '*博雅教育是唯一真正的教育*，大學的本意就是指的博雅教育。', src: AY, pos: 'top', y: 300 },
        { t0: 7.4, t1: 14.6, style: 'quote', text: '博雅教育是做什麼的？就是把各種複雜的、多層次的子系統\n*連綴節點*植入你的腦海', src: YD, pos: 'top', y: 290 },
      ] },
    { id: 's4_desks', dur: 16, trans: TR, grade: { sat: 0.8, warm: -0.05 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.62, z: 1.06 }], [16, { x: W * 0.5, y: H * 0.5, z: 1.3 }]], t, lin),
      fx: [{ draw: c => { const v = c.view(0.4), [x, y] = v.P(...c.meta.lamp), fl = 0.9 + 0.1 * Math.sin(c.t * 7);
        fx.glow(c.a, x, y, 700 * v.s, '255,220,150', 0.45 * fl); fx.glow(c.a, x, y + 30 * v.s, 120 * v.s, '255,240,200', 0.7); } }],
      caps: [
        chap('四', '做題家', 0.6, 15.6, { color: 'paper' }),
        { t0: 1.4, t1: 7.6, style: 'quote', text: '至於那些頭懸樑錐刺股的科舉文人，老實說，\n他們根本就是*無產階級當中耐力比較強的一類*。', src: AY, color: 'paper', pos: 'bottom', y: 1000, opt: { size: 48 } },
        { t0: 8, t1: 15.6, style: 'quote', text: '而華人做題家，想象自己像范進那樣考試進去，然後拿著一個好學歷去掙錢的人，\n那只是大學在資產階級時代和平民時代擴大以後的*附帶功能*。', src: '《劉仲敬論海內外費拉華人》', color: 'paper', pos: 'bottom', y: 1000, opt: { size: 42, max: 1850 } },
      ] },
    { id: 's5_tacit', dur: 14, trans: TR, grade: { warm: 0.1 },
      cam: t => keys([[0, { x: W * 0.36, y: H * 0.56, z: 1.2 }], [14, { x: W * 0.64, y: H * 0.56, z: 1.2 }]], t, lin),
      fx: [{ after: 'shop', draw: c => {
        c.meta.tags.forEach((p, i) => label(c, 0.4, p[0], p[1] + 20, '95', ease(prog(c.t, 2.5 + i * 0.6, 3.2 + i * 0.6)), { size: 60, col: '170,40,34' }));
        const v = c.view(0.4), [x, y] = v.P(...c.meta.crack); fx.glow(c.a, x, y, 120 * v.s, '255,110,80', 0.5 * ease(prog(c.t, 7, 8.5)));
        const [hx, hy] = v.P(...c.meta.hand); fx.glow(c.a, hx, hy, 300 * v.s, '255,200,120', 0.35);
      } }],
      caps: [
        chap('五', '默會知識', 0.6, 13.6),
        { t0: 1.4, t1: 7, style: 'quote', text: '技術水平很多都是*默會知識*，\n它用政治考核方式或者做題家考試方式是*看不出來*的。', src: '《劉仲敬訪談 139》', pos: 'top', y: 280, opt: { size: 50 } },
        { t0: 7.4, t1: 13.6, style: 'quote', text: '讀幾十部柏拉圖註疏這種做法恰恰是專業教育，\n*是做題家的讀書風格*', src: YD, pos: 'top', y: 280, opt: { size: 50 } },
      ] },
    { id: 's6_seed', dur: 16, trans: TR, grade: { warm: 0.15 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.42, z: 1.5 }], [8, { x: W * 0.5, y: H * 0.48, z: 1.2 }], [16, { x: W * 0.5, y: H * 0.62, z: 1.12 }]], t, ease),
      layers: { forest: t => ({ grow: lerp(-0.02, 1.02, ease(prog(t, 1.2, 8))), soft: 0.08 }), weeds: t => ({ grow: lerp(-0.02, 1.05, ease(prog(t, 8.5, 14.5))), soft: 0.05 }) },
      fx: [{ draw: c => fx.motes(c, [W * 0.5, H * 0.42], 0.4, { n: 30, k: ease(prog(c.t, 2, 6)) }) }],
      caps: [
        chap('六', '種子', 0.6, 15.6),
        { t0: 1.4, t1: 8, style: 'quote', text: '這樣的著作像*一粒粒的種子*，包含了大量路徑積分，\n因此內在的組織豐富度非常大。', src: YD, pos: 'top', y: 200, opt: { size: 46 } },
        { t0: 8.4, t1: 15.6, style: 'quote', text: '路徑要在蕪雜中自己顯露，\n才有*野草一樣的力量*。', src: AY, pos: 'top', y: 220, opt: { size: 56 } },
      ] },
    { id: 's7_master', dur: 18, trans: TR, grade: { warm: 0.25 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.56, z: 1.2 }], [11, { x: W * 0.62, y: H * 0.56, z: 1.16 }], [18, { x: W * 0.9, y: H * 0.56, z: 1.12 }]], t, ease),
      fx: [{ after: 'mid', draw: c => { const v = c.view(0.45);
        c.meta.stones.forEach((p, i) => { const k = ease(prog(c.t, 1.5 + i * 1.1, 2 + i * 1.1)); if (k <= 0) return; const [x, y] = v.P(p[0], p[1]);
          c.n.fillStyle = i % 2 ? 'rgba(245,240,228,0.95)' : 'rgba(30,30,36,0.95)'; c.n.beginPath(); c.n.ellipse(x, y, 11 * v.s, 6 * v.s, 0, 0, Math.PI * 2); c.n.fill();
          fx.glow(c.a, x, y, 50 * v.s, '255,226,150', 0.5 * (1 - prog(c.t, 2 + i * 1.1, 3.5 + i * 1.1))); });
        const [px, py] = v.P(...c.meta.peers); fx.glow(c.a, px, py, 260 * v.s, '255,200,120', 0.3 * ease(prog(c.t, 10, 12))); } }],
      caps: [
        chap('七', '師父與同伴', 0.6, 17.6),
        { t0: 1.4, t1: 6.6, style: 'quote', text: '你在學習圍棋的時候，師父要教給你一大堆棋譜，\n就是古代和今天的名家下出的各種棋局。', src: AY, pos: 'top', y: 280, opt: { size: 48 } },
        { t0: 7, t1: 12.4, style: 'quote', text: '職業學校一般來說都是多餘的。實踐的那一部分，\n你可以在工作場所通過*師徒傳授和同伴互相切磋*的方式學', src: AY, pos: 'top', y: 280, opt: { size: 48 } },
        { t0: 12.8, t1: 17.6, style: 'quote', text: '技術員性質的知識都是*很快就會過時*的，你學完也沒什麼太大用處，\n以後隨時查閱技術資料就行了。', src: '《劉仲敬論移民海外的心理準備》', pos: 'top', y: 280, opt: { size: 46, max: 1800 } },
      ] },
    { id: 's8_delete', dur: 14, trans: TR, grade: { warm: 0.05 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.6, z: 1.15 }], [14, { x: W * 0.5, y: H * 0.5, z: 1.05 }]], t, lin),
      layers: { thicket: t => ({ grow: lerp(0, 0.82, ease(prog(t, 2, 11))), conceal: true, soft: 0.1 }) },
      fx: [{ draw: c => fx.godrays(c, 1150, -120, { k: 0.3 * ease(prog(c.t, 6, 11)) }) }],
      caps: [
        chap('八', '刪除', 0.6, 13.6),
        { t0: 1.4, t1: 13.6, style: 'quote', text: '認知的主要功能不是記憶，\n而是*選擇和刪除*。', src: BA, pos: 'top', y: 280, opt: { size: 64 } },
      ] },
    { id: 's9_maps', dur: 15, trans: TR, grade: { warm: 0.1 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.5, z: 1.12 }], [15, { x: W * 0.5, y: H * 0.46, z: 1.04 }]], t, lin),
      fx: [{ after: 'maps', draw: c => ['遊客的地圖', '大學的地圖', '軍事的地圖'].forEach((s, i) =>
        label(c, 0.4, c.meta.panels[i][0], c.meta.panels[i][1], s, ease(prog(c.t, 1.5 + i * 0.8, 2.2 + i * 0.8)), { size: 40, col: '250,240,220' })) }],
      caps: [
        chap('九', '地圖', 0.6, 14.6, { color: 'paper' }),
        { t0: 1.4, t1: 7, style: 'quote', text: '所有人都會畫地圖的，*那要看你的目的*。', src: AY, color: 'paper', pos: 'top', y: 130, opt: { size: 52 } },
        { t0: 7.4, t1: 14.6, style: 'quote', text: '一張地圖要畫得清晰，並不是畫面越擠越好，\n而是*格局越正確越好*。', src: BA, color: 'paper', pos: 'top', y: 120, opt: { size: 48 } },
      ] },
    { id: 's10_spider', dur: 18, trans: TR, grade: { sat: 0.9 },
      cam: t => keys([[0, { x: 1100, y: H * 0.5, z: 1.12 }], [18, { x: 1700, y: H * 0.55, z: 1.12 }]], t, lin),
      sprites: (t, c) => [{ name: `spider_${Math.floor(t * 9) % 3}`, x: 500 + t * 110 + Math.sin(t * 1.3) * 60, y: c.meta.water + 4, d: 0.3, scale: 1.1 }],
      fx: [{ draw: c => { const v = c.view(0.3);
        for (let j = 0; j < 6; j++) { const t0 = Math.floor(c.t / 0.6) * 0.6 - j * 0.6, e = c.t - t0; if (t0 < 0) continue;
          const sx = 500 + t0 * 110 + Math.sin(t0 * 1.3) * 60, [x, y] = v.P(sx, c.meta.water + 6);
          c.n.strokeStyle = `rgba(240,240,250,${0.5 * (1 - e / 3.6)})`; c.n.lineWidth = 1.5; c.n.beginPath(); c.n.ellipse(x, y, e * 60 * v.s, e * 9 * v.s, 0, 0, Math.PI * 2); c.n.stroke(); } } }],
      caps: [
        chap('十', '水蜘蛛', 0.6, 17.6),
        { t0: 1.4, t1: 6.6, style: 'quote', text: '文筆是視野、境界和洞察力的鏡子，\n*這些比材料重要得多*。', src: '《劉仲敬文選 · 第四卷》', pos: 'top', y: 200, opt: { size: 52 } },
        { t0: 7, t1: 12.2, style: 'quote', text: '凱恩斯把這種人稱為*輕盈的水蜘蛛*，\n憑藉靈巧輕薄的才智，劃過水面的薄膜。', src: '劉仲敬人物評論', pos: 'top', y: 200, opt: { size: 52 } },
        { t0: 12.6, t1: 17.6, style: 'quote', text: '你找不出結構，那你永遠超越不了\n*技術員和學術工*這個境界。', src: '《劉仲敬入門第二講 · 通古今之變》', pos: 'top', y: 200, opt: { size: 52 } },
      ] },
    { id: 's11_ladder', dur: 20, grade: t => ({ warm: 0.25, expo: lerp(1.0, 0.92, prog(t, 12, 20)) }),
      cam: t => keys([[0, { x: W * 0.5, y: H * 1.4, z: 1.05 }], [17, { x: W * 0.54, y: H * 0.5, z: 1.05 }], [20, { x: W * 0.54, y: H * 0.48, z: 1.02 }]], t, ease),
      fx: [{ draw: c => { const v = c.view(0.4), [x, y] = v.P(...c.meta.top2); fx.glow(c.a, x, y, 380 * v.s, '255,230,170', 0.55 * ease(prog(c.t, 9, 14))); } }],
      caps: [
        chap('十一', '梯子', 0.6, 16.2),
        { t0: 1.4, t1: 7.8, style: 'quote', text: '「經」是建構認知圖景的棟梁，\n也是*攀登神秘世界的梯子*。', src: XU, pos: 'top', y: 280, opt: { size: 58 } },
        { t0: 8.2, t1: 16.2, style: 'quote', text: '正如愛因斯坦的梯子能夠達到牛頓的梯子達不到的層次，\n同時並不妨礙你用他的梯子*繼續去牛頓的層次*。', src: XU, color: 'paper', pos: 'top', y: 280, opt: { size: 48 } },
        { t0: 16.6, t1: 20, style: 'sub', text: '劉仲敬思想 · 其十二《梯子》', pos: 'center', color: 'paper', wash: false },
      ] },
  ],
};
