#!/usr/bin/env python
# -*- coding: utf-8 -*
#No extra package required to run the script
#However, be sure you read the documentation on http://picar.readthedocs.io/en/latest/chapters/usage/software.html#data-logging
import os
import serial
import time
import datetime
import sys
import csv
import threading
import picamera
import argparse
import signal
from socket_folder_server import send
from multiprocessing import Process,Event
from IMU_SETUP import lib



def pre_exec():
    # To ignore CTRL+C signal in the new process
    signal.signal(signal.SIGINT, signal.SIG_IGN)


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
    lib.lsm9ds1_readGyro(imu)
    lib.lsm9ds1_readMag(imu)
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
    mx = lib.lsm9ds1_getMagX(imu)
    my = lib.lsm9ds1_getMagY(imu)
    mz = lib.lsm9ds1_getMagZ(imu)
    cmx = lib.lsm9ds1_calcMag(imu,mx)
    cmy = lib.lsm9ds1_calcMag(imu,my)
    cmz = lib.lsm9ds1_calcMag(imu,mz)
    return (cax,cay,caz,cgx,cgy,cgz,cmx,cmy,cmz)



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
        return "UP"


#a timer wrapped inside a python generator to take picture
def filenames(alive,duration,cameraFreq,beginTime):
    startTime = time.time()
    lastTime = time.time()
    current = time.time()
    while current-startTime<duration and not alive.is_set():
        current = time.time()
        if current-lastTime>cameraFreq:
            name = datetime.datetime.now()
            #name = time.time()
            name = beginTime+'/camera/'+str(name)+'.jpg'
            lastTime = time.time()
            yield name


def capture(alive,duration,cameraFreq,beginTime):
    pre_exec()
    camera = picamera.PiCamera(resolution=(480,480), framerate=40)
    camera.capture_sequence(filenames(alive,duration,cameraFreq,beginTime), use_video_port=True)


#the function which calls getIMU and getLidar
def getData(alive,duration,precision,imuRate,lidarRate,datafile,rowList):
    pre_exec()
    global imu
    startTime = time.time()
    lastTimeLidar = time.time()
    lastTimeIMU = lastTimeLidar
    lastTime = lastTimeLidar
    current = time.time()
    while current - startTime < duration and not alive.is_set():
        #define the precision, i.e. the gap between two consecutive IMU or LiDar read
        if current-lastTime>precision:
            lastTime = current
            if current-lastTimeIMU>imuRate and lib.lsm9ds1_accelAvailable(imu) > 0 and current-lastTimeLidar>lidarRate and ser.in_waiting > 8:
                lastTimeIMU = time.time()
                IMUdata = getIMU()
                Lidardata = getLidar()
                currentTime = str(datetime.datetime.fromtimestamp(lastTimeIMU))
                #currentTime = str(lastTimeIMU)
                lastTimeLidar = lastTimeIMU
                rowList.append([currentTime,Lidardata,IMUdata[0],IMUdata[1],IMUdata[2],IMUdata[3],IMUdata[4],IMUdata[5],IMUdata[6],IMUdata[7],IMUdata[8]])
            elif current-lastTimeIMU>imuRate and lib.lsm9ds1_accelAvailable(imu) > 0:
                lastTimeIMU = time.time()
                IMUdata = getIMU()
                currentTime = str(datetime.datetime.fromtimestamp(lastTimeIMU))
                #currentTime = str(lastTimeIMU)
                rowList.append([currentTime,"NA",IMUdata[0],IMUdata[1],IMUdata[2],IMUdata[3],IMUdata[4],IMUdata[5],IMUdata[6],IMUdata[7],IMUdata[8]])
            elif current-lastTimeLidar>lidarRate and ser.in_waiting > 8:
                lastTimeLidar = time.time()
                Lidardata = getLidar()
                currentTime = str(datetime.datetime.fromtimestamp(lastTimeLidar))
                #currentTime = str(lastTimeLidar)
                rowList.append([currentTime,Lidardata,"NA","NA","NA","NA","NA","NA","NA","NA","NA"])

        current = time.time()

    print("start writing data")
    with open(datafile,"w") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for row in rowList:
            spamwriter.writerow(row)


#connect with IMU
imu = lib.lsm9ds1_create()
lib.lsm9ds1_begin(imu)
ser = serial.Serial("/dev/ttyS0", 115200) #serial port for Lidar


def getSensorAndCamera(host='192.168.1.121',port=6000,save=False,duration=5,endless=False,trAccRate=6,trGyroRate=6,trMagRate=7,accScale=2,gyroScale=245,magScale=4,cameraFreq=5,imuRate=50,lidarRate=50,precision=0.001):
    beginTime = str(datetime.datetime.now())
    os.makedirs(beginTime+"/camera")
    datafile = beginTime+'/Lidar_IMU_Data.csv'
    rowList=[]
    if endless:
        duration = 1000
    lidarRate = float(1)/lidarRate - 0.0007
    imuRate = float(1)/imuRate - 0.0007
    cameraFreq = float(1)/cameraFreq
    setIMUScale(accScale,gyroScale,magScale)
    setIMUodr(trAccRate,trGyroRate,trMagRate)
    if lib.lsm9ds1_begin(imu) == 0:
        print("Failed to communicate with LSM9DS1.")
        quit()
    lib.lsm9ds1_calibrate(imu)
    try:
        if ser.is_open == False:
            ser.open()
        print(time.time())
        alive = Event()
        #multicore process
        pic =  Process(target = capture,args=(alive,duration,cameraFreq,beginTime,))
        sensor = Process(target = getData,args=(alive,duration,precision,imuRate,lidarRate,datafile,rowList,))

        pic.start()
        sensor.start()
        pic.join()
        sensor.join()
        #subprocess.Popen("python3 socket_folder_server.py localhost 60004 \""+beginTime+"\"",shell=True)
    except KeyboardInterrupt:   # Ctrl+C
        if ser != None:
            ser.close()
        alive.set()
        pic.join()
        sensor.join()
    print(time.time())
    send(host,port,beginTime)
    if not save:
        os.system("rm -r \""+beginTime+"\"")


if __name__ == '__main__':
    beginTime = str(datetime.datetime.now())
    parser = argparse.ArgumentParser(description = 'PiCar log file generator', formatter_class = argparse.RawTextHelpFormatter, conflict_handler = 'resolve')
    parser.add_argument("--ip",help="Ip of this raspberry pi",default="192.168.1.121")
    parser.add_argument("--po",help = "port for connection",type = int,default=6000)
    parser.add_argument("-i","--t", help = "endless mode", action='store_const',const=1000 , default =5 )
    parser.add_argument("--t",help = "determine the duration that the test runs", type = int, default = 5)
    parser.add_argument("--sa",help = "set accelerometer ODR, available values(default = 6): \n 1 = 10 Hz    4 = 238 Hz \n 2 = 50 Hz    5 = 476 Hz \n 3 = 119 Hz   6 = 952 Hz", type = int, choices=[1,2,3,4,5,6], default = 6)
    parser.add_argument("--sg",help = "set gyro ODR, available values(default = 6): \n 1 = 14.9    4 = 238 \n 2 = 59.5    5 = 476 \n 3 = 119     6 = 952", type = int, choices = [1,2,3,4,5,6],default = 6)
    parser.add_argument("--sm",help = "set mag ODR, available values(default = 7): \n 0 = 0.625 Hz  4 = 10 Hz \n 1 = 1.25 Hz   5 = 20 Hz \n 2 = 2.5 Hz    6 = 40 Hz \n 3 = 5 Hz      7 = 80 Hz", type = int, choices = [0,1,2,3,4,5,6,7], default = 7)
    parser.add_argument("--a",help = "set acc scale, available values(default = 2): 2, 4, 8, 16 (g)", type = int, choices = [2,4,8,16], default = 2)
    parser.add_argument("--g",help = "set gyro scale, available values(default = 245): 245, 500, 2000", type = int, choices = [245,500,2000], default = 245)
    parser.add_argument("--m", help = "set mag scale, available values(default = 4) : 4, 8, 12, 16", type = int, choices = [4,8,12,16],default=4)
    parser.add_argument("--c",help = "set camera filming rate(Hz)", type = int, default = 5)
    parser.add_argument("--ri",help = "set imu reading rate(Hz)", type = int, default = 50)
    parser.add_argument("--rl", help = "set LiDar reading rate(Hz)", type = int, default = 50)
    parser.add_argument("--p",help = "set the precision of the timing", type = float, default = 0.001)
    parser.add_argument("-s",help = "save the log locally after test", action="store_true", default=False)
    re = parser.parse_args()

    os.makedirs(beginTime+"/camera")





    datafile = beginTime+'/Lidar_IMU_Data.csv'

    rowList = []
    host = re.ip
    port = re.po
    duration = re.t
    trAccRate = re.sa
    trGyroRate = re.sg
    trMagRate = re.sm
    accScale = re.a
    gyroScale = re.g
    magScale = re.m
    lidarRate = float(1)/(re.rl)-0.0007   # minus 0.0007 to compensate for the call of time.time()
    imuRate = 1/float(re.ri)-0.0007
    precision = re.p
    cameraFreq = 1/float(re.c)
    save = re.s
    setIMUScale(accScale,gyroScale,magScale)
    setIMUodr(trAccRate,trGyroRate,trMagRate)
    if lib.lsm9ds1_begin(imu) == 0:
        print("Failed to communicate with LSM9DS1.")
        quit()
    lib.lsm9ds1_calibrate(imu)
    try:
        if ser.is_open == False:
            ser.open()
        print(time.time())
        alive = Event()
        #multicore process
        pic =  Process(target = capture,args=(alive,duration,cameraFreq,beginTime,))
        sensor = Process(target = getData,args=(alive,duration,precision,imuRate,lidarRate,datafile,rowList,))

        pic.start()
        sensor.start()
        pic.join()
        sensor.join()
        #subprocess.Popen("python3 socket_folder_server.py localhost 60004 \""+beginTime+"\"",shell=True)
    except KeyboardInterrupt:   # Ctrl+C
        if ser != None:
            ser.close()
        alive.set()
        pic.join()
        sensor.join()
    print(time.time())
    send(host,port,beginTime)
    if not save:
        os.system("rm -r \""+beginTime+"\"")
