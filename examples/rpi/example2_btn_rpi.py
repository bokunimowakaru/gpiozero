#!/usr/bin/env python3
###############################################################################
# Example 3 ボタン [RPi.GPIO版] [HTTPクライアント搭載]
###############################################################################
#
# 参考文献：
# https://bokunimo.net/git/iot/blob/master/learning/example14_iot_btn.py
# https://bokunimo.net/git/iot/blob/master/learning/example09_LINE.py
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

port = 26                                       # GPIO ポート番号=26(37番ピン)

from RPi import GPIO                            # GPIOモジュールの取得
from time import sleep                          # スリープ実行モジュールの取得
from sys import argv                            # 本プログラムの引数argvを取得
import urllib.request                           # HTTP通信ライブラリを組み込む

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
        toLine('ボタンが押されました')          # LINE送信
except KeyboardInterrupt:                       # キー割り込み発生時
    print('\nKeyboardInterrupt')                # キーボード割り込み表示
GPIO.cleanup(port)                              # GPIOを未使用状態に戻す
exit()                                          # プログラムの終了
