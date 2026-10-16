// 第十部《胡蘿蔔》— 反勵志的人生建議
import { keys, ease, easeOut, easeIn, prog, clamp, lerp, hash } from '../lib/engine.js';
import * as fx from '../lib/fx.js';

const W = 2304, H = 1296, TR = 2, lin = x => x;
const AY = '《阿姨，我不想努力了》', YD = '《文明更迭的源代碼》';
const chap = (num, text, t0, t1, o = {}) => ({ style: 'chapter', num, text, t0, t1, ...o });

export default {
  title: '胡蘿蔔',
  fadeIn: 1.5, fadeOut: 2.5,
  scenes: [
    { id: 's1_birth', dur: 15, trans: TR, grade: { warm: 0.25 },
      cam: t => keys([[0, { x: 1000, y: H * 0.56, z: 1.12 }], [15, { x: 1700, y: H * 0.56, z: 1.12 }]], t, lin),
      sprites: (t, c) => [{ name: 'basket', x: 600 + t * 85, y: c.meta.river_y + Math.sin(t * 1.6) * 8, rot: Math.sin(t * 1.2) * 0.06, d: 0.45, after: 'mid' }],
      caps: [
        { t0: 1.4, t1: 6.6, style: 'title', text: '胡蘿蔔', pos: 'center', y: 400 },
        { t0: 2.5, t1: 6.6, style: 'sub', text: '劉仲敬思想 · 水彩短片 其十 —— 那些勵志書不會告訴你的', pos: 'center', y: 540, wash: false },
        chap('一', '養生祕訣', 7, 14.6),
        { t0: 7.4, t1: 14.6, style: 'quote', text: '唯一可靠的養生祕訣就是要*善於投胎*。', src: AY, pos: 'top', y: 300, opt: { size: 64 } },
      ] },
    { id: 's2_drop', dur: 16, trans: TR, grade: { expo: 1.02 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.6, z: 1.12 }], [16, { x: W * 0.5, y: H * 0.62, z: 1.2 }]], t, lin),
      fx: [{ after: 'bowl', draw: c => {
        const v = c.view(0.4), [bx, by] = c.meta.bowl;
        [2, 5.5, 8.4, 10.6, 12.4, 13.8, 14.8].forEach((td, i) => {
          const e = c.t - td, fall = 0.8;
          if (e > -fall && e < 0) { const [x, y] = v.P(bx, lerp(-100, by, (e + fall) / fall)); fx.glow(c.a, x, y, 26, '255,240,200', 0.9); }
          if (e >= 0 && e < 3) { const [x, y] = v.P(bx, by); const k = (1 - e / (2.2 - i * 0.2)) ; if (k > 0) {
            fx.glow(c.a, x, y, (300 + i * 60) * v.s, '255,226,160', 0.7 * k * k);
            c.n.strokeStyle = `rgba(255,230,180,${0.6 * k})`; c.n.lineWidth = 2; c.n.beginPath(); c.n.ellipse(x, y, e * 300 * v.s, e * 64 * v.s, 0, 0, Math.PI * 2); c.n.stroke(); } }
        });
      } }],
      caps: [
        chap('二', '快樂是什麼', 0.6, 15.6, { color: 'paper' }),
        { t0: 1.4, t1: 7.6, style: 'quote', text: '快樂就是*嗎啡類物質*在大腦裏面分泌出來的時候，它注定是*非常短暫*的。', src: AY, color: 'paper', pos: 'top', y: 290, opt: { size: 50 } },
        { t0: 8, t1: 15.6, style: 'quote', text: '如果你經常快樂或者不斷快樂的話，那實際上效果跟吸毒是差不多的，\n大腦的*閾值會越來越高*。', src: AY, color: 'paper', pos: 'top', y: 280, opt: { size: 48 } },
      ] },
    { id: 's3_donkey', dur: 17, trans: TR, grade: { warm: 0.15 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.6, z: 1.18 }], [17, { x: W * 0.5, y: H * 0.56, z: 1.06 }]], t, lin),
      sprites: (t, c) => {
        const [cx, cy] = c.meta.center, [rx, ry] = c.meta.ring, a = t * 0.42;
        const x = cx + Math.cos(a) * rx, y = cy + 60 + Math.sin(a) * ry;
        const ca = a + 0.32, carx = cx + Math.cos(ca) * (rx + 40), cary = cy + Math.sin(ca) * (ry + 10) - 220;
        const back = Math.sin(a) < 0;
        const don = { name: `donkey_${Math.floor(t * 4) % 4}`, x, y, d: 0.45, scale: 0.8 + 0.2 * Math.sin(a), flip: Math.cos(a + Math.PI / 2) < 0, after: back ? 'mid' : undefined };
        const car = { name: 'carrot', x: carx, y: cary, d: 0.45, rot: Math.sin(t * 3) * 0.15, scale: 0.8 + 0.2 * Math.sin(a), after: back ? 'mid' : undefined };
        return [don, car];
      },
      caps: [
        chap('三', '拉磨的驢子', 0.6, 16.6),
        { t0: 1.4, t1: 7.4, style: 'quote', text: '快樂基本上起的作用都相當於\n給*拉磨的驢子*前面放一個*胡蘿蔔*。', src: AY, pos: 'top', y: 280, opt: { size: 58 } },
        { t0: 7.8, t1: 16.6, style: 'quote', text: '背後都是意味著後面有一個*非常艱難而複雜的任務*要你去完成，\n所以才會用這個東西來做胡蘿蔔，引誘驢子前進。', src: AY, pos: 'top', y: 280, opt: { size: 46, max: 1800 } },
      ] },
    { id: 's4_caliph', dur: 15, trans: TR, grade: { expo: 1.02 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.45, z: 1.1 }], [15, { x: W * 0.5, y: H * 0.52, z: 1.18 }]], t, lin),
      fx: [{ after: 'palace', draw: c => { const v = c.view(0); c.meta.lamps.forEach((p, i) => { const [x, y] = v.P(p[0], p[1]);
        if (i < 14) { const k = ease(prog(c.t, 3 + i * 0.35, 3.6 + i * 0.35)); fx.glow(c.a, x, y, 60, '255,210,130', 0.6 * k); c.n.fillStyle = `rgba(255,230,160,${0.9 * k})`; }
        else c.n.fillStyle = 'rgba(70,66,80,0.6)';
        c.n.beginPath(); c.n.arc(x, y, 5, 0, Math.PI * 2); c.n.fill(); }); } }],
      caps: [
        chap('四', '十四天', 0.6, 14.6, { color: 'paper' }),
        { t0: 1.4, t1: 7.6, style: 'quote', text: '阿卜杜勒．拉赫曼說，他做哈里發做了幾十年，\n總共只有*十四天*的快樂時間。', src: AY, color: 'paper', pos: 'bottom', y: 1010 },
        { t0: 8, t1: 14.6, style: 'quote', text: '快樂只是一種*星星點點*的東西，而且它的背後隱藏著極大的危險。\n以追求快樂為目的的人生是*凶多吉少*的。', src: AY, color: 'paper', pos: 'bottom', y: 1000, opt: { size: 46, max: 1800 } },
      ] },
    { id: 's5_chase', dur: 16, trans: TR, grade: { warm: 0.15 },
      cam: t => keys([[0, { x: 1100, y: H * 0.54, z: 1.12 }], [16, { x: 1800, y: H * 0.56, z: 1.12 }]], t, lin),
      sprites: (t, c) => {
        const rx = 500 + t * 95, ry = c.meta.path_y;
        const k = ease(prog(t, 9, 14)), [ox, oy] = c.meta.rower;
        const bx = lerp(rx + 260 + Math.sin(t * 2.3) * 80, ox + 40, k), by = lerp(ry - 260 + Math.sin(t * 3.1) * 60, oy, k);
        return [{ name: `runner_${Math.floor(t * 3.2) % 4}`, x: Math.min(rx, 1700), y: ry, d: 0.45, scale: 0.8, after: 'mid' },
          { name: `bfly_${t > 14 ? 1 : Math.floor(t * 8) % 3}`, x: bx, y: by, d: 0.45, scale: 0.7 }];
      },
      caps: [
        chap('五', '追求幸福的人', 0.6, 15.6),
        { t0: 1.4, t1: 7, style: 'quote', text: '*追求幸福的人從來都得不到幸福*，差不多這是一條很固定的真理吧。', src: AY, pos: 'top', y: 300 },
        { t0: 7.4, t1: 15.6, style: 'quote', text: '多半是在時過境遷的時候才突然想起來，\n在那一段時間*你其實是幸福的*。', src: AY, pos: 'top', y: 290 },
      ] },
    { id: 's6_cushion', dur: 14, trans: TR, grade: { warm: 0.2 },
      cam: t => keys([[0, { x: W * 0.46, y: H * 0.6, z: 1.18 }], [14, { x: W * 0.55, y: H * 0.54, z: 1.06 }]], t, lin),
      caps: [
        chap('六', '軟綿綿的生活', 0.6, 13.6),
        { t0: 1.4, t1: 13.4, style: 'quote', text: '如果你一開始就把追求幸福設定為自己的目的的話，\n那你幾乎不可避免的要*降低標準*，走向一種*軟綿綿的生活*。', src: AY, pos: 'top', y: 280, opt: { size: 48 } },
        { t0: 6, t1: 13, style: 'note', text: '設定目的的人，便被人牽著走', x: 1660, y: 900, opt: { size: 34 } },
      ] },
    { id: 's7_mask', dur: 16, trans: TR, grade: { warm: 0.15 },
      cam: t => keys([[0, { x: W * 0.4, y: H * 0.52, z: 1.14 }], [16, { x: W * 0.6, y: H * 0.56, z: 1.14 }]], t, lin),
      fx: [{ after: 'fig', draw: c => { const v = c.view(0.4);
        c.meta.holes.forEach((h, i) => { const k = ease(prog(c.t, 9 + i * 0.6, 10 + i * 0.6)); if (k <= 0) return; const dir = h[0] > W * 0.72 ? 1 : -1;
          for (let j = 0; j < 14; j++) { const ph = (c.t * 1.8 + j / 14) % 1; const [x, y] = v.P(h[0] + dir * ph * 140, h[1] + ph * ph * 200);
            c.n.fillStyle = `rgba(110,160,210,${0.7 * k * (1 - ph)})`; c.n.beginPath(); c.n.arc(x, y, 5, 0, Math.PI * 2); c.n.fill(); } }); } }],
      caps: [
        chap('七', '偽裝的成本', 0.6, 15.6),
        { t0: 1.4, t1: 6, style: 'quote', text: '偽裝是件*成本很高*的事情，只能維持極短的時間。', src: AY, pos: 'top', y: 300 },
        { t0: 6.4, t1: 11, style: 'quote', text: '你要給別人造成某種印象，最好的辦法就是，\n你要讓自己*真正變成那種人*。', src: AY, pos: 'top', y: 290 },
        { t0: 11.4, t1: 15.6, style: 'quote', text: '你在這一個點上獲得收益，在其他地方會以其他方式*漏出去*的。', src: AY, pos: 'top', y: 300 },
      ] },
    { id: 's8_captain', dur: 15, trans: TR, grade: { sat: 0.85, warm: -0.1 },
      cam: t => keys([[0, { x: 1400, y: H * 0.5, z: 1.2 }], [15, { x: 1400, y: H * 0.54, z: 1.08 }]], t, lin),
      fx: [{ draw: c => { fx.rain(c, { n: 380, angle: 0.35 }); fx.flash(c, 4.5, { k: 0.5 }); fx.flash(c, 10.2, { k: 0.4 }); } }],
      caps: [
        chap('八', '身體上的船長', 0.6, 14.6),
        { t0: 1.4, t1: 7.4, style: 'quote', text: '變成一個*抽象的身體上面的船長*了，\n而且這個船長還有很多競爭者。', src: AY, pos: 'top', y: 280 },
        { t0: 7.8, t1: 14.6, style: 'quote', text: '你想得越多做得越少，*事情就越糟糕*。', src: AY, pos: 'top', y: 300, opt: { size: 64 } },
      ] },
    { id: 's9_swim', dur: 15, trans: TR, grade: { warm: 0.1 },
      cam: t => keys([[0, { x: W * 0.42, y: H * 0.56, z: 1.14 }], [15, { x: W * 0.55, y: H * 0.6, z: 1.12 }]], t, lin),
      sprites: (t, c) => { const [ex, ey] = c.meta.edge, [wx, wy] = c.meta.water;
        if (t < 3.2) return [{ name: 'diver_0', x: ex - 80, y: ey + 4, d: 0.4, after: 'lake' }];
        if (t < 4.2) return [{ name: 'diver_1', x: ex - 70, y: ey + 4, d: 0.4, after: 'lake' }];
        const k = prog(t, 4.2, 5.6); if (k >= 1) return [];
        return [{ name: 'diver_2', x: lerp(ex - 40, wx, k), y: lerp(ey, wy, k) - Math.sin(k * Math.PI) * 220, rot: k * 2.2, d: 0.4, after: 'lake' }]; },
      fx: [{ after: 'lake', draw: c => { fx.ripple(c, c.meta.water, 0.4, 5.6, { col: '255,255,255' });
        if (c.t > 5.6 && c.t < 7) { const v = c.view(0.4), [x, y] = v.P(...c.meta.water); for (let i = 0; i < 20; i++) { const e = c.t - 5.6, a = -Math.PI * (0.1 + 0.8 * hash(i, 4));
          c.n.fillStyle = `rgba(230,245,255,${0.8 * (1 - e / 1.4)})`; c.n.beginPath(); c.n.arc(x + Math.cos(a) * e * 240, y + Math.sin(a) * e * 300 + e * e * 300, 5, 0, Math.PI * 2); c.n.fill(); } } } }],
      caps: [
        chap('九', '先下水', 0.6, 14.6),
        { t0: 1.4, t1: 7.4, style: 'quote', text: '要游泳，你總得要*下水游一游*，\n然後根據相應的回饋才能確定自己的信心。', src: AY, pos: 'top', y: 290 },
        { t0: 7.8, t1: 14.6, style: 'quote', text: '不是你的知識引導了行動，\n而是*行動給你帶來了知識*。', src: AY, pos: 'top', y: 290, opt: { size: 60 } },
      ] },
    { id: 's10_cocoon', dur: 15, trans: TR, grade: { warm: 0.2 },
      cam: t => keys([[0, { x: W * 0.46, y: H * 0.44, z: 1.3 }], [15, { x: W * 0.55, y: H * 0.46, z: 1.08 }]], t, lin),
      layers: { cocoon: t => (t > 6 ? { hide: true } : { dx: Math.sin(t * 3) * 6 * prog(t, 3, 6) }), broken: t => (t < 6 ? { hide: true } : {}) },
      sprites: (t, c) => { if (t < 6) return []; const [cx, cy] = c.meta.cocoon, k = ease(prog(t, 8.5, 14));
        return [{ name: `bfly_${t < 8 ? 0 : Math.floor(t * 7) % 3}`, x: cx + k * 700 + Math.sin(t * 2) * 40 * k, y: cy + 40 - k * 420, d: 0.4, scale: 0.6 + 0.6 * ease(prog(t, 6, 8.5)), alpha: ease(prog(t, 6, 6.6)) }]; },
      caps: [
        chap('十', '毛毛蟲出殼', 0.6, 14.6),
        { t0: 1.4, t1: 14.6, style: 'quote', text: '定一個毛毛蟲必須像蝴蝶一樣的標準，要不然就不能讓它出殼，\n那樣的話它就*永遠出不了殼*了。', src: AY, pos: 'bottom', y: 990, opt: { size: 48 } },
      ] },
    { id: 's11_gardener', dur: 16, trans: TR, grade: t => ({ warm: 0.25 * Math.sin(t / 16 * Math.PI * 2), sat: 1 + 0.08 * Math.sin(t / 8 * Math.PI) }),
      cam: t => keys([[0, { x: 1200, y: H * 0.54, z: 1.12 }], [16, { x: 1600, y: H * 0.56, z: 1.14 }]], t, lin),
      sprites: (t, c) => { const cyc = (t * 0.5) % 1; return [{ name: `digger_${cyc < 0.35 ? 0 : cyc < 0.7 ? 1 : 2}`, x: c.meta.dig[0], y: c.meta.dig[1], d: 0.45, scale: 1.0, after: 'mid' }]; },
      fx: [{ draw: c => { if (c.t > 10) fx.snow(c, { n: 120, k: ease(prog(c.t, 10, 12)) }); else if (c.t > 4 && c.t < 9) fx.petals(c, { n: 40, cols: ['230,140,60', '210,100,50'], wind: 90, size: 1.2 }); } }],
      caps: [
        chap('十一', '給身體一個出口', 0.6, 15.6),
        { t0: 1.4, t1: 7.4, style: 'quote', text: '人類痛苦的絕大部分原因\n就是因為*缺乏體力活動*。', src: AY, pos: 'top', y: 290, opt: { size: 60 } },
        { t0: 7.8, t1: 15.6, style: 'quote', text: '把這個出口給封住了以後，\n壓力會在其他的出口以*扭曲的方式*體現出來', src: AY, pos: 'top', y: 290 },
      ] },
    { id: 's12_ridge', dur: 19, grade: t => ({ warm: 0.35, expo: lerp(1.0, 0.9, prog(t, 6, 18)) }),
      cam: t => keys([[0, { x: 1300, y: H * 0.5, z: 1.12 }], [19, { x: 1900, y: H * 0.5, z: 1.08 }]], t, lin),
      sprites: (t, c) => { const R = c.meta.ridge, u = clamp(0.22 + t / 19 * 0.5) * (R.length - 1), i = Math.floor(u), f = u - i;
        const [x0, y0] = R[i], [x1, y1] = R[Math.min(i + 1, R.length - 1)];
        return [{ name: `walker_${Math.floor(t * 2.6) % 4}`, x: lerp(x0, x1, f), y: lerp(y0, y1, f) + 8, d: 0.45, scale: 0.7 }]; },
      caps: [
        chap('十二', '決斷時刻', 0.6, 16.2),
        { t0: 1.4, t1: 8, style: 'quote', text: '我之所以要給讀者提供認知訓練，\n就是為了讓他們在即將來臨的*決斷時刻*正確判斷形勢。', src: '《經與史 · 跋》', pos: 'top', y: 280 },
        { t0: 8.4, t1: 16.2, style: 'quote', text: '歷史的可能性並不等於*你自身的可能性*，因為你是從自己的角度出發，\n你這個角色的路徑在三十歲以後就已經基本被鎖定', src: YD, pos: 'top', y: 280, opt: { size: 44, max: 1850 } },
        { t0: 16.4, t1: 19, style: 'sub', text: '劉仲敬思想 · 其十《胡蘿蔔》', pos: 'center', wash: false },
      ] },
  ],
};
