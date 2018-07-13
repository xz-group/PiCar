#!/bin/bash

filename=$1
avrdude -p atmega32u4 -C ~/avrdude_gpio.conf -c pi_2 -v -U flash:w:${filename}
