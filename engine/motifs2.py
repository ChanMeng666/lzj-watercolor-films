"""第二批母題：地圖、人群方陣、工廠、古代神廟、船、驢與磨、毛蟲與蝴蝶、羊與狼、望樓、特許狀、孤島、雜草……"""
import numpy as np
import cv2
from wc import blur, lblur, fbm, noise1d, F32
from motifs import *


# ---------------------------------------------------------------- 水彩地圖（虛構的地形，不對應現實國界）
def painted_map(L, n=14, palette=None, seed=3, sea=(0.72, 0.82, 0.90), land=(0.92, 0.86, 0.70), single=None,
                coast_ink=1.8, border_ink=1.3, region_tmap=None):
    """俯視的水彩地圖：海、海岸線、若干政體。回傳 (陸地遮罩, [(cx,cy,mask)...])
    single: 只上一種顏色（帝國版本）。region_tmap: 依區域寫入時間值，供逐區顯影。"""
    S, rng = L.S, np.random.default_rng(seed)
    H, W = L.h, L.w
    L.wash(np.ones((H, W), F32), sea, density=0.75, edge=0, gran=0.3)
    lm = fbm(H, W, 3, rng, 5, 0.5)
    yy, xx = np.mgrid[0:H, 0:W].astype(F32)
    fall = 1 - np.clip(((xx - W * 0.5) / (W * 0.55)) ** 2 + ((yy - H * 0.5) / (H * 0.6)) ** 2, 0, 1)
    landm = np.clip(((lm * 0.55 + fall * 0.75) - 0.62) * 25, 0, 1).astype(F32)
    landm = blur(landm, 1.2)
    L.wash(landm, land, density=0.8, edge=0.8, gran=0.5)
    # 海岸淺水
    L.wash(np.clip(blur(landm, 18) - landm, 0, 1) * 1.6, (0.60, 0.76, 0.86), density=0.5, edge=0, occlude=False)
    # 政體：隨機種子點的 Voronoi，邊界扭曲
    pts = []
    while len(pts) < n:
        x, y = rng.uniform(0.1, 0.9) * W, rng.uniform(0.1, 0.9) * H
        if landm[int(y), int(x)] > 0.5:
            pts.append((x, y))
    d = np.stack([(xx - x) ** 2 + (yy - y) ** 2 for x, y in pts])
    dx, dy = S.disp(90)
    d = np.stack([((xx + dx * 40) - x) ** 2 + ((yy + dy * 40) - y) ** 2 for x, y in pts])
    lab = d.argmin(0)
    pal = palette or [(0.90, 0.66, 0.56), (0.70, 0.80, 0.62), (0.94, 0.84, 0.56), (0.70, 0.74, 0.88), (0.86, 0.70, 0.80),
                      (0.78, 0.86, 0.80), (0.92, 0.76, 0.62), (0.80, 0.74, 0.62)]
    regions = []
    for i, (x, y) in enumerate(pts):
        m = ((lab == i).astype(F32) * landm)
        m = lblur(m, 1.0)
        c = single or pal[i % len(pal)]
        L.wash(m * 0.95, c, density=0.6 if single is None else 0.75, edge=0.9, gran=0.5, bloom=2)
        regions.append((x, y, m))
        if region_tmap is not None:
            np.minimum(region_tmap, np.where(m > 0.2, rng.uniform(0.05, 0.85), 9.0).astype(F32), out=region_tmap)
    # 墨線：海岸 + 邊界
    cs, _ = cv2.findContours((landm > 0.5).astype(np.uint8), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    for c in cs:
        c = c[:, 0, :].astype(F32)
        if len(c) > 30:
            for k in range(0, len(c), 220):
                L.ink(c[k:k + 230:3], width=coast_ink, dark=0.75, dry=0.3)
    if single is None and border_ink:
        edges = (cv2.Laplacian(lab.astype(np.float32), cv2.CV_32F) != 0) & (landm > 0.6)
        es = cv2.dilate(edges.astype(np.uint8), np.ones((2, 2), np.uint8))
        bc, _ = cv2.findContours(es, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
        for c in bc:
            c = c[:, 0, :].astype(F32)
            if len(c) > 20:
                for k in range(0, len(c) // 2, 160):
                    L.ink(c[k:k + 170:4], width=border_ink, dark=0.55, dry=0.5, color=INK_BROWN)
    return landm, regions


def mountains_icon(L, x, y, s):
    """地圖上的小山符號"""
    for k in range(3):
        cx = x + (k - 1) * s * 0.7
        pts = [(cx - s * 0.5, y), (cx, y - s * (0.8 + 0.2 * (k == 1))), (cx + s * 0.5, y)]
        L.wash(L.S.poly(pts, rough=0.8), (0.62, 0.56, 0.50), density=0.6, edge=0.7)
        L.ink(pts, width=1.4, dark=0.7, smooth=0)


# ---------------------------------------------------------------- 人群
def crowd_grid(L, x0, y0, cols, rows, dx, dy, h, robe=(0.58, 0.56, 0.58), perspective=0.0, ink=True, rng=None):
    """一模一樣的人排成方陣（編戶齊民）"""
    pos = []
    for r in range(rows):
        sc = 1 + perspective * r
        for c in range(cols):
            x = x0 + (c - (cols - 1) / 2) * dx * sc
            y = y0 + r * dy * sc
            figure(L, x, y, h * sc, robe=robe, arm=0.0, ink=ink)
            pos.append((x, y, h * sc))
    return pos


def villagers(L, pts, h, rng, ink=True):
    robes = [(0.70, 0.34, 0.30), (0.30, 0.42, 0.62), (0.76, 0.62, 0.34), (0.40, 0.54, 0.40), (0.56, 0.38, 0.56), (0.80, 0.50, 0.36)]
    for i, (x, y) in enumerate(pts):
        figure(L, x, y, h * rng.uniform(0.9, 1.1), robe=robes[i % len(robes)], arm=rng.uniform(0, 0.6),
               lean=rng.uniform(-0.2, 0.2), ink=ink)


# ---------------------------------------------------------------- 建築
def factory(L, x, yg, s, ink=True):
    """鋸齒屋頂廠房 + 煙囪；回傳煙囪頂"""
    S = L.S
    w = s * 2.4
    L.wash(S.poly([(x - w / 2, yg), (x - w / 2, yg - s * 0.5), (x + w / 2, yg - s * 0.5), (x + w / 2, yg)], rough=1),
           (0.66, 0.50, 0.44), density=0.85, edge=0.6, gran=0.6)
    teeth = []
    for k in range(5):
        a = x - w / 2 + k * w / 5
        teeth += [(a, yg - s * 0.5), (a + w / 5 * 0.75, yg - s * 0.78), (a + w / 5, yg - s * 0.5)]
    L.wash(S.poly(teeth + [(x + w / 2, yg - s * 0.48), (x - w / 2, yg - s * 0.48)], rough=1), (0.48, 0.44, 0.48), density=0.9)
    tops = []
    for k, (cx, hh) in enumerate([(x - w * 0.3, 1.5), (x + w * 0.05, 1.8), (x + w * 0.35, 1.3)]):
        pts = [(cx - s * 0.07, yg - s * 0.5), (cx - s * 0.05, yg - s * hh), (cx + s * 0.05, yg - s * hh), (cx + s * 0.07, yg - s * 0.5)]
        L.wash(S.poly(pts, rough=0.6), (0.56, 0.36, 0.32), density=0.9, edge=0.6)
        if ink:
            L.ink([pts[0], pts[1]], width=1.4, smooth=0); L.ink([pts[2], pts[3]], width=1.4, smooth=0)
        tops.append([cx, yg - s * hh])
    for k in range(8):
        wx = x - w / 2 + (k + 0.5) * w / 8
        L.wash(S.poly([(wx - s * 0.06, yg - s * 0.35), (wx + s * 0.06, yg - s * 0.35), (wx + s * 0.06, yg - s * 0.15),
                       (wx - s * 0.06, yg - s * 0.15)], rough=0.4), (0.30, 0.30, 0.36), density=0.9)
    if ink:
        L.ink(teeth, width=1.6, dark=0.8, smooth=0)
        L.box(x - w / 2, yg - s * 0.5, x + w / 2, yg, width=1.6, dark=0.75)
    return tops


def ziggurat(L, x, yg, s, ink=True):
    S = L.S
    for k in range(4):
        ww = s * (1.6 - 0.35 * k); hh = s * 0.22
        y1 = yg - k * hh
        pts = [(x - ww / 2, y1), (x - ww / 2 + s * 0.05, y1 - hh), (x + ww / 2 - s * 0.05, y1 - hh), (x + ww / 2, y1)]
        L.wash(S.poly(pts, rough=1), (0.86, 0.72, 0.52), density=0.85, edge=0.7, gran=0.7)
        L.wash(S.poly([(x + ww * 0.15, y1), (x + ww * 0.15, y1 - hh), pts[2], pts[3]], rough=0.6), (0.72, 0.56, 0.42), density=0.5)
        if ink:
            L.ink(pts, width=1.6, dark=0.75, smooth=0)
    L.wash(S.poly([(x - s * 0.06, yg), (x - s * 0.06, yg - s * 0.66), (x + s * 0.06, yg - s * 0.66), (x + s * 0.06, yg)], rough=0.5),
           (0.74, 0.60, 0.44), density=0.7)


def pyramid(L, x, yg, s, ink=True):
    S = L.S
    pts = [(x - s, yg), (x, yg - s * 0.95), (x + s, yg)]
    L.wash(S.poly(pts, rough=1), (0.92, 0.80, 0.56), density=0.85, edge=0.7, gran=0.7)
    L.wash(S.poly([(x, yg - s * 0.95), (x + s, yg), (x + s * 0.15, yg)], rough=1), (0.76, 0.60, 0.44), density=0.6)
    if ink:
        L.ink(pts, width=1.8, dark=0.8, smooth=0)
        L.ink([(x, yg - s * 0.95), (x + s * 0.15, yg)], width=1.4, dark=0.6, smooth=0)


def temple(L, x, yg, s, ink=True, col=(0.95, 0.92, 0.86)):
    """希臘式神廟：台階 + 柱廊 + 山花"""
    S = L.S
    w = s * 1.6
    for k in range(3):
        L.wash(S.poly([(x - w / 2 - (3 - k) * 6, yg - k * 8), (x - w / 2 - (3 - k) * 6, yg - k * 8 - 8),
                       (x + w / 2 + (3 - k) * 6, yg - k * 8 - 8), (x + w / 2 + (3 - k) * 6, yg - k * 8)], rough=0.5), col, density=0.6, edge=0.7)
    top = yg - 24 - s * 0.7
    n = 6
    for k in range(n):
        cx = x - w / 2 + w * (k + 0.5) / n
        L.wash(S.poly([(cx - s * 0.05, yg - 24), (cx - s * 0.045, top), (cx + s * 0.045, top), (cx + s * 0.05, yg - 24)], rough=0.4),
               col, density=0.6, edge=0.8)
        L.wash(S.poly([(cx + s * 0.01, yg - 24), (cx + s * 0.01, top), (cx + s * 0.045, top), (cx + s * 0.05, yg - 24)], rough=0.3),
               (0.70, 0.70, 0.76), density=0.5)
        if ink:
            L.ink([(cx - s * 0.05, yg - 24), (cx - s * 0.045, top)], width=1.2, smooth=0, dark=0.6)
            L.ink([(cx + s * 0.05, yg - 24), (cx + s * 0.045, top)], width=1.2, smooth=0, dark=0.6)
    L.wash(S.poly([(x - w / 2 - 8, top), (x + w / 2 + 8, top), (x + w / 2 + 8, top - s * 0.1), (x - w / 2 - 8, top - s * 0.1)], rough=0.5),
           col, density=0.7, edge=0.7)
    ped = [(x - w / 2 - 14, top - s * 0.1), (x, top - s * 0.42), (x + w / 2 + 14, top - s * 0.1)]
    L.wash(S.poly(ped, rough=0.6), col, density=0.7, edge=0.8)
    if ink:
        L.ink(ped + [ped[0]], width=1.6, smooth=0, dark=0.8)
        L.box(x - w / 2 - 8, top - s * 0.1, x + w / 2 + 8, top, width=1.4, dark=0.7)


def watchtower(L, x, yg, s, lit=False):
    """木製望樓；回傳燈位"""
    S = L.S
    for side in (-1, 1):
        L.ink([(x + side * s * 0.3, yg), (x + side * s * 0.18, yg - s)], width=max(2, s * 0.035), color=INK_BROWN, smooth=0)
    for k in range(3):
        y = yg - s * (0.25 + 0.25 * k)
        L.ink([(x - s * 0.28 + k * s * 0.03, y), (x + s * 0.28 - k * s * 0.03, y - s * 0.2)], width=max(1.5, s * 0.02),
              color=INK_BROWN, smooth=0, dark=0.7)
    hut = [(x - s * 0.28, yg - s), (x - s * 0.28, yg - s * 1.28), (x + s * 0.28, yg - s * 1.28), (x + s * 0.28, yg - s)]
    L.wash(S.poly(hut, rough=0.6), (0.62, 0.48, 0.36), density=0.9, edge=0.7)
    roof = [(x - s * 0.38, yg - s * 1.26), (x, yg - s * 1.55), (x + s * 0.38, yg - s * 1.26)]
    L.wash(S.poly(roof, rough=0.6), (0.50, 0.36, 0.30), density=0.9, edge=0.8)
    L.ink(roof, width=1.6, smooth=0); L.box(hut[0][0], hut[1][1], hut[2][0], hut[0][1], width=1.4)
    L.wash(S.poly([(x - s * 0.1, yg - s * 1.06), (x + s * 0.1, yg - s * 1.06), (x + s * 0.1, yg - s * 1.2),
                   (x - s * 0.1, yg - s * 1.2)], rough=0.3), (0.95, 0.80, 0.45) if lit else (0.30, 0.28, 0.32), density=0.9)
    return [x, yg - s * 1.13, s * 0.2]


def palisade(L, x0, x1, yg, h):
    rng = L.rng
    for x in np.arange(x0, x1, h * 0.16):
        hh = h * rng.uniform(0.9, 1.05)
        pts = [(x - h * 0.06, yg), (x - h * 0.06, yg - hh), (x, yg - hh - h * 0.12), (x + h * 0.06, yg - hh), (x + h * 0.06, yg)]
        L.wash(L.S.poly(pts, rough=0.6), (0.60, 0.46, 0.34), density=0.9, edge=0.7)
        L.ink(pts, width=1.3, smooth=0, dark=0.7)


def ship(L, x, yg, s, sails=(0.95, 0.92, 0.84)):
    """三桅帆船"""
    S = L.S
    hull = [(x - s, yg - s * 0.3), (x + s * 1.1, yg - s * 0.36), (x + s * 0.85, yg + s * 0.05), (x - s * 0.8, yg + s * 0.05)]
    L.wash(S.poly(hull, rough=1), (0.46, 0.32, 0.24), density=0.9, edge=0.8)
    L.ink(hull + [hull[0]], width=max(1.4, s * 0.02), smooth=0)
    for k, (mx, mh) in enumerate([(-0.5, 1.4), (0.1, 1.8), (0.65, 1.3)]):
        bx = x + mx * s
        L.ink([(bx, yg - s * 0.32), (bx, yg - s * mh)], width=max(1.4, s * 0.02), smooth=0)
        for j in range(2):
            t = yg - s * (0.45 + j * (mh - 0.5) / 2)
            b = t - s * (mh - 0.55) / 2.2
            sp = [(bx - s * 0.3, b), (bx + s * 0.3, b), (bx + s * 0.34, t), (bx - s * 0.34, t)]
            L.wash(S.poly(sp, rough=0.8), sails, density=0.55, edge=0.8)
            L.ink(sp + [sp[0]], width=1.0, dark=0.5, smooth=1)


def island(L, x, y, s, volcano=True):
    S = L.S
    m = S.blob(x, y, s, n=7, spread=1.0, squash=0.35, rough=s * 0.06)
    L.wash(m, (0.82, 0.78, 0.56), density=0.8, edge=0.8)
    if volcano:
        pts = [(x - s * 0.5, y - s * 0.05), (x - s * 0.1, y - s * 0.6), (x + s * 0.12, y - s * 0.6), (x + s * 0.55, y - s * 0.05)]
        L.wash(S.poly(pts, rough=1), (0.58, 0.52, 0.48), density=0.85, edge=0.8)
        L.ink(pts, width=1.6, smooth=0)
        return [x, y - s * 0.62]
    tree_round(L, x, y - s * 0.05, s * 0.6)
    return [x, y - s * 0.6]


# ---------------------------------------------------------------- 動物
def donkey(L, x, yg, s, phase=0.0, col=(0.60, 0.58, 0.60)):
    S = L.S
    by0, by1 = yg - s * 0.8, yg - s * 0.42
    body = [(x - s * 0.5, by0 + s * 0.05), (x + s * 0.32, by0), (x + s * 0.5, by0 - s * 0.12), (x + s * 0.62, by0 - s * 0.05),
            (x + s * 0.75, by0 + s * 0.12), (x + s * 0.66, by0 + s * 0.2), (x + s * 0.48, by0 + s * 0.14), (x + s * 0.42, by1),
            (x - s * 0.45, by1), (x - s * 0.56, by0 + s * 0.15)]
    L.wash(S.poly(body, rough=s * 0.01, scale=12), col, density=0.9, edge=0.8, gran=0.5)
    L.wash(S.poly(body, rough=0.5) * S.vgrad(by0, by1), (0.42, 0.40, 0.44), density=0.4)
    lw = max(1.5, s * 0.04)
    for lx, ph in [(-0.38, 0.0), (-0.28, 0.5), (0.28, 0.25), (0.38, 0.75)]:
        sw = np.sin((phase + ph) * 2 * np.pi) * s * 0.1
        L.ink([(x + s * lx, by1 - 4), (x + s * lx + sw * 0.5, yg - s * 0.2), (x + s * lx + sw, yg)], width=lw, smooth=1, taper=(0.05, 0.02))
    for e in (0, 1):  # 長耳朵
        L.ink([(x + s * (0.55 + 0.05 * e), by0 - s * 0.08), (x + s * (0.5 + 0.08 * e), by0 - s * 0.38)], width=lw * 1.4, dark=0.8)
    L.ink([(x - s * 0.55, by0 + s * 0.1), (x - s * 0.66, by0 + s * 0.35)], width=lw, dark=0.7)
    L.ink(body + [body[0]], width=lw * 0.5, dark=0.6, smooth=1)
    L.wash(S.ellipse(x + s * 0.68, by0 + s * 0.02, s * 0.025, s * 0.025, rough=0.2), (0.15, 0.12, 0.12), density=1.0)


def sheep(L, x, yg, s, col=(0.96, 0.95, 0.90)):
    S = L.S
    m = S.blob(x, yg - s * 0.5, s * 0.42, n=8, spread=0.6, squash=0.65, rough=s * 0.04)
    L.wash(m, col, density=0.5, edge=0.9, gran=0.4)
    L.wash(m * S.vgrad(yg - s * 0.7, yg - s * 0.2), (0.78, 0.78, 0.82), density=0.5)
    L.wash(S.ellipse(x + s * 0.42, yg - s * 0.55, s * 0.12, s * 0.09, rough=0.3), (0.30, 0.28, 0.30), density=0.9)
    for lx in (-0.22, -0.1, 0.12, 0.24):
        L.ink([(x + s * lx, yg - s * 0.25), (x + s * lx, yg)], width=max(1.2, s * 0.04), smooth=0, taper=(0.02, 0.02))
    canopy_contour_ink(L, m, width=1.0, frac=0.5)


def wolf(L, x, yg, s, col=(0.42, 0.40, 0.44)):
    S = L.S
    by0, by1 = yg - s * 0.7, yg - s * 0.4
    body = [(x - s * 0.5, by0 + s * 0.06), (x + s * 0.3, by0), (x + s * 0.48, by0 - s * 0.1), (x + s * 0.58, by0 - s * 0.16),
            (x + s * 0.62, by0 - s * 0.05), (x + s * 0.82, by0 + s * 0.04), (x + s * 0.6, by0 + s * 0.12), (x + s * 0.38, by1),
            (x - s * 0.45, by1), (x - s * 0.82, by0 + s * 0.2), (x - s * 0.58, by0 + s * 0.08)]
    L.wash(S.poly(body, rough=s * 0.012, scale=10), col, density=0.92, edge=0.8, gran=0.5)
    lw = max(1.4, s * 0.04)
    for lx in (-0.36, -0.26, 0.26, 0.34):
        L.ink([(x + s * lx, by1 - 3), (x + s * lx + s * 0.03, yg)], width=lw, smooth=0, taper=(0.03, 0.03))
    L.ink(body + [body[0]], width=lw * 0.5, dark=0.65, smooth=1)
    L.ink([(x + s * 0.5, by0 - s * 0.12), (x + s * 0.53, by0 - s * 0.3), (x + s * 0.58, by0 - s * 0.14)], width=lw * 0.8, smooth=0)


def caterpillar(L, x, y, s, col=(0.56, 0.72, 0.34)):
    S = L.S
    for k in range(7):
        cx = x - k * s * 0.22
        cy = y - abs(np.sin(k * 0.9)) * s * 0.12
        m = S.ellipse(cx, cy, s * 0.14, s * 0.13, rough=0.3)
        L.wash(m, col, density=0.85, edge=0.9)
        L.ink([(cx - s * 0.03, cy + s * 0.12), (cx - s * 0.05, cy + s * 0.2)], width=1.2, smooth=0)
    L.wash(S.ellipse(x + s * 0.08, y - s * 0.04, s * 0.15, s * 0.15, rough=0.3), (0.40, 0.56, 0.30), density=0.9, edge=0.9)
    L.ink([(x + s * 0.1, y - s * 0.18), (x + s * 0.16, y - s * 0.32)], width=1.3)


def butterfly(L, x, y, s, open_=1.0, c1=(0.95, 0.66, 0.32), c2=(0.30, 0.42, 0.66)):
    S = L.S
    for side in (-1, 1):
        wx = s * (0.2 + 0.8 * open_)
        up = [(x, y), (x + side * wx * 0.9, y - s * 0.9), (x + side * wx * 1.1, y - s * 0.4), (x + side * wx * 0.5, y)]
        lo = [(x, y), (x + side * wx * 0.7, y + s * 0.15), (x + side * wx * 0.6, y + s * 0.6), (x + side * wx * 0.15, y + s * 0.4)]
        L.wash(S.poly(up, rough=1), c1, density=0.85, edge=0.9)
        L.wash(S.poly(lo, rough=1), c2, density=0.8, edge=0.9)
        L.ink(up, width=1.2, dark=0.7, smooth=2); L.ink(lo, width=1.2, dark=0.7, smooth=2)
        L.ink([(x, y - s * 0.3), (x + side * s * 0.25, y - s * 0.75)], width=1.0, dark=0.6)
    L.ink([(x, y - s * 0.3), (x, y + s * 0.45)], width=max(2, s * 0.08), dark=0.9)


def boomerang(L, cx, cy, s, ang=0.0):
    S = L.S
    pts = []
    for t in np.linspace(-1, 1, 15):
        a = ang + t * 1.1
        r = s * (1 - 0.15 * abs(t))
        pts.append((cx + np.cos(a) * r, cy + np.sin(a) * r * 0.9))
    poly = np.concatenate([np.array(pts), (np.array(pts[::-1]) - [cx, cy]) * 0.7 + [cx, cy]])
    L.wash(S.poly(poly, rough=0.6), (0.72, 0.50, 0.32), density=0.9, edge=0.9)
    L.ink(poly, width=1.5, dark=0.8, smooth=1)


# ---------------------------------------------------------------- 物件
def charter(L, x, y, w, h, seal=True, lines=7):
    """羊皮紙特許狀 + 朱紅封蠟"""
    S = L.S
    pts = [(x - w / 2, y - h / 2), (x + w / 2, y - h / 2 + 4), (x + w / 2 - 4, y + h / 2), (x - w / 2 + 3, y + h / 2 - 3)]
    L.wash(S.poly(pts, rough=2), (0.95, 0.88, 0.72), density=0.8, edge=0.9, gran=0.6)
    L.ink(pts + [pts[0]], width=1.5, dark=0.7, smooth=0)
    for k in range(lines):
        yy = y - h / 2 + h * (0.15 + 0.6 * k / lines)
        L.ink([(x - w * 0.38, yy), (x + w * L.rng.uniform(0.2, 0.38), yy)], width=1.1, dark=0.5, tremor=1.5, dry=0.3)
    if seal:
        sx, sy = x + w * 0.25, y + h * 0.33
        L.ink([(sx - 10, y + h / 2 - 6), (sx - 18, y + h / 2 + 50)], width=3, color=(0.60, 0.20, 0.16), dark=0.8)
        L.wash(S.blob(sx, sy, w * 0.07, n=6, spread=0.3, rough=2), (0.72, 0.18, 0.14), density=1.0, edge=0.9)
        return [sx, sy]
    return [x, y]


def millstone(L, x, y, r):
    S = L.S
    m = S.ellipse(x, y, r, r * 0.38, rough=1.5)
    L.wash(m, (0.66, 0.64, 0.66), density=0.85, edge=0.8, gran=0.8)
    L.wash(S.poly([(x - r, y), (x - r, y + r * 0.25), (x + r, y + r * 0.25), (x + r, y)], rough=1) , (0.52, 0.50, 0.54), density=0.85, edge=0.7)
    L.wash(S.ellipse(x, y + r * 0.25, r, r * 0.38, rough=1.5) * S.vgrad(y + r * 0.2, y + r * 0.6), (0.52, 0.50, 0.54), density=0.85, edge=0.6)
    a = np.linspace(0, 2 * np.pi, 40)
    L.ink([(x + np.cos(t) * r, y + np.sin(t) * r * 0.38) for t in a], width=1.6, dark=0.75)
    L.ink([(x - r, y), (x - r, y + r * 0.25)], width=1.6, smooth=0); L.ink([(x + r, y), (x + r, y + r * 0.25)], width=1.6, smooth=0)
    L.ink([(x, y), (x, y - r * 0.8)], width=4, color=INK_BROWN)


def weeds(L, ys_top, y_bot, n, col=(0.40, 0.56, 0.28), tmap=None, t0=0.0, rng=None, h=(30, 70)):
    rng = rng or L.rng
    for _ in range(n):
        x = rng.uniform(0, L.w)
        y = rng.uniform(ys_top[int(x)] + 10, y_bot)
        hh = rng.uniform(*h)
        for k in range(4):
            a = -np.pi / 2 + (k - 1.5) * 0.35 + rng.normal(0, 0.1)
            pts = [(x, y), (x + np.cos(a) * hh * 0.5, y + np.sin(a) * hh * 0.5), (x + np.cos(a) * hh, y + np.sin(a) * hh + 6)]
            L.ink(pts, width=2.0, color=col, dark=0.9)
            if tmap is not None:
                from motifs import _paint_t
                tt = t0 + rng.uniform(0, 0.6)
                _paint_t(tmap, pts, 5, tt, tt + 0.3)


def torch(L, x, y, s):
    L.ink([(x, y), (x - s * 0.08, y + s)], width=max(3, s * 0.08), color=INK_BROWN)
    L.wash(L.S.ellipse(x, y - s * 0.05, s * 0.12, s * 0.07, rough=0.4), (0.40, 0.30, 0.24), density=0.9)
    return [x, y - s * 0.1]
