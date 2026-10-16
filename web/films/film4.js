// 第四部《窪地》— 秩序的輸入與輸出
import { keys, ease, easeOut, easeIn, prog, clamp, lerp, hash } from '../lib/engine.js';
import * as fx from '../lib/fx.js';

const W = 2304, H = 1296, TR = 2, lin = x => x;
const WD = '《中國窪地》', WJ = '《窪地與韭菜》', YD = '《文明更迭的源代碼》', F151 = '《劉仲敬訪談 151》';
const chap = (num, text, t0, t1, o = {}) => ({ style: 'chapter', num, text, t0, t1, ...o });

export default {
  title: '窪地',
  fadeIn: 1.5, fadeOut: 2.5,
  scenes: [
    { id: 's1_protect', dur: 16, trans: TR, grade: { warm: 0.3 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.5, z: 1.08 }], [16, { x: W * 0.58, y: H * 0.46, z: 1.18 }]], t, lin),
      sprites: (t, c) => {
        const [a, b] = c.meta.path, k = ease(prog(t, 2, 13));
        return [{ name: 'pilgrim', x: lerp(a[0], b[0], k), y: lerp(a[1], b[1], k) + 14 - Math.abs(Math.sin(t * 5)) * 4, d: 0.45, scale: 0.9, after: 'hill' }];
      },
      fx: [{ after: 'hill', draw: c => fx.glowAt(c, c.meta.rider, 0.45, 260, '255,220,160', 0.25 * ease(prog(c.t, 8, 10))) }],
      caps: [
        { t0: 1.5, t1: 6.8, style: 'title', text: '窪地', pos: 'center', y: 420 },
        { t0: 2.6, t1: 6.8, style: 'sub', text: '劉仲敬思想 · 水彩短片 其四 —— 秩序的輸入與輸出', pos: 'center', y: 560, wash: false },
        chap('一', '最原始的交易', 7.2, 15.6),
        { t0: 7.8, t1: 15.6, style: 'quote', text: '他需要*輸入秩序*，不輸入秩序他就活不了。', src: WD },
        { t0: 10, t1: 15.6, style: 'note', text: '秩序輸出者', x: 1560, y: 380, from: [1560, 410], at: [W * 0.72, H * 0.5, 0.45] },
      ] },
    { id: 's2_basin', dur: 16, trans: TR, grade: { warm: -0.1, sat: 0.9 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.45, z: 1.06 }], [16, { x: W * 0.5, y: H * 0.62, z: 1.28 }]], t, lin),
      fx: [
        { after: 'land', draw: c => { c.meta.streams.forEach((p, i) => fx.flow(c, p, 0.35, { seed: i * 7 }));
          fx.lamps(c, c.meta.hi, 0.35, { t0: 1, t1: 4, k: 0.7 }); } },
        { draw: c => fx.rain(c, { n: 380, k: 0.9 }) },
      ],
      caps: [
        chap('二', '低氣壓', 0.6, 15.6),
        { t0: 1.2, t1: 10, style: 'quote', text: '因為大自然厭惡真空，秩序生產力強的地方，\n自然而然的就會被秩序生產力弱的地方造成的*低氣壓*所吸引，\n導致秩序從一方輸入到另外一方。', src: WD, pos: 'bottom', y: 860, opt: { size: 50, max: 1500 } },
        { t0: 10.4, t1: 15.6, style: 'quote', text: '什麼是帝國呢？帝國就是一個*秩序的窪地*。', src: WD, pos: 'bottom', y: 880 },
      ] },
    { id: 's3_wall', dur: 14, trans: TR, grade: { sat: 0.85, warm: -0.05 },
      cam: t => keys([[0, { x: 1700, y: H * 0.5, z: 1.1 }], [14, { x: 1200, y: H * 0.52, z: 1.14 }]], t, lin),
      sprites: (t, c) => {
        const out = [];
        for (let i = 0; i < 7; i++) {
          const x = 2900 - t * (230 + 12 * i) - i * 200;
          out.push({ name: `rider_${Math.floor(t * 7 + i) % 4}`, x, y: c.meta.ride_y + (i % 3) * 30, d: 0.3, scale: 0.42 + 0.04 * (i % 3), flip: true, after: 'steppe' });
        }
        return out;
      },
      fx: [{ after: 'wall', draw: c => c.meta.towers.forEach((p, i) => { if (c.t > 2 + i * 1.2) fx.fire(c, p, 0.55, { size: 0.5, k: ease(prog(c.t, 2 + i * 1.2, 3 + i * 1.2)) }); }) }],
      caps: [
        chap('三', '轉折點', 0.6, 13.6),
        { t0: 1.6, t1: 13.4, style: 'quote', text: '以前，你殖民蠻族；\n以後，蠻族要越過長城入侵你了。', src: WD, pos: 'top', y: 260, opt: { size: 62 } },
        { t0: 6, t1: 13.4, style: 'note', text: '帝國：從秩序輸出\n轉為秩序輸入的那一刻', x: 470, y: 1000, wash: true },
      ] },
    { id: 's4_gate', dur: 14, trans: TR, grade: { warm: 0.35 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.5, z: 1.14 }], [14, { x: W * 0.5, y: H * 0.56, z: 1.06 }]], t, lin),
      sprites: (t, c) => {
        const out = [];
        for (let i = 0; i < 6; i++) {
          const k = clamp((t - i * 1.7) / 9);
          if (k <= 0 || k >= 1) continue;
          out.push({ name: `camel_${Math.floor(t * 4 + i) % 4}`, x: lerp(W * 0.5, W * 0.72, k), y: lerp(H * 0.79, H * 1.02, k * k), d: 0.6, scale: lerp(0.25, 1.25, k * k), alpha: clamp(k * 6) });
        }
        return out.sort((a, b) => a.y - b.y);
      },
      fx: [{ after: 'cliffs', draw: c => fx.godrays(c, 960, 300, { k: 0.5, n: 8, len: 1300, seed: 9 }) }],
      caps: [
        chap('四', '旋轉門', 0.6, 13.6),
        { t0: 1.6, t1: 13.4, style: 'quote', text: '中亞是個巨大的*旋轉門*，文明核心地帶、東地中海地區開創的東西，\n透過這裡源源不斷地向東方輸出。', src: YD, pos: 'top', y: 260, opt: { size: 50, max: 1600 } },
      ] },
    { id: 's5_chariot', dur: 12, trans: TR, grade: { sat: 0.9 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.52, z: 1.06 }], [12, { x: W * 0.5, y: H * 0.6, z: 1.24 }]], t, lin),
      fx: [{ draw: c => { fx.flash(c, 0.4); fx.flash(c, 1.1, { k: 0.6 }); fx.godrays(c, 1100, -150, { k: 0.6 * ease(prog(c.t, 0.6, 2)), n: 9, seed: 5 }); } }],
      caps: [
        chap('五', '平地一聲雷', 0.6, 11.6),
        { t0: 1.4, t1: 7.2, style: 'quote', text: '殷商賴以維持統治的法寶就是戰車，\n而戰車在中國像是飛機和坦克一樣，是*平地一聲雷*出現的。', src: F151, pos: 'top', y: 260, opt: { size: 50 } },
        { t0: 7.4, t1: 11.6, style: 'quote', text: '為什麼你的東西一開始就是完善的呢？\n因為你是*進口*的。', src: F151, pos: 'top', y: 260, opt: { size: 60 } },
      ] },
    { id: 's6_waves', dur: 16, trans: TR, grade: { warm: 0.1 },
      cam: t => keys([[0, { x: 1150, y: H * 0.54, z: 1.12 }], [16, { x: 1850, y: H * 0.56, z: 1.12 }]], t, lin),
      sprites: (t, c) => {
        const names = ['wave_rider', 'wave_factory', 'wave_ship'], at = [1.5, 6.5, 11];
        return names.map((n, i) => { const k = ease(prog(t, at[i], at[i] + 1.5)); return { name: n, x: c.meta.spots[i][0], y: c.meta.spots[i][1] + (1 - k) * 40, d: 0.5, scale: 0.75, alpha: k }; });
      },
      caps: [
        chap('六', '一波又一波', 0.6, 15.6),
        { t0: 2.2, t1: 6.3, style: 'note', text: '鮮卑', x: 640, y: 300 },
        { t0: 1.4, t1: 6.3, style: 'quote', text: '永嘉之亂輸入了第一批內亞部落的組織資源，\n產生了北朝和隋唐帝國', src: YD, pos: 'bottom', y: 940, opt: { size: 50 } },
        { t0: 7, t1: 11, style: 'concept', text: '工業化：蘇聯的秩序輸入', pos: 'bottom', y: 960 },
        { t0: 11.4, t1: 15.6, style: 'quote', text: '改革開放是*美國秩序的輸入*', src: '《劉仲敬訪談 106》', pos: 'bottom', y: 950 },
      ] },
    { id: 's7_vessels', dur: 16, trans: TR, grade: { warm: 0.25 },
      cam: t => keys([[0, { x: 900, y: H * 0.56, z: 1.2 }], [16, { x: 2100, y: H * 0.56, z: 1.2 }]], t, lin),
      fx: [{ draw: c => fx.glowAt(c, [c.cam.x, H * 0.3], 0.4, 900, '255,210,150', 0.18) }],
      caps: [
        chap('七', '瓦房店化', 0.6, 15.6),
        { t0: 1.2, t1: 8.6, style: 'quote', text: '只有你自己研發不出來的靠引進的東西，才會是一開始引進的東西非常完善，\n由你自己製造了以後就*一代不如一代*地垮下去。', src: F151, pos: 'top', y: 260, opt: { size: 46, max: 1700 } },
        { t0: 9, t1: 15.6, style: 'quote', text: '本土發展出來的那些萌芽還沒有來得及長大，就得不到回報而夭折了。\n因此，瓦房店化是*輪番不斷*的。', src: WJ, pos: 'top', y: 260, opt: { size: 46, max: 1700 } },
        { t0: 2, t1: 7, style: 'note', text: '引進', x: 420, y: 520, from: [420, 560], at: [420, H * 0.5, 0.4] },
        { t0: 10, t1: 15.4, style: 'note', text: '自己仿造', x: 1500, y: 520, from: [1500, 560], at: [2580, H * 0.5, 0.4] },
      ] },
    { id: 's8_armor', dur: 14, trans: TR, grade: { warm: 0.1 },
      cam: t => keys([[0, { x: W * 0.4, y: H * 0.56, z: 1.12 }], [14, { x: W * 0.62, y: H * 0.56, z: 1.12 }]], t, lin),
      caps: [
        chap('八', '誰下訂單', 0.6, 13.6),
        { t0: 1.4, t1: 13.4, style: 'quote', text: '鐵匠的訂貨者是封建領主，封建領主自己是要上戰場的，\n不能接受讓他自己送命的劣質產品。\n而官僚則是*讓別人去死*', src: WJ, pos: 'top', y: 260, opt: { size: 48, max: 1500 } },
        { t0: 4, t1: 13, style: 'note', text: '自己穿', x: 420, y: 1010 },
        { t0: 7, t1: 13, style: 'note', text: '給別人穿', x: 1500, y: 1010 },
      ] },
    { id: 's9_pigment', dur: 18, trans: TR, grade: t => ({ sat: lerp(1.05, 0.95, prog(t, 4, 12)), warm: 0.1 }),
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.5, z: 1.1 }], [18, { x: W * 0.5, y: H * 0.5, z: 1.04 }]], t, lin),
      layers: { color: t => ({ grow: lerp(-0.05, 1.08, ease(prog(t, 4.5, 12.5))), conceal: true, soft: 0.1 }) },
      sprites: (t, c) => {
        const out = [];
        for (let i = 0; i < 4; i++) {
          const x = 900 + t * 120 + i * 150;
          out.push({ name: `camel_${Math.floor(t * 4 + i) % 4}`, x, y: H * 0.36 + i * 4, d: 0.3, scale: 0.55, alpha: 1 - prog(t, 4, 7) });
        }
        return out;
      },
      caps: [
        chap('九', '連這幅畫也是', 0.6, 17.6),
        { t0: 1.4, t1: 11.8, style: 'quote', text: '唐代用來自巴達克山的內亞顏料繪製的各種*金碧輝煌*的複雜圖畫，\n在宋代就退化為只有*黑白兩色*的文人畫和山水畫。', src: WJ, pos: 'bottom', y: 940, opt: { size: 48, max: 1600 } },
        { t0: 12.2, t1: 17.6, style: 'quote', text: '只有宋徽宗才能用得起內亞顏料，\n普通士大夫只能改畫水墨畫', src: '劉仲敬 Twitter', pos: 'bottom', y: 950 },
      ] },
    { id: 's10_river', dur: 16, trans: TR, grade: { expo: 1.02 },
      cam: t => keys([[0, { x: 1200, y: H * 0.56, z: 1.12 }], [16, { x: 1800, y: H * 0.56, z: 1.12 }]], t, lin),
      sprites: (t, c) => [0, 1, 2].map(i => ({ name: 'boat', x: ((400 + i * 900 + t * 110) % 3100) - 100, y: c.meta.river_y + i * 30, d: 0.4, scale: 0.8, after: 'banks' })),
      fx: [
        { after: 'sky', draw: c => fx.stars(c, { n: 150, k: 0.7 }) },
        { after: 'banks', draw: c => {
          fx.lamps(c, c.meta.left, 0.4, { t0: -2, t1: -1, off: [3, 11], seed: 3 });
          fx.lamps(c, c.meta.right, 0.4, { t0: 5, t1: 14, seed: 4 });
          [0, 1, 2].forEach(i => fx.glowAt(c, [((400 + i * 900 + c.t * 110) % 3100) - 100, c.meta.river_y - 90 + i * 30], 0.4, 120, '255,200,120', 0.5));
        } },
      ],
      caps: [
        chap('十', '資金流過的地方', 0.6, 15.6, { color: 'paper' }),
        { t0: 1.4, t1: 10, style: 'quote', text: '只要你是資金流流過的地方，你的生命就會比較貴，你的秩序就會維持得比較好；\n資金流的線路從你那兒離開以後，很容易發生*戰亂和生命貶值*的現象。', src: WD, color: 'paper', pos: 'bottom', y: 940, opt: { size: 44, max: 1700 } },
        { t0: 10.4, t1: 15.6, style: 'quote', text: '朝鮮其實並沒有做錯什麼，只是它*被世界遺棄*了。', src: WD, color: 'paper', pos: 'bottom', y: 960 },
      ] },
    { id: 's11_throne', dur: 18, grade: t => ({ warm: 0.35, expo: lerp(1.0, 0.9, prog(t, 4, 16)) }),
      cam: t => keys([[0, { x: W * 0.55, y: H * 0.5, z: 1.2 }], [18, { x: W * 0.5, y: H * 0.5, z: 1.06 }]], t, lin),
      caps: [
        chap('十一', '壞人', 0.6, 15, { opt: { size: 64 } }),
        { t0: 1.4, t1: 8.6, style: 'quote', text: '壞人的意思就是說這個人*占據了秩序輸出者的生態位*，\n卻承擔不了提供秩序的責任。', src: YD, pos: 'top', y: 260, opt: { size: 50 } },
        { t0: 9, t1: 15, style: 'quote', text: '暴力行為如果達到了維持秩序的結果，常常會得到原諒和遺忘。\n軟弱的假冒統治者既然不能維持秩序，就算沒有罪名也可以臨時捏造。', src: YD, pos: 'top', y: 260, opt: { size: 44, max: 1600 } },
        { t0: 15.3, t1: 18, style: 'sub', text: '劉仲敬思想 · 其四《窪地》', pos: 'center', wash: false },
      ] },
  ],
};
