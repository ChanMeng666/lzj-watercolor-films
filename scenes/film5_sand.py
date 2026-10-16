"""第五部《散沙》— 費拉、編戶齊民、末人"""
import numpy as np
from kit import *

FILM = "film5"


def compound(L, x, yg, s, ink=True):
    """宗族大院：圍牆 + 堂屋 + 古樹"""
    S = L.S
    big_tree(L, x - s * 0.25, yg - s * 0.12, s * 1.3, seed_rng=np.random.default_rng(int(x)))
    house(L, x + s * 0.1, yg - s * 0.12, s * 0.8, s * 0.42, roof=(0.50, 0.42, 0.40), wall=(0.88, 0.82, 0.72), windows=2, chimney=False)
    w = [(x - s * 0.7, yg), (x - s * 0.7, yg - s * 0.22), (x + s * 0.7, yg - s * 0.22), (x + s * 0.7, yg)]
    L.wash(S.poly(w, rough=1), (0.82, 0.78, 0.70), density=0.85, edge=0.7, gran=0.6)
    L.ink(w, width=1.6, smooth=0)
    L.wash(S.poly([(x - s * 0.08, yg), (x - s * 0.08, yg - s * 0.17), (x + s * 0.08, yg - s * 0.17), (x + s * 0.08, yg)], rough=0.5),
           (0.45, 0.30, 0.26), density=0.95)


def s1_bow():
    s = Scene(FILM, "s1_bow", seed=501)
    sky_layer(s, 'grey', clouds_n=6)
    L = s.layer('shadow', 0.1)
    S = L.S
    figure(L, W * 0.62, H * 1.05, 1100, robe=(0.30, 0.28, 0.34), skin=(0.30, 0.28, 0.34), arm=0.2, ink=False)
    L.T = 1 - (1 - L.T) * 0.55                              # 讓巨影只是半透明的陰影
    L, ys = ground_layer(s, 0.82, 20, (0.66, 0.66, 0.56), (0.56, 0.56, 0.50))
    for p, ln in enumerate([0.1, 0.9]):
        sp = s.sprite(f'bower_{p}', 220, 300, anchor=(0.5, 0.97))
        figure(sp, 110, 290, 230, robe=(0.62, 0.56, 0.46), lean=ln, arm=0.1 + 0.4 * p)
    s.meta.update(bower=[W * 0.3, gy(ys, W * 0.3) + 14])
    fg_layer(s, 0.95, col=(0.56, 0.58, 0.46))
    return s


def s2_sift():
    s = Scene(FILM, "s2_sift", seed=502)
    sky_layer(s, 'day', clouds_n=8)
    far_layer(s, 0.5, 120, (0.70, 0.74, 0.86))
    L = s.layer('grid', 0.45)
    ys = ground(L, H * 0.56, 40, (0.76, 0.74, 0.56), cells=3, ink=1.0)
    for r in range(4):
        for c in range(13):
            x = 140 + c * 165 + (r % 2) * 50
            hut(L, x, H * 0.62 + r * 120, 70 + r * 12, snow=False)
    L = s.layer('clans', 0.45)
    ys2 = ground(L, H * 0.56, 40, (0.70, 0.80, 0.52), cells=3, second=(0.60, 0.70, 0.46), ink=1.0)
    for x, y, sc in [(420, H * 0.72, 300), (1150, H * 0.66, 260), (1880, H * 0.74, 320), (800, H * 0.95, 280), (1550, H * 0.98, 300)]:
        compound(L, x, y, sc)
    t = s.tmap('clans')
    t[:] = fbm(H, W, 5, np.random.default_rng(3), 4) * 0.9 + 0.05
    return s


def s3_doors():
    s = Scene(FILM, "s3_doors", seed=503)
    sky_layer(s, 'dusk', clouds_n=5)
    L = s.layer('street', 0.4)
    S = L.S
    vx, vy = W * 0.5, H * 0.5
    L.wash(S.poly([(0, H), (vx - 40, vy), (vx + 40, vy), (W, H)], rough=1), (0.70, 0.66, 0.60), density=0.8, edge=0.6, gran=0.6)
    lamps = []
    for side in (-1, 1):
        for k in range(9):
            f = 0.55 ** k
            xn = vx + side * (80 + 900 * f)
            xf = vx + side * (80 + 900 * f * 0.55)
            yb = vy + 520 * f
            yt = vy - 520 * f * 0.9
            pts = [(xn, yb), (xn, yt), (xf, vy - 520 * f * 0.55 * 0.9), (xf, vy + 520 * f * 0.55)]
            L.wash(S.poly(pts, rough=0.8), (0.84, 0.80, 0.72), density=0.8, edge=0.7)
            L.ink(pts + [pts[0]], width=max(1, 2 * f), smooth=0, dark=0.7)
            dx = (xn + xf) / 2
            dpts = [(dx - side * 60 * f, vy + 500 * f * 0.78), (dx - side * 60 * f, vy - 160 * f), (dx + side * 60 * f, vy - 140 * f),
                    (dx + side * 60 * f, vy + 500 * f * 0.76)]
            L.wash(S.poly(dpts, rough=0.4), (0.40, 0.30, 0.26), density=0.9)
            lamps.append([dx + side * 110 * f, vy - 220 * f, 50 * f])
    s.meta.update(lamps=lamps)
    return s


def s4_tower():
    s = Scene(FILM, "s4_tower", seed=504)
    sky_layer(s, 'desert', clouds_n=4)
    L = s.layer('land', 0.4)
    S = L.S
    xs = np.arange(W, dtype=F32)
    ys = H * 0.74 + 40 * np.sin(xs / 260) * (xs < W * 0.5) + 10 * noise1d(W, 5, L.rng)
    L.wash(S.below_curve(ys, 2) * (xs < W * 0.52)[None, :], (0.92, 0.82, 0.60), density=0.85, edge=0.8, gran=0.8)
    L.wash(S.below_curve(ys, 2) * (xs >= W * 0.52)[None, :], (0.62, 0.72, 0.46), density=0.85, edge=0.8, gran=0.6)
    # 沙丘上的孤塔
    tower(L, W * 0.24, gy(ys, W * 0.24) + 20, 150, 640, cone=False, wall=(0.86, 0.74, 0.62))
    # 盤根錯節的大樹
    big_tree(L, W * 0.74, gy(ys, W * 0.74) + 10, 760, seed_rng=np.random.default_rng(8))
    rr = np.random.default_rng(5)
    for k in range(9):   # 氣根
        x0 = W * 0.74 + rr.uniform(-280, 280)
        L.ink([(x0, gy(ys, W * 0.74) - 420 + rr.uniform(-60, 60)), (x0 + rr.uniform(-20, 20), gy(ys, x0) + 10)], width=2.2, color=INK_BROWN, dark=0.7)
    L.ink([(W * 0.52, H * 0.2), (W * 0.52, H)], width=1.2, dark=0.3, dry=0.7, smooth=0)
    s.meta.update(tower=[W * 0.24, gy(ys, W * 0.24) - 300])
    return s


def s5_canal():
    s = Scene(FILM, "s5_canal", seed=505, w=int(W * 1.25))
    sky_layer(s, 'gold', clouds_n=4)
    far_layer(s, 0.56, 90, (0.80, 0.70, 0.62))
    L = s.layer('fields', 0.45)
    S = L.S
    ys = ground(L, H * 0.6, 20, (0.86, 0.74, 0.52), cells=3, second=(0.76, 0.62, 0.46), ink=1.0)
    for _ in range(140):   # 龜裂
        x, y = L.rng.uniform(0, s.w), L.rng.uniform(H * 0.66, H)
        pts = [(x, y)]
        for k in range(3):
            pts.append((pts[-1][0] + L.rng.uniform(-40, 40), pts[-1][1] + L.rng.uniform(-14, 14)))
        L.ink(pts, width=1.2, dark=0.45, color=INK_BROWN)
    # 淤塞的渠道
    cy = H * 0.74
    L.wash(S.poly([(0, cy), (s.w, cy - 40), (s.w, cy + 30), (0, cy + 70)], rough=4), (0.70, 0.62, 0.52), density=0.8, edge=0.8)
    for x0 in [200, 900, 1700]:
        L.wash(S.ellipse(x0, cy + 18, 160, 14, rough=3), (0.56, 0.66, 0.70), density=0.7, edge=0.8)
    L.ink([(0, cy), (s.w, cy - 40)], width=1.8); L.ink([(0, cy + 70), (s.w, cy + 30)], width=1.8)
    # 廢棄水車
    wx, wy = 2300, cy - 20
    a = np.linspace(0, 2 * np.pi, 40)
    L.ink([(wx + np.cos(t) * 130, wy + np.sin(t) * 130) for t in a], width=4, color=INK_BROWN)
    for k in range(6):
        t = k * np.pi / 6
        L.ink([(wx - np.cos(t) * 130, wy - np.sin(t) * 130), (wx + np.cos(t) * 130, wy + np.sin(t) * 130)], width=2.5, color=INK_BROWN, smooth=0)
    weeds(L, np.full(s.w, cy - 80, F32), cy - 10, 30)
    s.meta.update(walk_y=H * 0.66)
    for p in range(4):
        sp = s.sprite(f'refugee_{p}', 200, 300, anchor=(0.5, 0.96))
        ph = np.sin(p / 4 * 2 * np.pi)
        figure(sp, 100, 288, 240, robe=(0.56, 0.50, 0.44), lean=0.35, legs=ph * 0.7, pose=ph, arm=0.1)
        sp.wash(sp.S.ellipse(70, 120, 34, 30, rough=1), (0.66, 0.56, 0.42), density=0.9, edge=0.8)   # 包袱
    return s


def s6_chives():
    s = Scene(FILM, "s6_chives", seed=506)
    sky_layer(s, 'day', clouds_n=6)
    L = s.layer('soil', 0.45)
    ys = ground(L, H * 0.5, 10, (0.62, 0.52, 0.40), cells=3, ink=1.0)
    for r in range(9):
        y = H * 0.56 + r * (60 + r * 6)
        for x in np.arange(30, W, 26 + r * 3):
            L.ink([(x, y), (x + 2, y - 8 - r)], width=1.6 + 0.3 * r, color=(0.38, 0.52, 0.26), dark=0.8, smooth=0)
    L = s.layer('chives', 0.45)
    t = s.tmap('chives')
    rng = np.random.default_rng(4)
    for r in range(9):
        y = H * 0.56 + r * (60 + r * 6)
        for x in np.arange(30, W, 26 + r * 3):
            hh = (50 + 18 * r) * rng.uniform(0.85, 1.1)
            for k in range(3):
                a = -np.pi / 2 + (k - 1) * 0.15 + rng.normal(0, 0.05)
                L.ink([(x, y), (x + np.cos(a) * hh * 0.5, y + np.sin(a) * hh * 0.5), (x + np.cos(a) * hh, y + np.sin(a) * hh)],
                      width=2 + 0.4 * r, color=(0.40, 0.64, 0.30), dark=0.9)
    xs = np.arange(W, dtype=F32)[None, :] / W
    t[:] = np.clip(xs * 0.95 + 0.03 * rng.random((H, W)), 0, 1)
    return s


def s7_cradle():
    s = Scene(FILM, "s7_cradle", seed=507)
    L = s.layer('room', 0.0, opaque=True)
    S = L.S
    L.wash(np.ones((H, W), F32), (0.50, 0.44, 0.42), density=0.8, edge=0, gran=0.4)
    L.wash(S.radial(W * 0.5, H * 0.62, W * 0.45), (0.98, 0.86, 0.64), density=0.6, edge=0, bloom=30)
    L = s.layer('props', 0.4)
    S = L.S
    yg = H * 0.82
    L.wash(S.below_curve(np.full(W, yg, F32), 1), (0.46, 0.34, 0.28), density=0.9, edge=0.6)
    cx = W * 0.5
    a = np.linspace(0.1, np.pi - 0.1, 30)
    rock = [(cx + np.cos(t) * 300, yg - 30 - np.sin(t) * 40) for t in a]
    L.ink(rock, width=5, color=INK_BROWN)
    body = [(cx - 260, yg - 220), (cx + 260, yg - 220), (cx + 220, yg - 60), (cx - 220, yg - 60)]
    L.wash(S.poly(body, rough=1), (0.70, 0.52, 0.36), density=0.9, edge=0.8, gran=0.6)
    L.ink(body + [body[0]], width=2, smooth=0)
    L.wash(S.ellipse(cx, yg - 220, 250, 26, rough=1), (0.92, 0.88, 0.80), density=0.6, edge=0.8)   # 空的被褥
    # 一疊賬冊
    for k in range(7):
        book(L, W * 0.2, yg - k * 34, 300 - k * 6, 30, color=[(0.60, 0.30, 0.26), (0.36, 0.40, 0.52), (0.62, 0.52, 0.34)][k % 3])
    book(L, W * 0.8, yg, 280, 30, color=(0.40, 0.30, 0.26)); book(L, W * 0.8, yg - 32, 260, 30, color=(0.36, 0.40, 0.52))
    s.meta.update(lamp=[W * 0.5, H * 0.3])
    return s


def s8_hill():
    s = Scene(FILM, "s8_hill", seed=508)
    sky_layer(s, 'day', clouds_n=7)
    L = s.layer('land', 0.4)
    S = L.S
    xs = np.arange(W, dtype=F32)
    ys = H * 0.78 - 140 * np.exp(-((xs - W * 0.18) / 260) ** 2) - 160 * np.exp(-((xs - W * 0.42) / 240) ** 2) \
         - 760 * np.exp(-((xs - W * 0.78) / 380) ** 2) + 30 * np.exp(-((xs - W * 0.3) / 130) ** 2) + 140 * np.exp(-((xs - W * 0.56) / 200) ** 2)
    m = S.below_curve(ys, 2)
    L.wash(m, (0.72, 0.80, 0.54), density=0.85, edge=0.8, gran=0.5)
    L.wash(m * S.vgrad(H * 0.3, H), (0.56, 0.62, 0.44), density=0.5, edge=0, bloom=20)
    ridge_ink(L, ys, 2.0, gap=0.05)
    bx = int(W * 0.3)
    L.wash(S.ellipse(bx, gy(ys, bx) - 44, 46, 46, rough=0.6), (0.58, 0.52, 0.50), density=0.95, edge=0.9)
    a = np.linspace(0, 2 * np.pi, 30)
    L.ink([(bx + np.cos(t) * 46, gy(ys, bx) - 44 + np.sin(t) * 46) for t in a], width=2)
    L.wash(S.poly([(W * 0.78 - 30, ys[int(W * 0.78)] + 4), (W * 0.78, ys[int(W * 0.78)] - 90), (W * 0.78 + 50, ys[int(W * 0.78)] - 60),
                   (W * 0.78 + 4, ys[int(W * 0.78)] - 40), (W * 0.78 + 4, ys[int(W * 0.78)] + 4)], rough=0.5), (0.80, 0.30, 0.24), density=0.9)
    s.meta.update(ball=[bx, gy(ys, bx) - 44], peak=[W * 0.78, ys[int(W * 0.78)] - 60], valley=[W * 0.56, gy(ys, W * 0.56)])
    return s


def s9_cards():
    s = Scene(FILM, "s9_cards", seed=509)
    L = s.layer('room', 0.0, opaque=True)
    S = L.S
    L.wash(np.ones((H, W), F32), (0.82, 0.76, 0.66), density=0.7, edge=0, gran=0.4)
    dx, dy, dw, dh = W * 0.78, H * 0.2, 360, 640    # 門
    L.wash(S.poly([(dx, dy), (dx + dw, dy), (dx + dw, dy + dh), (dx, dy + dh)], rough=1), (0.52, 0.40, 0.32), density=0.9, edge=0.7)
    L.box(dx, dy, dx + dw, dy + dh, width=3)
    L = s.layer('door_open', 0.0)
    S = L.S
    L.wash(S.poly([(dx, dy), (dx + dw, dy), (dx + dw, dy + dh), (dx, dy + dh)], rough=1), (0.92, 0.94, 0.98), density=0.5, edge=0.6)
    L.wash(S.poly([(dx, dy), (dx + 90, dy + 30), (dx + 90, dy + dh - 20), (dx, dy + dh)], rough=0.6), (0.52, 0.40, 0.32), density=0.95)
    L.box(dx, dy, dx + dw, dy + dh, width=3)
    L = s.layer('table', 0.3)
    S = L.S
    ty = H * 0.8
    L.wash(S.poly([(W * 0.1, ty), (W * 0.7, ty), (W * 0.72, ty + 50), (W * 0.08, ty + 50)], rough=1), (0.56, 0.38, 0.28), density=0.95, edge=0.8)
    L.ink([(W * 0.1, ty), (W * 0.7, ty)], width=3, smooth=0)
    for k in (0.12, 0.66):
        L.ink([(W * k, ty + 50), (W * k, H)], width=8, color=INK_BROWN, smooth=0)
    # 紙牌屋：每張牌是一個精靈
    sp = s.sprite('card', 150, 210, anchor=(0.5, 1.0))
    sp.wash(sp.S.poly([(8, 8), (142, 8), (142, 202), (8, 202)], rough=0.6), (0.97, 0.95, 0.90), density=0.5, edge=0.9)
    sp.box(8, 8, 142, 202, width=2)
    sp.wash(sp.S.ellipse(75, 105, 26, 34, rough=0.6), (0.76, 0.22, 0.20), density=0.9, edge=0.9)
    cards = []
    base_x = W * 0.4
    for lvl in range(4):
        n = 4 - lvl
        for i in range(n):
            cx = base_x + (i - (n - 1) / 2) * 170
            y = ty - lvl * 205
            cards.append([cx - 38, y, 0.26, lvl]); cards.append([cx + 38, y, -0.26, lvl])
    s.meta.update(cards=cards, ty=ty)
    return s


def s10_feast():
    s = Scene(FILM, "s10_feast", seed=510, w=int(W * 1.2))
    sky_layer(s, 'night', clouds_n=0, density=0.95)
    L = s.layer('town', 0.35)
    S = L.S
    ys = ground(L, H * 0.7, 20, (0.28, 0.28, 0.36), cells=3, ink=1.0)
    wins = palace(L, s.w * 0.36, gy(ys, s.w * 0.36) + 10, 360, wall=(0.46, 0.24, 0.24), roof=(0.56, 0.46, 0.30))
    for k, x in enumerate([s.w * 0.72, s.w * 0.82]):   # 空糧倉
        yg = gy(ys, x) + 10
        L.wash(S.poly([(x - 90, yg), (x - 90, yg - 220), (x + 90, yg - 220), (x + 90, yg)], rough=1), (0.40, 0.36, 0.40), density=0.9, edge=0.8)
        L.wash(S.poly([(x - 110, yg - 220), (x, yg - 320), (x + 110, yg - 220)], rough=1), (0.34, 0.30, 0.34), density=0.9)
        L.box(x - 30, yg - 140, x + 30, yg, width=1.6)
    L = s.layer('field', 0.8)
    ys2 = ground(L, H * 0.9, 20, (0.22, 0.24, 0.28), cells=4, ink=1.4)
    figure(L, s.w * 0.9, gy(ys2, s.w * 0.9) + 20, 200, robe=(0.26, 0.26, 0.32), skin=(0.32, 0.30, 0.34), lean=0.5)
    s.meta.update(lamps=[list(v) for v in wins])
    return s


def s11_garden():
    s = Scene(FILM, "s11_garden", seed=511)
    sky_layer(s, 'grey', clouds_n=6)
    far_layer(s, 0.56, 160, (0.80, 0.82, 0.88), snow=True)
    L = s.layer('snow', 0.45)
    ys = snowfield(L, H * 0.66, 50)
    cx = W * 0.5
    yg = gy(ys, cx) + 140
    wall = [(cx - 460, yg), (cx - 460, yg - 110), (cx + 460, yg - 110), (cx + 460, yg)]
    L.wash(L.S.poly([(cx - 440, yg), (cx - 440, yg - 100), (cx + 440, yg - 100), (cx + 440, yg)], rough=1), (0.62, 0.52, 0.42), density=0.6, edge=0.6)
    for k in range(18):
        seedling(L, cx - 380 + k * 45, yg - 6, 60 + 20 * np.sin(k), )
    L.wash(L.S.poly(wall, rough=1) * 0 + L.S.poly([(cx - 470, yg - 100), (cx - 470, yg - 130), (cx + 470, yg - 130), (cx + 470, yg - 100)], rough=1),
           (0.70, 0.64, 0.58), density=0.85, edge=0.7)
    L.wash(L.S.poly([(cx - 470, yg + 10), (cx - 470, yg - 20), (cx + 470, yg - 20), (cx + 470, yg + 10)], rough=1), (0.70, 0.64, 0.58), density=0.85, edge=0.7)
    w = hut(L, cx + 560, yg, 160, lit=True)
    s.meta.update(lamps=[list(v) for v in w], garden=[cx, yg - 60])
    return s


ALL = [s1_bow, s2_sift, s3_doors, s4_tower, s5_canal, s6_chives, s7_cradle, s8_hill, s9_cards, s10_feast, s11_garden]
