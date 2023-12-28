#!/bin/bash
###############################################################################
# GPIO 制御用 HTTPクライアント
#
# raspi-gpioコマンドに似た方法で、GPIOを制御します
#
#   gpio_zero set 4 dh # ポート4をHighレベル(楽3.3V)に設定します。
#   gpio_zero set 4 dL # ポート4をLowレベル(約0V)に設定します。
#   gpio_zero get 4    # ポート4の状態を応答します。
#
# 最新版：
# https://bokunimo.net/git/bash/blob/master/gpio/gpio_zero.sh
#
# 参考文献：
# https://gpiozero.readthedocs.io/
# raspi-gpio help
#
#                   Copyright (c) 2023-2024 Wataru KUNINO https://bokunimo.net/
###############################################################################

url_s="localhost:8080"                      # 宛先アドレス
gpio_srv_app="example6_gpio_api.py"         # GPIO制御サーバのプログラム名
gpio_srv_log="example6_gpio_api.log"        # ログ出力用のファイル名

if [[ ${#} == 0 ]]; then                    # 取得した引数が0個のとき
    echo "Usage: "${0}" <get|set> <port> [value]" # プログラム名と使い方を表示
    echo "       "${0}" set 4 dh # Digital High Output"
    echo "       "${0}" set 4 dl # Digital Low Output"
    echo "       "${0}" get 4    # Read Digital Value"
    echo "       "${0}" set 4 op # Digital Output Mode"
    echo "       "${0}" set 4 ip # same as 'get 4'"
    echo "       "${0}" quit     # Stop HTTP Server"
fi

dir=`cd $(dirname ${0}) && pwd`             # スクリプトの保存場所を取得
gpio_srv=${dir}"/"${gpio_srv_app}           # GPIO制御用HTTPサーバの場所を取得
pid_srv=`pidof -x ${gpio_srv_app}`          # 実行状態を取得
if [[ ! ${pid_srv} ]]; then                 # 実行されていないとき
    ${gpio_srv} &>> ${dir}"/"${gpio_srv_log} & # サーバを起動
    sleep 1                                 # 起動待ち
    pid_srv=`pidof -x ${gpio_srv_app}`      # 実行状態を取得
    echo "started http server : ${gpio_srv} &>> ${dir}/${gpio_srv_log}" # 開始表示
    echo "PID of ${gpio_srv_app} = "${pid_srv}  # PIDを表示
fi

com="none"                                  # コマンド名 none/get/set
port=4                                      # GPIO ポート番号
val="dl"                                    # GPIO 出力値
res=""                                      # 応答値
d=("dl" "dh")                               # GPIOの論理値の定義

if [[ ${#} -ge 1 ]]; then
    com=${1}
fi
if [[ ${#} -ge 2 ]]; then
    port=${2}
fi
if [[ ${#} -ge 3 ]]; then
    val=${3}
fi
if [[ ${com} = "quit" ]]; then
    kill ${pid_srv}
    echo
    echo "stopped http server"
    exit 0
fi
if [[ ${val} = "ip" ]]; then
    com="get"
fi
if [[ ${com} = "get" ]]; then
    res=`curl -s ${url_s}"/?port="${port}"&in"`
fi
if [[ ${com} = "set" ]]; then
    b=-1
    if [[ ${val} = ${d[0]} ]]; then
        b=0
    elif [[ ${val} = ${d[1]} ]]; then
        b=1
    fi
    if [[ ${b} -ge 0 ]]; then
        res=`curl -s ${url_s}"/?port="${port}"&out="${b}`
    else
        res=`curl -s ${url_s}"/?port="${port}"&out"`
    fi
fi
echo ${res}
exit 0

################################################################################
実行例

pi@raspberrypi:~/gpiozero/examples $ ./example6_gpio.sh
Usage: ./example6_gpio.sh <get|set> <port> [value]
       ./example6_gpio.sh set 4 dh # Digital High Output
       ./example6_gpio.sh set 4 dl # Digital Low Output
       ./example6_gpio.sh get 4    # Read Digital Value
       ./example6_gpio.sh set 4 op # Digital Output Mode
       ./example6_gpio.sh set 4 ip # same as 'get 4'
       ./example6_gpio.sh quit     # Stop HTTP Server
started http server : /home/pi/gpiozero/examples/example6_gpio_api.py &>> /home/pi/gpiozero/examples/example6_gpio_api.log

pi@raspberrypi:~/gpiozero/examples $ ./example6_gpio.sh set 4 dh
GPIO4=1

pi@raspberrypi:~/gpiozero/examples $ ./example6_gpio.sh set 4 dl
GPIO4=0

pi@raspberrypi:~/gpiozero/examples $ ./example6_gpio.sh get 4
GPIO4=0
