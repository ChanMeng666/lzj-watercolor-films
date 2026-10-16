"""第十二部《梯子》配樂。python audio/score_film12.py
場景起點：0 16 29 42 56 68 82 98 110 123 139，全長 159 秒"""
import sys
from score import Score
from arrange import section, melody


def film12():
    s = Score(1212); D = 159.0
    F = (4, 'F1', ['C3', 'F3', 'A3']); C = (4, 'C2', ['E3', 'G3', 'C4']); Dm = (4, 'D2', ['D3', 'F3', 'A3'])
    Bb = (4, 'Bb1', ['D3', 'F3', 'Bb3']); Gm = (4, 'G1', ['D3', 'G3', 'Bb3']); Am = (4, 'A1', ['E3', 'A3', 'C4'])
    # 0–16 臨摹「永」字：古箏一筆一畫
    section(s, 0, [F, (4, 'D2', ['D3', 'F3', 'A3']), Bb, C], 'zither', .45)
    melody(s, 6.4, 'dan_tranh', 'C5:1 D5:1 F5:2 G5:1 A5:1 G5:2 F5:1 D5:1 C5:3', vel=.42)
    # 16–29 棋盤：落子聲 → 格局浮現
    section(s, 16, [Dm, Bb, (5, 'C2', ['E3', 'G3', 'C4'])], 'pad', .4)
    for k in range(12): s.n(16.5 + k * 0.45, 'marimba', ['D5', 'A4', 'F5', 'C5'][k % 4], .4, .28 - .015 * k, .3 - .05 * k)
    for k, p in enumerate(['F5', 'A5', 'C6', 'F6']): s.n(21 + k * .8, 'vibraphone', p, 2, .3, -.2)
    # 29–42 導航：燈一盞盞亮起
    section(s, 29, [Am, F, C, (1, 'G1', ['D3', 'G3', 'B3'])], 'darkpad', .38)
    for k in range(10): s.n(36 + k * 0.55, 'glockenspiel', ['A5', 'C6', 'E6', 'G6', 'A6', 'C7', 'E6', 'G6', 'A6', 'C7'][k], 1.2, .32, -.5 + k * .1)
    melody(s, 37, 'flute', 'E5:1 G5:1 A5:2 C6:1 B5:1 A5:2', vel=.36)
    # 42–56 做題家：機械的撥奏
    section(s, 42, [Dm, (4, 'A1', ['C#3', 'E3', 'A3']), Dm, (2, 'A1', ['C#3', 'E3', 'A3'])], 'pizz', .42)
    for k in range(28): s.n(42 + k * .5, 'bassoon_stac', ['D3', 'A2', 'D3', 'F3'][k % 4], .35, .36, -.2)
    s.n(42.5, 'tubular_bells', 'D5', 3, .2)
    # 56–68 默會知識：工匠的手
    section(s, 56, [F, Bb, (4, 'C2', ['E3', 'G3', 'Bb3'])], 'folk', .45)
    melody(s, 57, 'cellos', 'F3:2 A3:1 C4:1 D4:2 C4:2 A3:2 G3:2', vel=.42)
    # 68–82 種子 → 野草
    section(s, 68, [Bb, F, (6, 'C2', ['E3', 'G3', 'C4'])], 'harp', .42)
    section(s, 74, [(8, 'F1', ['A3', 'C4', 'F4'])], 'music_box', .35)
    melody(s, 76.5, 'clarinet', 'C5:1 F5:1 A5:2 G5:1 F5:1 D5:2 C5:2', vel=.38)
    # 82–98 師父與同伴：樹下對弈
    section(s, 82, [F, Dm, Gm, C], 'zither', .42)
    section(s, 82, [F, Dm, Gm, C], 'pad', .28)
    melody(s, 83.5, 'erhu', 'A4:2 C5:1 D5:1 F5:2 D5:1 C5:1 A4:2 G4:2 F4:3', vel=.4)
    # 98–110 刪除：密林被洗去，留下一條路
    section(s, 98, [(4, 'D2', ['F3', 'A3', 'D4', 'E4']), (4, 'Bb1', ['F3', 'Bb3', 'D4']), (4, 'F1', ['A3', 'C4', 'F4'])], 'pad', .38)
    section(s, 98, [(4, 'D2', ['A4']), (4, 'Bb1', ['F4']), (4, 'F1', ['C5'])], 'sparse_piano', .4)
    # 110–123 三張地圖
    section(s, 110, [C, Am, F, (1, 'G1', ['D3', 'G3', 'B3'])], 'arp_piano', .4)
    melody(s, 111, 'oboe', 'E5:1 D5:1 C5:2 E5:1 G5:1 A5:2 G5:3', vel=.36)
    # 123–139 水蜘蛛：水面輕巧，水下深沉
    section(s, 123, [(4, 'E1', ['B2', 'E3', 'G3']), (4, 'C2', ['C3', 'G3', 'E4']), (4, 'A1', ['E3', 'A3', 'C4']), (4, 'B1', ['B2', 'D#3', 'F#3'])], 'darkpad', .42)
    for k in range(30): s.n(123.5 + k * .5, 'harp', ['E6', 'B5', 'G6', 'B5'][k % 4], .4, .22, .4)
    # 139–159 梯子：一級一級向上
    fin = [Bb, C, Dm, (4, 'Bb1', ['D3', 'F3', 'Bb3']), (4, 'F1', ['C3', 'F3', 'A3'])]
    section(s, 139, fin, 'pad', .45); section(s, 139, fin, 'harp', .38)
    for k in range(16): s.n(139.5 + k * .9, 'vibraphone', ['F4', 'G4', 'A4', 'Bb4', 'C5', 'D5', 'E5', 'F5', 'G5', 'A5', 'Bb5', 'C6', 'D6', 'E6', 'F6', 'A6'][k], 1.2, .26, -.3 + k * .04)
    melody(s, 147, 'horn', 'F4:2 A4:1 C5:1 D5:2 C5:2 Bb4:2 A4:2 F4:4', vel=.42)
    s.chord(153.5, 'piano', ['F1', 'C2', 'A2', 'F3', 'C4'], 5, .35, strum=.1); s.n(153.5, 'tubular_bells', 'F5', 4, .26)
    s.render(D, name='film12')


if __name__ == '__main__':
    film12()
