import numpy as np
import cv2
from matplotlib import pyplot as plt
import time

startTime = time.time()

imgL = cv2.imread('cactus0.png',0)
imgR = cv2.imread('cactus1.png',0)

stereo = cv2.StereoBM_create(numDisparities=16, blockSize=15)
disparity = stereo.compute(imgL,imgR)
finishTime = startTime - time.time()

plt.imshow(disparity,'gray')
plt.show()
