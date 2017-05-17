#!/usr/bin/env python

'''
Lucas-Kanade tracker
====================

Lucas-Kanade sparse optical flow demo. Uses goodFeaturesToTrack
for track initialization and back-tracking for match verification
between frames.

Usage
-----
lk_track.py


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
import matplotlib.pyplot as plt

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (224, 128)
camera.framerate = 30
camera.shutter_speed = 5000
rawCapture = PiRGBArray(camera, size=(224, 128))

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
video1 = cv2.VideoWriter('TestControl.avi',fourcc, 20.0, (width,height))

#camera.exposure_mode = 'off'
lk_params = dict( winSize  = (23, 23),
                  maxLevel = 3,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

feature_params = dict( maxCorners = 500,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )
ttcAvg = np.arange(10)
FILTER_COUNTS = 10

class App:
    def __init__(self):
        self.track_len = 10
        self.detect_interval = 5
        self.tracks = []
        self.frame_idx = 0
        self.prev_time = 0
        self.time = 0
        self.foe = np.matrix([0,0]).reshape(2,1)
        self.data = list()
        self.runCount = list()
        self.inc = 0
        
    def run(self):
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            #Read from camera
            img = frame.array
            
            #To grayscale and equalize
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            frame_gray = clahe.apply(cv2.cvtColor(img, cv2.COLOR_BGR2GRAY))
            
            vis = img.copy()
            
            if len(self.tracks) > 0:
                img0, img1 = self.prev_gray, frame_gray
                p0 = np.float32([tr[-1] for tr in self.tracks]).reshape(-1, 1, 2)
                p1, st, err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
                p0r, st, err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)
                self.time = time.time()
                
                vec = abs(p0-p0r).reshape(-1, 2)
                d = vec.max(-1)
                good = d < 1
                
                new_tracks = []

                i = 0
                ttcCount = 0
                ttcSum = 0
                xSum = 0
                ySum = 0
                
                for tr, (x, y), (u,v), (x2,y2), good_flag in zip(self.tracks, p1.reshape(-1, 2), vec, p0r.reshape(-1,2), good):
                    if not good_flag:
                        continue
                    tr.append((x, y))
                    
                    #Calculate matrices for FOE
                    b0 = x*v-y*u
                    if i == 0:
                        A = np.matrix([[u,v]])
                        b = np.matrix([[b0]])
                        i = i + 1
                    else:
                        A = np.vstack((A,(u,v)))
                        b = np.vstack((b,b0))

                    if len(tr) > self.track_len:
                        del tr[0]
                        
                    new_tracks.append(tr)
                    #cv2.circle(vis, (x, y), 2, (0, 255, 0), -1)

                    #TTC
                    d = math.sqrt((self.foe[0]-x)*(self.foe[0]-x)+(self.foe[1]-y)*(self.foe[1]-y))
                    dDot = math.sqrt((x2-x)*(x2-x)+(y2-y)*(y2-y))/(self.time-self.prev_time)
                    ttc = d/dDot

                    #Print TTC
                    if ttc < 15:
                        cv2.putText(vis,'%.2f' % ttc, (x,y), cv2.FONT_HERSHEY_SIMPLEX,.3,(0,255,0))
                        ttcCount = ttcCount+1
                        ttcSum = ttc + ttcSum
                        xSum = xSum + x
                        ySum = ySum + y
                        
                #ROLLING AVERAGE FILTER
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

                if xAvg == 0:
                    #draw_str(vis, (20, 20), 'STRAIGHT')
                    cv2.putText(vis,'STRAIGHT', (5,100), cv2.FONT_HERSHEY_SIMPLEX,.3,(0,255,0))
                elif xAvg < 112:
                    #draw_str(vis, (20, 20), 'RIGHT')
                    cv2.putText(vis,'RIGHT', (5,100), cv2.FONT_HERSHEY_SIMPLEX,.3,(0,255,0))
                else:
                    #draw_str(vis, (20, 20), 'LEFT')
                    cv2.putText(vis,'LEFT', (5,100), cv2.FONT_HERSHEY_SIMPLEX,.3,(0,255,0))
                    
                if ttcTotalAvg == 0:
                    cv2.putText(vis,'NOTHING', (5,60), cv2.FONT_HERSHEY_SIMPLEX,.3,(0,255,0))
                    #draw_str(vis, (20, 20), 'NOTHING')
                elif ttcTotalAvg < 7:
                    cv2.putText(vis,'MOVE BITCH', (5,60), cv2.FONT_HERSHEY_SIMPLEX,.3,(0,255,0))
                    #draw_str(vis, (20, 20), 'MOVE BITCH')
                else:
                    cv2.putText(vis,'MOVE SLIGHTLY', (5,60), cv2.FONT_HERSHEY_SIMPLEX,.3,(0,255,0))
                    #draw_str(vis, (20, 20), 'MOVE SLIGHTLY')
                    
                #Calculate new FOE
                try:
                        part1 = inv(np.matmul(A.transpose(),A))
                except:
                    print('ERROROROROROR-------------------CAUGHT')
                    self.foe = self.foe
                else:
                    self.foe = np.matmul(part1,np.matmul(A.transpose(),b))

                if ttcTotalAvg != 0:
                    self.data.append(ttcTotalAvg)
                    self.runCount.append(len(self.data))
                
                self.tracks = new_tracks
                #cv2.polylines(vis, [np.int32(tr) for tr in self.tracks], False, (0, 255, 0))
                #draw_str(vis, (20, 20), '%d' % len(self.tracks))
                draw_str(vis, (20, 20), '%.2f' % ttcTotalAvg)
          
            if self.frame_idx % self.detect_interval == 0:
                mask = np.zeros_like(frame_gray)
                mask[:] = 255
                for x, y in [np.int32(tr[-1]) for tr in self.tracks]:
                    cv2.circle(mask, (x, y), 5, 0, -1)
                p = cv2.goodFeaturesToTrack(frame_gray, mask = mask, **feature_params)
                if p is not None:
                    for x, y in np.float32(p).reshape(-1, 2):
                        self.tracks.append([(x, y)])


            self.frame_idx += 1
            self.prev_gray = frame_gray
            self.prev_time = self.time
            
            cv2.imshow('lk_track', vis)
            #cv2.imshow('Before Equalization', frame_gray_old)
            #cv2.imshow('CLAHE (8,8)',frame_gray)
            #Write frame to VideoWriter
            video1.write(vis)
            video1.write(vis)
            
            ch = cv2.waitKey(1)
            rawCapture.truncate(0)
            
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
