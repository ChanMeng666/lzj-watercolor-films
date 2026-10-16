// 第十三部《宗族》— 家庭與小共同體
import { keys, ease, easeOut, easeIn, prog, clamp, lerp, hash } from '../lib/engine.js';
import * as fx from '../lib/fx.js';

const W = 2304, H = 1296, TR = 2, lin = x => x;
const P7 = '《劉仲敬訪談 007》', P8 = '《劉仲敬訪談 008》', P19 = '《劉仲敬訪談 019》', YD = '《文明更迭的源代碼》', AY = '《阿姨，我不想努力了》';
const chap = (num, text, t0, t1, o = {}) => ({ style: 'chapter', num, text, t0, t1, ...o });
const along = (pts, u) => { const n = pts.length - 1, f = clamp(u) * n, i = Math.min(Math.floor(f), n - 1), k = f - i; return [lerp(pts[i][0], pts[i + 1][0], k), lerp(pts[i][1], pts[i + 1][1], k)]; };

export default {
  title: '宗族',
  fadeIn: 1.5, fadeOut: 2.5,
  scenes: [
    { id: 's1_courtyard', dur: 16, trans: TR, grade: { warm: 0.1 },
      cam: t => keys([[0, { x: 1100, y: H * 0.55, z: 1.1 }], [16, { x: 1550, y: H * 0.6, z: 1.22 }]], t, lin),
      fx: [{ after: 'house', draw: c => fx.lamps(c, c.meta.lamps, 0.42, { t0: 0.5, t1: 1.5, k: 1.3 }) },
        { after: 'family', draw: c => fx.glowAt(c, c.meta.lamp, 0.42, 160, '255,214,140', 0.5 * (0.9 + 0.1 * Math.sin(c.t * 7))) },
        { draw: c => fx.rain(c, { n: 360, angle: 0.18, k: 0.8 }) }],
      caps: [
        { t0: 1.4, t1: 6.6, style: 'title', text: '宗族', pos: 'center', y: 330 },
        { t0: 2.5, t1: 6.6, style: 'sub', text: '劉仲敬思想 · 水彩短片 其十三 —— 家庭與小共同體', pos: 'center', y: 470, wash: false },
        chap('一', '家門之內', 7, 15.6, { color: 'paper' }),
        { t0: 7.4, t1: 15.6, style: 'quote', text: '我是一家之長，我跟外面的人雖然是這樣爾虞我詐，\n但是我跟我的子孫和表兄弟之類的，*內部還是相互維護的*', src: P7, color: 'paper', pos: 'top', y: 260, opt: { size: 48 } },
      ] },
    { id: 's2_split', dur: 15, trans: TR, grade: t => ({ sat: lerp(1, 0.55, prog(t, 3, 12)), warm: -0.1 }),
      cam: t => keys([[0, { x: 1270, y: H * 0.62, z: 1.3 }], [15, { x: 1270, y: H * 0.58, z: 1.08 }]], t, lin),
      layers: { roof: t => ({ dy: -easeIn(prog(t, 2, 7)) * 500, alpha: 1 - ease(prog(t, 3, 7)) }) },
      sprites: (t, c) => { const [cx, cy] = c.meta.center; return [0, 1, 2, 3, 4, 5].map(i => {
        const side = i % 2 ? 1 : -1, k = easeOut(prog(t, 4 + (i >> 1) * 0.6, 14)), off = 80 + (i >> 1) * 70;
        return { name: `walker_${i}`, x: cx + side * (off + k * 900), y: cy + (i >> 1) * 26, d: 0.45, scale: 0.75 - (i >> 1) * 0.06, flip: side < 0, alpha: 1 - 0.5 * k }; }); },
      caps: [
        chap('二', '最後一道屏障', 0.6, 14.6),
        { t0: 1.4, t1: 14.6, style: 'quote', text: '所有人都變成孤立的人，\n即使是*父子和夫妻之間也像是敵人一樣*相互對待了。', src: P7, pos: 'top', y: 270, opt: { size: 56 } },
      ] },
    { id: 's3_net', dur: 15, trans: TR, grade: { warm: 0.15 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.62, z: 1.18 }], [15, { x: W * 0.5, y: H * 0.6, z: 1.06 }]], t, lin),
      fx: [{ after: 'people', draw: c => { const v = c.view(0.4), N = c.meta.nodes;
        c.meta.edges.forEach(([i, j], e) => { const k = ease(prog(c.t, 2.5 + hash(e, 3) * 6, 3.5 + hash(e, 3) * 6)); if (k <= 0) return;
          const [x0, y0] = v.P(...N[i]), [x1, y1] = v.P(...N[j]);
          c.n.strokeStyle = `rgba(150,96,40,${0.8 * k})`; c.n.lineWidth = 2.6 * v.s; c.n.beginPath(); c.n.moveTo(x0, y0); c.n.lineTo(lerp(x0, x1, k), lerp(y0, y1, k)); c.n.stroke(); });
        const g = ease(prog(c.t, 9, 12)); N.forEach(p => fx.glowAt(c, p, 0.4, 40, '255,214,140', 0.35 * g)); } }],
      caps: [
        chap('三', '組織力', 0.6, 14.6),
        { t0: 1.4, t1: 14.6, style: 'quote', text: '無論是真宗族還是假宗族，\n重點在於*有沒有足夠的組織力*。', src: YD, pos: 'top', y: 250, opt: { size: 60 } },
        { t0: 9, t1: 14.4, style: 'note', text: '血緣不是網，網是自己織的', x: 1560, y: 1000, opt: { size: 34 } },
      ] },
    { id: 's4_lantern', dur: 16, trans: TR, grade: { warm: 0.25 },
      cam: t => keys([[0, { x: 1100, y: H * 0.6, z: 1.12 }], [16, { x: 1700, y: H * 0.52, z: 1.14 }]], t, lin),
      fx: [{ after: 'hill', draw: c => fx.glowAt(c, c.meta.top, 0.45, 260, '255,200,110', 0.6 * (0.9 + 0.1 * Math.sin(c.t * 6))) }],
      sprites: (t, c) => { const out = [], P = c.meta.path;
        for (let i = 0; i < 4; i++) { const u = clamp(0.08 + i * 0.16 + t * 0.045), [x, y] = along(P, u), g = ease(prog(u, 0.55, 0.85)), f = Math.floor(t * 3 + i) % 4;
          out.push({ name: `grey_${f}`, x, y: y + 6, d: 0.45, scale: 0.75, alpha: 1 - g, after: 'hill' }, { name: `gold_${f}`, x, y: y + 6, d: 0.45, scale: 0.75, alpha: g, after: 'hill' }); }
        const k = ease(prog(t, 9, 14)), a = ease(prog(t, 8.4, 9.2));
        out.push({ name: 'banner_0', x: 760 - k * 120, y: 300 + k * 60, rot: -0.15 * k, d: 0.45, alpha: a * (1 - 0.5 * k) }, { name: 'banner_1', x: 800 + k * 120, y: 300 + k * 90, rot: 0.2 * k, d: 0.45, alpha: a * (1 - 0.5 * k) });
        return out; },
      caps: [
        chap('四', '弄假成真', 0.6, 15.6),
        { t0: 1.4, t1: 8, style: 'quote', text: '他下面的人本來跟他一點關係也沒有，\n但到後來就*弄假成真*了。', src: YD, pos: 'top', y: 270, opt: { size: 56 } },
        { t0: 8.4, t1: 15.6, style: 'quote', text: '像孔融家族那樣的真宗族\n最後反而*自己人互相打起來*。', src: YD, pos: 'top', y: 270, opt: { size: 56 } },
        { t0: 3, t1: 7.8, style: 'note', text: '田疇與投奔他的人', at: [2120, 560], x: 1460, y: 640, opt: { size: 32 } },
      ] },
    { id: 's5_rice', dur: 15, trans: TR, grade: { warm: 0.3 },
      cam: t => keys([[0, { x: 1000, y: H * 0.62, z: 1.18 }], [15, { x: 1500, y: H * 0.62, z: 1.14 }]], t, lin),
      fx: [{ after: 'hall', draw: c => fx.lamps(c, c.meta.lamps, 0.42, { t0: 0.6, t1: 1.2, k: 1.4 }) }],
      sprites: (t, c) => { const u = ease(prog(t, 2, 12)), [x, y] = along(c.meta.hands, u); return [{ name: 'bowl', x, y: y - Math.abs(Math.sin(u * 40)) * 12, d: 0.42 }]; },
      caps: [
        chap('五', '天然的福利組織', 0.6, 14.6),
        { t0: 1.4, t1: 7.4, style: 'quote', text: '在小範圍之內談福利制度其實沒有意義，\n因為*小共同體天然就是福利組織*。', src: YD, pos: 'top', y: 270 },
        { t0: 7.8, t1: 14.6, style: 'quote', text: '為自己的祠堂打架的話，捨生忘死，不害怕任何犧牲，\n打傷打死了，*自己的共同體會照顧他*。', src: '《劉仲敬論家庭模式與生育率》', pos: 'top', y: 270, opt: { size: 48 } },
      ] },
    { id: 's6_banyan', dur: 15, trans: TR, grade: { warm: 0.1 },
      cam: t => keys([[0, { x: 1325, y: H * 0.7, z: 1.2 }], [15, { x: 1325, y: H * 0.64, z: 1.1 }]], t, lin),
      fx: [{ after: 'homes', draw: c => { fx.lamps(c, c.meta.lamps, 0.45, { t0: 2, t1: 7, k: 0.8 }); fx.motes(c, [1325, H * 0.5], 0.45, { n: 30, k: 0.6 }); } }],
      caps: [
        chap('六', '先有社區，後有家庭', 0.6, 14.6),
        { t0: 1.4, t1: 7.4, style: 'quote', text: '真正重要的從來就不是經濟，\n真正重要的從來都是*小共同體*。', src: P19, pos: 'top', y: 500, opt: { size: 50 } },
        { t0: 7.8, t1: 14.6, style: 'quote', text: '*家庭關係的構建方式*是取決於*社區的構建方式*的。', src: AY, pos: 'top', y: 500, opt: { size: 50 } },
      ] },
    { id: 's7_wedding', dur: 13, trans: TR, grade: { warm: 0.25 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.56, z: 1.12 }], [13, { x: W * 0.5, y: H * 0.58, z: 1.04 }]], t, lin),
      fx: [{ after: 'table', draw: c => { const v = c.view(0.4), [a, b] = c.meta.crests, k = ease(prog(c.t, 2, 6));
        const [x0, y0] = v.P(...a), [x1, y1] = v.P(...b), mx = (x0 + x1) / 2, my = y0 + 160 * v.s;
        c.n.strokeStyle = 'rgba(196,40,36,0.9)'; c.n.lineWidth = 12 * v.s; c.n.lineCap = 'round'; c.n.beginPath();
        for (let i = 0; i <= 40 * k; i++) { const u = i / 40, x = (1 - u) ** 2 * x0 + 2 * u * (1 - u) * mx + u * u * x1, y = (1 - u) ** 2 * y0 + 2 * u * (1 - u) * my + u * u * y1 + Math.sin(u * 12 + c.t * 2) * 6 * v.s;
          i ? c.n.lineTo(x, y) : c.n.moveTo(x, y); } c.n.stroke();
        [a, b].forEach(p => fx.glowAt(c, p, 0.4, 150, '255,220,150', 0.35)); } }],
      caps: [
        chap('七', '婚姻是聯盟', 0.6, 12.6),
        { t0: 1.4, t1: 12.6, style: 'quote', text: '市井婚姻與王室婚姻同，均以*利益聯盟*為主，\n感情性愛皆居其次', src: '《劉仲敬豆瓣言論》', pos: 'top', y: 430, opt: { size: 54 } },
      ] },
    { id: 's8_soil', dur: 15, trans: TR, grade: { warm: 0.15 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.58, z: 1.1 }], [15, { x: W * 0.56, y: H * 0.6, z: 1.16 }]], t, lin),
      sprites: (t, c) => { const S = c.meta.spots, out = [];
        [[0.8, 0], [3.4, 1], [6, 2]].forEach(([t0, i]) => { const e = t - t0; if (e < 0 || e > 2.4) return; const [x, y] = S[i], k = clamp(e / 1.2);
          out.push({ name: 'seed', x: x + (i - 1) * 40 * (1 - k), y: lerp(100, y - 10, easeIn(k)) - (k >= 1 ? Math.max(0, Math.sin((e - 1.2) * 6)) * 30 * (i < 2 ? 1 : 0) : 0), rot: e * 3, d: 0.4, alpha: i < 2 ? 1 - ease(prog(e, 1.6, 2.4)) : 1 - ease(prog(e, 2, 2.4)) }); });
        const g = ease(prog(t, 8, 12)); if (g > 0) out.push({ name: 'sprout', x: S[2][0], y: S[2][1] + 4, d: 0.4, scale: 0.15 + 0.95 * g });
        return out; },
      fx: [{ after: 'soils', draw: c => fx.glowAt(c, [W * 0.86, H * 0.44], 0.4, 180, '255,230,170', 0.35 * ease(prog(c.t, 8, 10))) }],
      caps: [
        chap('八', '投胎', 0.6, 14.6),
        { t0: 1.4, t1: 7.4, style: 'quote', text: '你必須得投胎投在一個良好的、*價值觀堅定*、\n性格比較好的家庭裡面', src: AY, pos: 'top', y: 300, opt: { size: 52 } },
        { t0: 7.8, t1: 14.6, style: 'quote', text: '一個人的錯誤選擇影響到自己的比較少，\n*影響到他子孫後代的比較多*', src: P7, pos: 'top', y: 300, opt: { size: 52 } },
      ] },
    { id: 's9_jar', dur: 15, trans: TR, grade: t => ({ warm: 0.1, expo: lerp(1.02, 0.92, prog(t, 4, 15)) }),
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.6, z: 1.2 }], [15, { x: W * 0.52, y: H * 0.56, z: 1.08 }]], t, lin),
      fx: [{ after: 'jar', draw: c => { const v = c.view(0.4), [lx, ly] = c.meta.leak, k = ease(prog(c.t, 2, 3.5));
        for (let j = 0; j < 22; j++) { const ph = (c.t * 1.2 + j / 22) % 1, [x, y] = v.P(lx + ph * 60, ly + ph * ph * 260);
          c.n.fillStyle = `rgba(245,240,226,${0.85 * k * (1 - ph)})`; c.n.beginPath(); c.n.arc(x, y, 5 * v.s, 0, Math.PI * 2); c.n.fill(); }
        fx.smoke(c, [c.meta.steam], 0.4, { k: 0.6 }); } }],
      sprites: (t, c) => { const [sx, sy] = c.meta.steam; return [0, 1, 2].map(i => { const e = t - 6 - i * 1.6, a = ease(prog(e, 0, 1)) * (1 - ease(prog(e, 2, 4.5)));
        return { name: `face_${i}`, x: sx + (i - 1) * 200, y: sy - 80 - e * 40, d: 0.4, alpha: Math.max(0, a) * 0.85, scale: 0.9 }; }); },
      caps: [
        chap('九', '吃子孫飯', 0.6, 14.6),
        { t0: 1.4, t1: 7.6, style: 'quote', text: '你每一次逃避和後退，你都是要麼*消費祖先的遺德*，\n要麼*把你的子孫給預支了*。', src: P7, pos: 'top', y: 260, opt: { size: 50 } },
        { t0: 8, t1: 14.6, style: 'quote', text: '在他的子孫出生以前，\n他就開始*吃自己的子孫*了。', src: P19, pos: 'top', y: 260, opt: { size: 58 } },
      ] },
    { id: 's10_generations', dur: 15, trans: TR, grade: { warm: -0.05 },
      cam: t => keys([[0, { x: 1000, y: H * 0.6, z: 1.12 }], [15, { x: 2000, y: H * 0.6, z: 1.12 }]], t, lin),
      fx: [{ after: 'mid', draw: c => c.meta.gens.forEach((g, i) => fx.glowAt(c, [g[0], g[1] - 120], 0.45, 160, '255,236,190', 0.25 * ease(prog(c.t, 1 + i * 1.5, 2.5 + i * 1.5)))) },
        { after: 'estate', draw: c => fx.lamps(c, c.meta.lamps, 0.45, { t0: 9, t1: 11, k: 1.2 }) },
        { draw: c => fx.snow(c, { n: 200, k: ease(prog(c.t, 7, 10)) }) }],
      caps: [
        chap('十', '第三代、第四代', 0.6, 14.6),
        { t0: 1.4, t1: 7.6, style: 'quote', text: '你要能夠發揮作用，一般來說是*第三代、第四代*的事情，\n第二代都是很懸的。', src: AY, pos: 'top', y: 270, opt: { size: 50 } },
        { t0: 8, t1: 14.6, style: 'quote', text: '地主比起資本家來說，是更好和更可靠的*凝結核*，\n他必須*為幾代人的子孫考慮*', src: AY, pos: 'top', y: 270, opt: { size: 50 } },
      ] },
    { id: 's11_backstage', dur: 15, trans: TR, grade: { warm: 0.2 },
      cam: t => keys([[0, { x: W * 0.6, y: H * 0.5, z: 1.14 }], [15, { x: W * 0.36, y: H * 0.56, z: 1.2 }]], t, lin),
      fx: [{ after: 'stage', draw: c => fx.godrays(c, ...c.view(0.3).P(...c.meta.spot), { k: 0.5, n: 6, len: 900 }) },
        { after: 'wings', draw: c => fx.glowAt(c, c.meta.child, 0.5, 120, '255,220,160', 0.35 * ease(prog(c.t, 6, 8))) }],
      caps: [
        chap('十一', '後台的人', 0.6, 14.6, { color: 'paper' }),
        { t0: 1.4, t1: 7.6, style: 'quote', text: '你瞞得過台下的觀眾，瞞不過後台的人。\n*小孩就是後台的人*。', src: AY, color: 'paper', pos: 'bottom', y: 1000, opt: { size: 54 } },
        { t0: 8, t1: 14.6, style: 'quote', text: '母親和小孩之間的關係\n就像是*她和她的一個器官*的關係。', src: AY, color: 'paper', pos: 'bottom', y: 1000, opt: { size: 54 } },
      ] },
    { id: 's12_rebuild', dur: 19, grade: t => ({ warm: lerp(-0.1, 0.35, prog(t, 7, 13)), sat: lerp(0.8, 1.05, prog(t, 7, 13)) }),
      cam: t => keys([[0, { x: 900, y: H * 0.56, z: 1.14 }], [6, { x: 900, y: H * 0.56, z: 1.14 }], [12, { x: 1950, y: H * 0.58, z: 1.12 }], [19, { x: 1950, y: H * 0.56, z: 1.04 }]], t, ease),
      fx: [{ after: 'village', draw: c => fx.lamps(c, c.meta.lamps, 0.45, { t0: 9, t1: 15, k: 1.0, order: i => i / c.meta.lamps.length }) }],
      caps: [
        chap('十二', '重建小共同體', 0.6, 16.6),
        { t0: 1.4, t1: 6.4, style: 'quote', text: '這種內卷化的教育很不幸卻是虎媽和儒家文化型和漢字文化型的優秀父母的不二法門，\n他們用這種方法*坑死了他們的下一代*。', src: P8, pos: 'top', y: 270, opt: { size: 42, max: 1800 } },
        { t0: 6.6, t1: 10.6, style: 'quote', text: '中華夢的主角恰好相反，\n應該比其他人更擅長*自我剝削*', src: '《劉仲敬論錢穆 · 中華夢》', pos: 'top', y: 270, opt: { size: 54 } },
        { t0: 11, t1: 16.6, style: 'quote', text: '這個*能夠積累的環境*\n比起你事先帶去的任何東西都寶貴。', src: P7, pos: 'top', y: 270, opt: { size: 56 } },
        { t0: 16.8, t1: 19, style: 'sub', text: '劉仲敬思想 · 其十三《宗族》', pos: 'center', wash: false },
      ] },
  ],
};
