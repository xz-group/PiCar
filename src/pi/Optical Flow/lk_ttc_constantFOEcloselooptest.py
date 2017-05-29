#!/usr/bin/env python

'''
Lucas-Kanade tracker
====================

Lucas-Kanade sparse optical flow demo and time to contact calculation.

Usage
-----
lk_ttc.py
ESC to exit
'X' out plot

Keys
----
ESC - exit 
'''

# Python 2/3 compatibility
from __future__ import print_function
import time
import numpy as np
import spidev
import cv2
from common import anorm2, draw_str
from time import clock
from time import sleep
import video
import imutils
from picamera.array import PiRGBArray
from picamera import PiCamera
from numpy.linalg import inv
import math
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import sys
from sklearn.cluster import DBSCAN


SLAVE_SELECT = 18

spi = spidev.SpiDev()
spi.open(0,0)

GPIO.setmode(GPIO.BCM)
GPIO.setup(SLAVE_SELECT,GPIO.OUT)

SEND_PWM = [1]
SEND_SERVO = [2]
SEND_BACK = [3]
SEND_KILL = [4]

DEFAULT_ANGLE = 90


DELAY = .0001

width = 224
height = 128

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (width, height)
camera.framerate = 25
camera.shutter_speed = 5000
rawCapture = PiRGBArray(camera, size=(width, height))

# allow the camera to warmup
time.sleep(2)

#UNCOMMENT IF WANT TO RECORD VIDEO
#initialize VideoWriter object
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
video1 = cv2.VideoWriter('constFOE.avi',fourcc, 20.0, (width-24,height-28-18))

lk_params = dict( winSize  = (23, 23),
                  maxLevel = 3,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

feature_params = dict( maxCorners = 500,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

FILTER_COUNTS = 5
ttcAvg = np.arange(FILTER_COUNTS)
ttcMin = 5


#SPI Methods
def sendPWM(pwm):
    GPIO.output(SLAVE_SELECT,GPIO.LOW) 
    val1 = spi.xfer(SEND_PWM)
    sleep(DELAY)
    GPIO.output(SLAVE_SELECT,GPIO.HIGH)
    GPIO.output(SLAVE_SELECT,GPIO.LOW)
    val2 = spi.xfer(pwm)
    sleep(DELAY)
    GPIO.output(SLAVE_SELECT,GPIO.HIGH)
    #print(val1)
    #print(val2)

def sendBackPWM(pwm):
    GPIO.output(SLAVE_SELECT,GPIO.LOW)
    val1 = spi.xfer(SEND_BACK)
    sleep(DELAY)
    GPIO.output(SLAVE_SELECT,GPIO.HIGH)
    GPIO.output(SLAVE_SELECT,GPIO.LOW)
    val2 = spi.xfer(pwm)
    sleep(DELAY)
    GPIO.output(SLAVE_SELECT,GPIO.HIGH)
    #print(val1)
    #print(val2)

def sendServoAngle(servo):
    GPIO.output(SLAVE_SELECT,GPIO.LOW)
    val1 = spi.xfer(SEND_SERVO)
    sleep(DELAY)
    GPIO.output(SLAVE_SELECT,GPIO.HIGH) 
    GPIO.output(SLAVE_SELECT,GPIO.LOW)
    val2 = spi.xfer(servo)
    sleep(DELAY)
    GPIO.output(SLAVE_SELECT,GPIO.HIGH)
    #print(val1)
    #print(val2)
    
def sendKill():
    for i in range(0,10):
        GPIO.output(SLAVE_SELECT,GPIO.LOW);
        val1 = spi.xfer(SEND_KILL)
        GPIO.output(SLAVE_SELECT,GPIO.HIGH)
        print("Kill")

#PID Controller
def updatePID(self, err):
        """Calculates PID value for given reference feedback

        .. math::
            u(t) = K_p e(t) + K_i \int_{0}^{t} e(t)dt + K_d {de}/{dt}

        .. figure:: images/pid_1.png
           :align:   center

           Test PID with Kp=1.2, Ki=1, Kd=0.001 (test_pid.py)

        """

        self.current_time = time.time()
        delta_time = self.current_time - self.last_time
        delta_error = err - self.last_error

        iterm = 0
        
        sample_time = 0

        if (delta_time >= sample_time):
            pterm = self.Kp * err
            iterm += err * delta_time

            if (iterm < -self.windup_guard):
                iterm = -self.windup_guard
            elif (iterm > self.windup_guard):
                iterm = self.windup_guard

            dterm = 0.0
            if delta_time > 0:
                dterm = delta_error / delta_time

            # Remember last time and last error for next calculation
            self.last_time = self.current_time
            self.last_error = err

            output = pterm + (self.Ki * iterm) + (self.Kd * dterm)

            return output

class App:  

    def __init__(self):
        self.track_len = 10
        self.detect_interval = 1
        self.tracks = []
        self.frame_idx = 0
        self.prev_time = 0
        self.time = 0
        self.foe = np.matrix([100,45]).reshape(2,1)
        self.data = list()
        self.runCount = list()
        self.inc = 0

        #PID Variables
        self.current_time = 0
        self.last_time = 0
        self.Kp = 0.75
        self.Ki = 0.1
        self.Kd = 0
        self.last_error = 0
        self.windup_guard = 20


    def run(self):
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            #------------------------READ AND PREPROCESS IMAGE-------------------------------------------------
            #Read from camera
            img = frame.array
            
            
            #Slice unnecessary pixels off image
            img = img[18:height-28,12:212,:]
            
            #To grayscale and equalize
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))

            frame_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            std = np.std(frame_gray)

            vis = img.copy()
            
            if std < 20:
                rawCapture.truncate(0)
                continue
            
            frame_gray = clahe.apply(frame_gray)
            ttcCount = 0
            clusterData = np.matrix([[0,0]])


            #------------------------------CALCULATE OPTICAL FLOW-----------------------------------------
            if len(self.tracks) > 0:
                #img0, img1 = self.prev_gray, frame_gray
                
                #puts in right data type and size
                #p0 features in old frame to look for in new frame
                p0 = np.float32([tr[-1] for tr in self.tracks]).reshape(-1, 1, 2)
                
                #calculates optical flow (second optical flow used for a validity check)
                #p0 old coordinates, p1 new coordinates of same pixel
                lkTime = time.time()
                p1, st, err = cv2.calcOpticalFlowPyrLK(self.prev_gray, frame_gray, p0, None, **lk_params)
                p0r, st, err = cv2.calcOpticalFlowPyrLK(frame_gray, self.prev_gray, p1, None, **lk_params)
                lkTime = time.time()-lkTime
##                print('Optical Flow time = ')
##                print(lkTime)
##                print('')

                #timestamp used for velocity in ttc
                self.time = time.time()

                #Current points - previous points creates vector of displacement
                #used in ttc calculation
                vec = (p1-p0).reshape(-1,2)


                #Compare previous points with those found in second optical flow calculation
                d = abs(p0-p0r).reshape(-1, 2).max(-1)

                #validity check
                good = d < 1
                
                #rotation_filter = vec[:,0] > 10*vec[:,1]

                #reset parameters to be used in for loop below
                new_tracks = []
                i = 0
                ttcCount = 0
                clusterData = np.matrix([[0,0,0]])

                #Tracks are added, Focus of expansion is calculated, ttc calculated for each point
                for tr, (x, y), (u,v), good_flag in zip(self.tracks, p1.reshape(-1, 2), vec, good):
                    #If not valid, break from loop
                    if not good_flag:
                        continue
####                    if not rotation_check:
####                        continue
                  
                    #add feature to track
                    tr.append((x, y))
                    
                    if len(tr) > self.track_len:
                        del tr[0]
                        
                    new_tracks.append(tr)

                    #TTC (magnitude of displacement)/(velocity of displacement)
                    d = math.sqrt((self.foe[0]-x)*(self.foe[0]-x)+(self.foe[1]-y)*(self.foe[1]-y))
                    dDot = math.sqrt(u*u+v*v)/(self.time-self.prev_time)

                    #If dDot == 0, throws error so check
                    if dDot != 0:
                        ttc = d/dDot
                    else:
                        continue

                    #Print TTC for relevant points (ttcMin instantiated at beginning of program)
                    if ttc < ttcMin:
                        #cv2.putText(vis,'%.2f' % ttc, (x,y), cv2.FONT_HERSHEY_SIMPLEX,.3,(0,255,0))
                        ttcCount = ttcCount+1
                        
                        #Gather clustering data
                        if i == 0:
                            clusterData = np.matrix([[x,y,ttc]])
                            #clusterDataX = np.matrix([[x]])
                            i = i + 1
                        else:
                            clusterData = np.vstack((clusterData,(x,y,ttc)))
                            #clusterDataX = np.vstack((clusterDataX,x))
##
##            #K-MEANS CLUSTERING
##            if ttcCount > 5 :
##                # generating bright palette
##                cluster_n = 3
##                colors = np.zeros((1, cluster_n, 3), np.uint8)
##                colors[0,:] = 255
##                colors[0,:,0] = np.arange(0, 180, 180.0/cluster_n)
##                colors = cv2.cvtColor(colors, cv2.COLOR_HSV2BGR)[0]
##                
##                term_crit = (cv2.TERM_CRITERIA_EPS, 30, 0.1)
##                kmeansTime = time.time()
##                ret, labels, centers = cv2.kmeans(clusterData, cluster_n, None, term_crit, 10, 0)
##                kmeansTime = time.time()-kmeansTime
##                print('Number of points = %d ' % len(labels))
##                print('kmeans time = ')
##                print(kmeansTime)
##                print('')
##                
##                labels = labels.ravel()
##                for j in range(len(labels)):
##                    x_ = clusterData[j,0]
##                    y_ = clusterData[j,1]
##                    label_ = labels[j]
##                    
##                    c = list(map(int, colors[label_]))
##                    cv2.circle(vis, (x_, y_), 1, c, -1)

##                        #DBSCAN CLUSTERING ALGORITHM

                xSum,x0Sum,x1Sum,x2Sum,x3Sum,x4Sum = 0,0,0,0,0,0
                ySum,y0Sum,y1Sum,y2Sum,y3Sum,y4Sum = 0,0,0,0,0,0
                ttcSum = 0
                ttcSumArr = np.array([0.0,0.0,0.0,0.0,0.0])
                xSumArr = np.array([0,0,0,0,0])
                ySumArr = np.array([0,0,0,0,0])
                ttcCountArr = np.array([0,0,0,0,0])
                xAvg,yAvg,ttcTotalAvg = 0,0,0
                #ttc0Sum, ttc1Sum, ttc2Sum, ttc3Sum, ttc4Sum = 0,0,0,0,0,0
                
                dbscanTime = time.time()
                db = DBSCAN(eps=17,min_samples=2).fit(clusterData)
                dbscanTime = time.time()-dbscanTime
##                print('dbscan Time = ')
##                print(dbscanTime)
##                print('')
                
                labels = db.labels_
                n_clusters = len(set(labels))-(1 if -1 in labels else 0)
            
##                        print('Estimated number of clusters: %d' % n_clusters)
                #print(labels)                        
                for k in set(labels):
                    if k == -1:
                        continue
                    class_member_mask = (labels == k)
                    xy = clusterData[class_member_mask]

                    for x_,y_,ttc_ in zip(xy[:,0],xy[:,1],xy[:,2]):
                        if k == 0:
                            ttcSumArr[0] += ttc_
                            xSumArr[0] += x_
                            ySumArr[0] += y_
                            ttcCountArr[0]+=1
                            cv2.putText(vis,'x', (x_,y_), cv2.FONT_HERSHEY_SIMPLEX,.25,(255,0,0))
                        elif k == 1:
                            ttcSumArr[1] += ttc_
                            xSumArr[1] += x_
                            ySumArr[1] += y_
                            ttcCountArr[1]+=1
                            cv2.putText(vis,'x', (x_,y_), cv2.FONT_HERSHEY_SIMPLEX,.25,(0,255,0))
                        elif k == 2:
                            ttcSumArr[2] += ttc_
                            xSumArr[2] += x_
                            ySumArr[2] += y_
                            ttcCountArr[2]+=1
                            cv2.putText(vis,'x', (x_,y_), cv2.FONT_HERSHEY_SIMPLEX,.25,(0,0,255))
                        elif k == 3:
                            ttcSumArr[3] += ttc_
                            xSumArr[3] += x_
                            ySumArr[3] += y_
                            ttcCountArr[3]+=1
                            cv2.putText(vis,'x', (x_,y_), cv2.FONT_HERSHEY_SIMPLEX,.25,(0,255,255))
                        elif k == 4:
                            ttcSumArr[4] += ttc_
                            xSumArr[4] += x_
                            ySumArr[4] += y_
                            ttcCountArr[4]+=1
                            cv2.putText(vis,'x', (x_,y_), cv2.FONT_HERSHEY_SIMPLEX,.25,(255,0,255))
                            
                #print(ttcSumArr)
                if(sum(ttcCountArr) > 0):
                    ttcAvgArr = ttcSumArr/ttcCountArr
                    #print(ttcAvgArr)
                    ttcTotalAvg = min(m for m in ttcAvgArr if m > 0)
                    minIndex = np.where(ttcAvgArr == ttcTotalAvg)[0][0]
                    xAvg = xSumArr[minIndex]/ttcCountArr[minIndex]
                    yAvg = ySumArr[minIndex]/ttcCountArr[minIndex]
                    cv2.circle(vis,(int(xAvg),int(yAvg)),5,(255,0,100),-1)
                    if minIndex == 0:
                        cv2.putText(vis,'%.2f' % ttcTotalAvg, (5,40), cv2.FONT_HERSHEY_SIMPLEX,.3,(255,0,0))
                    elif minIndex == 1:
                        cv2.putText(vis,'%.2f' % ttcTotalAvg, (5,40), cv2.FONT_HERSHEY_SIMPLEX,.3,(0,255,0))
                    elif minIndex == 2:
                        cv2.putText(vis,'%.2f' % ttcTotalAvg, (5,40), cv2.FONT_HERSHEY_SIMPLEX,.3,(0,0,255))
                    elif minIndex == 3:
                        cv2.putText(vis,'%.2f' % ttcTotalAvg, (5,40), cv2.FONT_HERSHEY_SIMPLEX,.3,(0,255,255))
                    elif minIndex == 4:
                        cv2.putText(vis,'%.2f' % ttcTotalAvg, (5,40), cv2.FONT_HERSHEY_SIMPLEX,.3,(255,0,255))
                    
                    
                   # print('Smallest TTC = %.2f' % ttcTotalAvg)
                        
                #ROLLING AVERAGE FILTER
                #Each entry in rolling average array is the average of all points with small time to contact
##                ttcTotalAvg = 0
##                xAvg = 0
##                yAvg = 0
##
##                rAvgTime = time.time()
##
##                if ttcCount > 0:
##                    self.inc = self.inc + 1        
##                    ttcAvg[self.inc % FILTER_COUNTS] = ttcSum/ttcCount
##                    xAvg = xSum/ttcCount
##                    yAvg = ySum/ttcCount
##                    
##                    for val in ttcAvg:
##                        ttcTotalAvg = val + ttcTotalAvg
##                    
##                    ttcTotalAvg = ttcTotalAvg/FILTER_COUNTS
##
##                rAvgTime = time.time()-rAvgTime


                #-----------------------------A PRETEND CONTROL OUTPUT---------------------------------------
                #Decides which direction to turn based on location of the center of each point
                #Tells how quickly to turn based on magnitude of the ttc average

                temp = DEFAULT_ANGLE
                EPSILON = 5
                midpoint = 100
                #cv2.putText(vis,'%.2f' % ttcTotalAvg, (5,60), cv2.FONT_HERSHEY_SIMPLEX,.3,(0,255,0))
                cv2.line(vis,(midpoint-EPSILON,0),(midpoint-EPSILON,200),(0,0,255))
                cv2.line(vis,(midpoint+EPSILON,0),(midpoint+EPSILON,200),(0,0,255))
                if xAvg == 0:
                    #draw_str(vis, (20, 20), 'STRAIGHT')
                    cv2.putText(vis,'STRAIGHT', (5,70), cv2.FONT_HERSHEY_SIMPLEX,.3,(0,255,0))
                elif (xAvg < midpoint + EPSILON) and (xAvg > midpoint - EPSILON):
                    cv2.putText(vis,'BUFFER', (5,70), cv2.FONT_HERSHEY_SIMPLEX,.3,(0,255,0))
                    temp = int(midpoint + DEFAULT_ANGLE - xAvg)
                elif xAvg < midpoint:
                    #draw_str(vis, (20, 20), 'RIGHT')
                    cv2.putText(vis,'RIGHT', (5,70), cv2.FONT_HERSHEY_SIMPLEX,.3,(0,255,0))
                    ##in this elif desired xAvg is 0
                    xDes = 0
                    xErr = xAvg - xDes
##                    xErr = pVal*xErr
                    xErr = updatePID(self,xErr)
                    temp = int(((90.0*(xErr/224.0) + DEFAULT_ANGLE)))
                else:
                    #draw_str(vis, (20, 20), 'LEFT')
                    cv2.putText(vis,'LEFT', (5,70), cv2.FONT_HERSHEY_SIMPLEX,.3,(0,255,0))
                    ##in this elif desired xAvg is 224
                    xDes = 224
                    xErr = xAvg - xDes
##                    xErr = pVal*xErr
                    xErr = updatePID(self,xErr)
                    temp = int((DEFAULT_ANGLE + 90.0*xErr/224.0))

                #Servo Angle Saturation    

                if temp > 130: 
                    temp = 130
                elif temp < 50:
                    temp = 50
                angle = [temp]

                #PWM Saturation
                temp1 = int(16*ttcTotalAvg)
                if ttcTotalAvg == 0:
                    temp1 = 200
                elif temp1 < 60:
                    temp1 = 60

                pwm = [temp1]

                #backup code
##                if ttcTotalAvg > 2 or ttcTotalAvg == 0:
##                    sendPWM(pwm)
##                else:
##                    pwm = [200]
##                    sendBackPWM(pwm)
##                    sleep(.5)
                
                sendPWM(pwm)                                     
                sendServoAngle(angle)

                #Create data for the plot
                #!= 0 filters out data when there is nothing to track
                if ttcTotalAvg != 0:
                    self.data.append(ttcTotalAvg)
                    self.runCount.append(len(self.data))
                
                self.tracks = new_tracks

                #Draws the lines and the track count (unnecessary)
                #cv2.polylines(vis, [np.int32(tr) for tr in self.tracks], False, (0, 255, 0))
                #draw_str(vis, (20, 20), '%d' % len(self.tracks))
          
            if self.frame_idx % self.detect_interval == 0:
                mask = np.zeros_like(frame_gray)
                mask[:] = 255
                
                for x, y in [np.int32(tr[-1]) for tr in self.tracks]:
                    cv2.circle(mask, (x, y), 5, 0, -1)
                    
                #get new features
                p = cv2.goodFeaturesToTrack(frame_gray, mask = mask, **feature_params)
                
                if p is not None:
                    for x, y in np.float32(p).reshape(-1, 2):
                        #add features to tracked points
                        self.tracks.append([(x, y)])


            self.frame_idx += 1
            
            self.prev_gray = frame_gray
            self.prev_time = self.time

            #Display the video
            cv2.imshow('lk_track', vis)

##            cv2.imshow('CLAHE (8,8)',frame_gray)

            #UNCOMMENT TO WRITE FRAME TO VIDEO
            video1.write(vis)
            video1.write(vis)
            
            ch = cv2.waitKey(1)

            #Necessary to clear the camera stream before next image is read in
            rawCapture.truncate(0)

            #plot when escape key is called

            if ch == 27:
                video1.release()
                plt.axis([0 , self.inc,0, 15])
                plt.ylabel('Time to Contact (s)')
                plt.xlabel('time')
                plt.title('Time to Contact')
                plt.plot(self.runCount,self.data)
                plt.show()
                break

def main():
    import sys
    print(__doc__)
    App().run()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
