"""場景常用的搭景函數：天空層、遠山層、地面層、前景草，一行一層"""
import numpy as np
from scene import Scene, W, H
from wc import F32
from motifs3 import *

PAL = {
    'dawn':   dict(top=(0.62, 0.66, 0.84), hor=(0.98, 0.86, 0.66)),
    'day':    dict(top=(0.58, 0.70, 0.90), hor=(0.97, 0.95, 0.86)),
    'dusk':   dict(top=(0.46, 0.50, 0.72), hor=(0.99, 0.78, 0.55)),
    'night':  dict(top=(0.14, 0.16, 0.32), hor=(0.40, 0.40, 0.58)),
    'grey':   dict(top=(0.62, 0.64, 0.70), hor=(0.92, 0.90, 0.86)),
    'storm':  dict(top=(0.40, 0.42, 0.52), hor=(0.76, 0.78, 0.84)),
    'gold':   dict(top=(0.80, 0.62, 0.52), hor=(0.99, 0.88, 0.62)),
    'desert': dict(top=(0.62, 0.70, 0.86), hor=(0.99, 0.90, 0.72)),
}


def sky_layer(s, pal='day', clouds_n=8, cloud_col=None, glow=None, y_h=0.65, density=0.75):
    p = PAL[pal]
    L = s.layer('sky', 0.0, opaque=True)
    sky(L, top=p['top'], horizon=p['hor'], y_h=H * y_h, glow=glow, density=density)
    if clouds_n:
        cc = cloud_col or tuple(0.5 * a + 0.5 * b for a, b in zip(p['top'], (0.9, 0.9, 0.92)))
        clouds(L, clouds_n, H * 0.06, H * 0.38, cc, rmin=60, rmax=170, density=0.35)
    return L


def far_layer(s, base=0.62, amp=160, col=(0.70, 0.72, 0.86), depth=0.15, snow=False, ink=0.8, cells=3, name='far'):
    L = s.layer(name, depth)
    ys = mountains(L, H * base, amp, col, cells=cells, sharp=0.3, density=0.55, ink=ink, snow=snow)
    return L, ys


def ground_layer(s, base=0.74, amp=50, col=(0.72, 0.80, 0.52), second=(0.60, 0.68, 0.46), depth=0.45, name='mid', ink=1.3, cells=4):
    L = s.layer(name, depth)
    ys = ground(L, H * base, amp, col, cells=cells, second=second, ink=ink)
    return L, ys


def fg_layer(s, base=0.93, col=(0.58, 0.68, 0.40), depth=0.95, grass=450, name='fg', ink=2.0):
    L = s.layer(name, depth)
    ys = ground(L, H * base, 26, col, cells=5, ink=ink)
    if grass:
        field_strokes(L, ys, L.h, None, n=grass, h=(18, 46))
    return L, ys


def sprite_fig(s, name, h=260, w=None, **kw):
    sp = s.sprite(name, w or int(h * 0.7), int(h * 1.08), anchor=(0.5, 0.97))
    figure(sp, sp.w / 2, h * 1.05, h, **kw)
    return sp


def gy(ys, x):
    return float(ys[int(np.clip(x, 0, len(ys) - 1))])
