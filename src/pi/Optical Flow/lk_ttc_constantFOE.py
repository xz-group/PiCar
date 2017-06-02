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
import cv2
from common import anorm2, draw_str
from time import clock
import video
import imutils
from picamera.array import PiRGBArray
from picamera import PiCamera
from numpy.linalg import inv
import math
##import matplotlib.pyplot as plt

width = 640
height = 240
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (width, height)
camera.framerate = 30
camera.shutter_speed = 5000
rawCapture = PiRGBArray(camera, size=(width, height))

# allow the camera to warmup
time.sleep(2)

#grab image
camera.capture(rawCapture, format="bgr")
frame = rawCapture.array
height,width,layers = frame.shape

#clear stream
rawCapture.truncate(0)

#initialize VideoWriter object
fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
video1 = cv2.VideoWriter('ttc_screenshot.avi',fourcc, 20.0, (width,height))

lk_params = dict( winSize  = (23, 23),
                  maxLevel = 3,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

feature_params = dict( maxCorners = 500,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

ttcAvg = np.arange(10)
FILTER_COUNTS = 10
ttcMin = 15
class App:
    def __init__(self):
        self.track_len = 10
        self.detect_interval = 5
        self.tracks = []
        self.frame_idx = 0
        self.prev_time = 0
        self.time = 0
        self.foe = np.matrix([112,48]).reshape(2,1)
        self.data = list()
        self.runCount = list()
        self.inc = 0

    def run(self):
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            #------------------------READ AND PREPROCESS IMAGE-------------------------------------------------
            #Read from camera
            img = frame.array

            #Slice unnecessary pixels off image
##            img = img[int(height/8):int(7*height/8),:,:]
            print(img.shape)
            #To grayscale and equalize
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            frame_gray = clahe.apply(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
            
            vis = img.copy()


            #------------------------------CALCULATE OPTICAL FLOW-----------------------------------------
            if len(self.tracks) > 0:
                img0, img1 = self.prev_gray, frame_gray
                
                #puts in right data type and size
                p0 = np.float32([tr[-1] for tr in self.tracks]).reshape(-1, 1, 2)
                
                #calculates optical flow (second optical flow used for a validity check)
                p1, st, err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
                p0r, st, err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)

                #timestamp used for velocity in ttc
                self.time = time.time()

                #Current points - previous points creates vector of displacement
                vec = p1-p0

                #Compare previous points with those found in second optical flow calculation
                d = abs(p0-p0r).reshape(-1, 2).max(-1)

                #validity check
                good = d < 1

                #reset parameters to be used in for loop below
                new_tracks = []
                i = 0
                ttcCount = 0
                ttcSum = 0
                xSum = 0
                ySum = 0

                #Tracks are added, Focus of expansion is calculated, ttc calculated for each point
                for tr, (x, y), (u,v), good_flag in zip(self.tracks, p1.reshape(-1, 2), vec.reshape(-1,2), good):
                    #If not valid, break from loop
                    if not good_flag:
                        continue
                    
                    #add feature to track
                    tr.append((x, y))
                    
                    #Calculate matrices for FOE (see paper for calculations)

                    if len(tr) > self.track_len:
                        del tr[0]
                        
                    new_tracks.append(tr)
                    
                    #can be used to draw circles at each tracked point
                    #cv2.circle(vis, (x, y), 2, (0, 255, 0), -1)

                    #TTC (magnitude of displacement)/(velocity of displacement)
                    d = math.sqrt((self.foe[0]-x)*(self.foe[0]-x)+(self.foe[1]-y)*(self.foe[1]-y))
                    dDot = math.sqrt(u*u+v*v)/(self.time-self.prev_time)

                    #If dDot == 0, throws error so check
                    if dDot != 0:
                        ttc = d/dDot
                    else:
                        ttc = 100

                    #Print TTC for relevant points (ttcMin instantiated at beginning of program)
                    if ttc < ttcMin:
                        cv2.putText(vis,'%.2f' % ttc, (x,y), cv2.FONT_HERSHEY_SIMPLEX,.3,(0,255,0))
                        
                        ttcCount = ttcCount+1
                        ttcSum = ttc + ttcSum
                        xSum = xSum + x
                        ySum = ySum + y
                        
                #ROLLING AVERAGE FILTER
                #Each entry in rolling average array is the average of all points with small time to contact
                ttcTotalAvg = 0
                xAvg = 0
                yAvg = 0
                
                if ttcCount > 0:
                    self.inc = self.inc + 1        
                    ttcAvg[self.inc % FILTER_COUNTS] = ttcSum/ttcCount
                    xAvg = xSum/ttcCount
                    yAvg = ySum/ttcCount
                    
                    for val in ttcAvg:
                        ttcTotalAvg = val + ttcTotalAvg
                    
                    ttcTotalAvg = ttcTotalAvg/FILTER_COUNTS

                #-----------------------------A PRETEND CONTROL OUTPUT---------------------------------------
                #Decides which direction to turn based on location of the center of each point
                #Tells how quickly to turn based on magnitude of the ttc average
##                if xAvg == 0:
##                    #draw_str(vis, (20, 20), 'STRAIGHT')
##                    #cv2.putText(vis,'STRAIGHT', (5,80), cv2.FONT_HERSHEY_SIMPLEX,.3,(0,255,0))
##                elif xAvg < 112:
##                    #draw_str(vis, (20, 20), 'RIGHT')
##                    #cv2.putText(vis,'RIGHT', (5,80), cv2.FONT_HERSHEY_SIMPLEX,.3,(0,255,0))
##                else:
##                    #draw_str(vis, (20, 20), 'LEFT')
##                    #cv2.putText(vis,'LEFT', (5,80), cv2.FONT_HERSHEY_SIMPLEX,.3,(0,255,0))
##                    
##                if ttcTotalAvg == 0:
##                    #cv2.putText(vis,'NOTHING', (5,60), cv2.FONT_HERSHEY_SIMPLEX,.3,(0,255,0))
##                    #draw_str(vis, (20, 20), 'NOTHING')
##                elif ttcTotalAvg < 7:
##                    #cv2.putText(vis,'MOVE QUICKLY', (5,60), cv2.FONT_HERSHEY_SIMPLEX,.3,(0,255,0))
##                    #draw_str(vis, (20, 20), 'MOVE BITCH')
##                else:
##                    #cv2.putText(vis,'MOVE SLIGHTLY', (5,60), cv2.FONT_HERSHEY_SIMPLEX,.3,(0,255,0))
##                    #draw_str(vis, (20, 20), 'MOVE SLIGHTLY')
                    

                #Draw the FOE (not necessary)
                cv2.circle(vis, (self.foe[0], self.foe[1]), 2, (0, 0, 255), -1)

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
            #cv2.imshow('Before Equalization', frame_gray_old)
            #cv2.imshow('CLAHE (8,8)',frame_gray)

            video1.write(vis)
            video1.write(vis)
            #video1.write(vis)
            
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
