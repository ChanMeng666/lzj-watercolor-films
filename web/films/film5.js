// 第五部《散沙》— 費拉、編戶齊民、末人
import { keys, ease, easeOut, easeIn, prog, clamp, lerp, hash } from '../lib/engine.js';
import * as fx from '../lib/fx.js';

const W = 2304, H = 1296, TR = 2, lin = x => x;
const WJ = '《窪地與韭菜》', YD = '《文明更迭的源代碼》', JY = '《經與史》', TW = '劉仲敬 Twitter';
const chap = (num, text, t0, t1, o = {}) => ({ style: 'chapter', num, text, t0, t1, ...o });

// 韭菜：割了又長，長了又割
function chives(t) {
  const cuts = [[2, 6], [8, 11.5], [13.5, 16.5]];
  for (let i = 0; i < cuts.length; i++) {
    const [a, b] = cuts[i];
    if (t < a) return { grow: -0.1, conceal: true, alpha: i === 0 ? 1 : ease(prog(t, cuts[i - 1][1] + 0.3, a - 0.2)) };
    if (t <= b) return { grow: lerp(-0.05, 1.08, ease(prog(t, a, b))), conceal: true, soft: 0.05 };
  }
  return { grow: 1.1, conceal: true };
}

export default {
  title: '散沙',
  fadeIn: 1.5, fadeOut: 2.5,
  scenes: [
    { id: 's1_bow', dur: 16, trans: TR, grade: { sat: 0.8, warm: -0.05 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.5, z: 1.06 }], [16, { x: W * 0.42, y: H * 0.56, z: 1.16 }]], t, lin),
      sprites: (t, c) => [{ name: `bower_${Math.floor(t * 0.7) % 2}`, x: c.meta.bower[0], y: c.meta.bower[1], d: 0.45, scale: 1, after: 'mid' }],
      caps: [
        { t0: 1.5, t1: 6.8, style: 'title', text: '散沙', pos: 'center', y: 420 },
        { t0: 2.6, t1: 6.8, style: 'sub', text: '劉仲敬思想 · 水彩短片 其五 —— 費拉、編戶齊民與末人', pos: 'center', y: 560, wash: false },
        chap('一', '費拉的行為模式', 7.2, 15.6),
        { t0: 7.6, t1: 15.6, style: 'quote', text: '首先，費拉是*誰都惹不起*的。其次，費拉從來不能指望公正的待遇。\n最後，費拉相信自己的*話語價值為零*。', src: TW, pos: 'bottom', y: 900, opt: { size: 50, max: 1700 } },
      ] },
    { id: 's2_sift', dur: 16, trans: TR, grade: { warm: 0.05 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.56, z: 1.1 }], [16, { x: W * 0.5, y: H * 0.6, z: 1.16 }]], t, lin),
      layers: { clans: t => ({ grow: lerp(-0.05, 1.08, ease(prog(t, 3, 12))), conceal: true, soft: 0.08 }) },
      caps: [
        chap('二', '散沙是設計出來的', 0.6, 15.6),
        { t0: 1.2, t1: 8.4, style: 'vquote', text: '一盤散沙實為獨夫政體之設計目的，\n集權術之要在破除民間組織資源，\n化萬民為孤立散漫之原子。', src: '數卷殘編', x: 1720, y: 200, opt: { size: 50, col: 16 } },
        { t0: 8.8, t1: 15.6, style: 'quote', text: '「編戶齊民」不僅要毀滅封建，而且要*毀滅氏族*，\n將一切資源集中到國家手中。', src: JY, pos: 'top', y: 280 },
        { t0: 3, t1: 8, style: 'note', text: '宗族：有機的共同體', x: 520, y: 1020 },
        { t0: 11, t1: 15.4, style: 'note', text: '編戶：一模一樣的原子', x: 520, y: 1020 },
      ] },
    { id: 's3_doors', dur: 14, trans: TR, grade: { warm: 0.2 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.5, z: 1.06 }], [14, { x: W * 0.5, y: H * 0.5, z: 1.3 }]], t, lin),
      fx: [{ after: 'street', draw: c => fx.lamps(c, c.meta.lamps, 0.4, { t0: 1, t1: 6, k: 0.8, order: (i, n) => (i % 9) / 9 }) }],
      caps: [
        chap('三', '一筆交易', 0.6, 13.6),
        { t0: 1.6, t1: 13.4, style: 'quote', text: '如果登記成為編戶齊民，你是*最省心*的，\n但是你的子孫後代的地位也*最低*……', src: '《劉仲敬訪談 155》', pos: 'bottom', y: 940 },
      ] },
    { id: 's4_tower', dur: 16, trans: TR, grade: { warm: 0.15 },
      cam: t => keys([[0, { x: W * 0.34, y: H * 0.5, z: 1.18 }], [16, { x: W * 0.66, y: H * 0.5, z: 1.18 }]], t, lin),
      fx: [{ draw: c => fx.petals(c, { n: 90, cols: ['230,200,150', '210,180,130'], wind: 260, fall: 10, size: 0.35, k: 0.6 * (1 - prog(c.t, 8, 11)), seed: 3 }) }],
      caps: [
        chap('四', '強大的軟弱，軟弱的強大', 0.6, 15.6),
        { t0: 1.4, t1: 8.4, style: 'quote', text: '他們踐踏腳下的散沙，因此覺得只有自己強大；\n然而因為他們腳下只有散沙，所以*經不住任何覬覦者突然襲擊*。', src: JY, pos: 'bottom', y: 950, opt: { size: 48, max: 1600 } },
        { t0: 8.8, t1: 15.6, style: 'quote', text: '只要分枝沒有凋殘殆盡，\n無論多麼強大的突然襲擊都*不可能砍倒大樹*。', src: JY, pos: 'bottom', y: 950 },
        { t0: 2.5, t1: 8.2, style: 'note', text: '孤家寡人', x: 330, y: 300, from: [330, 330], at: [W * 0.24, H * 0.42, 0.4] },
        { t0: 10, t1: 15.4, style: 'note', text: '宗法：盤根錯節', x: 1560, y: 280 },
      ] },
    { id: 's5_canal', dur: 14, trans: TR, grade: { warm: 0.3, sat: 0.85 },
      cam: t => keys([[0, { x: 1300, y: H * 0.55, z: 1.1 }], [14, { x: 1700, y: H * 0.56, z: 1.12 }]], t, lin),
      sprites: (t, c) => [0, 1, 2, 3, 4, 5].map(i => ({ name: `refugee_${Math.floor(t * 2.6 + i) % 4}`, x: 300 + i * 150 + t * 55, y: c.meta.walk_y + (i % 2) * 14, d: 0.45, scale: 0.7, after: 'fields' })),
      caps: [
        chap('五', '流民的機器', 0.6, 13.6),
        { t0: 1.6, t1: 13.4, style: 'quote', text: '這樣的散沙開始是在技術上沒有創造力，最後連生存能力都沒有了，\n變成*製造流民的機器*，最終成為帝國的負擔。', src: '《劉仲敬訪談 016》', pos: 'top', y: 270, opt: { size: 48, max: 1600 } },
      ] },
    { id: 's6_chives', dur: 18, trans: TR, grade: { warm: 0.05 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.56, z: 1.1 }], [18, { x: W * 0.5, y: H * 0.6, z: 1.18 }]], t, lin),
      layers: { chives: chives },
      caps: [
        chap('六', '韭菜', 0.6, 17.6),
        { t0: 1.4, t1: 7.8, style: 'quote', text: '這些人的*人頭本身*就可以構成一個巨大的市場。', src: WJ, pos: 'top', y: 290 },
        { t0: 8.2, t1: 17.6, style: 'quote', text: '這些活動像是一個*掉進水裏面的人不斷地喝水*那樣，\n談不上是一種改革，只是一些應急措施而已。', src: WJ, pos: 'top', y: 290 },
      ] },
    { id: 's7_cradle', dur: 14, trans: TR, grade: { warm: 0.25 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.6, z: 1.2 }], [14, { x: W * 0.5, y: H * 0.58, z: 1.08 }]], t, lin),
      fx: [{ draw: c => { fx.glowAt(c, c.meta.lamp, 0.4, 700, '255,200,130', 0.25); fx.motes(c, c.meta.lamp, 0.4, { n: 30 }); } }],
      caps: [
        chap('七', '擊鼓傳花', 0.6, 13.6),
        { t0: 1.6, t1: 13.4, style: 'quote', text: '在博弈的所有各方當中，*沒有出生的嬰兒*是最弱勢的，\n所以博弈的結果必定是不利於他們的。', src: WJ, pos: 'top', y: 280 },
        { t0: 5, t1: 13, style: 'note', text: '時間轉移型政策的付款人：\n不能反抗、不能投票、不能退出', x: 1660, y: 600, opt: { size: 36 } },
      ] },
    { id: 's8_hill', dur: 16, trans: TR, grade: { warm: 0.05 },
      cam: t => keys([[0, { x: W * 0.42, y: H * 0.5, z: 1.12 }], [16, { x: W * 0.56, y: H * 0.46, z: 1.06 }]], t, lin),
      caps: [
        chap('八', '演化不能爬山坡', 0.6, 15.6),
        { t0: 1.4, t1: 8.6, style: 'quote', text: '……如果採取對長期更有利的方式，那麼他們在短期內就可能被篩掉了。\n*演化是不能夠爬山坡的*', src: WJ, pos: 'bottom', y: 960, opt: { size: 46, max: 1700 } },
        { t0: 9, t1: 15.6, style: 'quote', text: '所有人把手伸進別人的口袋裏面破壞別人製造的秩序很容易，\n而*自己製造秩序卻很難*。', src: '《劉仲敬訪談 057》', pos: 'bottom', y: 960, opt: { size: 48, max: 1600 } },
        { t0: 2.5, t1: 15.4, style: 'note', text: '互害：短期最優', x: 520, y: 520, from: [560, 560], at: [W * 0.3, H * 0.58, 0.4] },
        { t0: 4, t1: 15.4, style: 'note', text: '長期更優', x: 1500, y: 300, from: [1560, 320], at: [W * 0.77, H * 0.26, 0.4] },
        { t0: 5.5, t1: 15.4, style: 'note', text: '必須先走過的谷底', x: 1240, y: 760, from: [1260, 790], at: [W * 0.56, H * 0.86, 0.4] },
      ] },
    { id: 's9_cards', dur: 16, trans: TR, grade: { warm: 0.1 },
      cam: t => keys([[0, { x: W * 0.45, y: H * 0.52, z: 1.12 }], [16, { x: W * 0.5, y: H * 0.52, z: 1.06 }]], t, lin),
      layers: { door_open: t => (t < 7 ? { hide: true } : { alpha: ease(prog(t, 7, 7.3)) }) },
      sprites: (t, c) => c.meta.cards.map(([x, y, r, lvl], i) => {
        const t0 = 7.6 + (3 - lvl) * 0.12 + hash(i, 2) * 0.25;
        const e = Math.max(0, t - t0);
        const fall = Math.min(e * e * 900, y < c.meta.ty ? c.meta.ty - y : 0);
        const dir = r > 0 ? -1 : 1;
        return { name: 'card', x: x + dir * e * 160 * (e < 1.2 ? 1 : 0) + dir * Math.min(e, 1.2) * 0, y: y + fall,
                 rot: r + dir * Math.min(e * 2.6, 1.35), d: 0.3, scale: 1 };
      }),
      fx: [{ draw: c => { if (c.t > 7) fx.petals(c, { n: 40, cols: ['255,255,255'], wind: -500, fall: 30, size: 0.4, k: 0.5 * (1 - prog(c.t, 9, 11)), seed: 8 }); } }],
      caps: [
        chap('九', '心臟病組織', 0.6, 15.6),
        { t0: 1.4, t1: 15.6, style: 'quote', text: '這樣的組織像是一個患有*心臟病*的人，坐着不動的時候，看上去跟別人沒有什麼兩樣；\n一旦稍微遇到一點點外來壓力，就會*分崩離析*', src: WJ, pos: 'top', y: 270, opt: { size: 46, max: 1700 } },
      ] },
    { id: 's10_feast', dur: 16, trans: TR, grade: { warm: 0.1 },
      cam: t => keys([[0, { x: 1200, y: H * 0.5, z: 1.12 }], [16, { x: 1800, y: H * 0.52, z: 1.12 }]], t, lin),
      fx: [
        { after: 'sky', draw: c => fx.fireworks(c, [[0.5, 600, 300, '255,200,120'], [1.6, 1100, 220, '255,140,150'], [2.8, 800, 180, '200,220,255'],
          [3.9, 1300, 260, '255,230,150'], [5.0, 500, 200, '180,255,200'], [6.4, 1000, 150, '255,170,90'], [7.7, 1400, 240, '255,120,120'],
          [9.0, 700, 260, '255,220,180'], [10.4, 1200, 200, '210,190,255'], [11.8, 900, 280, '255,200,120']], 0.15) },
        { after: 'town', draw: c => fx.lamps(c, c.meta.lamps, 0.35, { t0: 0, t1: 1, k: 1.2 }) },
      ],
      caps: [
        chap('十', '盛世', 0.6, 15.6, { color: 'paper' }),
        { t0: 1.4, t1: 9, style: 'quote', text: '一個即將發財的人是什麼樣子的？在你身邊走過去了你都注意不到。\n但是一個已經發了財、正在*揮霍*他既有積累的人，卻是*人人都能看見*的。', src: YD, color: 'paper', pos: 'bottom', y: 940, opt: { size: 44, max: 1700 } },
        { t0: 9.4, t1: 15.6, style: 'quote', text: '末人不會覺得自己處於衰退的年代，甚至連*衰退的概念*都沒有……', src: YD, color: 'paper', pos: 'bottom', y: 960 },
        { t0: 3, t1: 9, style: 'note', text: '空了的糧倉', x: 1700, y: 520, color: 'paper' },
      ] },
    { id: 's11_garden', dur: 18, grade: { warm: -0.1, sat: 0.85 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.48, z: 1.06 }], [18, { x: W * 0.52, y: H * 0.6, z: 1.3 }]], t, lin),
      fx: [{ after: 'snow', draw: c => fx.lamps(c, c.meta.lamps, 0.45, { t0: 9, t1: 9.1, k: 1.0 }) }, { draw: c => fx.snow(c, { n: 260, wind: 30, speed: 0.7 }) }],
      caps: [
        chap('十一', '流沙之後', 0.6, 16),
        { t0: 1.4, t1: 6.6, style: 'quote', text: '一旦末人們把組織資源完全消耗，再也沒有辦法透支了，\n*整個架子就會倒下去*。', src: YD, pos: 'top', y: 270 },
        { t0: 7, t1: 11.8, style: 'quote', text: '費拉性實際上是一種比較低級的、用來*填補空白的流沙*。', src: WJ, pos: 'top', y: 280 },
        { t0: 12.2, t1: 16, style: 'quote', text: '而希望的種子，更可能保留在*小團體*裏面。', src: YD, pos: 'top', y: 280 },
        { t0: 16.2, t1: 18, style: 'sub', text: '劉仲敬思想 · 其五《散沙》', pos: 'center', wash: false },
      ] },
  ],
};
