"""第十一部《霉菌》— 宗教與秩序"""
import numpy as np
import cv2
from kit import *
from wc import lblur

FILM = "film11"
ROBES = [(0.70, 0.34, 0.30), (0.30, 0.42, 0.62), (0.76, 0.62, 0.34), (0.40, 0.54, 0.40), (0.56, 0.38, 0.56), (0.80, 0.50, 0.36)]


def room(s, col=(0.80, 0.72, 0.62), glow=None, dark=0.7):
    L = s.layer('room', 0.0, opaque=True)
    S = L.S
    L.wash(np.ones((s.h, s.w), F32), col, density=0.75, edge=0, gran=0.4)
    if glow:
        L.wash(S.radial(glow[0], glow[1], glow[2]), (0.98, 0.88, 0.66), density=0.6, edge=0, bloom=30)
    L.wash(1 - S.radial(s.w * 0.5, s.h * 0.5, s.w * 0.72), (0.30, 0.26, 0.30), density=dark, edge=0, bloom=40)
    return L


def dots_mask(S, pts, rough=1.5):
    """很多小圓點合成一張遮罩（一次 wash，比逐個畫快得多）"""
    m = S.blank()
    for x, y, r in pts:
        cv2.ellipse(m, (int(x * 16), int(y * 16)), (int(r * 16), int(r * 0.9 * 16)), 0, 0, 360, 1.0, -1, cv2.LINE_AA, shift=4)
    m = S.roughen(m, rough, 20)
    return lblur(m, 0.8)


def dots_tmap(t, pts, vals, pad=4):
    for (x, y, r), v in zip(pts, vals):
        cv2.ellipse(t, (int(x), int(y)), (int(r + pad), int(r + pad)), 0, 0, 360, float(v), -1)


# ---------------------------------------------------------------- 培養皿
DCX, DCY, DR = W * 0.5, H * 0.59, 440
COLONIES = [(DCX - 70, DCY + 24, 124, 270), (DCX + 245, DCY - 180, 46, 124), (DCX + 190, DCY + 228, 36, 100)]


def dish_base(s):
    L = s.layer('table', 0.0, opaque=True)
    S = L.S
    L.wash(np.ones((H, W), F32), (0.34, 0.26, 0.22), density=0.85, edge=0, gran=0.6)
    rng = np.random.default_rng(5)
    for k in range(40):   # 木紋
        y = rng.uniform(0, H)
        xs = np.linspace(-20, W + 20, 30)
        L.ink([(x, y + 14 * np.sin(x / 300 + k)) for x in xs], width=rng.uniform(0.8, 2.0), color=(0.20, 0.14, 0.12), dark=0.3, dry=0.5)
    L.wash(S.radial(W * 0.5, H * 0.45, W * 0.55), (0.70, 0.56, 0.42), density=0.4, edge=0, bloom=40)
    L.wash(S.ellipse(DCX + 40, DCY + 40, DR + 30, DR + 30, rough=2), (0.16, 0.12, 0.12), density=0.5, edge=0, bloom=30)   # 皿影
    L = s.layer('dish', 0.4)
    S = L.S
    L.wash(S.ellipse(DCX, DCY, DR, DR, rough=1), (0.90, 0.82, 0.58), density=0.62, edge=0.5, gran=0.7)
    L.wash(S.ellipse(DCX, DCY, DR, DR, rough=1) * (1 - S.radial(DCX, DCY, DR * 1.05)), (0.78, 0.66, 0.44), density=0.4, edge=0)
    a = np.linspace(0, 2 * np.pi, 120)
    L.ink([(DCX + np.cos(t) * DR, DCY + np.sin(t) * DR) for t in a], width=3.0, color=(0.30, 0.26, 0.24), dark=0.7)
    L.ink([(DCX + np.cos(t) * (DR - 22), DCY + np.sin(t) * (DR - 22)) for t in a], width=1.2, color=(0.30, 0.26, 0.24), dark=0.4)
    L.lift(S.ellipse(DCX - DR * 0.45, DCY - DR * 0.62, DR * 0.36, 26, ang=-32, rough=2), 0.5)   # 玻璃反光
    return L


def colony(L, x, y, r, rng):
    S = L.S
    L.wash(S.blob(x, y, r * 1.18, n=12, spread=0.3, rough=r * 0.08), (0.94, 0.95, 0.90), density=0.55, edge=0.3, gran=0.2)   # 白色菌絲邊
    L.wash(S.blob(x, y, r, n=12, spread=0.32, rough=r * 0.07), (0.38, 0.60, 0.54), density=0.85, edge=0.7, gran=0.9)
    L.wash(S.blob(x, y, r * 0.58, n=8, spread=0.3, rough=r * 0.05), (0.20, 0.40, 0.42), density=0.8, edge=0.8, gran=0.9)
    L.wash(S.radial(x, y, r * 0.25), (0.86, 0.90, 0.70), density=0.5, edge=0)
    for k in range(int(r * 0.5)):   # 孢子顆粒
        a, d = rng.uniform(0, 2 * np.pi), r * np.sqrt(rng.uniform(0, 1)) * 0.9
        L.ink([(x + np.cos(a) * d, y + np.sin(a) * d), (x + np.cos(a) * d + 2, y + np.sin(a) * d + 1)], width=rng.uniform(1.5, 3.5), color=(0.16, 0.30, 0.30), dark=0.6, smooth=0)


def bacteria_pts(rng, n, inside=None):
    """在皿內撒點；inside=None 表示落在各菌落的抑菌圈之外；否則只落在抑菌圈裡"""
    pts = []
    while len(pts) < n:
        a, d = rng.uniform(0, 2 * np.pi), (DR - 40) * np.sqrt(rng.uniform(0, 1))
        x, y = DCX + np.cos(a) * d, DCY + np.sin(a) * d
        ds = [np.hypot(x - cx, y - cy) / hr for cx, cy, cr, hr in COLONIES]
        inhalo = min(ds) < 1
        if (inside is None and not inhalo) or (inside is not None and inhalo and all(np.hypot(x - cx, y - cy) > cr * 1.25 for cx, cy, cr, hr in COLONIES)):
            pts.append((x, y, rng.uniform(5, 15)))
    return pts


def colony_dist(xs, ys):
    """每個像素到最近菌落的相對距離（以菌落半徑為 1）"""
    return np.min([np.hypot(xs - cx, ys - cy) / (cr * 1.25) for cx, cy, cr, hr in COLONIES], axis=0)


def halo_dist(xs, ys):
    return np.min([np.hypot(xs - cx, ys - cy) / hr for cx, cy, cr, hr in COLONIES], axis=0)


GRID = np.meshgrid(np.arange(W, dtype=F32), np.arange(H, dtype=F32))
BCOL = (0.76, 0.48, 0.42)


def s1_candles():
    s = Scene(FILM, "s1_candles", seed=1101)
    sky_layer(s, 'night', clouds_n=0)
    far_layer(s, 0.58, 90, (0.24, 0.24, 0.36), ink=0.4)
    L, ys = ground_layer(s, 0.66, 30, (0.22, 0.24, 0.26), (0.18, 0.20, 0.24), ink=0.6)
    wins = []
    for k, x in enumerate([260, 520, 1700, 1960, 2180]):
        wins += house(L, x, gy(ys, x) + 30, 180, 110, roof=(0.30, 0.28, 0.36), wall=(0.42, 0.40, 0.44), windows=2, ink=True)
    church(L, W * 0.5 + 360, gy(ys, W * 0.5 + 360) + 30, 130)
    fx0, fy0 = W * 0.42, H * 0.86
    figure(L, fx0, fy0, 220, robe=(0.34, 0.30, 0.40), lean=0.5, arm=0.5)
    rng = np.random.default_rng(11)
    cands = []
    for k in range(70):   # 從人物開始向外鋪開的燭光
        a, d = rng.uniform(np.pi, 2 * np.pi) if k % 3 else rng.uniform(0, np.pi), 80 + 1100 * np.sqrt(rng.uniform(0, 1))
        x, y = fx0 + np.cos(a) * d, fy0 + np.sin(a) * d * 0.16
        y = max(y, gy(ys, x) + 40)
        if 0 < x < W and y < H - 20:
            cands.append([float(x), float(y), 8.0 + 6 * (y - H * 0.66) / (H * 0.34), float(d)])
    cands.sort(key=lambda c: c[3])
    s.meta.update(candles=[c[:3] for c in cands], wins=[[float(w[0]), float(w[1]), 18.0] for w in wins], hand=[fx0 + 70, fy0 - 120])
    return s


def s2_dish():
    s = Scene(FILM, "s2_dish", seed=1102)
    dish_base(s)
    rng = np.random.default_rng(22)
    # 抑菌圈外：細菌菌落
    L = s.layer('bact', 0.4)
    pts = bacteria_pts(rng, 300)
    L.wash(dots_mask(L.S, pts), BCOL, density=0.8, edge=0.9, gran=0.5)
    t = s.tmap('bact')
    dots_tmap(t, pts, rng.uniform(0, 1, len(pts)))
    # 抑菌圈內：先有，後被清掉
    L = s.layer('bact_in', 0.4)
    pin = bacteria_pts(rng, 120, inside=True)
    L.wash(dots_mask(L.S, pin), BCOL, density=0.8, edge=0.9, gran=0.5)
    t = s.tmap('bact_in')
    dots_tmap(t, pin, [halo_dist(np.array(x), np.array(y)) for x, y, r in pin])
    # 霉菌
    L = s.layer('mould', 0.4)
    for cx, cy, cr, hr in COLONIES:
        colony(L, cx, cy, cr, rng)
    t = s.tmap('mould')
    xs, ys = GRID
    d = colony_dist(xs, ys)
    t[:] = np.where(d < 1.1, d, 9.0)
    s.meta.update(colonies=[[c[0], c[1], c[2], c[3]] for c in COLONIES])
    return s


def s3_wipe():
    s = Scene(FILM, "s3_wipe", seed=1103)
    dish_base(s)
    rng = np.random.default_rng(33)
    L = s.layer('bact', 0.4)
    pts = bacteria_pts(rng, 300)
    L.wash(dots_mask(L.S, pts), BCOL, density=0.8, edge=0.9, gran=0.5)
    L = s.layer('mould', 0.4)
    for cx, cy, cr, hr in COLONIES:
        colony(L, cx, cy, cr, rng)
    xs, ys = GRID
    sweep = np.clip((xs - (DCX - DR)) / (2 * DR), 0, 1).astype(F32)
    t = s.tmap('mould')
    t[:] = sweep
    # 被擦乾淨以後湧進來的細菌
    L = s.layer('flood', 0.4)
    pf = []
    while len(pf) < 200:
        a, dd = rng.uniform(0, 2 * np.pi), (DR - 40) * np.sqrt(rng.uniform(0, 1))
        x, y = DCX + np.cos(a) * dd, DCY + np.sin(a) * dd
        if halo_dist(np.array(x), np.array(y)) < 1.05:
            pf.append((x, y, rng.uniform(6, 16)))
    L.wash(dots_mask(L.S, pf), BCOL, density=0.8, edge=0.9, gran=0.5)
    t = s.tmap('flood')
    dots_tmap(t, pf, [np.clip((x - (DCX - DR)) / (2 * DR), 0, 1) + rng.uniform(0.05, 0.3) for x, y, r in pf])
    # 最頑強的菌株：深色大菌落
    L = s.layer('hard', 0.4)
    ph = []
    for k in range(22):
        a, dd = rng.uniform(0, 2 * np.pi), (DR - 90) * np.sqrt(rng.uniform(0, 1))
        ph.append((DCX + np.cos(a) * dd, DCY + np.sin(a) * dd, rng.uniform(24, 46)))
    L.wash(dots_mask(L.S, ph, rough=4), (0.42, 0.16, 0.18), density=0.95, edge=0.9, gran=0.8)
    t = s.tmap('hard')
    dots_tmap(t, ph, rng.uniform(0, 1, len(ph)), pad=8)
    sp = s.sprite('cloth', 360, 300, anchor=(0.5, 0.5))
    sp.wash(sp.S.blob(180, 150, 120, n=8, spread=0.4, squash=0.7, rough=8), (0.86, 0.90, 0.94), density=0.85, edge=0.8)
    for k in range(5):
        sp.ink([(90 + k * 10, 100 + k * 22), (270 - k * 8, 110 + k * 20)], width=1.2, color=(0.50, 0.56, 0.66), dark=0.5)
    s.meta.update(dish=[DCX, DCY, DR])
    return s


def s4_cell():
    s = Scene(FILM, "s4_cell", seed=1104)
    room(s, col=(0.62, 0.56, 0.50), glow=(W * 0.66, H * 0.62, 520), dark=0.8)
    L = s.layer('wall', 0.2)
    S = L.S
    L.wash(S.below_curve(np.full(W, H * 0.86, F32), 2), (0.42, 0.34, 0.30), density=0.85)
    cx, cy = W * 0.74, H * 0.34   # 牆上一個樸素的木十字
    L.ink([(cx, cy - 90), (cx, cy + 110)], width=9, color=INK_BROWN, smooth=0)
    L.ink([(cx - 60, cy - 30), (cx + 60, cy - 30)], width=9, color=INK_BROWN, smooth=0)
    L = s.layer('books', 0.4)
    rng = np.random.default_rng(4)
    y = H * 0.88
    x0 = W * 0.26
    for k in range(17):   # 一摞越疊越歪的註疏
        bw, bh = rng.uniform(220, 300), rng.uniform(34, 52)
        x = x0 + k * k * 0.9 + rng.uniform(-14, 14)
        book(L, x, y, bw, bh, color=[(0.52, 0.30, 0.28), (0.36, 0.38, 0.48), (0.58, 0.50, 0.34), (0.40, 0.34, 0.30)][k % 4])
        y -= bh
    L = s.layer('fig', 0.45)
    fx0, fy0 = W * 0.64, H * 0.88
    figure(L, fx0, fy0, 260, robe=(0.50, 0.42, 0.36), lean=0.6, arm=0.4)
    tip = candle(L, fx0 + 120, fy0 - 4, 70)
    s.meta.update(flame=tip, books=[x0, H * 0.5])
    return s


def s5_rose():
    s = Scene(FILM, "s5_rose", seed=1105)
    sky_layer(s, 'night', clouds_n=0, y_h=0.9)
    L = s.layer('rose', 0.3)
    S = L.S
    cx, cy, R = W * 0.5, H * 0.47, 430
    t = s.tmap('rose')
    xs, ys = GRID
    ang = (np.arctan2(ys - cy, xs - cx) + np.pi) / (2 * np.pi)
    glass = [(0.30, 0.40, 0.70), (0.72, 0.26, 0.26), (0.86, 0.70, 0.30), (0.34, 0.56, 0.44)]
    n = 12
    for k in range(n):   # 花瓣格
        a0, a1 = 2 * np.pi * k / n, 2 * np.pi * (k + 1) / n
        for ring, (r0, r1) in enumerate([(0.18, 0.5), (0.5, 0.82), (0.82, 0.98)]):
            pts = [(cx + np.cos(a) * R * r0, cy + np.sin(a) * R * r0) for a in np.linspace(a0, a1, 6)] + \
                  [(cx + np.cos(a) * R * r1, cy + np.sin(a) * R * r1) for a in np.linspace(a1, a0, 6)]
            L.wash(S.poly(pts, rough=1.5), glass[(k + ring) % 4], density=0.75, edge=0.7, gran=0.6)
    L.wash(S.ellipse(cx, cy, R * 0.18, R * 0.18, rough=1), (0.92, 0.80, 0.44), density=0.8, edge=0.7)
    gold = (0.86, 0.72, 0.42)
    for r in (0.18, 0.5, 0.82, 0.98):
        L.ink([(cx + np.cos(a) * R * r, cy + np.sin(a) * R * r) for a in np.linspace(0, 2 * np.pi, 120)], width=3.2, color=gold, dark=0.9)
    for k in range(n):
        a = 2 * np.pi * k / n
        L.ink([(cx + np.cos(a) * R * 0.18, cy + np.sin(a) * R * 0.18), (cx + np.cos(a) * R * 0.98, cy + np.sin(a) * R * 0.98)], width=3, color=gold, smooth=0)
        am = a + np.pi / n   # 尖拱
        L.ink([(cx + np.cos(a) * R * 0.5, cy + np.sin(a) * R * 0.5), (cx + np.cos(am) * R * 0.74, cy + np.sin(am) * R * 0.74),
               (cx + np.cos(a + 2 * np.pi / n) * R * 0.5, cy + np.sin(a + 2 * np.pi / n) * R * 0.5)], width=2.2, color=gold)
    t[:] = np.where(np.hypot(xs - cx, ys - cy) < R * 1.04, ang, 9.0)
    # 同樣幾何的星座
    stars = [[float(cx + np.cos(2 * np.pi * k / n) * R * 1.55 * (1.0 if k % 2 else 1.25)), float(cy + np.sin(2 * np.pi * k / n) * R * 1.0 * (1.0 if k % 2 else 1.25))] for k in range(n)]
    s.meta.update(rose=[cx, cy, R], stars=stars)
    return s


def s6_ship():
    s = Scene(FILM, "s6_ship", seed=1106, w=int(W * 1.3))
    sky_layer(s, 'dawn', clouds_n=8)
    L = s.layer('sea', 0.3)
    water(L, H * 0.62, H * 1.0, (0.44, 0.58, 0.72))
    L, ys = ground_layer(s, 0.64, 40, (0.60, 0.70, 0.48), (0.50, 0.60, 0.42), name='shore')
    L.clip(L.S.poly([(s.w * 0.78, 0), (s.w, 0), (s.w, H), (s.w * 0.74, H)], rough=30))
    for k, x in enumerate(np.arange(s.w * 0.82, s.w - 40, 90)):
        seedling(L, x, gy(ys, x) + 60 + (k % 2) * 30, 40 + 10 * (k % 3))
    sp = s.sprite('ship', 560, 520, anchor=(0.5, 0.86))
    ship(sp, 270, 440, 190)
    for k in range(4):
        figure(sp, 150 + k * 46, 380, 56, robe=ROBES[k], ink=True)
    sp.wash(sp.S.ellipse(390, 372, 36, 26, rough=1.5), (0.80, 0.68, 0.46), density=0.95, edge=0.9)   # 種子袋
    sp.ink([(370, 352), (410, 352)], width=1.6)
    s.meta.update(sea_y=H * 0.78, shore=[s.w * 0.82, H * 0.74])
    fg = s.layer('fgw', 0.8)
    water(fg, H * 0.94, H * 1.0, (0.36, 0.50, 0.66))
    return s


def s7_granary():
    s = Scene(FILM, "s7_granary", seed=1107, w=int(W * 1.15))
    sky_layer(s, 'day', clouds_n=7)
    far_layer(s, 0.56, 120, (0.70, 0.74, 0.86))
    L, ys = ground_layer(s, 0.68, 30, (0.78, 0.76, 0.52), (0.66, 0.66, 0.46))
    S = L.S
    mx = 420
    monastery(L, mx, gy(ys, mx) + 40, 220, lit=False)
    gx = 900
    house(L, gx, gy(ys, gx) + 40, 260, 200, roof=(0.56, 0.40, 0.30), wall=(0.80, 0.70, 0.54), windows=0, chimney=False)
    door = [gx, gy(ys, gx) + 40 - 70]
    L.wash(S.poly([(gx - 40, door[1] - 60), (gx + 40, door[1] - 60), (gx + 40, door[1] + 70), (gx - 40, door[1] + 70)], rough=1), (0.24, 0.18, 0.16), density=0.95)
    for k in range(8):   # 麥袋
        L.wash(S.ellipse(gx - 200 + k * 30, gy(ys, gx) + 30 - (k % 2) * 20, 28, 34, rough=1), (0.86, 0.74, 0.48), density=0.9, edge=0.9)
    rng = np.random.default_rng(7)
    pts = [(1400 + k * 140 + rng.uniform(-20, 20), gy(ys, 1400 + k * 140) + 90 + (k % 2) * 30) for k in range(7)]
    villagers(L, pts, 150, rng)
    bowls = []
    for x, y in pts:
        L.wash(S.ellipse(x + 30, y - 70, 22, 10, rough=0.5), (0.56, 0.40, 0.30), density=0.95)
        bowls.append([float(x + 30), float(y - 76)])
    B = s.layer('boards', 0.45)
    for k in range(3):
        B.ink([(gx - 60, door[1] - 40 + k * 46), (gx + 60, door[1] - 50 + k * 50)], width=11, color=(0.46, 0.34, 0.24), dark=0.8, smooth=0)
    for p in range(4):
        sp = s.sprite(f'wander_{p}', 220, 300, anchor=(0.5, 0.96))
        ph = np.sin(p / 4 * 2 * np.pi)
        figure(sp, 100, 288, 220, robe=(0.46, 0.44, 0.46), lean=0.35, legs=ph, pose=ph, arm=0.2)
        sp.ink([(150, 120), (150 + ph * 10, 290)], width=3, color=INK_BROWN, smooth=0)
    s.meta.update(door=door, bowls=bowls, road_y=gy(ys, 1200) + 150)
    fg_layer(s)
    return s


def s8_statue():
    s = Scene(FILM, "s8_statue", seed=1108)
    sky_layer(s, 'grey', clouds_n=6)
    L, ys = ground_layer(s, 0.8, 20, (0.64, 0.64, 0.56), (0.56, 0.56, 0.50))
    S = L.S
    yg = gy(ys, 600) + 40
    L.wash(S.poly([(260, yg + 10), (980, yg + 10), (940, yg - 80), (300, yg - 80)], rough=2), (0.56, 0.56, 0.58), density=0.9, edge=0.8)   # 基座
    figure(L, 640, yg - 80, 760, robe=(0.62, 0.62, 0.64), skin=(0.66, 0.66, 0.68), lean=0.7, arm=0.0)
    L.ink([(580, yg - 80), (760, yg - 80)], width=2.4)
    rng = np.random.default_rng(8)
    cx, cy = W * 0.72, gy(ys, W * 0.72) + 60
    L.wash(S.radial(cx, cy - 80, 360), (0.98, 0.86, 0.58), density=0.5, edge=0, bloom=30)
    pts = [(cx + np.cos(a) * 250, cy + np.sin(a) * 50) for a in np.linspace(0, 2 * np.pi, 9)[:-1]]
    villagers(L, pts, 150, rng)
    L.wash(S.ellipse(cx, cy - 20, 40, 18, rough=1), (0.96, 0.80, 0.40), density=0.9)
    sp = s.sprite('sap_0', 140, 180, anchor=(0.5, 0.96))
    seedling(sp, 70, 172, 120)
    sp = s.sprite('sap_1', 140, 180, anchor=(0.5, 0.96))
    sp.ink([(70, 172), (74, 120), (100, 100), (110, 120)], width=4, color=(0.46, 0.42, 0.24), dark=0.85)
    for k in range(3):
        sp.wash(sp.S.ellipse(90 + k * 8, 132 + k * 14, 16, 7, ang=60, rough=0.6), (0.64, 0.58, 0.32), density=0.9)
    for p in range(4):
        sp = s.sprite(f'leaver_{p}', 220, 300, anchor=(0.5, 0.96))
        ph = np.sin(p / 4 * 2 * np.pi)
        figure(sp, 110, 288, 200, robe=(0.56, 0.38, 0.56), legs=ph, pose=ph, lean=0.2)
    s.meta.update(sapling=[640 + 330, yg - 60], circle=[cx, cy], lamp=[cx, cy - 30])
    return s


def s9_summer():
    s = Scene(FILM, "s9_summer", seed=1109)
    sky_layer(s, 'day', clouds_n=7, y_h=0.45)
    surf = H * 0.44
    L = s.layer('soil', 0.4)
    S = L.S
    xs = np.arange(W, dtype=F32)
    ysurf = surf + 10 * noise1d(W, 8, L.rng)
    L.wash(S.below_curve(ysurf, 2), (0.50, 0.38, 0.28), density=0.9, edge=0.6, gran=0.8)
    L.wash(S.below_curve(ysurf, 2) * S.vgrad(surf, H), (0.30, 0.22, 0.18), density=0.7, edge=0, bloom=20)
    rng = np.random.default_rng(9)
    for k in range(120):   # 石子
        L.wash(S.ellipse(rng.uniform(0, W), rng.uniform(surf + 40, H), rng.uniform(6, 18), rng.uniform(4, 10), rough=1), (0.62, 0.56, 0.48), density=0.6, edge=0.9)
    church(L, W * 0.5, surf + 6, 110)
    L = s.layer('roots', 0.4)
    t = s.tmap('roots')
    roots(L, W * 0.5, surf + 12, H * 0.62, np.random.default_rng(19), tmap=t, width=10, n_main=7, color=(0.86, 0.72, 0.46))
    below = L.S.below_curve(np.full(W, surf + 4, F32), rough=0)
    L.clip(below)
    t[below < 0.5] = 9.0
    L = s.layer('flowers', 0.5)
    S = L.S
    cols = [(0.94, 0.52, 0.56), (0.98, 0.84, 0.40), (0.78, 0.60, 0.88), (0.96, 0.96, 0.92), (0.96, 0.62, 0.30)]
    L.wash(S.below_curve(ysurf - 150 + 30 * noise1d(W, 14, L.rng), 6) * (1 - S.below_curve(ysurf + 6, 1)), (0.46, 0.64, 0.34), density=0.85, edge=0.7)
    for k in range(5):
        pts = [(rng.uniform(0, W), rng.uniform(surf - 160, surf), rng.uniform(7, 16)) for _ in range(160)]
        L.wash(dots_mask(S, pts), cols[k], density=0.9, edge=0.9)
    field_strokes(L, ysurf - 120, surf, None, n=900, h=(20, 60), ink_col=(0.28, 0.40, 0.20))
    s.meta.update(church=[W * 0.5, surf - 60])
    return s


def s10_candle():
    s = Scene(FILM, "s10_candle", seed=1110)
    room(s, col=(0.34, 0.30, 0.36), glow=(W * 0.5, H * 0.32, 700), dark=0.85)
    L = s.layer('arches', 0.15)
    for x in np.arange(160, W, 400):
        arc = [(x - 150, H * 0.95)] + [(x + np.cos(t) * 150, H * 0.42 - np.sin(t) * 260) for t in np.linspace(np.pi, 0, 16)] + [(x + 150, H * 0.95)]
        L.ink(arc, width=2.4, color=(0.60, 0.54, 0.50), dark=0.5)
    L = s.layer('pool', 0.4)
    S = L.S
    cx, top, bot, rw = W * 0.5, H * 0.24, H * 0.88, 74
    L.wash(S.ellipse(cx, bot, 260, 40, rough=3), (0.94, 0.90, 0.80), density=0.85, edge=0.8)
    L.wash(S.poly([(cx - 330, bot + 30), (cx + 330, bot + 30), (cx + 300, bot + 90), (cx - 300, bot + 90)], rough=1), (0.62, 0.52, 0.40), density=0.9)   # 燭台
    L.ink([(cx - 330, bot + 30), (cx + 330, bot + 30)], width=2.4, smooth=0)
    L = s.layer('wax', 0.4)
    S = L.S
    L.wash(S.poly([(cx - rw, top), (cx + rw, top), (cx + rw, bot), (cx - rw, bot)], rough=1.5), (0.96, 0.92, 0.82), density=0.8, edge=0.7, gran=0.4)
    L.wash(S.poly([(cx + rw * 0.3, top), (cx + rw, top), (cx + rw, bot), (cx + rw * 0.3, bot)], rough=1.5), (0.80, 0.74, 0.64), density=0.5, edge=0.3)
    for k in range(5):   # 蠟淚
        x = cx - rw + 20 + k * 30
        L.ink([(x, top + k * 90), (x + 2, top + k * 90 + 120 + k * 20)], width=6, color=(0.92, 0.86, 0.74), dark=0.4)
    L.ink([(cx - rw, top), (cx - rw, bot)], width=1.6, dark=0.6, smooth=0)
    L.ink([(cx + rw, top), (cx + rw, bot)], width=1.6, dark=0.6, smooth=0)
    t = s.tmap('wax')
    yy = GRID[1]
    t[:] = np.clip((yy - top) / (bot - top), 0, 1)
    s.meta.update(top=top, bot=bot, cx=cx)
    return s


def city_layer(s, base, col, lit=0.0, rng=None):
    L = s.layer('city', 0.35)
    S = L.S
    rng = rng or np.random.default_rng(3)
    wins = []
    x = -20
    while x < s.w:
        bw, bh = rng.uniform(120, 220), rng.uniform(140, 380)
        L.wash(S.poly([(x, base), (x, base - bh), (x + bw, base - bh), (x + bw, base)], rough=1), col, density=0.92, edge=0.8)
        L.ink([(x, base), (x, base - bh), (x + bw, base - bh), (x + bw, base)], width=1.4, dark=0.6, smooth=0)
        for wy in np.arange(base - bh + 30, base - 30, 54):
            for wx in np.arange(x + 24, x + bw - 20, 40):
                if rng.random() < lit:
                    wins.append([float(wx), float(wy), 10.0])
        x += bw + rng.uniform(-10, 30)
    return L, wins


def s11_moon():
    s = Scene(FILM, "s11_moon", seed=1111)
    sky_layer(s, 'night', clouds_n=5, cloud_col=(0.30, 0.32, 0.46))
    L = s.layer('moon', 0.05)
    moon(L, W * 0.66, H * 0.26, 130)
    L, wins = city_layer(s, H * 0.92, (0.16, 0.16, 0.24), lit=0.25)
    church(L, W * 0.3, H * 0.92, 160)
    s.meta.update(moon=[W * 0.66, H * 0.26], wins=wins)
    return s


def s12_match():
    s = Scene(FILM, "s12_match", seed=1112, w=int(W * 1.15))
    sky_layer(s, 'night', clouds_n=4, cloud_col=(0.30, 0.32, 0.46))
    L = s.layer('street', 0.4)
    S = L.S
    yg = H * 0.8
    L.wash(S.below_curve(np.full(s.w, yg, F32) + 6 * noise1d(s.w, 10, L.rng), 2), (0.86, 0.88, 0.94), density=0.8, edge=0.6)   # 積雪的街
    church(L, 520, yg + 10, 200)
    L.wash(S.radial(520, yg - 200, 420), (0.08, 0.08, 0.16), density=0.5, edge=0, bloom=30)   # 暗下去的教堂
    hx = s.w - 640
    wins = house(L, hx, yg + 10, 520, 300, roof=(0.40, 0.34, 0.38), wall=(0.62, 0.52, 0.44), windows=4, win_light=False, chimney=True)
    L.ink([(hx - 200, yg - 240), (hx + 200, yg - 240)], width=3, color=(0.70, 0.20, 0.18))   # 新會堂的紅色布條
    for p in range(4):
        sp = s.sprite(f'girl_{p}', 160, 220, anchor=(0.5, 0.96))
        ph = np.sin(p / 4 * 2 * np.pi)
        figure(sp, 80, 212, 140, robe=(0.62, 0.30, 0.28), legs=ph * (1 if p else 0), pose=ph * (1 if p else 0), arm=0.5 if p == 0 else 0.2)
    s.meta.update(church_x=520, hall=[hx, yg], wins=[[float(w[0]), float(w[1]), 22.0] for w in wins], street_y=yg + 40)
    return s


def s13_winter():
    s = Scene(FILM, "s13_winter", seed=1113, w=int(W * 1.1))
    sky_layer(s, 'dusk', clouds_n=6, glow=(W * 0.8, H * 0.5, 300, (0.99, 0.74, 0.52)))
    far_layer(s, 0.52, 140, (0.70, 0.72, 0.86), snow=True)
    L = s.layer('village', 0.4)
    S = L.S
    ys = snowfield(L, H * 0.62, 30)
    wins = []
    rng = np.random.default_rng(13)
    for k, x in enumerate(np.arange(180, s.w - 100, 300)):
        if k == 4:
            church(L, x, gy(ys, x) + 40, 150)
            bell = [float(x - 90), float(gy(ys, x) + 40 - 270)]
            continue
        wins += house(L, x, gy(ys, x) + 40 + (k % 2) * 30, rng.uniform(180, 240), 120, roof=(0.92, 0.92, 0.96), wall=(0.70, 0.60, 0.52), windows=2, chimney=True)
    # 雪下的種子：地面剖面
    L = s.layer('frost', 0.5)
    S = L.S
    fy = H * 0.84
    L.wash(S.below_curve(np.full(s.w, fy, F32) + 8 * noise1d(s.w, 10, L.rng), 2), (0.40, 0.32, 0.30), density=0.9, edge=0.7, gran=0.8)
    L.wash(S.below_curve(np.full(s.w, fy - 30, F32), 3) * (1 - S.below_curve(np.full(s.w, fy + 4, F32), 2)), (0.94, 0.95, 0.98), density=0.8, edge=0.6)
    seeds = []
    for k in range(18):
        x, y = rng.uniform(60, s.w - 60), rng.uniform(fy + 50, H - 40)
        L.wash(S.ellipse(x, y, 16, 10, ang=rng.uniform(0, 180), rough=0.8), (0.82, 0.62, 0.34), density=0.95, edge=0.9)
        L.ink([(x - 12, y), (x + 12, y)], width=1.0, dark=0.5)
        seeds.append([float(x), float(y)])
    s.meta.update(wins=[[float(w[0]), float(w[1]), 16.0] for w in wins], bell=bell, seeds=seeds)
    return s


ALL = [s1_candles, s2_dish, s3_wipe, s4_cell, s5_rose, s6_ship, s7_granary, s8_statue, s9_summer, s10_candle, s11_moon, s12_match, s13_winter]
