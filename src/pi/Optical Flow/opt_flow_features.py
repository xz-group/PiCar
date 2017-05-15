#!/usr/bin/env python

'''

----------------------------IMPROVE-------------------
1. Need to figure out how lk_track.py works in order to implement features
2. goal is to create vector fields around features


example to show optical flow

USAGE: opt_flow.py [<video_source>]

Keys:
 1 - toggle HSV flow visualization
 2 - toggle glitch

Keys:
    ESC    - exit
'''

# Python 2/3 compatibility
from __future__ import print_function
import numpy as np
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
import imutils
import time


def draw_flow(img, flow, step=16):
    h, w = img.shape[:2]
    y, x = np.mgrid[step/2:h:step, step/2:w:step].reshape(2,-1).astype(int)
    fx, fy = flow[y,x].T
    lines = np.vstack([x, y, x+fx, y+fy]).T.reshape(-1, 2, 2)
    lines = np.int32(lines + 0.5)
    vis = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    cv2.polylines(vis, lines, 0, (0, 255, 0))
    for (x1, y1), (x2, y2) in lines:
        cv2.circle(vis, (x1, y1), 1, (0, 255, 0), -1)
    return vis

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (240, 180)
camera.framerate = 15
rawCapture = PiRGBArray(camera, size=(240, 180))

# allow the camera to warmup
time.sleep(0.1)

#grab image
camera.capture(rawCapture, format="bgr")
prev = rawCapture.array

prevgray = cv2.cvtColor(prev, cv2.COLOR_BGR2GRAY)
show_hsv = False
show_glitch = False
cur_glitch = prev.copy()

#clear stream
rawCapture.truncate(0)

for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    img = frame.array
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    flow = cv2.calcOpticalFlowFarneback(prevgray, gray, None, 0.5, 3, 15, 3, 5, 1.2, 0)
    prevgray = gray

    cv2.imshow('flow', draw_flow(gray, flow))


    ch = cv2.waitKey(5)
    if ch == 27:
        break

    rawCapture.truncate(0)
cv2.destroyAllWindows()
