"""第十三部《宗族》配樂：python audio/score_film13.py → audio/out/film13.wav
場景起點：0 14 27 40 54 67 80 91 104 117 130 143，全長 162 s"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__))); sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'lib'))
from score import Score
from arrange import section, melody, bells


def film13():
    s = Score(1013); D = 162.0
    G = (4, 'G1', ['D3', 'G3', 'B3']); Em = (4, 'E2', ['E3', 'G3', 'B3']); C = (4, 'C2', ['E3', 'G3', 'C4']); D7 = (4, 'D2', ['D3', 'F#3', 'A3'])
    Am = (4, 'A1', ['E3', 'A3', 'C4']); Bm = (4, 'B1', ['D3', 'F#3', 'B3'])
    # 0–14 雨夜一院燈火：古箏與溫暖的墊底
    section(s, 0, [G, Em, C, (2, 'D2', ['D3', 'A3'])], 'pad', .4)
    section(s, 6, [(4, 'G1', ['D4', 'G4']), (4, 'E2', ['B3', 'E4'])], 'zither', .4)
    melody(s, 7.5, 'erhu', 'D5:1 E5:1 G5:2 E5:1 D5:1 B4:2', vel=.38)
    # 14–27 屏障消失：顏色褪去，只剩稀疏的鋼琴
    section(s, 14, [(4, 'E2', ['E3', 'G3', 'B3']), (4, 'C2', ['E3', 'G3']), (5, 'B1', ['D3', 'F#3'])], 'darkpad', .35)
    section(s, 14, [(4, 'E2', ['B4']), (4, 'C2', ['G4']), (5, 'B1', ['F#4'])], 'sparse_piano', .4)
    # 27–40 組織力：撥弦一根根連起來
    section(s, 27, [G, D7, Em, (1, 'C2', ['E3', 'G3'])], 'pizz', .45)
    for k in range(18): s.n(29.5 + k * .45, 'harp', ['G4', 'B4', 'D5', 'G5', 'D5', 'B4'][k % 6], 1.2, .3, -.4 + .05 * k)
    # 40–54 弄假成真：民謠步伐，走上山坡
    section(s, 40, [C, G, Am, (2, 'D2', ['D3', 'F#3', 'A3'])], 'folk', .45)
    melody(s, 41, 'flute', 'G5:1 A5:1 B5:2 D6:1 B5:1 A5:2 G5:1 E5:1 G5:2', vel=.36)
    s.hit(48.5, 'timpani', 'drum1', .4)
    # 54–67 祠堂與福利：管風琴般的聖詠
    section(s, 54, [G, C, (5, 'D2', ['D3', 'F#3', 'A3'])], 'chorale', .42)
    melody(s, 55.5, 'cellos', 'G3:2 B3:1 D4:1 E4:2 D4:2 C4:2 B3:2', vel=.4)
    # 67–80 榕樹：豎琴分散和弦，一戶戶燈亮
    section(s, 67, [Em, C, G, (1, 'D2', ['D3', 'A3'])], 'harp', .45)
    for k in range(8): s.n(69 + k * .7, 'glockenspiel', ['B5', 'D6', 'E6', 'G6', 'B6', 'G6', 'E6', 'D6'][k], 1.4, .25, -.5 + .14 * k)
    # 80–91 婚姻聯盟：撥奏與鈴
    section(s, 80, [(4, 'D2', ['D3', 'F#3', 'A3']), (4, 'G1', ['D3', 'G3', 'B3']), (3, 'A1', ['E3', 'A3', 'C#4'])], 'pizz', .4)
    s.n(82, 'tubular_bells', 'D5', 3, .25); s.n(86, 'tubular_bells', 'A4', 3, .22)
    # 91–104 投胎：音樂盒，三粒種子
    section(s, 91, [C, Am, G, (1, 'G1', ['D3', 'G3'])], 'music_box', .4)
    for t0, p in [(91.8, 'C4'), (94.4, 'E4'), (97, 'G4')]: s.n(t0 + 1.2, 'marimba', p, .8, .4)
    melody(s, 99.5, 'clarinet', 'E5:1 G5:1 C6:2 B5:1 G5:1 A5:2', vel=.36)
    # 104–117 吃子孫飯：低音震音，漏水
    section(s, 104, [(4, 'E1', ['B2', 'E3', 'G3']), (4, 'C2', ['C3', 'G3', 'E4']), (5, 'B1', ['B2', 'D#3', 'F#3'])], 'trem', .4)
    for k in range(16): s.n(106 + k * .7, 'hand_chimes', ['E6', 'B5', 'G5', 'E5'][k % 4], .9, .14, .3)
    # 117–130 四代人：鋼琴琶音，雪落
    section(s, 117, [G, Bm, C, (1, 'D2', ['D3', 'A3'])], 'arp_piano', .4)
    section(s, 117, [G, Bm, C, (1, 'D2', ['D3', 'A3'])], 'pad', .28)
    melody(s, 118, 'horn', 'G3:2 B3:2 D4:3 C4:1 B3:2 A3:2', vel=.38)
    # 130–143 後台：極簡，鋼琴單音與暗墊
    section(s, 130, [(4, 'A1', ['E3', 'A3', 'C4']), (4, 'F1', ['C3', 'F3', 'A3']), (5, 'E1', ['B2', 'E3', 'G#3'])], 'darkpad', .35)
    section(s, 130, [(4, 'A1', ['E4']), (4, 'F1', ['C5']), (5, 'E1', ['B4'])], 'sparse_piano', .38)
    # 143–162 重建：從灰暗到溫暖，燈一盞盞亮
    fin = [(4, 'E2', ['E3', 'G3', 'B3']), (4, 'C2', ['E3', 'G3', 'C4']), (4, 'G1', ['D3', 'G3', 'B3']), (7, 'D2', ['D3', 'F#3', 'A3'])]
    section(s, 143, fin, 'pad', .42); section(s, 149, fin[1:], 'harp', .38)
    for k in range(10): s.n(152 + k * .6, 'celesta', ['G5', 'B5', 'D6', 'G6', 'B6'][k % 5], 1.5, .22, -.6 + .12 * k)
    melody(s, 150, 'erhu', 'B4:1 D5:1 E5:2 G5:2 E5:1 D5:1 B4:2 D5:3', vel=.38)
    s.chord(157.5, 'piano', ['G1', 'D2', 'B2', 'D3', 'G3'], 4.5, .35, strum=.1); s.n(157.5, 'tubular_bells', 'G4', 4, .25)
    s.render(D, name='film13')


if __name__ == '__main__':
    film13()
