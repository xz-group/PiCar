# Build & Run

Pin assignment is below: 

|RasPi|IMU|
|:-:|:-:|
|GND|GND|
|3.3VDC Power|VDD|
|Pin3|SDA|
|Pin5|SCL|

```
$ make
$ sudo -s
$ LD_LIBRARY_PATH=../lib ./LSM9DS1_Basic_I2C
```
