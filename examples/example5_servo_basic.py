#!/usr/bin/env python3
###############################################################################
# Example 4 Servo PWM Control BASIC [GPIO Zero 版]
#
#                   Copyright (c) 2021-2023 Wataru KUNINO https://bokunimo.net/
###############################################################################
#
# 実行方法(例)：
# pi@raspberrypi:~/gpiozero/examples $ ./example5_servo.py 
#
# 最新版：
# https://bokunimo.net/git/gpiozero/blob/master/examples/example5_servo.py
#
# 参考文献：
# https://bokunimo.net/git/raspifan/blob/master/ex05_servo.py
# https://gpiozero.readthedocs.io/
#
###############################################################################

# ラズベリー・パイに接続した Tower Pro製 マイクロ・サーボモータSG90を
# キーボードから入力した角度の位置に回転して合わせます。。
# 回転時に約120mAの電流が流れます(電源5.2V, 無負荷, 実測値, ピーク電流除く)。
# servo > のプロンプトが表示されたら角度0～180を入力してください。
# 終了するには[Ctrl]キーを押しながら[C]を押してください。

port = 14                                   # GPIO ポート番号=14 (8番ピン)
pwm_min = 3.0  / 100 * 0.020                # 180°のときのPWM幅(秒)
pwm_max = 11.8 / 100 * 0.020                # 0°のときのPWM幅(秒)

from gpiozero import AngularServo           # AngularServo モジュールの取得

servo = AngularServo(port, min_pulse_width=pwm_min, max_pulse_width=pwm_max)

while True:                                 # 繰り返し処理
    print('servo',end=' > ');               # キーボード入力待ち表示
    deg_s =input()                          # キーボードから入力
    if len(deg_s)<0 or not deg_s.isdigit(): # 入力が数字でないとき
        continue                            # whileの先頭に戻る
    deg = -(int(deg_s) - 90)                # 角度値0～180を指示値±90に変換
    if deg < -90 or deg > 90:               # ±90度の範囲外のとき
        continue                            # whileの先頭に戻る
    print('PWM('+str(port)+')=', deg)       # ポート番号と変数valを表示
    servo.angle = deg                       # 指示値に応じたPWMをサーボに出力
