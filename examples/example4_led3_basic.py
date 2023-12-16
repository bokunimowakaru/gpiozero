#!/usr/bin/env python3
###############################################################################
# Example 4 フルカラー Lチカ BASIC [GPIO Zero 版]
#
#                   Copyright (c) 2019-2023 Wataru KUNINO https://bokunimo.net/
###############################################################################
#
# 輝度0～9をRGBの各色に設定することができます。
#
# 実行方法(例)：
# pi@raspberrypi:~/gpiozero/examples $ ./example4_led3_basic.py 8 4 1
#
# 最新版：
# https://bokunimo.net/git/gpiozero/blob/master/examples/example4_led3.py
#
# 参考文献：
# https://bokunimo.net/git/iot/blob/master/learning/example19_iot_ledpwm.py
# https://gpiozero.readthedocs.io/
#
###############################################################################

port_R = 17                                     # 赤色LED用 GPIO ポート番号
port_G = 27                                     # 緑色LED用 GPIO ポート番号
port_B = 22                                     # 青色LED用 GPIO ポート番号

ports = [port_R, port_G, port_B]                # 各色のポート番号を配列変数へ
color = [0.5, 0.5, 0.5]                         # 初期カラー

from gpiozero import RGBLED                     # RGB LEDモジュールの取得
from signal import pause                        # シグナル待ち受けの取得
from sys import argv                            # 本プログラムの引数argvを取得

print('Usage:',argv[0],'[red green blue]')      # プログラム名を表示する
for i in range(len(argv)-1):                    # 引数があるとき
    color[i] = (int(argv[i+1]) % 10) / 9        # GPIOポート番号をport_chimeへ
print(color)                                    # 変数colorの値を表示

led3 = RGBLED(red=ports[0], green=ports[1], blue=ports[2]) # RGB LED led3を生成
led3.color = color                              # 輝度50%で RGBの全てを点灯
pause()                                         # 待ち受け待機する(永久ループ)
