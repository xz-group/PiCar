
import cv2
import numpy as np

'''
KEYPOINT FINDERS
Takes in an image and calculates the points that it should track

INPUT:
    vis - Grayscale image on which to apply keypoint detection
    bb - bounding box coordinates. Area of interest in vis
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
def randomSample(vis,bb):

    kp = np.empty((100, 2))
    kp[:, 0] = np.random.randint(bb[0], bb[2] + 1, 100)
    kp[:, 1] = np.random.randint(bb[1], bb[3] + 1, 100)
    kp = kp.astype(np.float32)
    return kp

def fast(vis,bb):
    fast = cv2.FastFeatureDetector_create()
    # print (bb[0], ":",bb[2],bb[2], ":",bb[3])
    # img = vis[bb[1]:bb[3],bb[0]:bb[2]]
    # cv2.imshow("VIS EHRE",img)
    # cv2.waitKey(0)
    kp = fast.detect(vis[bb[1]:bb[3],bb[0]:bb[2]],None)
    print("Number of fast keypoints found = ", len(kp))
    # cv2.rectangle(vis, bb[:2], bb[2:], (0, 255, 0), 2)
    if len(kp) > 0:
        for i in range(len(kp)):
            kp[i] = kp[i].pt
        kp = np.array([*kp]).astype(np.float32)
        print("Length of kp = ", len(kp))
        kp[:,0] += bb[0]
        kp[:,1] += bb[1]
        return kp
    else:
        return None

def sift(vis,bb):
    sift = cv2.xfeatures2d.SIFT_create()
    kp = sift.detect(vis[bb[1]:bb[3],bb[0]:bb[2]],None)
    print("Number of sift keypoints found = ", len(kp))
    for i in range(len(kp)):
        kp[i] = kp[i].pt
    kp = np.array([*kp]).astype(np.float32)
    kp[:,0] += bb[0]
    kp[:,1] += bb[1]
    return kp

def surf(vis,bb):
    surf = cv2.xfeatures2d.SURF_create()
    kp = surf.detect(vis[bb[1]:bb[3],bb[0]:bb[2]],None)
    print("Number of surf keypoints found = ", len(kp))
    for i in range(len(kp)):
        kp[i] = kp[i].pt
    kp = np.array([*kp]).astype(np.float32)
    kp[:,0] += bb[0]
    kp[:,1] += bb[1]
    return kp

def orb(vis,bb):
    orb = cv2.ORB_create()
    kp = orb.detect(vis[bb[1]:bb[3],bb[0]:bb[2]],None)
    print("Number of orb keypoints found = ", len(kp))
    for i in range(len(kp)):
        kp[i] = kp[i].pt
    kp = np.array([*kp]).astype(np.float32)
    kp[:,0] += bb[0]
    kp[:,1] += bb[1]
    return kp

def shi_tomasi(vis,bb):
    kp = cv2.goodFeaturesToTrack(vis[bb[1]:bb[3],bb[0]:bb[2]],25,0.01,10)
    kp = kp.reshape(-1, 2)
    kp = kp.astype(np.float32)
    kp[:,0] += bb[0]
    kp[:,1] += bb[1]
    print("Number of shi-tomasi keypoints found = ", len(kp))
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
