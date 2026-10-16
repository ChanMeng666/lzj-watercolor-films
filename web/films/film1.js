// 第一部《根》— 秩序是長出來的   60 BPM，一小節 4 秒
import { keys, ease, easeOut, easeIn, prog, clamp, lerp, hash } from '../lib/engine.js';
import * as fx from '../lib/fx.js';

const W = 2304, H = 1296, TR = 2;
const SRC = '《文明更迭的源代碼》';

export default {
  title: '根',
  fadeIn: 1.5, fadeOut: 2.5,
  scenes: [
    { id: 's1_seed', dur: 14, trans: TR, grade: { warm: 0.35, sat: 0.95 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.42, z: 1.06 }], [14, { x: W * 0.5, y: H * 0.6, z: 1.22 }]], t, x => x),
      sprites: (t, c) => {
        const [lx, ly] = c.meta.land;
        const k = prog(t, 5.5, 8.6);
        if (k <= 0) return [];
        const y = lerp(-120, ly, easeIn(k));
        const x = lx + Math.sin(k * 7) * 40 * (1 - k);
        return [{ name: 'seed', x, y, d: 0.9, rot: k * 5, scale: 1.4, alpha: 1 - prog(t, 10, 12) * 0.6 }];
      },
      fx: [{ draw: c => { fx.ripple(c, c.meta.land, 0.9, 8.6); fx.godrays(c, 1300, -120, { k: 0.35 }); } }],
    },
    { id: 's2_roots', dur: 18, trans: TR, grade: { warm: 0.15 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.45, z: 1.12 }], [18, { x: W * 0.5, y: H * 0.58, z: 1.16 }]], t, x => x),
      layers: {
        roots: t => ({ grow: lerp(-0.02, 1.02, ease(prog(t, 1.5, 15))), soft: 0.05 }),
        tree: t => ({ grow: lerp(-0.02, 1.08, ease(prog(t, 1.0, 13))), soft: 0.06 }),
      },
    },
    { id: 's3_village', dur: 14, trans: TR, grade: { warm: 0.4, expo: 0.98 },
      cam: t => keys([[0, { x: W * 0.4, y: H * 0.52, z: 1.14 }], [14, { x: W * 0.6, y: H * 0.5, z: 1.14 }]], t, x => x),
      fx: [
        { after: 'mid', draw: c => { fx.lamps(c, c.meta.lamps, 0.45, { t0: 2.5, t1: 9, seed: 3 }); fx.smoke(c, c.meta.smoke, 0.45); } },
      ],
    },
    { id: 's4_dance', dur: 18, trans: TR, grade: { warm: 0.3, expo: 0.96 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.6, z: 1.1 }], [18, { x: W * 0.5, y: H * 0.64, z: 1.22 }]], t, x => x),
      sprites: (t, c) => {
        const [cx, cy, rx, ry] = c.meta.ring;
        const sync = ease(prog(t, 2, 12));             // 從錯步到協調
        const out = [];
        for (let i = 0; i < 6; i++) {
          const jitter = (hash(i, 1) - 0.5) * 2;
          const a = t * 0.42 + i * Math.PI / 3 + jitter * 0.5 * (1 - sync) + Math.sin(t * 1.7 + i) * 0.25 * (1 - sync);
          const step = t * 2 + jitter * 1.7 * (1 - sync) + (1 - sync) * Math.sin(t * 2.3 + i * 4);
          const f = [0, 1, 2, 1][((Math.floor(step) % 4) + 4) % 4];
          const x = cx + Math.cos(a) * rx, y = cy + Math.sin(a) * ry + 40;
          const bob = Math.abs(Math.sin(step * Math.PI)) * 8;
          out.push({ name: `dancer${i}_${f}`, x, y: y - bob, d: 0.5, scale: 1.2 + 0.3 * Math.sin(a),
                     after: Math.sin(a) < 0 ? 'green' : undefined, flip: Math.cos(a + Math.PI / 2) < 0 });
        }
        return out.sort((p, q) => p.y - q.y);
      },
      fx: [
        { after: 'back', draw: c => fx.lamps(c, c.meta.lamps, 0.25, { t0: 0, t1: 1, k: 0.8 }) },
        { after: 'green', draw: c => fx.fire(c, c.meta.fire, 0.5, { k: ease(prog(c.t, 0, 2)) }) },
        { draw: c => fx.stars(c, { n: 120, k: 0.6, ymax: 0.3 }) },
      ],
    },
    { id: 's5_growth', dur: 14, trans: TR, grade: { warm: 0.1, sat: 1.05 },
      cam: t => keys([[0, { x: 1300, y: H * 0.52, z: 1.1 }], [14, { x: 2150, y: H * 0.5, z: 1.1 }]], t, x => x),
      sprites: (t, c) => c.meta.boats.map((b, i) => ({ name: 'boat', x: b[0] + t * (30 + 20 * i), y: b[1], d: 0.5, scale: 0.9, after: 'mid' })),
      fx: [{ draw: c => fx.petals(c, { n: 30, cols: ['255,255,240', '240,236,200'], size: 0.6, k: 0.6 }) }],
    },
    { id: 's6_harvester', dur: 14, trans: TR,
      grade: t => ({ warm: lerp(0.25, -0.1, prog(t, 5, 12)), sat: lerp(1.0, 0.7, prog(t, 5, 12)) }),
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.56, z: 1.08 }], [14, { x: W * 0.5, y: H * 0.5, z: 1.16 }]], t, x => x),
      layers: {
        wall: t => ({ dy: lerp(420, 0, easeOut(prog(t, 0.8, 6.5))) }),
        wheat: t => ({ grow: lerp(-0.05, 1.08, ease(prog(t, 5.5, 12.5))), conceal: true, soft: 0.08 }),
      },
    },
    { id: 's7_stalled', dur: 14, trans: TR, grade: { sat: 0.7, warm: -0.15, expo: 0.97 },
      cam: t => keys([[0, { x: W * 0.5, y: H * 0.46, z: 1.14 }], [14, { x: W * 0.5, y: H * 0.46, z: 1.1 }]], t, x => x),
      layers: { clouds: t => ({ dx: -t * 22 }) },
      fx: [
        { after: 'land', draw: c => {
          fx.cloudShadows(c, { speed: 240 });
          const k = ease(prog(c.t, 3, 5));
          const v = c.view(0.5);
          const [x0, y] = v.P(W * 0.5 - 560, c.meta.mark_y), [x1] = v.P(W * 0.5 + 560, c.meta.mark_y);
          c.n.setLineDash([18, 14]); c.n.strokeStyle = `rgba(150,40,30,${0.7 * k})`; c.n.lineWidth = 3;
          c.n.beginPath(); c.n.moveTo(lerp((x0 + x1) / 2, x0, k), y); c.n.lineTo(lerp((x0 + x1) / 2, x1, k), y); c.n.stroke();
          c.n.setLineDash([]);
        } },
      ],
    },
    { id: 's8_night', dur: 14, grade: { expo: 1.02, warm: -0.05 },
      cam: t => keys([[0, { x: W * 0.46, y: H * 0.45, z: 1.2 }], [14, { x: W * 0.5, y: H * 0.5, z: 1.06 }]], t, x => x),
      fx: [{ after: 'sky', draw: c => { fx.stars(c, { n: 260, k: ease(prog(c.t, 0, 3)) });
        const v = c.view(0); const [mx, my] = v.P(W * 0.76, H * 0.22); fx.glow(c.a, mx, my, 360, '230,230,255', 0.18); } }],
    },
  ],
  captions: [
    { t0: 2.0, t1: 7.5, style: 'title', text: '根', pos: 'center', y: 470 },
    { t0: 3.2, t1: 7.5, style: 'sub', text: '劉仲敬思想 · 水彩短片 其一', pos: 'center', y: 600, wash: false },
    { t0: 8.0, t1: 12.5, style: 'concept', text: '秩序從哪裏來？' },
    { t0: 15.0, t1: 26.5, style: 'quote', text: '如果樹長得高，那麼它地下的根就一定特別深。', src: SRC, y: 150 },
    { t0: 30.0, t1: 38.5, style: 'concept', text: '自組織資源 —— 文明的本金', color: 'ink', pos: 'top' },
    { t0: 42.0, t1: 54.5, style: 'quote', text: '剛開始跳舞的時候你會經常踩到別人的腳，\n但是時間長了以後，自己的動作就會協調起來。', src: SRC, color: 'paper', pos: 'top', y: 170 },
    { t0: 58.0, t1: 66.5, style: 'concept', text: '秩序是長出來的', pos: 'top' },
    { t0: 70.5, t1: 79.0, style: 'quote', text: '官僚制度和國家建制的出現\n都是最危險的收割者。', src: SRC, pos: 'top', y: 190 },
    { t0: 82.0, t1: 91.0, style: 'vquote', text: '過早地出現了收割者，\n那麼你的文明\n就會停留在\n收割者出現那一刻的高度。', src: SRC, x: 1700, y: 150, opt: { col: 12, size: 54 } },
    { t0: 94.0, t1: 102.5, style: 'quote', text: '你能夠做的就是盡可能少消耗社會的自組織資源，\n延長它的壽命。', src: SRC, color: 'paper', pos: 'bottom' },
    { t0: 102.8, t1: 106, style: 'sub', text: '劉仲敬思想 · 其一《根》', color: 'paper', pos: 'center', wash: false },
  ],
};
