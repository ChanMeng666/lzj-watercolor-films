"""第一部《根》— 秩序是長出來的"""
import numpy as np
from scene import Scene, W, H
from wc import blur, F32
from motifs import *

FILM = "film1"


def s1_seed():
    s = Scene(FILM, "s1_seed", seed=101)
    L = s.layer("sky", 0.0, opaque=True)
    sky(L, top=(0.62, 0.66, 0.84), horizon=(0.98, 0.86, 0.66), y_h=H * 0.7, glow=(W * 0.62, H * 0.62, 260, (0.98, 0.80, 0.55)))
    clouds(L, 9, H * 0.12, H * 0.45, (0.80, 0.70, 0.78), rmin=60, rmax=150, density=0.4)
    L = s.layer("mtn", 0.15)
    mountains(L, H * 0.66, 170, (0.70, 0.70, 0.84), cells=3, sharp=0.25, density=0.6, ink=1.0)
    L = s.layer("hills", 0.4)
    ys = ground(L, H * 0.74, 60, (0.78, 0.82, 0.58), cells=4, second=(0.66, 0.72, 0.50), ink=1.3)
    for x in [380, 1650, 1980]:
        tree_round(L, x, ys[x] + 6, 120, ink=True)
    L = s.layer("fg", 0.9)
    ys2 = ground(L, H * 0.86, 30, (0.62, 0.70, 0.42), cells=3, second=(0.50, 0.52, 0.36), ink=2.0)
    field_strokes(L, ys2, H, None, n=500, h=(14, 40))
    s.meta["land"] = [W * 0.5, float(ys2[W // 2]) + 30]
    sp = s.sprite("seed", 90, 70, anchor=(0.5, 0.5))
    m = sp.S.ellipse(45, 35, 22, 14, ang=-20, rough=1)
    sp.wash(m, (0.62, 0.45, 0.30), density=1.0, edge=0.8)
    sp.wash(m * sp.S.vgrad(25, 50), (0.45, 0.32, 0.25), density=0.6, edge=0.3)
    sp.ink([(25, 38), (40, 24), (62, 28), (68, 40), (50, 49), (27, 44), (25, 38)], width=2.0, dark=0.85)
    sp.ink([(32, 37), (60, 34)], width=1.0, dark=0.5)
    return s


def s2_roots():
    s = Scene(FILM, "s2_roots", seed=102)
    surf = H * 0.40
    L = s.layer("sky", 0.0, opaque=True)
    sky(L, top=(0.66, 0.76, 0.90), horizon=(0.97, 0.92, 0.78), y_h=surf)
    mountains(L, surf + 4, 90, (0.76, 0.78, 0.86), cells=4, density=0.5)
    L = s.layer("soil", 0.2)
    S = L.S
    ys = surf + 6 * noise1d(W, 6, L.rng)
    m = S.below_curve(ys, rough=2)
    L.wash(m, (0.86, 0.76, 0.58), density=0.9, edge=0.6, gran=0.6)
    for i, (y0, c) in enumerate([(H * 0.55, (0.78, 0.64, 0.48)), (H * 0.72, (0.66, 0.54, 0.44)), (H * 0.88, (0.52, 0.44, 0.40))]):
        yy = y0 + 30 * noise1d(W, 3 + i, L.rng)
        L.wash(S.below_curve(yy, rough=6), c, density=0.75, edge=0.7, gran=0.7, bloom=6)
    # 石塊
    for _ in range(26):
        x, y = L.rng.uniform(0, W), L.rng.uniform(surf + 80, H - 20)
        r = L.rng.uniform(10, 34)
        mm = S.ellipse(x, y, r, r * 0.65, ang=L.rng.uniform(0, 180), rough=3)
        L.wash(mm, (0.62, 0.60, 0.62), density=0.8, edge=0.8)
        L.ink([(x - r, y), (x - r * 0.3, y - r * 0.6), (x + r * 0.7, y - r * 0.4), (x + r, y + 2)], width=1.4, dark=0.6, dry=0.4)
    # 草皮
    L.wash(S.below_curve(ys - 6, 1) * (1 - S.below_curve(ys + 26, 4)), (0.55, 0.68, 0.38), density=0.9, edge=0.8)
    ridge_ink(L, ys, 1.8, gap=0.1)
    # 根系 (帶生長時間圖)
    L = s.layer("roots", 0.2)
    t = s.tmap("roots")
    roots(L, W * 0.5, surf + 14, H * 0.62, np.random.default_rng(7), tmap=t, width=9, n_main=6)
    below = L.S.below_curve(np.full(W, surf + 4, F32), rough=0)
    L.clip(below)
    t[below < 0.5] = 9.0
    # 小樹 (帶生長時間圖)
    L = s.layer("tree", 0.2)
    t2 = s.tmap("tree")
    big_tree(L, W * 0.5, surf + 14, 330, seed_rng=np.random.default_rng(5), tmap=t2)
    s.meta["origin"] = [W * 0.5, surf + 14]
    return s


def s3_village():
    s = Scene(FILM, "s3_village", seed=103)
    L = s.layer("sky", 0.0, opaque=True)
    sky(L, top=(0.46, 0.50, 0.72), horizon=(0.99, 0.78, 0.55), y_h=H * 0.72, glow=(W * 0.3, H * 0.7, 300, (0.99, 0.72, 0.45)))
    clouds(L, 7, H * 0.1, H * 0.4, (0.72, 0.56, 0.66), rmin=70, rmax=170, density=0.5)
    L = s.layer("far", 0.15)
    mountains(L, H * 0.68, 140, (0.58, 0.56, 0.74), cells=3, density=0.65, ink=0.9)
    L = s.layer("mid", 0.45)
    ys = ground(L, H * 0.78, 40, (0.66, 0.70, 0.50), cells=3, second=(0.52, 0.56, 0.46), ink=1.4)
    lamps, chim = [], []
    big_tree(L, W * 0.2, ys[int(W * 0.2)] + 8, 640, seed_rng=np.random.default_rng(31),
             green=(0.48, 0.58, 0.36), shadow=(0.30, 0.34, 0.42))
    for x, w, h, roof in [(790, 190, 130, (0.70, 0.40, 0.33)), (1180, 230, 150, (0.62, 0.38, 0.36)),
                          (1460, 170, 120, (0.74, 0.48, 0.36)), (1720, 240, 160, (0.60, 0.40, 0.38)),
                          (2020, 200, 130, (0.70, 0.44, 0.34)), (975, 140, 96, (0.66, 0.42, 0.36))]:
        yg = float(ys[x]) + 10
        wins = house(L, x, yg, w, h, roof=roof, wall=(0.90, 0.82, 0.70), windows=2)
        lamps += [[a, b, c] for a, b, c in wins]
        chim.append([x + w * 0.29, yg - h - h * 0.7 * 0.95])
    s.meta["lamps"] = lamps
    s.meta["smoke"] = chim
    L = s.layer("fg", 0.95)
    ys2 = ground(L, H * 0.93, 26, (0.48, 0.54, 0.38), cells=4, ink=2.0)
    field_strokes(L, ys2, H, None, n=400, h=(20, 50))
    # 籬笆
    for x in np.arange(60, W, 110):
        y = float(ys2[int(x)])
        L.ink([(x, y + 10), (x + 2, y - 70)], width=5, color=INK_BROWN, dark=0.85)
    L.ink([(40, ys2[40] - 50), (W, ys2[W - 1] - 48)], width=3.5, color=INK_BROWN, dark=0.8)
    L.ink([(40, ys2[40] - 20), (W, ys2[W - 1] - 22)], width=3.0, color=INK_BROWN, dark=0.8)
    return s


def s4_dance():
    s = Scene(FILM, "s4_dance", seed=104)
    L = s.layer("sky", 0.0, opaque=True)
    sky(L, top=(0.30, 0.32, 0.55), horizon=(0.86, 0.62, 0.55), y_h=H * 0.62)
    L = s.layer("back", 0.25)
    ys = ground(L, H * 0.56, 30, (0.42, 0.44, 0.48), cells=3, ink=1.0)
    lamps = []
    for x, w, h in [(260, 220, 150), (620, 260, 170), (1640, 250, 160), (2000, 230, 150)]:
        wins = house(L, x, float(ys[x]) + 6, w, h, roof=(0.45, 0.33, 0.36), wall=(0.62, 0.58, 0.60), win_light=True)
        lamps += [[a, b, c] for a, b, c in wins]
    big_tree(L, W * 0.52, float(ys[int(W * 0.52)]) + 8, 520, seed_rng=np.random.default_rng(31),
             green=(0.32, 0.38, 0.36), shadow=(0.22, 0.24, 0.34))
    s.meta["lamps"] = lamps
    L = s.layer("green", 0.5)
    S = L.S
    m = S.below_curve(np.full(W, H * 0.58, F32), rough=2)
    L.wash(m, (0.50, 0.55, 0.42), density=0.9, edge=0.4)
    L.wash(S.ellipse(W * 0.5, H * 0.78, 700, 170, rough=8), (0.86, 0.66, 0.40), density=0.45, edge=0.5, bloom=30)
    # 篝火 (柴堆)
    cx, cy = W * 0.5, H * 0.78
    for k in range(7):
        a = k / 7 * np.pi
        L.ink([(cx - np.cos(a) * 50, cy + 10), (cx + np.cos(a) * 10, cy - 50)], width=6, color=INK_BROWN, dark=0.9)
    s.meta["fire"] = [cx, cy - 30]
    s.meta["ring"] = [cx, cy, 520, 130]
    robes = [(0.70, 0.34, 0.30), (0.30, 0.42, 0.62), (0.76, 0.62, 0.34), (0.40, 0.54, 0.40), (0.56, 0.38, 0.56),
             (0.80, 0.50, 0.36)]
    for i, c in enumerate(robes):
        for p in range(3):
            sp = s.sprite(f"dancer{i}_{p}", 150, 260, anchor=(0.5, 0.97))
            figure(sp, 75, 252, 230, robe=c, pose=(p - 1) * 0.9, arm=0.75 + 0.2 * (p == 1), legs=(p - 1) * 0.8,
                   lean=(p - 1) * 0.1)
    return s


def s5_growth():
    s = Scene(FILM, "s5_growth", seed=105, w=int(W * 1.5))
    w = s.w
    L = s.layer("sky", 0.0, opaque=True)
    sky(L, top=(0.58, 0.70, 0.90), horizon=(0.98, 0.94, 0.82), y_h=H * 0.62)
    clouds(L, 14, H * 0.08, H * 0.38, (0.78, 0.80, 0.88), rmin=60, rmax=180, density=0.35)
    L = s.layer("far", 0.2)
    mountains(L, H * 0.56, 220, (0.66, 0.72, 0.86), cells=4, sharp=0.35, density=0.55, ink=0.8, snow=True)
    L = s.layer("mid", 0.5)
    ys = ground(L, H * 0.66, 90, (0.70, 0.78, 0.52), cells=5, second=(0.60, 0.66, 0.46), ink=1.2)
    water(L, H * 0.80, H * 0.86, (0.62, 0.74, 0.86))
    castle(L, 700, float(ys[700]) + 8, 150)
    church(L, 1800, float(ys[1800]) + 6, 150)
    for x in [1500, 1620, 2050, 2200, 2400, 2560]:
        house(L, x, float(ys[x]) + 6, 120, 85, roof=(0.72, 0.42, 0.34))
    for x in [300, 420, 1100, 1250, 2800, 3000, 3200]:
        tree_round(L, x, float(ys[x]) + 6, 180)
    big_tree(L, 3050 - 200, float(ys[2850]) + 8, 520, seed_rng=np.random.default_rng(31))
    L = s.layer("fg", 1.0)
    ys2 = ground(L, H * 0.92, 40, (0.56, 0.62, 0.40), cells=6, ink=2.2)
    field_strokes(L, ys2, H, None, n=700, h=(20, 50))
    for x in [200, 1300, 2600]:
        tree_round(L, x, float(ys2[x]) + 30, 340, light=0.4)
    s.meta["boats"] = [[900, H * 0.835], [2300, H * 0.84]]
    sp = s.sprite("boat", 260, 260, anchor=(0.5, 0.86))
    boat(sp, 130, 220, 100)
    return s


def s6_harvester():
    s = Scene(FILM, "s6_harvester", seed=106)
    L = s.layer("sky", 0.0, opaque=True)
    sky(L, top=(0.64, 0.66, 0.74), horizon=(0.94, 0.88, 0.76), y_h=H * 0.6)
    clouds(L, 8, H * 0.1, H * 0.4, (0.66, 0.66, 0.72), rmin=80, rmax=200, density=0.5)
    L = s.layer("wall", 0.2)
    great_wall(L, H * 0.62, 300, color=(0.60, 0.60, 0.64))
    L.wash(L.S.poly([(W * 0.44, H * 0.62), (W * 0.44, H * 0.62 - 380), (W * 0.56, H * 0.62 - 380), (W * 0.56, H * 0.62)], rough=2),
           (0.52, 0.52, 0.58), density=0.9, edge=0.7)
    cn_roof(L, W * 0.5, H * 0.62 - 380, W * 0.16, 90, color=(0.40, 0.40, 0.46))
    L.wash(L.S.ellipse(W * 0.5, H * 0.62 - 60, 70, 110, rough=1), (0.25, 0.24, 0.30), density=0.95)
    L = s.layer("stubble", 0.55)
    S = L.S
    ys = ground(L, H * 0.62, 10, (0.86, 0.76, 0.52), cells=3, ink=1.0)
    for _ in range(1400):
        x = L.rng.uniform(0, W)
        y = L.rng.uniform(ys[int(x)] + 10, H)
        k = (y - H * 0.62) / (H * 0.38)
        L.ink([(x, y), (x + L.rng.uniform(-2, 2), y - 6 - 10 * k)], width=1 + 1.5 * k, color=INK_BROWN, dark=0.5, dry=0.3)
    L = s.layer("wheat", 0.55)
    t = s.tmap("wheat")
    S = L.S
    m = S.below_curve(np.full(W, H * 0.60, F32) + 14 * noise1d(W, 8, L.rng), rough=4)
    L.wash(m, (0.94, 0.80, 0.42), density=0.95, edge=0.7, gran=0.5)
    L.wash(m * S.vgrad(H * 0.6, H), (0.86, 0.62, 0.34), density=0.6, edge=0, bloom=20)
    field_strokes(L, np.full(W, H * 0.6, F32), H, None, n=2200, h=(24, 70), ink_col=(0.45, 0.32, 0.18))
    xs = np.arange(W, dtype=F32)[None, :] / W
    t[:] = np.clip(xs + 0.06 * np.random.default_rng(3).random((H, W)), 0, 1)
    s.meta["wall_y"] = H * 0.62
    return s


def s7_stalled():
    s = Scene(FILM, "s7_stalled", seed=107)
    L = s.layer("sky", 0.0, opaque=True)
    sky(L, top=(0.58, 0.60, 0.66), horizon=(0.90, 0.86, 0.80), y_h=H * 0.7)
    L = s.layer("clouds", 0.05)
    clouds(L, 16, H * 0.05, H * 0.5, (0.56, 0.56, 0.62), rmin=80, rmax=220, density=0.55, lift=False)
    L = s.layer("wall", 0.2)
    great_wall(L, H * 0.7, 160, color=(0.62, 0.62, 0.66))
    L = s.layer("land", 0.5)
    ys = ground(L, H * 0.72, 20, (0.70, 0.68, 0.56), cells=3, ink=1.2)
    big_tree(L, W * 0.5, float(ys[W // 2]) + 10, 760, seed_rng=np.random.default_rng(31),
             green=(0.50, 0.56, 0.40), shadow=(0.34, 0.36, 0.40))
    s.meta["mark_y"] = float(ys[W // 2]) - 760
    return s


def s8_night():
    s = Scene(FILM, "s8_night", seed=108)
    L = s.layer("sky", 0.0, opaque=True)
    sky(L, top=(0.16, 0.18, 0.36), horizon=(0.44, 0.44, 0.62), y_h=H * 0.85, density=0.95)
    moon(L, W * 0.76, H * 0.22, 70)
    L = s.layer("hills", 0.2)
    mountains(L, H * 0.78, 120, (0.30, 0.30, 0.44), cells=3, density=0.8, ink=0.8)
    L = s.layer("tree", 0.5)
    ys = ground(L, H * 0.86, 30, (0.26, 0.28, 0.36), cells=3, ink=1.4)
    big_tree(L, W * 0.4, float(ys[int(W * 0.4)]) + 10, 820, seed_rng=np.random.default_rng(31),
             green=(0.24, 0.30, 0.36), shadow=(0.16, 0.18, 0.28))
    s.meta["stars_seed"] = 8
    return s


ALL = [s1_seed, s2_roots, s3_village, s4_dance, s5_growth, s6_harvester, s7_stalled, s8_night]
