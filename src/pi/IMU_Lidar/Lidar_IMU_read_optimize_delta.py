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


if sys.argv[1]=="-U":
    print("Usage")


sys.version[0] == '3' #declare for python 3

ser = serial.Serial("/dev/ttyS0", 115200) #serial port for Lidar
beginTime = str(datetime.datetime.now())
filename = beginTime+'/Lidar_IMU_Data.csv'

timeDiffer = []
rowList = []
duration = 10
setAccRate = 0.02
setGyroRate = 0.02
setMagRate = 0.02
trAccRate = 6
trGyroRate = 6
trMagRate = 7
lidarRate = 0.02
imuRate = 0.02

#see document for available scales

def setIMUScale(aScl=2,gScl=245,mScl=4):
    global imu
    lib.lsm9ds1_setAccelScale(imu,aScl)
    lib.lsm9ds1_setGyroScale(imu,gScl)
    lib.lsm9ds1_setMagScale(imu,mScl)

#see document for available tranmission rate

def setIMUodr(aRate=6,gRate=6,mRate=7):
    global imu
    lib.lsm9ds1_setAccelODR(imu,aScl)
    lib.lsm9ds1_setGyroODR(imu,gRate)
    lib.lsm9ds1_setMagODR(imu,mRate)

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
    global imu

    startTime = time.time()
    lastTimeLidar = time.time()
    lastTimeIMU = time.time()
    current = time.time()
    while current - startTime < duration:
        current = time.time()
        if current-lastTimeIMU>setAccRate and lib.lsm9ds1_accelAvailable(imu) > 0 and current-lastTimeLidar>lidarRate and ser.in_waiting > 8:
            lastTimeIMU = time.time()
            lastTimeLidar = lastTimeIMU
            currentTime = str(datetime.datetime.now())
            IMUdata = getIMU()
            Lidardata = getLidar()
            rowList.append([currentTime,Lidardata,IMUdata[0],IMUdata[1],IMUdata[2],IMUdata[3],IMUdata[4],IMUdata[5]])
        elif current-lastTimeIMU>setAccRate and lib.lsm9ds1_accelAvailable(imu) > 0:
            lastTimeIMU = time.time()
            currentTime = str(datetime.datetime.now())
            IMUdata = getIMU()
            rowList.append([currentTime,"NA",IMUdata[0],IMUdata[1],IMUdata[2],IMUdata[3],IMUdata[4],IMUdata[5]])
        elif current-lastTime>lidarRate and ser.in_waiting > 8:
            lastTimeLidar = time.time()
            currentTime = str(datetime.datetime.now())
            Lidardata = getLidar()
            rowList.append([currentTime,Lidardata,"NA","NA","NA","NA","NA","NA"])


    #After 10 seconds, write IMU and Lidar data into a csv file
    print("start writing data")
    with open(datafile,"a",newline = '') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for row in rowList:
            spamwriter.writerow(row)



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
