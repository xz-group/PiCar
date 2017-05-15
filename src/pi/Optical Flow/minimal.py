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

camera = PiCamera()
camera.resolution = (240, 180)
camera.framerate = 40
rawCapture = PiRGBArray(camera, size=(240, 180))

# allow the camera to warmup
time.sleep(0.1)

lk_params = dict( winSize  = (15, 15),
                  maxLevel = 2,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

feature_params = dict( maxCorners = 500,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

#grab image
camera.capture(rawCapture, format="bgr")
curr = rawCapture.array

curr_gray = cv2.cvtColor(curr, cv2.COLOR_BGR2GRAY)

#clear stream
rawCapture.truncate(0)
mask = np.zeros_like(curr_gray)
mask[:] = 255
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
        img = frame.array
        prev_gray = curr_gray;
        curr_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        p = cv2.goodFeaturesToTrack(curr_gray, mask = mask, **feature_params)
        p1, st, err = cv2.calcOpticalFlowPyrLK(prev_gray, curr_gray, p, None, **lk_params)
        mask = np.zeros_like(curr_gray)
        mask[:] = 255
        for i in range(p1.size):
            cv2.circle(mask, (p[i,0],p[i,1]), 5, 0, -1)
        cv2.imshow('lk_track', img)

        ch = cv2.waitKey(1)
        
        rawCapture.truncate(0)
            
        if ch == 27:
            break
        
