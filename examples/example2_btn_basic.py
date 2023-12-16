#!/usr/bin/env python3
###############################################################################
# Example 3 ボタン [GPIO Zero 版]
###############################################################################
#
# 参考文献：
# https://bokunimo.net/git/iot/blob/master/learning/example14_btn.py
# https://gpiozero.readthedocs.io/
#
#                   Copyright (c) 2019-2023 Wataru KUNINO https://bokunimo.net/
###############################################################################

port = 17                                       # GPIO ポート番号=17 (11番ピン)

from gpiozero import Button                     # GPIO Zero のButtonを取得
from signal import pause                        # シグナル待ち受けの取得
from sys import argv                            # 本プログラムの引数argvを取得

def pressed(bpdy = 'ボタンが押されました'):     # ボタンが押された時の処理
    print(body)                                 # メッセージを表示

print(argv[0])                                  # プログラム名を表示する
if len(argv) >= 2:                              # 引数があるとき
    port = int(argv[1])                         # 整数としてportへ代入
btn = Button(port)                              # ポート番号portをボタン入力に

btn.when_pressed = pressed                      # ボタンに関数pressedを割り当て
pause()                                         # 待ち受け待機する(永久ループ)
