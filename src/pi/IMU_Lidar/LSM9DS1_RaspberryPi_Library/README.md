SparkFun LSM9DS1 RaspberryPI Library
===

Porting [SparkFun_LSM9DS1_Arduino_Library](https://github.com/sparkfun/SparkFun_LSM9DS1_Arduino_Library) to Raspberry Pi

<p align="center"><img src="https://user-images.githubusercontent.com/17570265/29253393-a11ac3a6-80b6-11e7-846f-0d387fa2fbe4.jpeg" alt="LSM9DS1" width="200"/></p>

[LSM9DS1 Breakout Board (SEN-13284)](https://www.sparkfun.com/products/13284)

This library supports only I2C.

## Requirement

* [WiringPi](http://wiringpi.com/)

```
$ sudo apt-get install libi2c-dev
$ git clone git://git.drogon.net/wiringPi
$ cd wiringPi
$ git pull origin
$ ./build
```

## Install

```
$ git clone https://github.com/akimach/LSM9DS1_RaspberryPi_Library.git
$ cd LSM9DS1_RaspberryPi_Library
$ make
$ sudo make install
```

## Python version

```
$ cd LSM9DS1_RaspberryPi_Library/example
$ sudo python LSM9DS1_Basic_I2C.py
```
