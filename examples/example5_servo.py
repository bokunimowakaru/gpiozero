#!/usr/bin/env python3
###############################################################################
# Example 5 Servo PWM Controled Heat Dissipation Mechanism for Raspberry Pi
#
#                   Copyright (c) 2021-2023 Wataru KUNINO https://bokunimo.net/
###############################################################################
#
# 実行方法(例)：
# pi@raspberrypi:~/gpiozero/examples $ ./example5_servo.py 
#
# 最新版：
# https://bokunimo.net/git/gpiozero/blob/master/examples/example5_servo.py
#
# 参考文献：
# https://bokunimo.net/git/raspifan/blob/master/ex08_emission.py
# https://gpiozero.readthedocs.io/
#
###############################################################################

# ラズベリー・パイのCPU温度が60℃を超えたときに Tower Pro製 マイクロ・サーボ
# SG90を制御し、ケースの上蓋を開いて排熱します。
# インターネット・ブラウザから、CPU温度の確認と、上蓋の開閉制御を行うことも
# 可能です。

# インターネット・ブラウザ等から http://127.0.0.1:8080/ にアクセスして下さい。
# 他のPCのインターネットブラウザからラズベリーパイのIPアドレスを指定して、
# 「http://192.168.XX.XX:8080/」のようにアクセスすることも出来ます。
# 終了するには[Ctrl]キーを押しながら[C]を押してください。

port = 14                                       # GPIO ポート番号=14 (8番ピン)
pwm_min = 0.0005                                # -90°のときのPWM幅(秒)
pwm_max = 0.0024                                # +90°のときのPWM幅(秒)
cover_closed_deg = 60                           # ケースが閉じているときの角度
cover_opened_deg =  0                           # ケースが開いているときの角度
cover_status = 1                                # ケース状態の閉=0、開=1
cover_deg = [cover_closed_deg,cover_opened_deg] # ケースの各状態の角度
temp_emit_on = 60                               # 放熱をON(ケース開)する温度
temp_emit_off = 55                              # 放熱をOFF(ケース閉)する温度
filename = '/sys/class/thermal/thermal_zone0/temp' # 温度値が書かれたファイル

from wsgiref.simple_server import make_server   # HTTPサーバ用モジュールの取得
from gpiozero import AngularServo               # AngularServo モジュールの取得
from time import sleep                          # スリープ実行モジュールの取得
import threading                                # スレッド管理を組み込む

def coverCtrl(cover):                           # ケース上蓋を開閉制御する関数
    global port, pwm_min, pwm_max, cover_status # 各値を取得
    if cover != cover_status:                   # カバーの状態変化あり
        deg = cover_deg[cover]                  # サーボの角度を代入
        servo.angle = deg                       # 指示値に応じたPWMをサーボに出力
        sleep(0.5)                              # 回転の完了待ち
        servo.detach()                          # 制御の停止
        #del servo                              # サーボの停止
        cover_status = cover                    # 状態値を更新する

def getTemp():                                  # CPUの温度値を取得する関数
    fp = open(filename)                         # CPU温度ファイルを開く
    temp = round(float(fp.read()) / 1000,1)     # ファイルを読み込み1000で除算
    fp.close()                                  # ファイルを閉じる
    print('CPU Temperature =', temp)            # CPU温度を表示する
    return temp                                 # CPU温度値を返却する

def barChart(name, val, max, color='green'):    # 棒グラフHTMLを作成する関数
    html = '<tr><td>' + name + '</td>\n'        # 棒グラフ名を表示
    html +='<td align="right">'+str(val)+'</td>\n' # 変数valの値を表示
    i = round(200 * val / max)                  # 棒グラフの長さを計算
    if val >= max * 0.75:                       # 75％以上のとき
        color = 'red'                           # 棒グラフの色を赤に
        if val > max:                           # 最大値(100％)を超えた時
            i = 200                             # グラフ長を200ポイントに
    html += '<td><div style="background-color:' + color
    html += '; width:' + str(i) + 'px">&nbsp;</div></td>\n'
    return html                                 # HTMLデータを返却

def wsgi_app(environ, start_response):          # HTTPアクセス受信時の処理
    if environ.get('PATH_INFO') != '/':         # パスがルート以外のとき
        start_response('404 Not Found',[])      # 404エラー設定
        return ['404 Not Found\r\n'.encode()]   # 応答メッセージ(404)を返却
    global cover_status                         # cover_statusの取得(Thread用)
    query = environ.get('QUERY_STRING')         # 変数queryにHTTPクエリを代入
    sp = query.find('=')                        # 変数query内の「=」を探す
    if sp >= 0 and sp + 1 < len(query) and query[sp+1:].isdigit(): # 有効範囲内
        val = int(query[sp+1:])                 # 取得値を変数valへ
        val %= 2                                # 2の剰余を代入
        coverCtrl(val)                          # サーボを動かす
    temp = getTemp()                            # 温度を取得
    html = '<html>\n<head>\n'                   # HTMLコンテンツを作成
    html += '<meta http-equiv="refresh" content="10;URL=/">\n' # 自動更新
    html += '</head>\n<body>\n'                 # 以下はHTML本文
    html += '<table border=1>\n'                # 作表を開始
    html += '<tr><th>項目</th><th width=50>値</th>' # 「項目」「値」を表示
    html += '<th width=200>グラフ</th>\n'       # 「グラフ」を表示
    html += barChart('CPU温度(℃)', temp, 80)   # 温度値を棒グラフ化
    html += barChart('ケース状態', cover_status, 1) 
    html += '</tr>\n</table>\n'                 # 作表の終了
    html += 'ケース制御 <a href="/?=0">閉じる</a> <a href="/?=1">開く</a>'
    html += '</body>\n</html>\n'                # htmlの終了
    start_response('200 OK', [('Content-type', 'text/html; charset=utf-8')])
    return [html.encode('utf-8')]               # 応答メッセージを返却

def httpd():                                    # HTTPサーバ用スレッド
    htserv = make_server('', 8080, wsgi_app)    # HTTPサーバ実体化
    print('HTTP port', 8080)                    # ポート番号を表示
    try:                                        # 例外処理の監視
        htserv.serve_forever()                  # HTTPサーバを起動
    except KeyboardInterrupt as e:              # キー割り込み発生時
        raise e                                 # キー割り込み例外を発生

servo=AngularServo(port,min_pulse_width=pwm_min,max_pulse_width=pwm_max)
coverCtrl(0)                                    # カバーを閉じる
thread = threading.Thread(target=httpd, daemon=True) # httpdの実体化
thread.start()                                  # httpdの起動
while thread.is_alive:                          # 永久ループ
    sleep(30)                                   # 30秒間の待ち時間処理
    temp = getTemp()                            # 温度値を取得
    if temp >= temp_emit_on:                    # 放出温度に達した
        coverCtrl(1)                            # カバーを開く
    if temp <= temp_emit_off:                   # 放出停止温度以下
        coverCtrl(0)                            # カバーを閉じる

'''
動作の一例：
pi@raspberrypi:~ $ cd␣~/gpiozero/examples⏎
pi@raspberrypi:~/gpiozero/examples $ ./example5_servo.py
/usr/lib/python3/dist-packages/gpiozero/output_devices.py:1509: PWMSoftwareFallback: To reduce servo jitter, use the pigpio pin factory.See https://gpiozero.readthedocs.io/en/stable/api_output.html#servo for more info
  warnings.warn(PWMSoftwareFallback(
HTTP port 8080
CPU Temperature = 48.5
127.0.0.1 - - [28/Dec/2023 09:16:17] "GET / HTTP/1.1" 200 513
CPU Temperature = 48.5
127.0.0.1 - - [28/Dec/2023 09:16:26] "GET /?=1 HTTP/1.1" 200 513
CPU Temperature = 48.0
CPU Temperature = 47.4
'''
