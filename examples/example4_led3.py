#!/usr/bin/env python3
###############################################################################
# Example 4 フルカラー Lチカ BASIC [IoT対応：HTTPサーバ搭載]
###############################################################################
#
# 輝度0～9をRGBの各色に設定することができます。
#
# 本HTTPサーバへのアクセス方法(例)：
# http://127.0.0.1:8080/?R=3&G=6&B=8
#
# 最新版：
# https://bokunimo.net/git/gpiozero/blob/master/examples/example4_led3.py
#
# 参考文献：
# https://bokunimo.net/git/iot/blob/master/learning/example19_iot_ledpwm.py
# https://gpiozero.readthedocs.io/
#
#                   Copyright (c) 2019-2023 Wataru KUNINO https://bokunimo.net/
###############################################################################

port_R = 17                                     # 赤色LED用 GPIO ポート番号
port_G = 27                                     # 緑色LED用 GPIO ポート番号
port_B = 22                                     # 青色LED用 GPIO ポート番号

ports = [port_R, port_G, port_B]                # 各色のポート番号を配列変数へ
color = [0.0, 0.0, 0.0]                         # 初期カラー

from wsgiref.simple_server import make_server   # HTTPサーバ用モジュールの取得
from gpiozero import RGBLED                     # RGB LEDモジュールの取得
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
            color[i] = (int(val[0]) % 10) / 9   # 輝度数(10段階)の0～1に正規化
    print('Color =',color)                      # 配列変数colorの内容を表示
    led3.color = color                          # RGB LEDにcolor値を設定
    ok = 'Color=' + str(color) + '\r\n'         # 応答文を作成
    ok = ok.encode('utf-8')                     # バイト列へ変換
    start_response('200 OK', [('Content-type', 'text/plain; charset=utf-8')])
    return [ok]                                 # 応答メッセージを返却

led3 = RGBLED(red=ports[0], green=ports[1], blue=ports[2]) # RGB LED led3を生成
led3.color = color                              # 輝度50%で RGBの全てを点灯

httpd = make_server('', 8080, wsgi_app)         # ポート8080でHTTPサーバ実体化
print("HTTP port 8080")                         # 起動ポート番号の表示
httpd.serve_forever()                           # HTTPサーバを起動
