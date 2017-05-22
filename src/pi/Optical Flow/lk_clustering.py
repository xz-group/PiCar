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
import matplotlib.pyplot as plt
#from scipy.cluster.hierarchy import linkage
from sklearn.cluster import MeanShift

width = 224
height = 128
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (width, height)
camera.framerate = 30
camera.shutter_speed = 5000
rawCapture = PiRGBArray(camera, size=(width, height))
ms = MeanShift()
# allow the camera to warmup
time.sleep(2)

lk_params = dict( winSize  = (23, 23),
                  maxLevel = 3,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

feature_params = dict( maxCorners = 500,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

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
            img = img[int(height/8):int(7*height/8),:,:]
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
                
                self.cluster = np.matrix([0,0]).reshape(-1,2)
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
                        if i == 0:
                            clusterDataX = np.matrix([[x]])
                            clusterDataY = np.matrix([[x]])
                            clusterData = np.matrix([[x,y]])
                            i = i + 1
                        else:
                            clusterData = np.vstack((clusterData,(x,y)))
                            clusterDataX = np.vstack((clusterDataX,x))
                            clusterDataY = np.vstack((clusterDataY,y))
                #Draw the FOE (not necessary)
                cv2.circle(vis, (self.foe[0], self.foe[1]), 2, (0, 255, 0), -1)
                
                self.tracks = new_tracks
            
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

            z = linkage
            self.frame_idx += 1
            self.prev_gray = frame_gray
            self.prev_time = self.time

            #Display the video
            cv2.imshow('lk_track', vis)
            #cv2.imshow('Before Equalization', frame_gray_old)
            #cv2.imshow('CLAHE (8,8)',frame_gray)
            
            
            ch = cv2.waitKey(1)

            #Necessary to clear the camera stream before next image is read in
            rawCapture.truncate(0)
            
            #plot when escape key is called
            if ch == 27:
                #z = linkage(clusterData)
                #print(z)
                plt.axis([0 , 224,0, 96])
                plt.ylabel('y')
                plt.xlabel('x')
                plt.title('tracked Points with relevant TTC')
                plt.scatter(clusterDataX,clusterDataY)
                plt.show()

                ms.fit(clusterData)
                labels = ms.labels_
                cluster_centers = ms.cluster_centers_
                n_clusters_ = len(np.unique(labels))
                print("number of estimated clusters:", n_clusters_)
                
                colors = 10*['r.','g.','b.','c.','k.','y.','m.']
                for i in range(len(clusterData)):
                    plt.plot(clusterData[i][0], clusterData[i],[1], colors[labels[i]],markersize = 10)
                plt.scatter(cluster_centers[:,0], cluster_centers[:,1],marker="x", color='k',linewidths = 5, zorder=10)
                plt.axis([0 , 224,0, 96])
                plt.ylabel('y')
                plt.xlabel('x')
                plt.title('tracked Points with relevant TTC')
                plt.show()
                
                break

def main():
    import sys
    print(__doc__)
    App().run()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
