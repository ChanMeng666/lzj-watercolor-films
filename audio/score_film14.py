"""第十四部《車站》配樂。python audio/score_film14.py → audio/out/film14.wav
場景起點：0 14 26 40 52 66 78 91 104 118 131 143，全長 161 s"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score import Score
from arrange import section, melody, bells


def film14():
    s = Score(1414); D = 161.0
    Dm = (4, 'D2', ['D3', 'F3', 'A3']); Bb = (4, 'Bb1', ['D3', 'F3', 'Bb3']); F = (4, 'F1', ['C3', 'F3', 'A3']); C = (4, 'C2', ['E3', 'G3', 'C4'])
    Gm = (4, 'G1', ['D3', 'G3', 'Bb3']); A = (4, 'A1', ['C#3', 'E3', 'A3']); Am = (4, 'A1', ['E3', 'A3', 'C4'])
    # 0–14 河谷：格局早已刻好
    section(s, 0, [Dm, Bb, F, (2, 'C2', ['E3', 'G3', 'C4'])], 'pad', .4)
    melody(s, 6.5, 'horn', 'A3:2 D4:1 F4:1 E4:2 C4:2', vel=.4)
    # 14–26 鐵軌：車輪的節拍
    section(s, 14, [Dm, Gm, (4, 'A1', ['C#3', 'E3', 'A3'])], 'pizz', .45)
    for k in range(22): s.n(14.5 + k * .5, 'bassoon_stac', ['D3', 'A2', 'D3', 'A2'][k % 4], .35, .35, -.2)
    for k in range(5): s.hit(15 + k * 2, 'frame_drum', 'large_muted', .3, .1)
    # 26–40 車站：黃昏的燈
    section(s, 26, [F, C, Dm, (2, 'Bb1', ['D3', 'F3', 'Bb3'])], 'harp', .45)
    section(s, 26, [F, C, Dm, (2, 'Bb1', ['D3', 'F3', 'Bb3'])], 'pad', .28)
    for k, p in enumerate(['C6', 'F6', 'A6', 'C7', 'A6', 'F6']): s.n(27 + k * .6, 'glockenspiel', p, 1.4, .26, .2)
    melody(s, 33.5, 'clarinet', 'A4:1 C5:1 F5:2 E5:1 D5:1 C5:2', vel=.38)
    # 40–52 分岔的河：兩條旋律從同一個音分開
    section(s, 40, [Dm, (4, 'D2', ['D3', 'G3', 'Bb3']), (4, 'D2', ['C#3', 'E3', 'A3'])], 'arp_piano', .4)
    melody(s, 42, 'flute', 'A5:2 Bb5:1 C6:1 D6:2 F6:2 E6:3', vel=.36)
    melody(s, 42, 'cellos', 'A3:2 G3:1 F3:1 D3:2 Bb2:2 A2:3', vel=.42)
    # 52–66 閘門：蓄水，然後放水
    section(s, 52, [(4, 'D2', ['A2', 'D3', 'F3']), (3.6, 'D2', ['A2', 'D3', 'G3'])], 'darkpad', .4)
    s.hit(59.6, 'timpani', 'drum1', .6)
    for k, p in enumerate(['F6', 'D6', 'A5', 'F5', 'D5', 'A4', 'F4']): s.n(59.6 + k * .07, 'harp', p, 1.6, .42, .3, jit=0)
    section(s, 59.6, [F, C, (2.4, 'Dm'[0] and 'D2', ['D3', 'F3', 'A3'])], 'trem', .45)
    melody(s, 60, 'violins', 'F5:1 G5:1 A5:2 C6:2 A5:1 G5:1 F5:2', vel=.4)
    # 66–78 賭局：霧中的十字路口
    section(s, 66, [Gm, (4, 'Eb2', ['G3', 'Bb3', 'Eb4']), A], 'darkpad', .38)
    for k in range(8): s.n(67 + k * 1.3, 'marimba', ['D5', 'A4', 'F5', 'E5'][k % 4], .6, .26, (-1) ** k * .4)
    # 78–91 分娩：燭光與搖籃
    section(s, 78, [Dm, Bb, (5, 'A1', ['C#3', 'E3', 'A3'])], 'music_box', .32)
    section(s, 78, [Dm, Bb, (5, 'A1', ['C#3', 'E3', 'A3'])], 'pad', .3)
    melody(s, 80, 'oboe', 'D5:2 F5:1 E5:1 D5:2 C#5:3', vel=.36)
    # 91–104 羅慕路斯時刻：犁溝的古調
    section(s, 91, [Am, (4, 'G1', ['D3', 'G3', 'B3']), (5, 'A1', ['E3', 'A3', 'C4'])], 'chorale', .4)
    for k in range(6): s.hit(92 + k * 2, 'frame_drum', 'large_muted', .32, .1)
    melody(s, 93, 'horn', 'E4:2 A4:1 G4:1 E4:2 D4:2 E4:3', vel=.4)
    # 104–118 游士與土豪：野草回生
    section(s, 104, [F, C, Dm, (2, 'C2', ['E3', 'G3', 'C4'])], 'folk', .48)
    melody(s, 109, 'flute', 'C6:.5 D6:.5 F6:1 E6:1 D6:.5 C6:.5 A5:2 C6:1 D6:3', vel=.36)
    # 118–131 國父：樹下的會議
    section(s, 118, [(4, 'Bb1', ['D3', 'F3', 'Bb3']), F, (5, 'C2', ['E3', 'G3', 'C4'])], 'brass', .42)
    section(s, 118, [(4, 'Bb1', ['D3', 'F3', 'Bb3']), F, (5, 'C2', ['E3', 'G3', 'C4'])], 'pad', .3)
    # 131–143 天命：一束光
    section(s, 131, [Dm, (4, 'Bb1', ['F3', 'Bb3', 'D4']), (4, 'F1', ['A3', 'C4', 'F4'])], 'pad', .38)
    s.n(133, 'tubular_bells', 'A4', 4, .3); s.n(133, 'vibraphone', 'D6', 3, .3, .2)
    melody(s, 134, 'violin', 'A5:2 D6:1 C6:1 A5:2 F5:4', vel=.36)
    # 143–161 老橡樹：等得起的人
    fin = [F, C, Dm, Bb, (4, 'F1', ['C3', 'F3', 'A3'])]
    section(s, 143, fin, 'pad', .42); section(s, 143, fin, 'arp_piano', .32)
    melody(s, 144, 'cellos', 'F3:2 A3:1 C4:1 D4:2 C4:2 Bb3:2 A3:2 G3:2 F3:4', vel=.44)
    s.chord(156, 'piano', ['F1', 'C2', 'A2', 'C3', 'F3'], 5, .35, strum=.1); s.n(156, 'tubular_bells', 'F4', 4, .26)
    s.render(D, name='film14')


if __name__ == '__main__':
    film14()
