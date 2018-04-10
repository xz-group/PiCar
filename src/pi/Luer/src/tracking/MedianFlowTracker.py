import cv2
import math
import numpy as np
from keypointFinders import randomSample,fast,sift,surf,orb,shi_tomasi
import time

class MedianFlowTracker(object):
    def __init__(self,samplingMethod):
        self.lk_params = dict(winSize  = (11, 11),
                              maxLevel = 3,
                              criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.1))

        self._atan2 = np.vectorize(np.math.atan2)
        self._n_samples = 10
        self._num_frames = 0

        if samplingMethod == "random":
            self.getKeyPoints = randomSample
        elif samplingMethod == "fast":
            self.getKeyPoints = fast
        elif samplingMethod == "sift":
            self.getKeyPoints = sift
        elif samplingMethod == "surf":
            self.getKeyPoints = surf
        elif samplingMethod == "orb":
            self.getKeyPoints = orb
        elif samplingMethod == "shi-tomasi":
            self.getKeyPoints = shi_tomasi

        # if featureMatching == "bruteforce":
        #     self.matchFeatures = bruteforece
        # elif featureMatching == "flann":
        #     self.matchFeatures = flann
        # elif featureMatching == "opticalflow":
        #     self.matchFeatures = opticalflow


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
    # def bruteforce(self,p0,prev,next):
    #     # TO-DO
    #
    # def flann(self,p0,prev,next):
    #     # TO-DO
    #
    # def opticalflow(self,p0,prev,next):
        # TO-DO


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
        p0 = self.getKeyPoints(prev,bb)

        #TODO
        # Check for empty p0 list

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
            return "None",0


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
