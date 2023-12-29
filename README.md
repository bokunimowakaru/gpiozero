# GPIO ZeroでI/O制御プログラミング

## ラズパイ5入手前でも試せるGPIO Zero

Raspberry Pi 5 model Bの発売に合わせて登場したRaspberry Pi OS 12 Bookworm。  
本OSに標準搭載されている最新のGPIO制御用モジュール「GPIO Zero」を試してみましょう。

## GPIO Zeroとは

Ben Nuttall 氏とDave Jones氏が開発したラズベリー・パイ用のGPIO制御モジュール（ライブラリ）。
各種の具体的なGPIOデバイスに応じたクラスや関数が用意されている。
従来のRPi.GPIOよりも簡潔にプログラムを書くことが出来る。
実は，一つ古いRaspberry Pi OS 11 BullseyeでGPIO Zeroが標準搭載されていた。
しかし，Raspberry Pi 4ではRPi.GPIOが利用できたため，あまり利用されていなかった。
今回のRaspberry Pi 5の登場で，これからGPIO Zeroが主流になるだろう。

## GPIO Zero実験用ソフトウェア

ラズベリー・パイ上のLXTerminalから下記のコマンドを入力してダウンロードする。  

	$ git clone https://bokunimo.net/git/gpiozero  

ダウンロードに成功すると、gpiozeroフォルダが作成される。
下記を入力し、サンプル・プログラム集のフォルダに移動する。

	$ cd gpiozero/examples  

プログラムの一覧は「ls⏎」で表示される。  
プログラムexample1_led.pyを実行するには、このexamplesフォルダ内で下記を実行する

	$ ./example1_led.py  

プログラムを停止するには[Ctrl]+[C]を押下する。  

## 本プログラム集のウェブページ

[https://git.bokunimo.com/gpiozero/](https://git.bokunimo.com/gpiozero/)

by Wataru KUNINO 2023-2024 [https://bokunimo.net/](https://bokunimo.net/)

-------------------------------------------------------------------------------------------

## 参考文献

本プログラム集の作成にあたり、下記の文献を参考にした。

"Raspberry Pi and GPIO". Raspberry Pi documentation, Raspberry Pi Ltd.  
[https://www.raspberrypi.com/documentation/computers/raspberry-pi-5.html#raspberry-pi-and-gpio](https://www.raspberrypi.com/documentation/computers/raspberry-pi-5.html#raspberry-pi-and-gpio)  

Ben Nuttall, Dave Jones. "gpiozero".  
[https://gpiozero.readthedocs.io/](https://gpiozero.readthedocs.io/)  

"GPIO Registers Failed on Raspberry Pi 5". Raspberry Pi Forum, Raspberry Pi Ltd.  
https://forums.raspberrypi.com/viewtopic.php?t=359829  

Les Pounder (2023-10-28). "How to Control the Raspberry Pi 5 GPIO with Python 3".  
https://www.tomshardware.com/how-to/control-raspberry-pi-5-gpio-with-python-3  

SG-90 PDFデータシート; "SG90 9 g Micro Servo [参考資料]"  
https://akizukidenshi.com/download/ds/towerpro/SG90_a.pdf  
