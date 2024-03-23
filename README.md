# GPIO ZeroでI/O制御プログラミング

![Raspberry-Pi-5-GPIO](https://bokunimo.net/blog/wp-content/uploads/2024/03/pi5-gpio.jpg "GPIO Pins on Raspberry Pi 5 model B; ラズベリー・パイ5のGPIO端子")  

## ラズパイ5入手前でも試せるGPIO Zero

Raspberry Pi 5 model B （下図）の発売に合わせて登場したRaspberry Pi OS 12 Bookworm。  
本OSに標準搭載されている最新のGPIO制御用モジュール「GPIO Zero」を試してみましょう。

![Raspberry-Pi-5](https://bokunimo.net/blog/wp-content/uploads/2024/03/pi5_box.jpg "Raspberry Pi 5 model B; 最新のラズベリー・パイ5")  

## GPIO Zeroとは

一つ古いRaspberry Pi OS 11 BullseyeでGPIO Zeroが標準搭載されていいましたが、これまではRPi.GPIOが利用できたため，あまり利用されていませんでした。
Raspberry Pi 5 ではRPi.GPIOが使用できなくなったので、これからGPIO Zeroが主流になると思います。

- Ben Nuttall 氏とDave Jones氏が開発したラズベリー・パイ用のGPIO制御モジュール（ライブラリ）
- 各種の具体的なGPIOデバイスに応じたクラスや関数が用意されている
- 従来のRPi.GPIOよりも簡潔にプログラムを書くことが出来る

## 本プログラム集でできること(一例)

下図は本プログラム集の Example 5 を応用した製作品の一例です。サーボ・モータを使って、Raspberry Pi 5のケースの蓋の開閉を制御します。  

![controlled_case_cap](https://bokunimo.net/blog/wp-content/uploads/2024/03/controlled_case_cap.jpg "Raspberry Pi 5 model B; 最新のラズベリー・パイ5")  
[https://github.com/bokunimowakaru/gpiozero/blob/master/examples/example5_servo.py](https://github.com/bokunimowakaru/gpiozero/blob/master/examples/example5_servo.py)  


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

## 詳細な説明 #広告

プログラムの使い方や解説は、雑誌「Interface 2024年5月号」にて紹介していますので、お買い求めいただければ幸いです。  
[https://bokunimo.net/blog/raspberry-pi/4524/](https://bokunimo.net/blog/raspberry-pi/4524/)#広告  

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
