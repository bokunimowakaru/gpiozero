# GPIO ZeroでI/O制御プログラミング

## ラズパイ5入手前でも試せるGPIO Zero
Raspberry Pi 5 model Bの発売に合わせて登場したRaspberry Pi OS 12 Bookworm。  
本OSに標準搭載されている最新のGPIO制御用モジュール「GPIO Zero」を試してみましょう。

## GPIO Zeroとは
Ben Nuttall 氏とDave Jones氏が開発したラズベリー・パイ用のGPIO制御モジュール（ライブラリ）。
各種の具体的なGPIOデバイスに応じたクラスや関数が用意されている。
従来のRPi.GPIOよりも簡潔にプログラムを書くことが出来る。
実は，一つ古いRaspberry Pi OS 11 BullseyeでGPIO Zeroが標準搭載されていた．
しかし，Raspberry Pi 4ではRPi.GPIOが利用できたため，あまり利用されていなかった．
今回のRaspberry Pi 5の登場で，これからGPIO Zeroが主流になるだろう。

by Wataru KUNINO 2023
-------------------------------------------------------------------------------------------
参考文献
https://www.raspberrypi.com/documentation/computers/raspberry-pi-5.html#raspberry-pi-and-gpio
https://gpiozero.readthedocs.io/
