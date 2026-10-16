"""第三部《守先待後》"""
import numpy as np
from scene import Scene, W, H
from wc import blur, F32
from motifs import *

FILM = "film3"


def s1_monastery():
    s = Scene(FILM, "s1_monastery", seed=301)
    L = s.layer("sky", 0.0, opaque=True)
    sky(L, top=(0.14, 0.16, 0.32), horizon=(0.40, 0.42, 0.58), y_h=H * 0.8, density=0.95)
    L = s.layer("far", 0.12)
    mountains(L, H * 0.6, 300, (0.40, 0.42, 0.56), cells=3, sharp=0.4, density=0.7, ink=0.7, snow=True)
    L = s.layer("ridge", 0.4)
    S = L.S
    xs = np.arange(W, dtype=F32)
    ys = H * 0.62 + 260 * ((xs - W * 0.56) / W) ** 2 * 4 + 12 * noise1d(W, 6, L.rng)
    m = S.below_curve(ys, rough=3)
    L.wash(m, (0.84, 0.86, 0.94), density=0.4, edge=0.4)
    L.wash(m * (1 - S.vgrad(H * 0.6, H)), (0.52, 0.56, 0.72), density=0.6, edge=0, bloom=20)
    ridge_ink(L, ys, 1.4, gap=0.3, color=INK_BLUE)
    x = int(W * 0.56)
    s.meta["lamps"] = [list(v) for v in monastery(L, x - 60, float(ys[x]) + 12, 200)]
    for px in [W * 0.32, W * 0.38, W * 0.74, W * 0.8, W * 0.86]:
        tree_pine(L, px, float(ys[int(px)]) + 18, L.rng.uniform(150, 230), color=(0.24, 0.32, 0.36), snow=True)
    L = s.layer("fg", 1.0)
    ys2 = snowfield(L, H * 0.92, 40, shadow=(0.50, 0.54, 0.70), ink=1.6)
    for px in [120, 300, W - 220]:
        tree_pine(L, px, float(ys2[px]) + 80, L.rng.uniform(480, 620), color=(0.18, 0.24, 0.30), snow=True)
    return s


def s2_desk():
    s = Scene(FILM, "s2_desk", seed=302)
    L = s.layer("room", 0.0, opaque=True)
    S = L.S
    L.wash(np.ones((H, W), F32), (0.60, 0.48, 0.40), density=0.8, edge=0, gran=0.4)
    L.wash(S.radial(W * 0.5, H * 0.55, W * 0.6) ** 1.2, (0.98, 0.84, 0.60), density=0.6, edge=0, bloom=30)
    L.wash(1 - S.radial(W * 0.5, H * 0.5, W * 0.75), (0.30, 0.24, 0.26), density=0.9, edge=0, bloom=40)
    # 窗：窗外夜雪
    wx, wy, ww, wh = W * 0.74, H * 0.18, 380, 440
    win = S.poly([(wx, wy), (wx + ww, wy), (wx + ww, wy + wh), (wx, wy + wh)], rough=1)
    L.lift(win, 0.9)
    L.wash(win, (0.30, 0.34, 0.52), density=0.9, edge=0.6)
    L.box(wx, wy, wx + ww, wy + wh, width=5, color=INK_BROWN, dark=0.9)
    L.ink([(wx + ww / 2, wy), (wx + ww / 2, wy + wh)], width=4, color=INK_BROWN, dark=0.9, smooth=0)
    L.ink([(wx, wy + wh / 2), (wx + ww, wy + wh / 2)], width=4, color=INK_BROWN, dark=0.9, smooth=0)
    s.meta["window"] = [wx, wy, ww, wh]
    # 書架
    for row in range(3):
        y = H * 0.22 + row * 150
        L.ink([(W * 0.06, y), (W * 0.4, y)], width=5, color=INK_BROWN, dark=0.85)
        x = W * 0.07
        while x < W * 0.39:
            bw = L.rng.uniform(18, 34)
            bh = L.rng.uniform(90, 130)
            book(L, x + bw / 2, y - 3, bw, bh, color=[(0.55, 0.30, 0.28), (0.36, 0.40, 0.50), (0.62, 0.52, 0.34),
                                                    (0.40, 0.46, 0.36)][int(L.rng.integers(4))])
            x += bw + 2
    L = s.layer("desk", 0.4)
    S = L.S
    top = H * 0.68
    L.wash(S.poly([(-20, top), (W + 20, top - 10), (W + 20, H + 10), (-20, H + 10)], rough=1.5),
           (0.56, 0.38, 0.28), density=0.95, edge=0.7, gran=0.6)
    for k in range(18):
        y = top + 20 + k * 22
        L.ink([(0, y), (W, y + L.rng.uniform(-6, 6))], width=1.0, dark=0.3, dry=0.6, color=INK_BROWN)
    L.ink([(-20, top), (W + 20, top - 10)], width=3, dark=0.9)
    book(L, W * 0.48, top + 300, 1000, 340, open_=True, lines=12)
    book(L, W * 0.2, top + 70, 260, 50, color=(0.40, 0.28, 0.26))
    book(L, W * 0.2, top + 22, 230, 46, color=(0.30, 0.36, 0.46))
    flame = candle(L, W * 0.8, top + 170, 260)
    s.meta["flame"] = flame
    # 毛筆
    L.ink([(W * 0.64, top + 200), (W * 0.72, top + 120)], width=7, color=INK_BROWN, dark=0.9)
    L.ink([(W * 0.635, top + 205), (W * 0.62, top + 224)], width=9, dark=0.95)
    return s


def s3_clock():
    s = Scene(FILM, "s3_clock", seed=303)
    L = s.layer("sky", 0.0, opaque=True)
    sky(L, top=(0.60, 0.68, 0.84), horizon=(0.96, 0.92, 0.84), y_h=H * 0.7)
    clouds(L, 8, H * 0.05, H * 0.4, (0.76, 0.76, 0.84), rmin=80, rmax=200, density=0.35)
    L = s.layer("tower", 0.4)
    S = L.S
    cx = W * 0.5
    tw = 520
    yt, yb = H * 0.12, H + 20
    L.wash(S.poly([(cx - tw / 2, yb), (cx - tw / 2, yt), (cx + tw / 2, yt), (cx + tw / 2, yb)], rough=2),
           (0.84, 0.78, 0.68), density=0.85, edge=0.7, gran=0.7)
    L.wash(S.poly([(cx + tw * 0.2, yb), (cx + tw * 0.2, yt), (cx + tw / 2, yt), (cx + tw / 2, yb)], rough=1),
           (0.64, 0.62, 0.70), density=0.5, edge=0.3)
    cn = [(cx - tw / 2 - 30, yt), (cx, yt - 320), (cx + tw / 2 + 30, yt)]
    L.wash(S.poly(cn, rough=1.5), (0.40, 0.44, 0.58), density=0.9, edge=0.8)
    L.ink(cn, width=2.5, dark=0.85)
    L.ink([(cx - tw / 2, yt), (cx - tw / 2, yb)], width=2.5, smooth=0)
    L.ink([(cx + tw / 2, yt), (cx + tw / 2, yb)], width=2.5, smooth=0)
    for k in range(40):
        y = L.rng.uniform(yt, yb)
        x = L.rng.uniform(cx - tw / 2 + 10, cx + tw / 2 - 60)
        L.ink([(x, y), (x + 50, y)], width=1.0, dark=0.35, dry=0.5)
    # 鐘面
    fy = yt + 240
    face = S.ellipse(cx, fy, 170, 170, rough=1.2)
    L.wash(face, (0.98, 0.95, 0.86), density=0.4, edge=0.8)
    a = np.linspace(0, 2 * np.pi, 60)
    L.ink([(cx + np.cos(t) * 170, fy + np.sin(t) * 170) for t in a], width=4, dark=0.9)
    for k in range(12):
        t = k / 12 * 2 * np.pi
        L.ink([(cx + np.cos(t) * 140, fy + np.sin(t) * 140), (cx + np.cos(t) * 160, fy + np.sin(t) * 160)], width=3.5)
    s.meta["clock"] = [cx, fy, 150]
    # 擺錘窗口
    py0 = fy + 260
    L.wash(S.poly([(cx - 150, py0), (cx + 150, py0), (cx + 150, py0 + 520), (cx - 150, py0 + 520)], rough=1),
           (0.30, 0.26, 0.30), density=0.95, edge=0.7)
    L.box(cx - 150, py0, cx + 150, py0 + 520, width=3)
    s.meta["pivot"] = [cx, py0 + 16]
    sp = s.sprite("pendulum", 120, 480, anchor=(0.5, 0.03))
    sp.ink([(60, 10), (60, 400)], width=4, color=(0.70, 0.56, 0.30), dark=0.9)
    m = sp.S.ellipse(60, 420, 44, 44, rough=0.6)
    sp.wash(m, (0.88, 0.68, 0.30), density=1.0, edge=0.9)
    sp.lift(sp.S.ellipse(48, 408, 12, 10, rough=0.3), 0.7)
    sp.ink([(60 + np.cos(t) * 44, 420 + np.sin(t) * 44) for t in a], width=2, dark=0.8)
    for nm, ln, wd in [("hand_h", 90, 9), ("hand_m", 135, 6)]:
        sp = s.sprite(nm, 40, ln + 30, anchor=(0.5, (ln + 10) / (ln + 30)))
        sp.ink([(20, ln + 10), (20, 8)], width=wd, dark=0.95, taper=(0.05, 0.5))
    return s


def s4_digging():
    s = Scene(FILM, "s4_digging", seed=304)
    L = s.layer("sky", 0.0, opaque=True)
    sky(L, top=(0.70, 0.76, 0.88), horizon=(0.98, 0.94, 0.84), y_h=H * 0.6)
    L = s.layer("far", 0.15)
    mountains(L, H * 0.5, 160, (0.74, 0.78, 0.88), cells=3, density=0.5, ink=0.7, snow=True)
    L = s.layer("slope", 0.5)
    S = L.S
    xs = np.arange(W, dtype=F32)
    ys = H * 0.84 - (xs / W) * H * 0.3 + 10 * noise1d(W, 5, L.rng)
    m = S.below_curve(ys, rough=3)
    L.wash(m, (0.72, 0.70, 0.52), density=0.85, edge=0.7, gran=0.6)
    L.wash(m * S.vgrad(H * 0.5, H), (0.58, 0.52, 0.42), density=0.6, edge=0, bloom=20)
    for _ in range(14):  # 殘雪
        x = L.rng.uniform(0, W)
        L.lift(S.ellipse(x, float(ys[int(x)]) + L.rng.uniform(30, 300), L.rng.uniform(60, 180), L.rng.uniform(8, 20),
                         ang=-8, rough=5), 0.8)
    ridge_ink(L, ys, 1.6, gap=0.2)
    rowx = [W * 0.18, W * 0.3, W * 0.42]
    for x in rowx:  # 已種下的小樹
        tree_round(L, x, float(ys[int(x)]) + 20, 170, green=(0.62, 0.76, 0.42))
    hole_x = W * 0.62
    hy = float(ys[int(hole_x)]) + 30
    L.wash(S.ellipse(hole_x, hy, 70, 16, rough=2), (0.36, 0.28, 0.24), density=0.95, edge=0.8)
    L.wash(S.ellipse(hole_x + 130, hy - 4, 60, 26, rough=4), (0.50, 0.38, 0.30), density=0.9, edge=0.7)
    s.meta["dig"] = [hole_x + 150, hy + 6]
    s.meta["dirt"] = [hole_x, hy]
    s.meta["sapling"] = [W * 0.54, float(ys[int(W * 0.54)]) + 26]
    for p in range(3):
        sp = s.sprite(f"digger_{p}", 300, 360, anchor=(0.5, 0.95))
        digger(sp, 130, 342, 280, phase=p / 2)
    sp = s.sprite("sapling", 200, 260, anchor=(0.5, 0.97))
    seedling(sp, 100, 252, 220)
    return s


def s5_storm():
    s = Scene(FILM, "s5_storm", seed=305, w=int(W * 1.3))
    w = s.w
    L = s.layer("sky", 0.0, opaque=True)
    sky(L, top=(0.40, 0.42, 0.52), horizon=(0.76, 0.78, 0.84), y_h=H * 0.7)
    L = s.layer("far", 0.15)
    mountains(L, H * 0.62, 260, (0.56, 0.58, 0.68), cells=3, sharp=0.4, density=0.6, ink=0.6, snow=True)
    L = s.layer("field", 0.5)
    ys = snowfield(L, H * 0.8, 30, shadow=(0.66, 0.70, 0.82))
    for x in [400, 1900, 2600]:
        tree_pine(L, x, float(ys[x]) + 10, 260, color=(0.30, 0.36, 0.42), snow=True)
    s.meta["walk_y"] = float(H * 0.88)
    for p in range(4):
        sp = s.sprite(f"walker_{p}", 200, 300, anchor=(0.5, 0.96))
        ph = np.sin(p / 4 * 2 * np.pi)
        figure(sp, 100, 288, 250, robe=(0.42, 0.26, 0.24), lean=0.55, legs=ph * 0.9, pose=ph, arm=0.15)
        sp.ink([(150, 140), (178, 120), (196, 136)], width=3, color=(0.42, 0.26, 0.24), dark=0.8)  # 圍巾
    return s


def s6_sprout():
    s = Scene(FILM, "s6_sprout", seed=306)
    L = s.layer("sky", 0.0, opaque=True)
    sky(L, top=(0.62, 0.74, 0.90), horizon=(0.99, 0.94, 0.82), y_h=H * 0.62)
    L = s.layer("earth", 0.4)
    S = L.S
    ys = ground(L, H * 0.62, 50, (0.70, 0.62, 0.44), cells=3, second=(0.56, 0.46, 0.36), ink=1.3)
    L = s.layer("sprouts", 0.4)
    t = s.tmap("sprouts")
    rng = np.random.default_rng(9)
    for k in range(26):
        x = rng.uniform(80, W - 80)
        y = rng.uniform(float(ys[int(x)]) + 60, H - 40)
        hh = 50 + 160 * (y - H * 0.62) / (H * 0.38)
        seedling(L, x, y, hh, tmap=t, t0=rng.uniform(0, 0.4))
    L = s.layer("snow", 0.4)
    S = L.S
    m = S.below_curve(ys - 6, rough=3)
    L.wash(m, (0.95, 0.96, 0.99), density=0.5, edge=0.3, gran=0.2)
    L.wash(m * S.vgrad(H * 0.6, H), (0.78, 0.82, 0.92), density=0.6, edge=0.6, bloom=10)
    for _ in range(30):
        x = L.rng.uniform(0, W)
        L.wash(S.ellipse(x, L.rng.uniform(H * 0.66, H), L.rng.uniform(80, 260), L.rng.uniform(8, 16), rough=6),
               (0.74, 0.78, 0.90), density=0.5, edge=0.6)
    L.cov = np.maximum(L.cov, m)  # 雪是不透明的一層
    ts = s.tmap("snow")
    ts[:] = fbm(H, W, 6, np.random.default_rng(4), 4)
    return s


def s7_valley():
    s = Scene(FILM, "s7_valley", seed=307, w=int(W * 1.3))
    w = s.w
    L = s.layer("sky", 0.0, opaque=True)
    sky(L, top=(0.56, 0.70, 0.92), horizon=(0.99, 0.94, 0.80), y_h=H * 0.6,
        glow=(w * 0.5, H * 0.5, 280, (0.99, 0.90, 0.66)))
    clouds(L, 12, H * 0.05, H * 0.34, (0.80, 0.82, 0.92), rmin=60, rmax=180, density=0.3)
    L = s.layer("far", 0.15)
    mountains(L, H * 0.5, 240, (0.66, 0.74, 0.88), cells=4, sharp=0.3, density=0.5, ink=0.7, snow=True)
    L = s.layer("valley", 0.45)
    ys = ground(L, H * 0.62, 90, (0.70, 0.84, 0.50), cells=4, second=(0.60, 0.74, 0.44), ink=1.2)
    x = int(w * 0.5)
    s.meta["lamps"] = [list(v) for v in monastery(L, x - 80, float(ys[x]) + 10, 130)]
    rng = L.rng
    for xx in np.arange(150, w, 120):  # 果園
        if abs(xx - x) < 260:
            continue
        yy = float(ys[int(xx)]) + rng.uniform(40, 150)
        if rng.random() < 0.4:
            blossom_tree(L, xx, yy, 120)
        else:
            tree_round(L, xx, yy, 110, green=(0.60, 0.76, 0.40))
    L = s.layer("fg", 1.0)
    ys2 = ground(L, H * 0.94, 30, (0.58, 0.72, 0.40), cells=5, ink=2.0)
    field_strokes(L, ys2, H, None, n=600, h=(20, 50))
    for k, xx in enumerate([w * 0.3, w * 0.36, w * 0.62, w * 0.7]):
        figure(L, xx, float(ys2[int(xx)]) + 40, 200, robe=[(0.60, 0.34, 0.30), (0.34, 0.42, 0.60), (0.56, 0.52, 0.30),
                                                            (0.40, 0.50, 0.40)][k], arm=0.2 + 0.2 * k)
    return s


ALL = [s1_monastery, s2_desk, s3_clock, s4_digging, s5_storm, s6_sprout, s7_valley]
