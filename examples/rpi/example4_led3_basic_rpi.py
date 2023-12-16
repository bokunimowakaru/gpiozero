#!/usr/bin/env python3
###############################################################################
# Example 4 フルカラー Lチカ BASIC [RPi.GPIO版]
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
#                   Copyright (c) 2019-2023 Wataru KUNINO https://bokunimo.net/
###############################################################################

port_R = 17                                     # 赤色LED用 GPIO ポート番号
port_G = 27                                     # 緑色LED用 GPIO ポート番号
port_B = 22                                     # 青色LED用 GPIO ポート番号

ports = [port_R, port_G, port_B]                # 各色のポート番号を配列変数へ
color = [5,5,5]                                 # 初期カラー
pwm = []

from RPi import GPIO                            # GPIOモジュールの取得
from signal import pause                        # シグナル待ち受けの取得
from sys import argv                            # 本プログラムの引数argvを取得

print('Usage:',argv[0],'[red green blue]')      # プログラム名を表示する
for i in range(len(argv)-1):                    # 引数があるとき
    color[i] = (int(argv[i+1]) % 10) / 9        # GPIOポート番号をport_chimeへ
print(color)                                    # 変数colorの値を表示

GPIO.setmode(GPIO.BCM)                          # ポート番号の指定方法の設定
for i in range( len(ports) ):                   # 各ポート番号のindexを変数iへ
    GPIO.setup(ports[i], GPIO.OUT)              # ports[i]のGPIOポートを出力に
    pwm.append( GPIO.PWM(ports[i], 1000) )      # PWM出力用のインスタンスを生成
    pwm[i].start(0)                             # PWM出力を開始。デューティ0％
for i in range( len(ports) ):                   # 各ポート番号のindexを変数iへ
    port = ports[i]                             # ポート番号をportsから取得
    if color[i] > 0:                            # 輝度が0以外の時
        w = int(10 ** (color[i] / 4.5))         # パルス幅wを設定(1～9⇒1～100)
    else:                                       # 輝度が0の時
        w = 0                                   # パルス幅を0％へ
    pwm[i].ChangeDutyCycle(w)
try:
    pause()                                     # 待ち受け待機する(永久ループ)
except KeyboardInterrupt:                       # キー割り込み発生時
    print('\nKeyboardInterrupt')                # キーボード割り込み表示
for i in range( len(ports) ):                   # 各ポート番号のindexを変数iへ
    pwm[i].stop()                               # PWM出力停止
    GPIO.cleanup(ports[i])                      # GPIOを未使用状態に戻す
exit()                                          # プログラムの終了
