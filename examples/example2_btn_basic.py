#!/usr/bin/env python3
###############################################################################
# Example 2 ボタン BASIC [GPIO Zero 版]
#
#                   Copyright (c) 2019-2023 Wataru KUNINO https://bokunimo.net/
###############################################################################
#
# 最新版：
# https://bokunimo.net/git/gpiozero/blob/master/examples/example2_btn_basic.py
#
# 参考文献：
# https://bokunimo.net/git/iot/blob/master/learning/example14_btn.py
# https://gpiozero.readthedocs.io/
###############################################################################

port = 26                                       # GPIO ポート番号=26(37番ピン)

from gpiozero import Button                     # GPIO Zero のButtonを取得
from signal import pause                        # シグナル待ち受けの取得
from sys import argv                            # 本プログラムの引数argvを取得

def pressed():                                  # ボタン押下時の処理の定義
    print('ボタンが押されました')               # メッセージを表示

print(argv[0])                                  # プログラム名を表示する
if len(argv) >= 2:                              # 引数があるとき
    port = int(argv[1])                         # 整数としてportへ代入
btn = Button(port, bounce_time=0.1)             # ポート番号portをボタン入力に

btn.when_pressed = pressed                      # ボタンに関数pressedを割り当て
pause()                                         # 待ち受け待機する(永久ループ)
