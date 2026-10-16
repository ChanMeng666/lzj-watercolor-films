"""三部短片的原創配樂：全部用真實樂器採樣（VSCO 2 CE 管弦、Salamander 三角鋼琴、VCSL 豎琴／管鐘／彈撥、Karoryfer 二胡）
60 BPM，一拍 = 1 秒，一小節 = 4 秒，與畫面的場景邊界對齊。音效也用樂器演奏（落種＝豎琴刮奏、煙花＝定音鼓＋鐘琴、鐘＝撥弦）。
    python audio/score.py film1|film2|film3|all
"""
import os, sys, subprocess
import numpy as np
import soundfile as sf
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib'))
import sampler as S
from sfx import limit

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
os.makedirs(OUT, exist_ok=True)


class Score:
    def __init__(self, seed=1):
        self.ev = []
        self.rng = np.random.default_rng(seed)

    def n(self, t, inst, pitch, dur, vel=.6, pan=0.0, gain=1.0, jit=0.012, **kw):
        t = max(0.0, t + self.rng.normal(0, jit)) if jit else t
        v = float(np.clip(vel * (1 + self.rng.normal(0, .05)), .05, 1))
        e = dict(t=t, inst=inst, pitch=pitch, dur=dur, vel=v, pan=pan, gain=gain)
        e.update(kw)
        self.ev.append(e)

    def chord(self, t, inst, notes, dur, vel=.5, pan=0.0, strum=0.0, gain=1.0, spread=0.3, **kw):
        k = len(notes)
        for i, p in enumerate(notes):
            pp = pan + (i / max(1, k - 1) - .5) * spread
            self.n(t + i * strum, inst, p, dur, vel, pp, gain, **kw)

    def arp(self, t, inst, notes, step, count, vel=.5, pan=0.0, dur=None, gain=1.0, pattern=None, accent=0.15):
        pattern = pattern or list(range(len(notes)))
        for i in range(count):
            p = notes[pattern[i % len(pattern)] % len(notes)]
            self.n(t + i * step, inst, p, dur or step * 2.5, vel * (1 + accent * (i % 4 == 0)), pan, gain)

    def line(self, t, inst, seq, vel=.6, pan=0.0, gain=1.0, legato=1.05, **kw):
        """seq = [(pitch|None, beats), ...]"""
        for p, b in seq:
            if p is not None:
                self.n(t, inst, p, b * legato, vel, pan, gain, **kw)
            t += b
        return t

    def hit(self, t, inst, var=None, vel=.6, pan=0.0, gain=1.0):
        if inst == 'timpani':   # 有音高的鼓：按實測基頻演奏
            root = S.REG['timpani']['roots'][var]
            self.ev.append(dict(t=max(0, t), inst=inst, pitch=root, var=var, dur=3.0, vel=vel, pan=pan, gain=gain))
            return
        self.ev.append(dict(t=max(0, t), inst=inst, pitch=var, dur=None, vel=vel, pan=pan, gain=gain))

    def render(self, dur, room=(.55, .22), name='mix'):
        mix = S.render(self.ev, dur, master=False)
        mix = S.room(mix, size=room[0], mix=room[1])
        # 淡出
        n = len(mix); f = int(2.5 * S.SR)
        mix[n - f:] *= np.linspace(1, 0, f)[:, None] ** 1.5
        mix = mix / (np.abs(mix).max() + 1e-9) * 0.89
        mix = limit(mix, .9)
        raw = os.path.join(OUT, f'{name}_raw.wav')
        sf.write(raw, mix, S.SR, subtype='FLOAT')
        out = os.path.join(OUT, f'{name}.wav')
        # 響度正規化（靜態增益，不壓縮動態）：量整體響度 → 增益到 -16 LUFS → 限幅到 -1.5 dBFS
        r = subprocess.run(['ffmpeg', '-hide_banner', '-nostats', '-i', raw, '-af', 'ebur128', '-f', 'null', '-'],
                           capture_output=True, text=True).stderr
        I = float(r.split('Integrated loudness:')[1].split('I:')[1].split('LUFS')[0])
        g = 10 ** ((-16.0 - I) / 20)
        mix = limit(mix * g, 10 ** (-1.5 / 20))
        sf.write(out, mix, S.SR, subtype='PCM_24')
        os.remove(raw)
        print('wrote', out, f'{dur:.1f}s, {len(self.ev)} notes')


# ======================================================================= 第一部《根》
def film1():
    s = Score(11)
    D = 106.0
    # —— 0–12 落種：獨奏鋼琴動機
    M1 = [('A4', 1), ('D5', 1), ('E5', .5), ('F#5', 1.5), ('E5', 1), ('D5', 1), ('A4', 2)]
    s.n(0.5, 'piano', 'D2', 7, .45, -.2)
    s.n(0.5, 'piano', 'A2', 7, .35, -.1)
    s.line(1.0, 'piano', M1, vel=.5, pan=.1)
    s.chord(8.0, 'piano', ['G2', 'D3', 'B3', 'F#4'], 4, .4, strum=.08)
    # 種子落地 8.6s：豎琴刮奏
    for i, p in enumerate(['D4', 'E4', 'F#4', 'A4', 'B4', 'D5', 'E5', 'F#5', 'A5', 'B5', 'D6']):
        s.n(7.9 + i * 0.065, 'harp', p, 2.5, .45 + i * .02, -.3 + i * .06, jit=0)
    s.n(8.6, 'tubular_bells', 'D5', 4, .3, 0, jit=0)
    s.n(9.2, 'harp', 'A3', 3, .5, .2)
    s.n(10.0, 'piano', 'F#5', 2, .35, .2)
    s.n(10.5, 'piano', 'A5', 1.5, .3, .25)
    # —— 12–28 根：低音下行 D–C#–B–A（根往下長），鋼琴八分音型
    bass = ['D2', 'C#2', 'B1', 'A1']
    tops = [['A3', 'D4', 'E4', 'F#4'], ['A3', 'C#4', 'E4', 'F#4'], ['B3', 'D4', 'F#4', 'A4'], ['A3', 'C#4', 'E4', 'G4']]
    for b in range(4):
        t0 = 12 + b * 4
        s.n(t0, 'cellos', bass[b], 4.1, .45 + .05 * b, -.25)
        s.n(t0, 'contrabass', bass[b], 4.1, .4, -.3, gain=.8)
        tp = tops[b]
        s.arp(t0, 'piano', [['D3', 'C#3', 'B2', 'A2'][b]] + tp,
              .5, 8, vel=.36 + .03 * b, pan=.15, pattern=[0, 1, 2, 3, 4, 3, 2, 1])
        if b >= 2:
            s.chord(t0, 'violas', tp[:2], 4.1, .3, .3, gain=.8)
        s.n(t0 + 2.5, 'harp', tp[-1].replace('4', '5'), 2, .3, .4)
    s.line(20, 'violin', [('F#5', 2), ('E5', 1), ('D5', 1), ('C#5', 2), ('E5', 2), ('D5', 3), (None, 1)], vel=.32, pan=.35)
    # —— 28–40 村莊：G – D/F# – Em7 A7，彈撥（đàn tranh）旋律
    prog = [(28, 'G2', ['G3', 'B3', 'D4']), (32, 'F#2', ['F#3', 'A3', 'D4']), (36, 'E2', ['E3', 'G3', 'B3']), (38, 'A2', ['G3', 'C#4', 'E4'])]
    for t0, b, ch in prog:
        dur = 4 if t0 < 36 else 2
        s.n(t0, 'cellos', b, dur + .1, .45, -.25)
        s.chord(t0, 'violins', [p.replace('3', '4') for p in ch], dur + .1, .28, .25, gain=.7)
        s.arp(t0, 'harp', [b.replace('2', '3')] + ch, .5, int(dur * 2), vel=.35, pan=-.35, pattern=[0, 2, 1, 3, 2, 1])
    s.line(28.5, 'dan_tranh', [('D5', 1), ('E5', .5), ('F#5', 1), ('A5', 1.5), ('B5', 1), ('A5', 1), ('F#5', 2),
                               ('E5', 1), ('D5', .5), ('E5', 1.5), ('F#5', 1), ('E5', 2)], vel=.55, pan=.3)
    for i in range(10):     # 點燈：手鐘
        s.n(30.5 + i * 0.68 + s.rng.uniform(0, .3), 'hand_chimes', ['D6', 'F#6', 'A6', 'B6', 'E6'][i % 5], 2, .22, s.rng.uniform(-.6, .6))
    # —— 40–56 舞：撥弦舞曲，D–G–C–D（混合利底亞），節拍由錯亂到整齊
    hp = [('D2', ['F#4', 'A4', 'D5']), ('G2', ['G4', 'B4', 'D5']), ('C2', ['G4', 'C5', 'E5']), ('D2', ['F#4', 'A4', 'D5'])]
    for b in range(4):
        t0 = 40 + b * 4
        bs, ch = hp[b]
        for beat in range(4):
            tt = t0 + beat
            sync = np.clip((tt - 42) / 10, 0, 1)
            jit = .14 * (1 - sync)
            if beat % 2 == 0:
                s.n(tt + s.rng.normal(0, jit), 'cellos_pizz', bs if beat == 0 else bs.replace('2', '3'), 1, .6, -.2, jit=0)
            else:
                s.chord(tt + s.rng.normal(0, jit), 'violins_pizz', ch, 1, .45, .2, jit=0)
            s.hit(tt + s.rng.normal(0, jit), 'frame_drum', 'large' if beat % 2 == 0 else 'small', .35 + .15 * sync, 0)
            if beat % 2 == 1:
                s.chord(tt + s.rng.normal(0, jit), 'strumstick', [p.replace('5', '4') for p in ch], 1.5, .45, -.15, strum=.03, jit=0)
        s.chord(t0, 'violas', ['D3', 'A3'], 4.1, .3, .05, gain=.8)
    tune = [('D5', .5), ('F#5', .5), ('A5', 1), ('F#5', 1), ('D5', 1), ('G5', 1), ('F#5', .5), ('E5', .5), ('D5', 1), ('B4', 1),
            ('C5', 1), ('D5', .5), ('E5', .5), ('G5', 1), ('E5', 1), ('D5', 2), ('A4', 1), ('D5', 1)]
    s.line(44, 'violin', tune, vel=.5, pan=.1)
    s.line(44, 'flute', [(p.replace('5', '6') if p else p, b) for p, b in tune[:9]], vel=.25, pan=-.3)
    # —— 56–68 成長：全體弦樂 + 圓號
    for t0, b, ch in [(56, 'D2', ['D3', 'A3', 'F#4']), (58, 'C#2', ['E3', 'A3', 'E4']), (60, 'B1', ['D3', 'F#3', 'D4']),
                      (62, 'G1', ['D3', 'G3', 'B3']), (64, 'E2', ['E3', 'G3', 'B3']), (66, 'A1', ['E3', 'A3', 'C#4'])]:
        s.n(t0, 'contrabass', b.replace('1', '2'), 2.1, .55, -.3)
        s.n(t0, 'cellos', b.replace('1', '2'), 2.1, .55, -.25)
        s.chord(t0, 'violas', ch, 2.1, .45, -.05)
        s.chord(t0, 'horn', ch[1:], 2.1, .35, .1, gain=.7)
        s.arp(t0, 'harp', ch + [ch[0].replace('3', '4')], .25, 8, vel=.3, pan=-.4)
    s.line(56, 'violins', [('F#5', 1), ('E5', 1), ('D5', 1), ('C#5', 1), ('D5', 1), ('B4', 1), ('B4', 1), ('D5', 1),
                           ('E5', 1.5), ('F#5', .5), ('E5', 2)], vel=.6, pan=.25)
    s.hit(56, 'timpani', 'drum1', .4)
    s.hit(56, 'sus_cymbal', 'roll', .2)
    # —— 68–80 收割者：D 小調，管鐘、定音鼓滾奏、機械的大提琴跳弓
    s.hit(68.8, 'gran_cassa', 'cresc', .55)
    s.hit(72.0, 'gran_cassa', 'roll', .5)
    s.hit(74.5, 'timpani', 'drum1', .8)
    s.hit(74.5, 'gong', None, .5)
    for k in range(3):
        s.n(69 + k * 4, 'tubular_bells', 'D4', 4, .45, -.1, jit=0)
    s.chord(68.5, 'trombone', ['D2', 'A2', 'D3'], 11.5, .4, -.2)
    s.n(68.5, 'tuba', 'D1', 11.5, .4, -.2, gain=.8)
    s.chord(70, 'violins_trem', ['A5', 'Bb5'], 10, .25, .3, gain=.6)
    for i in range(int(11.5 / .5)):
        s.n(68.5 + i * .5, 'cellos_spic', 'D3' if i % 4 else 'D2', .4, .45, -.3, jit=0.004)
    # —— 80–92 停滯：同一個和弦不再前進
    for i in range(12):
        s.n(80 + i, 'piano', 'A4', 1, .32, .1)
        s.n(80 + i, 'violins_pizz', 'D6', .5, .18, .45)
    for t0 in (80, 84, 88):
        s.chord(t0, 'piano', ['D3', 'E3', 'F3', 'A3'], 4, .3, -.1)
        s.n(t0, 'cellos', 'D3', 4.1, .35, -.25)
    s.n(80, 'vibraphone_bowed', 'E5', 12, .3, .3)
    # —— 92–106 夜：動機回歸
    s.n(92, 'cellos', 'B1', 4.1, .4, -.2); s.n(96, 'cellos', 'G1', 4.1, .4, -.2); s.n(100, 'cellos', 'D2', 6, .4, -.2)
    s.chord(92, 'violas', ['D3', 'F#3', 'B3'], 4.1, .3, 0); s.chord(96, 'violas', ['D3', 'G3', 'B3'], 4.1, .3, 0)
    s.chord(100, 'violas', ['D3', 'F#3', 'A3'], 6, .3, 0)
    s.line(93, 'piano', M1, vel=.42, pan=.1)
    s.chord(100, 'piano', ['D2', 'A2', 'F#3', 'A3', 'E4', 'F#4'], 6, .35, strum=.12)
    s.arp(100, 'harp', ['D4', 'F#4', 'A4', 'D5', 'E5', 'F#5', 'A5'], .18, 7, vel=.3, pan=-.3)
    s.n(102.5, 'tubular_bells', 'D5', 4, .3, 0)
    s.n(102.5, 'glockenspiel', 'F#6', 3, .2, .3)
    s.render(D, name='film1')


# ======================================================================= 第二部《四季》
def film2():
    s = Score(22)
    D = 106.0
    # —— 0–12 春：長笛 + 豎琴
    for t0, b, ch in [(0, 'G2', ['G3', 'B3', 'D4']), (4, 'G2', ['G3', 'C4', 'E4']), (8, 'F#2', ['F#3', 'A3', 'D4'])]:
        s.n(t0, 'cellos', b, 4.1, .35, -.25)
        s.arp(t0, 'harp', [b.replace('2', '3')] + ch + [ch[1].replace('3', '4').replace('4', '5')], .5, 8, vel=.36, pan=-.3,
              pattern=[0, 1, 2, 3, 4, 3, 2, 1])
        s.chord(t0, 'violins_pizz', [p.replace('3', '5').replace('4', '5') for p in ch[1:]], .5, .2, .4)
    s.line(1, 'flute', [('D5', 1), ('G5', 1), ('A5', .5), ('B5', 1.5), ('C6', 1), ('B5', 1), ('A5', 1), ('G5', 1),
                        ('A5', 2), ('D5', 2)], vel=.5, pan=.2)
    for i in range(9):
        s.n(6.5 + i * .6 + s.rng.uniform(0, .25), 'hand_chimes', ['G6', 'A6', 'B6', 'D6', 'E6'][i % 5], 2, .2, s.rng.uniform(-.6, .6))
    # —— 12–24 夏：活潑的鋼琴八分音型 + 單簧管
    for t0, b, ch in [(12, 'C2', ['C4', 'E4', 'G4']), (16, 'D2', ['D4', 'F#4', 'A4']), (20, 'G2', ['D4', 'G4', 'B4'])]:
        s.n(t0, 'cellos', b, 4.1, .45, -.25)
        for k in range(8):
            s.n(t0 + k * .5, 'cellos_pizz', [b, b.replace('2', '3')][k % 2], .5, .4, -.3) if k % 2 == 0 else None
        s.arp(t0, 'piano', ch + [ch[0].replace('4', '5')], .25, 16, vel=.33, pan=.1, pattern=[0, 1, 2, 3, 2, 1, 2, 1])
        s.chord(t0, 'violins', [p.replace('4', '5') for p in ch[1:]], 4.1, .25, .3, gain=.7)
        s.hit(t0, 'triangle', 'open', .25, .5)
    s.line(12.5, 'clarinet', [('G4', 1), ('E5', 1), ('D5', .5), ('C5', .5), ('E5', 1.5), ('F#5', 1), ('A5', 1), ('G5', .5),
                              ('F#5', .5), ('D5', 2), ('B4', 1), ('D5', 1), ('G5', 2)], vel=.45, pan=-.2)
    # —— 24–36 秋：圓號 + 雙簧管，落葉的豎琴下行
    for t0, b, ch in [(24, 'E2', ['E3', 'G3', 'B3']), (28, 'C2', ['E3', 'G3', 'C4']), (32, 'A1', ['E3', 'A3', 'C4']), (34, 'D2', ['D3', 'F#3', 'C4'])]:
        dd = 4 if t0 < 32 else 2
        s.n(t0, 'contrabass', b.replace('1', '2'), dd + .1, .4, -.3)
        s.chord(t0, 'cellos', ch, dd + .1, .35, -.2)
        for k in range(int(dd * 1.5)):
            s.n(t0 + k * .66 + .3, 'harp', ['B5', 'G5', 'E5', 'D5', 'B4', 'A4'][k % 6], 2, .25, .4)
    s.line(24.5, 'horn', [('B3', 1), ('E4', 1), ('D4', 1), ('B3', 1), ('C4', 1.5), ('B3', .5), ('A3', 1), ('G3', 1),
                          ('A3', 1), ('B3', 1), ('F#3', 2)], vel=.5, pan=.1)
    s.line(29, 'oboe', [('G5', 1), ('E5', 2), (None, 1), ('A5', 1), ('C6', 1), ('B5', 2)], vel=.35, pan=.35)
    # —— 36–52 盛世煙花：銅管號角 + 定音鼓對準每一次爆炸
    for t0, b, ch in [(36, 'G1', ['G3', 'B3', 'D4']), (40, 'E2', ['E3', 'G3', 'B3']), (44, 'C2', ['G3', 'C4', 'E4']), (48, 'D2', ['F#3', 'A3', 'D4'])]:
        s.n(t0, 'contrabass', b.replace('1', '2'), 4.1, .55, -.3)
        s.n(t0, 'tuba', b, 4.1, .4, -.2, gain=.8)
        s.chord(t0, 'trombone', ch[:2], 4.1, .35, -.1)
        s.chord(t0, 'violins', [p.replace('3', '5').replace('4', '5') for p in ch], 4.1, .4, .25)
        s.chord(t0, 'trumpet', [ch[1].replace('3', '4'), ch[2].replace('3', '4')], 4, .4, .15, gain=.7)
    s.line(36, 'horn', [('D4', 1), ('G4', 1), ('B4', 2), ('B4', 1), ('A4', 1), ('G4', 2), ('E4', 1), ('G4', 1), ('C5', 2),
                        ('B4', 1), ('A4', 1), ('F#4', 2)], vel=.6, pan=0)
    bursts = [1.0, 2.2, 3.4, 4.3, 5.1, 6.0, 6.7, 7.4, 8.1, 8.6, 9.2, 9.8, 10.3, 10.9, 11.4]
    for wave in (0, 6.4):
        for i, tb in enumerate(bursts):
            te = 36 + tb + wave + 1.1
            if te > 51.5:
                continue
            s.hit(te, 'timpani', ['drum1', 'drum3', 'drum2', 'drum4'][i % 4], .45 + .1 * (i % 3 == 0), s.rng.uniform(-.4, .4))
            s.n(te + .02, 'glockenspiel', ['D6', 'G6', 'B6', 'A6', 'E6'][i % 5], 1.5, .25, s.rng.uniform(-.6, .6))
            if i % 4 == 0:
                s.hit(te, 'clash', 'crash', .3, s.rng.uniform(-.3, .3))
    # —— 52–64 熄燈：小調借和弦，樂器逐一退出
    for t0, b, ch in [(52, 'C2', ['C3', 'Eb3', 'G3', 'C4']), (56, 'Ab1', ['C3', 'Eb3', 'Ab3']), (60, 'G1', ['D3', 'G3', 'C4'])]:
        k = (t0 - 52) / 4
        s.n(t0, 'cellos', b.replace('1', '2'), 4.1, .45 - .08 * k, -.2)
        s.chord(t0, 'violas', ch, 4.1, .35 - .07 * k, 0)
        if k < 2:
            s.chord(t0, 'violins', [p.replace('3', '4') for p in ch[-2:]], 4.1, .3 - .1 * k, .3, gain=.7)
    s.n(62, 'violas', 'B3', 2.1, .2, 0)
    s.line(53, 'violin', [('G5', 2), ('F5', 1), ('Eb5', 1), ('D5', 2), ('C5', 2), ('Bb4', 1.5), ('Ab4', .5), ('G4', 3)], vel=.35, pan=.3)
    for i in range(10):
        s.n(54.5 + i * .9, 'harp', ['C3', 'G2', 'Eb3', 'C2', 'Ab2'][i % 5], 2, .22 - .015 * i, -.4)
    # —— 64–80 冬：鋼琴高音區稀疏，弓奏鐵琴
    for t0, b, ch in [(64, 'E2', ['E5', 'B5']), (68, 'C2', ['G5', 'B5']), (72, 'A1', ['E5', 'A5']), (76, 'B1', ['F#5', 'A5'])]:
        s.n(t0, 'cellos', b.replace('1', '2'), 4.1, .3, -.25)
        s.n(t0, 'vibraphone_bowed', ch[0], 4.1, .25, .2)
        s.n(t0 + .02, 'piano', b.replace('1', '2').replace('2', '3'), 4, .25, -.1)
    s.line(64.5, 'piano', [('B5', 2), ('G5', 1), ('E5', 1), ('F#5', 2), ('B4', 2), ('C6', 2), ('B5', 1), ('A5', 1), ('E5', 3),
                           (None, 1), ('D#5', 2), ('F#5', 2)], vel=.32, pan=.15)
    s.n(70, 'hand_chimes', 'B5', 3, .25, .3)
    # —— 80–92 草原：馬蹄節奏、二胡
    for i in range(48):
        tt = 80 + i * .25
        if i % 4 != 2:
            s.n(tt, 'cellos_spic', 'E2' if i % 4 == 0 else 'E3', .3, .5, -.3, jit=.005)
        if i % 4 == 0:
            s.hit(tt, 'toms', 'low_mallet', .45, -.1)
        elif i % 4 == 3:
            s.hit(tt, 'toms', 'high_mallet', .3, .1)
    for t0, ch in [(80, ['E3', 'B3']), (84, ['D3', 'A3']), (88, ['E3', 'B3'])]:
        s.chord(t0, 'violas', ch, 4.1, .4, 0)
        s.n(t0, 'contrabass', ch[0].replace('3', '2'), 4.1, .5, -.3)
    s.line(80.5, 'erhu', [('E5', 1), ('G5', .5), ('A5', .5), ('B5', 2), ('D6', 1), ('B5', .5), ('A5', .5), ('G5', 1), ('A5', 1),
                          ('E5', 2), ('G5', .5), ('A5', .5), ('E5', 1)], vel=.55, pan=.2)
    s.line(84, 'horn', [('B3', 1), ('E4', 3), ('D4', 1), ('B3', 3)], vel=.4, pan=-.1)
    # —— 92–106 新的春天
    for t0, b, ch in [(92, 'C2', ['C4', 'E4', 'G4']), (96, 'B1', ['D4', 'G4', 'B4']), (100, 'A1', ['C4', 'E4', 'A4']), (102, 'D2', ['C4', 'F#4', 'A4'])]:
        dd = 4 if t0 < 100 else 2
        s.n(t0, 'cellos', b.replace('1', '2'), dd + .1, .35, -.25)
        s.arp(t0, 'harp', ch + [ch[0].replace('4', '5')], .5, int(dd * 2), vel=.33, pan=-.3)
    s.line(92.5, 'flute', [('E5', 1), ('G5', 1), ('C6', 2), ('B5', 1), ('D6', 1), ('G5', 2), ('A5', 1), ('C6', 1), ('B5', 1), ('A5', 1)],
           vel=.45, pan=.2)
    s.chord(104, 'piano', ['G2', 'D3', 'B3', 'D4', 'G4'], 3, .32, strum=.1)
    s.n(104, 'flute', 'G5', 2.5, .4, .2)
    s.n(104, 'tubular_bells', 'G5', 3, .25, 0)
    s.render(D, name='film2')


# ======================================================================= 第三部《守先待後》
def film3():
    s = Score(33)
    D = 98.0
    # —— 0–12 雪夜修院：管風琴、鐘
    s.chord(0.3, 'organ_soft', ['A2', 'E3', 'A3'], 11.5, .35, 0)
    s.n(0.3, 'contrabass', 'A1', 11.5, .3, -.2)
    for k, tt in enumerate([0.6, 4.6, 8.6]):
        s.n(tt, 'tubular_bells', 'A3' if k < 2 else 'E4', 4, .4, -.1, jit=0)
    s.n(3.0, 'hand_chimes', 'E6', 3, .3, .3)
    s.n(7.5, 'vibraphone_bowed', 'C5', 4.5, .25, .3)
    # —— 12–28 燈下抄書：鋼琴聖詠 + 大提琴
    cho = [(12, ['A2', 'E3', 'C4', 'A4']), (14, ['A2', 'E3', 'B3', 'G#4']), (16, ['F2', 'C3', 'A3', 'F4']), (18, ['F2', 'C3', 'A3', 'E4']),
           (20, ['C2', 'G2', 'E3', 'C4', 'G4']), (22, ['C2', 'G2', 'E3', 'D4', 'G4']), (24, ['E2', 'B2', 'G#3', 'D4', 'B4']),
           (26, ['E2', 'B2', 'G#3', 'E4', 'B4'])]
    for t0, ch in cho:
        s.chord(t0, 'piano', ch, 2.1, .3, strum=.03)
    s.line(13, 'cellos', [('E3', 2), ('C3', 1), ('D3', 1), ('E3', 2), ('F3', 2), ('G3', 3), ('E3', 1), ('D3', 2), ('E3', 3)], vel=.35, pan=-.25)
    # —— 28–40 鐘：撥弦嘀嗒逐漸加快；時針
    t = 28.0; i = 0
    while t < 39.5:
        s.n(t, 'violins_pizz', 'E5' if i % 2 == 0 else 'A5', .4, .3, .35 if i % 2 else -.35, jit=0)
        lt = t - 28
        step = 1.0 - 0.75 * np.clip((lt - 2) / 7, 0, 1)
        t += step; i += 1
    s.n(28.1, 'tubular_bells', 'A3', 4, .4, 0, jit=0); s.n(38.0, 'tubular_bells', 'E4', 3, .3, 0, jit=0)
    for t0, b, ch in [(28, 'F2', ['F3', 'A3', 'C4', 'E4']), (32, 'G2', ['G3', 'B3', 'D4', 'F4']), (36, 'A2', ['A3', 'C4', 'E4', 'G4'])]:
        s.n(t0, 'cellos', b, 4.1, .35, -.25)
        s.arp(t0, 'harp', ch + [ch[0].replace('3', '4').replace('4', '5')], .25 if t0 > 28 else .5, 16 if t0 > 28 else 8, vel=.28, pan=-.3)
    # —— 40–56 挖坑種樹：民謠撥弦 + 大提琴；每兩秒一鏟
    for t0, b, ch in [(40, 'C2', ['C3', 'G3', 'C4', 'E4']), (44, 'A1', ['A2', 'E3', 'A3', 'C4']), (48, 'F1', ['F2', 'C3', 'F3', 'A3']),
                      (52, 'G1', ['G2', 'D3', 'G3', 'B3'])]:
        s.n(t0, 'contrabass', b.replace('1', '2'), 4.1, .4, -.3)
        s.arp(t0, 'strumstick', ch, .5, 8, vel=.5, pan=.25, pattern=[0, 2, 1, 3, 2, 1, 3, 2])
    s.line(40.5, 'cellos', [('E4', 1), ('G4', 1), ('A4', 2), ('C5', 1), ('B4', 1), ('A4', 2), ('F4', 1), ('A4', 1), ('C5', 1.5),
                            ('B4', .5), ('G4', 2), ('A4', 1), ('B4', 1)], vel=.42, pan=-.2)
    for k in range(6):
        s.hit(40 + k * 2, 'frame_drum', 'large_muted', .4, .1)
    for k, p in enumerate(['C6', 'E6', 'G6', 'C7']):
        s.n(51.2 + k * .8, 'glockenspiel', p, 2, .22, .3)
    # —— 56–68 風雪：顫弓、跳弓、圓號「求戰者安」
    for t0, b, ch in [(56, 'A1', ['A2', 'E3', 'C4']), (60, 'A1', ['A2', 'D3', 'F3']), (64, 'E1', ['B2', 'E3', 'G#3'])]:
        s.n(t0, 'contrabass', b.replace('1', '2'), 4.1, .55, -.3)
        s.chord(t0, 'violins_trem', [p.replace('2', '4').replace('3', '5') for p in ch], 4.1, .35, .3, gain=.7)
        for k in range(16):
            s.n(t0 + k * .25, 'cellos_spic', b.replace('1', '2') if k % 4 == 0 else b.replace('1', '3'), .25, .45, -.25, jit=.004)
    s.hit(56, 'gran_cassa', 'roll', .4); s.hit(64, 'gran_cassa', 'cresc', .45)
    s.line(57.5, 'horn', [('A3', 1), ('E4', 1), ('A4', 2), ('C5', 1.5), ('B4', .5), ('A4', 2), ('G#4', 1), ('B4', 1), ('E5', 3)], vel=.6, pan=0)
    s.line(57.5, 'trombone', [('A2', 4), ('D3', 4), ('E3', 4)], vel=.35, pan=-.15)
    # —— 68–84 雪融發芽：C 大調，鋼琴 + 弦樂漸強
    for t0, b, ch in [(68, 'F1', ['A3', 'C4', 'F4']), (72, 'E1', ['G3', 'C4', 'E4']), (76, 'D2', ['A3', 'C4', 'F4']), (80, 'G1', ['B3', 'D4', 'G4'])]:
        k = (t0 - 68) / 4
        s.n(t0, 'cellos', b.replace('1', '2'), 4.1, .35 + .05 * k, -.25)
        s.chord(t0, 'violas', ch, 4.1, .25 + .05 * k, 0)
        if k >= 1:
            s.chord(t0, 'violins', [p.replace('3', '5').replace('4', '5') for p in ch[1:]], 4.1, .2 + .06 * k, .3, gain=.7)
        s.arp(t0, 'piano', [b.replace('1', '3').replace('2', '3')] + ch, .5, 8, vel=.3, pan=.1, pattern=[0, 1, 2, 3, 2, 1, 2, 3])
    for k in range(10):
        s.n(73 + k * 1.05, 'hand_chimes', ['C6', 'E6', 'G6', 'A6', 'D6'][k % 5], 2, .22, s.rng.uniform(-.6, .6))
    s.line(76, 'flute', [('E5', 1), ('F5', 1), ('G5', 2), ('A5', 1), ('B5', 1), ('C6', 2)], vel=.35, pan=.3)
    # —— 84–98 春日山谷：終曲
    for t0, b, ch in [(84, 'C2', ['C3', 'G3', 'E4']), (88, 'B1', ['D3', 'G3', 'D4']), (92, 'A1', ['C3', 'E3', 'A3']), (94, 'G1', ['D3', 'G3', 'B3'])]:
        dd = 4 if t0 < 92 else 2
        s.n(t0, 'contrabass', b.replace('1', '2'), dd + .1, .45, -.3)
        s.chord(t0, 'cellos', ch, dd + .1, .4, -.2)
        s.chord(t0, 'violins', [p.replace('3', '4').replace('4', '5') for p in ch], dd + .1, .35, .25, gain=.8)
        s.arp(t0, 'harp', ch + [ch[0].replace('3', '5').replace('2', '5')], .25, int(dd * 4), vel=.28, pan=-.4)
    s.line(84.5, 'horn', [('G4', 1), ('C5', 1), ('E5', 2), ('D5', 1), ('B4', 1), ('G4', 2), ('A4', 1), ('C5', 1), ('B4', 1), ('D5', 1)],
           vel=.5, pan=.05)
    s.chord(96, 'piano', ['C2', 'G2', 'E3', 'G3', 'C4', 'E4'], 2, .35, strum=.1)
    s.chord(96, 'violins', ['E5', 'G5', 'C6'], 2, .3, .2)
    s.n(96, 'tubular_bells', 'C5', 3, .3, 0)
    s.n(96.1, 'glockenspiel', 'G6', 2, .2, .3)
    s.render(D, name='film3')


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'all'
    for f in (['film1', 'film2', 'film3'] if which == 'all' else [which]):
        globals()[f]()
