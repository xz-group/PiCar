
import cv2
import numpy as np

'''
KEYPOINT FINDERS
Takes in an image and calculates the points that it should track

INPUT:
    vis - Grayscale image on which to apply keypoint detection
    bb - bounding box coordinates. Area of interest in vis
    current - need to find features in larger unknown bb
    desc - used for flann and bruteforce matcher when feature descriptors needed
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
def convertKP(kp,bb):
    for i in range(len(kp)):
        kp[i] = kp[i].pt
    kp = np.array([*kp]).astype(np.float32)
    # print("Length of kp = ", len(kp))
    kp[:,0] += bb[0]
    kp[:,1] += bb[1]
    return kp

def bbCheck(vis,bb,curr):
    if curr is True:
        buffer = 20
        dims = np.shape(vis)
        x1 = max(bb[0]-buffer,0)
        y1 = max(bb[1]-buffer,0)
        x2 = min(bb[2]+buffer,dims[1])
        y2 = min(bb[3]+buffer,dims[0])
        return (x1,y1,x2,y2)
    return bb

def randomSample(vis,bb):
    kp = np.empty((100, 2))
    kp[:, 0] = np.random.randint(bb[0], bb[2] + 1, 100)
    kp[:, 1] = np.random.randint(bb[1], bb[3] + 1, 100)
    kp = kp.astype(np.float32)
    return kp

def fast(vis,bb,current=False,desc=False):
    bb = bbCheck(vis,bb,current)
    fast = cv2.FastFeatureDetector_create()
    kp = fast.detect(vis[bb[1]:bb[3],bb[0]:bb[2]],None)
    if len(kp) > 0:
        return convertKP(kp,bb)

    else:
        return None

def sift(vis,bb,current=False,desc=False):
    bb = bbCheck(vis,bb,current)
    sift = cv2.xfeatures2d.SIFT_create()

    # If feature descriptors needed
    if desc:
        kp,desc = sift.detectAndCompute(vis[bb[1]:bb[3],bb[0]:bb[2]],None)
        if len(kp) > 0:
            return convertKP(kp,bb),desc
            # return kp,desc
        else:
            return None,None
    else:
        kp = sift.detect(vis[bb[1]:bb[3],bb[0]:bb[2]],None)
        if len(kp) > 0:
            return convertKP(kp,bb)
    return None


def surf(vis,bb,current=False,desc=False):
    bb = bbCheck(vis,bb,current)
    surf = cv2.xfeatures2d.SURF_create()
    # print("Number of surf keypoints found = ", len(kp))

    # If feature descriptors needed
    if desc:
        kp,desc = surf.detectAndCompute(vis[bb[1]:bb[3],bb[0]:bb[2]],None)
        if len(kp) > 0:
            return convertKP(kp,bb),desc
            # return kp,desc
        else:
            return None,None
    else:
        kp = surf.detect(vis[bb[1]:bb[3],bb[0]:bb[2]],None)
        if len(kp) > 0:
            return convertKP(kp,bb)
        else:
            return None

def orb(vis,bb,current=False,desc=False):
    bb = bbCheck(vis,bb,current)
    orb = cv2.ORB_create()
    # cv2.imshow("SLICED", vis[bb[1]:bb[3],bb[0]:bb[2]])
    # cv2.waitKey(0)

    # If feature descriptors needed
    if desc:
        kp,desc = orb.detectAndCompute(vis[bb[1]:bb[3],bb[0]:bb[2]],None)
        # print("Number of orb keypoints found = ", len(kp))
        if len(kp) > 0:
            return convertKP(kp,bb),desc
            # return kp,desc
        else:

            return None,None
    else:
        kp = orb.detect(vis[bb[1]:bb[3],bb[0]:bb[2]],None)
        # print("Number of orb keypoints found = ", len(kp))
        if len(kp) > 0:
            return convertKP(kp,bb)
        else:
            return None


def shi_tomasi(vis,bb=None,current=False,desc=False):
    bb = bbCheck(vis,bb,current)
    kp = cv2.goodFeaturesToTrack(vis[bb[1]:bb[3],bb[0]:bb[2]],25,0.01,10)
    kp = kp.reshape(-1, 2)
    kp = kp.astype(np.float32)
    kp[:,0] += bb[0]
    kp[:,1] += bb[1]
    # print("Number of shi-tomasi keypoints found = ", len(kp))
    return kp

if __name__ == "__main__":
    source = cv2.VideoCapture("bouncing.mp4")
    ret, frame = source.read()
    framegray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


    # frame = cv2.imread("../testImg.png")
    # framegray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    box = (183, 0, 275, 77)
    kp1 = randomSample(framegray,box)
    kp3 = fast(framegray,(183, 0, 275, 77))
    # kp3 = sift(framegray,box)
    # kp4 = surf(framegray,[100,100,200,200])
    # kp5 = orb(framegray,[100,100,200,200])
    # kp6 = shi_tomasi(framegray,[100,100,200,200])
    # print(kp)

    # RANDOM SAMPLE
    for point in kp1:
        x,y = point
        img2 = cv2.putText(frame, ".",(x,y), cv2.FONT_HERSHEY_SIMPLEX,2, (0,0,255))

    # FAST DETECTOR
    # for point in kp2:
    #     x,y = point
    #     img2 = cv2.putText(frame, ".",(x,y), cv2.FONT_HERSHEY_SIMPLEX,2, (0,255,0))
    #
    # FAST DETECTOR
    for point in kp3:
        x,y = point
        img2 = cv2.putText(frame, ".",(x,y), cv2.FONT_HERSHEY_SIMPLEX,2, (255,0,0))
    #
    # # FAST DETECTOR
    # for point in kp4:
    #     x,y = point
    #     img2 = cv2.putText(frame, ".",(x,y), cv2.FONT_HERSHEY_SIMPLEX,2, (255,255,0))
    #
    # # FAST DETECTOR
    # for point in kp5:
    #     x,y = point
    #     img2 = cv2.putText(frame, ".",(x,y), cv2.FONT_HERSHEY_SIMPLEX,2, (255,0,255))
    #
    # # FAST DETECTOR
    # for point in kp6:
    #     x,y = point
    #     img2 = cv2.putText(frame, ".",(x,y), cv2.FONT_HERSHEY_SIMPLEX,2, (0,255,255))

    cv2.imwrite('../fast_true.png',img2)
    # cv2.imwrite('../random.png',img3)
