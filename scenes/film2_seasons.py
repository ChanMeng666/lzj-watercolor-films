"""第二部《四季》— 文明的季候"""
import numpy as np
from scene import Scene, W, H
from wc import blur, F32
from motifs import *

FILM = "film2"


def s1_spring():
    s = Scene(FILM, "s1_spring", seed=201, w=int(W * 1.3))
    w = s.w
    L = s.layer("sky", 0.0, opaque=True)
    sky(L, top=(0.62, 0.74, 0.90), horizon=(0.98, 0.95, 0.86), y_h=H * 0.6)
    clouds(L, 12, H * 0.06, H * 0.36, (0.80, 0.82, 0.90), rmin=60, rmax=160, density=0.3)
    L = s.layer("far", 0.15)
    ys = mountains(L, H * 0.52, 200, (0.70, 0.76, 0.88), cells=4, sharp=0.3, density=0.5, ink=0.8, snow=True)
    L = s.layer("hills", 0.4)
    lamps = []
    ys = ground(L, H * 0.62, 150, (0.72, 0.84, 0.54), cells=5, second=(0.60, 0.72, 0.46), ink=1.2)
    # 每個山頭一座小城堡／塔：千百個小中心
    peaks = [i for i in range(80, w - 80, 8) if ys[i] < ys[max(0, i - 120)] and ys[i] <= ys[min(w - 1, i + 120)]]
    picks = []
    for p in peaks:
        if all(abs(p - q) > 300 for q in picks):
            picks.append(p)
    for i, p in enumerate(picks):
        yg = float(ys[p]) + 12
        if i % 2 == 0:
            lamps += [list(v) for v in castle(L, p, yg, 70)]
        else:
            lamps.append(list(tower(L, p, yg, 46, 130)))
    for x in range(140, w, 260):
        tree_round(L, x + L.rng.uniform(-60, 60), float(ys[min(w - 1, x)]) + 60, 110,
                   green=(0.64, 0.78, 0.42))
    s.meta["lamps"] = lamps
    L = s.layer("fg", 1.0)
    ys2 = ground(L, H * 0.94, 30, (0.58, 0.70, 0.40), cells=5, ink=2.0)
    field_strokes(L, ys2, H, None, n=500, h=(20, 50))
    blossom_tree(L, 260, float(ys2[260]) + 40, 560)
    blossom_tree(L, w - 300, float(ys2[w - 300]) + 40, 480)
    return s


def s2_summer():
    s = Scene(FILM, "s2_summer", seed=202, w=int(W * 1.3))
    w = s.w
    L = s.layer("sky", 0.0, opaque=True)
    sky(L, top=(0.50, 0.68, 0.92), horizon=(0.96, 0.95, 0.88), y_h=H * 0.55)
    clouds(L, 10, H * 0.05, H * 0.3, (0.76, 0.80, 0.90), rmin=80, rmax=200, density=0.35)
    L = s.layer("far", 0.15)
    mountains(L, H * 0.5, 120, (0.70, 0.78, 0.86), cells=3, density=0.45)
    L = s.layer("town", 0.4)
    ys = ground(L, H * 0.56, 30, (0.70, 0.80, 0.50), cells=4, ink=1.0)
    rng = L.rng
    xs = list(range(120, w - 100, 150))
    for i, x in enumerate(xs):
        if i == 7:
            church(L, x, float(ys[x]) + 10, 120)
            continue
        if i in (6, 8):
            continue
        hh = rng.uniform(80, 130)
        house(L, x, float(ys[x]) + 10, 130, hh, roof=[(0.76, 0.42, 0.32), (0.70, 0.48, 0.34), (0.62, 0.40, 0.38)][i % 3],
              wall=(0.95, 0.88, 0.74), windows=2)
    L = s.layer("river", 0.6)
    S = L.S
    water(L, H * 0.62, H * 0.86, (0.56, 0.72, 0.86))
    # 石橋
    bx = w * 0.62
    arch = [(bx - 380, H * 0.63)]
    for k in range(4):
        cx = bx - 285 + k * 190
        for t in np.linspace(np.pi, 0, 9):
            arch.append((cx + np.cos(t) * 80, H * 0.71 - np.sin(t) * 55))
    arch += [(bx + 380, H * 0.63), (bx + 380, H * 0.60), (bx - 380, H * 0.60)]
    L.wash(S.poly(arch, rough=1.5), (0.78, 0.72, 0.64), density=0.9, edge=0.7, gran=0.6)
    L.ink(arch, width=2.0, dark=0.75)
    L = s.layer("bank", 1.0)
    ys2 = ground(L, H * 0.9, 20, (0.56, 0.68, 0.38), cells=5, ink=2.0)
    field_strokes(L, ys2, H, None, n=500, h=(20, 50))
    tree_round(L, 220, float(ys2[220]) + 40, 420, light=0.3)
    tree_round(L, w - 260, float(ys2[w - 260]) + 40, 380, light=0.3)
    s.meta["boats"] = [[600, H * 0.74], [1700, H * 0.80], [2500, H * 0.70]]
    sp = s.sprite("boat", 300, 300, anchor=(0.5, 0.86))
    boat(sp, 150, 258, 110)
    return s


def s3_autumn():
    s = Scene(FILM, "s3_autumn", seed=203)
    L = s.layer("sky", 0.0, opaque=True)
    sky(L, top=(0.80, 0.62, 0.52), horizon=(0.99, 0.88, 0.62), y_h=H * 0.65)
    clouds(L, 6, H * 0.06, H * 0.3, (0.86, 0.66, 0.56), rmin=80, rmax=200, density=0.4)
    L = s.layer("palace", 0.3)
    S = L.S
    L.wash(S.below_curve(np.full(W, H * 0.66, F32), 1), (0.86, 0.82, 0.72), density=0.8, edge=0.5, gran=0.5)
    # 兩側長牆
    great_wall(L, H * 0.66, 120, color=(0.74, 0.40, 0.32), x0=0, x1=W)
    palace(L, W * 0.5, H * 0.66, 520)
    L = s.layer("square", 0.6)
    S = L.S
    m = S.below_curve(np.full(W, H * 0.70, F32), 1)
    L.wash(m, (0.84, 0.80, 0.72), density=0.9, edge=0.6, gran=0.7)
    for k in range(12):  # 透視石板線
        x = W * 0.5 + (k - 5.5) * 220
        L.ink([(W * 0.5 + (k - 5.5) * 60, H * 0.70), (x * 1.0 + (k - 5.5) * 260, H)], width=1.2, dark=0.4, dry=0.5)
    for k in range(6):
        y = H * 0.70 + (H * 0.3) * (k / 6) ** 1.6
        L.ink([(0, y), (W, y)], width=1.1, dark=0.35, dry=0.5)
    L = s.layer("trees", 1.0)
    autumn = [(0.92, 0.56, 0.28), (0.86, 0.40, 0.24), (0.95, 0.72, 0.30)]
    big_tree(L, 260, H * 1.02, 900, autumn=autumn, shadow=(0.62, 0.30, 0.24), light=(0.98, 0.84, 0.50))
    big_tree(L, W - 240, H * 1.02, 820, autumn=autumn[::-1], shadow=(0.62, 0.30, 0.24), light=(0.98, 0.84, 0.50))
    return s


def _night_city(s, lights=True):
    L = s.layer("sky", 0.0, opaque=True)
    sky(L, top=(0.10, 0.12, 0.28), horizon=(0.34, 0.30, 0.46), y_h=H * 0.75, density=0.95)
    return L


def s4_fireworks():
    s = Scene(FILM, "s4_fireworks", seed=204)
    _night_city(s)
    L = s.layer("palace", 0.3)
    S = L.S
    L.wash(S.below_curve(np.full(W, H * 0.66, F32), 1), (0.40, 0.38, 0.46), density=0.9, edge=0.5, gran=0.5)
    great_wall(L, H * 0.66, 120, color=(0.40, 0.26, 0.30), x0=0, x1=W)
    wins = palace(L, W * 0.5, H * 0.66, 520, wall=(0.42, 0.22, 0.24), roof=(0.50, 0.42, 0.30))
    s.meta["lamps"] = [list(v) for v in wins]
    L = s.layer("crowd", 0.8)
    ys = ground(L, H * 0.86, 10, (0.24, 0.24, 0.32), cells=3, ink=1.0)
    for k in range(40):
        x = L.rng.uniform(0, W)
        figure(L, x, H + L.rng.uniform(-30, 30), L.rng.uniform(150, 220), robe=(0.20, 0.20, 0.28),
               skin=(0.30, 0.28, 0.34), arm=L.rng.uniform(0, 1))
    return s


def s5_dimming():
    s = Scene(FILM, "s5_dimming", seed=205, w=int(W * 1.2))
    w = s.w
    _night_city(s)
    L = s.layer("far", 0.2)
    mountains(L, H * 0.62, 120, (0.24, 0.24, 0.38), cells=3, density=0.8)
    L = s.layer("city", 0.5)
    ys = ground(L, H * 0.7, 40, (0.30, 0.30, 0.40), cells=4, ink=1.0)
    lamps = []
    rng = L.rng
    for row, (yoff, sc) in enumerate([(0, 0.7), (90, 0.85), (200, 1.0)]):
        for x in np.arange(60 + row * 50, w, 170 * sc):
            xi = int(min(w - 1, x))
            wins = house(L, x, float(ys[xi]) + yoff, 130 * sc, rng.uniform(80, 130) * sc,
                         roof=(0.30, 0.26, 0.34), wall=(0.42, 0.40, 0.48), win_light=True, windows=2)
            lamps += [list(v) for v in wins]
    s.meta["lamps"] = lamps
    return s


def s6_winter():
    s = Scene(FILM, "s6_winter", seed=206, w=int(W * 1.3))
    w = s.w
    L = s.layer("sky", 0.0, opaque=True)
    sky(L, top=(0.72, 0.74, 0.80), horizon=(0.92, 0.92, 0.92), y_h=H * 0.7)
    L = s.layer("far", 0.15)
    mountains(L, H * 0.56, 150, (0.80, 0.82, 0.88), cells=3, density=0.4, ink=0.6, snow=True)
    L = s.layer("field", 0.45)
    ys = snowfield(L, H * 0.64, 40)
    lamps = []
    for x in [420, 1300, 2100, 2700]:  # 彼此遠離的孤屋
        lamps += [list(v) for v in hut(L, x, float(ys[x]) + 20, 110, lit=(x == 1300))]
    for x in [700, 1650, 2400]:
        big_tree(L, x, float(ys[x]) + 30, 260, bare=True)
    s.meta["lamps"] = lamps
    L = s.layer("fg", 1.0)
    ys2 = snowfield(L, H * 0.9, 30, ink=1.8)
    for x in [180, w - 200]:
        big_tree(L, x, float(ys2[x]) + 60, 700, bare=True)
    return s


def s7_steppe():
    s = Scene(FILM, "s7_steppe", seed=207, w=int(W * 1.3))
    w = s.w
    L = s.layer("sky", 0.0, opaque=True)
    sky(L, top=(0.56, 0.62, 0.84), horizon=(0.99, 0.84, 0.62), y_h=H * 0.66,
        glow=(w * 0.7, H * 0.66, 300, (0.99, 0.78, 0.52)))
    clouds(L, 9, H * 0.08, H * 0.4, (0.80, 0.66, 0.70), rmin=80, rmax=220, density=0.4)
    L = s.layer("far", 0.15)
    mountains(L, H * 0.64, 110, (0.64, 0.62, 0.78), cells=4, density=0.55, ink=0.7)
    L = s.layer("steppe", 0.5)
    ys = steppe(L, H * 0.7)
    s.meta["ride_y"] = float(H * 0.84)
    for p in range(4):
        sp = s.sprite(f"rider_{p}", 600, 560, anchor=(0.5, 0.96))
        horse_rider(sp, 290, 535, 290, phase=p / 4)
    return s


def s8_spring2():
    s = Scene(FILM, "s8_spring2", seed=208)
    L = s.layer("sky", 0.0, opaque=True)
    sky(L, top=(0.64, 0.76, 0.92), horizon=(0.99, 0.95, 0.86), y_h=H * 0.6)
    clouds(L, 8, H * 0.06, H * 0.34, (0.82, 0.84, 0.92), rmin=60, rmax=160, density=0.3)
    L = s.layer("hills", 0.35)
    ys = ground(L, H * 0.64, 120, (0.72, 0.86, 0.54), cells=3, second=(0.62, 0.76, 0.48), ink=1.2)
    x = int(W * 0.62)
    s.meta["lamps"] = [list(tower(L, x, float(ys[x]) + 10, 60, 170))]
    L = s.layer("fg", 0.9)
    ys2 = ground(L, H * 0.92, 25, (0.60, 0.74, 0.42), cells=4, ink=2.0)
    field_strokes(L, ys2, H, None, n=500, h=(20, 50))
    blossom_tree(L, int(W * 0.24), float(ys2[int(W * 0.24)]) + 30, 640)
    return s


ALL = [s1_spring, s2_summer, s3_autumn, s4_fireworks, s5_dimming, s6_winter, s7_steppe, s8_spring2]
