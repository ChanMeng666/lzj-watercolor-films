// 第八部《血酬》— 武德、撫卹金、土豪與逆淘汰
import { keys, ease, easeOut, easeIn, prog, clamp, lerp, hash } from '../lib/engine.js';
import * as fx from '../lib/fx.js';

const W = 2304, H = 1296, TR = 2, lin = x => x;
const TW = '劉仲敬 Twitter', CB = '數卷殘編', JY = '《經與史》', AY = '《阿姨，我不想努力了》';
const chap = (num, text, t0, t1, o = {}) => ({ style: 'chapter', num, text, t0, t1, ...o });

export default {
  title: '血酬',
  fadeIn: 1.5, fadeOut: 2.5,
  scenes: [
    { id: 's1_two', dur: 15, trans: TR, grade: { warm: 0.25 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.5, z: 1.08 }], [15, { x: W * 0.5, y: H * 0.54, z: 1.16 }]], t, lin),
      fx: [{ after: 'mid', draw: c => { fx.lamps(c, c.meta.lamps.slice(0, -1), 0.45, { t0: 6, t1: 9, k: 0.8 }); fx.fire(c, c.meta.tower, 0.45, { size: 0.45, k: ease(prog(c.t, 7, 8)) }); } }],
      caps: [
        { t0: 1.4, t1: 6.6, style: 'title', text: '血酬', pos: 'center', y: 400 },
        { t0: 2.5, t1: 6.6, style: 'sub', text: '劉仲敬思想 · 水彩短片 其八 —— 武德、撫卹金與土豪', pos: 'center', y: 540, wash: false },
        chap('一', '自組織能力與統治者', 7, 14.6),
        { t0: 7.4, t1: 14.6, style: 'quote', text: '誰的社會自組織能力最差，\n誰就會得到*最殘暴的統治者*。', src: TW, pos: 'top', y: 290, opt: { size: 60 } },
      ] },
    { id: 's2_shield', dur: 16, trans: TR, grade: { expo: 1.02 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.6, z: 1.12 }], [16, { x: W * 0.5, y: H * 0.62, z: 1.2 }]], t, lin),
      fx: [{ after: 'sky', draw: c => fx.stars(c, { n: 150, k: 0.7 }) }, { after: 'mid', draw: c => fx.fire(c, c.meta.fire, 0.45, { size: 1.0 }) }],
      caps: [
        chap('二', '主權來自武力', 0.6, 15.6, { color: 'paper' }),
        { t0: 1.4, t1: 7.4, style: 'quote', text: '部落戰士才是標準，*武德產生統治權力*（不同於自然權利），非常接近歷史。', src: '劉仲敬豆瓣言論', color: 'paper', pos: 'top', y: 300, opt: { size: 48 } },
        { t0: 7.8, t1: 15.6, style: 'quote', text: '主權來自武力，而非勞動。共和國主權屬於公民戰士，福利源於撫恤金或*血酬*。\n公民可以不勞動，但*不能不戰鬥*。', src: CB, color: 'paper', pos: 'top', y: 290, opt: { size: 46, max: 1800 } },
      ] },
    { id: 's3_widow', dur: 14, trans: TR, grade: { sat: 0.85 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.56, z: 1.16 }], [14, { x: W * 0.5, y: H * 0.56, z: 1.08 }]], t, lin),
      fx: [{ after: 'mid', draw: c => fx.glowAt(c, c.meta.purse, 0.45, 120, '255,220,150', 0.4 * ease(prog(c.t, 4, 6))) }],
      caps: [
        chap('三', '撫卹金', 0.6, 13.6),
        { t0: 1.4, t1: 13.4, style: 'quote', text: '武士要幹什麼？你打仗可能犧牲，然後你的家屬要拿*撫恤金*。\n否則的話，*軍隊是沒有辦法組織的*。', src: '《劉仲敬訪談 090》', pos: 'top', y: 300 },
      ] },
    { id: 's4_queen', dur: 14, trans: TR, grade: { warm: 0.2 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.5, z: 1.06 }], [14, { x: W * 0.5, y: H * 0.56, z: 1.16 }]], t, lin),
      caps: [
        chap('四', '女王的賬本', 0.6, 13.6),
        { t0: 1.4, t1: 13.4, style: 'quote', text: '打起仗來，你們倫敦商人會發財，\n我可是要*付撫恤金*的。', src: '伊莉莎白一世語，見《劉仲敬訪談 056》', pos: 'bottom', y: 960, opt: { size: 60 } },
        { t0: 3, t1: 13, style: 'note', text: '商人的船', x: 380, y: 860 },
        { t0: 5, t1: 13, style: 'note', text: '戰士的墳', x: 1700, y: 860 },
      ] },
    { id: 's5_banner', dur: 16, trans: TR, grade: t => ({ warm: 0.3, expo: lerp(1.0, 0.9, prog(t, 6, 15)) }),
      cam: t => keys([[0, { x: 1100, y: H * 0.54, z: 1.14 }], [16, { x: 1500, y: H * 0.54, z: 1.1 }]], t, lin),
      sprites: (t, c) => [0, 1, 2, 3].map(i => {
        const k = ease(prog(t, 4 + i * 2, 10 + i * 2));
        return { name: `follower_${Math.floor(t * 2.6 + i) % 4}`, x: lerp(c.meta.door[0] + 100 + i * 60, c.meta.away[0], k), y: lerp(c.meta.door[1] + 40, c.meta.away[1], k), d: 0.45, scale: 0.75, after: 'mid' };
      }),
      fx: [{ after: 'mid', draw: c => fx.lamps(c, c.meta.lamps, 0.45, { t0: -2, t1: -1, off: [8, 14], seed: 2 }) }],
      caps: [
        chap('五', '政黨的真實功能', 0.6, 15.6),
        { t0: 1.4, t1: 15.6, style: 'quote', text: '你可以有沖天的意識形態理想，但如果你*拿不出錢來發撫卹金*，也無法給自己的追隨者謀到官職，\n那麼放心，你的追隨者大學畢業*五年後就會拋棄你*。', src: '《劉仲敬論民國第三大黨中國青年黨》', pos: 'top', y: 290, opt: { size: 44, max: 1800 } },
      ] },
    { id: 's6_wolves', dur: 16, trans: TR, grade: { warm: 0.05 },
      cam: t => keys([[0, { x: 1300, y: H * 0.54, z: 1.12 }], [16, { x: 1500, y: H * 0.56, z: 1.12 }]], t, lin),
      caps: [
        chap('六', '勇敢與公正', 0.6, 15.6),
        { t0: 1.4, t1: 8, style: 'quote', text: '勇敢和公正，只需要這兩者就行了。\n能夠勇敢，*讓敵人怕你*；能夠公正，*讓自己人服你*', src: AY, pos: 'top', y: 290, opt: { size: 54 } },
        { t0: 8.4, t1: 15.6, style: 'quote', text: '你用嚴厲的公正去懲罰別人，\n得罪的是少數，贏得的擁護是大多數', src: AY, pos: 'top', y: 290 },
      ] },
    { id: 's7_fort', dur: 17, trans: TR, grade: { warm: 0.25 },
      cam: t => keys([[0, { x: W * 0.4, y: H * 0.54, z: 1.14 }], [17, { x: W * 0.55, y: H * 0.52, z: 1.08 }]], t, lin),
      layers: { fort: t => ({ grow: lerp(-0.02, 0.95, ease(prog(t, 2, 11))), soft: 0.08 }) },
      fx: [{ after: 'mid', draw: c => { c.meta.militia.forEach((p, i) => fx.glowAt(c, [p[0] + 30, p[1] - 120], 0.45, 70, '255,200,120', 0.6 * ease(prog(c.t, 9 + i * 0.4, 10 + i * 0.4))));
        fx.lamps(c, c.meta.lamps, 0.45, { t0: 11, t1: 12, k: 0.9 }); } }],
      caps: [
        chap('七', '土豪與民兵', 0.6, 16.6),
        { t0: 1.4, t1: 8.8, style: 'quote', text: '小地方的小地主土豪由於形勢的原因不得不組織各種自衛團體，有了一定的並不是很強的武力，\n漸漸做大以後最後形成的*自發秩序*。', src: '《劉仲敬訪談 020》', pos: 'top', y: 290, opt: { size: 44, max: 1800 } },
        { t0: 9.2, t1: 16.6, style: 'quote', text: '*民兵就是自由秩序的完整版雛形*，例如美國建國前夜。', src: TW, pos: 'top', y: 300 },
      ] },
    { id: 's8_salt', dur: 16, trans: TR, grade: { warm: 0.1 },
      cam: t => keys([[0, { x: W * 0.42, y: H * 0.56, z: 1.14 }], [16, { x: W * 0.62, y: H * 0.5, z: 1.14 }]], t, lin),
      caps: [
        chap('八', '用鹽買下武力', 0.6, 15.6),
        { t0: 1.4, t1: 7, style: 'quote', text: '順民消費者通過支付官鹽的壟斷高價，買下了雇佣兵的武力，\n從而*免除了自己的軍事義務*。', src: JY, pos: 'top', y: 290 },
        { t0: 7.4, t1: 11.4, style: 'quote', text: '賤民軍隊沒有武德和社會性感情，因此帝國*早晚會失去戰鬥力*。', src: JY, pos: 'top', y: 300 },
        { t0: 11.8, t1: 15.6, style: 'quote', text: '貴族終歸是騎士的餘脈，*禮樂終歸是武德的餘脈*。', src: JY, pos: 'top', y: 300 },
        { t0: 12, t1: 15.4, style: 'note', text: '劍 → 筆 → 鈴', x: 1880, y: 820 },
        { t0: 3, t1: 7, style: 'note', text: '生鏽的矛', x: 340, y: 520 },
      ] },
    { id: 's9_flood', dur: 16, trans: TR, grade: { sat: 0.85, warm: -0.1 },
      cam: t => keys([[0, { x: 1300, y: H * 0.5, z: 1.1 }], [16, { x: 1500, y: H * 0.54, z: 1.14 }]], t, lin),
      layers: { flood: t => ({ dy: lerp(260, -40, ease(prog(t, 8, 15))) }) },
      fx: [{ draw: c => fx.rain(c, { n: 420, k: ease(prog(c.t, 6, 9)) }) }],
      caps: [
        chap('九', '免費的秩序，昂貴的秩序', 0.6, 15.6),
        { t0: 1.4, t1: 7.4, style: 'quote', text: '打土豪破壞了現代社會生產秩序的起點，就只能依賴吏治了，\n然而吏治是*秩序消費者和借貸者*，能量守恆。', src: '劉仲敬微信言論', pos: 'top', y: 290, opt: { size: 48 } },
        { t0: 7.8, t1: 15.6, style: 'quote', text: '有機體依靠*免費土豪*生產秩序，流沙依靠*高價龍騎兵*生產秩序，\n龍騎兵之後就是*洪水*。', src: CB, pos: 'top', y: 290 },
        { t0: 3, t1: 7.2, style: 'note', text: '有根的河岸', x: 480, y: 1000 },
        { t0: 4, t1: 7.2, style: 'note', text: '靠騎兵撐住的沙坡', x: 1640, y: 1000 },
      ] },
    { id: 's10_weeds', dur: 16, trans: TR, grade: t => ({ sat: lerp(1.05, 0.8, prog(t, 5, 12)) }),
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.5, z: 1.08 }], [16, { x: W * 0.5, y: H * 0.6, z: 1.18 }]], t, lin),
      layers: { flowers: t => ({ alpha: 1 - 0.85 * ease(prog(t, 4.5, 10)) }), resistant: t => ({ grow: lerp(-0.02, 1.0, ease(prog(t, 6, 14))), soft: 0.06 }) },
      sprites: (t, c) => (t > 0.5 && t < 7 ? [{ name: 'plane', x: lerp(-300, W + 300, (t - 0.5) / 6.5), y: c.meta.plane_y + Math.sin(t * 2) * 20, d: 0.3, scale: 0.9 }] : []),
      fx: [{ draw: c => { if (c.t < 9) { const v = c.view(0.3); for (let i = 0; i < 60; i++) { const tt = c.t - i * 0.08; if (tt < 0.5 || tt > 7) continue;
        const [x, y] = v.P(lerp(-300, W + 300, (tt - 0.5) / 6.5) - 180, c.meta.plane_y + 40);
        fx.glow(c.n, x + hash(i, 3) * 40, y + (c.t - tt) * 160, 60 + (c.t - tt) * 90, '235,240,225', 0.22 * (1 - (c.t - tt) / 5)); } } } }],
      caps: [
        chap('十', '逆淘汰定律', 0.6, 15.6),
        { t0: 1.4, t1: 15.6, style: 'vquote', text: '誅鋤政術，絕難去敵，\n無非驅敵入地下……\n其勢如農葯抗生素，\n殺滅一切有益或無抗葯性品系，\n促使本居極端少數之抗葯品系\n轉為優勢品系', src: CB, x: 1760, y: 150, opt: { size: 46, col: 14 } },
      ] },
    { id: 's11_bridge', dur: 18, grade: { sat: 0.85, warm: -0.1 },
      cam: t => keys([[0, { x: 1300, y: H * 0.52, z: 1.08 }], [18, { x: 1500, y: H * 0.54, z: 1.12 }]], t, lin),
      layers: { newbridge: t => { const e = Math.max(0, t - 9.5); return { dy: Math.sin(t * 9) * 4 * prog(t, 6, 9.5) + e * e * 260, alpha: 1 - prog(t, 11, 12.5) }; } },
      sprites: (t, c) => [0, 1, 2, 3].map(i => {
        const names = ['dog_0', 'wolf_0', 'dog_1', 'wolf_1'];
        return { name: names[i], x: ((t * 120 + i * 640) % 3200) - 300, y: H * 0.98, d: 0.6, scale: 0.7 + 0.12 * i, alpha: ease(prog(t, 12, 13)) };
      }),
      fx: [{ draw: c => { fx.rain(c, { n: 500, k: 1 - prog(c.t, 12, 15), angle: 0.4 }); fx.flash(c, 9.4, { k: 0.6 }); } }],
      caps: [
        chap('十一', '外壓之下', 0.6, 15.6),
        { t0: 1.4, t1: 9, style: 'quote', text: '有保護型的*牧羊犬*，也有掠奪型的*狼群*，狼群的升級導致牧羊犬的升級，\n這個軍備競賽是*永無止境*的。', src: '《劉仲敬訪談 028》', pos: 'top', y: 290, opt: { size: 46, max: 1800 } },
        { t0: 9.4, t1: 15.6, style: 'quote', text: '無需區別現代不現代，*土豪就是秩序生產者和輸出者*。', src: '劉仲敬微信言論', pos: 'top', y: 300 },
        { t0: 15.8, t1: 18, style: 'sub', text: '劉仲敬思想 · 其八《血酬》', pos: 'center', wash: false },
      ] },
  ],
};
