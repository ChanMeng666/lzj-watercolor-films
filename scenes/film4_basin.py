"""第四部《窪地》— 秩序的輸入與輸出"""
import numpy as np
from kit import *

FILM = "film4"


def s1_protect():
    s = Scene(FILM, "s1_protect", seed=401)
    sky_layer(s, 'dawn', glow=(W * 0.75, H * 0.45, 260, (0.99, 0.82, 0.58)))
    far_layer(s, 0.6, 150, (0.70, 0.70, 0.84))
    L = s.layer('hill', 0.45)
    S = L.S
    xs = np.arange(W, dtype=F32)
    ys = H * 0.86 - 420 * np.exp(-((xs - W * 0.72) / 520) ** 2) + 10 * noise1d(W, 6, L.rng)
    L.wash(S.below_curve(ys, 3), (0.72, 0.78, 0.50), density=0.85, edge=0.7, gran=0.5)
    L.wash(S.below_curve(ys, 3) * S.vgrad(H * 0.5, H), (0.56, 0.62, 0.42), density=0.5, edge=0, bloom=20)
    ridge_ink(L, ys, 1.6, gap=0.2)
    horse_rider(L, W * 0.72, gy(ys, W * 0.72) + 10, 170)
    lamps = []
    for x in [260, 420, 560, 700]:
        lamps += [list(v) for v in hut(L, x, gy(ys, x) + 16, 120, snow=False)]
    s.meta.update(lamps=lamps, rider=[W * 0.72, gy(ys, W * 0.72) - 170], path=[[800, gy(ys, 800)], [W * 0.62, gy(ys, W * 0.62)]])
    fg_layer(s)
    sp = sprite_fig(s, 'pilgrim', 200, robe=(0.62, 0.52, 0.40), lean=0.4, arm=0.7, legs=0.4)
    return s


def s2_basin():
    s = Scene(FILM, "s2_basin", seed=402)
    sky_layer(s, 'storm', clouds_n=12)
    L = s.layer('land', 0.35)
    S = L.S
    xs = np.arange(W, dtype=F32)
    ys = H * 0.42 + 520 * np.exp(-((xs - W * 0.5) / 560) ** 2) + 20 * noise1d(W, 8, L.rng)
    m = S.below_curve(ys, 3)
    L.wash(m, (0.70, 0.74, 0.56), density=0.85, edge=0.7, gran=0.6)
    L.wash(m * (1 - S.vgrad(H * 0.4, H * 0.95)), (0.52, 0.56, 0.48), density=0.5, edge=0, bloom=20)
    ridge_ink(L, ys, 1.8, gap=0.15)
    # 高地上的小城堡
    hi = []
    for x in [260, 520, W - 520, W - 260]:
        hi += [list(v) for v in castle(L, x, gy(ys, x) + 8, 50)]
    # 窪地底部的城
    cx = W * 0.5
    by = gy(ys, cx) + 10
    great_wall(L, by, 70, color=(0.62, 0.58, 0.58), x0=cx - 300, x1=cx + 300)
    palace(L, cx, by - 70, 150)
    # 溪流
    streams = []
    for sx in [380, 700, W - 700, W - 380]:
        pts = []
        x = sx
        for k in range(16):
            y = gy(ys, x) + 6
            pts.append([float(x), y])
            x += (cx - x) * 0.14
        L.ink(pts, width=3.2, color=(0.35, 0.50, 0.66), dark=0.8)
        streams.append(pts)
    s.meta.update(streams=streams, hi=hi, city=[cx, by - 120])
    return s


def s3_wall():
    s = Scene(FILM, "s3_wall", seed=403, w=int(W * 1.25))
    sky_layer(s, 'grey', clouds_n=10)
    far_layer(s, 0.5, 120, (0.70, 0.70, 0.78))
    L = s.layer('steppe', 0.3)
    ys = steppe(L, H * 0.54, color=(0.80, 0.76, 0.54))
    L = s.layer('wall', 0.55)
    xs = np.arange(s.w, dtype=F32)
    great_wall(L, H * 0.8, 170, color=(0.66, 0.62, 0.60))
    towers = []
    for x in np.arange(300, s.w, 700):
        L.wash(L.S.poly([(x - 70, H * 0.8), (x - 70, H * 0.8 - 300), (x + 70, H * 0.8 - 300), (x + 70, H * 0.8)], rough=1.5),
               (0.60, 0.56, 0.56), density=0.9, edge=0.8)
        L.box(x - 70, H * 0.8 - 300, x + 70, H * 0.8, width=1.6, dark=0.7)
        towers.append([float(x), H * 0.8 - 320])
    s.meta.update(towers=towers, ride_y=H * 0.62)
    fg_layer(s, 0.96, col=(0.62, 0.62, 0.50), grass=300)
    for p in range(4):
        sp = s.sprite(f"rider_{p}", 600, 560, anchor=(0.5, 0.96))
        horse_rider(sp, 290, 535, 290, phase=p / 4)
    return s


def s4_gate():
    s = Scene(FILM, "s4_gate", seed=404)
    sky_layer(s, 'desert', clouds_n=5, glow=(W * 0.5, H * 0.5, 300, (0.99, 0.88, 0.66)))
    far_layer(s, 0.62, 100, (0.80, 0.74, 0.70))
    L = s.layer('cliffs', 0.45)
    S = L.S
    for side in (-1, 1):
        x0 = W * 0.5 + side * 260
        x1 = W * 0.5 + side * 1300
        pts = [(x0, H), (x0 + side * 30, H * 0.3), (x0 + side * 120, H * 0.08), (x1, H * 0.02), (x1, H)]
        L.wash(S.poly(pts, rough=12, scale=50), (0.74, 0.58, 0.46), density=0.9, edge=0.8, gran=0.8)
        L.wash(S.poly(pts, rough=8) * S.vgrad(0, H), (0.52, 0.40, 0.38), density=0.6, edge=0, bloom=10)
        for k in range(30):
            y = L.rng.uniform(H * 0.1, H * 0.95)
            xx = x0 + side * L.rng.uniform(20, 500)
            L.ink([(xx, y), (xx + side * L.rng.uniform(30, 120), y + L.rng.uniform(-10, 30))], width=1.4, dark=0.5, dry=0.5)
        L.ink(pts[:4], width=2.2, dark=0.8)
    L = s.layer('road', 0.6)
    S = L.S
    m = S.below_curve(np.full(W, H * 0.78, F32), 2)
    L.wash(m, (0.88, 0.78, 0.60), density=0.85, edge=0.6, gran=0.6)
    L.wash(S.poly([(W * 0.46, H * 0.78), (W * 0.54, H * 0.78), (W * 0.8, H), (W * 0.2, H)], rough=4), (0.80, 0.66, 0.50), density=0.6, edge=0.5)
    s.meta.update(road=[[W * 0.5, H * 0.79], [W * 0.62, H * 0.98]])
    for p in range(4):
        sp = s.sprite(f"camel_{p}", 420, 380, anchor=(0.5, 0.96))
        camel(sp, 200, 365, 300, phase=p / 4)
    return s


def s5_chariot():
    s = Scene(FILM, "s5_chariot", seed=405)
    sky_layer(s, 'storm', clouds_n=14, density=0.85)
    L = s.layer('plain', 0.4)
    ys = steppe(L, H * 0.7, color=(0.78, 0.74, 0.54), second=(0.62, 0.60, 0.46))
    chariot(L, W * 0.46, H * 0.84, 300)
    s.meta.update(chariot=[W * 0.52, H * 0.6])
    return s


def s6_waves():
    s = Scene(FILM, "s6_waves", seed=406, w=int(W * 1.3))
    sky_layer(s, 'day', clouds_n=10)
    L = s.layer('sea', 0.2)
    water(L, H * 0.5, H * 0.72, (0.56, 0.70, 0.84))
    L = s.layer('beach', 0.5)
    S = L.S
    ys = H * 0.7 + 30 * noise1d(s.w, 5, L.rng)
    L.wash(S.below_curve(ys, 3), (0.92, 0.84, 0.64), density=0.8, edge=0.8, gran=0.7)
    for k in range(3):   # 浪線
        yy = ys - 10 - k * 18
        L.ink(np.stack([np.arange(0, s.w, 8), yy[::8]], 1), width=1.6, color=INK_BLUE, dark=0.5, dry=0.5)
    s.meta.update(spots=[[700, gy(ys, 700) + 120], [1500, gy(ys, 1500) + 120], [2300, gy(ys, 2300) + 120]])
    sp = s.sprite('wave_rider', 600, 560, anchor=(0.5, 0.96)); horse_rider(sp, 290, 535, 290, phase=0.2)
    sp = s.sprite('wave_factory', 700, 420, anchor=(0.5, 0.97)); factory(sp, 350, 405, 220)
    sp = s.sprite('wave_ship', 700, 520, anchor=(0.5, 0.92)); ship(sp, 330, 470, 260)
    return s


def s7_vessels():
    s = Scene(FILM, "s7_vessels", seed=407, w=int(W * 1.3))
    L = s.layer('room', 0.0, opaque=True)
    S = L.S
    L.wash(np.ones((H, s.w), F32), (0.80, 0.72, 0.60), density=0.7, edge=0, gran=0.4)
    L.wash(1 - S.vgrad(0, H * 0.7), (0.60, 0.50, 0.44), density=0.6, edge=0, bloom=30)
    L = s.layer('shelf', 0.4)
    S = L.S
    top = H * 0.74
    L.wash(S.poly([(-10, top), (s.w + 10, top), (s.w + 10, top + 60), (-10, top + 60)], rough=1), (0.56, 0.38, 0.28), density=0.95, edge=0.8)
    L.ink([(-10, top), (s.w + 10, top)], width=3, smooth=0)
    xs = []
    for i, c in enumerate([0.0, 0.2, 0.4, 0.6, 0.85]):
        x = 420 + i * 540
        vessel(L, x, top, 300, crude=c)
        xs.append([x, top - 330])
    s.meta.update(vessels=xs)
    return s


def s8_armor():
    s = Scene(FILM, "s8_armor", seed=408)
    L = s.layer('room', 0.0, opaque=True)
    S = L.S
    L.wash(np.ones((H, W), F32), (0.84, 0.78, 0.68), density=0.7, edge=0, gran=0.4)
    L.wash(S.poly([(W * 0.5, 0), (W, 0), (W, H), (W * 0.5, H)], rough=0), (0.70, 0.70, 0.74), density=0.5, edge=0)
    L.ink([(W * 0.5, 0), (W * 0.5, H)], width=4, smooth=0)
    L = s.layer('props', 0.4)
    S = L.S
    yg = H * 0.86
    L.wash(S.below_curve(np.full(W, yg, F32), 1), (0.60, 0.50, 0.42), density=0.8, edge=0.6)
    armor_stand(L, W * 0.2, yg, 360, good=True)
    figure(L, W * 0.34, yg, 420, robe=(0.55, 0.58, 0.66), arm=0.6)             # 領主試穿
    L.ink([(W * 0.39, yg - 300), (W * 0.42, yg - 520)], width=6, color=(0.5, 0.5, 0.56), smooth=0)   # 劍
    for k in range(4):
        armor_stand(L, W * 0.62 + k * 70, yg, 240, good=False)
    L.wash(S.poly([(W * 0.78, yg - 200), (W * 0.95, yg - 200), (W * 0.95, yg), (W * 0.78, yg)], rough=1), (0.50, 0.36, 0.28), density=0.9)
    figure(L, W * 0.86, yg - 200, 260, robe=(0.30, 0.30, 0.36), arm=0.2)       # 官僚坐在案後
    s.meta.update(stamp=[W * 0.88, yg - 220])
    return s


def s9_pigment():
    s = Scene(FILM, "s9_pigment", seed=409)
    L = s.layer('paper', 0.0, opaque=True)
    L.wash(np.ones((H, W), F32), (0.96, 0.93, 0.86), density=0.3, edge=0)
    L = s.layer('ink', 0.3)
    qinglv_landscape(L, ink_only=True)
    L = s.layer('color', 0.3)
    qinglv_landscape(L, ink_only=False)
    t = s.tmap('color')
    t[:] = fbm(H, W, 4, np.random.default_rng(11), 5) * 0.9 + 0.05
    for p in range(4):
        sp = s.sprite(f"camel_{p}", 260, 240, anchor=(0.5, 0.96))
        camel(sp, 125, 230, 180, phase=p / 4)
    return s


def s10_river():
    s = Scene(FILM, "s10_river", seed=410, w=int(W * 1.3))
    sky_layer(s, 'night', clouds_n=0, density=0.95)
    L = s.layer('banks', 0.4)
    S = L.S
    ys = ground(L, H * 0.56, 30, (0.30, 0.30, 0.40), cells=4, ink=1.0)
    water(L, H * 0.68, H * 0.86, (0.24, 0.28, 0.44))
    left, right = [], []
    for x in np.arange(120, s.w * 0.45, 170):
        left += [list(v) for v in house(L, x, gy(ys, x) + 10, 130, 100, roof=(0.30, 0.26, 0.34), wall=(0.44, 0.42, 0.50), win_light=True)]
    for x in np.arange(s.w * 0.55, s.w - 100, 170):
        right += [list(v) for v in house(L, x, gy(ys, x) + 10, 130, 100, roof=(0.30, 0.26, 0.34), wall=(0.44, 0.42, 0.50))]
    L.wash(S.below_curve(np.full(s.w, H * 0.86, F32), 2), (0.22, 0.24, 0.30), density=0.9, edge=0.6)
    s.meta.update(left=left, right=right, river_y=H * 0.77)
    sp = s.sprite('boat', 300, 300, anchor=(0.5, 0.86)); boat(sp, 150, 258, 110, sail=(0.80, 0.76, 0.70))
    return s


def s11_throne():
    s = Scene(FILM, "s11_throne", seed=411)
    sky_layer(s, 'gold', clouds_n=8, glow=(W * 0.3, H * 0.62, 280, (0.99, 0.76, 0.48)))
    far_layer(s, 0.66, 120, (0.62, 0.56, 0.70))
    L, ys = ground_layer(s, 0.78, 60, (0.70, 0.66, 0.46), (0.56, 0.50, 0.40))
    x = W * 0.58
    throne_rock(L, x, gy(ys, x) + 10, 260)
    figure(L, x, gy(ys, x) - 330, 200, robe=(0.42, 0.40, 0.50), arm=0.0)
    for k in range(5):   # 地上未舉起的盾
        sx = W * 0.3 + k * 120 + L.rng.uniform(-30, 30)
        L.wash(L.S.ellipse(sx, gy(ys, sx) + 60, 46, 18, ang=L.rng.uniform(-20, 20), rough=1), (0.58, 0.46, 0.34), density=0.9, edge=0.9)
        L.ink([(sx - 44, gy(ys, sx) + 60), (sx + 44, gy(ys, sx) + 58)], width=1.4, smooth=0)
    s.meta.update(throne=[x, gy(ys, x) - 330])
    fg_layer(s, 0.95, col=(0.58, 0.56, 0.40))
    return s


ALL = [s1_protect, s2_basin, s3_wall, s4_gate, s5_chariot, s6_waves, s7_vessels, s8_armor, s9_pigment, s10_river, s11_throne]
