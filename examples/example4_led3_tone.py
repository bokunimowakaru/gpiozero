#!/usr/bin/env python3
###############################################################################
# Example 4 フルカラーLEDで色調を表示する
#
#                   Copyright (c) 2023-2024 Wataru KUNINO https://bokunimo.net/
###############################################################################
#
# Usage: ./example4_led3_tone.py [color [brightness]]
#
# pi@raspberrypi:~/gpiozero/examples $ ./example4_led3_tone.py 0      # 赤50%
# pi@raspberrypi:~/gpiozero/examples $ ./example4_led3_tone.py 60     # 黄50%
# pi@raspberrypi:~/gpiozero/examples $ ./example4_led3_tone.py 120    # 緑50%
# pi@raspberrypi:~/gpiozero/examples $ ./example4_led3_tone.py 240 10 # 青10%
#
# 参考文献：
# https://gpiozero.readthedocs.io/

port_R = 17                                     # 赤色LED用 GPIO ポート番号
port_G = 27                                     # 緑色LED用 GPIO ポート番号
port_B = 22                                     # 青色LED用 GPIO ポート番号

ports = [port_R, port_G, port_B]                # 各色のポート番号を配列変数へ
color = [0.5, 0.5, 0.5]                         # 初期カラー

from gpiozero import RGBLED                     # RGB LEDモジュールの取得
from time import sleep                          # スリープ実行モジュールの取得
from sys import argv                            # 本プログラムの引数argvを取得

def tone2rgb(tone_color=0, brightness=0.5):     # ToDo colorzeroに置き換えれるはず
    v = brightness
    if v > 1:
        v = 1.0
    elif v < 0:
        v = 0.0
    f = float(tone_color % 60) / 60.
    t = f * v
    q = v - t
    i = int((tone_color%360) / 60)
    rgb = []
    if i==0:
        rgb = [v, t, 0]                         # case 0: r=v; g=t; b=0; break;
    elif i==1:
        rgb = [q, v, 0]                         # case 1: r=q; g=v; b=0; break;
    elif i==2:
        rgb = [0, v, t]                         # case 2: r=0; g=v; b=t; break;
    elif i==3:
        rgb = [0, q, v]                         # case 3: r=0; g=q; b=v; break;
    elif i==4:
        rgb = [t, 0, v]                         # case 4: r=t; g=0; b=v; break;
    elif i==5:
        rgb = [v, 0, q]                         # case 5: r=v; g=0; b=q; break;
    return rgb

print('Usage:',argv[0],'[color [brightness]]')  # プログラム名を表示する
led3 = RGBLED(red=ports[0], green=ports[1], blue=ports[2]) # RGB LED led3を生成

tone_color = None
brightness = 0.5
if len(argv) >= 2:                              # 引数があるとき
    tone_color = int(argv[1])
if len(argv) >= 3:                              # 引数が2つあるとき
    brightness = int(argv[2])/100
if tone_color is not None:
    led3.color = tone2rgb(tone_color,brightness)
    sleep(5)
    exit()
else:
    tone_color = 0
while True:
    led3.color = tone2rgb(tone_color)
    tone_color += 1
    sleep(10/360)
