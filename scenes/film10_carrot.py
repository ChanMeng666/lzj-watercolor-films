"""第十部《胡蘿蔔》— 反勵志的人生建議"""
import numpy as np
from kit import *

FILM = "film10"
ROBES = [(0.70, 0.34, 0.30), (0.30, 0.42, 0.62), (0.76, 0.62, 0.34), (0.40, 0.54, 0.40), (0.56, 0.38, 0.56), (0.80, 0.50, 0.36)]


def room(s, col=(0.80, 0.72, 0.62), glow=None):
    L = s.layer('room', 0.0, opaque=True)
    S = L.S
    L.wash(np.ones((H, W), F32), col, density=0.75, edge=0, gran=0.4)
    if glow:
        L.wash(S.radial(glow[0], glow[1], glow[2]), (0.98, 0.88, 0.66), density=0.6, edge=0, bloom=30)
    L.wash(1 - S.radial(W * 0.5, H * 0.5, W * 0.72), (0.36, 0.30, 0.32), density=0.7, edge=0, bloom=40)
    return L


def s1_birth():
    s = Scene(FILM, "s1_birth", seed=1001, w=int(W * 1.2))
    sky_layer(s, 'dawn', clouds_n=7)
    L, ys = ground_layer(s, 0.62, 10, (0.72, 0.78, 0.52), (0.62, 0.68, 0.46))
    water(L, H * 0.74, H * 0.94, (0.56, 0.70, 0.84))
    doors = []
    for i, x in enumerate(np.arange(300, s.w, 520)):   # 河岸上的幾扇門：不同的家
        yg = gy(ys, x) + 60
        kind = i % 4
        if kind == 0:
            castle(L, x, yg, 80)
        elif kind == 1:
            hut(L, x, yg, 140, snow=False)
        elif kind == 2:
            house(L, x, yg, 220, 150, roof=(0.40, 0.42, 0.56), windows=3)
        else:
            hut(L, x, yg, 110, snow=False)
        doors.append([float(x), yg])
    s.meta.update(doors=doors, river_y=H * 0.82)
    sp = s.sprite('basket', 260, 180, anchor=(0.5, 0.7))
    S = sp.S
    sp.wash(S.ellipse(130, 110, 110, 46, rough=1), (0.76, 0.58, 0.34), density=0.95, edge=0.9, gran=0.7)
    for k in range(8):
        sp.ink([(40 + k * 25, 80), (36 + k * 25, 140)], width=1.2, dark=0.6, smooth=0)
    sp.wash(S.ellipse(120, 78, 50, 22, rough=0.6), (0.96, 0.92, 0.86), density=0.6, edge=0.8)
    sp.wash(S.ellipse(150, 66, 18, 16, rough=0.4), (0.94, 0.80, 0.70), density=0.8, edge=0.8)
    return s


def s2_drop():
    s = Scene(FILM, "s2_drop", seed=1002)
    room(s, col=(0.40, 0.36, 0.42), glow=(W * 0.5, H * 0.6, 600))
    L = s.layer('bowl', 0.4)
    S = L.S
    cx, cy = W * 0.5, H * 0.72
    L.wash(S.ellipse(cx, cy, 520, 110, rough=1), (0.20, 0.20, 0.26), density=0.95, edge=0.8)
    L.wash(S.poly([(cx - 520, cy), (cx + 520, cy), (cx + 380, cy + 230), (cx - 380, cy + 230)], rough=1) * (1 - S.ellipse(cx, cy, 520, 110, rough=0)),
           (0.56, 0.44, 0.36), density=0.9, edge=0.9, gran=0.6)
    a = np.linspace(0, 2 * np.pi, 60)
    L.ink([(cx + np.cos(t) * 520, cy + np.sin(t) * 110) for t in a], width=2.4)
    s.meta.update(bowl=[cx, cy])
    return s


def s3_donkey():
    s = Scene(FILM, "s3_donkey", seed=1003)
    sky_layer(s, 'day', clouds_n=8)
    far_layer(s, 0.56, 110, (0.72, 0.76, 0.86))
    L, ys = ground_layer(s, 0.66, 10, (0.80, 0.74, 0.56), (0.70, 0.64, 0.50))
    S = L.S
    cx, cy = W * 0.5, H * 0.8
    a = np.linspace(0, 2 * np.pi, 80)
    L.ink([(cx + np.cos(t) * 620, cy + np.sin(t) * 150) for t in a], width=2.0, color=INK_BROWN, dark=0.5, dry=0.6)   # 磨出來的圓形小徑
    L.wash(S.ellipse(cx, cy, 640, 160, rough=3) * (1 - S.ellipse(cx, cy, 590, 130, rough=3)), (0.70, 0.60, 0.46), density=0.6, edge=0.5)
    millstone(L, cx, cy - 30, 170)
    s.meta.update(center=[cx, cy - 60], ring=[620, 150])
    for p in range(4):
        sp = s.sprite(f'donkey_{p}', 360, 300, anchor=(0.5, 0.96))
        donkey(sp, 170, 288, 240, phase=p / 4)
    sp = s.sprite('carrot', 120, 200, anchor=(0.5, 0.05))
    sp.ink([(60, 6), (60, 90)], width=1.4, dark=0.7, smooth=0)
    sp.wash(sp.S.poly([(40, 90), (80, 90), (60, 190)], rough=0.8), (0.95, 0.52, 0.18), density=1.0, edge=0.9)
    sp.ink([(60, 90), (44, 70)], width=2.5, color=(0.30, 0.56, 0.24)); sp.ink([(60, 90), (76, 68)], width=2.5, color=(0.30, 0.56, 0.24))
    return s


def s4_caliph():
    s = Scene(FILM, "s4_caliph", seed=1004)
    L = s.layer('palace', 0.0, opaque=True)
    S = L.S
    L.wash(np.ones((H, W), F32), (0.20, 0.20, 0.30), density=0.9, edge=0, gran=0.4)
    for x in np.arange(120, W, 280):   # 拱廊
        arc = [(x - 100, H * 0.9)] + [(x + np.cos(t) * 100, H * 0.4 - np.sin(t) * 140) for t in np.linspace(np.pi, 0, 14)] + [(x + 100, H * 0.9)]
        L.ink(arc, width=2.2, color=(0.70, 0.62, 0.40), dark=0.7)
    L = s.layer('carpet', 0.4)
    S = L.S
    cp = [(W * 0.2, H * 0.98), (W * 0.36, H * 0.72), (W * 0.64, H * 0.72), (W * 0.8, H * 0.98)]
    L.wash(S.poly(cp, rough=1), (0.62, 0.20, 0.22), density=0.95, edge=0.9, gran=0.6)
    L.ink(cp + [cp[0]], width=2, smooth=0)
    figure(L, W * 0.5, H * 0.86, 300, robe=(0.92, 0.88, 0.80), arm=0.2)
    L.wash(S.ellipse(W * 0.5, H * 0.86 - 290, 46, 30, rough=0.4), (0.96, 0.94, 0.90), density=0.6)   # 頭巾
    rng = np.random.default_rng(14)
    lamps = []
    for k in range(240):
        lamps.append([float(rng.uniform(60, W - 60)), float(rng.uniform(H * 0.08, H * 0.62)), 10.0])
    s.meta.update(lamps=lamps)
    return s


def s5_chase():
    s = Scene(FILM, "s5_chase", seed=1005, w=int(W * 1.2))
    sky_layer(s, 'day', clouds_n=8)
    far_layer(s, 0.56, 120, (0.72, 0.76, 0.88))
    L, ys = ground_layer(s, 0.66, 30, (0.72, 0.80, 0.52), (0.62, 0.70, 0.46))
    water(L, H * 0.8, H * 0.92, (0.56, 0.70, 0.84))
    boat(L, s.w * 0.78, H * 0.86, 120, sail=(0.90, 0.86, 0.78))
    figure(L, s.w * 0.78 - 30, H * 0.86 - 30, 160, robe=(0.40, 0.42, 0.56), arm=0.6, lean=0.4)   # 埋頭划船的人
    L.ink([(s.w * 0.78 + 30, H * 0.86 - 80), (s.w * 0.78 + 140, H * 0.9)], width=3, color=INK_BROWN)
    s.meta.update(rower=[s.w * 0.78 - 30, H * 0.86 - 190], path_y=gy(ys, 600) + 120)
    for p in range(4):
        sp = s.sprite(f'runner_{p}', 220, 300, anchor=(0.5, 0.96))
        ph = np.sin(p / 4 * 2 * np.pi)
        figure(sp, 110, 288, 240, robe=(0.62, 0.36, 0.30), lean=0.5, legs=ph, pose=ph, arm=0.9)
    for k, o in enumerate([0.15, 0.6, 1.0]):
        sp = s.sprite(f'bfly_{k}', 200, 180, anchor=(0.5, 0.5)); butterfly(sp, 100, 96, 70, open_=o)
    fg_layer(s)
    return s


def s6_cushion():
    s = Scene(FILM, "s6_cushion", seed=1006)
    room(s, col=(0.86, 0.76, 0.70), glow=(W * 0.4, H * 0.5, 700))
    L = s.layer('cushions', 0.4)
    S = L.S
    rng = np.random.default_rng(6)
    for k in range(16):
        x, y = W * 0.4 + rng.normal(0, 300), H * 0.8 + rng.normal(0, 60)
        m = S.blob(x, y, rng.uniform(90, 150), n=6, spread=0.4, squash=0.55, rough=6)
        L.wash(m, [(0.90, 0.62, 0.66), (0.70, 0.66, 0.86), (0.94, 0.84, 0.56), (0.74, 0.86, 0.74)][k % 4], density=0.7, edge=0.9)
        canopy_contour_ink(L, m, width=1.2, frac=0.6)
    figure(L, W * 0.42, H * 0.76, 260, robe=(0.56, 0.52, 0.62), lean=-0.9, arm=0.0)
    # 窗外：操縱的線
    wx = W * 0.72
    L.wash(S.poly([(wx, H * 0.14), (wx + 420, H * 0.14), (wx + 420, H * 0.6), (wx, H * 0.6)], rough=1), (0.46, 0.50, 0.64), density=0.85, edge=0.8)
    L.box(wx, H * 0.14, wx + 420, H * 0.6, width=4, color=INK_BROWN)
    for k in range(4):
        L.ink([(wx + 120 + k * 60, H * 0.14), (W * 0.42 + (k - 1.5) * 30, H * 0.56)], width=1.0, dark=0.5, smooth=0)
    figure(L, wx + 250, H * 0.58, 300, robe=(0.20, 0.20, 0.26), skin=(0.24, 0.22, 0.28), arm=1.0)
    return s


def s7_mask():
    s = Scene(FILM, "s7_mask", seed=1007)
    room(s, col=(0.82, 0.76, 0.66), glow=(W * 0.36, H * 0.5, 600))
    L = s.layer('fig', 0.4)
    S = L.S
    yg = H * 0.92
    L.wash(S.below_curve(np.full(W, yg, F32), 1), (0.56, 0.44, 0.36), density=0.85)
    figure(L, W * 0.32, yg, 560, robe=(0.42, 0.40, 0.52), arm=0.7)
    mx, my = W * 0.32 + 30, yg - 560 + 50
    L.wash(S.ellipse(mx, my, 70, 86, rough=1), (0.96, 0.90, 0.80), density=0.8, edge=0.9)          # 面具
    L.wash(S.ellipse(mx - 26, my - 14, 12, 8, rough=0.3), (0.20, 0.18, 0.20), density=1.0)
    L.wash(S.ellipse(mx + 26, my - 14, 12, 8, rough=0.3), (0.20, 0.18, 0.20), density=1.0)
    L.ink([(mx - 30, my + 30), (mx, my + 44), (mx + 30, my + 30)], width=2.4, color=(0.70, 0.20, 0.18))
    for k in range(5):  # 顏料從邊緣滴下
        L.ink([(mx - 60 + k * 30, my + 70), (mx - 62 + k * 30, my + 130 + k * 14)], width=3, color=(0.80, 0.70, 0.56), dark=0.7)
    # 漏水的桶
    bx, by = W * 0.72, yg
    L.wash(S.poly([(bx - 160, by - 360), (bx + 160, by - 360), (bx + 130, by), (bx - 130, by)], rough=1), (0.58, 0.44, 0.30), density=0.95, edge=0.9)
    for k in range(4):
        L.ink([(bx - 156 + k * 6, by - 360 + k * 110), (bx + 156 - k * 8, by - 360 + k * 110)], width=3, smooth=0)
    holes = [[bx - 140, by - 240], [bx + 136, by - 160], [bx - 120, by - 80], [bx + 60, by - 60]]
    s.meta.update(holes=holes, mask=[mx, my])
    return s


def s8_captain():
    s = Scene(FILM, "s8_captain", seed=1008, w=int(W * 1.2))
    sky_layer(s, 'storm', clouds_n=12)
    L = s.layer('sea', 0.3)
    water(L, H * 0.6, H * 1.0, (0.40, 0.48, 0.58))
    L = s.layer('giant', 0.45)
    S = L.S
    # 一個躺著不動的巨大身體，上面站著互相爭吵的小船長
    body = [(s.w * 0.2, H * 0.78), (s.w * 0.3, H * 0.62), (s.w * 0.6, H * 0.6), (s.w * 0.75, H * 0.66), (s.w * 0.82, H * 0.78)]
    L.wash(S.poly(body, rough=6), (0.62, 0.56, 0.60), density=0.9, edge=0.8, gran=0.6)
    L.wash(S.ellipse(s.w * 0.86, H * 0.7, 120, 100, rough=4), (0.86, 0.74, 0.66), density=0.85, edge=0.8)
    L.ink(body, width=2.2, smooth=1)
    caps = []
    for k in range(5):
        x = s.w * 0.36 + k * 160
        figure(L, x, H * 0.61 + (k % 2) * 6, 140, robe=ROBES[k], arm=0.6 + 0.3 * (k % 2), lean=(k % 3 - 1) * 0.4)
        caps.append([x, H * 0.61 - 150])
    L.ink([(s.w * 0.5, H * 0.6), (s.w * 0.5, H * 0.38)], width=4, color=INK_BROWN, smooth=0)   # 舵杆
    s.meta.update(caps=caps)
    return s


def s9_swim():
    s = Scene(FILM, "s9_swim", seed=1009)
    sky_layer(s, 'day', clouds_n=8)
    far_layer(s, 0.56, 100, (0.72, 0.78, 0.88))
    L = s.layer('lake', 0.4)
    water(L, H * 0.6, H * 1.0, (0.50, 0.68, 0.84))
    S = L.S
    L.wash(S.poly([(0, H * 0.7), (W * 0.42, H * 0.7), (W * 0.42, H * 0.74), (0, H * 0.74)], rough=1), (0.62, 0.46, 0.32), density=0.95, edge=0.9)
    for x in np.arange(40, W * 0.42, 120):
        L.ink([(x, H * 0.74), (x, H * 0.9)], width=6, color=INK_BROWN, smooth=0)
    L.ink([(0, H * 0.7), (W * 0.42, H * 0.7)], width=2, smooth=0)
    s.meta.update(edge=[W * 0.42, H * 0.7], water=[W * 0.55, H * 0.82])
    for k, (ln, arm) in enumerate([(0.0, 0.1), (0.4, 0.9), (1.0, 1.0)]):
        sp = s.sprite(f'diver_{k}', 300, 340, anchor=(0.5, 0.96))
        figure(sp, 150, 328, 280, robe=(0.30, 0.44, 0.62), lean=ln, arm=arm, legs=0.3 * k)
    return s


def s10_cocoon():
    s = Scene(FILM, "s10_cocoon", seed=1010)
    sky_layer(s, 'dawn', clouds_n=6)
    L = s.layer('branch', 0.4)
    S = L.S
    L.ink([(-20, H * 0.24), (W * 0.4, H * 0.3), (W * 0.7, H * 0.26), (W + 20, H * 0.32)], width=22, color=INK_BROWN, dark=0.9)
    for x, y in [(W * 0.2, H * 0.27), (W * 0.55, H * 0.29)]:
        leaf = [(x, y), (x + 100, y + 40), (x + 160, y + 140), (x + 40, y + 100)]
        L.wash(S.poly(leaf, rough=1.5), (0.50, 0.70, 0.36), density=0.9, edge=0.9)
        L.ink(leaf + [leaf[0]], width=1.6)
    cx, cy = W * 0.46, H * 0.44
    L.ink([(cx, H * 0.3), (cx, cy - 120)], width=1.6, dark=0.6, smooth=0)
    L = s.layer('cocoon', 0.4)
    S = L.S
    m = S.ellipse(cx, cy, 70, 130, rough=2)
    L.wash(m, (0.78, 0.72, 0.56), density=0.9, edge=0.9, gran=0.8)
    for k in range(7):
        L.ink([(cx - 60, cy - 100 + k * 32), (cx + 60, cy - 90 + k * 32)], width=1.2, dark=0.5)
    L = s.layer('broken', 0.4)
    S = L.S
    L.wash(S.poly([(cx - 70, cy - 20), (cx - 60, cy + 130), (cx + 60, cy + 130), (cx + 70, cy - 20), (cx + 30, cy + 10), (cx, cy - 30), (cx - 30, cy + 10)], rough=2),
           (0.78, 0.72, 0.56), density=0.9, edge=0.9, gran=0.8)
    for k, o in enumerate([0.1, 0.5, 1.0]):
        sp = s.sprite(f'bfly_{k}', 300, 260, anchor=(0.5, 0.5))
        butterfly(sp, 150, 140, 110, open_=o, c1=(0.86, 0.60, 0.36), c2=(0.42, 0.40, 0.58))
        sp.ink([(100, 60), (130, 90), (95, 110)], width=1.4, dark=0.6)   # 皺巴巴的翅膀
    s.meta.update(cocoon=[cx, cy])
    return s


def s11_gardener():
    s = Scene(FILM, "s11_gardener", seed=1011, w=int(W * 1.2))
    sky_layer(s, 'day', clouds_n=8)
    far_layer(s, 0.54, 140, (0.72, 0.76, 0.88))
    L, ys = ground_layer(s, 0.7, 40, (0.70, 0.66, 0.48), (0.60, 0.56, 0.42))
    for k, x in enumerate(np.arange(200, s.w * 0.6, 220)):
        tree_round(L, x, gy(ys, x) + 40, 120 + k * 40, green=(0.56, 0.72, 0.40))
    hole_x = s.w * 0.68
    L.wash(L.S.ellipse(hole_x, gy(ys, hole_x) + 50, 60, 14, rough=2), (0.36, 0.28, 0.24), density=0.95)
    s.meta.update(dig=[hole_x + 130, gy(ys, hole_x) + 60])
    for p in range(3):
        sp = s.sprite(f"digger_{p}", 300, 360, anchor=(0.5, 0.95))
        digger(sp, 130, 342, 280, phase=p / 2)
    fg_layer(s)
    return s


def s12_ridge():
    s = Scene(FILM, "s12_ridge", seed=1012, w=int(W * 1.3))
    sky_layer(s, 'gold', clouds_n=8, glow=(W * 0.9, H * 0.6, 300, (0.99, 0.76, 0.46)))
    far_layer(s, 0.62, 260, (0.62, 0.56, 0.72), snow=True)
    L = s.layer('ridge', 0.45)
    S = L.S
    xs = np.arange(s.w, dtype=F32)
    ys = H * 0.74 - 120 * np.sin(xs / s.w * np.pi) + 14 * noise1d(s.w, 10, L.rng)
    L.wash(S.below_curve(ys, 2), (0.50, 0.44, 0.48), density=0.9, edge=0.8, gran=0.6)
    L.wash(S.below_curve(ys, 2) * S.vgrad(H * 0.6, H), (0.30, 0.26, 0.32), density=0.6, edge=0, bloom=20)
    ridge_ink(L, ys, 2.2, gap=0.0)
    s.meta.update(ridge=[[float(x), float(ys[int(x)])] for x in np.arange(0, s.w, 40)])
    for p in range(4):
        sp = s.sprite(f'walker_{p}', 200, 300, anchor=(0.5, 0.96))
        ph = np.sin(p / 4 * 2 * np.pi)
        figure(sp, 100, 288, 250, robe=(0.36, 0.30, 0.34), lean=0.3, legs=ph * 0.8, pose=ph, arm=0.15)
    return s


ALL = [s1_birth, s2_drop, s3_donkey, s4_caliph, s5_chase, s6_cushion, s7_mask, s8_captain, s9_swim, s10_cocoon, s11_gardener, s12_ridge]
