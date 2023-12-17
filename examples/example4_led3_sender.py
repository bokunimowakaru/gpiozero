#!/usr/bin/env python3
###############################################################################
# Example 4 ラズベリー・パイのCPU温度を色情報に変換し、フルカラーLEDに送信する
#
#                   Copyright (c) 2023-2024 Wataru KUNINO https://bokunimo.net/
###############################################################################
#
# Usage: ./example4_led3_sender.py [temperature]
#
# 引き数なしで実行すると本機のCPU温度に相当する色情報をHTTPで送信し続けます。
# 引数があるときは、その引き数をCPU温度とした色情報をHTTPで送信し、終了します。
#
# 実行例：
# pi@raspberrypi:~/gpiozero/examples $ ./example4_led3.py & # HTTPサーバ起動
# [1] 5086
# HTTP port 8080
# pi@raspberrypi:~/gpiozero/examples $ ./example4_led3_sender.py # 送信機起動
# Usage: ./example4_led3_sender.py [temperature]
# CPU Temperature = 48.0
# Color = [0.1111111111111111, 0.4444444444444444, 0.0]
# 127.0.0.1 - - [17/Dec/2023 17:17:24] "GET /?R=1&G=4&B=0 HTTP/1.1" 200 53
# CPU Temperature = 48.5
# Color = [0.2222222222222222, 0.4444444444444444, 0.0]
# 127.0.0.1 - - [17/Dec/2023 17:17:34] "GET /?R=2&G=4&B=0 HTTP/1.1" 200 53
#
# url_sのIPアドレスをLAN上の他のラズベリーパイに設定することも出来ます。

url_s = 'http://127.0.0.1:8080/'                # アクセス先を変数url_sへ代入
temp_min = 30                                   # CPU温度の最小値(青色)
temp_max = 60                                   # CPU温度の最大値(赤色)
filename = '/sys/class/thermal/thermal_zone0/temp' # 温度値が書かれたファイル

import urllib.request                           # HTTP通信ライブラリを組み込む
from time import sleep                          # スリープ実行モジュールの取得
from sys import argv                            # 本プログラムの引数argvを取得

def httpSender(color):
    query =  '?R='+str(int(color[0]*9.99))
    query += '&G='+str(int(color[1]*9.99))
    query += '&B='+str(int(color[2]*9.99))
    res = urllib.request.urlopen(url_s+query)   # HTTPアクセスを実行
    res.close()                                 # HTTPアクセスの終了

def tone2rgb(tone_color=0, brightness=0.5):     # ToDo colorzeroに置き換えれるはず
    v = brightness
    if v > 1:
        v = 1.0
    elif v < 0:
        v = 0.0
    f = float(tone_color % 60) / 60.
    t = f * v
    q = v - t
    i = int((tone_color%360) / 60)
    rgb = []
    if i==0:
        rgb = [v, t, 0]                         # case 0: r=v; g=t; b=0; break;
    elif i==1:
        rgb = [q, v, 0]                         # case 1: r=q; g=v; b=0; break;
    elif i==2:
        rgb = [0, v, t]                         # case 2: r=0; g=v; b=t; break;
    elif i==3:
        rgb = [0, q, v]                         # case 3: r=0; g=q; b=v; break;
    elif i==4:
        rgb = [t, 0, v]                         # case 4: r=t; g=0; b=v; break;
    elif i==5:
        rgb = [v, 0, q]                         # case 5: r=v; g=0; b=q; break;
    return rgb

def temp2tone(temperature):
    hue = 240*(temp_max - temperature)/(temp_max - temp_min)
    if hue < 0:
        hue = 0
    if hue > 240:
        hue = 240
    return hue

def getTemp():
    fp = open(filename)                         # CPU温度ファイルを開く
    temp = round(float(fp.read()) / 1000,1)     # ファイルを読み込み1000で除算
    fp.close()                                  # ファイルを閉じる
    print('CPU Temperature =', temp)            # CPU温度を表示する
    return temp                                 # CPU温度値を返却する

print('Usage:',argv[0],'[temperature]')         # プログラム名を表示する

temp = None
brightness = 0.5
if len(argv) >= 2:
    temp = int(argv[1])
if len(argv) >= 3:
    brightness = int(argv[2])/100
if temp is not None:
    httpSender(tone2rgb(temp2tone(temp),brightness))
    exit()
while True:
    httpSender(tone2rgb(temp2tone(getTemp())))
    sleep(10)
