"""第十二部《梯子》— 博雅教育：先訓練，後問為什麼"""
import numpy as np
from kit import *
from motifs import _paint_t

FILM = "film12"
SPINES = [(0.62, 0.30, 0.26), (0.30, 0.40, 0.58), (0.70, 0.56, 0.30), (0.36, 0.50, 0.40), (0.52, 0.36, 0.52), (0.78, 0.66, 0.50)]


def room(s, col=(0.84, 0.76, 0.64), glow=None, vign=0.7):
    L = s.layer('room', 0.0, opaque=True)
    S = L.S
    L.wash(np.ones((s.h, s.w), F32), col, density=0.75, edge=0, gran=0.4)
    if glow:
        L.wash(S.radial(glow[0], glow[1], glow[2]), (0.98, 0.88, 0.66), density=0.6, edge=0, bloom=30)
    L.wash(1 - S.radial(s.w * 0.5, s.h * 0.5, s.w * 0.72), (0.36, 0.30, 0.32), density=vign, edge=0, bloom=40)
    return L


def go_board(L, cx, cy, half, grid=True, wood=(0.82, 0.64, 0.40)):
    """俯視棋盤：木板 + 十九路"""
    S = L.S
    pts = [(cx - half, cy - half), (cx + half, cy - half), (cx + half, cy + half), (cx - half, cy + half)]
    L.wash(S.poly(pts, rough=1.5), wood, density=0.85, edge=0.8, gran=0.7)
    L.ink(pts + [pts[0]], width=2.4, color=INK_BROWN, smooth=0)
    g = half * 0.9
    if grid:
        for k in range(19):
            u = -g + 2 * g * k / 18
            L.ink([(cx - g, cy + u), (cx + g, cy + u)], width=1.0, dark=0.55, smooth=0, tremor=0.3)
            L.ink([(cx + u, cy - g), (cx + u, cy + g)], width=1.0, dark=0.55, smooth=0, tremor=0.3)
    return g


def stone(L, x, y, r, black):
    S = L.S
    if black:
        L.wash(S.ellipse(x, y, r, r, rough=0.5), (0.16, 0.16, 0.20), density=1.0, edge=0.6)
        L.wash(S.ellipse(x - r * 0.3, y - r * 0.35, r * 0.3, r * 0.22, rough=0.3), (0.50, 0.52, 0.58), density=0.4, edge=0)
    else:
        L.wash(S.ellipse(x, y, r, r, rough=0.5), (0.96, 0.94, 0.88), density=0.6, edge=0.9)
        L.ink([(x + np.cos(t) * r, y + np.sin(t) * r) for t in np.linspace(0, 2 * np.pi, 16)], width=1.0, dark=0.45, tremor=0.2)


def s1_copy():
    """孩子臨摹「永」字：筆畫先寫出來，字的意思後來才顯現"""
    s = Scene(FILM, "s1_copy", seed=1201)
    room(s, col=(0.86, 0.78, 0.64), glow=(W * 0.62, H * 0.42, 700))
    L = s.layer('desk', 0.4)
    S = L.S
    yd = H * 0.8
    L.wash(S.poly([(W * 0.08, yd), (W * 0.92, yd), (W * 0.96, yd + 80), (W * 0.04, yd + 80)], rough=1), (0.52, 0.36, 0.26), density=0.95, edge=0.8, gran=0.6)
    for x in (W * 0.1, W * 0.9):
        L.ink([(x, yd + 80), (x, H)], width=12, color=INK_BROWN, smooth=0)
    # 宣紙
    px0, py0, px1, py1 = W * 0.44, H * 0.12, W * 0.82, yd - 10
    L.wash(S.poly([(px0, py0), (px1, py0), (px1, py1), (px0, py1)], rough=1), (0.98, 0.96, 0.90), density=0.35, edge=0.6)
    L.box(px0, py0, px1, py1, width=1.4, color=INK_BROWN, dark=0.5)
    for k in range(1, 3):   # 米字格淡線
        pass
    L.ink([(px0, (py0 + py1) / 2), (px1, (py0 + py1) / 2)], width=1.0, color=(0.75, 0.30, 0.25), dark=0.35, smooth=0)
    L.ink([((px0 + px1) / 2, py0), ((px0 + px1) / 2, py1)], width=1.0, color=(0.75, 0.30, 0.25), dark=0.35, smooth=0)
    figure(L, W * 0.28, yd + 10, 420, robe=(0.40, 0.50, 0.66), lean=0.5, arm=0.75)
    L.ink([(W * 0.28 + 140, yd - 270), (W * 0.28 + 200, yd - 330)], width=5, color=INK_BROWN)   # 毛筆
    for k in range(3):
        book(L, W * 0.14 + k * 4, yd - k * 26, 150, 24, color=SPINES[k])
    # 「永」字八法：逐筆寫出
    C = s.layer('char', 0.4)
    t = s.tmap('char')
    bx, by, bw, bh = px0 + 70, py0 + 60, (px1 - px0) - 140, (py1 - py0) - 110
    P = lambda pts: [(bx + u * bw, by + v * bh) for u, v in pts]
    strokes = [
        ([(0.44, 0.02), (0.52, 0.12), (0.54, 0.15)], 30),                    # 點
        ([(0.28, 0.27), (0.42, 0.25), (0.56, 0.24), (0.58, 0.28)], 30),       # 橫
        ([(0.54, 0.26), (0.54, 0.60), (0.54, 0.92), (0.44, 0.84)], 34),       # 豎鉤
        ([(0.18, 0.47), (0.36, 0.44), (0.40, 0.46), (0.16, 0.74)], 28),       # 橫撇
        ([(0.82, 0.34), (0.70, 0.46), (0.60, 0.52)], 26),                     # 短撇
        ([(0.58, 0.48), (0.70, 0.66), (0.80, 0.82), (0.90, 0.90)], 34),       # 捺
    ]
    n = len(strokes)
    for i, (pts, w) in enumerate(strokes):
        pp = P(pts)
        C.ink(pp, width=w, color=(0.08, 0.07, 0.07), dark=0.95, dry=0.35, taper=(0.1, 0.35))
        _paint_t(t, pp, w * 1.6, i / n, (i + 0.9) / n)
    s.meta.update(char=[(px0 + px1) / 2, (py0 + py1) / 2])
    return s


def s2_board():
    s = Scene(FILM, "s2_board", seed=1202)
    room(s, col=(0.46, 0.40, 0.42), glow=(W * 0.5, H * 0.5, 800), vign=0.8)
    L = s.layer('board', 0.4)
    cx, cy, half = W * 0.5, H * 0.52, H * 0.42
    g = go_board(L, cx, cy, half)
    St = s.layer('stones', 0.4)
    rng = np.random.default_rng(22)
    pts = []
    for k in range(90):
        i, j = rng.integers(0, 19, 2)
        x, y = cx - g + 2 * g * i / 18, cy - g + 2 * g * j / 18
        stone(St, x, y, g / 18 * 0.9, black=bool(k % 2))
    # 格局：幾條大勢的分界（金線，畫在 fx 裡）
    u = lambda a, b: [float(cx - g + 2 * g * a / 18), float(cy - g + 2 * g * b / 18)]
    s.meta.update(frame=[[u(0, 6), u(5, 7), u(9, 5), u(13, 8), u(18, 7)], [u(7, 18), u(8, 12), u(9, 5)], [u(9, 5), u(11, 0)], [u(13, 8), u(12, 13), u(18, 14)]])
    return s


def s3_nav():
    """灰色的亂路網，金色節點連成一條路線"""
    s = Scene(FILM, "s3_nav", seed=1203)
    L = s.layer('map', 0.0, opaque=True)
    S = L.S
    L.wash(np.ones((H, W), F32), (0.78, 0.78, 0.82), density=0.6, edge=0, gran=0.5)
    L.wash(1 - S.radial(W * 0.5, H * 0.5, W * 0.7), (0.30, 0.30, 0.40), density=0.8, edge=0, bloom=40)
    rng = np.random.default_rng(33)
    for k in range(140):
        x, y = rng.uniform(0, W), rng.uniform(0, H)
        pts = [(x, y)]
        a = rng.uniform(0, 2 * np.pi)
        for j in range(int(rng.integers(3, 8))):
            a += rng.normal(0, 0.6)
            x, y = x + np.cos(a) * rng.uniform(60, 200), y + np.sin(a) * rng.uniform(60, 200)
            pts.append((x, y))
        L.ink(pts, width=rng.uniform(1.0, 2.6), color=(0.30, 0.32, 0.40), dark=0.55, tremor=1.2)
    route = [(W * 0.08, H * 0.78), (W * 0.2, H * 0.62), (W * 0.3, H * 0.7), (W * 0.4, H * 0.5), (W * 0.5, H * 0.56), (W * 0.58, H * 0.38),
             (W * 0.68, H * 0.44), (W * 0.76, H * 0.3), (W * 0.86, H * 0.36), (W * 0.93, H * 0.2)]
    L.ink(route, width=3.0, color=(0.36, 0.30, 0.24), dark=0.6, smooth=2)
    side = []
    for k in range(40):   # 不在路線上的燈（亂亮又熄）
        side.append([float(rng.uniform(80, W - 80)), float(rng.uniform(80, H - 80)), 12.0])
    s.meta.update(route=[[float(x), float(y), 18.0] for x, y in route], side=side)
    return s


def s4_desks():
    """無盡的一模一樣的書桌，向遠處退去，像梯田"""
    s = Scene(FILM, "s4_desks", seed=1204)
    room(s, col=(0.36, 0.34, 0.40), glow=(W * 0.5, H * 0.18, 600), vign=0.85)
    L = s.layer('hall', 0.4)
    S = L.S
    vx, vy = W * 0.5, H * 0.28
    for r in range(11, -1, -1):
        k = 1 / (1 + r * 0.42)
        y = vy + (H * 0.98 - vy) * k
        n = 9
        for c in range(n):
            u = (c - (n - 1) / 2) / ((n - 1) / 2)
            x = vx + u * W * 0.62 * k
            dw, dh = 150 * k, 26 * k
            L.wash(S.poly([(x - dw, y - dh), (x + dw, y - dh), (x + dw * 1.05, y), (x - dw * 1.05, y)], rough=0.6), (0.56, 0.44, 0.34), density=0.9, edge=0.7)
            figure(L, x, y - dh * 0.4, 230 * k, robe=(0.50, 0.52, 0.58), lean=0.9, arm=0.15, ink=k > 0.18)
            L.wash(S.poly([(x - dw * 0.5, y - dh * 1.1), (x + dw * 0.5, y - dh * 1.1), (x + dw * 0.55, y - dh * 0.8), (x - dw * 0.55, y - dh * 0.8)], rough=0.3),
                   (0.96, 0.94, 0.88), density=0.5, edge=0.6)
    L.ink([(W * 0.5, 0), (W * 0.5, H * 0.14)], width=2, dark=0.8, smooth=0)
    L.wash(S.poly([(W * 0.5 - 50, H * 0.14), (W * 0.5 + 50, H * 0.14), (W * 0.5 + 20, H * 0.11), (W * 0.5 - 20, H * 0.11)], rough=0.5), (0.24, 0.24, 0.26), density=0.95)
    s.meta.update(lamp=[W * 0.5, H * 0.15])
    return s


def s5_tacit():
    """工匠與分數：兩件都打了 95 分的器物，一件有裂"""
    s = Scene(FILM, "s5_tacit", seed=1205)
    room(s, col=(0.84, 0.70, 0.54), glow=(W * 0.3, H * 0.4, 700))
    L = s.layer('shop', 0.4)
    S = L.S
    # 右半邊：冷藍的考場
    L.wash(S.poly([(W * 0.56, 0), (W, 0), (W, H), (W * 0.56, H)], rough=3), (0.46, 0.56, 0.72), density=0.7, edge=0.5, gran=0.5)
    yb = H * 0.8
    L.wash(S.poly([(0, yb), (W, yb), (W, yb + 60), (0, yb + 60)], rough=1), (0.48, 0.34, 0.26), density=0.95, edge=0.8, gran=0.6)
    figure(L, W * 0.2, yb + 10, 460, robe=(0.62, 0.44, 0.30), lean=0.4, arm=0.6)
    L.wash(S.ellipse(W * 0.33, yb - 30, 90, 26, rough=1), (0.40, 0.34, 0.30), density=0.9, edge=0.7)   # 轉盤
    vessel(L, W * 0.33, yb - 40, 140, crude=0.0, col=(0.62, 0.54, 0.44))
    for k, x in enumerate((W * 0.08, W * 0.12, W * 0.44)):
        vessel(L, x, H * 0.36, 70 + k * 6, crude=0.0, col=(0.58, 0.62, 0.52))
    L.ink([(0, H * 0.37), (W * 0.5, H * 0.37)], width=5, color=INK_BROWN, smooth=0)
    vessel(L, W * 0.68, yb, 200, crude=0.0, col=(0.48, 0.62, 0.54))
    vessel(L, W * 0.86, yb, 200, crude=0.0, col=(0.48, 0.62, 0.54))
    # 右邊那件有一道裂
    L.ink([(W * 0.86 - 20, yb - 150), (W * 0.86 + 10, yb - 110), (W * 0.86 - 6, yb - 80), (W * 0.86 + 18, yb - 40)], width=2.6, dark=0.95, smooth=0)
    for x in (W * 0.68, W * 0.86):
        charter(L, x, yb - 260, 120, 80, seal=False, lines=0)
    s.meta.update(tags=[[W * 0.68, yb - 260], [W * 0.86, yb - 260]], crack=[W * 0.86, yb - 100], hand=[W * 0.33, yb - 120])
    return s


def s6_seed():
    """剖開的種子裡藏著整片森林；鋪好的書單石板縫裡冒出野草"""
    s = Scene(FILM, "s6_seed", seed=1206)
    room(s, col=(0.88, 0.82, 0.68), glow=(W * 0.5, H * 0.4, 800), vign=0.55)
    L = s.layer('seed', 0.4)
    S = L.S
    cx, cy, rx, ry = W * 0.5, H * 0.42, 420, 300
    shell = S.ellipse(cx, cy, rx, ry, rough=3)
    L.wash(shell, (0.56, 0.40, 0.26), density=0.95, edge=0.9, gran=0.8)
    inner = S.ellipse(cx, cy, rx - 40, ry - 36, rough=2)
    L.lift(inner, 0.85)
    L.wash(inner, (0.96, 0.90, 0.72), density=0.5, edge=0.5)
    F = s.layer('forest', 0.4)
    t = s.tmap('forest')
    rng = np.random.default_rng(66)
    for k in range(26):
        x = cx + rng.uniform(-rx * 0.8, rx * 0.8)
        lim = (ry - 40) * np.sqrt(max(0, 1 - ((x - cx) / (rx - 40)) ** 2))
        yg = cy + lim * rng.uniform(0.3, 0.75)
        h = rng.uniform(70, 170) * (lim / ry + 0.3)
        if yg - h < cy - lim + 10:
            h = yg - (cy - lim + 10)
        if h < 30:
            continue
        tree_pine(F, x, yg, h, color=[(0.30, 0.48, 0.40), (0.42, 0.56, 0.36), (0.26, 0.40, 0.42)][k % 3], ink=True) if k % 2 else \
            tree_round(F, x, yg, h, green=(0.50, 0.66, 0.36))
        tt = (yg - (cy - ry)) / (2 * ry)
        t[int(max(0, yg - h - 30)):int(yg + 6), int(max(0, x - h * 0.6)):int(x + h * 0.6)] = np.minimum(
            t[int(max(0, yg - h - 30)):int(yg + 6), int(max(0, x - h * 0.6)):int(x + h * 0.6)], rng.uniform(0, 0.9))
    F.clip(inner)
    # 書單石板 + 野草
    P = s.layer('paving', 0.4)
    S = P.S
    y0 = H * 0.8
    for r in range(3):
        for c in range(12):
            x0 = c * 200 + (r % 2) * 100 - 60
            yy = y0 + r * 90
            P.wash(S.poly([(x0 + 6, yy + 6), (x0 + 194, yy + 6), (x0 + 194, yy + 84), (x0 + 6, yy + 84)], rough=1), (0.70, 0.68, 0.66), density=0.8, edge=0.8)
            P.box(x0 + 6, yy + 6, x0 + 194, yy + 84, width=1.2, dark=0.5)
            for j in range(3):
                P.ink([(x0 + 30, yy + 26 + j * 18), (x0 + 30 + rng.uniform(80, 140), yy + 26 + j * 18)], width=1.0, dark=0.35, smooth=0)
    G = s.layer('weeds', 0.4)
    tg = s.tmap('weeds')
    for k in range(70):
        c, r = rng.integers(0, 12), rng.integers(0, 3)
        x = c * 200 + (r % 2) * 100 - 60 + rng.choice([4, 196])
        y = y0 + r * 90 + rng.uniform(10, 84)
        hh = rng.uniform(40, 120)
        tt = rng.uniform(0, 0.7)
        for j in range(4):
            a = -np.pi / 2 + (j - 1.5) * 0.35 + rng.normal(0, 0.12)
            pts = [(x, y), (x + np.cos(a) * hh * 0.5, y + np.sin(a) * hh * 0.5), (x + np.cos(a) * hh, y + np.sin(a) * hh + 6)]
            G.ink(pts, width=2.4, color=(0.36, 0.56, 0.26), dark=0.95)
            _paint_t(tg, pts, 6, tt, tt + 0.3)
    return s


def s7_master():
    s = Scene(FILM, "s7_master", seed=1207, w=int(W * 1.15))
    sky_layer(s, 'dusk', clouds_n=6)
    far_layer(s, 0.56, 160, (0.66, 0.66, 0.82))
    L, ys = ground_layer(s, 0.72, 30, (0.66, 0.70, 0.48), (0.56, 0.60, 0.42))
    S = L.S
    big_tree(L, s.w * 0.24, gy(ys, s.w * 0.24) + 30, 560, seed_rng=np.random.default_rng(71))
    bx, by = s.w * 0.52, gy(ys, s.w * 0.52) + 110
    L.wash(S.poly([(bx - 170, by - 30), (bx + 170, by - 30), (bx + 200, by + 30), (bx - 200, by + 30)], rough=1), (0.80, 0.62, 0.38), density=0.9, edge=0.8)
    for k in range(9):
        u = -150 + k * 300 / 8
        L.ink([(bx + u * 1.0, by - 28), (bx + u * 1.18, by + 28)], width=0.9, dark=0.5, smooth=0)
    L.ink([(bx - 160, by), (bx + 160, by)], width=0.9, dark=0.5, smooth=0)
    figure(L, bx - 300, by + 40, 330, robe=(0.92, 0.90, 0.84), lean=0.35, arm=0.6)      # 老師
    L.ink([(bx - 300 + 20, by - 230), (bx - 300 + 34, by - 170)], width=6, color=(0.94, 0.94, 0.94), dark=0.4)   # 白鬚
    figure(L, bx + 300, by + 40, 290, robe=(0.40, 0.52, 0.66), lean=-0.35, arm=0.3)      # 徒弟
    # 另一邊：同伴在工作台前爭論
    wx = s.w * 0.84
    L.wash(S.poly([(wx - 160, by - 60), (wx + 160, by - 60), (wx + 160, by - 30), (wx - 160, by - 30)], rough=1), (0.50, 0.36, 0.26), density=0.95)
    for x in (wx - 140, wx + 140):
        L.ink([(x, by - 30), (x, by + 40)], width=6, color=INK_BROWN, smooth=0)
    figure(L, wx - 210, by + 40, 280, robe=(0.62, 0.40, 0.32), arm=0.9)
    figure(L, wx + 210, by + 40, 280, robe=(0.46, 0.54, 0.40), arm=0.7)
    stones = [[bx + u, by + v] for u, v in [(-60, -10), (40, 8), (-20, 18), (80, -14), (0, -18), (-100, 6), (110, 14)]]
    s.meta.update(stones=stones, peers=[wx, by - 220])
    fg_layer(s)
    return s


def s8_delete():
    """密林被一層層洗去，只剩一條路"""
    s = Scene(FILM, "s8_delete", seed=1208)
    sky_layer(s, 'day', clouds_n=7)
    far_layer(s, 0.5, 220, (0.66, 0.70, 0.86), snow=True)
    L, ys = ground_layer(s, 0.66, 30, (0.78, 0.80, 0.58), (0.68, 0.70, 0.50))
    path = [(W * 0.5, H * 1.02), (W * 0.46, H * 0.9), (W * 0.54, H * 0.8), (W * 0.5, H * 0.72), (W * 0.52, gy(ys, W * 0.52) + 6)]
    L.wash(L.S.poly([(W * 0.42, H * 1.02), (W * 0.58, H * 1.02), (W * 0.525, H * 0.7), (W * 0.505, gy(ys, W * 0.5))], rough=4), (0.86, 0.76, 0.56), density=0.7, edge=0.6)
    L.ink(path, width=2, color=INK_BROWN, dark=0.5)
    T = s.layer('thicket', 0.45)
    t = s.tmap('thicket')
    rng = np.random.default_rng(88)
    yy, xx = np.mgrid[0:H, 0:W].astype(F32)
    for k in range(160):
        x, y = rng.uniform(-50, W + 50), rng.uniform(H * 0.3, H * 1.05)
        r = rng.uniform(70, 170)
        m = T.S.blob(x, y, r, n=5, spread=0.4, squash=0.8, rough=6)
        T.wash(m, [(0.26, 0.40, 0.30), (0.34, 0.48, 0.32), (0.20, 0.32, 0.30), (0.40, 0.52, 0.34)][k % 4], density=0.85, edge=0.8, gran=0.6)
        if k % 3 == 0:
            canopy_contour_ink(T, m, width=1.2, frac=0.5)
    # 洗去的順序：離中央小路越近越早
    d = np.abs(xx - W * 0.5) / (W * 0.5)
    dy = np.clip((H * 0.95 - yy) / H, 0, 1)
    t[:] = np.clip(d * 0.75 + 0.12 * dy + 0.28 * (fbm(H, W, 10, rng) - 0.5), 0, 0.98)
    s.meta.update(eyes=[W * 0.5, H * 0.56])
    return s


def s9_maps():
    """同一片山，畫成三張地圖：遊客的、大學的、軍事的"""
    s = Scene(FILM, "s9_maps", seed=1209)
    room(s, col=(0.62, 0.52, 0.44), glow=(W * 0.5, H * 0.5, 900), vign=0.6)
    L = s.layer('maps', 0.4)
    S = L.S
    rng = np.random.default_rng(99)
    ridge = [(0.0, 0.62), (0.12, 0.40), (0.24, 0.52), (0.38, 0.28), (0.52, 0.46), (0.66, 0.34), (0.80, 0.50), (0.92, 0.42), (1.0, 0.56)]
    river = [(0.05, 0.95), (0.22, 0.80), (0.40, 0.84), (0.58, 0.70), (0.78, 0.76), (0.98, 0.66)]
    pw, ph = W * 0.28, H * 0.6
    panels = []
    for k in range(3):
        x0 = W * 0.06 + k * (pw + W * 0.03)
        y0 = H * 0.2 + (k - 1) ** 2 * 20
        P = lambda pts: [(x0 + 30 + u * (pw - 60), y0 + 30 + v * (ph - 60)) for u, v in pts]
        paper = [(x0, y0), (x0 + pw, y0 + 6), (x0 + pw - 4, y0 + ph), (x0 + 3, y0 + ph - 4)]
        L.wash(S.poly(paper, rough=1.5), [(0.98, 0.94, 0.80), (0.94, 0.94, 0.92), (0.84, 0.86, 0.74)][k], density=0.45, edge=0.8)
        L.ink(paper + [paper[0]], width=1.6, color=INK_BROWN, dark=0.6, smooth=0)
        rp = P(ridge)
        if k == 0:   # 遊客：彩色山頭、小圖示
            for i in range(1, len(rp) - 1, 2):
                mountains_icon(L, rp[i][0], rp[i][1] + 40, 60)
            L.ink(P(river), width=8, color=(0.40, 0.62, 0.86), dark=0.8)
            for i in range(5):
                x, y = P([(rng.uniform(0.1, 0.9), rng.uniform(0.55, 0.9))])[0]
                L.wash(S.ellipse(x, y, 16, 16, rough=0.3), [(0.92, 0.40, 0.36), (0.96, 0.72, 0.30), (0.50, 0.70, 0.40)][i % 3], density=0.95)
        elif k == 1:  # 大學：建築與道路
            L.ink(rp, width=2.2, dark=0.6)
            L.ink(P(river), width=4, color=(0.50, 0.60, 0.74), dark=0.7)
            for i in range(6):
                x, y = P([(0.15 + i * 0.13, 0.62 + 0.08 * (i % 2))])[0]
                L.wash(S.poly([(x - 26, y), (x + 26, y), (x + 26, y - 40), (x - 26, y - 40)], rough=0.4), (0.70, 0.40, 0.32), density=0.85)
            L.ink(P([(0.1, 0.72), (0.5, 0.7), (0.9, 0.74)]), width=2, dark=0.6, smooth=0)
        else:         # 軍事：方格、等高線、陰影
            for j in range(4):
                off = j * 0.05
                L.ink(P([(u, v + off) for u, v in ridge]), width=1.2, color=(0.36, 0.30, 0.22), dark=0.6)
            for g in range(1, 6):
                L.ink([(x0 + g * pw / 6, y0 + 8), (x0 + g * pw / 6, y0 + ph - 8)], width=0.9, dark=0.4, smooth=0)
                L.ink([(x0 + 8, y0 + g * ph / 6), (x0 + pw - 8, y0 + g * ph / 6)], width=0.9, dark=0.4, smooth=0)
            L.ink(P(river), width=3, color=(0.30, 0.40, 0.50), dark=0.8)
            for i in range(3):
                x, y = P([(0.25 + i * 0.25, 0.3 + 0.12 * (i % 2))])[0]
                L.ink([(x - 14, y - 14), (x + 14, y + 14)], width=3, color=(0.70, 0.18, 0.16))
                L.ink([(x + 14, y - 14), (x - 14, y + 14)], width=3, color=(0.70, 0.18, 0.16))
        panels.append([float(x0 + pw / 2), float(y0 + ph + 40)])
    s.meta.update(panels=panels)
    return s


def s10_spider():
    """水面上的水蜘蛛，水下是看不見的深處"""
    s = Scene(FILM, "s10_spider", seed=1210, w=int(W * 1.2))
    L = s.layer('pond', 0.0, opaque=True)
    S = L.S
    yw = H * 0.42
    L.wash(np.ones((H, s.w), F32), (0.76, 0.82, 0.90), density=0.45, edge=0, gran=0.5)
    L.wash(S.poly([(0, 0), (s.w, 0), (s.w, yw), (0, yw)], rough=3) * S.vgrad(0, yw), (0.98, 0.86, 0.62), density=0.35, edge=0)
    deep = S.poly([(0, yw), (s.w, yw), (s.w, H), (0, H)], rough=3)
    L.wash(deep, (0.16, 0.22, 0.40), density=0.95, edge=0.6, gran=0.5)
    L.wash(deep * S.vgrad(yw, H), (0.06, 0.08, 0.20), density=0.9, edge=0)
    for k in range(30):   # 水面的油光
        y = yw - 10 - k * 9
        L.ink([(0, y), (s.w, y + 4)], width=1.0, color=(0.94, 0.86, 0.70), dark=0.25, tremor=3)
    D = s.layer('depth', 0.3)
    S = D.S
    rng = np.random.default_rng(1010)
    for k in range(5):   # 沉在深處的柱廊與書
        x = 300 + k * 520
        D.wash(S.poly([(x - 30, H * 0.62), (x + 30, H * 0.62), (x + 34, H * 1.0), (x - 34, H * 1.0)], rough=2), (0.24, 0.30, 0.46), density=0.8, edge=0.6)
        D.wash(S.ellipse(x, H * 0.6, 60, 18, rough=2), (0.26, 0.32, 0.48), density=0.8)
    for k in range(9):
        x, y = rng.uniform(100, s.w - 100), rng.uniform(H * 0.6, H * 0.95)
        D.wash(S.ellipse(x, y, 60, 18, ang=rng.uniform(-20, 20), rough=2), (0.40, 0.42, 0.56), density=0.6)
    D.wash(S.blob(s.w * 0.6, H * 0.82, 160, n=4, squash=0.4), (0.18, 0.22, 0.38), density=0.8, edge=0.3)
    s.meta.update(water=yw)
    for p in range(3):
        sp = s.sprite(f'spider_{p}', 220, 120, anchor=(0.5, 0.75))
        S2 = sp.S
        sp.wash(S2.ellipse(110, 70, 22, 12, rough=0.4), (0.18, 0.16, 0.18), density=1.0)
        sp.wash(S2.ellipse(84, 68, 10, 9, rough=0.3), (0.20, 0.18, 0.20), density=1.0)
        for j in range(3):
            sw = np.sin((p / 3 + j / 3) * 2 * np.pi) * 10
            for side in (-1, 1):
                sp.ink([(110 + (j - 1) * 10, 70), (110 + (j - 1) * 40 + sw, 70 + side * 26), (110 + (j - 1) * 70 + sw, 70 + side * 40)], width=1.6, dark=0.95, smooth=1)
    return s


def s11_ladder():
    """書脊做的梯子穿過雲層；更高的梯子越過它的天花板"""
    HH = int(H * 1.9)
    s = Scene(FILM, "s11_ladder", seed=1211, h=HH)
    L = s.layer('sky', 0.0, opaque=True)
    S = L.S
    sky(L, top=(0.30, 0.34, 0.60), horizon=(0.99, 0.86, 0.62), y_h=HH * 0.85, glow=(W * 0.62, HH * 0.1, 400, (0.99, 0.90, 0.70)), density=0.75)
    C = s.layer('clouds', 0.2)
    clouds(C, 9, HH * 0.42, HH * 0.56, (0.94, 0.90, 0.92), rmin=90, rmax=220, density=0.45)
    clouds(C, 6, HH * 0.12, HH * 0.22, (0.90, 0.86, 0.94), rmin=80, rmax=200, density=0.35)
    G = s.layer('ground', 0.4)
    ys = ground(G, HH * 0.92, 30, (0.70, 0.72, 0.50), cells=4, ink=1.2)
    rng = np.random.default_rng(1111)

    def ladder(Lr, x, y_bot, y_top, wid):
        Lr.ink([(x - wid, y_bot), (x - wid * 0.8, y_top)], width=8, color=INK_BROWN, dark=0.9)
        Lr.ink([(x + wid, y_bot), (x + wid * 0.8, y_top)], width=8, color=INK_BROWN, dark=0.9)
        n = int((y_bot - y_top) / 70)
        for k in range(n):
            y = y_bot - 30 - k * 70
            f = (y_bot - y) / (y_bot - y_top)
            ww = wid * (1 - 0.2 * f)
            col = SPINES[k % len(SPINES)]
            Lr.wash(Lr.S.poly([(x - ww, y - 14), (x + ww, y - 14), (x + ww, y + 14), (x - ww, y + 14)], rough=0.6), col, density=0.9, edge=0.7)
            Lr.box(x - ww, y - 14, x + ww, y + 14, width=1.2, dark=0.6)
            Lr.ink([(x - ww * 0.5, y), (x + ww * 0.3, y)], width=1.4, color=(0.90, 0.78, 0.40), dark=0.8, smooth=0)

    A = s.layer('ladder1', 0.4)
    ladder(A, W * 0.42, HH * 0.93, HH * 0.4, 70)
    B = s.layer('ladder2', 0.4)
    ladder(B, W * 0.6, HH * 0.93, HH * 0.08, 80)
    figure(A, W * 0.42, HH * 0.4 + 10, 160, robe=(0.62, 0.36, 0.30), arm=0.9)
    s.meta.update(hh=HH, top2=[W * 0.6, HH * 0.08])
    return s


ALL = [s1_copy, s2_board, s3_nav, s4_desks, s5_tacit, s6_seed, s7_master, s8_delete, s9_maps, s10_spider, s11_ladder]
