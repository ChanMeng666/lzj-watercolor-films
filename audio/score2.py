"""第四部起的配樂（用 arrange 樣式庫）。python audio/score2.py film4 | all"""
import sys
import numpy as np
from score import Score
from arrange import section, melody, bells, up


def film4():
    s = Score(44); D = 150.0
    Em = (4, 'E2', ['E3', 'B3', 'D4']); C = (4, 'C2', ['E3', 'G3', 'C4']); Dm = (4, 'D2', ['D3', 'A3', 'F#4']); B7 = (4, 'B1', ['D#3', 'A3', 'F#4'])
    Am = (4, 'A1', ['E3', 'A3', 'C4'])
    # 一 0–14 草原與山丘
    section(s, 0, [Em, C, Dm, (2, 'E2', ['E3', 'B3', 'D4'])], 'zither', .5)
    melody(s, 3, 'erhu', 'B4:1 D5:1 E5:2 G5:1 F#5:1 E5:2 D5:1 B4:1 A4:2', vel=.5)
    # 二 14–28 低氣壓：雨水沿坡流入窪地
    section(s, 14, [Am, (4, 'F1', ['C3', 'F3', 'A3']), Em, (2, 'E1', ['B2', 'E3', 'G#3'])], 'darkpad', .5)
    for k in range(24):
        s.n(14 + k * .55, 'harp', ['E6', 'C6', 'A5', 'G5', 'E5', 'C5', 'A4', 'E4'][k % 8], 1.5, .25, .4)
    s.hit(14.2, 'gran_cassa', 'roll', .35)
    # 三 28–40 長城：馬蹄
    section(s, 28, [Em, (4, 'D2', ['D3', 'A3']), (4, 'C2', ['C3', 'G3'])], 'gallop', .55)
    melody(s, 29, 'horn', 'B3:1 E4:3 D4:1 B3:2 G3:1 A3:2 B3:2', vel=.45)
    # 四 40–52 旋轉門：絲路
    section(s, 40, [Em, (4, 'A1', ['E3', 'A3', 'C4']), B7], 'zither', .55)
    section(s, 40, [Em, (4, 'A1', ['E3', 'A3', 'C4']), B7], 'pad', .35)
    melody(s, 41, 'erhu', 'E5:1 F#5:.5 G5:.5 B5:2 A5:1 G5:1 F#5:2 E5:1 D5:1 E5:2', vel=.55)
    # 五 52–62 戰車：平地一聲雷
    s.hit(52.4, 'timpani', 'drum1', .9); s.hit(52.4, 'clash', 'crash', .5); s.hit(53.1, 'timpani', 'drum3', .7)
    section(s, 53, [(3, 'E1', ['E3', 'G#3', 'B3']), (3, 'A1', ['E3', 'A3', 'C#4']), (3, 'B1', ['F#3', 'B3', 'D#4'])], 'brass', .6)
    melody(s, 53.5, 'trumpet', 'E4:1 B4:1 E5:2 D#5:1 B4:1 G#4:2', vel=.5)
    # 六 62–76 一波又一波：三次輸入
    section(s, 62, [Em, C, (6, 'D2', ['D3', 'A3', 'F#4'])], 'pad', .45)
    melody(s, 63.5, 'horn', 'B3:1 E4:2 G4:1', vel=.5)
    s.hit(68.5, 'timpani', 'drum2', .6); s.chord(68.5, 'trombone', ['D2', 'A2'], 3, .45)
    for k in range(6): s.hit(68.5 + k * .5, 'snare', 'off', .3)
    s.chord(73, 'violins', ['F#5', 'A5', 'D6'], 3, .4, .2); s.n(73, 'tubular_bells', 'D5', 3, .3)
    # 七 76–90 瓦房店化：同一個動機，一次比一次殘缺
    motif = ['E6', 'G6', 'B6', 'A6', 'G6', 'E6', 'D6', 'E6']
    for rep in range(4):
        t0 = 76 + rep * 3.4
        keep = [p for i, p in enumerate(motif) if (i * 7 + rep * 3) % 8 >= rep * 2]
        for i, p in enumerate(keep):
            s.n(t0 + i * .4, 'glockenspiel', p, 1.2, .35 - .06 * rep, .2)
    section(s, 76, [Em, Am, C, (2, 'B1', ['D#3', 'F#3', 'B3'])], 'darkpad', .35)
    # 八 90–102 官僚的訂單：機械的進行曲
    section(s, 90, [(4, 'E2', ['E3', 'G3', 'B3']), (4, 'A1', ['E3', 'A3', 'C4']), (4, 'B1', ['D#3', 'F#3', 'B3'])], 'march', .45)
    # 九 102–118 顏料：從豐富到只剩黑白
    prog = [(4, 'G2', ['G3', 'B3', 'D4']), (4, 'E2', ['E3', 'G3', 'B3']), (4, 'C2', ['C3', 'E3', 'G3']), (4, 'D2', ['D3', 'F#3', 'A3'])]
    section(s, 102, prog[:2], 'pad', .45); section(s, 102, prog[:2], 'harp', .45)
    for k, p in enumerate(['B5', 'D6', 'G6', 'D6', 'B5', 'G5']):
        s.n(102.5 + k * .66, 'glockenspiel', p, 1.5, .25, .3)
    section(s, 110, prog[2:3], 'pad', .3)
    t = 102
    for b, bass, notes in prog:
        s.n(t, 'piano', bass, b, .4, -.1); s.n(t, 'piano', up(bass, 2), b, .3, .1)
        t += b
    melody(s, 106, 'piano', 'D5:2 B4:1 G4:1 E5:2 D5:2 C5:2 B4:2 A4:4', vel=.4)
    # 十 118–132 夜河：資金流
    section(s, 118, [(4, 'G1', ['D3', 'G3', 'B3']), (4, 'C2', ['E3', 'G3', 'C4']), (6, 'D2', ['D3', 'F#3', 'A3'])], 'folk', .45)
    section(s, 118, [(4, 'G1', ['D3', 'G3', 'B3']), (4, 'C2', ['E3', 'G3', 'C4']), (6, 'D2', ['D3', 'F#3', 'A3'])], 'pad', .3)
    bells(s, 123, ['D6', 'G6', 'A6', 'B6', 'D7', 'B6', 'G6', 'A6', 'E6', 'D6'], step=.85)
    # 十一 132–150 壞人：日落
    section(s, 132, [(4, 'E1', ['B2', 'E3', 'G3']), (4, 'C2', ['C3', 'G3', 'E4']), (4, 'A1', ['A2', 'E3', 'C4']), (6, 'E1', ['B2', 'E3', 'G#3'])],
            'darkpad', .4)
    section(s, 132, [(4, 'E2', ['B3']), (4, 'C2', ['G3']), (4, 'A1', ['E4']), (6, 'E2', ['G#3'])], 'sparse_piano', .45)
    s.n(144, 'tubular_bells', 'E4', 4, .3); s.n(144, 'erhu', 'B4', 4, .35, .2)
    s.render(D, name='film4')


def film5():
    s = Score(55); D = 154.0
    Dm = (4, 'D2', ['D3', 'F3', 'A3']); Bb = (4, 'Bb1', ['D3', 'F3', 'Bb3']); Gm = (4, 'G1', ['D3', 'G3', 'Bb3']); A7 = (4, 'A1', ['C#3', 'G3', 'E4'])
    F = (4, 'F1', ['C3', 'F3', 'A3']); C = (4, 'C2', ['E3', 'G3', 'C4'])
    # 0–14 費拉
    section(s, 0, [Dm, Bb, Gm, (2, 'A1', ['C#3', 'E3', 'A3'])], 'darkpad', .45)
    section(s, 0, [(4, 'D2', ['A3']), (4, 'Bb1', ['F3']), (4, 'G1', ['D4']), (2, 'A1', ['E4'])], 'sparse_piano', .45)
    # 14–28 有機 → 原子：彈撥旋律轉為木魚嘀嗒
    section(s, 14, [Dm, (3, 'C2', ['E3', 'G3', 'C4'])], 'zither', .5)
    section(s, 21, [(4, 'Bb1', ['D3', 'F3']), (3, 'A1', ['C#3', 'E3'])], 'clock', .5)
    # 28–40 一模一樣的門
    section(s, 28, [Dm, Gm, A7], 'clock', .45)
    bells(s, 29, ['D6', 'F6', 'A6', 'D7', 'A6', 'F6', 'D6'], step=.7)
    # 40–54 孤塔與大樹
    section(s, 40, [Dm, Bb, F, (2, 'A1', ['C#3', 'E3', 'A3'])], 'darkpad', .45)
    melody(s, 48, 'cellos', 'F3:1 A3:1 D4:2 C4:1 A3:1 F3:2', vel=.45)
    # 54–66 流民
    section(s, 54, [Dm, Gm, (4, 'A1', ['C#3', 'E3', 'A3'])], 'folk', .45)
    melody(s, 55, 'erhu', 'A4:1 D5:1 F5:2 E5:1 D5:1 C#5:2 D5:1 A4:1 F4:2', vel=.5)
    # 66–82 韭菜：割了又長
    section(s, 66, [Dm, Dm, Bb, A7], 'pizz', .45)
    for tc in (68, 74, 79.5):
        s.hit(tc, 'gran_cassa', 'hit', .5); s.hit(tc, 'clash', 'short', .3)
        for k in range(8): s.n(tc + k * .45, 'cellos_spic', 'D2', .3, .5, -.2)
    # 82–94 搖籃：小調搖籃曲
    section(s, 82, [Dm, Gm, (4, 'A1', ['C#3', 'E3', 'A3'])], 'music_box', .5)
    melody(s, 82.5, 'celesta' if False else 'vibraphone', 'A5:1 F5:1 D5:2 E5:1 F5:1 E5:2 C#5:1 E5:1 A4:2', vel=.35)
    # 94–108 演化不能爬山坡：旋律往上又落回
    section(s, 94, [F, C, Dm, (2, 'A1', ['C#3', 'E3', 'A3'])], 'arp_piano', .45)
    melody(s, 95, 'flute', 'F5:1 G5:1 A5:1 C6:1 D6:1 C6:.5 A5:.5 F5:2 G5:1 A5:1 Bb5:1 A5:1 F5:2', vel=.4)
    # 108–122 紙牌屋：門一開就塌
    section(s, 108, [(4, 'D2', ['F3', 'A3']), (3.6, 'Bb1', ['D3', 'F3'])], 'pizz', .35)
    s.hit(115.6, 'gong', None, .6); s.hit(115.6, 'gran_cassa', 'hit', .6); s.hit(115.7, 'clash', 'crash', .4)
    for k, p in enumerate(['D7', 'A6', 'F6', 'D6', 'A5', 'F5', 'D5', 'A4', 'F4', 'D4', 'A3']):
        s.n(115.7 + k * .07, 'harp', p, 2, .4, .3 - k * .05, jit=0)
    s.n(118, 'contrabass', 'D1', 4, .3, -.2)
    # 122–136 盛世：空洞的銅管 + 煙花
    section(s, 122, [(4, 'F1', ['F3', 'A3', 'C4']), (4, 'Bb1', ['F3', 'Bb3', 'D4']), (6, 'C2', ['G3', 'C4', 'E4'])], 'brass', .5)
    for tb in [0.5, 1.6, 2.8, 3.9, 5.0, 6.4, 7.7, 9.0, 10.4, 11.8]:
        s.hit(122 + tb + 1.1, 'timpani', 'drum3', .4); s.n(122 + tb + 1.12, 'glockenspiel', 'C7', 1, .2, .3)
    # 136–154 流沙之後：轉入大調的微光
    section(s, 136, [Dm, Bb, (4, 'F1', ['C3', 'F3', 'A3']), (6, 'C2', ['E3', 'G3', 'C4'])], 'pad', .4)
    section(s, 136, [(4, 'D2', ['A3']), (4, 'Bb1', ['F3']), (4, 'F1', ['C4']), (6, 'C2', ['E4'])], 'sparse_piano', .45)
    bells(s, 145.5, ['C6', 'E6', 'G6', 'A6', 'C7'], step=.9)
    s.chord(148, 'piano', ['F2', 'C3', 'A3', 'C4', 'F4'], 5, .35, strum=.1); s.n(148, 'tubular_bells', 'F4', 4, .3)
    s.render(D, name='film5')


def film6():
    s = Score(66); D = 179.0
    G = (4, 'G1', ['D3', 'G3', 'B3']); C = (4, 'C2', ['E3', 'G3', 'C4']); Em = (4, 'E2', ['E3', 'G3', 'B3']); Dd = (4, 'D2', ['D3', 'F#3', 'A3'])
    Am = (4, 'A1', ['E3', 'A3', 'C4'])
    # 0–13 細胞膜
    section(s, 0, [G, Em, C, (1, 'D2', ['D3', 'F#3', 'A3'])], 'pad', .4)
    for k in range(22):
        s.n(6.5 + k * .25, 'harp', ['G4', 'B4', 'D5', 'G5', 'B5', 'D6', 'G6', 'D6', 'B5', 'G5', 'D5'][k % 11], 1.5, .3, -.4 + .04 * k)
    # 13–25 名字
    section(s, 13, [G, C, (4, 'D2', ['D3', 'F#3', 'A3'])], 'folk', .5)
    melody(s, 13.5, 'flute', 'D5:1 G5:1 A5:1 B5:1 A5:1 G5:1 E5:2 D5:1 E5:1 F#5:2', vel=.4)
    # 25–37 泡沫
    section(s, 25, [Em, C, (4, 'D2', ['D3', 'F#3', 'A3'])], 'music_box', .5)
    s.n(35.5, 'glockenspiel', 'E7', 1, .4); s.chord(35.55, 'violins_pizz', ['E5', 'B5', 'E6'], .5, .4, .3)
    # 37–51 國王被刪掉
    section(s, 37, [(4, 'G1', ['D3', 'G3', 'B3']), (4, 'C2', ['E3', 'G3', 'C4'])], 'brass', .55)
    section(s, 45, [(3, 'E2', ['E3', 'G3', 'B3']), (3, 'C2', ['E3', 'G3', 'C4'])], 'pad', .4)
    melody(s, 45.5, 'violin', 'B4:1 C5:1 D5:2 E5:1 G5:2', vel=.35)
    # 51–65 語言的三角洲
    section(s, 51, [Am, (4, 'F1', ['C3', 'F3', 'A3']), C, (2, 'G1', ['D3', 'G3', 'B3'])], 'zither', .45)
    section(s, 51, [Am, (4, 'F1', ['C3', 'F3', 'A3']), C, (2, 'G1', ['D3', 'G3', 'B3'])], 'harp', .3)
    melody(s, 52, 'flute', 'E5:1 A5:1 C6:2 B5:1 A5:1 G5:2 A5:1 E5:1 C5:2', vel=.38)
    # 65–79 熊
    section(s, 65, [(4, 'E1', ['B2', 'E3', 'G3']), (4, 'F1', ['C3', 'F3', 'Ab3']), (6, 'E1', ['B2', 'E3', 'G#3'])], 'trem', .45)
    s.n(65, 'tuba', 'E1', 14, .35, -.2)
    # 79–92 樹木、木材、雲彩
    section(s, 79, [(4.5, 'G1', ['D3', 'G3', 'B3']), (4.5, 'E1', ['E3', 'G3', 'C4']), (4, 'C2', ['E3', 'A3', 'C4'])], 'chorale', .5)
    # 92–104 胎死腹中的發明
    section(s, 92, [Am, (4, 'F1', ['A3']), (4, 'C2', ['E4'])], 'sparse_piano', .45)
    bells(s, 96, ['A5', 'C6', 'E6', 'G6'], step=1.6)
    # 104–118 迴力鏢
    section(s, 104, [G, Dd, Em, (2, 'C2', ['E3', 'G3', 'C4'])], 'pizz', .5)
    for k in range(16): s.n(105.5 + k * .55, 'flute_stac', ['G5', 'B5', 'D6', 'G6', 'D6', 'B5', 'A5', 'F#5'][k % 8], .3, .3, .2)
    s.hit(115.6, 'timpani', 'drum1', .8); s.hit(115.6, 'clash', 'short', .4)
    # 118–131 邊界不一致
    section(s, 118, [(4, 'C2', ['C3', 'Eb3', 'G3']), (4, 'Db2', ['F3', 'Ab3', 'Db4']), (5, 'C2', ['E3', 'G3', 'C4'])], 'darkpad', .45)
    bells(s, 125, ['C6', 'E6', 'G6', 'D6', 'A6'], step=.9)
    # 131–147 邊界先於左右
    section(s, 131, [(4, 'A1', ['E3', 'A3', 'C4']), (4, 'D2', ['F3', 'A3', 'D4']), (4, 'E1', ['E3', 'G#3', 'B3']), (4, 'A1', ['E3', 'A3', 'C4'])], 'march', .45)
    # 147–161 蝴蝶
    section(s, 147, [C, (4, 'A1', ['E3', 'A3', 'C4']), (4, 'F1', ['C3', 'F3', 'A3']), (2, 'G1', ['D3', 'G3', 'B3'])], 'harp', .45)
    melody(s, 148, 'flute', 'G5:1 E5:1 C6:2 B5:1 A5:1 G5:2 A5:1 C6:1 E6:2', vel=.42)
    # 161–179 諸夏
    fin = [(4, 'C2', ['E3', 'G3', 'C4']), (4, 'G1', ['D3', 'G3', 'B3']), (4, 'A1', ['E3', 'A3', 'C4']), (6, 'F1', ['C3', 'F3', 'A3'])]
    section(s, 161, fin, 'pad', .5); section(s, 161, fin, 'folk', .4)
    melody(s, 161.5, 'horn', 'G3:1 C4:1 E4:2 D4:1 B3:1 G3:2 A3:1 C4:1 E4:2 F4:2 E4:2', vel=.5)
    bells(s, 168, ['C6', 'E6', 'G6', 'C7', 'G6', 'E6'], step=.8)
    s.chord(174, 'piano', ['C2', 'G2', 'E3', 'G3', 'C4', 'E4'], 5, .35, strum=.1); s.n(174, 'tubular_bells', 'C5', 4, .3)
    s.render(D, name='film6')


def film7():
    s = Score(77); D = 168.0
    Dd = (4, 'D2', ['D3', 'F#3', 'A3']); G = (4, 'G1', ['D3', 'G3', 'B3']); A = (4, 'A1', ['E3', 'A3', 'C#4']); Bm = (4, 'B1', ['D3', 'F#3', 'B3'])
    C = (4, 'C2', ['E3', 'G3', 'C4']); Em = (4, 'E2', ['E3', 'G3', 'B3'])
    # 0–13 林中小路
    section(s, 0, [Dd, G, (5, 'A1', ['E3', 'A3', 'C#4'])], 'harp', .45)
    melody(s, 1.5, 'recorder', 'A4:1 D5:1 E5:1 F#5:1 E5:2 D5:1 B4:1 A4:2 F#4:1 A4:2', vel=.45)
    # 13–26 父老的口傳
    section(s, 13, [Dd, Bm, G, (1, 'A1', ['E3', 'A3', 'C#4'])], 'organ', .45)
    melody(s, 14, 'cellos', 'D3:2 F#3:1 A3:1 B3:2 A3:2 G3:2 F#3:2', vel=.4)
    # 26–39 國王在社會之中
    section(s, 26, [G, Dd, (5, 'A1', ['E3', 'A3', 'C#4'])], 'pad', .45)
    melody(s, 27, 'horn', 'D4:1 F#4:1 A4:2 G4:1 F#4:1 E4:2 D4:1 E4:1 F#4:2', vel=.45)
    # 39–54 判例的市場：熱鬧的撥弦
    section(s, 39, [Dd, (4, 'C2', ['E3', 'G3', 'C4']), G, (3, 'D2', ['D3', 'F#3', 'A3'])], 'folk', .55)
    section(s, 39, [Dd, (4, 'C2', ['E3', 'G3', 'C4']), G, (3, 'D2', ['D3', 'F#3', 'A3'])], 'pizz', .35)
    melody(s, 40, 'recorder', 'D5:.5 E5:.5 F#5:1 A5:1 G5:.5 F#5:.5 E5:1 C5:1 D5:.5 E5:.5 G5:1 F#5:1 D5:2', vel=.45)
    bells(s, 50, ['A5', 'D6', 'F#6'], step=.5)
    # 54–67 契約：莊重
    section(s, 54, [Bm, G, Dd, (1, 'A1', ['E3', 'A3', 'C#4'])], 'chorale', .5)
    s.n(56, 'tubular_bells', 'D4', 4, .3); s.n(62, 'tubular_bells', 'A4', 4, .25)
    # 67–80 秩序的網絡
    section(s, 67, [Dd, A, Bm, (1, 'G1', ['D3', 'G3', 'B3'])], 'harp', .45)
    section(s, 67, [Dd, A, Bm, (1, 'G1', ['D3', 'G3', 'B3'])], 'pad', .35)
    for k in range(12): s.n(68 + k * .9, 'hand_chimes', ['D6', 'F#6', 'A6', 'B6'][k % 4], 1.5, .2, .3 * np.sin(k))
    # 80–94 莊園之夜，流官走來
    section(s, 80, [(4, 'B1', ['D3', 'F#3', 'B3']), (4, 'G1', ['D3', 'G3', 'B3']), (6, 'E1', ['E3', 'G3', 'B3'])], 'darkpad', .4)
    for k in range(7): s.hit(87 + k, 'woodblock', 'a', .35, .3)
    # 94–107 國王法庭：騎手
    section(s, 94, [Dd, G, (5, 'A1', ['E3', 'A3', 'C#4'])], 'gallop', .45)
    melody(s, 95, 'trumpet', 'D4:1 A4:1 D5:2 C#5:1 A4:1 E4:2', vel=.4)
    # 107–122 從決鬥到陪審團
    section(s, 107, [(4, 'E2', ['E3', 'G3', 'B3']), (4, 'C2', ['E3', 'G3', 'C4'])], 'trem', .4)
    section(s, 115, [G, (3, 'D2', ['D3', 'F#3', 'A3'])], 'chorale', .5)
    # 122–135 絕對主義：華麗的外殼
    section(s, 122, [Dd, (4, 'G1', ['D3', 'G3', 'B3']), (5, 'A1', ['E3', 'A3', 'C#4'])], 'brass', .4)
    section(s, 127, [(4, 'G1', ['B2', 'D3']), (4, 'A1', ['C#3', 'E3'])], 'folk', .45)
    # 135–149 沒有主權者
    section(s, 135, [Bm, G, Dd, (2, 'A1', ['E3', 'A3', 'C#4'])], 'organ', .4)
    melody(s, 136, 'violin', 'F#5:2 E5:1 D5:1 B4:2 A4:2 D5:2 F#5:2', vel=.35)
    # 149–168 周政與秦政
    section(s, 149, [G, (4, 'E2', ['E3', 'G3', 'B3']), C, (7, 'D2', ['D3', 'F#3', 'A3'])], 'pad', .45)
    section(s, 149, [G, (4, 'E2', ['E3', 'G3', 'B3']), C, (7, 'D2', ['D3', 'F#3', 'A3'])], 'harp', .35)
    melody(s, 150, 'recorder', 'A4:1 D5:1 E5:1 F#5:1 E5:2 D5:1 B4:1 A4:2 F#4:1 A4:3', vel=.4)
    s.chord(163, 'piano', ['D2', 'A2', 'F#3', 'A3', 'D4'], 5, .35, strum=.1); s.n(163, 'tubular_bells', 'D5', 4, .3)
    s.render(D, name='film7')


def film8():
    s = Score(88); D = 154.0
    Am = (4, 'A1', ['E3', 'A3', 'C4']); F = (4, 'F1', ['C3', 'F3', 'A3']); G = (4, 'G1', ['D3', 'G3', 'B3']); E = (4, 'E1', ['E3', 'G#3', 'B3'])
    Dm = (4, 'D2', ['D3', 'F3', 'A3']); C = (4, 'C2', ['E3', 'G3', 'C4'])
    # 0–13 兩個村莊
    section(s, 0, [Am, F, G, (1, 'E1', ['E3', 'G#3', 'B3'])], 'darkpad', .45)
    melody(s, 2, 'horn', 'A3:1 C4:1 E4:2 D4:1 C4:1 B3:2', vel=.45)
    s.hit(7, 'timpani', 'drum1', .7); s.hit(7, 'gong2', 'small', .3)
    # 13–27 議事的火堆：手鼓
    section(s, 13, [Am, (4, 'G1', ['D3', 'G3', 'B3']), F, (2, 'E1', ['E3', 'G#3', 'B3'])], 'darkpad', .45)
    for k in range(28):
        s.hit(13 + k * .5, 'frame_drum', 'large' if k % 4 == 0 else 'small', .45 if k % 4 == 0 else .3)
    melody(s, 15, 'cellos', 'A2:1 C3:1 E3:2 D3:1 C3:1 A2:2 G2:1 A2:3', vel=.5)
    # 27–39 寡婦與撫卹金
    section(s, 27, [Am, Dm, (4, 'E1', ['E3', 'G#3', 'B3'])], 'pad', .35)
    melody(s, 28, 'violin', 'E5:2 C5:1 A4:1 D5:2 F5:1 E5:1 B4:2 A4:2', vel=.38)
    # 39–51 女王的賬本
    section(s, 39, [C, (4, 'G1', ['D3', 'G3', 'B3']), (4, 'A1', ['E3', 'A3', 'C4'])], 'chorale', .5)
    s.n(39.5, 'harpsichord', 'C5', 1, .4, .2); s.n(40, 'harpsichord', 'E5', 1, .35, .2); s.n(40.5, 'harpsichord', 'G5', 1, .35, .2)
    # 51–65 追隨者離開
    for k, (b, n) in enumerate([('A1', ['E3', 'A3', 'C4']), ('F1', ['C3', 'F3', 'A3']), ('D2', ['D3', 'F3', 'A3'])]):
        section(s, 51 + k * 4.6, [(4.6, b, n)], 'march', .55 - .15 * k)
    s.n(64, 'contrabass', 'A1', 2, .3)
    # 65–79 勇敢與公正
    section(s, 65, [Am, F, C, (2, 'G1', ['D3', 'G3', 'B3'])], 'brass', .55)
    melody(s, 65.5, 'trumpet', 'E4:1 A4:1 C5:2 B4:1 A4:1 E4:2 F4:1 A4:1 C5:2 B4:2', vel=.5)
    # 79–94 土豪與民兵
    section(s, 79, [Am, G, F, (3, 'E1', ['E3', 'G#3', 'B3'])], 'folk', .5)
    section(s, 85, [(4, 'F1', ['C3', 'F3', 'A3']), (5, 'E1', ['E3', 'G#3', 'B3'])], 'march', .4)
    bells(s, 88, ['E6', 'A6', 'C7', 'B6', 'E6', 'A6'], step=.5)
    # 94–108 鹽與雇傭兵；劍 → 筆 → 鈴
    section(s, 94, [Dm, (4, 'A1', ['C#3', 'E3', 'A3'])], 'clock', .45)
    section(s, 102, [(6, 'D2', ['D3', 'F3', 'A3'])], 'music_box', .4)
    s.n(105.8, 'tubular_bells', 'A4', 3, .3)
    # 108–122 龍騎兵之後就是洪水
    section(s, 108, [Am, (4, 'F1', ['C3', 'F3', 'A3']), (6, 'E1', ['B2', 'E3', 'G#3'])], 'trem', .5)
    s.hit(116, 'gran_cassa', 'cresc', .5); s.hit(120, 'gran_cassa', 'roll', .45)
    # 122–136 逆淘汰：花謝，抗藥的雜草長起來
    section(s, 122, [(4, 'A1', ['E3', 'A3', 'C4'])], 'pizz', .45)
    section(s, 126, [(4, 'A1', ['Bb2', 'E3', 'A3']), (6, 'Ab1', ['D3', 'G3', 'C4'])], 'darkpad', .5)
    for k in range(8): s.n(128 + k * .9, 'bassoon', ['A2', 'Bb2', 'C3', 'Bb2', 'A2', 'G#2', 'A2', 'Bb2'][k], 1, .4, -.2)
    # 136–154 石橋與新橋
    section(s, 136, [Am, (4, 'F1', ['C3', 'F3', 'A3']), (1.5, 'E1', ['B2', 'E3', 'G#3'])], 'trem', .5)
    s.hit(145.4, 'gong', None, .6); s.hit(145.5, 'gran_cassa', 'hit', .6)
    section(s, 146, [(4, 'F1', ['C3', 'F3', 'A3']), (4, 'E1', ['E3', 'G#3', 'B3'])], 'brass', .45)
    s.chord(150, 'violins', ['E5', 'A5', 'C#6'], 4, .35, .2); s.chord(150, 'piano', ['A1', 'E2', 'C#3', 'E3', 'A3'], 4, .35, strum=.1)
    s.n(150, 'tubular_bells', 'A4', 4, .3)
    s.render(D, name='film8')


def film9():
    s = Score(99); D = 167.0
    Dm = (4, 'D2', ['D3', 'F3', 'A3']); C = (4, 'C2', ['E3', 'G3', 'C4']); Bb = (4, 'Bb1', ['D3', 'F3', 'Bb3']); A = (4, 'A1', ['C#3', 'E3', 'A3'])
    G = (4, 'G1', ['D3', 'G3', 'B3']); F = (4, 'F1', ['C3', 'F3', 'A3'])
    # 0–13 起火點：一盞盞向東點亮
    section(s, 0, [Dm, C, (5, 'Bb1', ['D3', 'F3', 'Bb3'])], 'zither', .45)
    for k in range(10): s.n(2 + k * 1.1, 'hand_chimes', ['D5', 'E5', 'F5', 'A5', 'C6', 'D6', 'E6', 'F6', 'A6', 'D7'][k], 2, .25, -.5 + k * .1)
    # 13–25 大洪水
    section(s, 13, [(4, 'D1', ['A2', 'D3', 'F3']), (4, 'Bb0', ['F2', 'Bb2', 'D3']), (4, 'A0', ['E2', 'A2', 'C#3'])], 'trem', .55)
    s.hit(15, 'gran_cassa', 'cresc', .55); s.hit(19, 'gong', None, .5)
    # 25–39 黑匣子落下
    section(s, 25, [Dm, Bb, (6, 'A1', ['C#3', 'E3', 'A3'])], 'darkpad', .45)
    for k, p in enumerate(['A6', 'G6', 'F6', 'E6', 'D6', 'C6', 'A5', 'F5', 'D5']): s.n(26.5 + k * .45, 'glockenspiel', p, 1.2, .25, .3)
    s.hit(31, 'timpani', 'drum1', .8); s.n(31, 'tubular_bells', 'D4', 4, .4)
    # 39–52 十分之一的人保存典籍
    section(s, 39, [Dm, G, (5, 'A1', ['C#3', 'E3', 'A3'])], 'organ', .45)
    melody(s, 40, 'cellos', 'D3:1 F3:1 A3:2 G3:1 F3:1 E3:2 D3:4', vel=.4)
    # 52–65 壓縮膠囊
    section(s, 52, [(4, 'D2', ['A3']), (4, 'Bb1', ['F3']), (5, 'C2', ['E4'])], 'sparse_piano', .45)
    s.n(57, 'vibraphone', 'A5', 3, .35); s.n(58, 'glockenspiel', 'D7', 2, .3); bells(s, 64, ['D6', 'F6', 'A6'], step=.4)
    # 65–79 方舟
    section(s, 65, [Dm, (4, 'F1', ['C3', 'F3', 'A3']), C, (2, 'A1', ['C#3', 'E3', 'A3'])], 'pad', .4)
    section(s, 65, [Dm, (4, 'F1', ['C3', 'F3', 'A3']), C, (2, 'A1', ['C#3', 'E3', 'A3'])], 'harp', .35)
    melody(s, 66, 'oboe', 'A4:2 D5:1 E5:1 F5:2 E5:1 D5:1 C5:2 A4:2', vel=.4)
    # 79–94 陸地上的海洋
    section(s, 79, [Dm, C, (4, 'D2', ['D3', 'A3', 'D4']), (3, 'C2', ['E3', 'G3', 'C4'])], 'zither', .5)
    melody(s, 80, 'erhu', 'D5:1 E5:.5 F5:.5 A5:2 G5:1 F5:1 E5:2 D5:1 C5:1 D5:3', vel=.5)
    # 94–106 英國人以前的英國人
    section(s, 94, [Dm, (4, 'C2', ['C3', 'G3']), (4, 'D2', ['D3', 'A3'])], 'gallop', .55)
    melody(s, 95, 'horn', 'D4:1 A4:3 G4:1 F4:1 E4:2 D4:2', vel=.5)
    # 106–121 種子落進蠻族的沃土，長成大教堂
    section(s, 106, [F, C, (4, 'D2', ['D3', 'F3', 'A3']), (3, 'Bb1', ['D3', 'F3', 'Bb3'])], 'organ', .5)
    s.n(108.4, 'harp', 'D3', 2, .4)
    for k, p in enumerate(['F3', 'A3', 'C4', 'F4', 'A4', 'C5', 'F5']): s.n(110 + k * 1.2, 'tubular_bells', p, 3, .25, -.2 + k * .06)
    # 121–135 虔誠勝過神學
    section(s, 121, [Dm, (4, 'A1', ['C#3', 'E3', 'A3']), (6, 'Bb1', ['D3', 'F3', 'Bb3'])], 'darkpad', .4)
    s.n(130, 'hand_chimes', 'F6', 3, .3)
    # 135–148 蜂巢與脈象
    section(s, 135, [C, G, (5, 'F1', ['C3', 'F3', 'A3'])], 'arp_piano', .45)
    # 148–167 孤島與蒸汽：終曲
    fin = [(4, 'D2', ['D3', 'F#3', 'A3']), (4, 'G1', ['D3', 'G3', 'B3']), (4, 'A1', ['C#3', 'E3', 'A3']), (7, 'D2', ['D3', 'F#3', 'A3'])]
    section(s, 148, fin, 'pad', .45); section(s, 148, fin, 'harp', .35)
    melody(s, 149, 'flute', 'A5:1 F#5:1 D5:2 E5:1 F#5:1 G5:2 A5:1 B5:1 A5:2 F#5:3', vel=.4)
    s.chord(162, 'piano', ['D2', 'A2', 'F#3', 'A3', 'D4'], 5, .35, strum=.1); s.n(162, 'tubular_bells', 'D5', 4, .3)
    s.render(D, name='film9')


def film10():
    s = Score(1010); D = 167.0
    C = (4, 'C2', ['E3', 'G3', 'C4']); Am = (4, 'A1', ['E3', 'A3', 'C4']); F = (4, 'F1', ['C3', 'F3', 'A3']); G = (4, 'G1', ['D3', 'G3', 'B3'])
    Em = (4, 'E2', ['E3', 'G3', 'B3']); Dm = (4, 'D2', ['D3', 'F3', 'A3'])
    # 0–13 投胎：搖籃般的豎琴
    section(s, 0, [C, Am, (5, 'F1', ['C3', 'F3', 'A3'])], 'harp', .45)
    melody(s, 1.5, 'clarinet', 'G4:1 C5:1 E5:2 D5:1 C5:1 A4:2 G4:1 A4:1 C5:3', vel=.42)
    # 13–27 快樂：一滴、一閃，越來越短
    section(s, 13, [(4, 'A1', ['E3', 'A3']), (4, 'F1', ['C3', 'F3']), (6, 'E1', ['B2', 'E3'])], 'darkpad', .35)
    for k, td in enumerate([2, 5.5, 8.4, 10.6, 12.4, 13.8, 14.8]):
        s.n(13 + td, 'glockenspiel', ['E6', 'G6', 'A6', 'C7', 'D7', 'E7', 'G7'][k], 1.5, .4 - .03 * k, .1)
        s.n(13 + td, 'vibraphone', ['E5', 'G5', 'A5', 'C6', 'D6', 'E6', 'G6'][k], 1.2 - .1 * k, .3, -.1)
    # 27–42 拉磨的驢子：繞圈的固定音型
    section(s, 27, [C, G, Am, (3, 'F1', ['C3', 'F3', 'A3'])], 'pizz', .5)
    for k in range(30): s.n(27 + k * .5, 'bassoon_stac', ['C3', 'E3', 'G3', 'E3'][k % 4], .4, .4, -.2)
    melody(s, 29, 'clarinet', 'E5:1 G5:1 C6:2 B5:1 G5:1 E5:2 F5:1 A5:1 G5:3', vel=.38)
    # 42–55 十四天
    section(s, 42, [(4, 'D2', ['D3', 'F3', 'A3']), (4, 'Bb1', ['D3', 'F3', 'Bb3']), (5, 'A1', ['C#3', 'E3', 'A3'])], 'darkpad', .4)
    for k in range(14): s.n(45 + k * .35, 'hand_chimes', ['D6', 'F6', 'A6', 'E6'][k % 4], 1.5, .2, -.6 + k * .09)
    s.n(50, 'oud' if False else 'dan_tranh', 'A4', 2, .45, .2); s.n(51, 'dan_tranh', 'D5', 2, .4, .2)
    # 55–69 追蝴蝶
    section(s, 55, [F, C, G, (2, 'C2', ['E3', 'G3', 'C4'])], 'arp_piano', .45)
    melody(s, 56, 'flute', 'C6:.5 D6:.5 E6:1 G6:1 E6:.5 D6:.5 C6:1 A5:1 G5:1 A5:1 C6:2', vel=.38)
    # 69–81 軟綿綿的生活
    section(s, 69, [(4, 'F1', ['A3', 'C4', 'E4']), (4, 'D2', ['F3', 'A3', 'C4']), (4, 'G1', ['F3', 'B3', 'D4'])], 'pad', .35)
    section(s, 69, [(4, 'F1', ['A4']), (4, 'D2', ['F4']), (4, 'G1', ['D5'])], 'sparse_piano', .4)
    # 81–95 面具與漏水的桶
    section(s, 81, [Am, Dm, (6, 'E1', ['E3', 'G#3', 'B3'])], 'pizz', .4)
    for k in range(10): s.n(90 + k * .45, 'marimba', ['A5', 'E5', 'C5', 'A4'][k % 4], .5, .3, .4)
    # 95–108 身體上的船長：風雨
    section(s, 95, [(4, 'E1', ['B2', 'E3', 'G3']), (4, 'C2', ['C3', 'G3', 'E4']), (5, 'B1', ['B2', 'D#3', 'F#3'])], 'trem', .45)
    s.hit(99.5, 'timpani', 'drum1', .6)
    # 108–121 下水
    section(s, 108, [C, (5, 'G1', ['D3', 'G3', 'B3']), (4, 'Am'[0] and 'A1', ['E3', 'A3', 'C4'])], 'pad', .4)
    for k, p in enumerate(['C7', 'G6', 'E6', 'C6', 'G5', 'E5', 'C5', 'G4']): s.n(113.6 + k * .06, 'harp', p, 1.5, .4, .3, jit=0)
    melody(s, 115, 'clarinet', 'E4:1 G4:1 C5:2 E5:1 D5:1 C5:2', vel=.4)
    # 121–134 出殼
    section(s, 121, [F, (4, 'G1', ['D3', 'G3', 'B3']), (5, 'C2', ['E3', 'G3', 'C4'])], 'harp', .45)
    section(s, 127, [(7, 'C2', ['E3', 'G3', 'C4'])], 'music_box', .4)
    # 134–148 挖坑種樹，四季流轉
    section(s, 134, [C, Am, F, (2, 'G1', ['D3', 'G3', 'B3'])], 'folk', .5)
    for k in range(7): s.hit(134 + k * 2, 'frame_drum', 'large_muted', .4, .1)
    # 148–167 山脊上的人：決斷時刻
    fin = [(4, 'A1', ['E3', 'A3', 'C4']), (4, 'F1', ['C3', 'F3', 'A3']), (4, 'C2', ['E3', 'G3', 'C4']), (7, 'G1', ['D3', 'G3', 'B3'])]
    section(s, 148, fin, 'pad', .45); section(s, 148, fin, 'arp_piano', .35)
    melody(s, 149, 'cellos', 'A3:2 C4:1 E4:1 F4:2 E4:2 G4:2 C4:2 D4:4', vel=.45)
    s.chord(162, 'piano', ['C2', 'G2', 'E3', 'G3', 'C4'], 5, .35, strum=.1); s.n(162, 'tubular_bells', 'C5', 4, .28)
    s.render(D, name='film10')


if __name__ == '__main__':
    w = sys.argv[1] if len(sys.argv) > 1 else 'all'
    for f in ([k for k in list(globals()) if k.startswith('film')] if w == 'all' else [w]):
        globals()[f]()
