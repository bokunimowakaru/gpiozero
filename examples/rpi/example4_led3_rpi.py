#!/usr/bin/env python3
###############################################################################
# Example 4 フルカラー Lチカ [RPi.GPIO版] [IoT対応：HTTPサーバ搭載]
#
#                   Copyright (c) 2019-2023 Wataru KUNINO https://bokunimo.net/
###############################################################################
#
# 輝度0～9をRGBの各色に設定することができます。
#
# 本HTTPサーバへのアクセス方法(例)：
# http://127.0.0.1:8080/?R=8&G=4&B=1
#
# 最新版：
# https://bokunimo.net/git/gpiozero/blob/master/examples/example4_led3.py
#
# 参考文献：
# https://bokunimo.net/git/iot/blob/master/learning/example19_iot_ledpwm.py
# https://gpiozero.readthedocs.io/
###############################################################################

port_R = 17                                     # 赤色LED用 GPIO ポート番号
port_G = 27                                     # 緑色LED用 GPIO ポート番号
port_B = 22                                     # 青色LED用 GPIO ポート番号

ports = [port_R, port_G, port_B]                # 各色のポート番号を配列変数へ
color = [0,0,0]                                 # 初期カラー
pwm = []

from wsgiref.simple_server import make_server   # HTTPサーバ用モジュールの取得
from RPi import GPIO                            # GPIOモジュールの取得
from urllib.parse import parse_qs               # クエリ・ストリングの解析用

def wsgi_app(environ, start_response):          # HTTPアクセス受信時の処理
    if environ['PATH_INFO'] != '/':             # リクエスト先がルート以外の時
        error='404 Not Found'                   # エラー処理
        start_response(error,[('Content-type','text/plain; charset=utf-8')])
        return [(error+'\r\n').encode('utf-8')] # 応答メッセージを返却
    query = environ.get('QUERY_STRING')         # 変数queryにHTTPクエリを代入
    query = parse_qs(query)                     # 辞書型に変換
    keys = ['R','G','B']                        # Query内の検索キーをkeysへ代入
    for i in range( len(keys) ):                # 検索キーのindexを変数iへ
        val = query.get(keys[i])                # キーを検索して値を取得する
        if val is not None and val[0].isdigit(): # 有効な値の時
            color[i] = int(val[0]) % 10         # 輝度数(10段階)の0～9に正規化
    print('Color =',color)                      # 配列変数colorの内容を表示
    for i in range( len(ports) ):               # 各ポート番号のindexを変数iへ
        port = ports[i]                         # ポート番号をportsから取得
        if color[i] > 0:                        # 輝度が0以外の時
            w = int(10 ** (color[i] / 4.5))     # パルス幅wを設定(1～9⇒1～100)
        else:                                   # 輝度が0の時
            w = 0                               # パルス幅を0％へ
        print('GPIO'+str(port),'=',w)           # ポート番号と変数wの値を表示
        pwm[i].ChangeDutyCycle(w)
    ok = 'Color=' + str(color) + '\r\n'         # 応答文を作成
    ok = ok.encode('utf-8')                     # バイト列へ変換
    start_response('200 OK', [('Content-type', 'text/plain; charset=utf-8')])
    return [ok]                                 # 応答メッセージを返却

GPIO.setmode(GPIO.BCM)                          # ポート番号の指定方法の設定
for i in range( len(ports) ):                   # 各ポート番号のindexを変数iへ
    GPIO.setup(ports[i], GPIO.OUT)              # ports[i]のGPIOポートを出力に
    pwm.append( GPIO.PWM(ports[i], 1000) )      # PWM出力用のインスタンスを生成
    pwm[i].start(0)                             # PWM出力を開始。デューティ0％

httpd = make_server('', 8080, wsgi_app)         # ポート8080でHTTPサーバ実体化
print("HTTP port 8080")                         # 起動ポート番号の表示
try:
    httpd.serve_forever()                       # HTTPサーバを起動
except KeyboardInterrupt:                       # キー割り込み発生時
    print('\nKeyboardInterrupt')                # キーボード割り込み表示
for i in range( len(ports) ):                   # 各ポート番号のindexを変数iへ
    pwm[i].stop()                               # PWM出力停止
    GPIO.cleanup(ports[i])                      # GPIOを未使用状態に戻す
exit()                                          # プログラムの終了
