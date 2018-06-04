CC = gcc
.PHONY: all
all: LSM9DS1_Basic_I2C

LSM9DS1_Basic_I2C: LSM9DS1_Basic_I2C.cpp
	$(CC) -Wall -O2 LSM9DS1_Basic_I2C.cpp -o LSM9DS1_Basic_I2C -llsm9ds1

clean:
	rm -f LSM9DS1_Basic_I2C
