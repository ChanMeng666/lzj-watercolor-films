"""第八部《血酬》— 武德、撫卹金、土豪與逆淘汰"""
import numpy as np
from kit import *

FILM = "film8"
ROBES = [(0.70, 0.34, 0.30), (0.30, 0.42, 0.62), (0.76, 0.62, 0.34), (0.40, 0.54, 0.40), (0.56, 0.38, 0.56), (0.80, 0.50, 0.36)]


def shield(L, x, y, r, col=(0.62, 0.24, 0.20)):
    S = L.S
    L.wash(S.ellipse(x, y, r, r * 1.15, rough=0.8), col, density=0.95, edge=0.9, gran=0.5)
    a = np.linspace(0, 2 * np.pi, 40)
    L.ink([(x + np.cos(t) * r, y + np.sin(t) * r * 1.15) for t in a], width=2.2)
    L.wash(S.ellipse(x, y, r * 0.22, r * 0.22, rough=0.3), (0.80, 0.70, 0.40), density=0.95)


def spearman(L, x, yg, h, robe, side=1):
    figure(L, x, yg, h, robe=robe, arm=0.6)
    L.ink([(x + side * h * 0.2, yg + 4), (x + side * h * 0.24, yg - h * 1.25)], width=max(2, h * 0.018), color=INK_BROWN, smooth=0)
    L.wash(L.S.poly([(x + side * h * 0.24 - 8, yg - h * 1.25), (x + side * h * 0.24, yg - h * 1.36), (x + side * h * 0.24 + 8, yg - h * 1.25)],
                    rough=0.3), (0.56, 0.58, 0.64), density=0.95)


def s1_two():
    s = Scene(FILM, "s1_two", seed=801)
    sky_layer(s, 'dusk', clouds_n=7)
    far_layer(s, 0.6, 120, (0.62, 0.60, 0.76))
    L, ys = ground_layer(s, 0.76, 30, (0.66, 0.70, 0.50), (0.54, 0.58, 0.44))
    lamps = []
    for x in (300, 460, 620):
        lamps += [list(v) for v in house(L, x, gy(ys, x) + 20, 140, 100)]
    palisade(L, 160, 760, gy(ys, 460) + 70, 90)
    lamps.append(watchtower(L, 820, gy(ys, 820) + 40, 220, lit=True))
    for x in (1580, 1760, 1940):
        house(L, x, gy(ys, x) + 20, 140, 100, roof=(0.50, 0.44, 0.42), wall=(0.70, 0.66, 0.62))
    for k in range(6):   # 倒塌的柵欄
        x = 1450 + k * 110
        L.ink([(x, gy(ys, x) + 80), (x + 60, gy(ys, x) + 40 - (k % 2) * 30)], width=4, color=INK_BROWN)
    L.wash(L.S.poly([(1500, H), (1700, gy(ys, 1700) + 60), (2304, gy(ys, 2200) + 40), (2304, H)], rough=3), (0.30, 0.28, 0.36), density=0.5, edge=0.2, occlude=False)
    s.meta.update(lamps=lamps, tower=lamps[-1])
    fg_layer(s)
    return s


def s2_shield():
    s = Scene(FILM, "s2_shield", seed=802)
    sky_layer(s, 'night', clouds_n=0, density=0.95)
    L, ys = ground_layer(s, 0.7, 20, (0.30, 0.32, 0.36), (0.24, 0.26, 0.30), ink=1.0)
    cx, cy = W * 0.5, H * 0.86
    rng = np.random.default_rng(2)
    pts = []
    for k in range(12):
        a = np.pi * (1.0 + k / 11)
        pts.append((cx + np.cos(a) * 640, cy + np.sin(a) * 160))
    for i, (x, y) in enumerate(sorted(pts, key=lambda p: p[1])):
        spearman(L, x, y, 240, (0.30, 0.28, 0.34), side=1 if x > cx else -1)
    # 犁留在田裏、盾掛在門上
    house(L, W * 0.15, gy(ys, W * 0.15) + 20, 220, 150, roof=(0.32, 0.28, 0.32), wall=(0.42, 0.40, 0.44), win_light=True)
    shield(L, W * 0.15 + 50, gy(ys, W * 0.15) - 110, 34)
    L.ink([(W * 0.82, gy(ys, W * 0.82) + 60), (W * 0.9, gy(ys, W * 0.82) + 10)], width=5, color=INK_BROWN)
    L.ink([(W * 0.82, gy(ys, W * 0.82) + 60), (W * 0.8, gy(ys, W * 0.82) + 80)], width=7, color=(0.5, 0.5, 0.56))
    s.meta.update(fire=[cx, cy - 40])
    return s


def s3_widow():
    s = Scene(FILM, "s3_widow", seed=803)
    sky_layer(s, 'grey', clouds_n=8)
    L, ys = ground_layer(s, 0.84, 10, (0.66, 0.66, 0.56), (0.56, 0.56, 0.50))
    S = L.S
    gx = W * 0.62
    for side in (-1, 1):
        L.wash(S.poly([(gx + side * 220, H * 0.86), (gx + side * 220, H * 0.3), (gx + side * 340, H * 0.3), (gx + side * 340, H * 0.86)], rough=1.5),
               (0.70, 0.68, 0.66), density=0.9, edge=0.8, gran=0.8)
    L.wash(S.poly([(gx - 340, H * 0.3), (gx + 340, H * 0.3), (gx + 340, H * 0.22), (gx - 340, H * 0.22)], rough=1.5), (0.66, 0.64, 0.62), density=0.9)
    figure(L, W * 0.4, H * 0.9, 380, robe=(0.24, 0.24, 0.30), arm=0.5, lean=0.1)             # 寡婦
    figure(L, W * 0.44, H * 0.9, 200, robe=(0.36, 0.36, 0.44), arm=0.2)                       # 孩子
    figure(L, W * 0.58, H * 0.9, 400, robe=(0.56, 0.24, 0.22), arm=0.6, lean=-0.1)            # 武士團的人
    L.wash(S.blob(W * 0.5, H * 0.66, 30, n=5, spread=0.3, rough=2), (0.70, 0.56, 0.34), density=0.95, edge=0.9)   # 錢袋
    L.ink([(W * 0.5 - 8, H * 0.635), (W * 0.5 + 8, H * 0.635)], width=2, smooth=0)
    s.meta.update(purse=[W * 0.5, H * 0.66])
    return s


def s4_queen():
    s = Scene(FILM, "s4_queen", seed=804)
    L = s.layer('room', 0.0, opaque=True)
    S = L.S
    L.wash(np.ones((H, W), F32), (0.80, 0.72, 0.62), density=0.7, edge=0, gran=0.4)
    for wx, kind in ((W * 0.12, 'ships'), (W * 0.72, 'graves')):
        ww, wh = 460, 520
        L.wash(S.poly([(wx, H * 0.16), (wx + ww, H * 0.16), (wx + ww, H * 0.16 + wh), (wx, H * 0.16 + wh)], rough=1), (0.80, 0.86, 0.92), density=0.6, edge=0.7)
        L.box(wx, H * 0.16, wx + ww, H * 0.16 + wh, width=4, color=INK_BROWN)
        sub = s.layer('view_' + kind, 0.0)
    L = s.layer('scenery', 0.0)
    S = L.S
    wx = W * 0.12
    water(L, H * 0.5, H * 0.16 + 520, (0.50, 0.66, 0.82))
    L.clip(S.poly([(wx + 4, H * 0.16 + 4), (wx + 456, H * 0.16 + 4), (wx + 456, H * 0.16 + 516), (wx + 4, H * 0.16 + 516)], rough=0))
    ship(L, wx + 160, H * 0.56, 70); ship(L, wx + 340, H * 0.6, 56)
    wx2 = W * 0.72
    L2 = s.layer('graves', 0.0)
    S = L2.S
    L2.wash(S.poly([(wx2 + 4, H * 0.5), (wx2 + 456, H * 0.46), (wx2 + 456, H * 0.16 + 516), (wx2 + 4, H * 0.16 + 516)], rough=1), (0.62, 0.70, 0.50), density=0.8)
    for k in range(12):
        x = wx2 + 40 + (k % 6) * 72
        y = H * 0.44 + (k // 6) * 90
        L2.ink([(x, y), (x, y - 50)], width=4, smooth=0); L2.ink([(x - 16, y - 34), (x + 16, y - 34)], width=4, smooth=0)
    L = s.layer('desk', 0.4)
    S = L.S
    yg = H * 0.96
    L.wash(S.poly([(W * 0.3, yg - 200), (W * 0.7, yg - 200), (W * 0.7, yg), (W * 0.3, yg)], rough=1), (0.48, 0.32, 0.24), density=0.95, edge=0.8)
    figure(L, W * 0.5, yg - 170, 380, robe=(0.62, 0.22, 0.26), arm=0.3)
    cx = W * 0.5
    top = yg - 170 - 380
    cr = [(cx - 26, top), (cx - 30, top - 40), (cx - 10, top - 20), (cx, top - 46), (cx + 10, top - 20), (cx + 30, top - 40), (cx + 26, top)]
    L.wash(S.poly(cr, rough=0.3), (0.95, 0.76, 0.30), density=1.0, edge=0.9); L.ink(cr + [cr[0]], width=1.6, smooth=0)
    book(L, W * 0.44, yg - 200, 220, 40, open_=False, color=(0.30, 0.36, 0.30))
    return s


def s5_banner():
    s = Scene(FILM, "s5_banner", seed=805, w=int(W * 1.2))
    sky_layer(s, 'dusk', clouds_n=6)
    L, ys = ground_layer(s, 0.74, 20, (0.66, 0.66, 0.52), (0.56, 0.56, 0.46))
    S = L.S
    hx = s.w * 0.3
    wins = house(L, hx, gy(ys, hx) + 20, 520, 280, roof=(0.42, 0.30, 0.30), wall=(0.80, 0.74, 0.64), windows=3, win_light=True, chimney=False)
    L.ink([(hx + 300, gy(ys, hx) - 480), (hx + 300, gy(ys, hx) + 20)], width=4, color=INK_BROWN, smooth=0)
    bn = [(hx + 300, gy(ys, hx) - 470), (hx + 520, gy(ys, hx) - 440), (hx + 480, gy(ys, hx) - 370), (hx + 300, gy(ys, hx) - 360)]
    L.wash(S.poly(bn, rough=1), (0.76, 0.18, 0.16), density=0.95, edge=0.9)
    L.ink(bn, width=1.6, smooth=1)
    L.wash(S.ellipse(hx - 120, gy(ys, hx) + 60, 70, 40, rough=1), (0.30, 0.28, 0.30), density=0.95)       # 飯鍋
    L.wash(S.poly([(hx + 60, gy(ys, hx) + 90), (hx + 200, gy(ys, hx) + 90), (hx + 200, gy(ys, hx) + 20), (hx + 60, gy(ys, hx) + 20)], rough=0.6),
           (0.60, 0.40, 0.24), density=0.95)                                                                   # 撫卹金箱
    L.box(hx + 60, gy(ys, hx) + 20, hx + 200, gy(ys, hx) + 90, width=1.6)
    s.meta.update(lamps=[list(v) for v in wins], door=[hx, gy(ys, hx) + 60], away=[s.w * 0.95, gy(ys, s.w * 0.95) + 60])
    for k in range(4):
        sp = s.sprite(f'follower_{k}', 200, 300, anchor=(0.5, 0.96))
        ph = np.sin(k / 4 * 2 * np.pi)
        figure(sp, 100, 288, 240, robe=ROBES[k % 6], lean=0.25, legs=ph * 0.7, pose=ph, arm=0.1)
    return s


def s6_wolves():
    s = Scene(FILM, "s6_wolves", seed=806, w=int(W * 1.2))
    sky_layer(s, 'grey', clouds_n=8)
    L = s.layer('forest', 0.3)
    ys = ground(L, H * 0.6, 20, (0.50, 0.60, 0.44), cells=3, ink=0.8)
    rng = np.random.default_rng(6)
    for k in range(18):
        x = s.w * 0.62 + rng.uniform(0, s.w * 0.4)
        tree_pine(L, x, gy(ys, x) + rng.uniform(0, 80), rng.uniform(300, 520), color=(0.26, 0.36, 0.32))
    L, ys2 = ground_layer(s, 0.78, 20, (0.66, 0.72, 0.50), (0.56, 0.62, 0.44))
    big_tree(L, s.w * 0.2, gy(ys2, s.w * 0.2) + 10, 700, seed_rng=np.random.default_rng(31))
    villagers(L, [(s.w * 0.12 + k * 90, gy(ys2, s.w * 0.12) + 60 + (k % 2) * 30) for k in range(6)], 190, rng)
    x = s.w * 0.5
    figure(L, x, gy(ys2, x) + 80, 330, robe=(0.40, 0.36, 0.46), arm=0.7, lean=0.2)
    shield(L, x + 70, gy(ys2, x) - 120, 70)
    for k in range(4):
        wolf(L, s.w * 0.66 + k * 150, gy(ys2, s.w * 0.66 + k * 150) + 40 + (k % 2) * 30, 200)
    fg_layer(s)
    return s


def s7_fort():
    s = Scene(FILM, "s7_fort", seed=807)
    sky_layer(s, 'dusk', clouds_n=6)
    far_layer(s, 0.56, 110, (0.62, 0.60, 0.76))
    L, ys = ground_layer(s, 0.76, 30, (0.66, 0.72, 0.48), (0.56, 0.60, 0.42))
    LM = L
    for x in (500, 700, 900):
        house(L, x, gy(ys, x) + 20, 160, 110)
    L = s.layer('fort', 0.45)
    t = s.tmap('fort')
    cx = 700
    x0, x1 = 260, 1140
    base = gy(ys, cx) + 120
    stages = [(60, 0.0), (130, 0.3), (220, 0.6)]
    for hh, tt in stages:
        m = L.S.poly([(x0, base), (x0, base - hh), (x1, base - hh), (x1, base)], rough=2)
        L.wash(m, (0.70, 0.62, 0.52), density=0.7, edge=0.9, gran=0.7)
        np.minimum(t, np.where(m > 0.2, tt, 9.0).astype(F32), out=t)
    lamps = []
    for k, tx in enumerate((x0, x1)):
        tw = tower(L, tx, base, 110, 380, cone=False, wall=(0.70, 0.62, 0.52))
        m = L.S.poly([(tx - 55, base), (tx - 55, base - 400), (tx + 55, base - 400), (tx + 55, base)], rough=1)
        np.minimum(t, np.where(m > 0.2, 0.85, 9.0).astype(F32), out=t)
        lamps.append(list(tw))
    L.box(x0, base - 220, x1, base, width=2)
    militia = [[1500 + k * 120, gy(ys, 1500 + k * 120) - 30 - k * 8] for k in range(6)]
    for x, y in militia:
        spearman(LM, x, y + 40, 150, (0.30, 0.30, 0.36))
    s.meta.update(lamps=lamps, militia=militia)
    fg_layer(s)
    return s


def s8_salt():
    s = Scene(FILM, "s8_salt", seed=808)
    sky_layer(s, 'day', clouds_n=7)
    L, ys = ground_layer(s, 0.8, 20, (0.76, 0.74, 0.56), (0.66, 0.64, 0.48))
    S = L.S
    for k in range(5):   # 鹽袋
        x = W * 0.36 + (k % 3) * 90
        y = H * 0.88 - (k // 3) * 80
        L.wash(S.blob(x, y, 56, n=6, spread=0.4, squash=1.1, rough=3), (0.84, 0.78, 0.64), density=0.9, edge=0.9)
        L.ink([(x - 20, y - 50), (x + 20, y - 52)], width=2, smooth=0)
    figure(L, W * 0.24, gy(ys, W * 0.24) + 80, 300, robe=(0.62, 0.56, 0.44), arm=0.5)         # 順民
    L.ink([(W * 0.12, gy(ys, W * 0.12) + 90), (W * 0.15, gy(ys, W * 0.12) - 200)], width=4, color=(0.62, 0.40, 0.24))   # 生鏽的矛
    spearman(L, W * 0.62, gy(ys, W * 0.62) + 90, 340, (0.40, 0.40, 0.46))                     # 雇傭兵
    # 劍 → 筆 → 鈴
    for k, (x, kind) in enumerate([(W * 0.78, 'sword'), (W * 0.86, 'brush'), (W * 0.94, 'bell')]):
        y = H * 0.5
        if kind == 'sword':
            L.ink([(x, y + 100), (x, y - 100)], width=6, color=(0.56, 0.58, 0.64), smooth=0); L.ink([(x - 30, y + 60), (x + 30, y + 60)], width=5, smooth=0)
        elif kind == 'brush':
            L.ink([(x, y + 100), (x, y - 60)], width=6, color=INK_BROWN, smooth=0); L.ink([(x, y - 60), (x, y - 110)], width=12, smooth=0)
        else:
            L.wash(S.poly([(x - 40, y + 60), (x - 30, y - 40), (x, y - 70), (x + 30, y - 40), (x + 40, y + 60)], rough=0.6), (0.72, 0.60, 0.30), density=0.95, edge=0.9)
        if k < 2:
            L.ink([(x + 18, y), (x + 50, y)], width=1.6, dark=0.6, smooth=0)
    return s


def s9_flood():
    s = Scene(FILM, "s9_flood", seed=809, w=int(W * 1.2))
    sky_layer(s, 'storm', clouds_n=12)
    L = s.layer('banks', 0.4)
    S = L.S
    xs = np.arange(s.w, dtype=F32)
    ys = H * 0.6 + 40 * noise1d(s.w, 4, L.rng)
    L.wash(S.below_curve(ys, 2) * (xs < s.w * 0.5)[None, :], (0.56, 0.66, 0.44), density=0.9, edge=0.8)
    L.wash(S.below_curve(ys + 30, 2) * (xs >= s.w * 0.5)[None, :], (0.90, 0.80, 0.60), density=0.9, edge=0.8, gran=0.8)
    big_tree(L, s.w * 0.24, gy(ys, s.w * 0.24) + 10, 640, seed_rng=np.random.default_rng(3))
    roots(L, s.w * 0.24, gy(ys, s.w * 0.24) + 20, 300, np.random.default_rng(7), width=5, n_main=6)
    for k in range(4):
        x = s.w * 0.62 + k * 170
        horse_rider(L, x, gy(ys, x) + 60, 170, phase=k / 4)
    L = s.layer('flood', 0.4)
    water(L, H * 0.74, H * 1.0, (0.40, 0.50, 0.62))
    s.meta.update(tree=[s.w * 0.24, gy(ys, s.w * 0.24) - 300], sand=[s.w * 0.75, gy(ys, s.w * 0.75)])
    return s


def s10_weeds():
    s = Scene(FILM, "s10_weeds", seed=810)
    sky_layer(s, 'day', clouds_n=7)
    L, ys = ground_layer(s, 0.56, 10, (0.62, 0.56, 0.42), (0.52, 0.46, 0.36))
    L = s.layer('flowers', 0.45)
    rng = np.random.default_rng(10)
    for _ in range(260):
        x, y = rng.uniform(0, W), rng.uniform(H * 0.6, H)
        L.ink([(x, y), (x, y - 40)], width=2, color=(0.40, 0.60, 0.30), smooth=0)
        L.wash(L.S.ellipse(x, y - 44, 9, 9, rough=0.3), ROBES[int(rng.integers(6))], density=0.85, edge=0.9)
    L = s.layer('resistant', 0.45)
    t = s.tmap('resistant')
    weeds(L, np.full(W, H * 0.58, F32), H, 40, col=(0.18, 0.24, 0.18), tmap=t, rng=rng, h=(90, 200))
    s.meta.update(plane_y=H * 0.22)
    sp = s.sprite('plane', 420, 200, anchor=(0.5, 0.5))
    S = sp.S
    sp.wash(S.poly([(30, 110), (330, 96), (390, 110), (330, 124)], rough=0.5), (0.80, 0.30, 0.24), density=0.95, edge=0.9)
    sp.wash(S.poly([(150, 60), (240, 60), (240, 160), (150, 160)], rough=0.5), (0.86, 0.80, 0.70), density=0.7, edge=0.9)
    sp.ink([(30, 110), (330, 96), (390, 110), (330, 124), (30, 110)], width=2, smooth=0)
    sp.ink([(390, 80), (390, 140)], width=3, smooth=0)
    return s


def s11_bridge():
    s = Scene(FILM, "s11_bridge", seed=811, w=int(W * 1.2))
    sky_layer(s, 'storm', clouds_n=10)
    far_layer(s, 0.56, 140, (0.52, 0.54, 0.64))
    L = s.layer('river', 0.45)
    S = L.S
    ys = ground(L, H * 0.62, 20, (0.50, 0.56, 0.44), cells=3, ink=1.0)
    water(L, H * 0.72, H * 1.0, (0.40, 0.50, 0.62))
    bx = s.w * 0.3
    arch = [(bx - 420, H * 0.62)]
    for k in range(3):
        cx = bx - 280 + k * 280
        for tt in np.linspace(np.pi, 0, 9):
            arch.append((cx + np.cos(tt) * 120, H * 0.76 - np.sin(tt) * 90))
    arch += [(bx + 420, H * 0.62), (bx + 420, H * 0.58), (bx - 420, H * 0.58)]
    L.wash(S.poly(arch, rough=1.5), (0.66, 0.62, 0.58), density=0.95, edge=0.8, gran=0.8)
    L.ink(arch, width=2.4)
    L = s.layer('newbridge', 0.45)
    bx2 = s.w * 0.74
    deck = [(bx2 - 400, H * 0.6), (bx2 + 400, H * 0.6), (bx2 + 400, H * 0.63), (bx2 - 400, H * 0.63)]
    L.wash(L.S.poly(deck, rough=0.6), (0.86, 0.40, 0.34), density=0.9, edge=0.9)
    for k in range(5):
        x = bx2 - 360 + k * 180
        L.ink([(x, H * 0.63), (x + 10, H * 0.8)], width=3, color=INK_BROWN, smooth=0)
    L.box(*[bx2 - 400, H * 0.6, bx2 + 400, H * 0.63], width=1.6)
    s.meta.update(new=[bx2, H * 0.62])
    for k in range(4):
        sp = s.sprite(f'dog_{k % 2}' if k < 2 else f'wolf_{k % 2}', 360, 280, anchor=(0.5, 0.96))
        if k < 2:
            wolf(sp, 160, 268, 200 + 40 * k, col=(0.78, 0.66, 0.44))
        else:
            wolf(sp, 160, 268, 200 + 40 * (k - 2), col=(0.36, 0.34, 0.40))
    return s


ALL = [s1_two, s2_shield, s3_widow, s4_queen, s5_banner, s6_wolves, s7_fort, s8_salt, s9_flood, s10_weeds, s11_bridge]
