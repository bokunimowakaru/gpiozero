#!/usr/bin/env python3
###############################################################################
# Example 2 ボタン [GPIO Zero 版] [LINE Messaging API 対応版]
#
#                   Copyright (c) 2019-2024 Wataru KUNINO https://bokunimo.net/
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
# LINE 公式アカウントと Messaging API 用のChannel情報が必要です。
#   1. https://entry.line.biz/start/jp/ からLINE公式アカウントを取得する
#   2. https://manager.line.biz/ の設定で「Messaging APIを利用する」を実行する
#   3. Channel 情報 (Channel ID と Channel secret) を取得する
#   4. スクリプト内の変数 line_ch_id にChannel IDを記入する
#   5. スクリプト内の変数 line_ch_pw にChannel secretを記入する
#
#                      Copyright (c) 2024 Wataru KUNINO (https://bokunimo.net/)
###############################################################################
# 注意事項
# ・メッセージ送信回数の無料枠は200回/月です。超過分は有料となります。
# ・15分間だけ有効なステートレスチャネルアクセストークンを使用しています。
# 　本スクリプトでは、実行の度にTokenを取得するので問題ありません。
# 　関数line_notifyを複数回、呼び出すような場合は、15分以内にget_line_tokenで
# 　Tokenを再取得してください。(このスクリプトを改変する場合)
###############################################################################


# Messaging API用 Channel情報
line_ch_id="0000000000"                         # LINEで取得した Channel ID
line_ch_pw="00000000000000000000000000000000"   # LINEで取得した Channel secret
url_s="https://api.line.me/"                    # LINE Messaging API のURL
url_token_s = url_s + "oauth2/v3/token"         # Token取得用のURL
url_broad_s = url_s + "v2/bot/message/broadcast" # MessageのBroadcast送信用URL

port = 26                                       # GPIO ポート番号=26(37番ピン)

from gpiozero import Button                     # GPIO Zero のButtonを取得
from signal import pause                        # シグナル待ち受けの取得
from sys import argv                            # 本プログラムの引数argvを取得
import urllib.request                           # HTTP通信ライブラリを組み込む
import json                                     # JSON変換ライブラリを組み込む

def get_line_token():
    head_dict = {'Content-Type':'application/x-www-form-urlencoded'}
    body =  'grant_type=client_credentials&'
    body += 'client_id=' + line_ch_id + '&'
    body += 'client_secret=' + line_ch_pw
    post = urllib.request.Request(url_token_s,body.encode(),head_dict)
    try:                                        # 例外処理の監視を開始
        res = urllib.request.urlopen(post)      # HTTPアクセスを実行
        res_s = res.read().decode()             # 受信テキストを変数res_sへ
        res.close()                             # HTTPアクセスの終了
        res_dict = json.loads(res_s)            # 辞書型の変数res_dictへ代入
    except Exception as e:                      # 例外処理発生時
        print(e,url_s)                          # エラー内容と変数url_sを表示
        exit()                                  # プログラムの終了
    return res_dict

def toLine():                                   # LINEへメッセージを送信する
    line_token = get_line_token().get('access_token') # LINE Token を取得する
    head_dict = {'Authorization':'Bearer ' + line_token,
                 'Content-Type':'application/json'} # ヘッダを変数head_dictへ
    print(head_dict)                            # 送信ヘッダhead_dictを表示
    body = 'message=ボタンが押されました'       # 送信するbody(message=)を作成
    body_json='{"messages":[{"type":"text","text":"' + body + '"}]}'
    print(body)                                 # 送信内容bodyを表示
    post = urllib.request.Request(url_broad_s, body_json.encode(), head_dict)
                                                # POSTリクエストデータを作成
    try:                                        # 例外処理の監視を開始
        res = urllib.request.urlopen(post)      # HTTPアクセスを実行
    except Exception as e:                      # 例外処理発生時
        print(e,url_s)                          # エラー内容と変数url_sを表示
        return                                  # 処理の中断
    res_str = res.read().decode()               # 受信テキストを変数res_strへ
    res.close()                                 # HTTPアクセスの終了
    if len(res_str):                            # 受信テキストがあれば
        print('Response:', res_str)             # 変数res_strの内容を表示
    else:
        print('Done')                           # Doneを表示

print(argv[0])                                  # プログラム名を表示する
if len(argv) >= 2:                              # 引数があるとき
    port = int(argv[1])                         # 整数としてportへ代入
btn = Button(port, bounce_time=0.1)             # ポート番号portをボタン入力に

btn.when_pressed = toLine                       # ボタンにLINE送信を割り当て
pause()                                         # 待ち受け待機する(永久ループ)
