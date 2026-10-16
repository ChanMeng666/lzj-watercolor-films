"""第三批母題：駱駝、戰車、青銅鼎、盔甲、青綠山水、王座石"""
import numpy as np
from wc import blur, lblur, fbm, noise1d, F32
from motifs import *
from motifs2 import *


def camel(L, x, yg, s, phase=0.0, col=(0.80, 0.66, 0.46), pack=True):
    S = L.S
    by0, by1 = yg - s * 0.85, yg - s * 0.5
    body = [(x - s * 0.45, by0 + s * 0.1), (x - s * 0.25, by0 - s * 0.12), (x - s * 0.1, by0), (x + s * 0.08, by0 - s * 0.14),
            (x + s * 0.28, by0 + s * 0.02), (x + s * 0.42, by0 + s * 0.02), (x + s * 0.55, by0 - s * 0.3), (x + s * 0.72, by0 - s * 0.32),
            (x + s * 0.74, by0 - s * 0.22), (x + s * 0.6, by0 - s * 0.18), (x + s * 0.5, by0 + s * 0.18), (x + s * 0.38, by1),
            (x - s * 0.4, by1), (x - s * 0.5, by0 + s * 0.2)]
    L.wash(S.poly(body, rough=s * 0.01, scale=12), col, density=0.9, edge=0.8, gran=0.5)
    lw = max(1.5, s * 0.035)
    for lx, ph in [(-0.32, 0.0), (-0.22, 0.5), (0.26, 0.25), (0.34, 0.75)]:
        sw = np.sin((phase + ph) * 2 * np.pi) * s * 0.1
        L.ink([(x + s * lx, by1 - 3), (x + s * lx + sw * 0.5, yg - s * 0.25), (x + s * lx + sw, yg)], width=lw, smooth=1,
              taper=(0.05, 0.02))
    L.ink(body + [body[0]], width=lw * 0.5, dark=0.6, smooth=1)
    if pack:
        for k, c in enumerate([(0.62, 0.30, 0.26), (0.30, 0.40, 0.58)]):
            px = x - s * 0.2 + k * s * 0.3
            L.wash(S.poly([(px - s * 0.12, by0 - s * 0.05), (px + s * 0.12, by0 - s * 0.05), (px + s * 0.14, by0 + s * 0.22),
                           (px - s * 0.14, by0 + s * 0.22)], rough=0.6), c, density=0.9, edge=0.7)


def chariot(L, x, yg, s, phase=0.0):
    """雙輪戰車 + 馬 + 御者"""
    S = L.S
    hx = x + s * 0.95
    by0, by1 = yg - s * 0.9, yg - s * 0.5
    body = [(hx - s * 0.45, by0 + s * 0.05), (hx + s * 0.25, by0), (hx + s * 0.42, by0 - s * 0.25), (hx + s * 0.58, by0 - s * 0.28),
            (hx + s * 0.62, by0 - s * 0.15), (hx + s * 0.45, by0 + s * 0.05), (hx + s * 0.38, by1), (hx - s * 0.4, by1),
            (hx - s * 0.52, by0 + s * 0.18)]
    L.wash(S.poly(body, rough=s * 0.01), (0.46, 0.32, 0.26), density=0.95, edge=0.8)
    L.ink(body + [body[0]], width=1.5, dark=0.65, smooth=1)
    for lx, ph in [(-0.33, 0.0), (-0.24, 0.5), (0.24, 0.25), (0.32, 0.75)]:
        sw = np.sin((phase + ph) * 2 * np.pi) * s * 0.14
        L.ink([(hx + s * lx, by1 - 3), (hx + s * lx + sw * 0.5, yg - s * 0.22), (hx + s * lx + sw, yg)],
              width=max(1.5, s * 0.035), smooth=1, taper=(0.05, 0.02))
    L.ink([(x + s * 0.1, yg - s * 0.55), (hx - s * 0.3, by0 + s * 0.2)], width=max(2, s * 0.03), color=INK_BROWN)
    box = [(x - s * 0.35, yg - s * 0.45), (x - s * 0.3, yg - s * 0.85), (x + s * 0.25, yg - s * 0.85), (x + s * 0.3, yg - s * 0.45)]
    L.wash(S.poly(box, rough=0.6), (0.70, 0.44, 0.28), density=0.9, edge=0.8)
    L.ink(box, width=1.6, smooth=0)
    figure(L, x - s * 0.02, yg - s * 0.8, s * 0.55, robe=(0.62, 0.30, 0.24), lean=0.3, arm=0.4)
    wx, wy, wr = x, yg - s * 0.32, s * 0.32
    a = np.linspace(0, 2 * np.pi, 40)
    L.ink([(wx + np.cos(t) * wr, wy + np.sin(t) * wr) for t in a], width=max(2.5, s * 0.04), color=INK_BROWN, dark=0.95)
    for k in range(4):
        t = k / 4 * np.pi + phase * np.pi / 2
        L.ink([(wx - np.cos(t) * wr, wy - np.sin(t) * wr), (wx + np.cos(t) * wr, wy + np.sin(t) * wr)], width=1.4,
              color=INK_BROWN, smooth=0)


def vessel(L, x, yg, s, crude=0.0, col=(0.48, 0.62, 0.54)):
    """青銅鼎：crude 0（精良）→ 1（粗劣）"""
    S, rng = L.S, L.rng
    r = 1.5 + crude * 9
    body = [(x - s * 0.5, yg - s * 0.75), (x + s * 0.5, yg - s * 0.75), (x + s * 0.42, yg - s * 0.3), (x + s * 0.2, yg - s * 0.18),
            (x - s * 0.2, yg - s * 0.18), (x - s * 0.42, yg - s * 0.3)]
    tone = tuple(c * (1 - 0.35 * crude) + 0.6 * 0.35 * crude for c in col)
    L.wash(S.poly(body, rough=r, scale=14), tone, density=0.95, edge=0.8, gran=0.5 + 0.5 * crude)
    for side in (-1, 1):
        L.ink([(x + side * s * 0.25, yg - s * 0.2), (x + side * s * (0.3 + 0.05 * crude), yg)], width=max(2, s * 0.06), smooth=0)
        L.ink([(x + side * s * 0.35, yg - s * 0.75), (x + side * s * 0.38, yg - s * 0.95), (x + side * s * 0.25, yg - s * 0.95),
               (x + side * s * 0.25, yg - s * 0.75)], width=max(1.5, s * 0.03), smooth=0, tremor=0.5 + 3 * crude)
    L.ink(body + [body[0]], width=max(1.4, s * 0.02), dark=0.8, smooth=0, tremor=0.6 + 3 * crude)
    n = int(14 * (1 - crude))
    for k in range(n):
        xx = x - s * 0.4 + k * s * 0.8 / max(1, n - 1)
        L.ink([(xx, yg - s * 0.62), (xx + s * 0.03, yg - s * 0.55), (xx, yg - s * 0.48)], width=1.1, dark=0.6, smooth=0)
    if crude > 0.3:
        for k in range(int(crude * 4)):
            cx = x + rng.uniform(-0.3, 0.3) * s
            L.ink([(cx, yg - s * 0.72), (cx + rng.uniform(-8, 8), yg - s * 0.55), (cx + rng.uniform(-12, 12), yg - s * 0.4)],
                  width=1.0, dark=0.7)


def armor_stand(L, x, yg, s, good=True):
    S = L.S
    L.ink([(x, yg), (x, yg - s * 1.4)], width=3, color=INK_BROWN, smooth=0)
    L.ink([(x - s * 0.3, yg), (x + s * 0.3, yg)], width=3, color=INK_BROWN, smooth=0)
    plate = [(x - s * 0.32, yg - s * 1.3), (x + s * 0.32, yg - s * 1.3), (x + s * 0.26, yg - s * 0.75), (x, yg - s * 0.66),
             (x - s * 0.26, yg - s * 0.75)]
    col = (0.70, 0.72, 0.78) if good else (0.68, 0.62, 0.54)
    L.wash(S.poly(plate, rough=0.8 if good else 4), col, density=0.9, edge=0.9)
    L.ink(plate + [plate[0]], width=1.8, smooth=0, tremor=0.6 if good else 3.0)
    if good:
        L.lift(S.ellipse(x - s * 0.1, yg - s * 1.1, s * 0.06, s * 0.14, rough=0.5), 0.6)
        for k in range(5):
            L.ink([(x - s * 0.25, yg - s * (1.2 - 0.1 * k)), (x + s * 0.25, yg - s * (1.2 - 0.1 * k))], width=1.0, dark=0.4, smooth=0)
    else:
        for k in range(4):
            L.ink([(x + L.rng.uniform(-0.2, 0.2) * s, yg - s * 1.2), (x + L.rng.uniform(-0.2, 0.2) * s, yg - s * 0.9)],
                  width=1.0, dark=0.6)
    L.wash(S.ellipse(x, yg - s * 1.5, s * 0.17, s * 0.16, rough=0.6 if good else 3), col, density=0.9, edge=0.9)


def qinglv_landscape(L, ink_only=False):
    """青綠山水：赭石底、石青石綠、金線勾邊；ink_only=True 時只剩水墨"""
    S, rng = L.S, np.random.default_rng(77)
    W, H = L.w, L.h
    for k, (base, amp, cells) in enumerate([(H * 0.55, 420, 3), (H * 0.72, 360, 4), (H * 0.9, 300, 5)]):
        r2 = np.random.default_rng(40 + k)
        xs = np.arange(W, dtype=F32)
        prof = np.zeros(W, F32)
        for _ in range(6 + 2 * k):
            c, wd, hh = r2.uniform(-100, W + 100), r2.uniform(90, 230), r2.uniform(0.5, 1.0) * amp * 1.6
            prof = np.maximum(prof, hh * np.exp(-np.abs((xs - c) / wd) ** 1.4))
        ys = base - prof - 18 * noise1d(W, 12, r2)
        m = S.below_curve(ys, rough=3)
        if ink_only:
            L.wash(m, (0.66, 0.66, 0.66), density=0.5 + 0.15 * k, edge=0.8, gran=0.5)
            L.wash(m * (1 - S.vgrad(H * 0.2, H)), (0.38, 0.38, 0.40), density=0.5, edge=0, bloom=12, occlude=False)
        else:
            L.wash(m, (0.86, 0.76, 0.52), density=0.7, edge=0.6, gran=0.5)
            top = m * (1 - np.clip((np.arange(H, dtype=F32)[:, None] - ys[None, :]) / (amp * 0.6), 0, 1))
            L.wash(top, [(0.30, 0.52, 0.72), (0.34, 0.62, 0.52), (0.26, 0.48, 0.66)][k], density=0.95, edge=0.9, gran=0.8)
        for _ in range(60):
            x = rng.uniform(0, W - 1)
            y = ys[int(x)] + rng.uniform(10, amp * 0.8)
            L.ink([(x, y), (x + rng.uniform(-20, 20), y + rng.uniform(20, 60))], width=1.3, dark=0.5, dry=0.6)
        ridge_ink(L, ys, 2.2, gap=0.1, color=(0.62, 0.45, 0.12) if not ink_only else INK)
    for x in [W * 0.3, W * 0.62]:
        tree_pine(L, x, H * 0.86, 220, color=(0.30, 0.50, 0.40) if not ink_only else (0.36, 0.36, 0.37))


def throne_rock(L, x, yg, s):
    S = L.S
    rock = [(x - s, yg), (x - s * 0.8, yg - s * 0.55), (x - s * 0.35, yg - s * 0.6), (x - s * 0.3, yg - s * 1.3),
            (x + s * 0.3, yg - s * 1.35), (x + s * 0.35, yg - s * 0.6), (x + s * 0.8, yg - s * 0.55), (x + s, yg)]
    L.wash(S.poly(rock, rough=s * 0.03), (0.62, 0.60, 0.62), density=0.9, edge=0.8, gran=0.8)
    L.wash(S.poly(rock, rough=1) * S.vgrad(yg - s * 1.3, yg), (0.42, 0.40, 0.46), density=0.5)
    L.ink(rock, width=2.0, smooth=1, dark=0.8)


def oak_moot(L, x, yg, h, n=10, rng=None):
    """橡樹下的集會：大樹 + 圍坐的人"""
    rng = rng or L.rng
    big_tree(L, x, yg, h, seed_rng=np.random.default_rng(12))
    pts = []
    for k in range(n):
        a = np.pi * (0.1 + 0.8 * k / (n - 1))
        pts.append((x + np.cos(a) * h * 0.5, yg + 30 + np.sin(a) * h * 0.08))
    villagers(L, pts, h * 0.22, rng)
