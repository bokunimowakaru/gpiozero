#!/usr/bin/env python3
###############################################################################
# Example 2 ボタン [GPIO Zero 版] [IoT対応：HTTPクライアント搭載]
#
#                   Copyright (c) 2019-2023 Wataru KUNINO https://bokunimo.net/
###############################################################################
#
# 最新版：
# https://bokunimo.net/git/gpiozero/blob/master/examples/example2_btn.py
#
# 参考文献：
# https://bokunimo.net/git/iot/blob/master/learning/example14_iot_btn.py
# https://bokunimo.net/git/iot/blob/master/learning/example09_LINE.py
# https://gpiozero.readthedocs.io/
###############################################################################
'''
 ※LINE アカウントと LINE Notify 用のトークンが必要です。
    1. https://notify-bot.line.me/ へアクセスしてログインする
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

port = 26                                       # GPIO ポート番号=26(37番ピン)

from gpiozero import Button                     # GPIO Zero のButtonを取得
from signal import pause                        # シグナル待ち受けの取得
from sys import argv                            # 本プログラムの引数argvを取得
import urllib.request                           # HTTP通信ライブラリを組み込む

url_s = 'https://notify-api.line.me/api/notify' # アクセス先
head_dict = {'Authorization':'Bearer ' + line_token,
             'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8'}

def toLine():                                   # LINEへメッセージを送信する
    print(head_dict)                            # 送信ヘッダhead_dictを表示
    body = 'message=ボタンが押されました'       # 送信するbody(message=)を作成
    print(body)                                 # 送信内容bodyを表示
    post = urllib.request.Request(url_s, body.encode(), head_dict)
    try:                                        # 例外処理の監視を開始
        res = urllib.request.urlopen(post)      # HTTPアクセスを実行
    except Exception as e:                      # 例外処理発生時
        print(e,url_s)                          # エラー内容と変数url_sを表示
        return                                  # 処理の中断
    res_str = res.read().decode()               # 受信テキストを変数res_strへ
    res.close()                                 # HTTPアクセスの終了
    print('Response:', res_str)                 # 変数res_strの内容を表示

print(argv[0])                                  # プログラム名を表示する
if len(argv) >= 2:                              # 引数があるとき
    port = int(argv[1])                         # 整数としてportへ代入
btn = Button(port, bounce_time=0.1)             # ポート番号portをボタン入力に

btn.when_pressed = toLine                       # ボタンにLINE送信を割り当て
pause()                                         # 待ち受け待機する(永久ループ)
