"""第十三部《宗族》— 家庭與小共同體"""
import numpy as np
from kit import *

FILM = "film13"
ROBES = [(0.70, 0.34, 0.30), (0.30, 0.42, 0.62), (0.76, 0.62, 0.34), (0.40, 0.54, 0.40), (0.56, 0.38, 0.56), (0.80, 0.50, 0.36)]
GREY = (0.46, 0.46, 0.50)


def room(s, col=(0.80, 0.72, 0.62), glow=None, name='room'):
    L = s.layer(name, 0.0, opaque=True)
    S = L.S
    L.wash(np.ones((H, s.w), F32), col, density=0.75, edge=0, gran=0.4)
    if glow:
        L.wash(S.radial(glow[0], glow[1], glow[2]), (0.98, 0.88, 0.66), density=0.6, edge=0, bloom=30)
    L.wash(1 - S.radial(s.w * 0.5, H * 0.5, s.w * 0.72), (0.36, 0.30, 0.32), density=0.7, edge=0, bloom=40)
    return L


def hall(L, x, yg, s, wall=(0.84, 0.78, 0.68), roof=(0.40, 0.36, 0.40), pillar=(0.62, 0.24, 0.20), roofed=True, doors_open=True):
    """祠堂：台基、紅柱、門洞、飛檐；回傳 (門內燈位, 門中心)"""
    S = L.S
    L.wash(S.poly([(x - s * 1.1, yg), (x - s * 1.02, yg - s * 0.12), (x + s * 1.02, yg - s * 0.12), (x + s * 1.1, yg)], rough=1.2),
           (0.78, 0.76, 0.72), density=0.8, edge=0.6)
    b = yg - s * 0.12
    L.wash(S.poly([(x - s * 0.9, b), (x - s * 0.9, b - s * 0.62), (x + s * 0.9, b - s * 0.62), (x + s * 0.9, b)], rough=1), wall, density=0.85, edge=0.6, gran=0.4)
    dw, dh = s * 0.34, s * 0.5
    L.wash(S.poly([(x - dw / 2, b), (x - dw / 2, b - dh), (x + dw / 2, b - dh), (x + dw / 2, b)], rough=0.6),
           (0.98, 0.84, 0.54) if doors_open else (0.36, 0.20, 0.18), density=0.9, edge=0.7, bloom=6 if doors_open else 0)
    for k in (-1, 1):
        px = x + k * dw * 0.62
        L.wash(S.poly([(px - s * 0.035, b), (px - s * 0.035, b - s * 0.62), (px + s * 0.035, b - s * 0.62), (px + s * 0.035, b)], rough=0.4), pillar, density=0.95, edge=0.8)
        for j in (1.3, 2.2):
            px2 = x + k * dw * 0.62 * j
            L.wash(S.poly([(px2 - s * 0.03, b), (px2 - s * 0.03, b - s * 0.62), (px2 + s * 0.03, b - s * 0.62), (px2 + s * 0.03, b)], rough=0.4), pillar, density=0.9, edge=0.8)
    L.ink([(x - s * 0.9, b), (x - s * 0.9, b - s * 0.62), (x + s * 0.9, b - s * 0.62), (x + s * 0.9, b)], width=max(1.4, s * 0.006), dark=0.7)
    if roofed:
        cn_roof(L, x, b - s * 0.62, s * 2.25, s * 0.42, roof)
    # 匾額
    L.wash(S.poly([(x - s * 0.16, b - s * 0.56), (x - s * 0.16, b - s * 0.68), (x + s * 0.16, b - s * 0.68), (x + s * 0.16, b - s * 0.56)], rough=0.4),
           (0.22, 0.20, 0.24), density=0.95, edge=0.8)
    return [x, b - dh * 0.5, dh * 0.5], [x, b]


def courtyard_house(L, x, yg, s, lit=True):
    """江南小院：白牆黛瓦，正中一扇亮窗"""
    S = L.S
    L.wash(S.poly([(x - s, yg), (x - s, yg - s * 0.55), (x + s, yg - s * 0.55), (x + s, yg)], rough=1), (0.90, 0.88, 0.84), density=0.85, edge=0.7, gran=0.4)
    for k in (-1, 1):   # 馬頭牆
        L.wash(S.poly([(x + k * s, yg - s * 0.55), (x + k * s, yg - s * 0.8), (x + k * s * 0.8, yg - s * 0.8), (x + k * s * 0.8, yg - s * 0.55)], rough=0.8),
               (0.90, 0.88, 0.84), density=0.85, edge=0.7)
        L.ink([(x + k * s * 1.04, yg - s * 0.8), (x + k * s * 0.76, yg - s * 0.8)], width=6, color=(0.20, 0.20, 0.24), smooth=0)
    cn_roof(L, x, yg - s * 0.55, s * 1.7, s * 0.3, (0.24, 0.24, 0.30))
    L.ink([(x - s, yg), (x - s, yg - s * 0.8)], width=1.6, dark=0.6); L.ink([(x + s, yg), (x + s, yg - s * 0.8)], width=1.6, dark=0.6)
    ww, wh = s * 0.5, s * 0.3
    L.wash(S.poly([(x - ww, yg - s * 0.08), (x - ww, yg - s * 0.08 - wh), (x + ww, yg - s * 0.08 - wh), (x + ww, yg - s * 0.08)], rough=0.6),
           (0.98, 0.82, 0.50) if lit else (0.30, 0.30, 0.36), density=0.95, edge=0.7, bloom=8 if lit else 0)
    L.box(x - ww, yg - s * 0.08 - wh, x + ww, yg - s * 0.08, width=2.4, color=INK_BROWN)
    return [x, yg - s * 0.08 - wh * 0.5, ww * 0.7]


def bowl(L, x, y, r, col=(0.92, 0.90, 0.84)):
    S = L.S
    L.wash(S.poly([(x - r, y), (x + r, y), (x + r * 0.6, y + r * 0.7), (x - r * 0.6, y + r * 0.7)], rough=0.6), col, density=0.9, edge=0.8)
    L.wash(S.ellipse(x, y, r, r * 0.25, rough=0.4), (0.96, 0.96, 0.94), density=0.8, edge=0.7)
    L.ink([(x - r, y), (x - r * 0.6, y + r * 0.7), (x + r * 0.6, y + r * 0.7), (x + r, y)], width=1.4, dark=0.7, smooth=0)


# ===================================================================== scenes
def s1_courtyard():
    """雨夜：一院燈火，院外黑巷"""
    s = Scene(FILM, "s1_courtyard", seed=1301, w=int(W * 1.15))
    sky_layer(s, 'night', clouds_n=6, cloud_col=(0.26, 0.28, 0.40))
    L = s.layer('alleys', 0.2)
    S = L.S
    for k, x in enumerate(np.arange(-60, s.w + 200, 300)):   # 院外的屋脊，沒有燈
        yg = H * 0.66 + (k % 2) * 30
        L.wash(S.poly([(x - 160, H), (x - 160, yg), (x + 160, yg), (x + 160, H)], rough=1), (0.24, 0.24, 0.30), density=0.9, edge=0.6)
        cn_roof(L, x, yg, 380, 70, (0.14, 0.14, 0.20), ink=False)
    L = s.layer('house', 0.42)
    S = L.S
    yg = H * 0.9
    L.wash(S.below_curve(np.full(s.w, yg, F32), 2), (0.30, 0.30, 0.34), density=0.9, edge=0.5)
    cx = s.w * 0.5
    win = courtyard_house(L, cx, yg, 520)
    L = s.layer('family', 0.42)
    S = L.S
    lamp = [cx, yg - 160]
    L.wash(S.ellipse(cx, yg - 30, 200, 26, rough=1), (0.48, 0.34, 0.26), density=0.9, edge=0.8)   # 桌
    for i, dx in enumerate([-150, -60, 60, 150]):
        figure(L, cx + dx, yg - 20, [150, 110, 120, 160][i], robe=ROBES[i], arm=0.3 if i % 2 else 0.0)
    L = s.layer('outside', 0.6)
    for x in (s.w * 0.12, s.w * 0.2, s.w * 0.84, s.w * 0.92):   # 窗外的灰影
        figure(L, x, H * 0.98, 300, robe=(0.22, 0.22, 0.28), skin=(0.26, 0.26, 0.32), ink=False)
    s.meta.update(lamps=[win], lamp=lamp)
    return s


def s2_split():
    """屋頂沒了的祠堂，人背過身去，越走越遠"""
    s = Scene(FILM, "s2_split", seed=1302, w=int(W * 1.1))
    sky_layer(s, 'grey', clouds_n=9)
    L, ys = ground_layer(s, 0.82, 16, (0.66, 0.64, 0.58), (0.58, 0.56, 0.52))
    cx = s.w * 0.5
    L = s.layer('hall', 0.45)
    hall(L, cx, H * 0.84, 360, wall=(0.76, 0.74, 0.70), pillar=(0.52, 0.30, 0.28), roofed=False, doors_open=False)
    for k in range(6):   # 柱子上的顏料往下流
        x = cx + (k - 2.5) * 70
        L.ink([(x, H * 0.84 - 300), (x + 2, H * 0.84 - 140 - k * 12)], width=4, color=(0.62, 0.36, 0.32), dark=0.5, dry=0.5)
    L = s.layer('roof', 0.45)
    cn_roof(L, cx, H * 0.84 - 360 * 0.12 - 360 * 0.62, 360 * 2.25, 360 * 0.42, (0.40, 0.36, 0.40))
    for i in range(6):
        sp = s.sprite(f'walker_{i}', 200, 300, anchor=(0.5, 0.96))
        figure(sp, 100, 288, 240, robe=tuple(0.5 * c + 0.5 * g for c, g in zip(ROBES[i], GREY)), lean=0.3 * (1 if i % 2 else -1), legs=0.5 * (i % 3 - 1), pose=0.5)
    s.meta.update(center=[cx, H * 0.9])
    return s


def s3_net():
    """沒有根的樹也能站住：一張繩網把人網在一起"""
    s = Scene(FILM, "s3_net", seed=1303)
    room(s, col=(0.80, 0.74, 0.62), glow=(W * 0.5, H * 0.5, 800))
    L = s.layer('people', 0.4)
    rng = np.random.default_rng(13)
    pts = []
    for r in range(3):
        for c in range(7):
            x = W * 0.16 + c * W * 0.113 + (r % 2) * W * 0.056 + rng.normal(0, 14)
            y = H * 0.58 + r * 150
            figure(L, x, y, 150 + r * 30, robe=ROBES[(r * 7 + c) % 6], arm=rng.uniform(0, 0.4))
            pts.append([float(x), float(y - (150 + r * 30) * 0.55)])
    edges = []
    for i, p in enumerate(pts):
        for j in range(i + 1, len(pts)):
            q = pts[j]
            if np.hypot(p[0] - q[0], p[1] - q[1]) < W * 0.14:
                edges.append([i, j])
    s.meta.update(nodes=pts, edges=edges)
    return s


def s4_lantern():
    """陌生人走上山坡，衣服漸漸染上提燈者的顏色"""
    s = Scene(FILM, "s4_lantern", seed=1304, w=int(W * 1.15))
    sky_layer(s, 'dusk', clouds_n=7)
    far_layer(s, 0.58, 140, (0.52, 0.50, 0.66))
    L = s.layer('hill', 0.45)
    S = L.S
    xs = np.arange(s.w, dtype=F32)
    ys = H * 0.92 - (H * 0.36) * np.clip(xs / (s.w * 0.78), 0, 1) ** 1.3 + 10 * noise1d(s.w, 8, L.rng)
    ys[xs > s.w * 0.78] = ys[int(s.w * 0.78)]
    L.wash(S.below_curve(ys, 2), (0.50, 0.50, 0.40), density=0.9, edge=0.8, gran=0.6)
    ridge_ink(L, ys, 2.0, gap=0.2)
    field_strokes(L, ys, H, None, n=500, h=(14, 34))
    for x in (s.w * 0.08, s.w * 0.3, s.w * 0.52, s.w * 0.9):
        tree_round(L, x, float(ys[int(min(x, s.w - 1))]) + 30, 200, green=(0.42, 0.50, 0.34))
    top = [s.w * 0.8, float(ys[int(s.w * 0.8)])]
    figure(L, top[0], top[1] + 6, 230, robe=(0.82, 0.56, 0.24), arm=1.0)
    s.meta.update(path=[[float(x), float(ys[int(x)])] for x in np.arange(0, s.w * 0.8, 30)], top=[top[0] + 50, top[1] - 220])
    for p in range(4):
        ph = np.sin(p / 4 * 2 * np.pi)
        sp = s.sprite(f'grey_{p}', 200, 300, anchor=(0.5, 0.96))
        figure(sp, 100, 288, 240, robe=(0.46, 0.46, 0.52), lean=0.4, legs=ph, pose=ph)
        sp = s.sprite(f'gold_{p}', 200, 300, anchor=(0.5, 0.96))
        figure(sp, 100, 288, 240, robe=(0.82, 0.56, 0.24), lean=0.4, legs=ph, pose=ph)
    # 撕成兩半的真家族旗幟（右上遠處）
    for k, (dx, rot) in enumerate([(-40, -0.1), (40, 0.12)]):
        sp = s.sprite(f'banner_{k}', 160, 300, anchor=(0.5, 0.0))
        sp.ink([(80 - dx * 0.4, 0), (80 - dx * 0.4, 300)], width=3, color=INK_BROWN, smooth=0)
        pts = [(80, 20), (80 + (1 if k else -1) * 70, 30), (80 + (1 if k else -1) * 60, 200), (80, 180)]
        sp.wash(sp.S.poly(pts, rough=3), (0.30, 0.38, 0.58), density=0.9, edge=0.9)
    return s


def s5_rice():
    """祠堂門開，一碗飯一雙雙手傳下去"""
    s = Scene(FILM, "s5_rice", seed=1305, w=int(W * 1.1))
    sky_layer(s, 'gold', clouds_n=6)
    L, ys = ground_layer(s, 0.82, 10, (0.78, 0.70, 0.52), (0.70, 0.62, 0.48))
    L = s.layer('hall', 0.42)
    hx = s.w * 0.24
    lamp, door = hall(L, hx, H * 0.84, 300)
    L = s.layer('row', 0.42)
    hands = []
    for i in range(8):
        x = hx + 260 + i * 190
        yg = H * 0.9
        figure(L, x, yg, 200 + (i % 3) * 14, robe=ROBES[i % 6], arm=0.5, lean=-0.1)
        hands.append([float(x - 50), float(yg - 120)])
    # 一個受傷的人被抬回家
    fx_ = s.w * 0.88
    figure(L, fx_ - 60, H * 0.93, 200, robe=ROBES[2], arm=0.6)
    figure(L, fx_ + 90, H * 0.93, 200, robe=ROBES[4], arm=0.6)
    L.wash(L.S.ellipse(fx_ + 15, H * 0.93 - 110, 110, 22, rough=1), (0.86, 0.82, 0.74), density=0.9, edge=0.8)
    sp = s.sprite('bowl', 90, 70, anchor=(0.5, 0.5))
    bowl(sp, 45, 26, 34)
    sp.wash(sp.S.ellipse(45, 22, 26, 10, rough=0.6), (0.99, 0.98, 0.96), density=0.9, edge=0.7)
    s.meta.update(hands=[[door[0], door[1] - 100]] + hands, lamps=[lamp])
    return s


def s6_banyan():
    """一棵榕樹，每條氣根都是一戶人家，撐起上面的大樹冠"""
    s = Scene(FILM, "s6_banyan", seed=1306, w=int(W * 1.15))
    sky_layer(s, 'day', clouds_n=8)
    far_layer(s, 0.6, 100, (0.70, 0.76, 0.86))
    L, ys = ground_layer(s, 0.84, 14, (0.66, 0.76, 0.48), (0.56, 0.66, 0.42))
    L = s.layer('tree', 0.45)
    S = L.S
    cx = s.w * 0.5
    rng = np.random.default_rng(16)
    L.wash(S.poly([(cx - 90, H * 0.88), (cx - 50, H * 0.5), (cx - 20, H * 0.34), (cx + 30, H * 0.34), (cx + 60, H * 0.5), (cx + 110, H * 0.88)], rough=4),
           (0.42, 0.32, 0.24), density=0.95, edge=0.9, gran=0.8)
    for k in range(10):   # 氣根：從枝上垂下，落地成幹
        x = cx + (k - 4.5) * 135 + rng.normal(0, 16)
        x0 = cx + (x - cx) * 0.5
        L.ink([(x0, H * 0.38), ((x0 + x) / 2, H * 0.44), (x, H * 0.6), (x + rng.normal(0, 6), H * 0.87)], width=9 + (k % 3) * 4, color=INK_BROWN, dark=0.8)
    for k in range(4):
        L.ink([(cx, H * 0.4), (cx + (k - 1.5) * 260, H * 0.34 + abs(k - 1.5) * 20)], width=18, color=(0.40, 0.30, 0.22), dark=0.85)
    for k in range(22):
        m = S.blob(cx + rng.normal(0, 400), H * 0.27 + rng.normal(0, 50), rng.uniform(120, 200), n=7, spread=0.5, squash=0.6, rough=8)
        L.wash(m, [(0.40, 0.58, 0.32), (0.50, 0.66, 0.36), (0.34, 0.50, 0.32)][k % 3], density=0.75, edge=0.9, gran=0.6)
        canopy_contour_ink(L, m, width=1.3, frac=0.4)
    L = s.layer('homes', 0.45)
    wins = []
    for k in range(8):
        x = cx + (k - 3.5) * 150
        wins += house(L, x, H * 0.88, 110, 80, roof=[(0.66, 0.36, 0.30), (0.40, 0.42, 0.56), (0.70, 0.58, 0.36)][k % 3], windows=1, chimney=False)
    s.meta.update(lamps=[list(w) for w in wins])
    return s


def s7_wedding():
    """婚禮的桌子擺得像談判桌：兩家族徽，一條紅綢，底下壓著賬本"""
    s = Scene(FILM, "s7_wedding", seed=1307)
    room(s, col=(0.84, 0.70, 0.60), glow=(W * 0.5, H * 0.4, 700))
    L = s.layer('guests', 0.4)
    S = L.S
    crests = []
    for k, (x, col) in enumerate([(W * 0.22, (0.30, 0.40, 0.60)), (W * 0.78, (0.40, 0.56, 0.36))]):
        figure(L, x, H * 0.84, 420, robe=col, arm=0.3)
        figure(L, x + (1 if k == 0 else -1) * 170, H * 0.86, 330, robe=tuple(c * 0.8 for c in col))
        cy = H * 0.26
        L.wash(S.ellipse(x, cy, 110, 120, rough=1.5), col, density=0.9, edge=0.9)
        L.wash(S.ellipse(x, cy, 60, 64, rough=1), (0.94, 0.88, 0.70), density=0.85, edge=0.8)
        crests.append([float(x), float(cy)])
    L = s.layer('table', 0.4)
    S = L.S
    tp = [(W * 0.18, H * 0.66), (W * 0.82, H * 0.66), (W * 0.9, H * 0.86), (W * 0.1, H * 0.86)]
    L.wash(S.poly(tp, rough=1), (0.56, 0.22, 0.20), density=0.95, edge=0.9, gran=0.6)
    L.ink(tp + [tp[0]], width=2.2, smooth=0)
    for k, x in enumerate([W * 0.4, W * 0.56]):   # 賬本
        L.wash(S.poly([(x - 80, H * 0.72), (x + 80, H * 0.72), (x + 90, H * 0.8), (x - 70, H * 0.8)], rough=0.6), (0.92, 0.86, 0.70), density=0.9, edge=0.8)
        for j in range(4):
            L.ink([(x - 60, H * 0.735 + j * 14), (x + 60, H * 0.735 + j * 14)], width=1.0, dark=0.5, smooth=0)
    s.meta.update(crests=crests)
    return s


def s8_soil():
    """一粒種子落向三種土：石、沙、園；搖籃上方是祖父的畫像"""
    s = Scene(FILM, "s8_soil", seed=1308)
    sky_layer(s, 'dawn', clouds_n=5)
    L = s.layer('soils', 0.4)
    S = L.S
    yg = H * 0.74
    cols = [((0.56, 0.56, 0.60), 'rock'), ((0.90, 0.80, 0.58), 'sand'), ((0.40, 0.30, 0.22), 'garden')]
    spots = []
    for k, (c, kind) in enumerate(cols):
        x0, x1 = W * (0.06 + k * 0.31), W * (0.33 + k * 0.31)
        L.wash(S.poly([(x0, yg), (x1, yg), (x1 - 20, H * 0.98), (x0 + 20, H * 0.98)], rough=4), c, density=0.9, edge=0.8, gran=0.8)
        if kind == 'rock':
            for j in range(6):
                L.ink([(x0 + 40 + j * 70, yg + 30), (x0 + 70 + j * 70, yg + 90)], width=1.6, dark=0.6)
        if kind == 'garden':
            for j in range(9):
                L.ink([(x0 + 30 + j * 60, yg + 2), (x0 + 30 + j * 60, yg - 30)], width=2, color=(0.30, 0.50, 0.26), dark=0.8)
        spots.append([float((x0 + x1) / 2), float(yg)])
    # 祖父畫像（右上）
    px, py = W * 0.86, H * 0.44
    L.wash(S.poly([(px - 110, py - 140), (px + 110, py - 140), (px + 110, py + 140), (px - 110, py + 140)], rough=0.6), (0.82, 0.74, 0.58), density=0.9, edge=0.8)
    L.box(px - 110, py - 140, px + 110, py + 140, width=5, color=INK_BROWN)
    figure(L, px, py + 140, 250, robe=(0.30, 0.30, 0.36), arm=0.0)
    sp = s.sprite('seed', 60, 80, anchor=(0.5, 0.5))
    sp.wash(sp.S.ellipse(30, 40, 14, 22, rough=0.6), (0.58, 0.40, 0.22), density=1.0, edge=0.9)
    sp = s.sprite('sprout', 200, 320, anchor=(0.5, 1.0))
    sp.ink([(100, 320), (98, 180), (104, 60)], width=5, color=(0.30, 0.50, 0.24), dark=0.8)
    for side in (-1, 1):
        for j, y in enumerate([200, 130, 70]):
            leaf = [(100, y), (100 + side * 70, y - 30), (100 + side * 40, y - 6)]
            sp.wash(sp.S.poly(leaf, rough=1), (0.44, 0.66, 0.32), density=0.9, edge=0.9)
    s.meta.update(spots=spots)
    return s


def s9_jar():
    """祖先留下的米缸，裂了一道縫；子孫的臉在蒸汽裡淡去"""
    s = Scene(FILM, "s9_jar", seed=1309)
    room(s, col=(0.62, 0.56, 0.54), glow=(W * 0.5, H * 0.45, 620))
    L = s.layer('jar', 0.4)
    S = L.S
    cx, cy = W * 0.5, H * 0.6
    jar = S.blob(cx, cy, 300, n=5, spread=0.15, squash=1.15, rough=3)
    L.wash(jar, (0.52, 0.36, 0.26), density=0.95, edge=0.9, gran=0.8)
    top = float(np.nonzero((jar > 0.5).any(axis=1))[0].min()) + 30
    cy = top + 330
    L.wash(S.ellipse(cx, cy - 330, 150, 34, rough=1), (0.36, 0.26, 0.20), density=0.95, edge=0.8)
    L.wash(S.ellipse(cx, cy - 326, 120, 22, rough=1), (0.96, 0.94, 0.88), density=0.85, edge=0.7)
    rows = np.nonzero((jar > 0.5).any(axis=1))[0]
    for k in range(4):
        yy = rows.min() + (rows.max() - rows.min()) * (0.2 + 0.2 * k)
        xs_ = np.nonzero(jar[int(yy)] > 0.5)[0]
        L.ink([(xs_.min() + 14, yy), (xs_.max() - 14, yy)], width=2, dark=0.4, dry=0.6)
    crack = [(cx + 120, cy - 120), (cx + 140, cy - 40), (cx + 120, cy + 40), (cx + 150, cy + 140)]
    L.ink(crack, width=3, dark=0.95, smooth=0)
    L.wash(S.below_curve(np.full(W, H * 0.92, F32), 1), (0.40, 0.32, 0.30), density=0.8)
    for k in range(3):   # 子孫的臉
        sp = s.sprite(f'face_{k}', 180, 200, anchor=(0.5, 0.5))
        sp.wash(sp.S.ellipse(90, 100, 60, 76, rough=1), (0.94, 0.84, 0.74), density=0.6, edge=0.6, bloom=6)
        sp.ink([(66, 92), (74, 92)], width=3, dark=0.6); sp.ink([(106, 92), (114, 92)], width=3, dark=0.6)
        sp.ink([(76, 130), (90, 136), (104, 130)], width=2, dark=0.5)
    s.meta.update(leak=[cx + 150, cy + 140], steam=[cx, cy - 360], crack=[[float(a), float(b)] for a, b in crack])
    return s


def s10_generations():
    """四代人四層顏色：老人種下的樹第四代才有樹蔭；雪中地主的院子像雪花的凝結核"""
    s = Scene(FILM, "s10_generations", seed=1310, w=int(W * 1.3))
    sky_layer(s, 'grey', clouds_n=6)
    far_layer(s, 0.6, 90, (0.74, 0.76, 0.84), snow=True)
    L, ys = ground_layer(s, 0.82, 16, (0.86, 0.88, 0.90), (0.78, 0.80, 0.86))
    gens = []
    for k in range(4):
        x = s.w * (0.14 + k * 0.22)
        yg = gy(ys, x) + 40
        L.wash(L.S.poly([(x - s.w * 0.11, yg + 10), (x + s.w * 0.11, yg + 10), (x + s.w * 0.11, H), (x - s.w * 0.11, H)], rough=3),
               [(0.84, 0.80, 0.70), (0.78, 0.82, 0.70), (0.70, 0.80, 0.66), (0.62, 0.76, 0.60)][k], density=0.6, edge=0.6)
        if k == 0:
            seedling(L, x, yg, 70)
        else:
            tree_round(L, x, yg, 160 + k * 140, green=(0.40, 0.56, 0.36))
        figure(L, x + 140 + k * 30, yg + 20, 200, robe=ROBES[k], arm=0.3 if k == 0 else 0.0, lean=0.3 if k == 0 else 0.0)
        gens.append([float(x), float(yg)])
    # 雪中的院落群：中心一座大院，四周小屋
    hx = s.w * 0.84
    L = s.layer('estate', 0.45)
    wins = house(L, hx, gy(ys, hx) + 60, 260, 150, roof=(0.40, 0.38, 0.46), windows=3, chimney=True)
    s.meta.update(gens=gens, lamps=[list(w) for w in wins])
    return s


def s11_backstage():
    """從後台看舞台：台前的父親意氣風發，後台的小孩什麼都看見了"""
    s = Scene(FILM, "s11_backstage", seed=1311)
    room(s, col=(0.30, 0.26, 0.32))
    L = s.layer('stage', 0.3)
    S = L.S
    L.wash(S.poly([(W * 0.38, H * 0.1), (W * 1.0, H * 0.1), (W * 1.0, H * 0.8), (W * 0.38, H * 0.8)], rough=1), (0.92, 0.74, 0.46), density=0.85, edge=0.8, bloom=20)
    L.wash(S.poly([(W * 0.38, H * 0.8), (W * 1.0, H * 0.8), (W * 1.0, H * 0.9), (W * 0.38, H * 0.9)], rough=1), (0.52, 0.34, 0.24), density=0.95, edge=0.8)
    for k in range(5):   # 台下觀眾的剪影
        figure(L, W * 0.48 + k * 110, H * 1.04, 200, robe=(0.18, 0.16, 0.20), skin=(0.20, 0.18, 0.22), ink=False)
    L = s.layer('actor', 0.32)
    figure(L, W * 0.72, H * 0.8, 380, robe=(0.72, 0.30, 0.26), arm=1.0)
    L = s.layer('wings', 0.5)
    S = L.S
    L.wash(S.poly([(0, 0), (W * 0.38, 0), (W * 0.4, H), (0, H)], rough=2), (0.22, 0.12, 0.14), density=0.95, edge=0.6)
    for k in range(6):
        L.ink([(W * (0.30 + k * 0.015), 0), (W * (0.31 + k * 0.016), H)], width=6, color=(0.40, 0.14, 0.16), dark=0.6, dry=0.3)
    # 後台：父親換下面具，桌上酒瓶；小孩在旁邊看
    figure(L, W * 0.2, H * 0.9, 360, robe=(0.34, 0.30, 0.34), arm=0.2, lean=0.3)
    L.wash(S.ellipse(W * 0.26, H * 0.62, 40, 50, rough=0.6), (0.96, 0.90, 0.80), density=0.85, edge=0.8)
    figure(L, W * 0.09, H * 0.92, 170, robe=(0.76, 0.62, 0.34), arm=0.0)
    s.meta.update(child=[W * 0.09, H * 0.92 - 150], spot=[W * 0.72, H * 0.2])
    return s


def s12_rebuild():
    """題山磨坊：孩子們圍著試卷堆；最後一盞盞小屋的燈圍著重修的祠堂亮起"""
    s = Scene(FILM, "s12_rebuild", seed=1312, w=int(W * 1.25))
    sky_layer(s, 'dusk', clouds_n=7)
    far_layer(s, 0.6, 120, (0.56, 0.54, 0.70))
    L, ys = ground_layer(s, 0.78, 26, (0.56, 0.60, 0.44), (0.48, 0.52, 0.40))
    # 左：試卷山和埋頭的孩子
    px = s.w * 0.2
    L2 = s.layer('papers', 0.45)
    S = L2.S
    L2.wash(S.poly([(px - 300, H * 0.86), (px - 60, H * 0.36), (px + 40, H * 0.34), (px + 300, H * 0.86)], rough=6), (0.94, 0.92, 0.86), density=0.85, edge=0.8, gran=0.6)
    rng = np.random.default_rng(112)
    for k in range(40):
        y = rng.uniform(H * 0.42, H * 0.84)
        half = (y - H * 0.34) / (H * 0.52) * 280
        x = px + rng.uniform(-half, half)
        L2.ink([(x - 30, y), (x + 30, y + rng.uniform(-4, 4))], width=1.2, dark=0.5, smooth=0)
    for k in range(6):
        x = px - 340 + k * 140
        figure(L2, x, H * 0.92, 130, robe=(0.50, 0.50, 0.56), lean=0.8, arm=0.6)
    # 右：重修的祠堂和四周的小屋
    hx = s.w * 0.68
    L3 = s.layer('village', 0.45)
    lamp, door = hall(L3, hx, gy(ys, hx) + 60, 260)
    wins = []
    for k, (dx, dy) in enumerate([(-520, 30), (-360, 70), (360, 70), (520, 30), (-660, 90), (660, 90), (-200, 110), (220, 110)]):
        x = hx + dx
        wins += house(L3, x, gy(ys, x) + 60 + dy, 120, 80, roof=[(0.62, 0.34, 0.30), (0.40, 0.42, 0.56), (0.66, 0.56, 0.36)][k % 3], windows=1, chimney=k % 2 == 0)
    wins.sort(key=lambda w: abs(w[0] - hx))
    s.meta.update(lamps=[lamp] + [list(w) for w in wins])
    fg_layer(s, grass=300)
    return s


ALL = [s1_courtyard, s2_split, s3_net, s4_lantern, s5_rice, s6_banyan, s7_wedding, s8_soil, s9_jar, s10_generations, s11_backstage, s12_rebuild]
