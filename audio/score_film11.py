"""第十一部《霉菌》配樂。python audio/score_film11.py
場景起點：0 13 27 40 52 62 74 88 101 114 125 134 147，全長 166 s"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from score import Score
from arrange import section, melody


def film11():
    s = Score(1111); D = 166.0
    Dm = (4, 'D2', ['D3', 'F3', 'A3']); Bb = (4, 'Bb1', ['D3', 'F3', 'Bb3']); F = (4, 'F1', ['C3', 'F3', 'A3']); C = (4, 'C2', ['E3', 'G3', 'C4'])
    Gm = (4, 'G1', ['D3', 'G3', 'Bb3']); A = (4, 'A1', ['C#3', 'E3', 'A3'])
    # 0–13 夜裡點燭：管風琴般的長音 + 鐘
    section(s, 0, [(5, 'D2', ['A3', 'D4']), Bb, (4, 'F1', ['A3', 'C4', 'F4'])], 'organ', .32)
    for k in range(10): s.n(4 + k * .9, 'hand_chimes', ['A5', 'D6', 'F6', 'E6', 'C6'][k % 5], 1.6, .18, -.5 + k * .1)
    melody(s, 7.5, 'cellos', 'D3:2 F3:1 A3:1 G3:2 F3:1 E3:1 D3:3', vel=.4)
    # 13–27 培養皿：撥奏細菌 + 長笛霉菌
    section(s, 13, [Dm, (4, 'A1', ['E3', 'A3', 'C4']), Bb, (2, 'C2', ['E3', 'G3', 'C4'])], 'pizz', .4)
    for k in range(24): s.n(13.5 + k * .35, 'marimba', ['D5', 'F5', 'A5', 'E5', 'C5', 'G5'][k % 6], .3, .16 + .004 * k, .4)
    melody(s, 17, 'flute', 'A5:2 D6:1 C6:1 A5:2 F5:2 G5:1 A5:1 D5:3', vel=.36)
    # 27–40 抗生素：震音弦樂，越來越暗
    section(s, 27, [(4, 'E1', ['B2', 'E3', 'G3']), (4, 'C2', ['C3', 'G3', 'Eb4']), (5, 'B1', ['B2', 'D3', 'F#3'])], 'trem', .45)
    s.hit(31, 'timpani', 'drum1', .5); s.hit(35.6, 'timpani', 'drum1', .6)
    # 40–52 斗室：一根蠟燭，豎琴
    section(s, 40, [F, C, (4, 'Dm'[0] and 'D2', ['F3', 'A3', 'D4'])], 'harp', .4)
    melody(s, 41.5, 'clarinet', 'C5:1 F5:1 A5:2 G5:1 F5:1 E5:2 D5:1 C5:3', vel=.36)
    # 52–62 玫瑰窗：聖詠
    section(s, 52, [(3, 'F1', ['A3', 'C4', 'F4']), (3, 'Bb1', ['D4', 'F4', 'Bb4']), (4, 'C2', ['E4', 'G4', 'C5'])], 'chorale', .4)
    s.n(56, 'tubular_bells', 'F5', 3, .25)
    # 62–74 清教徒的船：民謠
    section(s, 62, [F, C, Dm], 'folk', .45)
    melody(s, 63, 'violin', 'F5:1 G5:1 A5:2 C6:1 A5:1 G5:2 F5:1 D5:1 F5:3', vel=.38)
    # 74–88 穀倉：先溫暖，後封門
    section(s, 74, [F, (4, 'Bb1', ['D3', 'F3', 'Bb3'])], 'harp', .42)
    melody(s, 75, 'oboe', 'A4:1 C5:1 F5:2 E5:1 D5:1 C5:2', vel=.36)
    section(s, 83, [(5, 'D2', ['D3', 'F3', 'A3']), (5, 'A1', ['E3', 'A3', 'C4'])], 'darkpad', .4)
    s.hit(83.2, 'timpani', 'drum1', .5)
    # 88–101 雕像與幼苗
    section(s, 88, [Gm, Dm, (5, 'A1', ['C#3', 'E3', 'A3'])], 'sparse_piano', .4)
    section(s, 88, [Gm, Dm, (5, 'A1', ['C#3', 'E3', 'A3'])], 'pad', .28)
    # 101–114 花朵之下：明亮的琶音，再向地下沉
    section(s, 101, [F, C, Bb, (1, 'C2', ['E3', 'G3', 'C4'])], 'arp_piano', .42)
    melody(s, 102, 'flute', 'C6:.5 D6:.5 F6:1 A6:1 G6:1 F6:1 D6:1 C6:2', vel=.32)
    melody(s, 108, 'cellos', 'F2:2 C3:2 D3:2', vel=.4)
    # 114–125 燃燒的蠟燭：漸強再消耗
    section(s, 114, [Dm, Bb, (3, 'A1', ['C#3', 'E3', 'A3'])], 'organ', .38)
    melody(s, 115, 'horn', 'D4:2 F4:1 A4:1 D5:3 C5:1 A4:2', vel=.4)
    # 125–134 月亮
    section(s, 125, [(4, 'Bb1', ['F3', 'Bb3', 'D4']), (5, 'F1', ['F3', 'A3', 'C4'])], 'music_box', .35)
    section(s, 125, [(4, 'Bb1', ['F3', 'Bb3', 'D4']), (5, 'F1', ['F3', 'A3', 'C4'])], 'pad', .25)
    # 134–147 賣火柴的小女孩
    section(s, 134, [Dm, Gm, (5, 'A1', ['C#3', 'E3', 'A3'])], 'sparse_piano', .4)
    for k, td in enumerate([1, 3.6, 6.2]): s.n(134 + td, 'glockenspiel', ['A6', 'F6', 'D6'][k], 1.2, .3, .2)
    melody(s, 142.5, 'clarinet', 'A4:1 D5:1 F5:2 E5:1 C#5:1 D5:3', vel=.36)
    # 147–166 嚴冬、種子、鐘聲
    fin = [(4, 'D2', ['D3', 'F3', 'A3']), (4, 'Bb1', ['D3', 'F3', 'Bb3']), (4, 'F1', ['C3', 'F3', 'A3']), (7, 'C2', ['E3', 'G3', 'C4'])]
    section(s, 147, fin, 'pad', .42); section(s, 147, fin, 'harp', .32)
    for td in (10, 12, 14): s.n(147 + td, 'tubular_bells', 'F4', 4, .28, -.2)
    melody(s, 148, 'cellos', 'D3:2 F3:1 A3:1 Bb3:2 A3:2 F3:2 G3:2 E3:4', vel=.42)
    s.chord(161, 'piano', ['F2', 'C3', 'A3', 'C4', 'F4'], 5, .32, strum=.1); s.n(161, 'tubular_bells', 'F5', 4, .26)
    s.render(D, name='film11')


if __name__ == '__main__':
    film11()
