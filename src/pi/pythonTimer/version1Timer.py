#!/usr/bin/env python
# -*- coding: utf-8 -*
from threading import Timer
from multiprocessing import Pool
from IMU_SETUP import lib
from collections import deque
import numpy as np
import time,datetime,serial,sys,csv,picamera,os

sys.version[0] == '3'
ser = serial.Serial("/dev/ttyS0", 115200)

imu = lib.lsm9ds1_create()
lib.lsm9ds1_begin(imu)

#Frequency for reading data
readFrequency = 0.019
cameraFrequency = 0.5
#taskDuration = 10
frames = 5

#Frequency for writing data
sensorData = []
writeFrequency = 10
dataFile = "sensorData.csv"


#write sensor data to a csv file based on writeFrequency
def writeSensorData():
    global sensorDataNumpyArray
    #writeStart = time.time()
    with open(dataFile,"a",newline = '') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for element in sensorData:
            #row = [sensorData.pop()]
            spamwriter.writerow([element])
    #After each writing, we clear the list to ease pressure
    sensorData.clear()

    writeEnd = time.time()
    #print("total writing time is %f" % (writeEnd - writeStart))
    Timer(writeFrequency,writeSensorData).start()


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


#get IMU and Lidar data at same time
def getData():
    global last
    global sensorDataNumpyArray
    Timer(writeFrequency,writeSensorData).start()
    while True:
        time.sleep(readFrequency)
        if lib.lsm9ds1_accelAvailable(imu) > 0 and ser.in_waiting > 8:
            #print("time for sensors:%f" % (time.time() - last))
            Lidardata = getLidar()
            IMUdata = getIMU()
            currentTime = str(datetime.datetime.now())

            row = [currentTime,Lidardata,IMUdata[0],IMUdata[1],IMUdata[2],IMUdata[3],IMUdata[4],IMUdata[5]]
            sensorData.append(row)
            #print(Lidardata,IMUdata)
            #last = time.time()


#generate photo names based on time, the number is determined by variable frames.
def filenames():
    frame = 0
    while frame < frames:
        name = datetime.datetime.now()
        yield '%s.jpg' % name
        frame = frame + 1


#rapidly capturing photos, number is frames
def capture():
    global last
    with picamera.PiCamera(resolution=(480,480), framerate=40) as camera:
        while True:
            time.sleep(cameraFrequency)
            #print("time for camera:%f" % (time.time() - last))
            camera.capture_sequence(filenames(), use_video_port=True)
            last = time.time()



last = time.time()
if __name__ == '__main__':
    if lib.lsm9ds1_begin(imu) == 0:
        print("Failed to communicate with LSM9DS1.")
        quit()
    lib.lsm9ds1_calibrate(imu)

    if ser.is_open == False:
        ser.open()

    pool = Pool()
    sensors = pool.apply_async(getData) #here sensors reading will run on one cpu
    camera = pool.apply_async(capture) #image capturing will run on another cpu

    #'get' helps to keep the programe run all the time, we do not expect any value from
    #sensors or data. This might be tricky, if it is hard to understand, just think the
    #following code as:
    #while True:
    #sensorReading
    #cameraReading
    sensors.get()
    camera.get()
