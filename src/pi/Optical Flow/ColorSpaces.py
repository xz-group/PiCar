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

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (240, 180)
camera.framerate = 30
camera.shutter_speed = 5000
rawCapture = PiRGBArray(camera, size=(240, 180))

# allow the camera to warmup
time.sleep(2)
#camera.exposure_mode = 'off'
lk_params = dict( winSize  = (23, 23),
                  maxLevel = 3,
                  criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

feature_params = dict( maxCorners = 500,
                       qualityLevel = 0.3,
                       minDistance = 7,
                       blockSize = 7 )

class App:
    def __init__(self, video_src):
        self.track_len = 10
        self.detect_interval = 5
        self.tracks = []
        self.cam = video.create_capture(video_src)
        self.frame_idx = 0

    def run(self):
        for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            #Read from camera
            img = frame.array
            vis2 = img.copy()
            visEq = img.copy()
            
            #Equalize saturated values of image
            visEq = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            visEq[:,:,2] = cv2.equalizeHist(visEq[:,:,2])

            #Convert to Grayscale
            frame_gray_old = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            
            frame_bgr_oldEq = cv2.cvtColor(visEq, cv2.COLOR_HSV2BGR)
            frame_gray_oldEq = cv2.cvtColor(frame_bgr_oldEq, cv2.COLOR_BGR2GRAY)

            #Equalize Histogram
            frame_gray = cv2.equalizeHist(frame_gray_old)
            frame_grayEq = cv2.equalizeHist(frame_gray_oldEq)

            #frame_gray = frame_gray_old
            vis = img.copy()
            
            if len(self.tracks) > 0:
                img0, img1 = self.prev_gray, frame_gray
                p0 = np.float32([tr[-1] for tr in self.tracks]).reshape(-1, 1, 2)
                p1, st, err = cv2.calcOpticalFlowPyrLK(img0, img1, p0, None, **lk_params)
                p0r, st, err = cv2.calcOpticalFlowPyrLK(img1, img0, p1, None, **lk_params)

                d = abs(p0-p0r).reshape(-1, 2).max(-1)
                good = d < 1
                new_tracks = []
                for tr, (x, y), good_flag in zip(self.tracks, p1.reshape(-1, 2), good):
                    if not good_flag:
                        continue
                    tr.append((x, y))
                    if len(tr) > self.track_len:
                        del tr[0]
                    new_tracks.append(tr)
                    cv2.circle(vis, (x, y), 2, (0, 255, 0), -1)
                self.tracks = new_tracks
                cv2.polylines(vis, [np.int32(tr) for tr in self.tracks], False, (0, 255, 0))
                draw_str(vis, (20, 20), 'track count: %d' % len(self.tracks))

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
            cv2.imshow('lk_track', vis)
            cv2.imshow('Before Equalization', frame_gray_old)
            cv2.imshow('After Equalization',frame_gray)

            cv2.imshow('Saturated to gray', frame_gray_oldEq)
            cv2.imshow('s2g equalized',frame_grayEq)
            
            cv2.imshow('saturated image', visEq)
                
            ch = cv2.waitKey(1)
            rawCapture.truncate(0)
            
            if ch == 27:
                break

def main():
    import sys
    try:
        video_src = sys.argv[1]
    except:
        video_src = 0

    print(__doc__)
    App(video_src).run()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main()
