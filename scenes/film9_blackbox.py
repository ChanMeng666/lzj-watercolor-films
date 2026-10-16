"""第九部《黑匣子》— 三代文明、內亞海洋、種子庫"""
import numpy as np
from kit import *

FILM = "film9"
ROBES = [(0.70, 0.34, 0.30), (0.30, 0.42, 0.62), (0.76, 0.62, 0.34), (0.40, 0.54, 0.40), (0.56, 0.38, 0.56), (0.80, 0.50, 0.36)]


def s1_ignite():
    s = Scene(FILM, "s1_ignite", seed=901, w=int(W * 1.3))
    sky_layer(s, 'dusk', clouds_n=6, glow=(W * 0.3, H * 0.62, 300, (0.99, 0.74, 0.46)))
    far_layer(s, 0.62, 80, (0.70, 0.62, 0.70))
    L, ys = ground_layer(s, 0.7, 20, (0.86, 0.76, 0.56), (0.76, 0.64, 0.48))
    ziggurat(L, 520, gy(ys, 520) + 30, 300)
    chain = [[520, gy(ys, 520) - 190]]
    for k, x in enumerate(np.arange(1000, s.w, 360)):
        y = gy(ys, x) + 10 - k * 4
        if k % 3 == 0:
            temple(L, x, y, 70)
        elif k % 3 == 1:
            pyramid(L, x, y, 70)
        else:
            tower(L, x, y, 40, 120)
        chain.append([float(x), y - 100])
    s.meta.update(chain=chain)
    return s


def s2_wave():
    s = Scene(FILM, "s2_wave", seed=902)
    sky_layer(s, 'storm', clouds_n=12)
    L, ys = ground_layer(s, 0.76, 20, (0.82, 0.72, 0.54), (0.70, 0.60, 0.46))
    ziggurat(L, W * 0.62, gy(ys, W * 0.62) + 20, 340)
    for k in range(10):   # 泥板滑入洪水
        x = W * 0.7 + k * 40
        L.wash(L.S.poly([(x, H * 0.86), (x + 30, H * 0.85), (x + 32, H * 0.9), (x + 2, H * 0.91)], rough=0.5), (0.70, 0.56, 0.40), density=0.9)
    L = s.layer('wave', 0.5)
    S = L.S
    xs = np.arange(W, dtype=F32)
    crest = H * 0.4 + 180 * np.sin(xs / 300) * 0.3 + 60 * noise1d(W, 8, L.rng)
    m = S.below_curve(crest, 6)
    L.wash(m, (0.40, 0.48, 0.60), density=0.95, edge=0.9, gran=0.6)
    L.wash(m * (1 - S.vgrad(H * 0.38, H * 0.6)), (0.86, 0.90, 0.94), density=0.5, edge=0, occlude=False)
    ridge_ink(L, crest, 2.4, gap=0.05, color=INK_BLUE)
    for _ in range(40):
        x = L.rng.uniform(0, W)
        L.ink([(x, gy(crest, x) + 20), (x + 80, gy(crest, x) - 30), (x + 140, gy(crest, x) + 10)], width=2, color=INK_BLUE, dark=0.6)
    for p in range(4):
        sp = s.sprite(f"rider_{p}", 600, 560, anchor=(0.5, 0.96))
        horse_rider(sp, 290, 535, 290, phase=p / 4)
    return s


def s3_blackbox():
    s = Scene(FILM, "s3_blackbox", seed=903)
    sky_layer(s, 'gold', clouds_n=10)
    L, ys = ground_layer(s, 0.8, 30, (0.86, 0.76, 0.56), (0.76, 0.64, 0.48))
    S = L.S
    bx, by = W * 0.62, gy(ys, W * 0.62) + 60
    L.wash(S.poly([(bx - 160, by), (bx - 160, by - 120), (bx + 160, by - 120), (bx + 160, by)], rough=1), (0.56, 0.36, 0.24), density=0.95, edge=0.9)
    L.box(bx - 160, by - 120, bx + 160, by, width=2)
    for k in range(3):
        L.wash(S.ellipse(bx - 90 + k * 90, by - 140, 40, 22, rough=0.5), (0.95, 0.90, 0.76), density=0.6, edge=0.9)
        L.ink([(bx - 130 + k * 90, by - 140), (bx - 50 + k * 90, by - 140)], width=1.2, smooth=0)
    s.meta.update(box=[bx, by - 160])
    sp = s.sprite('blackbox', 160, 130, anchor=(0.5, 0.5))
    sp.wash(sp.S.poly([(20, 20), (140, 20), (140, 110), (20, 110)], rough=0.5), (0.94, 0.52, 0.18), density=1.0, edge=0.9)
    sp.box(20, 20, 140, 110, width=2.4)
    sp.ink([(20, 50), (140, 50)], width=1.6, smooth=0)
    return s


def s4_ten():
    s = Scene(FILM, "s4_ten", seed=904)
    sky_layer(s, 'day', clouds_n=7)
    L, ys = ground_layer(s, 0.62, 10, (0.80, 0.74, 0.56), (0.70, 0.64, 0.50))
    cx, cy = W * 0.5, H * 0.84
    pts = []
    for k in range(10):
        a = -np.pi / 2 + k / 10 * 2 * np.pi
        pts.append((cx + np.cos(a) * 640, cy + np.sin(a) * 170, k))
    for x, y, k in sorted(pts, key=lambda p: p[1]):
        if k == 0:
            figure(L, x, y, 230, robe=(0.30, 0.30, 0.44), arm=0.6)
            book(L, x + 40, y - 120, 90, 46, open_=True, lines=2)
        else:
            figure(L, x, y, 230, robe=ROBES[k % 6], arm=0.9)
            L.wash(L.S.ellipse(x, y - 240, 46, 24, rough=1), (0.70, 0.56, 0.36), density=0.9, edge=0.8)   # 頭頂的籃子
    s.meta.update(scholar=[pts[0][0], pts[0][1] - 160])
    return s


def s5_capsule():
    s = Scene(FILM, "s5_capsule", seed=905)
    L = s.layer('space', 0.0, opaque=True)
    S = L.S
    L.wash(np.ones((H, W), F32), (0.18, 0.20, 0.34), density=0.95, edge=0, gran=0.4)
    L.wash(S.radial(W * 0.5, H * 0.5, W * 0.5), (0.40, 0.42, 0.62), density=0.5, edge=0, bloom=30)
    for half in (0, 1):
        sp = s.sprite(f'cap_{half}', 260, 200, anchor=(1.0 if half == 0 else 0.0, 0.5))
        x0 = 30 if half == 0 else 0
        pts = [(x0 + (0 if half == 0 else 0), 30)]
        m = sp.S.ellipse(130 + (60 if half == 0 else -60), 100, 130, 70, rough=0.5) * (
            (np.arange(260)[None, :] < 230) if half == 0 else (np.arange(260)[None, :] > 30)).astype(F32)
        sp.wash(m, (0.86, 0.30, 0.28) if half == 0 else (0.96, 0.92, 0.80), density=0.95, edge=0.9)
        sp.lift(sp.S.ellipse(100 if half == 0 else 160, 70, 50, 14, rough=0.3), 0.6)
    sp = s.sprite('seed', 120, 90, anchor=(0.5, 0.5))
    m = sp.S.ellipse(60, 45, 34, 22, ang=-20, rough=0.6)
    sp.wash(m, (0.62, 0.45, 0.30), density=1.0, edge=0.8)
    sp.ink([(30, 50), (60, 26), (90, 34), (92, 50), (60, 66), (30, 50)], width=1.8, dark=0.85)
    sp = s.sprite('sprout', 200, 260, anchor=(0.5, 0.97)); seedling(sp, 100, 252, 220)
    return s


def s6_ark():
    s = Scene(FILM, "s6_ark", seed=906, w=int(W * 1.2))
    sky_layer(s, 'grey', clouds_n=14, density=0.85)
    L = s.layer('sea', 0.3)
    water(L, H * 0.52, H * 1.0, (0.50, 0.56, 0.64))
    for x in [300, 900, s.w - 600]:   # 枯樹露出水面
        big_tree(L, x, H * 0.62, 260, bare=True)
    sp = s.sprite('ark', 520, 360, anchor=(0.5, 0.86))
    S = sp.S
    hull = [(30, 230), (490, 220), (430, 300), (90, 305)]
    sp.wash(S.poly(hull, rough=1), (0.46, 0.32, 0.24), density=0.95, edge=0.9)
    sp.ink(hull + [hull[0]], width=2, smooth=0)
    sp.wash(S.poly([(150, 228), (150, 140), (370, 140), (370, 226)], rough=0.6), (0.62, 0.46, 0.32), density=0.95, edge=0.8)
    sp.wash(S.poly([(130, 145), (260, 80), (390, 145)], rough=0.6), (0.40, 0.30, 0.26), density=0.95)
    sp.box(150, 140, 370, 226, width=1.6)
    sp.wash(S.ellipse(260, 185, 18, 22, rough=0.3), (0.95, 0.82, 0.46), density=0.95)
    return s


def s7_grassea():
    s = Scene(FILM, "s7_grassea", seed=907, w=int(W * 1.35))
    sky_layer(s, 'day', clouds_n=12)
    L = s.layer('sea', 0.35)
    ys = steppe(L, H * 0.5, color=(0.74, 0.82, 0.50), second=(0.60, 0.70, 0.44))
    for k in range(10):   # 草浪
        y = H * 0.58 + k * 48
        xs = np.arange(0, s.w, 10)
        L.ink(np.stack([xs, y + 10 * np.sin(xs / 140 + k)], 1), width=1.6, color=(0.40, 0.52, 0.30), dark=0.5, dry=0.5)
    # 港口城市：北京
    hx = s.w - 520
    great_wall(L, H * 0.62, 90, color=(0.70, 0.60, 0.56), x0=hx - 380, x1=s.w)
    palace(L, hx, H * 0.62 - 90, 150)
    L.ink([(hx - 400, H * 0.66), (hx - 400, H * 0.52)], width=4, color=INK_BROWN, smooth=0)       # 碼頭標杆
    s.meta.update(port=[hx - 450, H * 0.66])
    for p in range(4):
        sp = s.sprite(f"camel_{p}", 420, 380, anchor=(0.5, 0.96))
        camel(sp, 200, 365, 300, phase=p / 4)
    return s


def s8_english():
    s = Scene(FILM, "s8_english", seed=908, w=int(W * 1.25))
    sky_layer(s, 'dawn', clouds_n=8)
    far_layer(s, 0.6, 120, (0.70, 0.70, 0.84))
    L = s.layer('steppe', 0.45)
    ys = steppe(L, H * 0.66)
    s.meta.update(ride_y=H * 0.84)
    for p in range(4):
        sp = s.sprite(f"rider_{p}", 600, 600, anchor=(0.5, 0.9))
        horse_rider(sp, 290, 540, 290, phase=p / 4)
        sp.ink([(330, 420), (340, 80)], width=3, color=INK_BROWN, smooth=0)
        sp.wash(sp.S.poly([(340, 80), (440, 100), (340, 140)], rough=0.5), (0.86, 0.22, 0.20), density=0.95, edge=0.9)
    return s


def s9_germanic():
    s = Scene(FILM, "s9_germanic", seed=909)
    sky_layer(s, 'grey', clouds_n=8)
    L = s.layer('forest', 0.3)
    ys = ground(L, H * 0.62, 20, (0.34, 0.42, 0.34), cells=3, ink=0.8)
    rng = np.random.default_rng(9)
    for k in range(24):
        x = rng.uniform(0, W)
        if abs(x - W * 0.5) < 300:
            continue
        tree_pine(L, x, gy(ys, x) + rng.uniform(0, 160), rng.uniform(320, 600), color=(0.22, 0.32, 0.28))
    L = s.layer('soil', 0.45)
    L.wash(L.S.below_curve(np.full(W, H * 0.86, F32), 2), (0.36, 0.28, 0.24), density=0.95, edge=0.8)
    L = s.layer('cathedral', 0.45)
    t = s.tmap('cathedral')
    cx, yg = W * 0.5, H * 0.86
    S = L.S
    body = [(cx - 260, yg), (cx - 260, yg - 300), (cx + 260, yg - 300), (cx + 260, yg)]
    L.wash(S.poly(body, rough=1), (0.82, 0.78, 0.72), density=0.85, edge=0.9, gran=0.7)
    L.box(cx - 260, yg - 300, cx + 260, yg, width=2)
    for side in (-1, 1):
        tw = [(cx + side * 160 - 60, yg - 300), (cx + side * 160 - 60, yg - 620), (cx + side * 160, yg - 820), (cx + side * 160 + 60, yg - 620),
              (cx + side * 160 + 60, yg - 300)]
        L.wash(S.poly(tw, rough=1), (0.78, 0.74, 0.70), density=0.85, edge=0.9, gran=0.7)
        L.ink(tw, width=2, smooth=0)
    rose = S.ellipse(cx, yg - 200, 70, 70, rough=0.5)
    L.wash(rose, (0.50, 0.40, 0.70), density=0.9, edge=0.9)
    for k in range(8):
        a = k / 8 * np.pi * 2
        L.ink([(cx, yg - 200), (cx + np.cos(a) * 70, yg - 200 + np.sin(a) * 70)], width=1.6, smooth=0)
    yy = np.arange(H, dtype=F32)[:, None]
    t[:] = np.clip((yg - yy) / 860, 0, 1) * 0.95 * np.ones((1, W), F32)
    s.meta.update(seed=[cx, yg + 20])
    return s


def s10_desert():
    s = Scene(FILM, "s10_desert", seed=910)
    sky_layer(s, 'desert', clouds_n=4)
    L = s.layer('cells', 0.4)
    S = L.S
    xs = np.arange(W, dtype=F32)
    ys = H * 0.68 + 60 * np.sin(xs / 300) + 20 * noise1d(W, 6, L.rng)
    L.wash(S.below_curve(ys, 2) * (xs < W * 0.6)[None, :], (0.92, 0.80, 0.58), density=0.85, edge=0.8, gran=0.8)
    cells = []
    for k in range(14):
        x = 100 + k * 90
        y = gy(ys, x) + 60 + (k % 3) * 70
        L.wash(S.ellipse(x, y, 34, 44, rough=1), (0.36, 0.28, 0.26), density=0.95, edge=0.8)
        L.wash(S.ellipse(x, y + 12, 18, 10, rough=0.4), (0.95, 0.90, 0.76), density=0.6)
        cells.append([float(x), float(y)])
    t = s.tmap('cells')
    t[:] = fbm(H, W, 5, np.random.default_rng(10), 4) * 0.9 + 0.05
    L = s.layer('north', 0.4)
    S = L.S
    L.wash(S.below_curve(ys, 2) * (xs >= W * 0.6)[None, :], (0.44, 0.52, 0.40), density=0.9, edge=0.8)
    for k in range(6):
        tree_pine(L, W * 0.64 + k * 120, gy(ys, W * 0.64 + k * 120) + 30, 300, color=(0.26, 0.34, 0.30))
    wins = hut(L, W * 0.84, gy(ys, W * 0.84) + 120, 220, snow=False, lit=True)
    s.meta.update(cells=cells, hut=[list(v) for v in wins])
    return s


def s11_honeycomb():
    s = Scene(FILM, "s11_honeycomb", seed=911)
    L = s.layer('paper', 0.0, opaque=True)
    L.wash(np.ones((H, W), F32), (0.96, 0.92, 0.84), density=0.35, edge=0)
    L = s.layer('comb', 0.3)
    S = L.S
    r = 52
    for row in range(9):
        for col in range(9):
            cx = W * 0.14 + col * r * 1.75 + (row % 2) * r * 0.87
            cy = H * 0.24 + row * r * 1.5
            pts = [(cx + np.cos(a) * r * 0.95, cy + np.sin(a) * r * 0.95) for a in np.linspace(np.pi / 6, np.pi / 6 + 2 * np.pi, 7)]
            L.wash(S.poly(pts, rough=0.5), (0.96, 0.78, 0.34), density=0.8, edge=0.9, gran=0.5)
            L.ink(pts, width=1.6, smooth=0, dark=0.8)
    L = s.layer('sketch', 0.3)
    S = L.S
    m = S.blob(W * 0.74, H * 0.5, 230, n=10, spread=0.6, rough=30)
    L.wash(m, (0.94, 0.94, 0.92), density=0.4, edge=0.9)
    rng = np.random.default_rng(4)
    for k in range(26):
        x, y = W * 0.74 + rng.normal(0, 120), H * 0.5 + rng.normal(0, 110)
        L.ink([(x, y), (x + rng.uniform(-90, 90), y + rng.uniform(-60, 60)), (x + rng.uniform(-90, 90), y + rng.uniform(-60, 60))], width=1.2, dark=0.6)
    canopy_contour_ink(L, m, width=1.8, frac=0.8)
    for k in range(5):   # 失敗的公式
        x = W * 0.66 + k * 40
        L.ink([(x, H * 0.82), (x + 26, H * 0.82)], width=1.4, smooth=0)
    return s


def s12_islands():
    s = Scene(FILM, "s12_islands", seed=912, w=int(W * 1.25))
    sky_layer(s, 'day', clouds_n=10)
    L = s.layer('sea', 0.3)
    water(L, H * 0.5, H * 1.0, (0.52, 0.68, 0.84))
    vents = []
    for k, (x, y, r) in enumerate([(400, H * 0.66, 160), (1100, H * 0.62, 110), (1700, H * 0.74, 200), (2400, H * 0.64, 130)]):
        vents.append(island(L, x, y, r, volcano=(k % 2 == 0)))
    for x, y in [(380, H * 0.6), (420, H * 0.59), (1700, H * 0.68)]:   # 島上的小鳥
        L.ink([(x - 14, y), (x, y - 8), (x + 14, y)], width=2, smooth=1)
    s.meta.update(vents=vents)
    return s


ALL = [s1_ignite, s2_wave, s3_blackbox, s4_ten, s5_capsule, s6_ark, s7_grassea, s8_english, s9_germanic, s10_desert, s11_honeycomb, s12_islands]
