#!/usr/bin/env python3
###############################################################################
# Example 2 チャイム [GPIO Zero 版] [HTTPサーバ搭載]
###############################################################################
#
# 参考文献：
# https://bokunimo.net/git/iot/blob/master/learning/example13_chime.py
# https://bokunimo.net/git/iot/blob/master/learning/example18_iot_chime_n.py
# https://gpiozero.readthedocs.io/
#
#                   Copyright (c) 2019-2023 Wataru KUNINO https://bokunimo.net/
###############################################################################

port = 4                                        # GPIO ポート番号 = 4 (7番ピン)
ping_f = 'C5'                                   # チャイム音の周波数1
pong_f = 'A4'                                   # チャイム音の周波数2

from wsgiref.simple_server import make_server   # HTTPサーバmake_serverを取得
from gpiozero import TonalBuzzer                # GPIO Zero のTonalBuzzerを取得
from gpiozero.tones import Tone                 # GPIO Zero のToneを取得
from time import sleep                          # スリープ実行モジュールの取得
from sys import argv                            # 本プログラムの引数argvを取得
import threading                                # スレッド用ライブラリの取得

def chime():                                    # チャイム（スレッド用）
    mutex.acquire()                             # mutex状態に設定(排他処理開始)
    pwm.play(Tone(ping_f))                      # PWM周波数の変更
    sleep(0.5)                                  # 0.5秒の待ち時間処理
    pwm.play(Tone(pong_f))                      # PWM周波数の変更
    sleep(0.5)                                  # 0.5秒の待ち時間処理
    pwm.stop()                                  # PWM出力停止
    mutex.release()                             # mutex状態の開放(排他処理終了)

def wsgi_app(environ, start_response):          # HTTPアクセス受信時の処理
    if environ['PATH_INFO'] == '/':             # リクエスト先がルートのとき
        thread = threading.Thread(target=chime) # 関数chimeをスレッド化
        thread.start()                          # スレッドchimeの起動
    ok = 'OK\r\n'                               # 応答メッセージ作成
    ok = ok.encode()                            # バイト列へ変換
    start_response('200 OK', [('Content-type', 'text/plain; charset=utf-8')])
    return [ok]                                 # 応答メッセージを返却

print(argv[0])                                  # プログラム名を表示する
if len(argv) >= 2:                              # 引数があるとき
    port_chime = int(argv[1])                   # GPIOポート番号をport_chimeへ

pwm = TonalBuzzer(port)                         # PWM出力用のインスタンスを生成
mutex = threading.Lock()                        # 排他処理用のオブジェクト生成

httpd = make_server('', 8080, wsgi_app)         # ポート8080でHTTPサーバ実体化
print("HTTP port 8080")                         # 起動ポート番号の表示
httpd.serve_forever()                           # HTTPサーバを起動
exit()                                          # プログラムの終了
