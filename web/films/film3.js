// 第三部《守先待後》   60 BPM，一小節 4 秒
import { keys, ease, easeOut, easeIn, prog, clamp, lerp, hash } from '../lib/engine.js';
import * as fx from '../lib/fx.js';

const W = 2304, H = 1296, TR = 2;
const SRC = '《文明更迭的源代碼》';
const lin = x => x;

export default {
  title: '守先待後',
  fadeIn: 1.5, fadeOut: 2.5,
  scenes: [
    { id: 's1_monastery', dur: 14, trans: TR, grade: { warm: -0.1 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.4, z: 1.06 }], [14, { x: W * 0.52, y: H * 0.5, z: 1.24 }]], t, lin),
      fx: [
        { after: 'sky', draw: c => fx.stars(c, { n: 200, k: 0.8 }) },
        { after: 'ridge', draw: c => fx.lamps(c, c.meta.lamps.slice(0, 1), 0.4, { t0: 3, t1: 3.1, k: 1.3 }) },
        { draw: c => fx.snow(c, { n: 200, wind: 25, speed: 0.6 }) },
      ],
    },
    { id: 's2_desk', dur: 18, trans: TR, grade: { warm: 0.2, expo: 1.02 },
      cam: t => keys([[0, { x: W * 0.55, y: H * 0.62, z: 1.2 }], [18, { x: W * 0.5, y: H * 0.6, z: 1.1 }]], t, lin),
      fx: [
        { after: 'room', draw: c => {      // 窗外的雪
          const v = c.view(0); const [wx, wy, ww, wh] = c.meta.window;
          const [x0, y0] = v.P(wx, wy), [x1, y1] = v.P(wx + ww, wy + wh);
          c.n.save(); c.n.beginPath(); c.n.rect(x0, y0, x1 - x0, y1 - y0); c.n.clip();
          fx.snow(c, { n: 220, wind: 15, speed: 0.5, k: 0.7 }); c.n.restore();
        } },
        { draw: c => { fx.flame(c, c.meta.flame, 0.4, { size: 1.3 }); fx.motes(c, c.meta.flame, 0.4); } },
      ],
    },
    { id: 's3_clock', dur: 14, trans: TR,
      grade: t => { const k = prog(t, 0, 14); return { warm: Math.sin(k * Math.PI * 2) * 0.35, sat: 0.95 + 0.1 * Math.sin(k * 6.28), expo: 1 - 0.06 * Math.sin(k * 12.56) ** 2 }; },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.5, z: 1.14 }], [14, { x: W * 0.5, y: H * 0.42, z: 1.08 }]], t, lin),
      layers: { sky: t => ({ dx: 0 }) },
      sprites: (t, c) => {
        const [px, py] = c.meta.pivot, [cx, cy] = c.meta.clock;
        const sp = 1 + 9 * ease(prog(t, 2, 9));   // 時間加速：年復一年
        const tt = t + 3 * sp * prog(t, 2, 14) * t;
        return [
          { name: 'pendulum', x: px, y: py, d: 0.4, rot: Math.sin(t * Math.PI) * 0.32, after: 'tower' },
          { name: 'hand_h', x: cx, y: cy, d: 0.4, rot: tt * 0.1, after: 'tower' },
          { name: 'hand_m', x: cx, y: cy, d: 0.4, rot: tt * 1.2, after: 'tower' },
        ];
      },
      fx: [{ after: 'sky', draw: c => fx.cloudShadows(c, { speed: 500, k: 0.6 }) }],
    },
    { id: 's4_digging', dur: 18, trans: TR, grade: { warm: 0.15 },
      cam: t => keys([[0, { x: W * 0.52, y: H * 0.5, z: 1.1 }], [18, { x: W * 0.58, y: H * 0.56, z: 1.2 }]], t, lin),
      sprites: (t, c) => {
        const [dx, dy] = c.meta.dig;
        const cyc = (t * 0.5) % 1;   // 每兩秒一鏟
        const f = cyc < 0.35 ? 0 : cyc < 0.7 ? 1 : 2;
        const out = [{ name: `digger_${f}`, x: dx, y: dy, d: 0.5, scale: 1.05, after: 'slope' }];
        const g = ease(prog(t, 11, 15));
        if (g > 0) out.push({ name: 'sapling', x: c.meta.sapling[0], y: c.meta.sapling[1], d: 0.5, scale: 0.5 + 0.5 * g, alpha: g, after: 'slope' });
        return out;
      },
      fx: [{ after: 'slope', draw: c => {   // 拋出的土
        const v = c.view(0.5); const [hx, hy] = c.meta.dirt;
        const cyc = (c.t * 0.5) % 1;
        if (cyc > 0.7 && c.t < 11) {
          const k = (cyc - 0.7) / 0.3;
          for (let i = 0; i < 9; i++) {
            const [x, y] = v.P(hx + 60 + k * (60 + 40 * hash(i, 3)), hy - 120 * Math.sin(k * Math.PI) * (0.6 + 0.6 * hash(i, 4)));
            c.n.fillStyle = `rgba(90,66,48,${0.8 * (1 - k * 0.5)})`;
            c.n.beginPath(); c.n.arc(x, y, 4 + 4 * hash(i, 5), 0, Math.PI * 2); c.n.fill();
          }
        }
      } }, { draw: c => fx.godrays(c, 1700, -100, { k: 0.3, seed: 5 }) }],
    },
    { id: 's5_storm', dur: 14, trans: TR, grade: { warm: -0.25, sat: 0.75, expo: 0.95 },
      cam: t => keys([[0, { x: 1400, y: H * 0.55, z: 1.12 }], [14, { x: 1800, y: H * 0.56, z: 1.12 }]], t, lin),
      sprites: (t, c) => {
        const ph = Math.floor(t * 3.2) % 4;
        return [{ name: `walker_${ph}`, x: 1050 + t * 62, y: c.meta.walk_y + Math.abs(Math.sin(t * 3.2 * Math.PI / 2)) * -4, d: 0.5, scale: 1.0 }];
      },
      fx: [{ draw: c => { fx.snow(c, { n: 700, wind: -520, speed: 2.4, k: 1.0, seed: 7 }); fx.snow(c, { n: 160, wind: -900, speed: 3.5, k: 1.6, seed: 17 }); } }],
    },
    { id: 's6_sprout', dur: 18, trans: TR, grade: t => ({ warm: lerp(-0.15, 0.25, prog(t, 1, 12)), sat: lerp(0.8, 1.1, prog(t, 1, 12)) }),
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.56, z: 1.1 }], [18, { x: W * 0.5, y: H * 0.62, z: 1.2 }]], t, lin),
      layers: {
        snow: t => ({ grow: lerp(-0.05, 1.08, ease(prog(t, 1.0, 9.0))), conceal: true, soft: 0.12 }),
        sprouts: t => ({ grow: lerp(-0.02, 1.12, ease(prog(t, 5.0, 16.0))), soft: 0.06 }),
      },
      fx: [{ draw: c => fx.godrays(c, 900, -120, { k: 0.45 * ease(prog(c.t, 4, 10)), seed: 8 }) }],
    },
    { id: 's7_valley', dur: 14, grade: { warm: 0.15, sat: 1.05 },
      cam: t => keys([[0, { x: 1500, y: H * 0.5, z: 1.22 }], [14, { x: 1728, y: H * 0.5, z: 1.06 }]], t, lin),
      fx: [
        { after: 'valley', draw: c => fx.lamps(c, c.meta.lamps.slice(0, 3), 0.45, { t0: 6, t1: 9, k: 0.6, warm: '255,214,140' }) },
        { draw: c => fx.petals(c, { n: 70, seed: 21 }) },
      ],
    },
  ],
  captions: [
    { t0: 1.6, t1: 6.8, style: 'title', text: '守先待後', pos: 'center', y: 470, color: 'paper' },
    { t0: 2.8, t1: 6.8, style: 'sub', text: '劉仲敬思想 · 水彩短片 其三', pos: 'center', y: 620, color: 'paper', wash: false },
    { t0: 7.4, t1: 12.2, style: 'concept', text: '大洪水之後，種子保存在哪裏？', color: 'paper', pos: 'bottom', y: 940 },
    { t0: 14.5, t1: 26.5, style: 'vquote', text: '這粒種子不可能\n一直保持種子狀態，\n因為種子歸根結底\n還是要發芽的。', src: SRC, x: 1720, y: 150, color: 'paper', opt: { size: 56 } },
    { t0: 30.0, t1: 38.5, style: 'concept', text: '年復一年', x: 480, y: 300 },
    { t0: 42.5, t1: 54.5, style: 'quote', text: '就像是禪宗所說的那樣，「砍柴提水」，\n或者我說的挖坑種樹那樣', src: '《劉仲敬論知識與虛無感》', pos: 'top', y: 170 },
    { t0: 58.0, t1: 67.0, style: 'quote', text: '求戰者安，求安者亡。', src: '數卷殘編', pos: 'top', y: 200, opt: { size: 76 } },
    { t0: 71.0, t1: 82.5, style: 'quote', text: '世界上很少有死亡解決不了的問題。\n而希望的種子，更可能保留在小團體裡面。', src: SRC, pos: 'top', y: 170 },
    { t0: 87.0, t1: 93.5, style: 'concept', text: '守先待後', pos: 'top', y: 150 },
    { t0: 94.2, t1: 98, style: 'sub', text: '劉仲敬思想 · 其三《守先待後》', pos: 'center', wash: false },
  ],
};
