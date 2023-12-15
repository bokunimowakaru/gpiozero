#!/usr/bin/env python3
###############################################################################
# Example 3 ボタン [GPIO Zero 版] [HTTPクライアント搭載]
###############################################################################
#
# 参考文献：
# https://bokunimo.net/git/iot/blob/master/learning/example14_iot_btn.py
# https://bokunimo.net/git/iot/blob/master/learning/example09_LINE.py
# https://gpiozero.readthedocs.io/
#
#                   Copyright (c) 2019-2023 Wataru KUNINO https://bokunimo.net/
###############################################################################
'''
 ※LINE アカウントと LINE Notify 用のトークンが必要です。
    1. https://notify-bot.line.me/ へアクセス
    2. 右上のアカウントメニューから「マイページ」を選択
    3. アクセストークンの発行で「トークンを発行する」を選択
    4. トークン名「raspi」（任意）を入力
    5. 送信先のトークルームを選択する（「1:1でLINE Notifyから通知を受け取る」など）
    6. [発行する]ボタンでトークンが発行される
    7. [コピー]ボタンでクリップボードへコピー
    8. 下記のline_tokenに貼り付け
'''

line_token='xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
                                                # ↑ここにLINEのTOKENを入力

port = 17                                       # GPIO ポート番号=17 (11番ピン)

from gpiozero import Button                     # GPIO Zero のButtonを取得
from time import sleep                          # スリープ実行モジュールの取得
from signal import pause                        # シグナル待ち受けの取得
from sys import argv                            # 本プログラムの引数argvを取得
import urllib.request                           # HTTP通信ライブラリを組み込む
import json                                     # JSON変換ライブラリを組み込む

url_s = 'https://notify-api.line.me/api/notify' # アクセス先
head_dict = {'Authorization':'Bearer ' + line_token,
             'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}

def toLine(body):                               # LINEへメッセージを送信する
    print(head_dict)                            # 送信ヘッダhead_dictを表示
    print(body)                                 # 送信内容bodyを表示
    post = urllib.request.Request(url_s, body.encode(), head_dict)
    try:                                        # 例外処理の監視を開始
        res = urllib.request.urlopen(post)      # HTTPアクセスを実行
    except Exception as e:                      # 例外処理発生時
        print(e,url_s)                          # エラー内容と変数url_sを表示
        return                                  # 処理の中断
    res_str = res.read().decode()               # 受信テキストを変数res_strへ
    res.close()                                 # HTTPアクセスの終了
    if len(res_str):                            # 受信テキストがあれば
        print('Response:', res_str)             # 変数res_strの内容を表示
    else:                                       # 受信テキストが無いとき
        print('Done')                           # Doneを表示

print(argv[0])                                  # プログラム名を表示する
if len(argv) >= 2:                              # 引数があるとき
    port = int(argv[1])                         # 整数としてportへ代入
btn = Button(port)                              # ポート番号portをボタン入力に
btn.when_pressed = toLine('ボタンが押されました') # ボタンにLINE送信を割り当て
pause()                                         # 待ち受け待機する(永久ループ)
