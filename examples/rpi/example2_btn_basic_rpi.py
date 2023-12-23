#!/usr/bin/env python3
###############################################################################
# Example 2 ボタン [RPi.GPIO版]
#
#                   Copyright (c) 2019-2023 Wataru KUNINO https://bokunimo.net/
###############################################################################
#
# 参考文献：
# https://bokunimo.net/git/iot/blob/master/learning/example14_btn.py
###############################################################################

port = 26                                       # GPIO ポート番号=26(37番ピン)

from RPi import GPIO                            # GPIOモジュールの取得
from time import sleep                          # スリープ実行モジュールの取得
from sys import argv                            # 本プログラムの引数argvを取得

def pressed():                                  # ボタン押下時の処理の定義
    print('ボタンが押されました')               # メッセージを表示

print(argv[0])                                  # プログラム名を表示する
if len(argv) >= 2:                              # 引数があるとき
    port = int(argv[1])                         # 整数としてportへ代入
GPIO.setmode(GPIO.BCM)                          # ポート番号の指定方法の設定
GPIO.setup(port, GPIO.IN, pull_up_down=GPIO.PUD_UP) # GPIO 26 を入力に

try:                                            # キー割り込みの監視を開始
    while True:                                 # 繰り返し処理
        sleep(0.1)                              # 0.1秒間の待ち時間処理
        b = GPIO.input(port)                    # GPIO入力値を変数bへ代入
        if b:                                   # ボタンが押されていない時
            continue                            # whileに戻る
        while b == 0:                           # ボタンが押されている間
            sleep(0.1)                          # 0.1秒間の待ち時間処理
            b = GPIO.input(port)                # GPIO入力値を変数bへ代入
        pressed()                               # ボタン押下時の処理を実行
except KeyboardInterrupt:                       # キー割り込み発生時
    print('\nKeyboardInterrupt')                # キーボード割り込み表示
GPIO.cleanup(port)                              # GPIOを未使用状態に戻す
exit()                                          # プログラムの終了
