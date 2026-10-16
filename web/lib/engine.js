// 水彩短片播放器：WebGL2 景深合成 + Canvas2D 特效/字幕 + 水彩暈染轉場 + 調色
// 每一幀都是時間 t 的純函數（無 Math.random、無時鐘），供無頭瀏覽器逐幀截圖。
import { drawCaption } from './type.js';

export const VW = 1920, VH = 1080;
const BASE = VH / 1296;          // 場景高 1296 → 視口高 1080

// ------------------------------------------------------------------ utils
export const clamp = (x, a = 0, b = 1) => Math.min(b, Math.max(a, x));
export const lerp = (a, b, t) => a + (b - a) * t;
export const ease = t => { t = clamp(t); return t * t * (3 - 2 * t); };
export const easeOut = t => 1 - Math.pow(1 - clamp(t), 3);
export const easeIn = t => Math.pow(clamp(t), 2.2);
export const prog = (t, a, b) => clamp((t - a) / (b - a));
export function hash(i, s = 0) {
  let x = Math.imul((i | 0) ^ 0x9e3779b9, 0x85ebca6b) ^ Math.imul((s | 0) + 0x632be5ab, 0xc2b2ae35);
  x ^= x >>> 15; x = Math.imul(x, 0x2c1b3c6d); x ^= x >>> 12; x = Math.imul(x, 0x297a2d39); x ^= x >>> 15;
  return (x >>> 0) / 4294967296;
}
// 關鍵幀插值：[[t, {x,y,z}], ...]
export function keys(list, t, fn = ease) {
  if (t <= list[0][0]) return { ...list[0][1] };
  for (let i = 0; i < list.length - 1; i++) {
    const [t0, a] = list[i], [t1, b] = list[i + 1];
    if (t <= t1) {
      const k = fn((t - t0) / (t1 - t0)); const o = {};
      for (const key in a) o[key] = lerp(a[key], b[key] ?? a[key], k);
      return o;
    }
  }
  return { ...list[list.length - 1][1] };
}

// ------------------------------------------------------------------ GL
const VS = `#version 300 es
in vec2 a; uniform vec2 uO, uU, uV; out vec2 uv;
void main(){ uv = a; vec2 p = uO + a.x*uU + a.y*uV;
  gl_Position = vec4(p.x/${VW}.0*2.0-1.0, 1.0-p.y/${VH}.0*2.0, 0, 1); }`;
const FS_LAYER = `#version 300 es
precision highp float; in vec2 uv; out vec4 o;
uniform sampler2D tex, tmap; uniform float useT, grow, soft, conceal, alpha; uniform vec3 tint;
uniform vec4 crop;
void main(){
  vec2 st = crop.xy + uv*crop.zw;
  vec4 c = texture(tex, st);
  if (useT > 0.5) {
    float t = texture(tmap, st).r;
    float k = 1.0 - smoothstep(grow - soft, grow, t);
    if (conceal > 0.5) k = 1.0 - k;
    c *= k;
  }
  c.rgb *= tint; o = c * alpha; }`;
const FS_POST = `#version 300 es
precision highp float; in vec2 uv; out vec4 o;
uniform sampler2D A, B, paper, noise, cap;
uniform float p, frame, fade, paperK, vig, grainK, twoScenes;
uniform vec4 gA1, gB1; uniform vec3 gA2, gB2; uniform vec3 fadeCol;
vec3 grade(vec3 c, vec4 g, vec3 tint){
  c *= g.x; c = (c - 0.5) * g.y + 0.5;
  float l = dot(c, vec3(.299,.587,.114)); c = mix(vec3(l), c, g.z);
  c += vec3(g.w, g.w*0.25, -g.w) * 0.08; return c * tint; }
float h(vec2 q){ return fract(sin(dot(q, vec2(12.9898,78.233)) + frame*0.618) * 43758.5453); }
void main(){
  vec2 q = vec2(uv.x, 1.0 - uv.y);
  vec3 nz = texture(noise, uv).rgb;
  float n = nz.b * 0.65 + nz.g * 0.35;
  float e = p * 1.3 - 0.15;
  float mB = twoScenes > 0.5 ? 1.0 - smoothstep(e - 0.035, e + 0.035, n) : 0.0;
  float near = exp(-pow((n - e) / 0.06, 2.0)) * twoScenes;
  vec2 d = (texture(noise, uv * 2.7).rg - 0.5) * 0.018 * near;
  vec3 a = grade(texture(A, q + d).rgb, gA1, gA2);
  vec3 col = a;
  if (twoScenes > 0.5) {
    vec3 b = grade(texture(B, q - d).rgb, gB1, gB2);
    col = mix(a, b, mB);
    float rim = exp(-pow((n - e) / 0.010, 2.0));
    col *= 1.0 - 0.22 * rim;                    // 水跡邊緣積色
    col = mix(col, col * vec3(0.96, 0.94, 0.92), near * 0.5);
  }
  col *= mix(vec3(1.0), texture(paper, uv).rgb / vec3(0.972, 0.958, 0.925), paperK);
  vec2 c = uv - 0.5; c.x *= 1.25;
  col *= 1.0 - vig * smoothstep(0.25, 0.85, length(c));
  col += (h(uv * 1000.0) - 0.5) * grainK;
  vec4 t = texture(cap, uv);
  col = col * (1.0 - t.a) + t.rgb;
  col = mix(col, fadeCol, fade);
  o = vec4(col, 1.0); }`;

function compile(gl, vs, fs) {
  const p = gl.createProgram();
  for (const [type, src] of [[gl.VERTEX_SHADER, vs], [gl.FRAGMENT_SHADER, fs]]) {
    const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s);
    if (!gl.getShaderParameter(s, gl.COMPILE_STATUS)) throw new Error(gl.getShaderInfoLog(s));
    gl.attachShader(p, s);
  }
  gl.bindAttribLocation(p, 0, 'a'); gl.linkProgram(p);
  if (!gl.getProgramParameter(p, gl.LINK_STATUS)) throw new Error(gl.getProgramInfoLog(p));
  const u = {}; const n = gl.getProgramParameter(p, gl.ACTIVE_UNIFORMS);
  for (let i = 0; i < n; i++) { const info = gl.getActiveUniform(p, i); u[info.name] = gl.getUniformLocation(p, info.name); }
  return { p, u };
}

export class Player {
  constructor(canvas, film, base) {
    this.film = film; this.base = base;
    const gl = this.gl = canvas.getContext('webgl2', { premultipliedAlpha: false, preserveDrawingBuffer: true, antialias: false });
    this.L = compile(gl, VS, FS_LAYER); this.P = compile(gl, VS, FS_POST);
    const vb = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, vb);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([0, 0, 1, 0, 0, 1, 1, 1]), gl.STATIC_DRAW);
    gl.enableVertexAttribArray(0); gl.vertexAttribPointer(0, 2, gl.FLOAT, false, 0, 0);
    this.fbo = [0, 1].map(() => this.makeFBO());
    this.cache = new Map();         // scene id → {man, tex:{}}
    this.pending = new Map();
    this.fxc = [];                   // 特效畫布池
    this.cap = document.createElement('canvas'); this.cap.width = VW; this.cap.height = VH;
    this.capTex = this.texFromCanvas(null);
    // 時間表
    let s = 0; this.starts = [];
    film.scenes.forEach((sc, i) => { this.starts.push(s); s += sc.dur - (i < film.scenes.length - 1 ? (sc.trans ?? 1.5) : 0); });
    this.duration = film.duration ?? s;
    // 場景內的字幕（局部時間）→ 全片時間
    film.captions = film.captions || [];
    film.scenes.forEach((sc, i) => (sc.caps || []).forEach(c => film.captions.push({ ...c, sci: i, t0: this.starts[i] + c.t0, t1: this.starts[i] + c.t1 })));
  }
  makeFBO() {
    const gl = this.gl, t = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, t);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA8, VW, VH, 0, gl.RGBA, gl.UNSIGNED_BYTE, null);
    this.texParams();
    const f = gl.createFramebuffer(); gl.bindFramebuffer(gl.FRAMEBUFFER, f);
    gl.framebufferTexture2D(gl.FRAMEBUFFER, gl.COLOR_ATTACHMENT0, gl.TEXTURE_2D, t, 0);
    return { f, t };
  }
  texParams(wrap) {
    const gl = this.gl;
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MIN_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_MAG_FILTER, gl.LINEAR);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_S, wrap || gl.CLAMP_TO_EDGE);
    gl.texParameteri(gl.TEXTURE_2D, gl.TEXTURE_WRAP_T, wrap || gl.CLAMP_TO_EDGE);
  }
  texFromCanvas(cv, tex) {
    const gl = this.gl; tex = tex || gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, tex);
    gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, true);
    if (cv) gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, cv);
    else gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, 1, 1, 0, gl.RGBA, gl.UNSIGNED_BYTE, new Uint8Array(4));
    gl.pixelStorei(gl.UNPACK_PREMULTIPLY_ALPHA_WEBGL, false);
    this.texParams(); return tex;
  }
  async loadImg(url, wrap) {
    const b = await (await fetch(url)).blob();
    const bmp = await createImageBitmap(b, { premultiplyAlpha: 'premultiply', colorSpaceConversion: 'none' });
    const gl = this.gl, tex = gl.createTexture();
    gl.bindTexture(gl.TEXTURE_2D, tex);
    gl.texImage2D(gl.TEXTURE_2D, 0, gl.RGBA, gl.RGBA, gl.UNSIGNED_BYTE, bmp);
    this.texParams(wrap); const r = { tex, w: bmp.width, h: bmp.height }; bmp.close(); return r;
  }
  async init() {
    const g = this.gl;
    this.paper = await this.loadImg(`${this.base}/assets/paper.jpg`);
    this.noise = await this.loadImg(`${this.base}/assets/noise.png`, g.REPEAT);
    await document.fonts.ready;
  }
  async loadScene(id) {
    if (this.cache.has(id)) return this.cache.get(id);
    if (this.pending.has(id)) return this.pending.get(id);
    const pr = (async () => {
      const dir = `${this.base}/assets/${this.film.id}/${id}`;
      const man = await (await fetch(`${dir}/manifest.json`)).json();
      const tex = {};
      const jobs = [];
      for (const l of man.layers) {
        jobs.push(this.loadImg(`${dir}/${l.file}`).then(r => tex[l.name] = r));
        if (l.tmap) jobs.push(this.loadImg(`${dir}/${l.tmap}`).then(r => tex[l.name + '_t'] = r));
      }
      for (const s of man.sprites) jobs.push(this.loadImg(`${dir}/${s.file}`).then(r => tex['sp_' + s.name] = r));
      await Promise.all(jobs);
      const sp = {}; for (const s of man.sprites) sp[s.name] = s;
      const ent = { man, tex, sp };
      this.cache.set(id, ent); this.pending.delete(id);
      // 只保留最近 4 個場景的貼圖
      while (this.cache.size > 4) {
        const k = this.cache.keys().next().value; const e = this.cache.get(k);
        for (const t of Object.values(e.tex)) this.gl.deleteTexture(t.tex);
        this.cache.delete(k);
      }
      return ent;
    })();
    this.pending.set(id, pr); return pr;
  }
  // 視口中有哪些場景
  active(t) {
    const out = [];
    this.film.scenes.forEach((sc, i) => {
      const s0 = this.starts[i], s1 = s0 + sc.dur;
      if (t >= s0 && t < s1) out.push({ i, sc, lt: t - s0 });
    });
    if (!out.length) { const i = this.film.scenes.length - 1; out.push({ i, sc: this.film.scenes[i], lt: t - this.starts[i] }); }
    return out.slice(0, 2);
  }
  // 景深相機
  camFor(ent, sc, lt) {
    const man = ent.man;
    const c = sc.cam ? sc.cam(lt) : { x: man.w / 2, y: man.h / 2, z: 1.08 };
    return { x: c.x ?? man.w / 2, y: c.y ?? man.h / 2, z: c.z ?? 1.08, r: c.r ?? 0, man };
  }
  view(cam, d) {
    const f = 0.12 + 0.88 * d, man = cam.man;
    const z = 1 + (cam.z - 1) * f;
    const s = BASE * z;
    let cx = man.w / 2 + (cam.x - man.w / 2) * f, cy = man.h / 2 + (cam.y - man.h / 2) * f;
    const hw = VW / s / 2, hh = VH / s / 2;
    cx = clamp(cx, hw, man.w - hw); cy = clamp(cy, hh, man.h - hh);
    return { s, cx, cy, P: (x, y) => [(x - cx) * s + VW / 2, (y - cy) * s + VH / 2] };
  }
  fxCanvas(k) {
    while (this.fxc.length <= k) {
      const n = document.createElement('canvas'); n.width = VW; n.height = VH;
      const a = document.createElement('canvas'); a.width = VW; a.height = VH;
      this.fxc.push({ n, a, nx: n.getContext('2d'), ax: a.getContext('2d'), nt: null, at: null });
    }
    return this.fxc[k];
  }
  quad(tex, O, U, V, o = {}) {
    const gl = this.gl, u = this.L.u;
    gl.uniform2f(u.uO, O[0], O[1]); gl.uniform2f(u.uU, U[0], U[1]); gl.uniform2f(u.uV, V[0], V[1]);
    gl.activeTexture(gl.TEXTURE0); gl.bindTexture(gl.TEXTURE_2D, tex); gl.uniform1i(u.tex, 0);
    if (o.tmap) { gl.activeTexture(gl.TEXTURE1); gl.bindTexture(gl.TEXTURE_2D, o.tmap); gl.uniform1i(u.tmap, 1); }
    gl.uniform1f(u.useT, o.tmap ? 1 : 0); gl.uniform1f(u.grow, o.grow ?? 1.1); gl.uniform1f(u.soft, o.soft ?? 0.04);
    gl.uniform1f(u.conceal, o.conceal ? 1 : 0); gl.uniform1f(u.alpha, o.alpha ?? 1);
    const tn = o.tint ?? [1, 1, 1]; gl.uniform3f(u.tint, tn[0], tn[1], tn[2]);
    const cr = o.crop ?? [0, 0, 1, 1]; gl.uniform4f(u.crop, cr[0], cr[1], cr[2], cr[3]);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
  }
  drawScene(k, item, T) {
    const { sc, lt } = item; const gl = this.gl;
    const ent = this.cache.get(sc.id); const man = ent.man;
    gl.bindFramebuffer(gl.FRAMEBUFFER, this.fbo[k].f); gl.viewport(0, 0, VW, VH);
    gl.clearColor(0.972, 0.958, 0.925, 1); gl.clear(gl.COLOR_BUFFER_BIT);
    gl.useProgram(this.L.p); gl.enable(gl.BLEND); gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
    const cam = this.camFor(ent, sc, lt);
    const ctx = { t: lt, T, cam, man, meta: man.meta, view: d => this.view(cam, d), player: this, sc };
    const spr = sc.sprites ? sc.sprites(lt, ctx) : [];
    const fx = sc.fx || [];
    let slot = 0;
    const doFx = after => {
      for (const f of fx) if ((f.after ?? 'top') === after) {
        const c = this.fxCanvas(k * 8 + slot++);
        c.nx.setTransform(1, 0, 0, 1, 0, 0); c.ax.setTransform(1, 0, 0, 1, 0, 0);
        c.nx.clearRect(0, 0, VW, VH); c.ax.clearRect(0, 0, VW, VH);
        f.draw({ ...ctx, n: c.nx, a: c.ax });
        c.nt = this.texFromCanvas(c.n, c.nt); c.at = this.texFromCanvas(c.a, c.at);
        gl.useProgram(this.L.p);
        gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
        this.quad(c.nt, [0, 0], [VW, 0], [0, VH]);
        gl.blendFunc(gl.ONE, gl.ONE);
        this.quad(c.at, [0, 0], [VW, 0], [0, VH]);
        gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
      }
    };
    for (const l of man.layers) {
      const ov = (sc.layers && sc.layers[l.name]) ? sc.layers[l.name](lt, ctx) : {};
      if (ov.hide) { doFx(l.name); continue; }
      const v = this.view(cam, ov.depth ?? l.depth);
      const dx = ov.dx ?? 0, dy = ov.dy ?? 0;
      const O = v.P(dx, dy);
      this.quad(ent.tex[l.name].tex, O, [man.w * v.s, 0], [0, man.h * v.s], {
        tmap: l.tmap ? ent.tex[l.name + '_t'].tex : null, grow: ov.grow, soft: ov.soft, conceal: ov.conceal,
        alpha: ov.alpha, tint: ov.tint,
      });
      for (const s of spr) if (s.after === l.name) this.drawSprite(ent, s, cam);
      doFx(l.name);
    }
    for (const s of spr) if (!s.after) this.drawSprite(ent, s, cam);
    doFx('top');
  }
  drawSprite(ent, s, cam) {
    const info = ent.sp[s.name]; if (!info) return;
    const v = this.view(cam, s.d ?? 0.5);
    const [px, py] = v.P(s.x, s.y);
    const sc = v.s * (s.scale ?? 1);
    const w = info.w * sc * (s.flip ? -1 : 1), h = info.h * sc;
    const r = s.rot ?? 0, cs = Math.cos(r), sn = Math.sin(r);
    const U = [cs * w, sn * w], V = [-sn * h, cs * h];
    const ax = info.anchor[0], ay = info.anchor[1];
    const O = [px - U[0] * ax - V[0] * ay, py - U[1] * ax - V[1] * ay];
    this.quad(ent.tex['sp_' + s.name].tex, O, U, V, { alpha: s.alpha ?? 1, tint: s.tint });
  }
  gradeOf(item) {
    const g = Object.assign({ expo: 1, con: 1, sat: 1, warm: 0, tint: [1, 1, 1] },
      typeof item.sc.grade === 'function' ? item.sc.grade(item.lt) : item.sc.grade || {});
    return g;
  }
  async seek(T) {
    const act = this.active(T);
    // 預載下一場
    const nx = this.film.scenes[act[act.length - 1].i + 1];
    await Promise.all(act.map(a => this.loadScene(a.sc.id)));
    if (nx) this.loadScene(nx.id);
    act.forEach((a, k) => this.drawScene(k, a, T));
    const gl = this.gl;
    // 字幕
    const cx = this.cap.getContext('2d'); cx.setTransform(1, 0, 0, 1, 0, 0); cx.clearRect(0, 0, VW, VH);
    for (let c of this.film.captions) if (T >= c.t0 - 0.1 && T < c.t1 + 0.1) {
      if (c.at) {   // 箭頭指向場景座標 [x, y, 景深]
        const a = act.find(a => a.i === c.sci); if (!a) continue;
        const ent = this.cache.get(a.sc.id); const v = this.view(this.camFor(ent, a.sc, a.lt), c.at[2] ?? 0.5);
        c = { ...c, to: v.P(c.at[0], c.at[1]) };
      }
      drawCaption(cx, c, T);
    }
    this.capTex = this.texFromCanvas(this.cap, this.capTex);
    // 合成
    gl.bindFramebuffer(gl.FRAMEBUFFER, null); gl.viewport(0, 0, VW, VH);
    gl.disable(gl.BLEND); gl.useProgram(this.P.p);
    const u = this.P.u;
    const two = act.length > 1;
    let p = 0;
    if (two) { const a = act[0], tr = a.sc.trans ?? 1.5; p = clamp((a.lt - (a.sc.dur - tr)) / tr); }
    const gA = this.gradeOf(act[0]), gB = two ? this.gradeOf(act[1]) : gA;
    const bind = (name, tex, unit) => { gl.activeTexture(gl.TEXTURE0 + unit); gl.bindTexture(gl.TEXTURE_2D, tex); gl.uniform1i(u[name], unit); };
    bind('A', this.fbo[0].t, 0); bind('B', this.fbo[1].t, 1); bind('paper', this.paper.tex, 2);
    bind('noise', this.noise.tex, 3); bind('cap', this.capTex, 4);
    gl.uniform1f(u.p, p); gl.uniform1f(u.twoScenes, two ? 1 : 0); gl.uniform1f(u.frame, Math.round(T * 30) % 97);
    gl.uniform4f(u.gA1, gA.expo, gA.con, gA.sat, gA.warm); gl.uniform3f(u.gA2, ...gA.tint);
    gl.uniform4f(u.gB1, gB.expo, gB.con, gB.sat, gB.warm); gl.uniform3f(u.gB2, ...gB.tint);
    const F = this.film;
    const fin = F.fadeIn ?? 1.2, fout = F.fadeOut ?? 2.0;
    let fade = Math.max(1 - clamp(T / fin), clamp((T - (this.duration - fout)) / fout));
    gl.uniform1f(u.fade, ease(fade)); gl.uniform3f(u.fadeCol, ...(F.fadeCol ?? [0.972, 0.958, 0.925]));
    gl.uniform1f(u.paperK, 1.0); gl.uniform1f(u.vig, F.vig ?? 0.28); gl.uniform1f(u.grainK, 0.018);
    gl.uniform2f(u.uO, 0, 0); gl.uniform2f(u.uU, VW, 0); gl.uniform2f(u.uV, 0, VH);
    gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    gl.finish();
  }
}
