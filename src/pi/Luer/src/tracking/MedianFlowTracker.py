import cv2
import math
import numpy as np
from keypointFinders import randomSample,fast,sift,surf,orb,shi_tomasi
from featureMatchings import opticalflow,flann,bruteforce
import time

class MedianFlowTracker(object):
    def __init__(self,samplingMethod,featureMatching):


        self._atan2 = np.vectorize(np.math.atan2)
        self._n_samples = 10
        self._num_frames = 0
        self.sample = samplingMethod
        self.match = featureMatching

        if samplingMethod == "random":
            self.getKeyPoints = randomSample
            print("[INFO] Using random sampling")
        elif samplingMethod == "fast":
            self.getKeyPoints = fast
            print("[INFO] Using fast for sampling")
        elif samplingMethod == "sift":
            self.getKeyPoints = sift
            print("[INFO] Using SIFT for sampling")
        elif samplingMethod == "surf":
            self.getKeyPoints = surf
            print("[INFO] Using SURF for sampling")
        elif samplingMethod == "orb":
            self.getKeyPoints = orb
            print("[INFO] Using ORB for sampling")
        elif samplingMethod == "shi-tomasi":
            self.getKeyPoints = shi_tomasi
            print("[INFO] Using Shi-Tomasi for sampling")

        if featureMatching == "opticalflow":
            self.matchFeatures = opticalflow
            print("[INFO] Using optical flow as feature matcher")
        elif featureMatching == "bruteforce":
            self.matchFeatures = bruteforce
            print("[INFO] Using bruteforce as feature matcher")
        elif featureMatching == "flann":
            self.matchFeatures = flann
            print("[INFO] Using FLANN as feature matcher")



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
        # RECORD DATA
        csvWrite = ""
        vsPoints = ""
        p0,p1 = self.matchFeatures(prev,curr,bb,self.getKeyPoints)

        if p0 is None or p1 is None:
            return "None",0
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
