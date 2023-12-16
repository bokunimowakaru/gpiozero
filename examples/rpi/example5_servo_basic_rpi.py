#!/usr/bin/env python3
###############################################################################
# Example 4 Servo PWM Control BASIC [GPIO Zero 版]
#
#                   Copyright (c) 2021-2023 Wataru KUNINO https://bokunimo.net/
###############################################################################

# ラズベリー・パイに接続した Tower Pro製 マイクロ・サーボモータSG90を
# キーボードから入力した角度の位置に回転して合わせます。。
# 回転時に約120mAの電流が流れます(電源5.2V, 無負荷, 実測値, ピーク電流除く)。
# servo > のプロンプトが表示されたら角度0～180を入力してください。
# 終了するには[Ctrl]キーを押しながら[C]を押してください。

port = 14                                       # GPIO ポート番号=14 (8番ピン)
duty_min = 3.0                                  # 180°のときのPWMのDuty比
duty_max = 11.8                                 # 0°のときのPWMのDuty比

from RPi import GPIO                            # GPIOモジュールの取得

GPIO.setmode(GPIO.BCM)                          # ポート番号の指定方法の設定
GPIO.setup(port, GPIO.OUT)                      # ポートportのGPIOを出力に設定
pwm = GPIO.PWM(port, 50)                        # 50Hzを設定
pwm.start(0)                                    # PWM出力 0% (Lレベル)

try:                                            # キー割り込みの監視を開始
    while True:                                 # 繰り返し処理
        print('servo',end=' > ');               # キーボード入力待ち表示
        deg_s =input()                          # キーボードから入力
        if len(deg_s)<0 or not deg_s.isdigit(): # 入力が数字でないとき
            continue                            # whileの先頭に戻る
        deg = int(deg_s)                        # 整数値をdegに代入
        if deg < 0 or deg > 180:                # 0〜180の範囲外のとき
            continue                            # whileの先頭に戻る
        duty = (duty_max - duty_min) * (180 - deg) / 180 + duty_min                            pwm.ChangeDutyCycle(duty)               # サーボの制御を実行
        print('PWM('+str(port)+')=', duty)      # ポート番号と変数dutyを表示

except (KeyboardInterrupt,EOFError):            # キー割り込み発生時
    print('\nKeyboardInterrupt')                # キーボード割り込み表示
    GPIO.cleanup(port)                          # GPIOを未使用状態に戻す
    exit()                                      # 終了
