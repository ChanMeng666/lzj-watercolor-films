// 第九部《黑匣子》— 三代文明、內亞海洋、種子庫
import { keys, ease, easeOut, easeIn, prog, clamp, lerp, hash } from '../lib/engine.js';
import * as fx from '../lib/fx.js';

const W = 2304, H = 1296, TR = 2, lin = x => x;
const YD = '《文明更迭的源代碼》', WD = '《中國窪地》';
const chap = (num, text, t0, t1, o = {}) => ({ style: 'chapter', num, text, t0, t1, ...o });

export default {
  title: '黑匣子',
  fadeIn: 1.5, fadeOut: 2.5,
  scenes: [
    { id: 's1_ignite', dur: 15, trans: TR, grade: { warm: 0.35 },
      cam: t => keys([[0, { x: 1000, y: H * 0.5, z: 1.14 }], [15, { x: 1800, y: H * 0.5, z: 1.1 }]], t, lin),
      fx: [{ after: 'mid', draw: c => c.meta.chain.forEach((p, i) => { const k = ease(prog(c.t, 2 + i * 1.1, 3 + i * 1.1)); if (k > 0) { fx.glowAt(c, p, 0.45, 160, '255,200,120', 0.5 * k); fx.fire(c, p, 0.45, { size: 0.25, k }); } }) }],
      caps: [
        { t0: 1.4, t1: 6.6, style: 'title', text: '黑匣子', pos: 'center', y: 400 },
        { t0: 2.5, t1: 6.6, style: 'sub', text: '劉仲敬思想 · 水彩短片 其九 —— 三代文明與種子庫', pos: 'center', y: 540, wash: false },
        chap('一', '同一個起火點', 7, 14.6),
        { t0: 7.4, t1: 14.6, style: 'quote', text: '世界其他地方的文明都是直接或間接地\n在*西亞第一代文明*的刺激下產生的。', src: '《劉仲敬論巴蜀利亞民族發明學》', pos: 'top', y: 290 },
      ] },
    { id: 's2_wave', dur: 14, trans: TR, grade: { sat: 0.85 },
      cam: t => keys([[0, { x: W * 0.55, y: H * 0.56, z: 1.1 }], [14, { x: W * 0.5, y: H * 0.5, z: 1.06 }]], t, lin),
      layers: { wave: t => ({ dx: lerp(2700, -100, easeOut(prog(t, 2, 10))) }) },
      sprites: (t, c) => [0, 1, 2, 3, 4].map(i => ({ name: `rider_${Math.floor(t * 7 + i) % 4}`, x: lerp(2700, -100, easeOut(prog(t, 2, 10))) + 200 + i * 420, y: H * 0.44 + (i % 2) * 30, d: 0.5, scale: 0.55, flip: true, after: 'wave' })),
      caps: [
        chap('二', '大洪水', 0.6, 13.6),
        { t0: 1.4, t1: 13.4, style: 'quote', text: '對於當時的世界來說，印歐蠻族入侵就是一場*「大洪水」*，\n把過去埃及和兩河流域已經進入晚期的文明*徹底洗蕩乾淨*。', src: YD, pos: 'top', y: 260, opt: { size: 46, max: 1800 } },
      ] },
    { id: 's3_blackbox', dur: 16, trans: TR, grade: { warm: 0.3 },
      cam: t => keys([[0, { x: W * 0.55, y: H * 0.42, z: 1.08 }], [16, { x: W * 0.6, y: H * 0.6, z: 1.2 }]], t, lin),
      sprites: (t, c) => { const k = easeIn(prog(t, 1.5, 6)); const [bx, by] = c.meta.box;
        return [{ name: 'blackbox', x: lerp(bx - 900, bx, k), y: lerp(-150, by, k), d: 0.45, rot: (1 - k) * 8, scale: 1.2, alpha: 1 - prog(t, 7, 8) }]; },
      fx: [{ draw: c => { const v = c.view(0.45), [bx, by] = c.meta.box;
        for (let i = 0; i < 26; i++) { const tt = c.t - i * 0.1; if (tt < 1.5 || tt > 6) continue; const k = easeIn(prog(tt, 1.5, 6));
          const [x, y] = v.P(lerp(bx - 900, bx, k), lerp(-150, by, k)); fx.glow(c.n, x, y - 10, 30 + i * 4, '60,56,60', 0.25 * (1 - i / 26)); fx.glow(c.a, x, y, 40, '255,150,60', 0.4 * (1 - i / 26)); }
        fx.ripple(c, [bx, by + 140], 0.45, 6); } }],
      caps: [
        chap('三', '黑匣子', 0.6, 15.6),
        { t0: 1.4, t1: 7.6, style: 'quote', text: '希伯來正典是人類第一代文明的*唯一繼承者*，\n它更接近於文明種子基因庫的角色', src: YD, pos: 'top', y: 290 },
        { t0: 8, t1: 15.6, style: 'quote', text: '在飛機快要墜毀的時候，負責保存最寶貴資訊的*黑匣子*就被拋出去了。\n後來人的解讀可能不見得正確，但這是*有跡可尋的唯一線索*。', src: YD, pos: 'top', y: 280, opt: { size: 46, max: 1800 } },
      ] },
    { id: 's4_ten', dur: 15, trans: TR, grade: { warm: 0.2 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.62, z: 1.1 }], [15, { x: W * 0.5, y: H * 0.6, z: 1.2 }]], t, lin),
      fx: [{ after: 'mid', draw: c => fx.glowAt(c, c.meta.scholar, 0.45, 220, '255,226,160', 0.45 * ease(prog(c.t, 3, 5))) }],
      caps: [
        chap('四', '保種是一筆重稅', 0.6, 14.6),
        { t0: 1.4, t1: 6.4, style: 'quote', text: '對於他們自己的共同體來說，是個*極其殘酷而又沉重的負擔*。', src: YD, pos: 'top', y: 300 },
        { t0: 6.8, t1: 14.6, style: 'quote', text: '猶太社會沒有祭司、武士等角色，也不建立國家，……\n把*十分之一的人口*都培養成學生，專門負責保存典籍', src: YD, pos: 'top', y: 290 },
      ] },
    { id: 's5_capsule', dur: 15, trans: TR, grade: { expo: 1.04 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.5, z: 1.1 }], [15, { x: W * 0.5, y: H * 0.5, z: 1.2 }]], t, lin),
      sprites: (t, c) => { const o = ease(prog(t, 5, 8)) * 200, out = [
        { name: 'cap_0', x: W * 0.5 - o, y: H * 0.5, d: 0.3, rot: -o / 900 }, { name: 'cap_1', x: W * 0.5 + o, y: H * 0.5, d: 0.3, rot: o / 900 }];
        if (t > 6) out.push({ name: 'seed', x: W * 0.5, y: H * 0.5 + ease(prog(t, 9, 12)) * 260, d: 0.3, scale: 1.2, alpha: ease(prog(t, 6, 7)) });
        if (t > 12) out.push({ name: 'sprout', x: W * 0.5, y: H * 0.5 + 300, d: 0.3, scale: 0.4 + 0.5 * ease(prog(t, 12, 15)), alpha: ease(prog(t, 12, 13)) });
        return out; },
      fx: [{ after: 'space', draw: c => { fx.stars(c, { n: 200, k: 0.8, ymax: 1 }); fx.glowAt(c, [W * 0.5, H * 0.5], 0.3, 400, '255,240,200', 0.4 * ease(prog(c.t, 6, 8))); } }],
      caps: [
        chap('五', '壓縮膠囊', 0.6, 14.6, { color: 'paper' }),
        { t0: 1.4, t1: 14.6, style: 'quote', text: '這有點像是宇航員吃的*太空食品*，把最為主要的營養成分存放在一個膠囊裏面，\n占的空間盡可能小。', src: YD, color: 'paper', pos: 'bottom', y: 960, opt: { size: 46, max: 1800 } },
      ] },
    { id: 's6_ark', dur: 16, trans: TR, grade: { sat: 0.8, warm: -0.05 },
      cam: t => keys([[0, { x: 1300, y: H * 0.5, z: 1.12 }], [16, { x: 1500, y: H * 0.5, z: 1.12 }]], t, lin),
      sprites: (t, c) => [{ name: 'ark', x: 1100 + t * 30, y: H * 0.72 + Math.sin(t * 1.4) * 10, rot: Math.sin(t * 1.1) * 0.03, d: 0.3, scale: 1 }],
      fx: [{ draw: c => fx.rain(c, { n: 260, k: 0.6, angle: 0.15 }) }],
      caps: [
        chap('六', '方舟', 0.6, 15.6),
        { t0: 1.4, t1: 8, style: 'quote', text: '這粒孤零零的種子像*諾亞方舟*一樣漂泊在洪水之上，\n然後等著洪水退去後出現新的沃土。', src: YD, pos: 'top', y: 290 },
        { t0: 8.4, t1: 15.6, style: 'quote', text: '當嚴冬來臨的時候人們就會發現，跟初期的情況一樣，\n又是*只有種子能夠存活下來*，負責保護文明基因。', src: YD, pos: 'top', y: 290 },
      ] },
    { id: 's7_grassea', dur: 17, trans: TR, grade: { warm: 0.1 },
      cam: t => keys([[0, { x: 1200, y: H * 0.5, z: 1.12 }], [17, { x: 2100, y: H * 0.5, z: 1.12 }]], t, lin),
      sprites: (t, c) => [0, 1, 2, 3, 4].map(i => ({ name: `camel_${Math.floor(t * 4 + i) % 4}`, x: 300 + i * 260 + t * 120, y: H * 0.7 + Math.sin(t * 2 + i) * 8 + (i % 2) * 20, d: 0.35, scale: 0.6 })),
      caps: [
        chap('七', '陸地上的海洋', 0.6, 16.6),
        { t0: 1.4, t1: 6.6, style: 'quote', text: '如果我們把內亞大草原看成一個*陸地上的海洋*、一個流動性的通道', src: WD, pos: 'top', y: 300 },
        { t0: 7, t1: 16.6, style: 'quote', text: '內亞的船隻（駱駝商隊）*在北京登陸上岸*，\n就像英國人的船隻在上海和廣州卸貨一樣。', src: WD, pos: 'top', y: 290 },
        { t0: 9, t1: 16.4, style: 'note', text: '港口', x: 1700, y: 600 },
      ] },
    { id: 's8_english', dur: 14, trans: TR, grade: { warm: 0.3 },
      cam: t => keys([[0, { x: 1300, y: H * 0.56, z: 1.1 }], [14, { x: 1600, y: H * 0.56, z: 1.1 }]], t, lin),
      sprites: (t, c) => [0, 1, 2, 3, 4, 5].map(i => ({ name: `rider_${Math.floor(t * 7 + i) % 4}`, x: -400 + i * 330 + t * 260, y: c.meta.ride_y + (i % 3) * 40, d: 0.45, scale: 0.6 + 0.06 * (i % 3) })),
      caps: [
        chap('八', '英國人以前的英國人', 0.6, 13.6),
        { t0: 1.4, t1: 13.4, style: 'quote', text: '蒙古部落不是郭嵩燾他們想像的那些野蠻人，\n他們是*英國人以前的英國人*。', src: WD, pos: 'top', y: 290, opt: { size: 60 } },
      ] },
    { id: 's9_germanic', dur: 17, trans: TR, grade: { warm: 0.05 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.6, z: 1.18 }], [17, { x: W * 0.5, y: H * 0.48, z: 1.08 }]], t, lin),
      layers: { cathedral: t => ({ grow: lerp(-0.02, 1.02, ease(prog(t, 3, 12))), soft: 0.06 }) },
      fx: [{ draw: c => { const v = c.view(0.45), [sx, sy] = c.meta.seed; const k = easeIn(prog(c.t, 0.5, 2.4));
        if (c.t < 3) { const [x, y] = v.P(sx, lerp(-100, sy, k)); c.n.fillStyle = 'rgba(120,80,50,0.95)'; c.n.beginPath(); c.n.ellipse(x, y, 12, 8, 0.4, 0, Math.PI * 2); c.n.fill(); }
        fx.ripple(c, [sx, sy], 0.45, 2.4, { col: '200,170,120' }); fx.godrays(c, 960, -100, { k: 0.4 * ease(prog(c.t, 8, 12)), seed: 4 }); } }],
      caps: [
        chap('九', '蠻族的沃土', 0.6, 16.6),
        { t0: 1.4, t1: 8.4, style: 'quote', text: '這個載體必須是一個「營養」足夠豐富、屬於原始豐饒的沃土，\n*雅利安和日耳曼蠻族*剛好提供了這個條件。', src: YD, pos: 'top', y: 280, opt: { size: 48 } },
        { t0: 8.8, t1: 16.6, style: 'quote', text: '也可以假定英美做為第三波文明的核心區，在遙遠的未來也會變成消耗殆盡的地方，\n然後更未來的文明核心應該是出現在*新邊疆*。', src: YD, pos: 'top', y: 280, opt: { size: 44, max: 1850 } },
      ] },
    { id: 's10_desert', dur: 16, trans: TR, grade: { warm: 0.2 },
      cam: t => keys([[0, { x: W * 0.36, y: H * 0.56, z: 1.16 }], [16, { x: W * 0.66, y: H * 0.56, z: 1.16 }]], t, lin),
      layers: { cells: t => ({ grow: lerp(-0.05, 1.08, ease(prog(t, 5.5, 10.5))), conceal: true, soft: 0.1 }) },
      fx: [{ after: 'north', draw: c => fx.lamps(c, c.meta.hut, 0.4, { t0: 9, t1: 9.1, k: 1.2 }) }],
      caps: [
        chap('十', '虔誠勝過神學', 0.6, 15.6),
        { t0: 1.4, t1: 6.8, style: 'quote', text: '日耳曼蠻族的理論肯定講不過埃及人，\n但是他們的信仰*肯定要虔誠得多*。', src: YD, pos: 'top', y: 290 },
        { t0: 7.2, t1: 12, style: 'quote', text: '埃及沙漠裏有幾千個隱修會，……但是穆斯林殺過來以後，埃及還剩多少基督徒呢？\n*連人口的十分之一都不到*。', src: YD, pos: 'top', y: 280, opt: { size: 44, max: 1850 } },
        { t0: 12.4, t1: 15.6, style: 'quote', text: '憑一個人的著作來判斷他的重要性，這是*知識分子的標準*', src: YD, pos: 'top', y: 300 },
      ] },
    { id: 's11_honeycomb', dur: 15, trans: TR, grade: { warm: 0.15 },
      cam: t => keys([[0, { x: W * 0.36, y: H * 0.5, z: 1.2 }], [15, { x: W * 0.62, y: H * 0.5, z: 1.1 }]], t, lin),
      caps: [
        chap('十一', '私智算不過演化', 0.6, 14.6),
        { t0: 1.4, t1: 7.4, style: 'quote', text: '因為蜜蜂那一套是經過*達爾文演化*選擇出來的，\n是經過反覆淘汰後剩下的最優選', src: YD, pos: 'bottom', y: 1000 },
        { t0: 7.8, t1: 14.6, style: 'quote', text: '就像算命先生給你算命、老中醫給你看病，他看你的氣色和脈象，\n氣色和脈象是不斷變化的，所以他要*不斷地修改預言*。', src: YD, pos: 'bottom', y: 990, opt: { size: 46, max: 1800 } },
        { t0: 2.5, t1: 7.2, style: 'note', text: '蜂巢', x: 420, y: 160 },
        { t0: 3.5, t1: 7.2, style: 'note', text: '用中學數學設計的蜂巢', x: 1640, y: 220 },
      ] },
    { id: 's12_islands', dur: 19, grade: { warm: 0.15 },
      cam: t => keys([[0, { x: 1200, y: H * 0.56, z: 1.14 }], [19, { x: 1700, y: H * 0.54, z: 1.06 }]], t, lin),
      fx: [{ after: 'sea', draw: c => c.meta.vents.forEach((p, i) => fx.smoke(c, [p], 0.3, { k: 1.4, seed: i * 5 })) }],
      caps: [
        chap('十二', '孤島與蒸汽', 0.6, 16.2),
        { t0: 1.4, t1: 7.8, style: 'quote', text: '不管後人的理論講得多玄，最初那個點，那個島，\n仍然是它*真正的基本盤*', src: YD, pos: 'top', y: 290 },
        { t0: 8.2, t1: 16.2, style: 'quote', text: '滅絕和替代可以釋放更多的可能性，世界上很少有死亡解決不了的問題。\n而*希望的種子*，更可能保留在小團體裏面。', src: YD, pos: 'top', y: 280, opt: { size: 46, max: 1800 } },
        { t0: 16.4, t1: 19, style: 'sub', text: '劉仲敬思想 · 其九《黑匣子》', pos: 'center', wash: false },
      ] },
  ],
};
