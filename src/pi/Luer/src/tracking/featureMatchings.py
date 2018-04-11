
import cv2
import numpy as np
import time

'''
Feature Matching
Takes in current frame, previous frame, and keypoints from previous frame and matches the keypoints to current frame

INPUT:
    prev - previous image
    curr - current image
    kp - keypoints in prev
    bb - bounding box in prev
    keypointFinder - keypoint finding method (see keypointFinders.py)
OUTPUT:
    p0 - filtered keypoints in prev
    p1 - Keypoints in curr

opticalflow
    - https://github.com/opencv/opencv/blob/master/samples/python/lk_track.py
flann
    -
bruteforce
    -
'''


def opticalflow(prev,curr,bb,keypointFinder):
    fb_max_dist = 1
    min_n_points = 10

    # RECORD DATA
    csvWrite = ""
    vsPoints = ""

    # TIMING FOR SAMPLING
    samplingStart = time.time()
    p0 = keypointFinder(prev,bb)
    samplingEnd = time.time()-samplingStart;
    # csvWrite += str(samplingEnd) + ","

    if p0 is None:
        return None,None
    lk_params = dict(winSize  = (11, 11),maxLevel = 3,criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.1))

    # TIMING FOR FEATURE MATCHING
    checkStart = time.time()

    p1, st, err = cv2.calcOpticalFlowPyrLK(prev, curr, p0, None, **lk_params)
    indx = np.where(st == 1)[0]
    p0 = p0[indx, :]
    p1 = p1[indx, :]
    p0r, st, err = cv2.calcOpticalFlowPyrLK(curr, prev, p1, None, **lk_params)

    checkEnd = time.time()-checkStart
    # csvWrite += str(checkEnd) + ","
    # vsPoints += str(checkEnd) + "\n"

    # vsPoints += str(len(p1)) + ","

    if err is None:
        return None,None

    # check forward-backward error and min number of points
    fb_dist = np.abs(p0 - p0r).max(axis=1)
    good = fb_dist < fb_max_dist

    # keep half of the points
    err = err[good].flatten()
    if len(err) < min_n_points:
        return None,None

    indx = np.argsort(err)
    half_indx = indx[:len(indx) // 2]
    p0 = (p0[good])[half_indx]
    p1 = (p1[good])[half_indx]
    # print("p0 OF = ", p0)
    return p0,p1

def flann(prev,curr,bb,keypointFinder):
    # FLANN parameters
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks=50)   # or pass empty dictionary

    p0,desc0 = keypointFinder(prev,bb,desc=True)
    p1,desc1 = keypointFinder(curr,bb,current=True,desc=True)
    if p0 is None:
        return None,None
    if len(p0) < 3:
        return None,None
    # print(desc0)
    desc0 = np.float32(desc0)
    # print(desc1)
    desc1 = np.float32(desc1)
    # print(desc1)
    flann = cv2.FlannBasedMatcher(index_params,search_params)

    matches = flann.knnMatch(desc0,desc1,k=2)
    matchesMask = [0 for i in range(len(matches))]

    p0good = []
    p1good = []
    # ratio test as per Lowe's paper
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.75*n.distance:
            matchesMask[i]=1

    # print("MATCHES: ", matches)
    # print("SHAPE OF MATCHES: ", np.shape(matches))
    for i in range(len(p0)):
        if matchesMask[i] == 1:
            p0good.append(p0[matches[i][0].queryIdx])
            p1good.append(p1[matches[i][0].trainIdx])

    draw_params = dict(matchColor = (0,255,0),
                       singlePointColor = (255,0,0),
                       matchesMask = matchesMask,
                       flags = 0)
    # img3 = cv2.drawMatchesKnn(prev[bb[1]:bb[3],bb[0]:bb[2]],p0,curr,p1,matches,None,**draw_params)
    # cv2.imshow("matches",img3)
    # cv2.waitKey(0)
    # print(matchesMask)

    # print(matches)
    p0good = np.array([*p0good]).astype(int)
    p1good = np.array([*p1good]).astype(int)

    # print("RETURNING: ")
    # print(p0good)
    # print("p1")
    # print(p1good)
    if len(p0good) < 3:
        print("[ERROR] Not enough features to track")
        return None,None
    return p0good,p1good

def bruteforce(prev,curr,bb,keypointFinder):

    p0,desc0 = keypointFinder(prev,bb,desc=True)
    p1,desc1 = keypointFinder(curr,bb,current=True,desc=True)
    if p0 is None:
        return None,None
    if len(p0) < 3:
        return None,None

    desc0 = np.float32(desc0)
    desc1 = np.float32(desc1)

    bf = cv2.BFMatcher()

    matches = bf.knnMatch(desc0,desc1,k=2)
    matchesMask = [0 for i in range(len(matches))]

    p0good = []
    p1good = []
    # ratio test as per Lowe's paper
    for i,(m,n) in enumerate(matches):
        if m.distance < 0.7*n.distance:
            matchesMask[i]=1

    # print("MATCHES: ", matches)
    # print("SHAPE OF MATCHES: ", np.shape(matches))
    for i in range(len(p0)):
        if matchesMask[i] == 1:
            p0good.append(p0[matches[i][0].queryIdx])
            p1good.append(p1[matches[i][0].trainIdx])

    draw_params = dict(matchColor = (0,255,0),
                       singlePointColor = (255,0,0),
                       matchesMask = matchesMask,
                       flags = 0)
    # img3 = cv2.drawMatchesKnn(prev[bb[1]:bb[3],bb[0]:bb[2]],p0,curr,p1,matches,None,**draw_params)
    # cv2.imshow("matches",img3)
    # cv2.waitKey(0)
    # print(matchesMask)

    # print(matches)
    p0good = np.array([*p0good]).astype(int)
    p1good = np.array([*p1good]).astype(int)
    if len(p0good) < 3:
        print("[ERROR] Not enough features to track")
        return None,None
    return p0good,p1good
# if __name__ == "__main__":
#     source = cv2.VideoCapture("bouncing.mp4")
#     ret, frame = source.read()
#     framegray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
