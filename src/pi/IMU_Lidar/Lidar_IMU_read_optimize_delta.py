#!/usr/bin/env python
# -*- coding: utf-8 -*
import os
import serial
import time
import datetime
import sys
import csv
import threading
import picamera
import argparse
from multiprocessing import Process
from IMU_SETUP import lib



beginTime = str(datetime.datetime.now())

os.makedirs(beginTime+"/camera")


sys.version[0] == '3' #declare for python 3

ser = serial.Serial("/dev/ttyS0", 115200) #serial port for Lidar

datafile = beginTime+'/Lidar_IMU_Data.csv'

parser = argparse.ArgumentParser(description = 'PiCar log file generator', formatter_class = argparse.RawTextHelpFormatter)
parser.add_argument("--t", help = "determine the duration that the test runs", type = int, default =5 )
parser.add_argument("--sa",help = "set accelerometer ODR, available values(default = 6): \n 1 = 10 Hz    4 = 238 Hz \n 2 = 50 Hz    5 = 476 Hz \n 3 = 119 Hz   6 = 952 Hz", type = int, choices=[1,2,3,4,5,6], default = 6)
parser.add_argument("--sg",help = "set gyro ODR, available values(default = 6): \n 1 = 14.9    4 = 238 \n 2 = 59.5    5 = 476 \n 3 = 119     6 = 952", type = int, choices = [1,2,3,4,5,6],default = 6)
parser.add_argument("--sm",help = "set mag ODR, available values(default = 7): \n 0 = 0.625 Hz  4 = 10 Hz \n 1 = 1.25 Hz   5 = 20 Hz \n 2 = 2.5 Hz    6 = 40 Hz \n 3 = 5 Hz      7 = 80 Hz", type = int, choices = [0,1,2,3,4,5,6,7], default = 7)
parser.add_argument("--a",help = "set acc scale, available values(default = 2): 2, 4, 8, 16 (g)", type = int, choices = [2,4,8,16], default = 2)
parser.add_argument("--g",help = "set gyro scale, available values(default = 245): 245, 500, 2000", type = int, choices = [245,500,2000], default = 245)
parser.add_argument("--m", help = "set mag scale, available values(default = 4) : 4, 8, 12, 16", type = int, choices = [4,8,12,16],default=4)
parser.add_argument("--c",help = "set camera filming rate(Hz)", type = int, default = 24)
parser.add_argument("--ri",help = "set imu reading rate(Hz)", type = int, default = 50)
parser.add_argument("--rl", help = "set LiDar reading rate(Hz)", type = int, default = 50)
parser.add_argument("--p",help = "set the precision of the timing", type = float, default = 0.001)
re = parser.parse_args()

rowList = []
duration = re.t
trAccRate = re.sa
trGyroRate = re.sg
trMagRate = re.sm
accScale = re.a
gyroScale = re.g
magScale = re.m
lidarRate = float(1)/(re.rl)-0.0007
imuRate = 1/float(re.ri)-0.0007
precision = re.p
cameraFreq = 1/float(re.c)


#see document for available scales

def setIMUScale(aScl=2,gScl=245,mScl=4):
    global imu
    lib.lsm9ds1_setAccelScale(imu,aScl)
    lib.lsm9ds1_setGyroScale(imu,gScl)
    lib.lsm9ds1_setMagScale(imu,mScl)

#see document for available tranmission rate

def setIMUodr(aRate=6,gRate=6,mRate=7):
    global imu
    lib.lsm9ds1_setAccelODR(imu,aRate)
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
    else:
        ser.reset_input_buffer()
        return "value"
    
def filenames():
    startTime = time.time()
    lastTime = time.time()
    current = time.time()
    while current-startTime<duration:
        current = time.time()
        if current-lastTime>cameraFreq:
            name = datetime.datetime.now()
            name = beginTime+'/camera/'+str(name)+'.jpg'
            lastTime = time.time()
            yield name
    
    
def capture():
    camera = picamera.PiCamera(resolution=(480,480), framerate=40)
    camera.capture_sequence(filenames(), use_video_port=True)


#the function which calls getIMU and getLidar
def getData():
    global imu
    startTime = time.time()
    lastTimeLidar = time.time()
    lastTimeIMU = lastTimeLidar
    lastTime = lastTimeLidar
    current = time.time()
    while current - startTime < duration:
        if current-lastTime>precision:
            lastTime = current
            if current-lastTimeIMU>imuRate and lib.lsm9ds1_accelAvailable(imu) > 0 and current-lastTimeLidar>lidarRate and ser.in_waiting > 8:
                lastTimeIMU = time.time()
                IMUdata = getIMU()
                Lidardata = getLidar()
                currentTime = str(datetime.datetime.fromtimestamp(lastTimeIMU))
                lastTimeLidar = lastTimeIMU
                rowList.append([currentTime,Lidardata,IMUdata[0],IMUdata[1],IMUdata[2],IMUdata[3],IMUdata[4],IMUdata[5]])
            elif current-lastTimeIMU>imuRate and lib.lsm9ds1_accelAvailable(imu) > 0:
                lastTimeIMU = time.time()
                IMUdata = getIMU()
                currentTime = str(datetime.datetime.fromtimestamp(lastTimeIMU))
                rowList.append([currentTime,"NA",IMUdata[0],IMUdata[1],IMUdata[2],IMUdata[3],IMUdata[4],IMUdata[5]])
            elif current-lastTimeLidar>lidarRate and ser.in_waiting > 8:
                lastTimeLidar = time.time()
                Lidardata = getLidar()
                currentTime = str(datetime.datetime.fromtimestamp(lastTimeLidar))
                rowList.append([currentTime,Lidardata,"NA","NA","NA","NA","NA","NA"])

        current = time.time()



    #After 10 seconds, write IMU and Lidar data into a csv file
    print("start writing data")
    with open(datafile,"w") as csvfile:
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
        print(time.time())
        pic =  Process(target = capture)
        sensor = Process(target = getData)
        
        pic.start()
        sensor.start()
        pic.join()
        sensor.join()
        
        print(time.time())
    except KeyboardInterrupt:   # Ctrl+C
        if ser != None:
            ser.close()
        sys.exit()
