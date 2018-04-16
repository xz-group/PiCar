# -*- coding: utf-8 -*-
""" MedianFlow sandbox

Usage:
  medianflow.py SOURCE KEYPOINTFINDER

Options:
  SOURCE    INT: camera, STR: video file
  KEYPOINTFINDER    STR: random, fast, sift, surf, orb, shi_tomasi
"""
  # FEATUREMATCHING   bruteforce,flann,opticalflow

from __future__ import print_function
from __future__ import division
from os.path import exists
import argparse
import numpy as np
import cv2
import time
from MedianFlowTracker import MedianFlowTracker
from ReportGenerator import ReportGenerator

def draw(vis,box):
    x0, y0, x1, y1 = box
    cv2.rectangle(vis, (x0, y0), (x1, y1), (0, 255, 0), 2)
    return True


class TrackingManager(object):
    def __init__(self, win, source, featurematcher):
        # VIDEO SOURCE
        self._device = cv2.VideoCapture(source)


        # WINDOW NAME
        self.win = win
        cv2.namedWindow(self.win, 1)
        self._bounding_box = None

        # CONSTRUCT MEDIANFLOWTRACKER
        self._tracker = MedianFlowTracker(win, featurematcher)

    def run(self):
        prev, curr = None, None
        time.sleep(1)

        ret, frame = self._device.read()
        if not ret:
            raise IOError('can\'t reade frame')

        a,b,c,d = 0,0,0,0

        # FIND INITIAL BOUNDING BOX
        # while a == 0 and b == 0 and c == 0 and d == 0:
        #     coord = cv2.selectROI(self.win,frame,False,False)
        #     a,b,c,d = coord
        #     c += a
        #     d += b

        self._bounding_box = (a,b,c,d)

        #bouncing red ball
        # self._bounding_box = (183, 0, 275, 77)

        #basketball
        self._bounding_box = (195, 50, 280, 130)

        #Bottle
        self._bounding_box = (460,260,590,600)

        print("[INFO] Bounding box = ", self._bounding_box)

        nFrames = 0
        while True:
            ret, grabbed_frame = self._device.read()
            if not ret:
                break

            frame = grabbed_frame.copy()

            prev, curr = curr, cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if prev is not None and self._bounding_box is not "None":
                # Run Medianflow tracking
                bb,fps = self._tracker.track(self._bounding_box, prev, curr)

                # If bounding box is found, update, draw it
                if bb is not "None":
                    self._bounding_box = bb
                    cv2.rectangle(frame, self._bounding_box[:2], self._bounding_box[2:], (0, 255, 0), 2)
                    cv2.putText(frame, str(fps), (50, 50),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

                # Bounding box not found
                # Draw old coordinates in red
                else:
                    cv2.rectangle(frame, self._bounding_box[:2], self._bounding_box[2:], (0, 0, 255), 2)
                    cv2.putText(frame, str(fps), (50, 50),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
            # draw(frame,self._bounding_box)
            nFrames += 1
            cv2.imshow(self.win, frame)

            ch = cv2.waitKey(1)
            if ch == 27 or ch in (ord('q'), ord('Q')):
                break

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-e","--error", action="store_true", help="Use this flag to calculate error and show plots")
    ap.add_argument("-s", "--source", required=True, help="Enter the path to your video or enter 0 to use your webcam.")
    ap.add_argument("-k", "--keypoint", required=True, help="Enter the method of keypoint detection. Options are random, fast, sift, surf, orb, shi-tomasi.")
    ap.add_argument("-m", "--matching", required=True, help="Enter the method of feature matching. Options are bruteforce, flann, opticalflow.")
    args = vars(ap.parse_args())
    source = args["source"]
    keypointmethod = args["keypoint"]
    featurematcher = args["matching"]
    errorCalculate = args["error"]
    if featurematcher == "flann" or featurematcher == "bruteforce":
        if keypointmethod == "random" or keypointmethod == "fast" or keypointmethod == "shi-tomasi":
            print("[USAGE] Cannot use", keypointmethod, "and", featurematcher, "together")
        else:
            # START TRACKER
            TrackingManager(keypointmethod, source,featurematcher).run()
            if errorCalculate:
                print("calling generator")
                generator = ReportGenerator(source,"data/trueBottleData.csv","data/test.csv","TIMINGPATH",keypointmethod,featurematcher).generateReport()
    else:
        # START TRACKER
        TrackingManager(keypointmethod, source,featurematcher).run()
        if errorCalculate:
            print("calling generator")
            generator = ReportGenerator(source,"data/trueBottleData.csv","data/test.csv","timingData.csv",keypointmethod,featurematcher).calculateErrors()
