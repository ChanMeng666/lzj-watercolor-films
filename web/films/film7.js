// 第七部《小路》— 習慣法、封建契約、沒有主權者的國家
import { keys, ease, easeOut, easeIn, prog, clamp, lerp, hash } from '../lib/engine.js';
import * as fx from '../lib/fx.js';

const W = 2304, H = 1296, TR = 2, lin = x => x;
const DC = '《英格蘭習慣法與自治社團》講座', DB = '《簡明英國政治史》講座', YD = '《文明更迭的源代碼》', JY = '《經與史》';
const chap = (num, text, t0, t1, o = {}) => ({ style: 'chapter', num, text, t0, t1, ...o });

export default {
  title: '小路',
  fadeIn: 1.5, fadeOut: 2.5,
  scenes: [
    { id: 's1_path', dur: 15, trans: TR, grade: { warm: 0.25 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.5, z: 1.08 }], [15, { x: W * 0.5, y: H * 0.58, z: 1.2 }]], t, lin),
      layers: { path: t => ({ grow: lerp(-0.02, 1.0, ease(prog(t, 3, 12))), soft: 0.15 }) },
      fx: [{ draw: c => fx.godrays(c, 1300, -120, { k: 0.4, seed: 7 }) }],
      caps: [
        { t0: 1.4, t1: 6.6, style: 'title', text: '小路', pos: 'center', y: 400 },
        { t0: 2.5, t1: 6.6, style: 'sub', text: '劉仲敬思想 · 水彩短片 其七 —— 習慣法與沒有主權者的國家', pos: 'center', y: 540, wash: false },
        chap('一', '踩出來的路', 7, 14.6),
        { t0: 7.4, t1: 14.6, style: 'quote', text: '習慣法不是你正式投資修的*高速公路*，\n它是普普通通的獵人和牧民在叢林中*踩出的小路*。', src: DC, pos: 'top', y: 290 },
      ] },
    { id: 's2_elder', dur: 15, trans: TR, grade: { warm: 0.15 },
      cam: t => keys([[0, { x: W * 0.45, y: H * 0.56, z: 1.14 }], [15, { x: W * 0.5, y: H * 0.5, z: 1.08 }]], t, lin),
      caps: [
        chap('二', '法律是發現的', 0.6, 14.6),
        { t0: 1.4, t1: 6.6, style: 'quote', text: '你只能夠*發現*法律，不能夠制定法律，不能夠發明法律。', src: DB, pos: 'top', y: 300 },
        { t0: 7, t1: 14.6, style: 'quote', text: '懺悔者愛德華和布拉克頓都覺得：立法者除了*輯錄父老口傳的風俗*、\n給民眾的集體記憶提供一個副本以外，什麼都不能做。', src: JY, pos: 'top', y: 290, opt: { size: 46 } },
        { t0: 3, t1: 14, style: 'note', text: '父老', x: 1500, y: 560, from: [1480, 590], at: [W * 0.55, H * 0.66, 0.45] },
        { t0: 8, t1: 14, style: 'note', text: '羊皮紙上的副本', x: 560, y: 600, from: [600, 630], at: [W * 0.32, H * 0.72, 0.45] },
      ] },
    { id: 's3_king', dur: 15, trans: TR, grade: { warm: 0.1 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.56, z: 1.2 }], [15, { x: W * 0.5, y: H * 0.54, z: 1.08 }]], t, lin),
      caps: [
        chap('三', '在社會之中，而非之上', 0.6, 14.6),
        { t0: 1.4, t1: 7.8, style: 'quote', text: '君主可發現法而不可制定法……\n如繪製山川地圖，本無需問其何者為善何者當改。', src: '劉仲敬四維言論', pos: 'top', y: 290 },
        { t0: 8.2, t1: 14.6, style: 'quote', text: '若君主者，亦*在社會之中而非社會之上*，\n貴族之首而非其主', src: '劉仲敬四維言論', pos: 'top', y: 290 },
      ] },
    { id: 's4_market', dur: 17, trans: TR, grade: { warm: 0.15, sat: 1.05 },
      cam: t => keys([[0, { x: 1100, y: H * 0.52, z: 1.12 }], [17, { x: 1700, y: H * 0.52, z: 1.12 }]], t, lin),
      fx: [{ after: 'mid', draw: c => c.meta.scrolls.forEach((p, i) => {
        const pulse = i === 5 ? (c.t < 6 ? 1 : c.t < 9 ? 1 - ease(prog(c.t, 6, 7.5)) : ease(prog(c.t, 11, 12.5))) : 0.15 + 0.15 * Math.sin(c.t * 2 + i);
        fx.glowAt(c, p, 0.45, 90, '255,226,150', 0.6 * pulse);
      }) }],
      caps: [
        chap('四', '判例的市場', 0.6, 16.6),
        { t0: 1.4, t1: 6.6, style: 'quote', text: '普通法是一種類似*市場經濟*的東西，就是說它允許自由選擇，\n你可以要也可以不要，這個判例你可以引用也可以不引用。', src: YD, pos: 'top', y: 290, opt: { size: 46, max: 1700 } },
        { t0: 7, t1: 12.4, style: 'quote', text: '所謂主流的判例，就像最流行的*蘋果手機*一樣……新的判例很容易產生，\n也很容易取代舊的判例，但是舊的判例也很容易*捲土重來*。', src: YD, pos: 'top', y: 290, opt: { size: 44, max: 1800 } },
        { t0: 12.8, t1: 16.6, style: 'quote', text: '所謂沒有立法者的法，實際上就等於*人人都是立法者*', src: YD, pos: 'top', y: 300 },
      ] },
    { id: 's5_homage', dur: 15, trans: TR, grade: { warm: 0.2 },
      cam: t => keys([[0, { x: W * 0.48, y: H * 0.56, z: 1.14 }], [15, { x: W * 0.52, y: H * 0.52, z: 1.06 }]], t, lin),
      caps: [
        chap('五', '私人契約', 0.6, 14.6),
        { t0: 1.4, t1: 14.6, style: 'quote', text: '我們私人之間有契約，我保護你，你給我盡什麼什麼義務，\n比如*服役40天*，這跟其他人有什麼關係。', src: DB, pos: 'bottom', y: 980 },
        { t0: 4, t1: 14, style: 'note', text: '四十天', x: 330, y: 560 },
        { t0: 6, t1: 14, style: 'note', text: '兩枚同樣大小的封印', x: 1700, y: 900 },
      ] },
    { id: 's6_network', dur: 15, trans: TR, grade: { warm: 0.1 },
      cam: t => keys([[0, { x: 1200, y: H * 0.56, z: 1.1 }], [15, { x: 1700, y: H * 0.56, z: 1.1 }]], t, lin),
      fx: [{ after: 'mid', draw: c => {
        const v = c.view(0.45), N = c.meta.nodes;
        c.n.lineWidth = 3; c.n.lineCap = 'round';
        for (let i = 0; i < N.length; i++) for (let j = i + 1; j < Math.min(N.length, i + 3); j++) {
          const k = ease(prog(c.t, 1 + (i + j) * 0.35, 2.5 + (i + j) * 0.35)); if (k <= 0) continue;
          const [x0, y0] = v.P(...N[i]), [x1, y1] = v.P(...N[j]);
          const mx = (x0 + x1) / 2, my = Math.min(y0, y1) - 60;
          c.n.strokeStyle = `rgba(170,50,40,${0.55 * k})`;
          c.n.beginPath(); c.n.moveTo(x0, y0);
          for (let s = 1; s <= 20 * k; s++) { const u = s / 20; c.n.lineTo((1 - u) ** 2 * x0 + 2 * (1 - u) * u * mx + u * u * x1, (1 - u) ** 2 * y0 + 2 * (1 - u) * u * my + u * u * y1); }
          c.n.stroke();
        }
      } }],
      caps: [
        chap('六', '秩序的自由市場', 0.6, 14.6),
        { t0: 1.4, t1: 14.6, style: 'quote', text: '*封建主義是秩序的自由市場*，\n資本主義則是秩序自由市場在民族國家取消武力競爭以後的殘餘。', src: '劉仲敬 Twitter', pos: 'top', y: 290, opt: { size: 50 } },
      ] },
    { id: 's7_manor', dur: 16, trans: TR, grade: { expo: 1.02 },
      cam: t => keys([[0, { x: 1100, y: H * 0.56, z: 1.12 }], [16, { x: 1500, y: H * 0.56, z: 1.12 }]], t, lin),
      sprites: (t, c) => { const [a, b] = c.meta.road, k = ease(prog(t, 7, 15)); return k > 0 ? [{ name: 'official', x: lerp(a[0], b[0], k), y: lerp(a[1], b[1], k), d: 0.45, scale: 0.8, after: 'mid' }] : []; },
      fx: [{ after: 'sky', draw: c => fx.stars(c, { n: 150, k: 0.7 }) }, { after: 'mid', draw: c => { fx.lamps(c, c.meta.lamps, 0.45, { t0: 0, t1: 1, k: 1.4 }); } }],
      caps: [
        chap('七', '凝結核', 0.6, 15.6, { color: 'paper' }),
        { t0: 1.4, t1: 7.6, style: 'quote', text: '紳士的凝結核作用，關鍵就在*掌握司法權*，至少是宗族習慣法。', src: '劉仲敬微信言論', color: 'paper', pos: 'top', y: 300 },
        { t0: 8, t1: 15.6, style: 'quote', text: '吏治國家靠流官進行統治，流官的真正任務是*削平土豪*，\n而土豪正是有機共同體的凝結核。', src: '數卷殘編', color: 'paper', pos: 'top', y: 290 },
      ] },
    { id: 's8_writ', dur: 15, trans: TR, grade: { warm: 0.25 },
      cam: t => keys([[0, { x: 1100, y: H * 0.54, z: 1.12 }], [15, { x: 1900, y: H * 0.54, z: 1.12 }]], t, lin),
      sprites: (t, c) => { const k = prog(t, 1, 12); return [{ name: `rider_${Math.floor(t * 7) % 4}`, x: lerp(500, c.meta.end, ease(k)), y: c.meta.ride_y, d: 0.45, scale: 0.6, after: 'mid' }]; },
      caps: [
        chap('八', '國王法庭', 0.6, 14.6),
        { t0: 1.4, t1: 14.6, style: 'quote', text: '你把國王法庭當成*爭取客戶的公司*……\n中世紀法庭必須陪著笑臉去爭取客戶。', src: DC, pos: 'top', y: 300 },
        { t0: 6, t1: 14, style: 'note', text: '令狀早上下，晚上給你解決了', x: 1500, y: 900, opt: { size: 38 } },
      ] },
    { id: 's9_jury', dur: 17, trans: TR, grade: { warm: 0.1 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.6, z: 1.14 }], [17, { x: W * 0.5, y: H * 0.6, z: 1.08 }]], t, lin),
      layers: { duel: t => ({ grow: lerp(-0.05, 1.08, ease(prog(t, 5, 10))), conceal: true, soft: 0.1 }), jury: t => ({ alpha: ease(prog(t, 5.5, 9.5)) }) },
      caps: [
        chap('九', '陪審團', 0.6, 16.6),
        { t0: 1.4, t1: 7.8, style: 'quote', text: '就是原先來觀看你*決鬥*的那些父老鄉親，現在變成*陪審團*了。', src: DC, pos: 'top', y: 300 },
        { t0: 8.2, t1: 16.6, style: 'quote', text: '法庭和陪審團是不是接受我的話，主要不看你收集了多少科學證據，\n而是要看，我這個人平時*在鄰居中間的名譽*好不好。', src: DC, pos: 'top', y: 290, opt: { size: 46, max: 1700 } },
      ] },
    { id: 's10_palace', dur: 15, trans: TR, grade: { warm: 0.3 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.52, z: 1.08 }], [15, { x: W * 0.5, y: H * 0.56, z: 1.18 }]], t, lin),
      layers: { facade: t => ({ grow: lerp(-0.05, 0.75, ease(prog(t, 5, 11))), conceal: true, soft: 0.12 }) },
      caps: [
        chap('十', '絕對主義的真相', 0.6, 14.6),
        { t0: 1.4, t1: 8, style: 'quote', text: '不如說絕對主義是一種*過渡狀態*，\n是封建主義瓦解過程中的一個過渡狀態', src: YD, pos: 'top', y: 290 },
        { t0: 8.4, t1: 14.6, style: 'quote', text: '如果你按法國標準去比較的話，那英國*根本就沒有絕對主義*', src: YD, pos: 'top', y: 300 },
        { t0: 9, t1: 14.4, style: 'note', text: '封建的梁架仍在底下', x: 520, y: 1060 },
      ] },
    { id: 's11_america', dur: 16, trans: TR, grade: { warm: 0.15 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.52, z: 1.06 }], [16, { x: W * 0.5, y: H * 0.6, z: 1.2 }]], t, lin),
      fx: [{ after: 'floor', draw: c => fx.godrays(c, 960, -100, { k: 0.4, n: 6, seed: 12 }) }],
      caps: [
        chap('十一', '沒有主權者的國家', 0.6, 15.6),
        { t0: 1.4, t1: 9.4, style: 'quote', text: '美國是一個*沒有主權者*的國家，這恰好是中世紀國家的特徵。\n中世紀國家是依靠法律和習慣建立起來的司法國，*司法就是最高政治*。', src: '《劉仲敬論基辛格》', pos: 'top', y: 290, opt: { size: 46, max: 1800 } },
        { t0: 9.8, t1: 15.6, style: 'quote', text: '法蘭西國王和聖殿騎士團打官司打了幾十年都沒有出結果。', src: '《劉仲敬論基辛格》', pos: 'top', y: 300 },
        { t0: 3, t1: 9, style: 'note', text: '空著的王座', x: 1460, y: 820, from: [1430, 840], at: [W * 0.5, H * 0.72, 0.4] },
      ] },
    { id: 's12_zhouqin', dur: 19, grade: { warm: 0.1 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.56, z: 1.08 }], [19, { x: W * 0.5, y: H * 0.56, z: 1.04 }]], t, lin),
      caps: [
        chap('十二', '周政與秦政', 0.6, 16),
        { t0: 1.4, t1: 8, style: 'quote', text: '「天下一人」（秦政）、抑或「諸侯之首」（周政），\n即楚漢間*憲法問題之首*。', src: '《劉仲敬文選》', pos: 'top', y: 290 },
        { t0: 8.4, t1: 16, style: 'quote', text: '周政的原始性是*自然演化*的早期階段，\n秦政的原始性則是*人為收割*造成的退化。', src: JY, pos: 'top', y: 290 },
        { t0: 3, t1: 15.6, style: 'note', text: '周政：諸侯之首', x: 480, y: 1060 },
        { t0: 4, t1: 15.6, style: 'note', text: '秦政：天下一人', x: 1640, y: 1060, color: 'paper' },
        { t0: 16.3, t1: 19, style: 'sub', text: '劉仲敬思想 · 其七《小路》', pos: 'center', wash: false },
      ] },
  ],
};
