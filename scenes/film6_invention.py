"""第六部《發明》— 民族發明學"""
import numpy as np
from kit import *

FILM = "film6"
ROBES = [(0.70, 0.34, 0.30), (0.30, 0.42, 0.62), (0.76, 0.62, 0.34), (0.40, 0.54, 0.40), (0.56, 0.38, 0.56), (0.80, 0.50, 0.36)]


def s1_cell():
    s = Scene(FILM, "s1_cell", seed=601)
    sky_layer(s, 'day', clouds_n=6)
    L, ys = ground_layer(s, 0.62, 20, (0.76, 0.80, 0.56), (0.66, 0.70, 0.50))
    rng = np.random.default_rng(6)
    cx, cy = W * 0.5, H * 0.8
    pts = [(cx + rng.normal(0, 380), cy + rng.normal(0, 90)) for _ in range(26)]
    villagers(L, sorted(pts, key=lambda p: p[1]), 150, rng)
    L = s.layer('membrane', 0.45)
    S = L.S
    a = np.linspace(0, 2 * np.pi, 120)
    ring = [(cx + np.cos(t) * 700 * (1 + 0.04 * np.sin(t * 5)), cy - 40 + np.sin(t) * 260) for t in a]
    m = S.poly(ring, rough=10, scale=60)
    edge = np.clip(m - lblur(m, 22), 0, 1) * 3
    L.wash(np.clip(edge, 0, 1), (0.40, 0.56, 0.72), density=0.9, edge=0.9, gran=0.5, bloom=3)
    L.wash(m, (0.70, 0.82, 0.90), density=0.25, edge=0.3, occlude=False)
    L.ink(ring, width=3, color=INK_BLUE, dark=0.7)
    t = s.tmap('membrane')
    yy, xx = np.mgrid[0:H, 0:W].astype(F32)
    t[:] = ((np.arctan2(yy - cy, xx - cx) + np.pi) / (2 * np.pi)) * 0.95
    return s


def s2_names():
    s = Scene(FILM, "s2_names", seed=602)
    sky_layer(s, 'dawn', clouds_n=6)
    L, ys = ground_layer(s, 0.8, 30, (0.72, 0.78, 0.52), (0.60, 0.66, 0.46))
    tips = big_tree(L, W * 0.5, gy(ys, W * 0.5) + 10, 760, seed_rng=np.random.default_rng(14))
    rng = np.random.default_rng(3)
    tags = []
    for k, (x, y) in enumerate(tips):
        for j in range(2):
            tx, ty = x + rng.uniform(-60, 60), y + rng.uniform(20, 120)
            L.ink([(tx, ty - 50), (tx, ty)], width=1.0, dark=0.6, smooth=0)
            col = ROBES[(k + j) % 6]
            L.wash(L.S.poly([(tx - 18, ty), (tx + 18, ty), (tx + 18, ty + 46), (tx - 18, ty + 46)], rough=0.5), col, density=0.8, edge=0.9)
            L.box(tx - 18, ty, tx + 18, ty + 46, width=1.0, dark=0.6)
            tags.append([tx, ty + 23])
    villagers(L, [(W * 0.3, gy(ys, W * 0.3) + 30), (W * 0.36, gy(ys, W * 0.36) + 50), (W * 0.64, gy(ys, W * 0.64) + 40), (W * 0.7, gy(ys, W * 0.7) + 25)], 230, rng)
    s.meta.update(tags=tags)
    fg_layer(s)
    return s


def s3_bubble():
    s = Scene(FILM, "s3_bubble", seed=603)
    sky_layer(s, 'day', clouds_n=8)
    far_layer(s, 0.6, 120, (0.72, 0.76, 0.88))
    L, ys = ground_layer(s, 0.78, 40, (0.72, 0.80, 0.52), (0.62, 0.70, 0.46))
    for x in [600, 820, 1050, 1300, 1550, 1750]:
        house(L, x, gy(ys, x) + 10, 150, 100)
    figure(L, W * 0.5, gy(ys, W * 0.5) + 160, 260, robe=(0.40, 0.42, 0.60), arm=1.0)
    s.meta.update(blow=[W * 0.5 + 40, gy(ys, W * 0.5) - 80])
    fg_layer(s)
    return s


def s4_crown():
    s = Scene(FILM, "s4_crown", seed=604)
    L = s.layer('hall', 0.0, opaque=True)
    S = L.S
    L.wash(np.ones((H, W), F32), (0.84, 0.76, 0.66), density=0.7, edge=0, gran=0.4)
    for x in np.arange(160, W, 400):
        L.wash(S.poly([(x - 50, H), (x - 40, 0), (x + 40, 0), (x + 50, H)], rough=1), (0.90, 0.86, 0.78), density=0.6, edge=0.8)
        L.ink([(x - 50, H), (x - 40, 0)], width=1.4, smooth=0); L.ink([(x + 50, H), (x + 40, 0)], width=1.4, smooth=0)
    L = s.layer('throne', 0.4)
    S = L.S
    cx, yg = W * 0.5, H * 0.86
    L.wash(S.below_curve(np.full(W, yg, F32), 1), (0.56, 0.24, 0.22), density=0.85, edge=0.6)
    th = [(cx - 200, yg), (cx - 200, yg - 520), (cx - 140, yg - 640), (cx + 140, yg - 640), (cx + 200, yg - 520), (cx + 200, yg)]
    L.wash(S.poly(th, rough=1), (0.80, 0.62, 0.30), density=0.9, edge=0.8, gran=0.6)
    L.wash(S.poly([(cx - 150, yg - 260), (cx + 150, yg - 260), (cx + 150, yg - 520), (cx - 150, yg - 520)], rough=1), (0.62, 0.20, 0.20), density=0.9)
    L.ink(th, width=2.4, smooth=0)
    villagers(L, [(cx + dx, yg + 40 + abs(dx) * 0.04) for dx in (-700, -560, -420, 420, 560, 700)], 260, np.random.default_rng(2))
    L = s.layer('crown', 0.4)
    S = L.S
    cr = [(cx - 110, yg - 690), (cx - 120, yg - 800), (cx - 60, yg - 740), (cx, yg - 830), (cx + 60, yg - 740), (cx + 120, yg - 800), (cx + 110, yg - 690)]
    L.wash(S.poly(cr, rough=0.8), (0.95, 0.76, 0.30), density=1.0, edge=0.9)
    L.ink(cr + [cr[0]], width=2.4, smooth=0)
    for k in (-60, 0, 60):
        L.wash(S.ellipse(cx + k, yg - 715, 12, 12, rough=0.3), (0.70, 0.16, 0.16), density=1.0)
    t = s.tmap('crown')
    t[:] = fbm(H, W, 6, np.random.default_rng(2), 4) * 0.9 + 0.05
    s.meta.update(seat=[cx, yg - 300])
    return s


def s5_delta():
    s = Scene(FILM, "s5_delta", seed=605)
    L = s.layer('land', 0.0, opaque=True)
    S = L.S
    L.wash(np.ones((H, W), F32), (0.86, 0.84, 0.66), density=0.8, edge=0, gran=0.6)
    rng = np.random.default_rng(5)
    cols = [(0.40, 0.60, 0.80), (0.50, 0.70, 0.56), (0.80, 0.56, 0.44), (0.66, 0.50, 0.70), (0.84, 0.72, 0.40), (0.40, 0.66, 0.70)]
    chans = []

    def river(x, y, a, w, d, k):
        pts = [(x, y)]
        for i in range(10):
            a += rng.normal(0, 0.12)
            x += np.cos(a) * 30; y += np.sin(a) * 30
            pts.append((x, y))
        poly = ribbon(pts, w, w * 0.8)
        c = cols[k % len(cols)] if d < 3 else (0.48, 0.62, 0.78)
        L.wash(S.poly(poly, rough=2, feather=1), c, density=0.85, edge=0.9, gran=0.5)
        L.ink(poly[:len(pts)], width=1.2, dark=0.6); L.ink(poly[len(pts):], width=1.2, dark=0.6)
        chans.append(pts)
        if d > 0:
            for j, da in enumerate((-0.45, 0.45)):
                river(x, y, a + da, w * 0.72, d - 1, k * 2 + j)

    river(W * 0.55, -40, np.pi / 2, 110, 4, 0)
    s.meta.update(chans=[[list(map(float, p)) for p in c] for c in chans])
    L = s.layer('reader', 0.5)
    yg = H * 0.97
    figure(L, W * 0.16, yg, 380, robe=(0.36, 0.30, 0.40), arm=0.6)
    book(L, W * 0.16 + 70, yg - 230, 120, 60, open_=True, lines=3)
    for k in range(4):
        figure(L, W * 0.24 + k * 90, yg + 10, 200, robe=ROBES[k], arm=0.0)
    s.meta.update(lamp=[W * 0.16, yg - 450])
    return s


def s6_bear():
    s = Scene(FILM, "s6_bear", seed=606, w=int(W * 1.2))
    sky_layer(s, 'storm', clouds_n=6)
    L, ys = ground_layer(s, 0.8, 30, (0.68, 0.70, 0.54), (0.56, 0.58, 0.48))
    lamps = []
    for x in np.arange(150, s.w, 180):
        lamps += [list(v) for v in house(L, x, gy(ys, x) + 10, 120 + (x % 3) * 10, 90, roof=ROBES[int(x) % 6], windows=1, win_light=True)]
    s.meta.update(lamps=lamps)
    L = s.layer('bear', 0.15)
    S = L.S
    cx, cy = s.w * 0.55, H * 0.36
    m = S.blob(cx, cy, 520, n=12, spread=0.8, squash=0.6, rough=40)
    for dx, dy, r in [(-460, -220, 170), (-300, -330, 110), (-620, -320, 100), (380, 180, 220), (-120, 230, 230)]:
        m = np.maximum(m, S.blob(cx + dx, cy + dy, r, n=6, rough=20))
    L.wash(m, (0.36, 0.34, 0.42), density=0.9, edge=0.8, gran=0.5, bloom=6)
    L.wash(m * S.vgrad(cy - 400, cy + 400), (0.22, 0.20, 0.28), density=0.6, edge=0, bloom=20, occlude=False)
    L.lift(S.ellipse(cx - 480, cy - 250, 22, 16, rough=1), 0.9)
    canopy_contour_ink(L, m, width=2, frac=0.6)
    s.meta.update(bear=[cx, cy])
    return s


def s7_triptych():
    s = Scene(FILM, "s7_triptych", seed=607)
    L = s.layer('paper', 0.0, opaque=True)
    L.wash(np.ones((H, W), F32), (0.97, 0.94, 0.88), density=0.3, edge=0)
    L = s.layer('panels', 0.3)
    S = L.S
    pw = W / 3
    for i in range(3):
        x0, x1 = i * pw + 50, (i + 1) * pw - 50
        L.box(x0, 170, x1, H - 230, width=2.2, dark=0.8)
        yg = H - 330
        L.wash(S.poly([(x0 + 4, yg), (x1 - 4, yg), (x1 - 4, H - 234), (x0 + 4, H - 234)], rough=1), (0.62, 0.50, 0.38), density=0.85, edge=0.6)
        cx = (x0 + x1) / 2
        if i == 0:   # 土壤裏長出的樹
            big_tree(L, cx, yg + 4, 560, seed_rng=np.random.default_rng(9))
            roots(L, cx, yg + 10, 160, np.random.default_rng(4), width=4, n_main=5)
        elif i == 1:  # 斧頭砍下的木材
            for k in range(3):
                y = yg - 30 - k * 46
                L.wash(S.poly([(cx - 220 + k * 20, y), (cx + 200 - k * 20, y), (cx + 200 - k * 20, y + 44), (cx - 220 + k * 20, y + 44)], rough=1),
                       (0.70, 0.52, 0.36), density=0.9, edge=0.8)
                L.wash(S.ellipse(cx + 200 - k * 20, y + 22, 18, 22, rough=0.5), (0.90, 0.76, 0.56), density=0.8, edge=0.9)
                L.box(cx - 220 + k * 20, y, cx + 200 - k * 20, y + 44, width=1.4)
            L.ink([(cx - 240, yg - 260), (cx - 100, yg - 160)], width=6, color=INK_BROWN)
            L.wash(S.poly([(cx - 110, yg - 190), (cx - 60, yg - 210), (cx - 70, yg - 140), (cx - 120, yg - 150)], rough=0.6), (0.56, 0.58, 0.64), density=0.95)
            L.ink([(cx - 300, yg + 2), (cx - 250, yg - 40), (cx - 200, yg + 2)], width=3, color=INK_BROWN)
        else:         # 森林上空漂浮的雲
            m = S.blob(cx, 420, 230, n=9, spread=1.2, squash=0.5, rough=20)
            L.wash(m, (0.80, 0.82, 0.90), density=0.6, edge=0.9)
            canopy_contour_ink(L, m, width=1.6, frac=0.6)
            for k in range(5):
                tree_pine(L, cx - 240 + k * 120, yg + 4, 160 + (k % 2) * 50, color=(0.40, 0.52, 0.44))
    return s


def s8_seeds():
    s = Scene(FILM, "s8_seeds", seed=608)
    sky_layer(s, 'day', clouds_n=7)
    L, ys = ground_layer(s, 0.6, 20, (0.72, 0.68, 0.50), (0.62, 0.56, 0.44))
    rng = np.random.default_rng(8)
    for _ in range(160):   # 未發芽的種子
        x, y = rng.uniform(0, W), rng.uniform(H * 0.65, H)
        L.wash(L.S.ellipse(x, y, 6, 4, ang=rng.uniform(0, 180), rough=0.3), (0.50, 0.38, 0.28), density=0.9)
    for k in range(6):     # 倒在草裏的褪色旗
        x, y = rng.uniform(100, W - 100), rng.uniform(H * 0.7, H * 0.95)
        L.ink([(x, y), (x + 140, y - 30)], width=2.2, color=INK_BROWN)
        L.wash(L.S.poly([(x + 140, y - 30), (x + 100, y - 10), (x + 120, y + 30), (x + 165, y + 10)], rough=0.8), ROBES[k], density=0.35, edge=0.6)
    L = s.layer('sprouts', 0.45)
    t = s.tmap('sprouts')
    for x, y, hh in [(W * 0.3, H * 0.8, 220), (W * 0.62, H * 0.86, 280), (W * 0.84, H * 0.74, 160)]:
        seedling(L, x, y, hh, tmap=t, t0=rng.uniform(0, 0.3))
    fg_layer(s, 0.97, grass=200)
    return s


def s9_boomerang():
    s = Scene(FILM, "s9_boomerang", seed=609, w=int(W * 1.2))
    sky_layer(s, 'day', clouds_n=8)
    far_layer(s, 0.6, 110, (0.70, 0.74, 0.86))
    L, ys = ground_layer(s, 0.72, 20, (0.72, 0.80, 0.52), (0.62, 0.70, 0.46))
    water(L, H * 0.8, H * 0.88, (0.56, 0.70, 0.84))
    sp = s.sprite('thrower_0', 260, 340, anchor=(0.5, 0.97)); figure(sp, 130, 330, 300, robe=(0.40, 0.42, 0.60), arm=1.0, lean=-0.2)
    sp = s.sprite('thrower_1', 260, 340, anchor=(0.5, 0.97)); figure(sp, 130, 330, 300, robe=(0.40, 0.42, 0.60), arm=0.2, lean=0.5)
    sp = s.sprite('boomerang', 260, 260, anchor=(0.5, 0.5)); boomerang(sp, 140, 130, 100, 0.4)
    s.meta.update(thrower=[460, gy(ys, 460) + 20], far=[s.w * 0.85, H * 0.42])
    fg_layer(s, 0.96)
    return s


def s10_overlay():
    s = Scene(FILM, "s10_overlay", seed=610)
    L = s.layer('map', 0.0, opaque=True)
    landm, regions = painted_map(L, n=16, seed=21, single=(0.92, 0.88, 0.76), border_ink=0)
    rng = np.random.default_rng(7)
    L = s.layer('gaps', 0.0)
    for _ in range(40):   # 縫隙中長出的小花
        x, y = rng.uniform(W * 0.25, W * 0.75), rng.uniform(H * 0.25, H * 0.75)
        L.wash(L.S.ellipse(x, y, 9, 9, rough=0.3), ROBES[int(rng.integers(6))], density=0.9, edge=0.9)
    for name, col, cx in [('red', (0.86, 0.46, 0.40), W * 0.46), ('blue', (0.42, 0.56, 0.84), W * 0.54)]:
        L = s.layer(name, 0.0)
        m = L.S.blob(cx, H * 0.5, 480, n=12, spread=0.9, squash=0.75, rough=36)
        L.wash(m, col, density=0.5, edge=0.95, gran=0.4)
        canopy_contour_ink(L, m, width=2.4, frac=1.0, dark=0.75)
    return s


def s11_furrow():
    s = Scene(FILM, "s11_furrow", seed=611)
    sky_layer(s, 'grey', clouds_n=6)
    L, ys = ground_layer(s, 0.58, 15, (0.74, 0.74, 0.54), (0.64, 0.62, 0.48))
    for x0, col, side in [(W * 0.22, ROBES[0], -1), (W * 0.78, ROBES[1], 1)]:
        palisade(L, x0 - 260, x0 + 260, H * 0.7, 120 if side > 0 else 60)
        L.ink([(x0, H * 0.66), (x0, H * 0.4)], width=3, color=INK_BROWN, smooth=0)
        L.wash(L.S.poly([(x0, H * 0.4), (x0 + 120, H * 0.43), (x0, H * 0.47)], rough=0.6), col, density=0.9, edge=0.9)
        villagers(L, [(x0 - 120 + k * 80, H * 0.86 + (k % 2) * 20) for k in range(4)], 200, np.random.default_rng(int(x0)))
    L = s.layer('furrow', 0.45)
    t = s.tmap('furrow')
    pts = [(W * 0.5 + 30 * np.sin(k * 0.7), H * 0.6 + k * (H * 0.4 / 14)) for k in range(15)]
    L.wash(L.S.poly(ribbon(pts, 26, 70), rough=3), (0.46, 0.16, 0.14), density=0.95, edge=0.9, gran=0.6)
    L.ink(pts, width=3, dark=0.8)
    yy = np.arange(H, dtype=F32)[:, None]
    t[:] = np.clip((yy - H * 0.58) / (H * 0.42), 0, 1) * np.ones((1, W), F32)
    return s


def s12_butterfly():
    s = Scene(FILM, "s12_butterfly", seed=612)
    sky_layer(s, 'dawn', clouds_n=6)
    L, ys = ground_layer(s, 0.86, 20, (0.66, 0.76, 0.48), (0.56, 0.64, 0.42))
    S = L.S
    # 葉子與毛蟲
    leaf = [(W * 0.12, H * 0.72), (W * 0.3, H * 0.6), (W * 0.42, H * 0.66), (W * 0.3, H * 0.76)]
    L.wash(S.poly(leaf, rough=2), (0.50, 0.70, 0.36), density=0.9, edge=0.9)
    L.ink(leaf + [leaf[0]], width=1.8)
    caterpillar(L, W * 0.32, H * 0.67, 170)
    # 博物館玻璃櫃裏的種子標本
    bx = W * 0.8
    L.wash(S.poly([(bx - 200, H * 0.86), (bx - 200, H * 0.62), (bx + 200, H * 0.62), (bx + 200, H * 0.86)], rough=0.6), (0.86, 0.92, 0.96), density=0.4, edge=0.9)
    L.box(bx - 200, H * 0.62, bx + 200, H * 0.86, width=2)
    L.wash(S.ellipse(bx, H * 0.76, 40, 24, rough=0.5), (0.52, 0.40, 0.30), density=0.95, edge=0.9)
    L.ink([(bx - 60, H * 0.72), (bx + 60, H * 0.81)], width=1.6, color=(0.6, 0.2, 0.16), smooth=0)
    L.wash(S.poly([(bx - 60, H * 0.84), (bx + 60, H * 0.84), (bx + 60, H * 0.82), (bx - 60, H * 0.82)], rough=0.3), (0.96, 0.94, 0.88), density=0.5)
    for k, o in enumerate([0.15, 0.6, 1.0]):
        sp = s.sprite(f'bfly_{k}', 340, 300, anchor=(0.5, 0.5))
        butterfly(sp, 170, 160, 130, open_=o)
    s.meta.update(cat=[W * 0.32, H * 0.6], case=[bx, H * 0.62])
    return s


def s13_towns():
    s = Scene(FILM, "s13_towns", seed=613, w=int(W * 1.35))
    sky_layer(s, 'day', clouds_n=12, glow=(W * 0.6, H * 0.5, 280, (0.99, 0.90, 0.70)))
    far_layer(s, 0.5, 200, (0.66, 0.74, 0.88), snow=True)
    L, ys = ground_layer(s, 0.6, 40, (0.72, 0.82, 0.52), (0.62, 0.72, 0.46), cells=6)
    water(L, H * 0.74, H * 0.8, (0.56, 0.72, 0.86))
    lamps = []
    for i, x in enumerate(np.arange(220, s.w, 420)):
        yg = gy(ys, x) + 40 + (i % 2) * 60
        great_wall(L, yg, 50, color=(0.78, 0.72, 0.64), x0=x - 140, x1=x + 140)
        lamps += [list(v) for v in house(L, x, yg - 50, 150, 90, roof=ROBES[i % 6], windows=1)]
        if i % 2:
            tower(L, x + 110, yg - 40, 40, 120)
        L.ink([(x - 120, yg - 120), (x - 120, yg - 230)], width=2, color=INK_BROWN, smooth=0)
        L.wash(L.S.poly([(x - 120, yg - 230), (x - 50, yg - 215), (x - 120, yg - 200)], rough=0.4), ROBES[(i + 2) % 6], density=0.9)
    s.meta.update(lamps=lamps)
    fg_layer(s, 0.95)
    return s


ALL = [s1_cell, s2_names, s3_bubble, s4_crown, s5_delta, s6_bear, s7_triptych, s8_seeds, s9_boomerang, s10_overlay, s11_furrow,
       s12_butterfly, s13_towns]
