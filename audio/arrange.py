"""配器樣式庫：給一段和弦進行 + 一種樣式，生成一段音樂（全部真實樂器採樣）。
和弦寫法：[(拍數, 低音, [和弦音...]), ...]；一拍 = 1 秒 (60 BPM)。
"""
import re
import numpy as np
from score import Score, S

_N = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}


def up(p, k=1):
    """移八度"""
    m = re.fullmatch(r'([A-G][#b]?)(-?\d)', p)
    return f'{m.group(1)}{int(m.group(2)) + k}'


def section(s: Score, t0, chords, style, vel=0.5, pan=0.0):
    t = t0
    for beats, bass, notes in chords:
        STY[style](s, t, beats, bass, notes, vel, pan)
        t += beats
    return t


def _pad(s, t, b, bass, notes, v, pan):
    s.n(t, 'cellos', bass, b + .15, v * .8, -.25)
    s.chord(t, 'violas', notes[:2], b + .15, v * .6, -.05, gain=.8)
    s.chord(t, 'violins', [up(x) for x in notes[1:]], b + .15, v * .5, .25, gain=.7)


def _darkpad(s, t, b, bass, notes, v, pan):
    s.n(t, 'contrabass', bass, b + .15, v * .8, -.3)
    s.n(t, 'cellos', up(bass), b + .15, v * .7, -.2)
    s.chord(t, 'violas', notes, b + .15, v * .5, 0, gain=.8)


def _arp_piano(s, t, b, bass, notes, v, pan):
    s.n(t, 'cellos', bass, b + .15, v * .7, -.25)
    pool = [up(bass)] + list(notes) + [up(notes[0])]
    s.arp(t, 'piano', pool, .5, int(b * 2), vel=v * .7, pan=.12, pattern=[0, 1, 2, 3, 4, 3, 2, 1])


def _harp(s, t, b, bass, notes, v, pan):
    s.n(t, 'cellos', bass, b + .15, v * .6, -.25)
    pool = [up(bass)] + list(notes) + [up(x) for x in notes]
    s.arp(t, 'harp', pool, .25, int(b * 4), vel=v * .55, pan=-.3, pattern=[0, 1, 2, 3, 4, 5, 6, 5, 4, 3, 2, 1])


def _pizz(s, t, b, bass, notes, v, pan):
    for k in range(int(b)):
        if k % 2 == 0:
            s.n(t + k, 'cellos_pizz', bass if k % 4 == 0 else up(bass), 1, v, -.2)
        else:
            s.chord(t + k, 'violins_pizz', [up(x) for x in notes], 1, v * .75, .2)
    s.chord(t, 'violas', notes[:2], b + .1, v * .4, 0, gain=.7)


def _chorale(s, t, b, bass, notes, v, pan):
    s.chord(t, 'piano', [bass] + list(notes), b + .1, v * .65, strum=.025)
    s.n(t, 'cellos', bass, b + .1, v * .45, -.25)


def _organ(s, t, b, bass, notes, v, pan):
    s.chord(t, 'organ_soft', [bass] + list(notes), b + .1, v * .6, 0)


def _march(s, t, b, bass, notes, v, pan):
    s.n(t, 'contrabass', bass, b + .1, v * .8, -.3)
    s.chord(t, 'trombone', [up(bass), notes[0]], b + .1, v * .55, -.15)
    s.chord(t, 'violins', [up(x) for x in notes], b + .1, v * .5, .25, gain=.8)
    for k in range(int(b)):
        s.hit(t + k, 'snare', 'on' if k % 2 else 'off', v * (.5 if k % 2 else .35), .1)
        if k % 2 == 0:
            s.hit(t + k, 'bass_drum', None, v * .6, 0)
        s.hit(t + k + .5, 'snare', 'off', v * .25, .1)


def _trem(s, t, b, bass, notes, v, pan):
    s.n(t, 'contrabass', bass, b + .1, v * .9, -.3)
    s.chord(t, 'violins_trem', [up(x) for x in notes], b + .1, v * .55, .3, gain=.7)
    for k in range(int(b * 4)):
        s.n(t + k * .25, 'cellos_spic', up(bass) if k % 4 else bass, .25, v * .8, -.25, jit=.004)
    s.hit(t, 'timpani', 'drum1', v * .8)


def _gallop(s, t, b, bass, notes, v, pan):
    for k in range(int(b * 4)):
        if k % 4 != 2:
            s.n(t + k * .25, 'cellos_spic', bass if k % 4 == 0 else up(bass), .3, v, -.3, jit=.005)
        if k % 4 == 0:
            s.hit(t + k * .25, 'toms', 'low_mallet', v * .9, -.1)
        elif k % 4 == 3:
            s.hit(t + k * .25, 'toms', 'high_mallet', v * .6, .1)
    s.chord(t, 'violas', notes[:2], b + .1, v * .7, 0)


def _folk(s, t, b, bass, notes, v, pan):
    s.n(t, 'contrabass', bass, b + .1, v * .7, -.3)
    pool = [up(bass)] + list(notes)
    s.arp(t, 'strumstick', pool, .5, int(b * 2), vel=v, pan=.25, pattern=[0, 2, 1, 3, 2, 1, 3, 2])


def _zither(s, t, b, bass, notes, v, pan):
    s.n(t, 'cellos', bass, b + .1, v * .6, -.25)
    pool = list(notes) + [up(x) for x in notes]
    s.arp(t, 'dan_tranh', pool, .5, int(b * 2), vel=v * .9, pan=.2, pattern=[0, 2, 4, 3, 1, 3, 2, 5])


def _music_box(s, t, b, bass, notes, v, pan):
    pool = [up(x, 2) for x in notes]
    for k in range(int(b * 2)):
        s.n(t + k * .5, 'glockenspiel' if k % 2 == 0 else 'hand_chimes', pool[(k * 2) % len(pool)], 1.5, v * .4, .3 * np.sin(k))
    s.n(t, 'vibraphone_bowed', up(notes[0]), b + .1, v * .4, -.2)


def _clock(s, t, b, bass, notes, v, pan):
    for k in range(int(b)):
        s.hit(t + k, 'woodblock', 'a' if k % 2 else 'b', v * .5, .4 if k % 2 else -.4)
    s.n(t, 'cellos', bass, b + .1, v * .5, -.25)
    s.chord(t, 'violas', notes[:2], b + .1, v * .35, 0)


def _brass(s, t, b, bass, notes, v, pan):
    s.n(t, 'tuba', bass, b + .1, v * .6, -.2)
    s.chord(t, 'horn', notes, b + .1, v * .55, 0)
    s.chord(t, 'trombone', [up(bass), notes[0]], b + .1, v * .45, -.15)
    s.chord(t, 'violins', [up(x) for x in notes], b + .1, v * .45, .25, gain=.8)
    s.hit(t, 'timpani', 'drum2', v * .6)


def _sparse_piano(s, t, b, bass, notes, v, pan):
    s.n(t, 'piano', bass, b, v * .45, -.15)
    s.n(t + b * 0.5, 'piano', up(notes[-1]), b * .5, v * .4, .2)
    s.n(t, 'vibraphone_bowed', notes[0], b + .1, v * .3, .2)


STY = dict(pad=_pad, darkpad=_darkpad, arp_piano=_arp_piano, harp=_harp, pizz=_pizz, chorale=_chorale, organ=_organ,
           march=_march, trem=_trem, gallop=_gallop, folk=_folk, zither=_zither, music_box=_music_box, clock=_clock,
           brass=_brass, sparse_piano=_sparse_piano)


def melody(s, t, inst, seq, vel=.55, pan=.1, **kw):
    """seq 字串：'E5:1 G5:1 A5:2 -:1 ...'（- 為休止）"""
    for tok in seq.split():
        p, b = tok.split(':')
        b = float(b)
        if p != '-':
            s.n(t, inst, p, b * 1.05, vel, pan, **kw)
        t += b
    return t


def bells(s, t, notes, inst='hand_chimes', step=.6, vel=.22):
    for i, p in enumerate(notes):
        s.n(t + i * step + s.rng.uniform(0, step * .4), inst, p, 2, vel, s.rng.uniform(-.6, .6))
