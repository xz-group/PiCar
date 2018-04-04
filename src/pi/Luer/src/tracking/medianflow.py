# -*- coding: utf-8 -*-
""" MedianFlow sandbox

Usage:
  medianflow.py SOURCE TRACKINGMETHOD

Options:
  SOURCE    INT: camera, STR: video file
  TRACKINGMETHOD    Medianflow, KCF
"""
from __future__ import print_function
from __future__ import division
from docopt import docopt
from os.path import abspath, exists
from keypointfinders import draw,randomSample
import numpy as np
import cv2
import time


def draw(vis,box):
    x0, y0, x1, y1 = box
    cv2.rectangle(vis, (x0, y0), (x1, y1), (0, 255, 0), 2)
    return True

class MedianFlowTracker(object):
    def __init__(self):
        self.lk_params = dict(winSize  = (11, 11),
                              maxLevel = 3,
                              criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.1))

        self._atan2 = np.vectorize(np.math.atan2)
        self._n_samples = 10
        self._num_frames = 0
    def track(self, bb, prev, curr):

        fpsTimeStart = time.time()
        # TO MEASURE TIME AS FUNCTION OF DATA POINTS TRACKED
        # if self._num_frames % 15 == 0:
        #     self._n_samples += 1
        self._n_samples = 100
        self._num_frames += 1

        self._fb_max_dist = 1
        self._ds_factor = 0.95
        self._min_n_points = 10

        csvWrite = ""
        vsPoints = ""
        # TIMING 1
        samplingStart = time.time()

        # sample points inside the bounding box
        p0 = self.getPoints(prev[bb[0]:bb[2]+1,bb[1]:bb[3]+1])




        p0 = p0.astype(np.float32)

        mask = np.zeros_like(prev)
        mask[:] = 255

        samplingEnd = time.time()-samplingStart;

        csvWrite += str(samplingEnd) + ","

        # TIMING FEATURE TRACKING AND CHECKING
        checkStart = time.time()

        # forward-backward tracking
        p1, st, err = cv2.calcOpticalFlowPyrLK(prev, curr, p0, None, **self.lk_params)
        vsPoints += str(len(p1)) + ","
        indx = np.where(st == 1)[0]
        p0 = p0[indx, :]
        p1 = p1[indx, :]
        p0r, st, err = cv2.calcOpticalFlowPyrLK(curr, prev, p1, None, **self.lk_params)
        if err is None:
            return None


        # check forward-backward error and min number of points
        fb_dist = np.abs(p0 - p0r).max(axis=1)
        good = fb_dist < self._fb_max_dist

        # keep half of the points
        err = err[good].flatten()
        if len(err) < self._min_n_points:
            return "None",0

        checkEnd = time.time()-checkStart
        csvWrite += str(checkEnd) + ","
        vsPoints += str(checkEnd) + "\n"
        indx = np.argsort(err)
        half_indx = indx[:len(indx) // 2]
        p0 = (p0[good])[half_indx]
        p1 = (p1[good])[half_indx]

        # TIMING HORIZONTAL AND VERTICAL TRANSLATION
        trackEstimateStart = time.time()

        # estimate displacement
        dx = np.median(p1[:, 0] - p0[:, 0])
        dy = np.median(p1[:, 1] - p0[:, 1])

        # all pairs in prev and curr
        i, j = np.triu_indices(len(p0), k=1)
        pdiff0 = p0[i] - p0[j]
        pdiff1 = p1[i] - p1[j]

        # estimate change in scale
        p0_dist = np.sum(pdiff0 ** 2, axis=1)
        p1_dist = np.sum(pdiff1 ** 2, axis=1)
        ds = np.sqrt(np.median(p1_dist / (p0_dist + 2**-23)))
        ds = (1.0 - self._ds_factor) + self._ds_factor * ds;

        trackEstimateEnd = time.time()-trackEstimateStart
        csvWrite += str(trackEstimateEnd) + "\n"

        writeFile = open('timingData.csv', "a")
        writeFile.write(csvWrite)
        writeFile.close()

        # writeFile = open('timingPoints.csv', "a")
        # writeFile.write(vsPoints)
        # writeFile.close()

        # update bounding box
        dx_scale = (ds - 1.0) * 0.5 * (bb[3] - bb[1] + 1)
        dy_scale = (ds - 1.0) * 0.5 * (bb[2] - bb[0] + 1)
        bb_curr = (int(bb[0] + dx - dx_scale + 0.5),
                   int(bb[1] + dy - dy_scale + 0.5),
                   int(bb[2] + dx + dx_scale + 0.5),
                   int(bb[3] + dy + dy_scale + 0.5))

        fpsTimeEnd = time.time()-fpsTimeStart
        fps = 1/fpsTimeEnd

        if bb_curr[0] >= bb_curr[2] or bb_curr[1] >= bb_curr[3]:
            return "None",fps

        bb_curr = (min(max(0, bb_curr[0]), curr.shape[1]),
                   min(max(0, bb_curr[1]), curr.shape[0]),
                   min(max(0, bb_curr[2]), curr.shape[1]),
                   min(max(0, bb_curr[3]), curr.shape[0]))

        return bb_curr,fps


class API(object):
    def __init__(self, win, source, samplingMethod):
        self._device = cv2.VideoCapture(source)
        if isinstance(source, str):
            self.paused = True
        else:
            self.paused = False

        self.win = win
        cv2.namedWindow(self.win, 1)
        # self.rect_selector = RectSelector(self.win, self.on_rect)

        self._bounding_box = None
        self._tracker = MedianFlowTracker()

        if samplingMethod == "random":
            self.getKeyPoints = randomSample
        elif samplingMethod == "fast":
            self.getKeyPoints = fastSample
        elif samplingMethod == "sift":
            self.getKeyPoints = sift
        elif samplingMethod == "surf":
            self.getKeyPoints = surf
        elif samplingMethod == "orb":
            self.getKeyPoints = orb
        elif samplingMethod == "shi-tomasi":
            self.getKeyPoints = shi_tomasi

    def on_rect(self, rect):
        self._bounding_box = rect

'''
KEYPOINT FINDERS
Takes in an image and calculates the points that it should track

INPUT:
    vis - Small grayscale image of larger iamge(bounding box in the larger image)
OUTPUT:
    kp - Keypoints in image
randomSample
    - randomly samples n keypoints in image
fastSample
    - https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_fast/py_fast.html
sift
    - https://docs.opencv.org/3.1.0/da/df5/tutorial_py_sift_intro.html
surf
    - https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_surf_intro/py_surf_intro.html
shi_tomasi:
    - https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_feature2d/py_shi_tomasi/py_shi_tomasi.html
'''
    def randomSample(self,vis):
        kp = np.empty((self._n_samples, 2))
        kp[:, 0] = np.random.randint(bb[0], bb[2] + 1, self._n_samples)
        kp[:, 1] = np.random.randint(bb[1], bb[3] + 1, self._n_samples)
        return kp

    def fastSample(vis):
        # TO-DO

    def sift(vis):
        # TO-DO

    def surf(vis):
        # TO-DO

    def orb(vis):
        # TO-DO

    def shi_tomasi(vis):
        # TO-DO

'''
FEATURE MATCHING
Takes in array of keypoints found via a keypoint detector and performs forward-backward checking
on the kepoints with images prev and next

INPUT:
    p0 - an array of keypoints found in prev
    prev - first image
    next - next image
OUTPUT
    kp - points to track

bruteforce
flann
opticalflow
'''
    def bruteforce(p0,prev,next):
        # TO-DO

    def flann(p0,prev,next):
        # TO-DO

    def opticalflow(p0,prev,next):
        # TO-DO



    def run(self):
        prev, curr = None, None

        ret, frame = self._device.read()
        if not ret:
            raise IOError('can\'t reade frame')

        time.sleep(1)
        a,b,c,d = 0,0,0,0
        while a == 0 and b == 0 and c == 0 and d == 0:
            coord = cv2.selectROI(self.win,frame,False,False)
            print("coord = ", coord)
            a,b,c,d = coord
            c += a
            d += b

        self._bounding_box = (a,b,c,d)
        print("Bounding box = ", self._bounding_box)
        while True:
            ret, grabbed_frame = self._device.read()
            if not ret:
                break

            frame = grabbed_frame.copy()

            prev, curr = curr, cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            if prev is not None and self._bounding_box is not "None":
                bb,fps = self._tracker.track(self._bounding_box, prev, curr)

                if bb is not "None":
                    self._bounding_box = bb
                    cv2.rectangle(frame, self._bounding_box[:2], self._bounding_box[2:], (0, 255, 0), 2)
                    cv2.putText(frame, str(fps), (50, 50),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 2)

                else:
                    cv2.rectangle(frame, self._bounding_box[:2], self._bounding_box[2:], (0, 0, 255), 2)
                    cv2.putText(frame, str(fps), (50, 50),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 2)
            # draw(frame,self._bounding_box)

            cv2.imshow(self.win, frame)

            ch = cv2.waitKey(1)
            if ch == 27 or ch in (ord('q'), ord('Q')):
                break
            elif ch in (ord('p'), ord('P')):
                self.paused = not self.paused

if __name__ == "__main__":
    args = docopt(__doc__)

    try:
        source = int(args['SOURCE'])
        method = args['TRACKINGMETHOD']
    except:
        source = abspath(str(args['SOURCE']))
        if not exists(source):
            raise IOError('file does not exists')

    API(method, source).run()
