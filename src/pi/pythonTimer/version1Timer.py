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

readFrequency = 0.019
cameraFrequency = 0.5
taskDuration = 10
frames = 5


sensorDataDeque = deque()
sensorData = []
writeFrequency = 10
dataFile = "sensorData.csv"

sensorDataNumpyArray = np.array(['time','distance','ax','ay','az','gx','gy','gz'])

#write sensor data to a csv file
def writeSensorData():
    global sensorDataNumpyArray
    writeStart = time.time()
    with open(dataFile,"a",newline = '') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
##        for row in sensorDataNumpyArray:
##            spamwriter.writerow([row])
        #writeTime = "writeTime:" + str(datetime.datetime.now())
        #title = [writeTime,len(sensorData)]
        #spamwriter.writerow(title)
        #length = len(sensorData)
        for element in sensorData:
            #row = [sensorData.pop()]
            spamwriter.writerow([element])
##        for element in sensorDataDeque:
##            spamwriter.writerow([element])
    sensorData.clear()
##    sensorDataNumpyArray = np.delete(sensorDataNumpyArray,slice(0,sensorDataNumpyArray.ndim),axis=0)    
    writeEnd = time.time()
    print("total writing time is %f" % (writeEnd - writeStart))
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


def getData():
    global last
    global sensorDataNumpyArray
    #print("pid for sensors:%d" % os.getpid())
    Timer(writeFrequency,writeSensorData).start()
    while True:
        time.sleep(readFrequency)
        #print("time for sensors:%f" % (time.time() - last))
        if lib.lsm9ds1_accelAvailable(imu) > 0 and ser.in_waiting > 8:
            #print("time for sensors:%f" % (time.time() - last))
            Lidardata = getLidar()
            IMUdata = getIMU()
            currentTime = str(datetime.datetime.now())
            #row = np.array([currentTime,Lidardata,IMUdata[0],IMUdata[1],IMUdata[2],IMUdata[3],IMUdata[4],IMUdata[5]])
            #sensorDataNumpyArray = np.vstack((sensorDataNumpyArray,row))
            row = [currentTime,Lidardata,IMUdata[0],IMUdata[1],IMUdata[2],IMUdata[3],IMUdata[4],IMUdata[5]]
            #sensorDataDeque.append(row)
            sensorData.append(row)
            #print(sensorDataNumpyArray)
            #print(Lidardata,IMUdata)
            #last = time.time()
        #last = time.time()
    #Timer(readFrequency,getData).start()


#generate photo names based on how many frames taken each time
def filenames():
    frame = 0
    while frame < frames:
        name = datetime.datetime.now()
        yield '%s.jpg' % name
        frame = frame + 1


#rapidly capturing photos, number is frames
def capture():
    #print("pid for camera %i" % os.getpid())
    global last
##    camera = PiCamera()
##    camera.resolution = (480,480)
##    camera.framerate = 40
    with picamera.PiCamera(resolution=(480,480), framerate=40) as camera:
        while True:
            time.sleep(cameraFrequency)
            #print("time for camera:%f" % (time.time() - last))
            #camera.capture_sequence(filenames(), use_video_port=True)
            last = time.time()
    #Timer(cameraFrequency,capture).start()


last = time.time()
if __name__ == '__main__':
    if lib.lsm9ds1_begin(imu) == 0:
        print("Failed to communicate with LSM9DS1.")
        quit()
    lib.lsm9ds1_calibrate(imu)
    
    if ser.is_open == False:
        ser.open()
    #Timer(readFrequency,getData).start()
    #Timer(cameraFrequency,capture).start()
    pool = Pool()
    sensors = pool.apply_async(getData)
    camera = pool.apply_async(capture)
    sensors.get()
    camera.get()
