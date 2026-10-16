"""第十四部《車站》— 格局、節點與決斷"""
import numpy as np
from kit import *

FILM = "film14"
ROBES = [(0.70, 0.34, 0.30), (0.30, 0.42, 0.62), (0.76, 0.62, 0.34), (0.40, 0.54, 0.40), (0.56, 0.38, 0.56), (0.80, 0.50, 0.36)]
RAIL = (0.24, 0.20, 0.20)


def rails(L, pts, gauge, sleepers=True, col=RAIL, w=2.4):
    """沿一條中心線畫一對鐵軌與枕木；gauge 可為常數或隨點變化的列表"""
    pts = np.asarray(pts, F32)
    g = np.broadcast_to(np.asarray(gauge, F32), (len(pts),))
    d = np.gradient(pts, axis=0)
    n = np.stack([-d[:, 1], d[:, 0]], 1)
    n /= np.linalg.norm(n, axis=1, keepdims=True) + 1e-6
    if sleepers:
        for i in range(0, len(pts), 2):
            a, b = pts[i] + n[i] * g[i] * 0.75, pts[i] - n[i] * g[i] * 0.75
            L.ink([a, b], width=max(1.2, g[i] * 0.12), color=(0.42, 0.32, 0.26), dark=0.7, smooth=0)
    for sgn in (1, -1):
        L.ink(pts + sgn * n * g[:, None] * 0.5, width=w, color=col, dark=0.85, smooth=1)


def persp_track(x0, y0, x1, y1, n=40, bend=0.0):
    """從近處 (x0,y0) 延伸到遠處 (x1,y1) 的透視路線"""
    t = np.linspace(0, 1, n)
    k = 1 - (1 - t) ** 1.6
    xs = x0 + (x1 - x0) * k + bend * np.sin(t * np.pi)
    ys = y0 + (y1 - y0) * k
    return np.stack([xs, ys], 1), t


def river(L, pts, w0, w1, col=(0.50, 0.66, 0.82), ink=True):
    S = L.S
    m = S.poly(ribbon(pts, w0, w1), rough=4, scale=40)
    L.lift(m, 0.95)
    L.wash(m, col, density=0.85, edge=0.8, gran=0.4)
    L.wash(m * S.vgrad(0, H), (0.86, 0.92, 0.96), density=0.25, edge=0)
    return m


def s1_valley():
    s = Scene(FILM, "s1_valley", seed=1401, w=int(W * 1.2))
    sky_layer(s, 'dusk', clouds_n=7)
    far_layer(s, 0.46, 150, (0.66, 0.64, 0.80))
    far_layer(s, 0.56, 110, (0.60, 0.66, 0.72), depth=0.3, name='hills', cells=4)
    L, ys = ground_layer(s, 0.62, 30, (0.72, 0.74, 0.50), (0.62, 0.64, 0.44))
    # 早已刻好的河床：從遠處蜿蜒而來
    pts = [(s.w * 0.52 + 320 * np.sin(k / 40 * 4.2) * (k / 40) ** 1.2, H * 0.62 + (k / 40) ** 1.4 * H * 0.42) for k in range(41)]
    river(L, pts, 10, 360)
    for k, x in enumerate(np.arange(120, s.w, 260)):
        if abs(x - s.w * 0.55) > 420:
            tree_round(L, x, gy(ys, x) + 60 + (k % 3) * 40, 110 + (k % 4) * 30, green=(0.52, 0.64, 0.38))
    fg_layer(s, col=(0.52, 0.60, 0.40), grass=300)
    return s


def s2_rails():
    s = Scene(FILM, "s2_rails", seed=1402)
    sky_layer(s, 'grey', clouds_n=5, y_h=0.55)
    far_layer(s, 0.52, 70, (0.74, 0.76, 0.82), ink=0.4)
    L, ys = ground_layer(s, 0.56, 8, (0.68, 0.72, 0.56), (0.62, 0.66, 0.52), ink=0.6)
    pts, t = persp_track(W * 0.36, H * 1.05, W * 0.62, H * 0.56, n=60, bend=-160)
    S = L.S
    L.wash(S.poly(ribbon(pts, 520, 8), rough=3), (0.64, 0.56, 0.48), density=0.7, edge=0.6, gran=0.7)
    rails(L, pts, 520 * (1 - t) ** 1.6 + 8)
    # 路堤上的野花
    rng = np.random.default_rng(14)
    for k in range(160):
        i = rng.integers(0, 50)
        side = rng.choice([-1, 1])
        x = pts[i, 0] + side * (300 * (1 - t[i]) ** 1.6 + 30 + rng.uniform(0, 400 * (1 - t[i])))
        y = pts[i, 1] + rng.uniform(-10, 10)
        r = 3 + 10 * (1 - t[i])
        L.wash(S.ellipse(x, y, r, r * 0.8, rough=0.5), [(0.92, 0.56, 0.50), (0.96, 0.86, 0.50), (0.80, 0.70, 0.90)][k % 3], density=0.8, edge=0.9)
    s.meta.update(track=pts.tolist())
    # 火車精靈：車頭 + 兩節車廂
    sp = s.sprite('train', 520, 260, anchor=(0.5, 0.92))
    S = sp.S
    sp.wash(S.poly([(30, 90), (200, 90), (200, 230), (30, 230)], rough=1), (0.34, 0.30, 0.34), density=0.95, edge=0.9)
    sp.wash(S.poly([(200, 130), (380, 130), (380, 230), (200, 230)], rough=1), (0.30, 0.28, 0.30), density=0.95, edge=0.9)
    sp.wash(S.poly([(250, 60), (300, 60), (300, 130), (250, 130)], rough=0.6), (0.24, 0.22, 0.24), density=1.0)
    sp.wash(S.poly([(380, 160), (470, 190), (470, 230), (380, 230)], rough=1), (0.60, 0.22, 0.20), density=0.95)
    for x in (70, 150, 230, 330):
        sp.wash(S.ellipse(x, 232, 26, 26, rough=0.3), (0.16, 0.14, 0.14), density=1.0)
    for x in (60, 130):
        sp.wash(S.poly([(x, 120), (x + 40, 120), (x + 40, 160), (x, 160)], rough=0.4), (0.98, 0.84, 0.52), density=0.9)
    sp.box(30, 90, 380, 230, width=2.2)
    return s


def s3_station():
    s = Scene(FILM, "s3_station", seed=1403, w=int(W * 1.15))
    sky_layer(s, 'dusk', clouds_n=6, glow=(W * 0.85, H * 0.5, 320, (0.99, 0.74, 0.48)))
    far_layer(s, 0.5, 120, (0.56, 0.52, 0.70))
    L, ys = ground_layer(s, 0.58, 6, (0.56, 0.54, 0.46), (0.50, 0.48, 0.42), ink=0.6)
    S = L.S
    # 站房與月台
    cx = s.w * 0.5
    L.wash(S.poly([(cx - 520, H * 0.62), (cx + 520, H * 0.62), (cx + 560, H * 0.68), (cx - 560, H * 0.68)], rough=1), (0.70, 0.66, 0.60), density=0.9, edge=0.8)
    wins = house(L, cx, H * 0.62, 520, 220, roof=(0.42, 0.34, 0.40), wall=(0.86, 0.78, 0.64), windows=4, chimney=True)
    # 站牌
    L.ink([(cx + 380, H * 0.62), (cx + 380, H * 0.44)], width=4, color=INK_BROWN, smooth=0)
    L.wash(S.poly([(cx + 300, H * 0.42), (cx + 460, H * 0.42), (cx + 460, H * 0.47), (cx + 300, H * 0.47)], rough=0.5), (0.94, 0.90, 0.80), density=0.9)
    L.box(cx + 300, H * 0.42, cx + 460, H * 0.47, width=1.8)
    lamps = [[float(w[0]), float(w[1]), 14.0] for w in (wins or [])]
    for x in np.arange(cx - 460, cx + 480, 180):   # 月台燈柱
        L.ink([(x, H * 0.66), (x, H * 0.5)], width=3, color=INK, smooth=0)
        lamps.append([float(x), H * 0.5, 16.0])
    # 由近處同一點分岔出去的鐵軌：扇形
    hub = (cx, H * 1.04)
    ends = [(-200, H * 0.7), (s.w * 0.18, H * 0.66), (s.w * 0.82, H * 0.66), (s.w + 200, H * 0.7), (cx - 120, H * 0.69)]
    for k, (ex, ey) in enumerate(ends):
        t = np.linspace(0, 1, 40)
        xs = hub[0] + (ex - hub[0]) * t ** 1.3
        ysr = hub[1] + (ey - hub[1]) * (1 - (1 - t) ** 2)
        rails(L, np.stack([xs, ysr], 1), 120 * (1 - t) + 16, w=2.0)
    figure(L, cx - 60, H * 0.665, 150, robe=(0.36, 0.40, 0.56), arm=0.1)   # 等車的旅人
    L.ink([(cx - 10, H * 0.665), (cx - 10, H * 0.62)], width=2, color=INK_BROWN, smooth=0)
    s.meta.update(lamps=lamps)
    return s


def s4_split():
    s = Scene(FILM, "s4_split", seed=1404)
    L = s.layer('land', 0.0, opaque=True)
    S = L.S
    L.wash(np.ones((H, W), F32), (0.86, 0.82, 0.66), density=0.7, edge=0, gran=0.5)
    L.wash(S.poly([(0, H * 0.55), (W * 0.46, H * 0.62), (W * 0.3, H), (0, H)], rough=10), (0.60, 0.70, 0.46), density=0.7, edge=0.6)   # 左：綠洲
    L.wash(S.poly([(W, H * 0.55), (W * 0.54, H * 0.62), (W * 0.7, H), (W, H)], rough=10), (0.86, 0.70, 0.48), density=0.7, edge=0.6)  # 右：沙原
    for k in range(9):
        tree_round(L, 120 + k * 90, H * 0.78 + (k % 3) * 60, 70 + (k % 4) * 20, green=(0.44, 0.60, 0.36))
    for k in range(5):
        L.wash(S.ellipse(W * 0.72 + k * 120, H * 0.82 + (k % 2) * 60, 90, 18, rough=4), (0.78, 0.60, 0.42), density=0.5)
    # 水流：上方一條，於石子處分成兩支
    L = s.layer('water', 0.0)
    S = L.S
    px, py = W * 0.5, H * 0.42
    top = [(W * 0.5 + 40 * np.sin(k), -20 + k * (py + 20) / 6) for k in range(7)]
    lft = [(px - k * 120 - 8 * k * k, py + k * 72 + 4 * k * k) for k in range(1, 10)]
    rgt = [(px + k * 120 + 8 * k * k, py + k * 72 + 4 * k * k) for k in range(1, 10)]
    m = S.poly(ribbon(top, 60, 80), rough=3)
    for br in (lft, rgt):
        m = np.maximum(m, S.poly(ribbon([(px, py)] + br, 60, 280), rough=4))
    L.wash(m, (0.46, 0.64, 0.82), density=0.9, edge=0.8, gran=0.4)
    t = s.tmap('water')
    yy, xx = np.mgrid[0:H, 0:W].astype(F32)
    t[:] = np.clip(yy / H, 0, 1)
    L = s.layer('pebble', 0.0)
    L.wash(L.S.ellipse(px, py + 14, 34, 22, rough=1), (0.44, 0.42, 0.44), density=0.95, edge=0.9)
    L.ink([(px - 34, py + 14), (px, py - 6), (px + 34, py + 14)], width=1.6)
    s.meta.update(pebble=[px, py])
    return s


def s5_sluice():
    s = Scene(FILM, "s5_sluice", seed=1405, w=int(W * 1.1))
    sky_layer(s, 'day', clouds_n=7)
    far_layer(s, 0.48, 130, (0.70, 0.74, 0.86))
    L = s.layer('dam', 0.4)
    S = L.S
    L.wash(S.below_curve(np.full(s.w, H * 0.5, F32), 3), (0.62, 0.70, 0.50), density=0.8, edge=0.6)
    L.wash(S.poly([(0, H * 0.5), (s.w * 0.3, H * 0.5), (s.w * 0.3, H * 0.62), (0, H * 0.62)], rough=3), (0.42, 0.58, 0.76), density=0.9, edge=0.6)   # 水庫
    gx = s.w * 0.32
    L.wash(S.poly([(gx - 40, H * 0.34), (gx + 60, H * 0.34), (gx + 60, H * 0.7), (gx - 40, H * 0.7)], rough=1), (0.70, 0.66, 0.62), density=0.95, edge=0.9, gran=0.8)
    L.ink([(gx - 40, H * 0.34), (gx + 60, H * 0.34)], width=3, smooth=0)
    for k in range(5):
        L.ink([(gx - 40, H * 0.4 + k * 55), (gx + 60, H * 0.4 + k * 55)], width=1.2, dark=0.5, smooth=0)
    L.ink([(gx + 10, H * 0.34), (gx + 10, H * 0.2)], width=5, color=INK_BROWN, smooth=0)   # 閘門絞盤
    L.wash(S.ellipse(gx + 10, H * 0.2, 36, 36, rough=0.4), (0.50, 0.36, 0.28), density=0.9)
    # 新沖出的水道
    L = s.layer('channel', 0.4)
    S = L.S
    pts = [(gx + 60 + k * 140, H * 0.6 + 120 * np.sin(k * 0.6) + k * 26) for k in range(14)]
    L.wash(S.poly(ribbon(pts, 70, 260), rough=6), (0.44, 0.62, 0.80), density=0.9, edge=0.8, gran=0.4)
    L.ink([p for p in pts], width=1.4, dark=0.4, color=(0.30, 0.40, 0.56))
    t = s.tmap('channel')
    xx = np.arange(s.w, dtype=F32)[None, :]
    t[:] = np.clip((xx - gx) / (s.w - gx), 0, 1) * np.ones((H, 1), F32)
    s.meta.update(gate=[gx + 60, H * 0.6], flow=[[float(x), float(y)] for x, y in pts])
    fg_layer(s, col=(0.52, 0.62, 0.38), grass=250)
    return s


def s6_wager():
    s = Scene(FILM, "s6_wager", seed=1406)
    sky_layer(s, 'grey', clouds_n=4, y_h=0.5)
    L, ys = ground_layer(s, 0.58, 10, (0.66, 0.68, 0.60), (0.58, 0.60, 0.54), ink=0.5)
    S = L.S
    # 十字路口，四條路沒入霧中
    for ex, ey in [(W * 0.08, H * 0.6), (W * 0.92, H * 0.6), (W * 0.5, H * 0.585)]:
        pts = [(W * 0.5 + (ex - W * 0.5) * k / 10, H * 0.82 + (ey - H * 0.82) * (1 - (1 - k / 10) ** 2)) for k in range(11)]
        L.wash(S.poly(ribbon(pts, 220, 20), rough=4), (0.76, 0.70, 0.60), density=0.75, edge=0.6, gran=0.6)
    L.wash(S.poly(ribbon([(W * 0.5, H * 1.05), (W * 0.5, H * 0.82)], 600, 260), rough=4), (0.76, 0.70, 0.60), density=0.75, edge=0.6)
    L.ink([(W * 0.58, H * 0.8), (W * 0.58, H * 0.5)], width=6, color=INK_BROWN, smooth=0)   # 路標
    for k, (dx, dy) in enumerate([(-160, 0), (150, 40), (-120, 80)]):
        L.wash(S.poly([(W * 0.58, H * 0.52 + dy), (W * 0.58 + dx, H * 0.52 + dy - 10), (W * 0.58 + dx, H * 0.52 + dy + 30), (W * 0.58, H * 0.52 + dy + 30)], rough=0.5), (0.90, 0.84, 0.70), density=0.85)
    L = s.layer('fig', 0.45)
    figure(L, W * 0.47, H * 0.86, 360, robe=(0.34, 0.36, 0.48), arm=0.9, lean=0.2)
    s.meta.update(lantern=[W * 0.47 + 120, H * 0.86 - 340], fog=[[W * 0.1, H * 0.55], [W * 0.5, H * 0.55], [W * 0.9, H * 0.55]])
    return s


def s7_birth():
    s = Scene(FILM, "s7_birth", seed=1407)
    L = s.layer('room', 0.0, opaque=True)
    S = L.S
    L.wash(np.ones((H, W), F32), (0.30, 0.26, 0.32), density=0.85, edge=0, gran=0.4)
    L.wash(S.radial(W * 0.46, H * 0.6, 700), (0.96, 0.80, 0.54), density=0.6, edge=0, bloom=40)
    L = s.layer('table', 0.4)
    S = L.S
    L.wash(S.poly([(W * 0.18, H * 0.74), (W * 0.82, H * 0.74), (W * 0.86, H * 0.8), (W * 0.14, H * 0.8)], rough=1), (0.52, 0.38, 0.28), density=0.95, edge=0.8)
    cx, cy = W * 0.36, H * 0.74
    candle(L, cx, cy, 200)
    # 搖籃
    bx, by = W * 0.6, H * 0.74
    L.wash(S.ellipse(bx, by - 70, 220, 90, rough=1) * (S.vgrad(by - 110, by - 70)), (0.78, 0.62, 0.42), density=0.95, edge=0.9, gran=0.6)
    a = np.linspace(0, np.pi, 30)
    L.ink([(bx + np.cos(t) * 220, by - 70 + np.sin(t) * 90) for t in a], width=2.4)
    L.ink([(bx - 200, by - 20), (bx - 240, by)], width=3, smooth=0); L.ink([(bx + 200, by - 20), (bx + 240, by)], width=3, smooth=0)
    L.wash(S.ellipse(bx - 60, by - 100, 110, 40, rough=1), (0.96, 0.92, 0.86), density=0.7)
    L.wash(S.ellipse(bx + 80, by - 104, 36, 32, rough=0.5), (0.95, 0.80, 0.70), density=0.85)
    s.meta.update(flame=[cx, cy - 214], cradle=[bx, by - 100])
    return s


def s8_furrow():
    s = Scene(FILM, "s8_furrow", seed=1408, w=int(W * 1.15))
    sky_layer(s, 'gold', clouds_n=7, glow=(W * 0.2, H * 0.55, 300, (0.99, 0.78, 0.50)))
    far_layer(s, 0.52, 90, (0.66, 0.60, 0.70))
    L, ys = ground_layer(s, 0.62, 70, (0.72, 0.70, 0.46), (0.64, 0.60, 0.42), cells=5)
    S = L.S
    river(L, [(s.w * 0.08 + k * 30, H * 0.62 + k * 60) for k in range(8)], 30, 200, col=(0.50, 0.62, 0.74))   # 台伯河
    L = s.layer('furrow', 0.45)
    S = L.S
    cx, cy, rx, ry = s.w * 0.56, H * 0.74, 640, 150
    a = np.linspace(0, 2 * np.pi, 120)
    ring = [(cx + np.cos(t) * rx, cy + np.sin(t) * ry) for t in a]
    m = S.poly(ribbon(ring, 26, 26), rough=2)
    L.wash(m, (0.38, 0.26, 0.20), density=0.9, edge=0.8, gran=0.7)
    L.ink(ring, width=1.6, dark=0.5)
    t = s.tmap('furrow')
    yy, xx = np.mgrid[0:H, 0:s.w].astype(F32)
    ang = (np.arctan2((yy - cy) / ry, (xx - cx) / rx) + np.pi / 2) % (2 * np.pi)
    t[:] = ang / (2 * np.pi)
    # 母狼與雙子：小丘上的剪影（象徵）
    L = s.layer('wolf', 0.45)
    hx, hy = s.w * 0.2, gy(ys, s.w * 0.2) + 20
    wolf(L, hx, hy, 220, col=(0.30, 0.24, 0.24))
    L.wash(L.S.ellipse(hx - 60, hy - 30, 26, 18, rough=0.4), (0.86, 0.70, 0.58), density=0.85)
    L.wash(L.S.ellipse(hx - 10, hy - 26, 26, 18, rough=0.4), (0.86, 0.70, 0.58), density=0.85)
    s.meta.update(furrow=[cx, cy, rx, ry])
    sp = s.sprite('ox', 260, 200, anchor=(0.5, 0.95))
    S2 = sp.S
    sp.wash(S2.ellipse(120, 110, 90, 50, rough=1), (0.62, 0.50, 0.40), density=0.95, edge=0.9)
    sp.wash(S2.ellipse(210, 90, 34, 28, rough=0.6), (0.58, 0.46, 0.36), density=0.95)
    for x in (60, 90, 150, 180):
        sp.ink([(x, 140), (x, 190)], width=6, color=INK_BROWN, smooth=0)
    sp.ink([(200, 66), (190, 46)], width=3); sp.ink([(222, 66), (236, 48)], width=3)
    sp.ink([(30, 110), (4, 170)], width=4, color=INK_BROWN, smooth=0)
    return s


def s9_grass():
    s = Scene(FILM, "s9_grass", seed=1409, w=int(W * 1.2))
    sky_layer(s, 'day', clouds_n=8)
    far_layer(s, 0.54, 120, (0.72, 0.76, 0.86))
    L, ys = ground_layer(s, 0.64, 30, (0.46, 0.40, 0.36), (0.40, 0.36, 0.34), ink=0.8)   # 燒過的草地
    L = s.layer('regrow', 0.45)
    S = L.S
    L.wash(S.below_curve(ys - 4, 3), (0.56, 0.70, 0.40), density=0.85, edge=0.6, gran=0.5)
    weeds(L, ys, H, 900, col=(0.36, 0.56, 0.28), h=(30, 80))
    for k, x in enumerate(np.arange(300, s.w, 520)):
        house(L, x, gy(ys, x) + 40, 200, 130, roof=(0.62, 0.40, 0.32), windows=2)
    big_tree(L, s.w * 0.72, gy(ys, s.w * 0.72) + 60, 620, seed_rng=np.random.default_rng(9))
    t = s.tmap('regrow')
    xx = np.arange(s.w, dtype=F32)[None, :]
    yy = np.arange(H, dtype=F32)[:, None]
    t[:] = np.clip(0.6 * (s.w - xx) / s.w + 0.4 * (yy < H * 0.6) + 0.1 * np.sin(xx / 90), 0, 1)
    s.meta.update(road_y=gy(ys, 600) + 110)
    for p in range(4):
        sp = s.sprite(f'scholar_{p}', 240, 320, anchor=(0.5, 0.96))
        ph = np.sin(p / 4 * 2 * np.pi)
        figure(sp, 120, 308, 260, robe=(0.84, 0.82, 0.76), lean=0.25, legs=ph * 0.7, pose=ph, arm=0.2)
        sp.wash(sp.S.poly([(150, 150), (210, 140), (214, 200), (154, 206)], rough=0.6), (0.60, 0.46, 0.32), density=0.95)   # 書囊
    fg_layer(s, col=(0.50, 0.64, 0.36), grass=350)
    return s


def s10_assembly():
    s = Scene(FILM, "s10_assembly", seed=1410)
    sky_layer(s, 'day', clouds_n=6)
    far_layer(s, 0.54, 100, (0.72, 0.78, 0.86))
    L, ys = ground_layer(s, 0.68, 20, (0.66, 0.76, 0.48), (0.58, 0.68, 0.42))
    big_tree(L, W * 0.5, H * 0.74, 900, seed_rng=np.random.default_rng(10))
    L = s.layer('circle', 0.45)
    S = L.S
    cx, cy = W * 0.5, H * 0.86
    L.wash(S.ellipse(cx, cy - 10, 160, 40, rough=1), (0.58, 0.44, 0.32), density=0.9)   # 木桌
    charter(L, cx - 70, cy - 70, 140, 60, seal=True, lines=4)
    rng = np.random.default_rng(3)
    for k in range(9):
        a = np.pi * (0.05 + 0.9 * k / 8)
        x, y = cx + np.cos(a) * 420, cy - np.sin(a) * 90 + 40
        figure(L, x, y, 200 - np.sin(a) * 40, robe=ROBES[k % len(ROBES)], arm=0.1 + 0.2 * (k % 2))
    s.meta.update(table=[cx, cy - 40])
    fg_layer(s, col=(0.54, 0.66, 0.40), grass=300)
    return s


def s11_light():
    s = Scene(FILM, "s11_light", seed=1411)
    sky_layer(s, 'storm', clouds_n=10, y_h=0.5)
    L, ys = ground_layer(s, 0.6, 10, (0.62, 0.62, 0.58), (0.54, 0.54, 0.52), ink=0.6)
    S = L.S
    # 無數淡淡的小徑匯成一條路
    rng = np.random.default_rng(11)
    for k in range(40):
        x0 = rng.uniform(-100, W + 100)
        pts = [(x0 + (W * 0.5 - x0) * (j / 10) ** 0.7 + rng.normal(0, 8), H * 0.6 + (H * 0.42) * (j / 10)) for j in range(11)]
        L.ink(pts, width=1.2 + 0.08 * k, color=(0.62, 0.52, 0.42), dark=0.35, dry=0.4)
    L = s.layer('crowd', 0.45)
    pts = []
    for row in range(3):
        for k in range(14):
            pts.append((140 + k * 150 + row * 60 + rng.normal(0, 10), H * 0.72 + row * 70))
    for i, (x, y) in enumerate(pts):
        if i == 17:
            continue
        figure(L, x, y, 170 + (y - H * 0.72) * 0.5, robe=(0.46, 0.46, 0.50), arm=0.0, lean=-0.1)
    L = s.layer('one', 0.45)
    x, y = pts[17]
    figure(L, x, y, 210, robe=(0.82, 0.40, 0.30), arm=0.6, lean=0.3)
    s.meta.update(one=[x, y - 200])
    return s


def s12_oak():
    s = Scene(FILM, "s12_oak", seed=1412, w=int(W * 1.2))
    sky_layer(s, 'gold', clouds_n=8, glow=(W * 1.0, H * 0.56, 320, (0.99, 0.80, 0.52)))
    far_layer(s, 0.56, 120, (0.66, 0.62, 0.74))
    L, ys = ground_layer(s, 0.68, 40, (0.68, 0.72, 0.46), (0.58, 0.62, 0.42))
    # 蜿蜒而從不回頭的河
    pts = [(-40 + k * 140, H * 0.74 + 50 * np.sin(k * 0.8)) for k in range(int(s.w / 140) + 2)]
    river(L, pts, 50, 70, col=(0.52, 0.66, 0.82))
    big_tree(L, s.w * 0.3, gy(ys, s.w * 0.3) + 40, 980, seed_rng=np.random.default_rng(31))   # 英格蘭的老橡樹
    L = s.layer('sapling', 0.45)
    sx = s.w * 0.72
    yg = gy(ys, sx) + 120
    seedling(L, sx, yg, 120)
    L.wash(L.S.ellipse(sx, yg + 6, 60, 12, rough=1), (0.40, 0.30, 0.24), density=0.9)
    figure(L, sx + 110, yg + 10, 230, robe=(0.42, 0.38, 0.46), lean=0.6, arm=0.3)   # 種樹的老人
    L.ink([(sx + 70, yg - 150), (sx + 30, yg + 6)], width=4, color=INK_BROWN, smooth=0)
    fg_layer(s, col=(0.52, 0.60, 0.38), grass=300)
    return s


ALL = [s1_valley, s2_rails, s3_station, s4_split, s5_sluice, s6_wager, s7_birth, s8_furrow, s9_grass, s10_assembly, s11_light, s12_oak]
