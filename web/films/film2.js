// 第二部《四季》— 文明的季候   60 BPM，一小節 4 秒
import { keys, ease, easeOut, easeIn, prog, clamp, lerp, hash } from '../lib/engine.js';
import * as fx from '../lib/fx.js';

const W = 2304, H = 1296, TR = 2;
const SRC = '《文明更迭的源代碼》';
const lin = x => x;

// 煙花：時間、場景座標、顏色
const BURSTS = [
  [1.0, 700, 300, '255,200,120'], [2.2, 1500, 240, '255,140,150'], [3.4, 1100, 180, '200,220,255'],
  [4.3, 520, 260, '255,230,150'], [5.1, 1800, 300, '180,255,200'], [6.0, 1250, 150, '255,170,90'],
  [6.7, 860, 220, '255,120,120'], [7.4, 1600, 170, '255,220,180'], [8.1, 400, 300, '210,190,255'],
  [8.6, 1950, 230, '255,200,120'], [9.2, 1150, 260, '255,150,200'], [9.8, 700, 160, '255,240,200'],
  [10.3, 1450, 120, '255,180,110'], [10.9, 950, 300, '190,230,255'], [11.4, 1700, 260, '255,130,140'],
];

export default {
  title: '四季',
  fadeIn: 1.5, fadeOut: 2.5,
  scenes: [
    { id: 's1_spring', dur: 14, trans: TR, grade: { warm: 0.1, sat: 1.05 },
      cam: t => keys([[0, { x: 1200, y: H * 0.5, z: 1.1 }], [14, { x: 1800, y: H * 0.5, z: 1.14 }]], t, lin),
      fx: [
        { after: 'hills', draw: c => fx.lamps(c, c.meta.lamps, 0.4, { t0: 6.5, t1: 12, warm: '255,214,140', k: 0.7, seed: 4 }) },
        { draw: c => fx.petals(c, { n: 60 }) },
      ],
    },
    { id: 's2_summer', dur: 14, trans: TR, grade: { warm: 0.15, sat: 1.1 },
      cam: t => keys([[0, { x: 1300, y: H * 0.52, z: 1.12 }], [14, { x: 1700, y: H * 0.54, z: 1.12 }]], t, lin),
      sprites: (t, c) => c.meta.boats.map((b, i) => ({ name: 'boat', x: b[0] + t * (40 - 25 * i), y: b[1] + Math.sin(t * 1.5 + i) * 3,
        d: 0.6, scale: 0.8 + 0.25 * i, after: 'river', flip: i === 1 })),
      fx: [{ draw: c => fx.godrays(c, 300, -150, { k: 0.3, seed: 6 }) }],
    },
    { id: 's3_autumn', dur: 14, trans: TR, grade: { warm: 0.35, sat: 1.05 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.62, z: 1.08 }], [14, { x: W * 0.5, y: H * 0.44, z: 1.22 }]], t, lin),
      fx: [{ draw: c => fx.petals(c, { n: 55, cols: ['230,140,60', '210,100,50', '240,180,70'], wind: 90, fall: 70, size: 1.3, seed: 12 }) }],
    },
    { id: 's4_fireworks', dur: 18, trans: TR, grade: { expo: 1.0, warm: 0.1 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.5, z: 1.08 }], [18, { x: W * 0.5, y: H * 0.42, z: 1.18 }]], t, lin),
      fx: [
        { after: 'sky', draw: c => { fx.stars(c, { n: 120, k: 0.5 }); fx.fireworks(c, BURSTS, 0.15); fx.fireworks(c, BURSTS.map(b => [b[0] + 6.4, b[1] + 200, b[2] + 40, b[3]]), 0.15); } },
        { after: 'palace', draw: c => fx.lamps(c, c.meta.lamps, 0.3, { t0: 0, t1: 1.5, k: 1.2 }) },
      ],
    },
    { id: 's5_dimming', dur: 14, trans: TR, grade: t => ({ expo: lerp(1.0, 0.82, prog(t, 2, 12)), sat: lerp(1.0, 0.75, prog(t, 2, 12)) }),
      cam: t => keys([[0, { x: 1300, y: H * 0.56, z: 1.16 }], [14, { x: 1500, y: H * 0.52, z: 1.08 }]], t, lin),
      fx: [
        { after: 'sky', draw: c => fx.stars(c, { n: 160, k: 0.6 }) },
        { after: 'city', draw: c => fx.lamps(c, c.meta.lamps, 0.5, { t0: -2, t1: -1, off: [2.5, 11.5], seed: 9 }) },
      ],
    },
    { id: 's6_winter', dur: 18, trans: TR, grade: { warm: -0.2, sat: 0.8 },
      cam: t => keys([[0, { x: 1300, y: H * 0.5, z: 1.1 }], [18, { x: 1700, y: H * 0.52, z: 1.16 }]], t, lin),
      fx: [
        { after: 'field', draw: c => { fx.lamps(c, c.meta.lamps.slice(1, 2), 0.45, { t0: 6, t1: 6.1, k: 0.9 }); fx.smoke(c, [[1300 + 32, H * 0.64 - 120]], 0.45, { k: 0.6 }); } },
        { draw: c => fx.snow(c, { n: 380, wind: 60 }) },
      ],
    },
    { id: 's7_steppe', dur: 14, trans: TR, grade: { warm: 0.3 },
      cam: t => keys([[0, { x: 1300, y: H * 0.56, z: 1.12 }], [14, { x: 1900, y: H * 0.58, z: 1.12 }]], t, lin),
      sprites: (t, c) => {
        const out = [];
        for (let i = 0; i < 6; i++) {
          const z = 0.5 + 0.12 * (i % 3);
          const x = -300 + i * 230 + t * (190 + 15 * i);
          const ph = Math.floor(t * 7 + i * 1.3) % 4;
          out.push({ name: `rider_${ph}`, x, y: c.meta.ride_y + (i % 3) * 60 - 60, d: z, scale: 0.6 + 0.12 * (i % 3) });
        }
        return out.sort((a, b) => a.y - b.y);
      },
      fx: [{ draw: c => fx.godrays(c, 1500, 380, { k: 0.5, n: 9, len: 1800, rgb: '255,210,150', seed: 3 }) }],
    },
    { id: 's8_spring2', dur: 14, grade: { warm: 0.12, sat: 1.05 },
      cam: t => keys([[0, { x: W * 0.52, y: H * 0.5, z: 1.2 }], [14, { x: W * 0.5, y: H * 0.5, z: 1.06 }]], t, lin),
      fx: [
        { after: 'hills', draw: c => fx.lamps(c, c.meta.lamps, 0.35, { t0: 3, t1: 3.1, warm: '255,214,140', k: 0.8 }) },
        { draw: c => fx.petals(c, { n: 80, seed: 15 }) },
      ],
    },
  ],
  captions: [
    { t0: 1.6, t1: 6.6, style: 'title', text: '四季', pos: 'center', y: 470 },
    { t0: 2.8, t1: 6.6, style: 'sub', text: '劉仲敬思想 · 水彩短片 其二', pos: 'center', y: 620, wash: false },
    { t0: 7.2, t1: 12.2, style: 'concept', text: '春 · 封建 —— 千百個小中心', pos: 'top' },
    { t0: 14.2, t1: 23.5, style: 'concept', text: '夏 · 自由城市 —— 秩序輸出', pos: 'top' },
    { t0: 26.2, t1: 35.5, style: 'concept', text: '秋 · 理性化與官僚', pos: 'top', y: 150 },
    { t0: 40.0, t1: 50.8, style: 'quote', text: '在他們的眼中，揮霍才是進步。', src: SRC, color: 'paper', pos: 'bottom', y: 900 },
    { t0: 54.0, t1: 63.0, style: 'quote', text: '普遍性進步實際上是相當消耗社會資源的……\n它是一種破壞，它代表著既有積累的毀滅。', src: SRC, color: 'paper', pos: 'top', y: 190 },
    { t0: 66.5, t1: 78.5, style: 'vquote', text: '冬 · 編戶齊民\n散沙化的人群', x: 1640, y: 170, opt: { size: 58 } },
    { t0: 82.0, t1: 91.0, style: 'quote', text: '蠻族入侵帶來的新生機會', src: '《經與史：華夏世界的歷史建構》', pos: 'top', y: 170 },
    { t0: 94.5, t1: 102.3, style: 'concept', text: '季候輪轉 —— 春天在邊緣重新開始', pos: 'top' },
    { t0: 102.6, t1: 106, style: 'sub', text: '劉仲敬思想 · 其二《四季》', pos: 'center', wash: false },
  ],
};
