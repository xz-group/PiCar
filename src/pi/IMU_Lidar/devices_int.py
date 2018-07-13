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
from counter_read import counter

def pre_exec():
    """
    Easy to use function to prevent the subprocess to receive KeyboardInterrupt
    """
    # To ignore CTRL+C signal in the new process
    signal.signal(signal.SIGINT, signal.SIG_IGN)

def filenames(alive,duration,cameraFreq,beginTime):
    """
    Filename generator: Used with Camera class to generate a series of filename for the picture to be stored at
    """
    startTime = time.time()
    lastTime = time.time()
    current = time.time()
    while current - startTime < duration and not alive.is_set():
        current = time.time()
        if current - lastTime > cameraFreq:
            #name = time.time()
            name = beginTime+'/camera/'+str(current)+'.jpg'
            lastTime = time.time()
            yield name


class Killer:
    def __init__(self,state):
        self.state = state
        signal.signal(signal.SIGINT, self.exit)
        signal.signal(signal.SIGTERM, self.exit)

    def exit(self,signum, frame):
        self.state.set()


class device(object):
    """
    Base class for all Devices
    """
    def __init__(self, name="D"):
        """
        device class constructor: child class initialize the communication, the device name and type here, act according to the behavior of the device, quit script if neccesary
        """
        self.name = name
        self.type = "virtual"

    def whoAmI(self):
        """
        A function that could be called to tell what device it is
        """
        print("My name is {}, I am a {} device".format(self.name, self.type))


class sensor(device):
    """
    Base class for all Sensors
    """
    def __init__(self, name="S"):
        self.name = name
        self.type = "sensor"
        self.__conn = None

    def setConn(self,conn):
        """
        A sensor's connection should be able to be reset by this function
        """
        print("You are assigning connection to a virtual sensor")
        self.__conn = conn

    def getConn(self):
        """
        The connection could be returned by this function
        """
        print("You are getting connection from a virtual sensor")
        return self.__conn

    def getValue(self):
        """
        A sensor should implement this method to return values in a list
        """
        print("Don't ask too much from a virtual sensor")
        return None

    def getFieldSize(self):
        """
        A sensor should implement this method to return the field size requested by the sensor in logging file
        """
        return 0

    def getHeader(self):
        """
        A sensor should implement this method to return the header of it requested field in a list
        """
        return ("Void")

    def detect(self):
        """
        A sensor should implement this method to tell if the sensor is currently available
        """
        print("I am virtual")
        return False

class pmucounter(sensor):
    """
    PMU (Performance Monitoring Unit) reader
    """
    def __init__(self, name = "P"):
        self.name = name
        self.type = "counter"
        self.__conn = counter

    def getValue(self):
        return self.__conn.ccnt_read()

    def getFieldSize(self):
        return 1

    def getHeader(self):
        return ("PMUreading")

    def detect(self):
        return True

class IMU(sensor):
    """
    This class for IMU sensor
    """
    def __init__(self, name="I"):
        """
        Constructor of IMU object:
        Usage: IMU(self, name = "I")
        It initializes an IMU object using lsm9ds1 library
        """
        self.name = name
        self.type = "IMU"
        self.__conn = lib.lsm9ds1_create()
        if lib.lsm9ds1_begin(self.__conn)==0:
            self.__conn = None
            print("Connection failed")
            quit()

    def setConn(self, conn):
        self.__conn = conn

    def calibrate(self):
        """
        A wrapper for IMU calibration
        """
        lib.lsm9ds1_calibrate(self.__conn)

    def detect(self):
        """
        This function tests if accel, gyro and mag are all available
        """
        if lib.lsm9ds1_accelAvailable(self.__conn) and lib.lsm9ds1_gyroAvailable(self.__conn) and lib.lsm9ds1_magAvailable(self.__conn):
            return True
        else:
            return False

    def setIMUodr(self, aRate=6, gRate=6, mRate=7):
        """
        Output rate setter for IMU
        Available rate for accel: 1 = 10 Hz    4 = 238 Hz
                                  2 = 50 Hz    5 = 476 Hz
                                  3 = 119 Hz   6 = 952 Hz
        Available rate for gyro : 1 = 14.9     4 = 238
                                  2 = 59.5     5 = 476
                                  3 = 119      6 = 952
        Available rate for mag  : 0 = 0.625 Hz  4 = 10 Hz
                                  1 = 1.25 Hz   5 = 20 Hz
                                  2 = 2.5 Hz    6 = 40 Hz
                                  3 = 5 Hz      7 = 80 Hz
        """
        lib.lsm9ds1_setAccelODR(self.__conn, aRate)
        lib.lsm9ds1_setGyroODR(self.__conn, gRate)
        lib.lsm9ds1_setMagODR(self.__conn, mRate)

    def setIMUScale(self, aScl=2, gScl=245, mScl=4):
        """
        Scale for IMU_SETUP
        Available rate for accel: 2, 4, 8, 16
        Available rate for gyro : 245, 500, 2000
        Available rate for mag  : 4, 8, 12, 16
        (Value set other than these value might cause IMU to crush)
        """
        lib.lsm9ds1_setAccelScale(self.__conn, aScl)
        lib.lsm9ds1_setGyroScale(self.__conn, gScl)
        lib.lsm9ds1_setMagScale(self.__conn, mScl)

    def getFieldSize(self):
        return 9

    def getHeader(self):
        return ["AccelX","AccelY","AccelZ","GyroX","GyroY","GyroZ","MagX","MagY","MagZ"]

    def getValue(self):
        """
        Return a 9-elements list containing all IMU reading
        """
        lib.lsm9ds1_readAccel(self.__conn)
        lib.lsm9ds1_readGyro(self.__conn)
        lib.lsm9ds1_readMag(self.__conn)
        ax = lib.lsm9ds1_getAccelX(self.__conn)
        ay = lib.lsm9ds1_getAccelY(self.__conn)
        az = lib.lsm9ds1_getAccelZ(self.__conn)
        cax = lib.lsm9ds1_calcAccel(self.__conn, ax)
        cay = lib.lsm9ds1_calcAccel(self.__conn, ay)
        caz = lib.lsm9ds1_calcAccel(self.__conn, az)
        gx = lib.lsm9ds1_getGyroX(self.__conn)
        gy = lib.lsm9ds1_getGyroY(self.__conn)
        gz = lib.lsm9ds1_getGyroZ(self.__conn)
        cgx = lib.lsm9ds1_calcGyro(self.__conn, gx)
        cgy = lib.lsm9ds1_calcGyro(self.__conn, gy)
        cgz = lib.lsm9ds1_calcGyro(self.__conn, gz)
        mx = lib.lsm9ds1_getMagX(self.__conn)
        my = lib.lsm9ds1_getMagY(self.__conn)
        mz = lib.lsm9ds1_getMagZ(self.__conn)
        cmx = lib.lsm9ds1_calcMag(self.__conn, mx)
        cmy = lib.lsm9ds1_calcMag(self.__conn, my)
        cmz = lib.lsm9ds1_calcMag(self.__conn, mz)
        return [cax, cay, caz, cgx, cgy, cgz, cmx, cmy, cmz]

class LiDar(sensor):
    def __init__(self, name="L"):
        self.name = name
        self.type = "LiDar"
        self.__conn = serial.Serial("/dev/ttyS0", 115200)

    def setConn(self, conn):
        self.__conn = conn

    def open(self):
        if self.__conn.is_open == False:
            self.__conn.open()

    def close(self):
        if self.__conn.is_open == True:
            self.__conn.close()

    def detect(self):
        if self.__conn.in_waiting > 8:
            return True
        else:
            return False

    def getFieldSize(self):
        return 1

    def getHeader(self):
        return ["LiDar"]

    def getValue(self):
        """
        Return a 1 element list
        """
        recv = self.__conn.read(9)
        self.__conn.reset_input_buffer()

        if recv[0] == 0x59 and recv[1] == 0x59:
            distance = recv[2] + recv[3] * 256
            self.__conn.reset_input_buffer()
            return [distance]
        else:
            self.__conn.reset_input_buffer()
            return [None]

class Camera(device):
    def __init__(self, name="C", res=(480,480), fr = 40):
        self.name = name
        self.type = "camera"
        self.camera = picamera.PiCamera(resolution=res, framerate=fr)

    def __del__(self):
        self.camera.close()

    def setRes(self, res):
        """
        res is a tuple (length,width) in pixel
        """
        self.camera.resolution = res

    def setFrameRate(self, fr):
        """
        fr is in Hz
        """
        self.camera.framerate = fr

    def capture(self, gen, *args):
        """
        gen : a filename generator that has timing functionality
        *args : contains all the arguments gen needs
        """
        self.camera.capture_sequence(gen(*args), use_video_port=True)


class Timer:
    """
    A Timer class that helps get delta timing for a sensor
    """
    def __init__(self, kit, gap):
        """
        kit : the Sensor
        gap : the delta time
        """
        self.gap = gap
        self.kit = kit
        self.last = time.time()
        self.size = self.kit.getFieldSize()

    def read(self,t):
        if t-self.gap>self.last and self.kit.detect():
            self.last = t
            return self.kit.getValue()
        else:
            return [None]*self.size


def getCamera(gen,alive,duration,cameraFreq,beginTime):
    """
    The filming function executed in a different core
    gen        : the filenames generator
    alive      : the global variable to track the state in the main function
    duration   : the elapse time for the test
    cameraFreq : the cameraFrequncy in Hz
    beginTime  : (string) the directory of the root folder for the logging files
    """
    pre_exec()
    cam = Camera()
    cam.capture(gen,alive,duration,cameraFreq,beginTime)

def getSensor(alive,rowList,duration,precision,datafile,timers):
    """
    The data logging function executed in a different core
    alive: the global variable to track the state in the main function
    rowList: a list stores timestamp and logging data
    duration: the elapse time for the test
    precision: the gap between two visit of the script to sensors
    datafile: file name of the datafile
    timers: a list of timers holding sensors
    """
    pre_exec()
    #print("enter sensor")
    startTime = time.time()
    lastTime = time.time()
    current = time.time()
    while current-startTime<duration and not alive.is_set():
        #print("enterloop")
        if current-lastTime>precision:
            lastTime = current
            r = [current]
            f = False
            for timer in timers:
                k = timer.read(current)
                if not f and k[0]!=None:
                    f = True
                r+=k[0:]
            if f:
                #print("goodline")
                rowList.append(r)
        current = time.time()
    print("start writing data")
    with open(datafile,"w") as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for row in rowList:
            spamwriter.writerow(row)



def getSensorAndCamera(host='192.168.1.121',port=6000,save=False,duration=5,endless=False,trAccRate=6,trGyroRate=6,
                        trMagRate=7,accScale=2,gyroScale=245,magScale=4,cameraFreq=5,imuRate=50,lidarRate=50,precision=0.001,tm=[]):
    """
    A easy to use logging version supporting camera data logging, IMU reading, Lidar reading
    """
    beginTime = str(datetime.datetime.now()).replace(" ","@")
    os.makedirs(beginTime+"/camera")
    datafile = beginTime+'/Lidar_IMU_Data.csv'
    rowList=[]
    if endless:
        duration = 1000
    lidarRate = float(1)/lidarRate - 0.0007
    imuRate = float(1)/imuRate - 0.0007
    cameraFreq = float(1)/cameraFreq
    imu = IMU()
    imu.setIMUScale(accScale,gyroScale,magScale)
    imu.setIMUodr(trAccRate,trGyroRate,trMagRate)
    imu.calibrate()
    lidar = LiDar()
    pc = pmucounter()
    pc_timer = Timer(pc, 0.02)
    imu_timer = Timer(imu, imuRate)
    lidar_timer = Timer(lidar, lidarRate)
    a = [None]
    timers = [pc_timer,lidar_timer,imu_timer]+tm[0:]
    for timer in timers:
        a+=timer.kit.getHeader()[0:]
    rowList.append(a)
    lidar.open()
    print(datetime.datetime.now())
    alive = Event()
    k = Killer(alive)
    #multicore process
    pic =  Process(target = getCamera,args=(filenames,alive,duration,cameraFreq,beginTime,))
    sensor = Process(target = getSensor,args=(alive,rowList,duration,precision,datafile,timers,))
    pic.start()
    sensor.start()
    pic.join()
    sensor.join()
        #subprocess.Popen("python3 socket_folder_server.py localhost 60004 \""+beginTime+"\"",shell=True)

    lidar.close()
    print(datetime.datetime.now())
    send(host,port,beginTime)
    if not save:
        os.system("rm -r \""+beginTime+"\"")



if __name__ == '__main__':
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


    host = re.ip
    port = re.po
    duration = re.t
    trAccRate = re.sa
    trGyroRate = re.sg
    trMagRate = re.sm
    accScale = re.a
    gyroScale = re.g
    magScale = re.m
    lidarRate = re.rl   # minus 0.0007 to compensate for the call of time.time()
    imuRate = re.ri
    precision = re.p
    cameraFreq = re.c
    save = re.s

    getSensorAndCamera(host,port,save,duration,False,trAccRate,trGyroRate,trMagRate,accScale,gyroScale,magScale,cameraFreq,imuRate,lidarRate,precision)
