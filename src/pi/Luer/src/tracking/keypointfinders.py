def draw(vis,box):
    x0, y0, x1, y1 = box
    cv2.rectangle(vis, (x0, y0), (x1, y1), (0, 255, 0), 2)
    return True



'''
The following methods
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

def fastSample(vis):


def sift(vis):


def surf(vis):


def orb(vis):


def shi_tomasi(vis):
