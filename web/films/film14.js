// 第十四部《車站》— 格局、節點與決斷
import { keys, ease, easeOut, easeIn, prog, clamp, lerp, hash } from '../lib/engine.js';
import * as fx from '../lib/fx.js';

const W = 2304, H = 1296, TR = 2, lin = x => x;
const T2 = '《劉仲敬入門第二講 · 通古今之變》', V20 = '《劉仲敬訪談 020 再論土豪與游士》', V59 = '《劉仲敬訪談 059》';
const AY = '《阿姨，我不想努力了》', YD = '《文明更迭的源代碼》';
const chap = (num, text, t0, t1, o = {}) => ({ style: 'chapter', num, text, t0, t1, ...o });
const at = (pts, u) => { const f = clamp(u) * (pts.length - 1), i = Math.min(Math.floor(f), pts.length - 2), k = f - i;
  return [lerp(pts[i][0], pts[i + 1][0], k), lerp(pts[i][1], pts[i + 1][1], k)]; };

export default {
  title: '車站',
  fadeIn: 1.5, fadeOut: 2.5,
  scenes: [
    { id: 's1_valley', dur: 16, trans: TR, grade: { warm: 0.2 },
      cam: t => keys([[0, { x: 1100, y: H * 0.5, z: 1.1 }], [16, { x: 1700, y: H * 0.56, z: 1.16 }]], t, lin),
      fx: [{ draw: c => fx.godrays(c, 1500, -150, { k: 0.25, seed: 14 }) }],
      caps: [
        { t0: 1.4, t1: 6.6, style: 'title', text: '車站', pos: 'center', y: 400 },
        { t0: 2.5, t1: 6.6, style: 'sub', text: '劉仲敬思想 · 水彩短片 其十四 —— 格局、節點與決斷', pos: 'center', y: 540, wash: false },
        chap('一', '格局', 7, 15.6),
        { t0: 7.4, t1: 15.6, style: 'quote', text: '*路徑決定命運，格局決定路徑*，這兩件事情做到以後，\n然後其他的一些因素是輕如鴻毛。', src: T2, pos: 'top', y: 290 },
      ] },
    { id: 's2_rails', dur: 14, trans: TR, grade: { sat: 0.9 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.56, z: 1.1 }], [14, { x: W * 0.5, y: H * 0.6, z: 1.04 }]], t, lin),
      sprites: (t, c) => { const u = 1 - prog(t, 1, 13), p = at(c.meta.track, 0.05 + 0.9 * u);
        return [{ name: 'train', x: p[0], y: p[1], d: 0.45, scale: 0.18 + 1.0 * Math.pow(1 - u, 1.6), after: 'mid' }]; },
      fx: [{ draw: c => { const u = 1 - prog(c.t, 1, 13), p = at(c.meta.track, 0.05 + 0.9 * u), s = 0.18 + 1.0 * Math.pow(1 - u, 1.6);
        fx.smoke(c, [[p[0] - 40 * s, p[1] - 220 * s]], 0.45, { k: 0.7 }); } }],
      caps: [
        chap('二', '鐵軌', 0.6, 13.6),
        { t0: 1.4, t1: 13.4, style: 'quote', text: '節點和一般的歷史路徑的差別就在於，\n*節點是火車站，一般的歷史路徑是鐵軌*。', src: V20, pos: 'top', y: 280, opt: { size: 56 } },
      ] },
    { id: 's3_station', dur: 16, trans: TR, grade: { warm: 0.3 },
      cam: t => keys([[0, { x: W * 0.62, y: H * 0.56, z: 1.2 }], [16, { x: W * 0.58, y: H * 0.6, z: 1.06 }]], t, lin),
      fx: [{ after: 'mid', draw: c => fx.lamps(c, c.meta.lamps, 0.45, { t0: 0.5, t1: 4, seed: 14 }) }],
      caps: [
        chap('三', '換車', 0.6, 15.6),
        { t0: 1.4, t1: 7.4, style: 'quote', text: '但在節點的時候，在同一個車站\n*你可以換不同方向的車*。', src: V20, pos: 'top', y: 280, opt: { size: 56 } },
        { t0: 7.8, t1: 15.6, style: 'quote', text: '節點就是奇點現象，*奇點的選擇會被無限放大*，\n而奇點過後基本上就是路徑積分在起作用了。', src: V59, pos: 'top', y: 280 },
      ] },
    { id: 's4_split', dur: 14, trans: TR, grade: { warm: 0.1 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.4, z: 1.3 }], [14, { x: W * 0.5, y: H * 0.52, z: 1.04 }]], t, lin),
      layers: { water: t => ({ grow: lerp(-0.02, 1.02, ease(prog(t, 0.5, 10))), soft: 0.08 }) },
      fx: [{ draw: c => fx.glowAt(c, c.meta.pebble, 0, 90, '255,236,190', 0.5 * ease(prog(c.t, 3, 5)) * (1 - prog(c.t, 9, 12))) }],
      caps: [
        chap('四', '一點點', 0.6, 13.6),
        { t0: 1.4, t1: 13.4, style: 'quote', text: '在節點上面只需要差*這麼一點點*，\n最後的分化就會*非常之大*。', src: AY, pos: 'bottom', y: 950, opt: { size: 58 } },
      ] },
    { id: 's5_sluice', dur: 16, trans: TR, grade: { expo: 1.02 },
      cam: t => keys([[0, { x: 1400, y: H * 0.52, z: 1.14 }], [16, { x: 1700, y: H * 0.54, z: 1.1 }]], t, lin),
      layers: { channel: t => ({ grow: lerp(-0.02, 1.02, ease(prog(t, 7.6, 14.5))), soft: 0.06 }) },
      fx: [{ after: 'channel', draw: c => fx.flow(c, c.meta.flow, 0.4, { k: ease(prog(c.t, 8, 10)), col: '210,230,250' }) }],
      caps: [
        chap('五', '放水出閥', 0.6, 15.6),
        { t0: 1.4, t1: 7.2, style: 'quote', text: '（朝鮮戰爭）它的節點意義與1937年的盧溝橋事變和1928年的北伐相比，\n*是微不足道的*。', src: T2, pos: 'top', y: 280, opt: { size: 46, max: 1800 } },
        { t0: 7.6, t1: 15.6, style: 'quote', text: '1972年的大轉向就是*放水出閥*，\n之後無論如何都會在地上衝出一條水道', src: T2, pos: 'top', y: 280 },
      ] },
    { id: 's6_wager', dur: 14, trans: TR, grade: { sat: 0.8, warm: -0.05 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.56, z: 1.04 }], [14, { x: W * 0.48, y: H * 0.6, z: 1.16 }]], t, lin),
      fx: [{ after: 'mid', draw: c => fx.smoke(c, c.meta.fog, 0.45, { k: 1.2, seed: 6 }) },
        { after: 'fig', draw: c => { fx.glowAt(c, c.meta.lantern, 0.45, 220, '255,210,130', 0.75); fx.flame(c, c.meta.lantern, 0.45, { size: 0.8 }); } }],
      caps: [
        chap('六', '賭局', 0.6, 13.6),
        { t0: 1.4, t1: 6.6, style: 'quote', text: '決斷是包括對世界的不確定性未來的*一個賭局*。', src: V20, pos: 'top', y: 300 },
        { t0: 7, t1: 13.6, style: 'quote', text: '如果一切都是確定的，像超市裡面的貨物一樣……\n那你就*用不著決斷*了。', src: V20, pos: 'top', y: 290 },
      ] },
    { id: 's7_birth', dur: 15, trans: TR, grade: { warm: 0.35 },
      cam: t => keys([[0, { x: W * 0.48, y: H * 0.56, z: 1.16 }], [15, { x: W * 0.5, y: H * 0.58, z: 1.06 }]], t, lin),
      fx: [{ after: 'table', draw: c => { fx.flame(c, c.meta.flame, 0.4, { size: 1.3 }); fx.glowAt(c, c.meta.flame, 0.4, 360, '255,200,120', 0.55);
        fx.glowAt(c, c.meta.cradle, 0.4, 300, '255,226,170', 0.4 * ease(prog(c.t, 8, 12))); } }],
      caps: [
        chap('七', '分娩', 0.6, 14.6, { color: 'paper' }),
        { t0: 1.4, t1: 6.8, style: 'quote', text: '決斷時刻都意味著災難，\n決斷是對*政治德性的極大消耗*。', src: YD, color: 'paper', pos: 'top', y: 280, opt: { size: 56 } },
        { t0: 7.2, t1: 14.6, style: 'quote', text: '一個決斷是可以使你徹底毀滅的，*相當於女人生孩子*……\n有可能會誕下新的生命，但也有可能自己也就此完蛋。', src: YD, color: 'paper', pos: 'top', y: 280, opt: { size: 46, max: 1800 } },
      ] },
    { id: 's8_furrow', dur: 15, trans: TR, grade: { warm: 0.3 },
      cam: t => keys([[0, { x: 1100, y: H * 0.54, z: 1.1 }], [15, { x: 1400, y: H * 0.58, z: 1.14 }]], t, lin),
      layers: { furrow: t => ({ grow: lerp(-0.01, 1.01, prog(t, 1.5, 13)), soft: 0.02 }) },
      sprites: (t, c) => { const [cx, cy, rx, ry] = c.meta.furrow, g = clamp(prog(t, 1.5, 13)), a = g * Math.PI * 2 - Math.PI / 2;
        return [{ name: 'ox', x: cx + Math.cos(a) * rx, y: cy + Math.sin(a) * ry + 10, d: 0.45, scale: 0.8 + 0.2 * Math.sin(a), flip: Math.sin(a) > 0, after: Math.sin(a) < 0 ? 'mid' : undefined }]; },
      caps: [
        chap('八', '羅慕路斯時刻', 0.6, 14.6),
        { t0: 1.4, t1: 7, style: 'quote', text: '……羅慕路斯殺死他的弟弟一樣，\n*羅馬城就是建立在這個罪行之上的*。', src: YD, pos: 'top', y: 280 },
        { t0: 7.4, t1: 14.6, style: 'quote', text: '西塞羅這樣的憲法學家，從來沒有迴避過\n羅馬共和國需要自己的*「羅慕路斯時刻」*。', src: '《窪地與韭菜》', pos: 'top', y: 280 },
        { t0: 3, t1: 12, style: 'note', text: '傳說：犁出的一道溝，就是城界', x: 1400, y: 1040, opt: { size: 32 } },
      ] },
    { id: 's9_grass', dur: 16, trans: TR, grade: { warm: 0.1 },
      cam: t => keys([[0, { x: 1100, y: H * 0.54, z: 1.12 }], [16, { x: 1700, y: H * 0.56, z: 1.12 }]], t, lin),
      layers: { regrow: t => ({ grow: lerp(-0.02, 1.05, ease(prog(t, 5, 15))), soft: 0.1 }) },
      sprites: (t, c) => [{ name: `scholar_${Math.floor(t * 3) % 4}`, x: 500 + t * 100, y: c.meta.road_y, d: 0.45, scale: 0.8, after: 'regrow' }],
      caps: [
        chap('九', '游士與土豪', 0.6, 15.6),
        { t0: 1.4, t1: 5.2, style: 'quote', text: '世界上有*游士和土豪*這兩種人', src: V20, pos: 'top', y: 300, opt: { size: 62 } },
        { t0: 5.6, t1: 9.8, style: 'quote', text: '*自發秩序*不是游士能夠搞得起來的。', src: V20, pos: 'top', y: 300 },
        { t0: 10.2, t1: 15.6, style: 'quote', text: '土豪*像野草一樣*是不斷生長的……\n以後一有機會土豪還是會不斷生長。', src: V20, pos: 'top', y: 290 },
      ] },
    { id: 's10_assembly', dur: 15, trans: TR, grade: { warm: 0.15 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.5, z: 1.06 }], [15, { x: W * 0.5, y: H * 0.62, z: 1.24 }]], t, lin),
      fx: [{ after: 'circle', draw: c => fx.glowAt(c, c.meta.table, 0.45, 200, '255,226,160', 0.5 * ease(prog(c.t, 8, 11))) }],
      caps: [
        chap('十', '國父', 0.6, 14.6),
        { t0: 1.4, t1: 7, style: 'quote', text: '美國在建國時期是*根本沒有游士*的，\n所以它的建國條件極其好。', src: V20, pos: 'top', y: 280 },
        { t0: 7.4, t1: 14.6, style: 'quote', text: '制憲會議的成功和憲法的長期穩定證明：\n*國父們善於理解和完成他們的任務*。', src: '《劉仲敬文選 · 第七卷》', pos: 'top', y: 280 },
      ] },
    { id: 's11_light', dur: 14, trans: TR, grade: t => ({ sat: 0.8, expo: lerp(0.94, 1.02, prog(t, 2, 6)) }),
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.56, z: 1.04 }], [14, { x: W * 0.46, y: H * 0.6, z: 1.18 }]], t, lin),
      fx: [{ after: 'one', draw: c => { const v = c.view(0.45), [x, y] = v.P(...c.meta.one);
        fx.godrays(c, x, y - 900, { k: 0.6 * ease(prog(c.t, 2, 4.5)), n: 5, len: 1100, seed: 11 }); fx.glowAt(c, c.meta.one, 0.45, 160, '255,236,190', 0.5 * ease(prog(c.t, 2, 4.5))); } }],
      caps: [
        chap('十一', '天命', 0.6, 13.6),
        { t0: 1.4, t1: 6.6, style: 'quote', text: '他的衝動*突然降臨*在他的身上', src: AY, pos: 'top', y: 300, opt: { size: 62 } },
        { t0: 7, t1: 13.6, style: 'quote', text: '正義規則是*路徑積分的總和*。', src: AY, pos: 'top', y: 300, opt: { size: 62 } },
      ] },
    { id: 's12_oak', dur: 18, grade: t => ({ warm: 0.35, expo: lerp(1.0, 0.92, prog(t, 8, 17)) }),
      cam: t => keys([[0, { x: 1200, y: H * 0.52, z: 1.1 }], [18, { x: 1800, y: H * 0.56, z: 1.12 }]], t, lin),
      fx: [{ draw: c => fx.petals(c, { n: 30, cols: ['230,180,90', '210,140,70'], wind: 60, size: 1.0, k: 0.7 }) }],
      caps: [
        chap('十二', '等得起', 0.6, 15.6),
        { t0: 1.4, t1: 9, style: 'quote', text: '其實*沒有轉捩點*才比較符合自然生長的正常形態，有轉捩點就是對自然生長的傷害了，\n無論你的彎轉得多好，中間肯定都有能量損失。', src: YD, pos: 'top', y: 280, opt: { size: 42, max: 1850 } },
        { t0: 9.4, t1: 15.6, style: 'quote', text: '凡是*能夠等得起*的人，在政治上都是勝利者。', src: V20, pos: 'top', y: 300, opt: { size: 58 } },
        { t0: 15.8, t1: 18, style: 'sub', text: '劉仲敬思想 · 其十四《車站》', pos: 'center', wash: false },
      ] },
  ],
};
