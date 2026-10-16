"""第七部《小路》— 習慣法、封建契約、沒有主權者的國家"""
import numpy as np
from kit import *

FILM = "film7"
ROBES = [(0.70, 0.34, 0.30), (0.30, 0.42, 0.62), (0.76, 0.62, 0.34), (0.40, 0.54, 0.40), (0.56, 0.38, 0.56), (0.80, 0.50, 0.36)]


def forest(L, n, y0, y1, rng, h=(300, 520), col=(0.40, 0.56, 0.40)):
    for _ in range(n):
        x = rng.uniform(-50, L.w + 50)
        y = rng.uniform(y0, y1)
        k = (y - y0) / max(1, y1 - y0)
        if rng.random() < 0.5:
            tree_pine(L, x, y, rng.uniform(*h) * (0.6 + 0.6 * k), color=col)
        else:
            tree_round(L, x, y, rng.uniform(*h) * (0.5 + 0.5 * k), green=(0.50, 0.66, 0.40))


def s1_path():
    s = Scene(FILM, "s1_path", seed=701)
    sky_layer(s, 'dawn', clouds_n=5)
    far_layer(s, 0.56, 100, (0.70, 0.74, 0.84))
    L = s.layer('woods', 0.3)
    ys = ground(L, H * 0.58, 20, (0.56, 0.70, 0.44), cells=3, ink=0.8)
    water(L, H * 0.6, H * 0.64, (0.56, 0.72, 0.86))
    forest(L, 34, H * 0.58, H * 0.66, np.random.default_rng(2), h=(160, 260))
    L = s.layer('path', 0.6)
    S = L.S
    L.wash(S.below_curve(np.full(W, H * 0.66, F32), 2), (0.52, 0.66, 0.40), density=0.85, edge=0.6, gran=0.5)
    pts = [(W * 0.5 + 300 * np.sin(k * 0.5) * (k / 14), H * 0.66 + k * (H * 0.36 / 14)) for k in range(15)]
    m = S.poly(ribbon(pts, 18, 220), rough=6, scale=30)
    L.wash(m, (0.76, 0.66, 0.48), density=0.8, edge=0.8, gran=0.7)
    t = s.tmap('path')
    yy = np.arange(H, dtype=F32)[:, None]
    t[:] = np.clip(1 - (yy - H * 0.64) / (H * 0.38), 0, 1) * np.ones((1, W), F32) * 0.95
    L = s.layer('fg', 0.95)
    for x in (60, 260, W - 240, W - 60):
        tree_pine(L, x, H * 1.02, 900, color=(0.28, 0.40, 0.34))
    return s


def s2_elder():
    s = Scene(FILM, "s2_elder", seed=702)
    sky_layer(s, 'day', clouds_n=7)
    L, ys = ground_layer(s, 0.84, 20, (0.66, 0.76, 0.48), (0.56, 0.64, 0.42))
    big_tree(L, W * 0.62, gy(ys, W * 0.62) + 10, 980, seed_rng=np.random.default_rng(18))
    figure(L, W * 0.55, gy(ys, W * 0.55) + 40, 330, robe=(0.66, 0.62, 0.58), arm=0.4, lean=0.15)        # 長老
    L.ink([(W * 0.55 - 40, gy(ys, W * 0.55) - 200), (W * 0.55 - 30, gy(ys, W * 0.55) - 160)], width=8, color=(0.95, 0.95, 0.92))  # 白鬍子
    figure(L, W * 0.38, gy(ys, W * 0.38) + 50, 300, robe=(0.30, 0.30, 0.40), arm=0.6, lean=-0.1)       # 書記
    charter(L, W * 0.32, gy(ys, W * 0.38) - 110, 160, 120, seal=False, lines=4)
    L.ink([(W * 0.35, gy(ys, W * 0.38) - 170), (W * 0.39, gy(ys, W * 0.38) - 240)], width=2, smooth=0)  # 鵝毛筆
    s.meta.update(elder=[W * 0.55, gy(ys, W * 0.55) - 200], clerk=[W * 0.32, gy(ys, W * 0.38) - 110])
    return s


def s3_king():
    s = Scene(FILM, "s3_king", seed=703)
    sky_layer(s, 'day', clouds_n=8)
    far_layer(s, 0.6, 150, (0.70, 0.76, 0.86))
    L, ys = ground_layer(s, 0.8, 20, (0.72, 0.80, 0.52), (0.62, 0.70, 0.46))
    cx = W * 0.5
    pts = []
    for k in range(9):
        a = np.pi * (0.05 + 0.9 * k / 8)
        pts.append((cx + np.cos(a) * 620, gy(ys, cx) + 60 + np.sin(a) * 90))
    rng = np.random.default_rng(3)
    for i, (x, y) in enumerate(sorted(pts, key=lambda p: p[1])):
        figure(L, x, y, 280, robe=ROBES[i % 6], arm=0.2)
    figure(L, cx, gy(ys, cx) + 120, 280, robe=(0.60, 0.20, 0.24), arm=0.3)   # 國王：一樣高
    cr = [(cx - 26, gy(ys, cx) + 120 - 280), (cx - 30, gy(ys, cx) + 120 - 315), (cx - 10, gy(ys, cx) + 120 - 298), (cx, gy(ys, cx) + 120 - 322),
          (cx + 10, gy(ys, cx) + 120 - 298), (cx + 30, gy(ys, cx) + 120 - 315), (cx + 26, gy(ys, cx) + 120 - 280)]
    L.wash(L.S.poly(cr, rough=0.3), (0.95, 0.76, 0.30), density=1.0, edge=0.9)
    L.ink(cr + [cr[0]], width=1.6, smooth=0)
    s.meta.update(king=[cx, gy(ys, cx) - 170])
    fg_layer(s)
    return s


def s4_market():
    s = Scene(FILM, "s4_market", seed=704, w=int(W * 1.2))
    sky_layer(s, 'day', clouds_n=8)
    L, ys = ground_layer(s, 0.62, 10, (0.80, 0.74, 0.58), (0.72, 0.64, 0.50))
    scrolls = []
    for i, x in enumerate(np.arange(260, s.w, 470)):
        yg = gy(ys, x) + 240
        aw = [(x - 200, yg - 330), (x + 200, yg - 330), (x + 230, yg - 250), (x - 230, yg - 250)]
        L.wash(L.S.poly(aw, rough=1), ROBES[i % 6], density=0.85, edge=0.9)
        for k in range(6):
            L.ink([(x - 230 + k * 92, yg - 250), (x - 210 + k * 80, yg - 230)], width=1.2, smooth=0)
        L.ink([(x - 190, yg - 250), (x - 190, yg)], width=4, color=INK_BROWN, smooth=0)
        L.ink([(x + 190, yg - 250), (x + 190, yg)], width=4, color=INK_BROWN, smooth=0)
        L.wash(L.S.poly([(x - 200, yg - 80), (x + 200, yg - 80), (x + 200, yg - 50), (x - 200, yg - 50)], rough=0.6), (0.56, 0.40, 0.30), density=0.9)
        for k in range(4):
            sx = x - 140 + k * 92
            L.wash(L.S.ellipse(sx, yg - 100, 30, 18, rough=0.4), (0.95, 0.90, 0.76), density=0.6, edge=0.9)
            L.ink([(sx - 30, yg - 100), (sx + 30, yg - 100)], width=1.0, smooth=0)
            scrolls.append([sx, yg - 100])
        figure(L, x + 60, yg + 140, 230, robe=ROBES[(i + 3) % 6], arm=0.5)
    s.meta.update(scrolls=scrolls)
    fg_layer(s, 0.97, col=(0.70, 0.64, 0.50), grass=150)
    return s


def s5_homage():
    s = Scene(FILM, "s5_homage", seed=705)
    L = s.layer('hall', 0.0, opaque=True)
    S = L.S
    L.wash(np.ones((H, W), F32), (0.78, 0.70, 0.60), density=0.75, edge=0, gran=0.5)
    for x in np.arange(0, W, 140):   # 石牆
        for y in np.arange(0, H, 70):
            L.ink([(x + (y / 70 % 2) * 70, y), (x + (y / 70 % 2) * 70 + 130, y)], width=1.0, dark=0.25, dry=0.6, smooth=0)
    L = s.layer('figs', 0.4)
    S = L.S
    yg = H * 0.86
    L.wash(S.below_curve(np.full(W, yg, F32), 1), (0.50, 0.40, 0.34), density=0.85, edge=0.6)
    figure(L, W * 0.4, yg, 600, robe=(0.56, 0.20, 0.22), arm=0.5)               # 領主
    figure(L, W * 0.54, yg + 10, 340, robe=(0.36, 0.44, 0.58), lean=-0.8, arm=0.9, legs=0.6)  # 跪下的封臣
    charter(L, W * 0.74, H * 0.52, 360, 280, seal=True)
    L.wash(L.S.blob(W * 0.74 - 90, H * 0.52 + 92, 25, n=6, spread=0.3, rough=2), (0.72, 0.18, 0.14), density=1.0, edge=0.9)
    for k in range(40):   # 四十天的記號
        x = W * 0.08 + (k % 10) * 34
        y = H * 0.24 + (k // 10) * 60
        L.ink([(x, y), (x + 4, y + 40)], width=3, dark=0.8, smooth=0)
    L.ink([(W * 0.06, H * 0.2), (W * 0.06, H * 0.5)], width=5, color=INK_BROWN, smooth=0)
    L.wash(L.S.poly([(W * 0.06 - 14, H * 0.2), (W * 0.06, H * 0.14), (W * 0.06 + 14, H * 0.2)], rough=0.3), (0.56, 0.58, 0.64), density=0.95)
    return s


def s6_network():
    s = Scene(FILM, "s6_network", seed=706, w=int(W * 1.25))
    sky_layer(s, 'day', clouds_n=10)
    far_layer(s, 0.5, 160, (0.70, 0.76, 0.88), snow=True)
    L, ys = ground_layer(s, 0.62, 80, (0.72, 0.82, 0.52), (0.62, 0.72, 0.46), cells=5)
    nodes = []
    rng = np.random.default_rng(6)
    for i, x in enumerate(np.arange(220, s.w, 330)):
        y = gy(ys, x) + rng.uniform(40, 300)
        kind = i % 3
        if kind == 0:
            castle(L, x, y, 70)
        elif kind == 1:
            church(L, x, y, 70)
        else:
            for k in range(3):
                house(L, x - 60 + k * 60, y, 60, 46)
        nodes.append([float(x), float(y - 60)])
    s.meta.update(nodes=nodes)
    fg_layer(s)
    return s


def s7_manor():
    s = Scene(FILM, "s7_manor", seed=707, w=int(W * 1.2))
    sky_layer(s, 'night', clouds_n=0, density=0.95)
    L, ys = ground_layer(s, 0.7, 30, (0.30, 0.32, 0.38), (0.24, 0.26, 0.32), ink=1.0)
    cx = s.w * 0.4
    wins = house(L, cx, gy(ys, cx) + 20, 420, 240, roof=(0.36, 0.30, 0.34), wall=(0.50, 0.46, 0.50), windows=4, win_light=True)
    pts = []
    rng = np.random.default_rng(7)
    for k in range(22):
        a = rng.uniform(0, 2 * np.pi); d = rng.uniform(320, 700)
        pts.append((cx + np.cos(a) * d, gy(ys, cx) + 140 + np.sin(a) * 120))
    for i, (x, y) in enumerate(sorted(pts, key=lambda p: p[1])):
        figure(L, x, y, 130, robe=(0.30, 0.30, 0.36), skin=(0.34, 0.32, 0.36), arm=0.2)
    L.ink([(s.w * 0.62, gy(ys, s.w * 0.62) + 60), (s.w, gy(ys, s.w) + 120)], width=26, color=(0.40, 0.38, 0.40), dark=0.6)
    s.meta.update(lamps=[list(v) for v in wins], road=[[s.w * 0.98, gy(ys, s.w * 0.98) + 110], [s.w * 0.66, gy(ys, s.w * 0.66) + 70]])
    sp = s.sprite('official', 200, 300, anchor=(0.5, 0.97)); figure(sp, 100, 290, 250, robe=(0.52, 0.52, 0.56), arm=0.1)
    return s


def s8_writ():
    s = Scene(FILM, "s8_writ", seed=708, w=int(W * 1.3))
    sky_layer(s, 'dawn', clouds_n=8, glow=(W * 0.2, H * 0.6, 260, (0.99, 0.82, 0.58)))
    far_layer(s, 0.6, 120, (0.70, 0.70, 0.84))
    L, ys = ground_layer(s, 0.72, 40, (0.72, 0.78, 0.50), (0.60, 0.66, 0.44))
    castle(L, 300, gy(ys, 300) + 10, 90)
    for x in [s.w - 700, s.w - 520, s.w - 360]:
        house(L, x, gy(ys, x) + 20, 140, 100)
    villagers(L, [(s.w - 600, gy(ys, s.w - 600) + 130), (s.w - 450, gy(ys, s.w - 450) + 140)], 200, np.random.default_rng(1))
    s.meta.update(ride_y=gy(ys, s.w * 0.5) + 160, end=s.w - 800)
    for p in range(4):
        sp = s.sprite(f"rider_{p}", 600, 560, anchor=(0.5, 0.96))
        horse_rider(sp, 290, 535, 290, phase=p / 4)
    fg_layer(s)
    return s


def s9_jury():
    s = Scene(FILM, "s9_jury", seed=709)
    sky_layer(s, 'day', clouds_n=7)
    L, ys = ground_layer(s, 0.62, 10, (0.72, 0.78, 0.52), (0.62, 0.66, 0.46))
    L = s.layer('jury', 0.45)
    S = L.S
    yb = H * 0.82
    L.wash(S.poly([(W * 0.2, yb - 60), (W * 0.8, yb - 60), (W * 0.8, yb - 30), (W * 0.2, yb - 30)], rough=0.8), (0.56, 0.40, 0.30), density=0.95)
    for k in range(12):
        x = W * 0.24 + k * (W * 0.52 / 11)
        figure(L, x, yb - 40 + (k % 2) * 6, 230, robe=ROBES[k % 6], arm=0.0)
    L = s.layer('duel', 0.45)
    S = L.S
    pts = []
    rng = np.random.default_rng(2)
    for k in range(14):
        a = np.pi * (1.05 + 0.9 * k / 13)
        pts.append((W * 0.5 + np.cos(a) * 700, H * 0.88 + np.sin(a) * 150))
    villagers(L, pts, 210, rng)
    for side in (-1, 1):
        x = W * 0.5 + side * 140
        figure(L, x, H * 0.9, 300, robe=(0.50, 0.50, 0.56), lean=-side * 0.4, arm=0.9)
        L.ink([(x - side * 60, H * 0.9 - 250), (x - side * 210, H * 0.9 - 330)], width=4, color=(0.5, 0.5, 0.56), smooth=0)
    t = s.tmap('duel')
    t[:] = fbm(H, W, 5, np.random.default_rng(5), 4) * 0.9 + 0.05
    return s


def s10_palace():
    s = Scene(FILM, "s10_palace", seed=710)
    sky_layer(s, 'gold', clouds_n=6)
    L, ys = ground_layer(s, 0.8, 10, (0.80, 0.76, 0.58), (0.70, 0.66, 0.50))
    L = s.layer('beams', 0.4)
    yg = H * 0.8
    for k in range(9):     # 封建的梁架（底層）
        x = W * 0.12 + k * W * 0.095
        L.ink([(x, yg), (x + 60, yg - 420)], width=6, color=INK_BROWN)
        L.ink([(x + 60, yg - 420), (x + W * 0.095, yg)], width=4, color=INK_BROWN)
    L.ink([(W * 0.1, yg - 420), (W * 0.92, yg - 420)], width=6, color=INK_BROWN, smooth=0)
    L = s.layer('facade', 0.4)
    S = L.S
    L.wash(S.poly([(W * 0.1, yg), (W * 0.1, yg - 380), (W * 0.9, yg - 380), (W * 0.9, yg)], rough=1), (0.94, 0.88, 0.76), density=0.7, edge=0.9)
    for k in range(18):
        x = W * 0.13 + k * W * 0.043
        L.wash(S.poly([(x - 14, yg - 60), (x - 14, yg - 230), (x + 14, yg - 230), (x + 14, yg - 60)], rough=0.4), (0.62, 0.70, 0.80), density=0.6)
        L.box(x - 14, yg - 230, x + 14, yg - 60, width=1.0, dark=0.5)
    L.wash(S.poly([(W * 0.08, yg - 380), (W * 0.92, yg - 380), (W * 0.5, yg - 520)], rough=1), (0.66, 0.66, 0.74), density=0.8, edge=0.9)
    L.ink([(W * 0.08, yg - 380), (W * 0.5, yg - 520), (W * 0.92, yg - 380)], width=2, smooth=0)
    L.box(W * 0.1, yg - 380, W * 0.9, yg, width=2)
    t = s.tmap('facade')
    t[:] = fbm(H, W, 6, np.random.default_rng(10), 4) * 0.9 + 0.05
    return s


def s11_america():
    s = Scene(FILM, "s11_america", seed=711)
    L = s.layer('hall', 0.0, opaque=True)
    S = L.S
    L.wash(np.ones((H, W), F32), (0.90, 0.86, 0.78), density=0.6, edge=0, gran=0.4)
    for k, x in enumerate([W * 0.2, W * 0.5, W * 0.8]):     # 三道門
        L.wash(S.poly([(x - 150, H * 0.8), (x - 150, H * 0.34), (x, H * 0.26), (x + 150, H * 0.34), (x + 150, H * 0.8)], rough=1),
               [(0.52, 0.36, 0.28), (0.36, 0.42, 0.52), (0.44, 0.48, 0.38)][k], density=0.9, edge=0.8)
        L.ink([(x - 150, H * 0.8), (x - 150, H * 0.34), (x, H * 0.26), (x + 150, H * 0.34), (x + 150, H * 0.8)], width=2.4, smooth=0)
    for x in np.arange(80, W, 300):
        L.wash(S.poly([(x - 24, H * 0.82), (x - 20, H * 0.08), (x + 20, H * 0.08), (x + 24, H * 0.82)], rough=0.5), (0.96, 0.94, 0.90), density=0.5, edge=0.9)
    L = s.layer('floor', 0.4)
    S = L.S
    L.wash(S.below_curve(np.full(W, H * 0.82, F32), 1), (0.62, 0.48, 0.38), density=0.85, edge=0.6)
    cx, yg = W * 0.5, H * 0.92
    th = [(cx - 110, yg), (cx - 110, yg - 360), (cx - 70, yg - 430), (cx + 70, yg - 430), (cx + 110, yg - 360), (cx + 110, yg)]
    L.wash(S.poly(th, rough=0.8), (0.66, 0.50, 0.34), density=0.9, edge=0.8)
    L.ink(th, width=2, smooth=0)
    L.wash(S.poly([(cx - 90, yg - 180), (cx + 90, yg - 180), (cx + 90, yg - 150), (cx - 90, yg - 150)], rough=0.4), (0.52, 0.36, 0.28), density=0.9)
    s.meta.update(throne=[cx, yg - 300])
    return s


def s12_zhouqin():
    s = Scene(FILM, "s12_zhouqin", seed=712)
    sky_layer(s, 'day', clouds_n=8)
    far_layer(s, 0.56, 120, (0.72, 0.76, 0.88))
    L, ys = ground_layer(s, 0.66, 30, (0.72, 0.80, 0.52), (0.62, 0.70, 0.46))
    for i, x in enumerate(np.arange(120, W * 0.48, 180)):
        yg = gy(ys, x) + 60 + (i % 3) * 90
        great_wall(L, yg, 34, color=(0.80, 0.74, 0.64), x0=x - 70, x1=x + 70)
        house(L, x, yg - 34, 90, 60, roof=ROBES[i % 6], windows=1, chimney=False)
    great_wall(L, H * 0.92, 260, color=(0.58, 0.56, 0.60), x0=W * 0.52, x1=W)
    L.ink([(W * 0.5, H * 0.3), (W * 0.5, H)], width=1.4, dark=0.5, smooth=0, dry=0.6)
    return s


ALL = [s1_path, s2_elder, s3_king, s4_market, s5_homage, s6_network, s7_manor, s8_writ, s9_jury, s10_palace, s11_america, s12_zhouqin]
