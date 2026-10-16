"""程序化水彩引擎 (numpy + OpenCV)

物理模型（簡化版 Kubelka–Munk 透明疊色）：
  每一層紙面保存「透射率」T (H,W,3)，白紙 = 1。每上一遍水彩，
  T *= exp(-吸收係數 * 濃度)。顏料以「在白紙上滿濃度時的反射色」描述。
  因此兩遍黃 + 一遍藍 會真實地疊出綠，而不是 alpha 混合。

水彩特徵：
  - 紙紋顆粒 (granulation)：顏料沉積在紙紋凹處
  - 邊緣積色 (edge darkening)：水分蒸發時顏料被帶到水跡邊緣
  - 濕畫暈染 (wet bloom)：大半徑擴散 + 水漬回流 (backrun)
  - 濃度不均 (pooling)：低頻噪聲調製
鋼筆墨線：
  - 樣條重採樣、垂直方向低頻手抖、壓感粗細、起筆頓、收筆尖、乾筆飛白
"""
import numpy as np
import cv2

F32 = np.float32


# ----------------------------------------------------------------- noise
def fbm(h, w, cells, rng, octaves=5, persist=0.5):
    """分形值噪聲, 範圍約 0..1。cells = 最低頻沿寬度方向的格數"""
    acc = np.zeros((h, w), F32)
    amp, tot = 1.0, 0.0
    for o in range(octaves):
        gw = max(2, int(cells * 2 ** o))
        gh = max(2, int(gw * h / w) + 1)
        g = rng.random((gh, gw)).astype(F32)
        acc += amp * cv2.resize(g, (w, h), interpolation=cv2.INTER_CUBIC)
        tot += amp
        amp *= persist
    acc /= tot
    lo, hi = np.percentile(acc[::8, ::8], [1, 99])
    return np.clip((acc - lo) / (hi - lo + 1e-6), 0, 1).astype(F32)


def noise1d(n, cells, rng, octaves=3):
    """1D 平滑噪聲, 範圍 -1..1"""
    out = np.zeros(n, F32)
    amp, tot = 1.0, 0.0
    x = np.linspace(0, 1, n)
    for o in range(octaves):
        k = max(2, int(cells * 2 ** o)) + 1
        g = rng.uniform(-1, 1, k)
        xs = np.linspace(0, 1, k)
        # 三次插值
        from scipy.interpolate import CubicSpline
        out += amp * CubicSpline(xs, g)(x).astype(F32)
        tot += amp
        amp *= 0.5
    return out / tot


def blur(a, sigma):
    if sigma <= 0:
        return a
    k = int(sigma * 3) * 2 + 1
    return cv2.GaussianBlur(a, (k, k), sigma)


def bbox(m, pad, h=None, w=None, thr=1e-4):
    """非零區域的包圍盒 (y0, y1, x0, x1)，向外擴 pad；全空回傳 None"""
    h = h or m.shape[0]; w = w or m.shape[1]
    rows = np.flatnonzero((m > thr).any(axis=1))
    if not len(rows):
        return None
    cols = np.flatnonzero((m > thr).any(axis=0))
    pad = int(pad)
    return (max(0, rows[0] - pad), min(h, rows[-1] + pad + 1), max(0, cols[0] - pad), min(w, cols[-1] + pad + 1))


def lblur(m, sigma):
    """只在非零區域附近做高斯模糊"""
    if sigma <= 0:
        return m
    b = bbox(m, sigma * 3 + 2)
    if b is None:
        return m
    y0, y1, x0, x1 = b
    out = np.zeros_like(m)
    out[y0:y1, x0:x1] = blur(np.ascontiguousarray(m[y0:y1, x0:x1]), sigma)
    return out


# ----------------------------------------------------------------- paper
class Paper:
    def __init__(self, w, h, seed=7):
        rng = np.random.default_rng(seed)
        self.w, self.h = w, h
        coarse = fbm(h, w, max(60, w // 5), rng, octaves=2)
        fine = blur(rng.random((h, w)).astype(F32), 0.8)
        fine = (fine - fine.min()) / (np.ptp(fine) + 1e-6)
        g = 0.55 * coarse + 0.45 * fine
        # 紙纖維
        fib = np.zeros((h, w), F32)
        for _ in range(int(w * h / 2500)):
            x, y = rng.uniform(0, w), rng.uniform(0, h)
            a = rng.uniform(0, np.pi)
            L = rng.uniform(6, 26)
            cv2.line(fib, (int(x), int(y)),
                     (int(x + L * np.cos(a)), int(y + L * np.sin(a))),
                     float(rng.uniform(0.3, 1)), 1, cv2.LINE_AA)
        g = np.clip(g - 0.18 * blur(fib, 0.6), 0, 1)
        self.grain = g.astype(F32)                      # 1 = 紙紋凸起
        self.tint = np.array([0.972, 0.958, 0.925], F32)  # 暖白水彩紙 (RGB)

    def texture_rgb(self):
        """整張紙的明暗紋理 (供最終合成時乘上)"""
        g = self.grain
        shade = 1.0 - 0.045 * (1 - g)
        return np.clip(shade[..., None] * self.tint[None, None, :], 0, 1)


# ----------------------------------------------------------------- masks
class Shapes:
    """形狀遮罩生成器；所有遮罩都帶水彩式的不規則邊緣"""

    def __init__(self, w, h, rng):
        self.w, self.h, self.rng = w, h, rng
        self._disp = {}

    def disp(self, scale):
        if scale not in self._disp:
            cells = max(4, int(self.w / scale))
            dx = (fbm(self.h, self.w, cells, self.rng, 4) - 0.5) * 2
            dy = (fbm(self.h, self.w, cells, self.rng, 4) - 0.5) * 2
            self._disp[scale] = (dx, dy)
        return self._disp[scale]

    def roughen(self, m, amp=4.0, scale=60):
        """以噪聲位移場扭曲遮罩邊緣"""
        if amp <= 0:
            return m
        dx, dy = self.disp(scale)
        if not hasattr(self, '_grid'):
            self._grid = np.meshgrid(np.arange(self.w, dtype=F32), np.arange(self.h, dtype=F32))
        xs, ys = self._grid
        m = m.astype(F32)
        b = bbox(m, abs(amp) + 3)
        if b is None:
            return m
        y0, y1, x0, x1 = b
        full = (y1 - y0) * (x1 - x0) > 0.6 * self.w * self.h
        if full:
            return cv2.remap(m, (xs + dx * amp).astype(F32), (ys + dy * amp).astype(F32), cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_REPLICATE)
        mx = (xs[y0:y1, x0:x1] + dx[y0:y1, x0:x1] * amp - x0).astype(F32)
        my = (ys[y0:y1, x0:x1] + dy[y0:y1, x0:x1] * amp - y0).astype(F32)
        out = np.zeros_like(m)
        out[y0:y1, x0:x1] = cv2.remap(np.ascontiguousarray(m[y0:y1, x0:x1]), mx, my, cv2.INTER_LINEAR,
                                      borderMode=cv2.BORDER_CONSTANT, borderValue=0)
        return out

    def blank(self):
        return np.zeros((self.h, self.w), F32)

    def poly(self, pts, rough=4, scale=60, feather=0.8):
        m = self.blank()
        p = np.round(np.asarray(pts, np.float64) * 16).astype(np.int32)
        cv2.fillPoly(m, [p], 1.0, cv2.LINE_AA, shift=4)
        m = self.roughen(m, rough, scale)
        return lblur(m, feather)

    def ellipse(self, cx, cy, rx, ry, ang=0, rough=4, scale=50, feather=0.8):
        m = self.blank()
        cv2.ellipse(m, (int(cx * 16), int(cy * 16)), (int(rx * 16), int(ry * 16)),
                    ang, 0, 360, 1.0, -1, cv2.LINE_AA, shift=4)
        m = self.roughen(m, rough, scale)
        return lblur(m, feather)

    def blob(self, cx, cy, r, n=9, spread=0.6, rough=6, squash=1.0):
        """一團樹冠／雲：多個橢圓疊合"""
        m = self.blank()
        rng = self.rng
        for i in range(n):
            a = rng.uniform(0, 2 * np.pi)
            d = rng.uniform(0, r * spread)
            rr = r * rng.uniform(0.45, 0.8)
            x = cx + np.cos(a) * d
            y = cy + np.sin(a) * d * squash * 0.8
            cv2.ellipse(m, (int(x * 16), int(y * 16)), (int(rr * 16), int(rr * squash * 16)),
                        0, 0, 360, 1.0, -1, cv2.LINE_AA, shift=4)
        m = self.roughen(m, rough, max(20, r * 0.6))
        return lblur(m, 1.0)

    def below_curve(self, ys, rough=3):
        """曲線以下的區域；ys 長度 = w"""
        yy = np.arange(self.h, dtype=F32)[:, None]
        m = np.clip(yy - ys[None, :] + 0.5, 0, 1).astype(F32)
        return self.roughen(m, rough, 40)

    def ridge(self, base, amp, cells, rng=None, octaves=4, sharp=0.0):
        """山脊輪廓：回傳 ys"""
        rng = rng or self.rng
        n = noise1d(self.w, cells, rng, octaves)
        if sharp:
            n = np.sign(n) * np.abs(n) ** (1 - sharp)
        return base - amp * (n * 0.5 + 0.5)

    def vgrad(self, y0, y1):
        yy = np.arange(self.h, dtype=F32)[:, None]
        g = np.clip((yy - y0) / (y1 - y0 + 1e-6), 0, 1)
        return np.repeat(g, self.w, axis=1)

    def radial(self, cx, cy, r):
        if not hasattr(self, '_grid'):
            self._grid = np.meshgrid(np.arange(self.w, dtype=F32), np.arange(self.h, dtype=F32))
        xs, ys = self._grid
        d = np.sqrt((xs - cx) ** 2 + (ys - cy) ** 2) / r
        return np.clip(1 - d, 0, 1)


# ----------------------------------------------------------------- layer
def _pig(color):
    c = np.clip(np.asarray(color, F32), 0.02, 1.0)
    return -np.log(c)  # 吸收係數


class Layer:
    def __init__(self, w, h, paper, rng):
        self.w, self.h = w, h
        self.paper = paper
        self.rng = rng
        self.T = np.ones((h, w, 3), F32)
        self.cov = np.zeros((h, w), F32)
        self.S = Shapes(w, h, rng)
        self._pool = None

    def pool(self):
        if self._pool is None:
            self._pool = fbm(self.h, self.w, 3, self.rng, 4, persist=0.42)
        return self._pool

    # ---- 透明水彩一遍
    def wash(self, mask, color, density=0.7, edge=0.6, gran=0.5, bloom=0.0,
             var=0.25, cover=1.0, backrun=0.0, occlude=True):
        m = np.clip(mask, 0, 1).astype(F32)
        b = bbox(m, max(bloom * 3, 3.5 * 3) + 4)
        if b is None:
            return
        y0, y1, x0, x1 = b
        sl = (slice(y0, y1), slice(x0, x1))
        m = np.ascontiguousarray(m[sl])
        if bloom > 0:  # 濕畫：顏料向外擴散，中心變淡
            spread = blur(m, bloom)
            m = np.clip(0.55 * m + 0.75 * spread, 0, 1) * np.clip(spread * 3, 0, 1)
        d = m * density
        # 濃度不均（沉積、水跡）
        pool = self.pool()[sl]
        d *= 1 + var * (pool - 0.5) * 2
        # 紙紋顆粒：顏料積在凹處 (grain 低處)
        d *= 1 + gran * 0.55 * (0.5 - self.paper.grain[sl]) * 2
        # 邊緣積色
        if edge > 0:
            inner = blur(m, 3.5)
            e = np.clip(m - inner, 0, 1) * 2.6 + np.clip(m - blur(m, 1.5), 0, 1) * 2.5
            d += e * edge * density
        if backrun > 0:  # 水漬回流：花椰菜狀淺色斑
            br = fbm(self.h, self.w, 18, self.rng, 3)[sl]
            ring = np.abs(br - 0.5) < 0.04
            d *= 1 - backrun * 0.5 * blur(ring.astype(F32), 2.5)
        d = np.clip(d, 0, 3)
        self.T[sl] *= np.exp(-_pig(color)[None, None, :] * d[..., None])
        if occlude:
            self.cov[sl] = np.maximum(self.cov[sl], np.clip(m * cover * 1.6, 0, 1))

    def lift(self, mask, amount=0.6):
        """洗白／留白：把顏料提起來"""
        b = bbox(mask, 1)
        if b is None:
            return
        sl = (slice(b[0], b[1]), slice(b[2], b[3]))
        m = np.clip(mask[sl], 0, 1)[..., None] * amount
        self.T[sl] = self.T[sl] * (1 - m) + m

    def clip(self, mask):
        """只保留 mask 內的畫面（其餘還原成白紙、透明）"""
        m = np.clip(mask, 0, 1)
        self.T = 1 - (1 - self.T) * m[..., None]
        self.cov *= m

    # ---- 鋼筆墨線
    def ink(self, pts, width=2.2, color=(0.10, 0.08, 0.07), tremor=0.8, dark=0.9,
            taper=(0.15, 0.3), dry=0.0, press=None, occlude=True, smooth=2):
        pts = np.asarray(pts, F32)
        if len(pts) < 2:
            return
        # chaikin 平滑（smooth=0 保留硬角）
        for _ in range(smooth):
            if len(pts) < 3:
                break
            q = 0.75 * pts[:-1] + 0.25 * pts[1:]
            r = 0.25 * pts[:-1] + 0.75 * pts[1:]
            pts = np.concatenate([pts[:1], np.stack([q, r], 1).reshape(-1, 2), pts[-1:]])
        seg = np.linalg.norm(np.diff(pts, axis=0), axis=1)
        s = np.concatenate([[0], np.cumsum(seg)])
        L = s[-1]
        if L < 1:
            return
        n = max(4, int(L / 0.9))
        t = np.linspace(0, L, n)
        x = np.interp(t, s, pts[:, 0])
        y = np.interp(t, s, pts[:, 1])
        dx, dy = np.gradient(x), np.gradient(y)
        nl = np.sqrt(dx * dx + dy * dy) + 1e-6
        nx, ny = -dy / nl, dx / nl
        # 手抖：低頻 + 極細高頻
        cells = max(2, int(L / 40))
        jit = noise1d(n, cells, self.rng, 3) * tremor * 1.4
        jit += self.rng.normal(0, 0.08 * tremor, n)
        x = x + nx * jit
        y = y + ny * jit
        u = t / L
        # 壓感：起筆頓（略粗）→ 行筆 → 收筆尖
        if press is None:
            p = 0.75 + 0.35 * noise1d(n, max(2, int(L / 70)), self.rng, 2)
        else:
            p = np.interp(u, np.linspace(0, 1, len(press)), press)
        a0, a1 = taper
        start = np.clip(u / max(a0, 1e-3), 0, 1)
        start = 0.55 + 0.45 * np.sin(start * np.pi / 2) + 0.25 * np.exp(-((u - a0 * 0.4) / (a0 * 0.35 + 1e-3)) ** 2)
        end = np.clip((1 - u) / max(a1, 1e-3), 0, 1) ** 0.7
        wv = width * p * start * (0.12 + 0.88 * end)
        # 繪製到局部 alpha
        x0, x1 = int(max(0, x.min() - width * 3)), int(min(self.w, x.max() + width * 3 + 1))
        y0, y1 = int(max(0, y.min() - width * 3)), int(min(self.h, y.max() + width * 3 + 1))
        if x1 <= x0 or y1 <= y0:
            return
        A = np.zeros((y1 - y0, x1 - x0), F32)
        for xi, yi, wi in zip(x - x0, y - y0, wv):
            r = max(wi * 0.5, 0.35)
            cv2.circle(A, (int(xi * 16), int(yi * 16)), int(r * 16), 1.0, -1, cv2.LINE_AA, shift=4)
        g = self.paper.grain[y0:y1, x0:x1]
        if dry > 0:  # 乾筆飛白：紙紋凸起處沾不到墨
            A *= np.clip(1 - dry * 2.2 * np.clip(g - 0.45, 0, 1) * 2, 0, 1)
        A *= 0.85 + 0.15 * (1 - g)
        A = np.clip(A, 0, 1) * dark
        ab = _pig(color)
        self.T[y0:y1, x0:x1] *= np.exp(-ab[None, None, :] * A[..., None] * 1.0)
        if occlude:
            self.cov[y0:y1, x0:x1] = np.maximum(self.cov[y0:y1, x0:x1], A)

    def box(self, x0, y0, x1, y1, width=2.0, **kw):
        """手繪方框：四條獨立的直筆，略有出頭"""
        r = self.rng
        o = lambda: r.uniform(-1, 1) * width * 1.5
        for a, b in [((x0 - width * 2, y0 + o()), (x1 + width * 2, y0 + o())), ((x1 + o(), y0 - width * 2), (x1 + o(), y1 + width * 2)),
                     ((x1 + width * 2, y1 + o()), (x0 - width * 2, y1 + o())), ((x0 + o(), y1 + width * 2), (x0 + o(), y0 - width * 2))]:
            self.ink([a, b], width=width, smooth=0, **kw)

    def ink_stroke_set(self, strokes, **kw):
        for s in strokes:
            self.ink(s, **kw)

    # ---- 輸出
    def to_rgba(self, opaque=False):
        """回傳 (RGB 非預乘, alpha)；在白紙上合成時與原畫完全一致"""
        C = self.T  # 白紙上的顏色
        if opaque:
            return np.clip(C, 0, 1), np.ones((self.h, self.w), F32)
        A = np.clip(blur(self.cov, 0.7), 0, 1)
        dark = (1 - C).max(axis=2)
        A = np.maximum(A, np.clip(dark * 1.15, 0, 1))
        U = 1 - (1 - C) / np.maximum(A, 1e-3)[..., None]
        return np.clip(U, 0, 1), A


def save_layer(path, rgb, a=None, quality=90):
    """rgb: float RGB 0..1"""
    bgr = (np.clip(rgb[..., ::-1], 0, 1) * 255 + 0.5).astype(np.uint8)
    if a is None:
        if path.endswith(".jpg"):
            cv2.imwrite(path, bgr, [cv2.IMWRITE_JPEG_QUALITY, 92])
        else:
            cv2.imwrite(path, bgr, [cv2.IMWRITE_WEBP_QUALITY, quality])
        return
    aa = (np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8)
    bgra = np.dstack([bgr, aa])
    cv2.imwrite(path, bgra, [cv2.IMWRITE_WEBP_QUALITY, quality])


def save_gray(path, g):
    cv2.imwrite(path, (np.clip(g, 0, 1) * 255 + 0.5).astype(np.uint8))
