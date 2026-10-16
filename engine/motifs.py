"""水彩母題庫：天空、山、樹、根、房屋、城堡、宮殿、人物……
每個函數都只往 Layer 上「畫」——一遍遍上水彩、勾墨線。座標是畫布像素。
"""
import numpy as np
import cv2
from wc import Layer, Paper, blur, lblur, fbm, noise1d, F32

INK = (0.13, 0.10, 0.09)
INK_BLUE = (0.16, 0.18, 0.26)
INK_BROWN = (0.30, 0.20, 0.14)


def mix(a, b, t):
    return tuple(float(x) * (1 - t) + float(y) * t for x, y in zip(a, b))


# ================================================================ sky
def sky(L, top, horizon, y_h=None, density=0.75, glow=None, bloom=40):
    """濕畫法天空：先上地平線暖色，再趁濕從上往下壓天頂色"""
    S, H = L.S, L.h
    y_h = y_h or H * 0.65
    L.wash(np.ones((L.h, L.w), F32), horizon, density=density * 0.6, edge=0, gran=0.12, var=0.15)
    m = 1 - S.vgrad(H * 0.02, y_h)
    m = m ** 1.3
    L.wash(m, top, density=density, edge=0, gran=0.15, bloom=bloom, var=0.3)
    if glow is not None:
        gx, gy, gr, gc = glow
        L.lift(S.radial(gx, gy, gr) ** 1.5, 0.7)
        L.wash(S.radial(gx, gy, gr * 1.6) ** 2, gc, density=0.5, edge=0, gran=0.2)


def clouds(L, n, y0, y1, color, rmin=40, rmax=120, squash=0.45, density=0.35, lift=True, rng=None):
    rng = rng or L.rng
    S = L.S
    for _ in range(n):
        x = rng.uniform(-50, L.w + 50)
        y = rng.uniform(y0, y1)
        r = rng.uniform(rmin, rmax)
        m = S.blob(x, y, r, n=7, spread=1.4, squash=squash, rough=r * 0.15)
        if lift:
            L.lift(lblur(m, 4) * 0.9, 0.45)
        # 雲底陰影
        sh = m * S.vgrad(y - r * 0.2, y + r * 0.5)
        L.wash(lblur(sh, 3), color, density=density, edge=0.5, gran=0.3, bloom=6)


def moon(L, x, y, r, color=(0.97, 0.93, 0.80)):
    m = L.S.ellipse(x, y, r, r, rough=1.5, feather=1.2)
    L.lift(lblur(m, 2), 0.95)
    L.lift(L.S.radial(x, y, r * 3) ** 2, 0.35)
    L.wash(m, color, density=0.3, edge=0.6, gran=0.2)


# ================================================================ land
def mountains(L, base, amp, color, cells=3, sharp=0.2, density=0.8, ink=0.0,
              shade=None, snow=False, rng=None):
    S = L.S
    ys = S.ridge(base, amp, cells, rng=rng, sharp=sharp)
    m = S.below_curve(ys, rough=3)
    L.wash(m, color, density=density, edge=0.7, gran=0.45)
    # 背光面：山脊下方漸淡
    fade = np.clip((np.arange(L.h, dtype=F32)[:, None] - ys[None, :]) / (amp * 1.2 + 1), 0, 1)
    L.wash(m * (1 - fade) ** 2 * 0.8, shade or color, density=density * 0.5, edge=0.0, gran=0.3, bloom=8)
    if snow:
        depth = np.arange(L.h, dtype=F32)[:, None] - ys[None, :]
        high = np.clip(((base - ys) / amp - 0.5) / 0.3, 0, 1).astype(F32)
        cap = m * np.clip(1 - depth / (amp * 0.22 * (0.4 + high[None, :])), 0, 1) * high[None, :]
        capr = L.S.roughen(cap, 9, 22)
        snowm = blur((capr > 0.3).astype(F32), 1.2) * m
        L.lift(snowm, 0.88)
        L.wash(snowm * L.S.vgrad(base - amp, base), (0.80, 0.84, 0.94), density=0.35, edge=0.6, gran=0.2, occlude=False)
    if ink > 0:
        ridge_ink(L, ys, ink)
    return ys


def ridge_ink(L, ys, width, gap=0.35, color=INK):
    rng = L.rng
    x = 0
    while x < L.w - 10:
        seg = int(rng.uniform(60, 260))
        if rng.random() > gap:
            xs = np.arange(x, min(L.w - 1, x + seg), 6)
            if len(xs) > 2:
                L.ink(np.stack([xs, ys[xs] + 1], 1), width=width * rng.uniform(0.6, 1.2),
                      color=color, dry=0.4, dark=0.75)
        x += seg + int(rng.uniform(10, 80))


def ground(L, base, amp, color, cells=4, density=0.85, second=None, ink=0.0):
    S = L.S
    ys = S.ridge(base, amp, cells, sharp=0.0)
    m = S.below_curve(ys, rough=2)
    L.wash(m, color, density=density, edge=0.6, gran=0.45)
    if second:
        # 濕中濕：在下半部壓另一種顏色
        L.wash(m * S.vgrad(base, L.h), second, density=density * 0.7, edge=0, bloom=25, gran=0.4)
    if ink:
        ridge_ink(L, ys, ink, gap=0.55)
    return ys


def water(L, y0, y1, color, sky_col=None):
    S = L.S
    m = S.vgrad(y0 - 1, y0 + 1) * (1 - S.vgrad(y1 - 1, y1 + 1))
    L.wash(m, color, density=0.6, edge=0.4, gran=0.3)
    # 水平筆觸的倒影高光
    rng = L.rng
    for _ in range(int((y1 - y0) / 6)):
        y = rng.uniform(y0 + 4, y1 - 4)
        x = rng.uniform(0, L.w)
        w = rng.uniform(60, 300)
        L.lift(S.ellipse(x, y, w, 1.6, rough=1, feather=0.8), 0.5)
    for _ in range(int((y1 - y0) / 14)):
        y = rng.uniform(y0 + 6, y1)
        x = rng.uniform(0, L.w)
        w = rng.uniform(30, 140)
        L.ink([(x, y), (x + w, y + rng.uniform(-1, 1))], width=1.0, color=INK_BLUE, dark=0.35, dry=0.5)


def field_strokes(L, ys_top, y_bot, color, density=0.6, n=900, h=(10, 26), ink_col=INK_BROWN):
    """麥田／草：大量短筆觸"""
    rng = L.rng
    for _ in range(n):
        x = rng.uniform(0, L.w)
        yt = ys_top[int(np.clip(x, 0, L.w - 1))]
        y = rng.uniform(yt + 4, y_bot)
        k = (y - yt) / max(1, y_bot - yt)
        hh = rng.uniform(*h) * (0.5 + k)
        lean = rng.uniform(-0.3, 0.3) * hh
        L.ink([(x, y), (x + lean * 0.5, y - hh * 0.6), (x + lean, y - hh)],
              width=0.8 + 1.2 * k, color=ink_col, dark=0.35 + 0.3 * k, dry=0.3, tremor=0.4)


# ================================================================ trees
def tree_round(L, x, yg, h, green=(0.55, 0.68, 0.36), shadow=(0.38, 0.45, 0.42),
               trunk=INK_BROWN, ink=True, light=0.0):
    S, rng = L.S, L.rng
    r = h * 0.42
    cy = yg - h + r
    m = S.blob(x, cy, r, n=10, spread=0.55, rough=r * 0.12)
    # 樹幹
    tw = max(2.0, h * 0.045)
    L.wash(S.poly([(x - tw, yg), (x - tw * 0.6, cy), (x + tw * 0.6, cy), (x + tw, yg)], rough=1),
           (0.55, 0.42, 0.32), density=0.9, edge=0.5)
    L.wash(m, green, density=0.85, edge=0.75, gran=0.5)
    # 陰影：右下
    sh = m * np.clip(S.radial(x + r * 0.5, cy + r * 0.7, r * 1.4) * 1.4, 0, 1)
    L.wash(S.roughen(sh, r * 0.1, r * 0.4), shadow, density=0.75, edge=0.6, gran=0.4)
    if light:
        L.lift(S.blob(x - r * 0.35, cy - r * 0.35, r * 0.45, n=4) * m, light)
    if ink:
        L.ink([(x, yg + 2), (x + rng.uniform(-2, 2), cy + r * 0.5), (x + rng.uniform(-4, 4), cy)],
              width=tw * 0.9, color=trunk, dark=0.85)
        # 殘缺的樹冠輪廓
        k = int(rng.integers(2, 4))
        for i in range(k):
            a0 = rng.uniform(0.1, 1.0) * np.pi + np.pi * 0.0
            a = np.linspace(a0, a0 + rng.uniform(0.5, 1.1), 10)
            rr = r * rng.uniform(0.85, 1.0)
            pts = [(x + np.cos(t) * rr * 1.0, cy - np.sin(t) * rr * 0.95) for t in a]
            L.ink(pts, width=max(1.0, h * 0.012), color=INK, dark=0.55, dry=0.5)
    return m


def tree_pine(L, x, yg, h, color=(0.36, 0.48, 0.42), snow=False, ink=True):
    S, rng = L.S, L.rng
    tiers = 5
    w = h * 0.36
    for i in range(tiers):
        t0 = i / tiers
        top = yg - h + t0 * h * 0.85
        bot = top + h * 0.3
        ww = w * (0.3 + 0.75 * t0)
        pts = [(x, top), (x + ww * 0.55, top + (bot - top) * 0.6), (x + ww, bot),
               (x, bot - h * 0.03), (x - ww, bot), (x - ww * 0.55, top + (bot - top) * 0.6)]
        m = S.poly(pts, rough=h * 0.012, scale=20)
        L.wash(m, color, density=0.85, edge=0.7, gran=0.4)
        if snow:
            L.lift(S.poly([(x, top), (x + ww * 0.6, top + (bot - top) * 0.55),
                           (x - ww * 0.6, top + (bot - top) * 0.55)], rough=2), 0.9)
    if ink:
        L.ink([(x, yg), (x, yg - h * 0.95)], width=max(1.2, h * 0.02), color=INK, dark=0.7)


def branches(L, x, y, ang, length, width, depth, rng, out=None, color=INK, tmap=None, t0=0.0, tspan=1.0,
             spread=0.45, shrink=0.72, droop=0.0, clamp=None):
    """遞迴分枝；可同時寫入生長時間圖 tmap；clamp=(amin,amax) 限制方向"""
    if depth <= 0 or length < 3:
        return
    n = 6
    pts = []
    a = ang
    cx, cy = x, y
    for i in range(n + 1):
        pts.append((cx, cy))
        a += rng.normal(0, 0.12) + droop
        if clamp:
            a = float(np.clip(a, *clamp))
        cx += np.cos(a) * length / n
        cy += np.sin(a) * length / n
    L.ink(pts, width=width, color=color, dark=0.8, taper=(0.05, 0.25), tremor=0.6)
    if tmap is not None:
        _paint_t(tmap, pts, width + 3, t0, t0 + tspan)
    k = 2 if depth > 1 else 0
    if rng.random() < 0.35:
        k = 3
    for j in range(k):
        na = a + rng.uniform(-spread, spread) + (j - (k - 1) / 2) * spread
        if clamp:
            na = float(np.clip(na, *clamp))
        branches(L, cx, cy, na, length * rng.uniform(shrink - 0.08, shrink + 0.08),
                 width * 0.68, depth - 1, rng, color=color, tmap=tmap,
                 t0=t0 + tspan, tspan=tspan * 0.9, spread=spread, shrink=shrink, droop=droop, clamp=clamp)


def _paint_t(tmap, pts, w, ta, tb):
    """沿折線把時間值寫入 tmap（取最小值）"""
    pts = np.asarray(pts)
    n = len(pts)
    for i in range(n - 1):
        t = ta + (tb - ta) * i / (n - 1)
        tmp = np.full_like(tmap, 9.0)
        cv2.line(tmp, tuple(int(v) for v in pts[i]), tuple(int(v) for v in pts[i + 1]), float(t),
                 int(max(2, w)), cv2.LINE_AA)
        np.minimum(tmap, tmp, out=tmap)


def ribbon(pts, w0, w1):
    """沿折線生成由 w0 漸細到 w1 的多邊形"""
    pts = np.asarray(pts, F32)
    d = np.gradient(pts, axis=0)
    n = np.stack([-d[:, 1], d[:, 0]], 1)
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-6
    w = np.linspace(w0, w1, len(pts))[:, None] / 2
    return np.concatenate([pts + n * w, (pts - n * w)[::-1]])


def canopy_contour_ink(L, m, width=1.4, frac=0.45, dark=0.55):
    """沿樹冠／雲團輪廓隨機勾幾段殘缺墨線"""
    rng = L.rng
    cs, _ = cv2.findContours((m > 0.5).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in cs:
        c = c[:, 0, :].astype(F32)
        if len(c) < 40:
            continue
        i = 0
        while i < len(c) - 10:
            seg = int(rng.uniform(25, 120))
            if rng.random() < frac:
                L.ink(c[i:i + seg:3], width=width, dark=dark, dry=0.5, tremor=0.5)
            i += seg + int(rng.uniform(20, 140))


def big_tree(L, x, yg, h, green=(0.50, 0.64, 0.34), shadow=(0.32, 0.42, 0.40), seed_rng=None,
             tmap=None, autumn=None, bare=False, light=(0.80, 0.84, 0.50)):
    """大樹：水彩樹幹 + 墨線輪廓 + 一整團合併的樹冠（陰影、亮部、殘缺勾線）"""
    rng = seed_rng or L.rng
    S = L.S
    rr = np.random.default_rng(int(rng.integers(1 << 30)))
    limbs, tips = [], []

    def rec(px, py, a, ln, w, d, t):
        pts = [(px, py)]
        cx, cy = px, py
        for i in range(6):
            a += rr.normal(0, 0.08)
            cx += np.cos(a) * ln / 6
            cy += np.sin(a) * ln / 6
            pts.append((cx, cy))
        limbs.append((pts, w, w * 0.62, d, t))
        if d == 1:
            tips.append((cx, cy, t + 0.18))
            return
        k = 2 if rr.random() < 0.75 else 3
        for j in range(k):
            na = a + (j - (k - 1) / 2) * rr.uniform(0.6, 0.9) + rr.normal(0, 0.1)
            na += (-np.pi / 2 - na) * 0.18
            rec(cx, cy, na, ln * rr.uniform(0.66, 0.76), w * 0.64, d - 1, t + 0.15)

    rec(x, yg, -np.pi / 2 + rr.normal(0, 0.04), h * 0.30, h * 0.085, 5, 0.0)
    bark = (0.52, 0.42, 0.36)
    for pts, w0, w1, d, t in limbs:
        if d < 2 and not bare:
            continue
        poly = ribbon(pts, w0, w1)
        L.wash(S.poly(poly, rough=1.0, scale=12, feather=0.6), bark, density=0.95, edge=0.7, gran=0.5)
        side = ribbon([(px + w0 * 0.18, py) for px, py in pts], w0 * 0.45, w1 * 0.45)
        L.wash(S.poly(side, rough=0.8, feather=0.6), (0.36, 0.30, 0.32), density=0.7, edge=0.4)
        if tmap is not None:
            _paint_t(tmap, pts, w0 + 4, t, t + 0.18)
        if d >= 3:
            n = len(pts)
            L.ink(poly[:n], width=max(1.0, h * 0.004), dark=0.7, dry=0.3)
            L.ink(poly[n:], width=max(1.0, h * 0.005), dark=0.8, dry=0.3)
        else:
            L.ink(pts, width=max(1.0, w0 * 0.25), dark=0.55, dry=0.4)
    for k in range(4):
        a = np.pi * (0.15 + 0.7 * k / 3)
        L.ink([(x + np.cos(a) * h * 0.04, yg - 4), (x + np.cos(a) * h * 0.1, yg + 6)], width=max(1, h * 0.006), dark=0.6)
    if bare:
        return [(a, b) for a, b, _ in tips]
    cols = [green] if autumn is None else autumn
    U = S.blank()
    blobs = []
    for i, (tx, ty, tt) in enumerate(tips):
        r = h * rr.uniform(0.09, 0.13)
        m = S.blob(tx, ty - r * 0.25, r, n=9, spread=0.8, rough=r * 0.18, squash=0.85)
        blobs.append((m, tx, ty, r, tt))
        U = np.maximum(U, m)
    L.wash(U, light, density=0.55, edge=0.5, gran=0.4, bloom=3)
    for i, (m, tx, ty, r, tt) in enumerate(blobs):
        L.wash(m * 0.9, cols[i % len(cols)], density=0.45, edge=0.15, gran=0.3, bloom=6, occlude=False)
    sh = U * np.clip(S.vgrad(yg - h * 0.95, yg - h * 0.35), 0, 1) ** 1.2
    for m, tx, ty, r, tt in blobs:
        sh = np.maximum(sh, m * S.vgrad(ty - r * 0.1, ty + r * 0.9) * 0.9)
    sh = S.roughen(sh, h * 0.012, h * 0.05)
    L.wash(sh, shadow, density=0.85, edge=0.75, gran=0.5)
    for m, tx, ty, r, tt in blobs[::2]:
        L.lift(lblur(S.blob(tx - r * 0.3, ty - r * 0.55, r * 0.35, n=4, rough=r * 0.1), 3) * U, 0.15)
    canopy_contour_ink(L, U, width=max(1.0, h * 0.0028), frac=0.4)
    if tmap is not None:
        for m, tx, ty, r, tt in blobs:
            mt = np.where(m > 0.15, tt + 0.1 * rr.random(), 9.0).astype(F32)
            np.minimum(tmap, mt, out=tmap)
    return [(a, b) for a, b, _ in tips]


def roots(L, x, y, depth_px, rng, tmap=None, width=7, n_main=5, color=(0.30, 0.20, 0.15)):
    for i in range(n_main):
        a = np.pi / 2 + (i - (n_main - 1) / 2) * (1.9 / n_main) + rng.normal(0, 0.06)
        branches(L, x, y, a, depth_px * rng.uniform(0.26, 0.34), width, 7, rng, color=color,
                 tmap=tmap, t0=0.0, tspan=0.14, spread=0.38, shrink=0.76, droop=0.0,
                 clamp=(np.pi * 0.12, np.pi * 0.88))


# ================================================================ buildings
def house(L, x, yg, w, h, roof=(0.72, 0.42, 0.34), wall=(0.92, 0.86, 0.74), win_light=False,
          chimney=True, ink=True, roof_h=None, windows=2):
    """回傳窗戶中心點列表 (供點燈)"""
    S, rng = L.S, L.rng
    roof_h = roof_h or h * 0.7
    x0, x1 = x - w / 2, x + w / 2
    top = yg - h
    L.wash(S.poly([(x0, yg), (x0, top), (x1, top), (x1, yg)], rough=1.2, scale=15), wall,
           density=0.8, edge=0.6, gran=0.3)
    # 側面陰影
    L.wash(S.poly([(x1 - w * 0.28, yg), (x1 - w * 0.28, top), (x1, top), (x1, yg)], rough=1), (0.70, 0.68, 0.72),
           density=0.5, edge=0.3)
    rp = [(x0 - w * 0.08, top + 2), (x - w * 0.05, top - roof_h), (x + w * 0.05, top - roof_h), (x1 + w * 0.08, top + 2)]
    L.wash(S.poly(rp, rough=1.5, scale=15), roof, density=0.9, edge=0.8, gran=0.5)
    if chimney:
        cx = x + w * 0.25
        L.wash(S.poly([(cx, top - roof_h * 0.3), (cx, top - roof_h * 0.95), (cx + w * 0.09, top - roof_h * 0.95),
                       (cx + w * 0.09, top - roof_h * 0.2)], rough=0.8), (0.55, 0.40, 0.36), density=0.9)
    wins = []
    ww, wh = w * 0.13, h * 0.26
    for i in range(windows):
        wx = x0 + w * (i + 1) / (windows + 1)
        wy = top + h * 0.38
        col = (0.95, 0.80, 0.45) if win_light else (0.36, 0.34, 0.40)
        L.wash(S.poly([(wx - ww / 2, wy), (wx + ww / 2, wy), (wx + ww / 2, wy + wh), (wx - ww / 2, wy + wh)],
                      rough=0.6), col, density=0.95, edge=0.4)
        wins.append((wx, wy + wh / 2, max(ww, wh)))
    if ink:
        lw = max(1.0, w * 0.018)
        L.ink([(x0, yg), (x0, top)], width=lw, dark=0.8)
        L.ink([(x1, top), (x1 + rng.uniform(-1, 1), yg)], width=lw, dark=0.8)
        L.ink(rp, width=lw * 1.1, dark=0.85)
        L.ink([(x0 - w * 0.1, yg + 1), (x1 + w * 0.1, yg + 1)], width=lw * 0.8, dark=0.6, dry=0.4)
        door_x = x1 - w * 0.18
        L.ink([(door_x - w * 0.06, yg), (door_x - w * 0.06, yg - h * 0.5), (door_x + w * 0.06, yg - h * 0.5),
               (door_x + w * 0.06, yg)], width=lw * 0.7, dark=0.7)
    return wins


def tower(L, x, yg, w, h, wall=(0.80, 0.76, 0.70), roof=(0.45, 0.48, 0.62), cone=True, ink=True):
    S, rng = L.S, L.rng
    x0, x1 = x - w / 2, x + w / 2
    top = yg - h
    L.wash(S.poly([(x0, yg), (x0 + w * 0.03, top), (x1 - w * 0.03, top), (x1, yg)], rough=1.2), wall,
           density=0.8, edge=0.6, gran=0.5)
    L.wash(S.poly([(x + w * 0.15, yg), (x + w * 0.15, top), (x1, top), (x1, yg)], rough=1),
           (0.62, 0.62, 0.70), density=0.5, edge=0.3)
    if cone:
        rp = [(x0 - w * 0.12, top), (x, top - w * 1.3), (x1 + w * 0.12, top)]
    else:  # 雉堞
        rp = []
        n = 4
        for i in range(n * 2 + 1):
            xx = x0 - w * 0.06 + (w * 1.12) * i / (n * 2)
            up = top - w * 0.22 if i % 2 == 0 else top - w * 0.08
            rp += [(xx, up)]
        rp = [(x0 - w * 0.06, top + w * 0.05)] + rp + [(x1 + w * 0.06, top + w * 0.05)]
    L.wash(S.poly(rp, rough=1), roof if cone else wall, density=0.9, edge=0.7)
    win = (x, top + h * 0.25, w * 0.18)
    L.wash(S.ellipse(x, top + h * 0.25, w * 0.08, w * 0.14, rough=0.5), (0.30, 0.30, 0.38), density=0.95)
    if ink:
        lw = max(1.0, w * 0.03)
        L.ink([(x0, yg), (x0 + w * 0.03, top)], width=lw)
        L.ink([(x1 - w * 0.03, top), (x1, yg)], width=lw)
        L.ink(rp, width=lw * 0.9, dark=0.8)
        for k in range(int(h / (w * 0.35))):  # 石塊肌理
            yy = top + rng.uniform(0.3, 1) * h
            xx = rng.uniform(x0 + 3, x1 - 10)
            L.ink([(xx, yy), (xx + w * 0.15, yy)], width=lw * 0.5, dark=0.35, dry=0.5)
    return win


def castle(L, x, yg, s, ink=True):
    wins = []
    L.wash(L.S.poly([(x - s, yg), (x - s, yg - s * 0.55), (x + s, yg - s * 0.55), (x + s, yg)], rough=1.5),
           (0.80, 0.76, 0.70), density=0.8, edge=0.6, gran=0.5)
    wins.append(tower(L, x - s, yg, s * 0.4, s * 0.95, cone=True, ink=ink))
    wins.append(tower(L, x + s, yg, s * 0.4, s * 0.85, cone=True, ink=ink))
    wins.append(tower(L, x, yg, s * 0.55, s * 1.35, cone=False, ink=ink))
    if ink:
        L.ink([(x - s, yg - s * 0.55), (x + s, yg - s * 0.55)], width=max(1, s * 0.012), dark=0.7)
    return wins


def church(L, x, yg, s, ink=True):
    house(L, x, yg, s * 1.6, s * 0.7, roof=(0.50, 0.50, 0.62), wall=(0.88, 0.84, 0.76), windows=3,
          chimney=False, ink=ink, roof_h=s * 0.4)
    w = tower(L, x - s * 0.6, yg, s * 0.42, s * 1.5, roof=(0.42, 0.45, 0.60), ink=ink)
    if ink:
        tx, ty = x - s * 0.6, yg - s * 1.5 - s * 0.42 * 1.3
        L.ink([(tx, ty), (tx, ty - s * 0.25)], width=1.5)
        L.ink([(tx - s * 0.07, ty - s * 0.17), (tx + s * 0.07, ty - s * 0.17)], width=1.5)
    return w


def cn_roof(L, x, y, w, h, color=(0.55, 0.30, 0.25), ink=True):
    """飛檐屋頂"""
    S = L.S
    pts = []
    for t in np.linspace(-1, 1, 21):
        yy = y - h * (1 - abs(t) ** 0.6)
        pts.append((x + t * w / 2, yy + h * 0.15 * abs(t) ** 6 * -1.6))
    pts = [(x - w / 2 - w * 0.03, y - h * 0.25)] + pts + [(x + w / 2 + w * 0.03, y - h * 0.25), (x + w * 0.42, y),
                                                          (x - w * 0.42, y)]
    L.wash(S.poly(pts, rough=1.2), color, density=0.9, edge=0.8, gran=0.4)
    if ink:
        L.ink(pts[:-2], width=max(1.2, w * 0.006), dark=0.85)


def palace(L, x, yg, s, wall=(0.70, 0.30, 0.25), roof=(0.82, 0.64, 0.30), ink=True):
    """帝都大殿：台基 + 紅牆 + 重檐金頂；回傳窗燈位置"""
    S = L.S
    # 台基
    L.wash(S.poly([(x - s * 1.25, yg), (x - s * 1.15, yg - s * 0.18), (x + s * 1.15, yg - s * 0.18),
                   (x + s * 1.25, yg)], rough=1.5), (0.82, 0.80, 0.76), density=0.8, edge=0.6)
    if ink:
        for k in range(5):
            yy = yg - s * 0.18 * k / 5
            L.ink([(x - s * 1.25 + k * 2, yy), (x + s * 1.25 - k * 2, yy)], width=1.0, dark=0.5, dry=0.4)
    b = yg - s * 0.18
    L.wash(S.poly([(x - s * 0.95, b), (x - s * 0.95, b - s * 0.42), (x + s * 0.95, b - s * 0.42), (x + s * 0.95, b)],
                  rough=1), wall, density=0.85, edge=0.6, gran=0.4)
    wins = []
    for i in range(9):
        cx = x - s * 0.84 + i * s * 0.21
        L.wash(S.poly([(cx - s * 0.06, b), (cx - s * 0.06, b - s * 0.3), (cx + s * 0.06, b - s * 0.3),
                       (cx + s * 0.06, b)], rough=0.5), (0.40, 0.22, 0.20), density=0.8)
        wins.append((cx, b - s * 0.15, s * 0.12))
        if ink:
            L.ink([(cx - s * 0.105, b), (cx - s * 0.105, b - s * 0.42)], width=max(1, s * 0.008), dark=0.6)
    cn_roof(L, x, b - s * 0.42, s * 2.3, s * 0.32, roof, ink)
    L.wash(S.poly([(x - s * 0.7, b - s * 0.6), (x - s * 0.7, b - s * 0.78), (x + s * 0.7, b - s * 0.78),
                   (x + s * 0.7, b - s * 0.6)], rough=1), wall, density=0.85, edge=0.5)
    cn_roof(L, x, b - s * 0.74, s * 1.7, s * 0.3, roof, ink)
    return wins


def great_wall(L, yg, h, color=(0.55, 0.55, 0.58), ink=True, x0=0, x1=None):
    """灰色官署巨牆（收割者）"""
    S, rng = L.S, L.rng
    x1 = x1 or L.w
    m = S.poly([(x0, yg), (x0, yg - h), (x1, yg - h), (x1, yg)], rough=2)
    L.wash(m, color, density=0.9, edge=0.6, gran=0.6)
    L.wash(m * S.vgrad(yg - h, yg), (0.45, 0.45, 0.52), density=0.6, edge=0, bloom=10)
    if ink:
        rows = int(h / 26)
        for r in range(rows):
            yy = yg - h + (r + 1) * h / (rows + 1)
            L.ink([(x0, yy), (x1, yy + rng.uniform(-2, 2))], width=1.1, dark=0.45, dry=0.5, tremor=0.5)
            off = (r % 2) * 40
            for xx in np.arange(x0 + off, x1, 80):
                L.ink([(xx, yy), (xx, yy - h / (rows + 1))], width=1.0, dark=0.35, dry=0.4)
        # 雉堞
        for xx in np.arange(x0, x1, 46):
            L.wash(S.poly([(xx, yg - h), (xx, yg - h - 18), (xx + 26, yg - h - 18), (xx + 26, yg - h)], rough=0.6),
                   color, density=0.9, edge=0.5)
        L.ink([(x0, yg - h), (x1, yg - h)], width=1.8, dark=0.8)


# ================================================================ figures
def figure(L, x, yg, h, robe=(0.55, 0.35, 0.30), pose=0.0, arm=0.0, ink=True, skin=(0.92, 0.78, 0.66),
           lean=0.0, legs=0.0):
    """簡筆人物：頭 + 長袍；pose 控制步態 -1..1；arm 手臂舉起 0..1"""
    S = L.S
    hr = h * 0.085
    hx, hy = x + lean * h * 0.15, yg - h + hr
    sx = hx
    sy = hy + hr * 1.6
    sp = legs * h * 0.12
    body = [(sx - h * 0.09, sy), (sx + h * 0.09, sy), (x + h * 0.15 + sp, yg - h * 0.12), (x + h * 0.06 + sp, yg),
            (x - h * 0.06 - sp, yg), (x - h * 0.15 - sp, yg - h * 0.12)]
    L.wash(S.poly(body, rough=h * 0.01, scale=12), robe, density=0.85, edge=0.7, gran=0.4)
    L.wash(S.ellipse(hx, hy, hr, hr * 1.1, rough=0.6), skin, density=0.7, edge=0.6)
    if ink:
        lw = max(0.9, h * 0.016)
        L.ink(body + [body[0]], width=lw, dark=0.7, tremor=0.4)
        a = np.linspace(0, 2 * np.pi, 14)
        L.ink([(hx + np.cos(t) * hr, hy + np.sin(t) * hr * 1.1) for t in a], width=lw * 0.9, dark=0.75, tremor=0.3)
        # 手臂
        ax0, ay0 = sx + h * 0.08, sy + h * 0.05
        ang = 0.4 * np.pi * (1 - arm) + pose * 0.4
        L.ink([(ax0, ay0), (ax0 + np.cos(ang) * h * 0.13, ay0 + np.sin(ang) * h * 0.13),
               (ax0 + np.cos(ang - 0.3) * h * 0.26, ay0 + np.sin(ang - 0.3) * h * 0.26)], width=lw, dark=0.7)
        ax0 = sx - h * 0.08
        ang = np.pi - (0.4 * np.pi * (1 - arm) + pose * 0.4)
        L.ink([(ax0, ay0), (ax0 + np.cos(ang) * h * 0.13, ay0 + np.sin(ang) * h * 0.13),
               (ax0 + np.cos(ang + 0.3) * h * 0.26, ay0 + np.sin(ang + 0.3) * h * 0.26)], width=lw, dark=0.7)


def horse_rider(L, x, yg, s, phase=0.0, col=(0.45, 0.33, 0.26), ink=True):
    """馬與騎手；phase 0..1 為步態"""
    S = L.S
    by0, by1 = yg - s * 0.92, yg - s * 0.48       # 軀幹上下緣
    body = [(x - s * 0.55, by0 + s * 0.06), (x - s * 0.2, by0), (x + s * 0.3, by0 + s * 0.02), (x + s * 0.45, by0 - s * 0.05),
            (x + s * 0.62, by0 - s * 0.3), (x + s * 0.8, by0 - s * 0.32), (x + s * 0.86, by0 - s * 0.2), (x + s * 0.68, by0 - s * 0.05),
            (x + s * 0.55, by0 + s * 0.2), (x + s * 0.48, by1), (x - s * 0.45, by1 + s * 0.02), (x - s * 0.62, by0 + s * 0.2)]
    m = S.poly(body, rough=s * 0.01, scale=12)
    L.wash(m, col, density=0.95, edge=0.8, gran=0.4)
    L.wash(m * S.vgrad(by0, by1 + 10), (0.30, 0.22, 0.20), density=0.5, edge=0.2)
    lw = max(1.5, s * 0.045)
    for lx, ph in [(-0.42, 0.0), (-0.3, 0.5), (0.3, 0.25), (0.42, 0.75)]:
        sw = np.sin((phase + ph) * 2 * np.pi) * s * 0.16
        top = (x + s * lx, by1 - s * 0.05)
        knee = (x + s * lx + sw * 0.6, yg - s * 0.24)
        hoof = (x + s * lx + sw, yg)
        L.ink([top, knee, hoof], width=lw, color=INK, dark=0.85, smooth=1, taper=(0.05, 0.02))
        L.wash(S.poly([(top[0] - lw, top[1]), (top[0] + lw, top[1]), (knee[0] + lw * 0.6, knee[1]), (knee[0] - lw * 0.6, knee[1])],
                      rough=0.5), col, density=0.9)
    L.ink([(x - s * 0.58, by0 + s * 0.1), (x - s * 0.78, by0 + s * 0.25), (x - s * 0.82, by0 + s * 0.45)],
          width=lw * 1.6, dark=0.75, dry=0.5)
    L.ink([(x + s * 0.5, by0 - s * 0.12), (x + s * 0.62, by0 - s * 0.36)], width=lw * 1.2, dark=0.7, dry=0.5)  # 鬃
    figure(L, x + s * 0.02, by0 + s * 0.12, s * 0.62, robe=(0.35, 0.33, 0.40), lean=0.6, arm=0.3, ink=ink, legs=0.6)
    if ink:
        L.ink(body + [body[0]], width=lw * 0.5, dark=0.65, smooth=1)


def boat(L, x, yg, s, sail=(0.93, 0.88, 0.78), hull=(0.45, 0.32, 0.25), ink=True):
    S = L.S
    hp = [(x - s, yg - s * 0.18), (x + s, yg - s * 0.22), (x + s * 0.7, yg + s * 0.05), (x - s * 0.75, yg + s * 0.05)]
    L.wash(S.poly(hp, rough=1), hull, density=0.9, edge=0.7)
    sp = [(x + s * 0.05, yg - s * 0.25), (x + s * 0.05, yg - s * 1.6), (x + s * 0.75, yg - s * 0.35)]
    L.wash(S.poly(sp, rough=1), sail, density=0.6, edge=0.7)
    sp2 = [(x - s * 0.05, yg - s * 0.3), (x - s * 0.05, yg - s * 1.3), (x - s * 0.7, yg - s * 0.35)]
    L.wash(S.poly(sp2, rough=1), sail, density=0.5, edge=0.6)
    if ink:
        lw = max(1, s * 0.03)
        L.ink(hp + [hp[0]], width=lw, dark=0.8)
        L.ink([(x, yg - s * 0.2), (x, yg - s * 1.7)], width=lw, dark=0.85)
        L.ink(sp, width=lw * 0.7, dark=0.6)
        L.ink(sp2, width=lw * 0.7, dark=0.6)


# ================================================================ more motifs
def blossom_tree(L, x, yg, h, petal=(0.96, 0.74, 0.80), deep=(0.86, 0.52, 0.62)):
    big_tree(L, x, yg, h, green=petal, shadow=deep, light=(0.99, 0.90, 0.90))
    rng = L.rng
    for _ in range(int(h * 0.6)):
        a = rng.uniform(0, 2 * np.pi)
        d = rng.uniform(0, h * 0.42)
        px, py = x + np.cos(a) * d * 1.1, yg - h * 0.62 + np.sin(a) * d * 0.7
        L.wash(L.S.ellipse(px, py, 3, 2.4, rough=0.3, feather=0.6), deep, density=0.8, edge=0.3)


def snowfield(L, base, amp, shadow=(0.80, 0.84, 0.92), cells=3, ink=1.2):
    """雪地：大面積留白，只上一層冷藍陰影"""
    S = L.S
    ys = S.ridge(base, amp, cells)
    m = S.below_curve(ys, rough=2)
    L.wash(m, (0.97, 0.97, 0.99), density=0.3, edge=0.2, gran=0.2)
    sh = m * (1 - S.vgrad(base - amp, base + 160)) * 0.9
    L.wash(S.roughen(sh, 10, 80), shadow, density=0.6, edge=0.5, gran=0.3, bloom=10)
    for _ in range(int(L.w / 160)):
        x = L.rng.uniform(0, L.w)
        y = L.rng.uniform(base + 40, L.h)
        L.wash(L.S.ellipse(x, y, L.rng.uniform(80, 300), L.rng.uniform(6, 18), rough=6), shadow,
               density=0.5, edge=0.6, gran=0.2)
    if ink:
        ridge_ink(L, ys, ink, gap=0.6, color=INK_BLUE)
    return ys


def hut(L, x, yg, w, snow=True, lit=False):
    wins = house(L, x, yg, w, w * 0.6, roof=(0.55, 0.45, 0.42), wall=(0.76, 0.70, 0.64), windows=1,
                 chimney=True, win_light=lit)
    if snow:
        top = yg - w * 0.6
        rh = w * 0.6 * 0.7
        L.lift(L.S.poly([(x - w * 0.58, top + 2), (x - w * 0.05, top - rh), (x + w * 0.05, top - rh), (x + w * 0.58, top + 2),
                         (x + w * 0.4, top - rh * 0.25), (x - w * 0.4, top - rh * 0.25)], rough=2), 0.92)
    return wins


def monastery(L, x, yg, s, lit=True):
    """山中小修院：主屋 + 鐘樓，回傳窗燈"""
    wins = house(L, x, yg, s * 1.5, s * 0.7, roof=(0.50, 0.42, 0.44), wall=(0.84, 0.80, 0.74), windows=3,
                 chimney=False, roof_h=s * 0.45, win_light=lit)
    w = tower(L, x + s * 0.95, yg, s * 0.42, s * 1.45, roof=(0.42, 0.40, 0.48))
    return wins + [w]


def candle(L, x, y, h=80):
    S = L.S
    L.wash(S.poly([(x - 9, y), (x - 9, y - h), (x + 9, y - h), (x + 9, y)], rough=0.6), (0.96, 0.92, 0.80), density=0.7, edge=0.7)
    L.ink([(x - 9, y), (x - 9, y - h), (x + 9, y - h + 3), (x + 9, y)], width=1.4, dark=0.7)
    L.wash(S.ellipse(x, y + 4, 34, 8, rough=1), (0.70, 0.60, 0.40), density=0.9, edge=0.6)
    L.ink([(x, y - h), (x, y - h - 10)], width=1.5, dark=0.9)
    return [x, y - h - 26]


def book(L, x, y, w, h, color=(0.55, 0.30, 0.28), open_=False, lines=0):
    S = L.S
    if open_:
        for side in (-1, 1):
            pts = [(x, y), (x + side * w * 0.5, y - h * 0.05), (x + side * w * 0.52, y - h), (x, y - h * 1.04)]
            L.wash(S.poly(pts, rough=0.8), (0.97, 0.93, 0.84), density=0.5, edge=0.8)
            L.ink(pts, width=1.6, dark=0.7, smooth=1)
            for k in range(lines):
                yy = y - h * 0.14 - k * h * 0.8 / lines
                xs = x + side * w * 0.07
                xe = x + side * w * L.rng.uniform(0.32, 0.46)
                # 直書：豎行小字
                L.ink([(xs + side * k * 0, yy), (xe, yy)], width=1.0, dark=0.5, dry=0.3, tremor=1.4)
        L.ink([(x, y), (x, y - h * 1.04)], width=1.6, dark=0.8)
    else:
        pts = [(x - w / 2, y), (x - w / 2, y - h), (x + w / 2, y - h), (x + w / 2, y)]
        L.wash(S.poly(pts, rough=0.6), color, density=0.9, edge=0.7)
        L.box(x - w / 2, y - h, x + w / 2, y, width=1.2, dark=0.7)
        L.ink([(x - w / 2 + 4, y - h * 0.5), (x + w / 2 - 4, y - h * 0.5)], width=1.0, dark=0.4, smooth=0)


def digger(L, x, yg, h, phase=0.0):
    """挖土的人：phase 0 鏟子入土 / 0.5 抬起 / 1 拋土"""
    lean = 0.5 - 0.6 * phase
    figure(L, x, yg, h, robe=(0.42, 0.40, 0.50), lean=lean, arm=0.2 + 0.6 * phase, legs=0.5)
    hx = x + lean * h * 0.15
    hy = yg - h * 0.55
    tip_x = x + h * (0.45 - 0.25 * phase)
    tip_y = yg - h * (0.02 + 0.45 * phase)
    L.ink([(hx - h * 0.1, hy - h * 0.1 * phase), (tip_x, tip_y)], width=max(1.5, h * 0.022), color=INK_BROWN, dark=0.9)
    L.wash(L.S.ellipse(tip_x, tip_y, h * 0.05, h * 0.035, ang=40 - 60 * phase, rough=0.4), (0.50, 0.52, 0.56), density=0.9)


def seedling(L, x, yg, h, tmap=None, t0=0.0):
    rng = L.rng
    pts = [(x, yg), (x + rng.uniform(-3, 3), yg - h * 0.5), (x + rng.uniform(-4, 4), yg - h)]
    L.ink(pts, width=max(1.2, h * 0.04), color=(0.30, 0.40, 0.20), dark=0.85)
    if tmap is not None:
        _paint_t(tmap, pts, h * 0.06 + 3, t0, t0 + 0.5)
    for k, side in enumerate([-1, 1, -1, 1]):
        yy = yg - h * (0.45 + 0.15 * k)
        cx = pts[2][0] * (0.45 + 0.15 * k) + x * (0.55 - 0.15 * k)
        lx = cx + side * h * 0.22
        m = L.S.ellipse((cx + lx) / 2, yy - h * 0.05, h * 0.13, h * 0.055, ang=-25 * side, rough=0.6)
        L.wash(m, (0.56, 0.74, 0.36), density=0.9, edge=0.8)
        if tmap is not None:
            np.minimum(tmap, np.where(m > 0.1, t0 + 0.5 + 0.1 * k, 9.0).astype(F32), out=tmap)


def steppe(L, base, color=(0.80, 0.80, 0.52), second=(0.66, 0.70, 0.44)):
    ys = ground(L, base, 25, color, cells=2, second=second, ink=1.0)
    field_strokes(L, ys, L.h, None, n=900, h=(12, 34), ink_col=(0.40, 0.42, 0.24))
    return ys
