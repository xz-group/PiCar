#!/usr/bin/env python
# -*- coding: utf-8 -*

import serial
import time
import datetime
import sys
import csv
import threading
from multiprocessing import Pool
from IMU_SETUP import lib

sys.version[0] == '3' #declare for python 3

ser = serial.Serial("/dev/ttyS0", 115200) #serial port for Lidar
filename = 'Lidar_IMU_Frequency_optimize.csv'
datafile = 'Lidar_IMU_data_optimize.csv'
timeDiffer = []
rowList = []


#get IMU data
def getIMU():
    global imu
    lib.lsm9ds1_readAccel(imu)
    ax = lib.lsm9ds1_getAccelX(imu)
    ay = lib.lsm9ds1_getAccelY(imu)
    az = lib.lsm9ds1_getAccelZ(imu)
    cax = lib.lsm9ds1_calcAccel(imu, ax)
    cay = lib.lsm9ds1_calcAccel(imu, ay)
    caz = lib.lsm9ds1_calcAccel(imu, az)
    gx = lib.lsm9ds1_getGyroX(imu)
    gy = lib.lsm9ds1_getGyroY(imu)
    gz = lib.lsm9ds1_getGyroZ(imu)
    cgx = lib.lsm9ds1_calcGyro(imu, gx)
    cgy = lib.lsm9ds1_calcGyro(imu, gy)
    cgz = lib.lsm9ds1_calcGyro(imu, gz)
    return (cax,cay,caz,cgx,cgy,cgz)


#get TFmini Lidar data
def getLidar():
    #TFmini data
    recv = ser.read(9)
    ser.reset_input_buffer()

    if recv[0] == 0x59 and recv[1] == 0x59:
        distance = recv[2] + recv[3] * 256
        ser.reset_input_buffer()
        return distance


#the function which calls getIMU and getLidar
def getData():
    global lasttime
    global imu

    current = time.time()
    while current - startTime < 10:

        current = time.time()
        if lib.lsm9ds1_accelAvailable(imu) > 0 and ser.in_waiting > 8:
            IMUdata = getIMU()
            Lidardata = getLidar()

            currentTime = str(datetime.datetime.now()); #timestamp data
            row = [currentTime,Lidardata,IMUdata[0],IMUdata[1],IMUdata[2],IMUdata[3],IMUdata[4],IMUdata[5]] #the row being written to csv file, just x and y accel
            rowList.append(row)
            diff = time.time() - lasttime
            timeDiffer.append(diff)
            #print(diff)
            lasttime = time.time()
            #print(row)

    #After 10 seconds, write IMU and Lidar data into a csv file
    print("start writing data")
    with open(datafile,"a",newline = '') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(rowList)):
            row = [rowList[i]]
            spamwriter.writerow(row)

    #write reading frequency into a csv file
    print("start writing frequency")
    with open(filename,"a",newline = '') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(timeDiffer)):
            row = [timeDiffer[i]]
            spamwriter.writerow(row)


startTime = time.time()
lasttime = time.time()
#connect with IMU
imu = lib.lsm9ds1_create()
lib.lsm9ds1_begin(imu)


if __name__ == '__main__':
    if lib.lsm9ds1_begin(imu) == 0:
        print("Failed to communicate with LSM9DS1.")
        quit()
    lib.lsm9ds1_calibrate(imu)
    try:
        if ser.is_open == False:
            ser.open()
        getData()
    except KeyboardInterrupt:   # Ctrl+C
        if ser != None:
            ser.close()
        sys.exit()
