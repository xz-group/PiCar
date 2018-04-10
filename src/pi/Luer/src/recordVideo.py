from picamera.array import PiRGBArray
from picamera import PiCamera
import cv2
import time


width = 640
height = 480
# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (width, height)
camera.framerate = 25
camera.shutter_speed = 5000
rawCapture = PiRGBArray(camera, size=(width, height))
time.sleep(1)

out = cv2.VideoWriter("trackingTester.avi",cv2.VideoWriter_fourcc(*"MJPG"),10,(width,height))
frameCount = 0
numFrames = 300

for img in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    if frameCount = 0:
        time.sleep(1)
    else:
        if frameCount > numFrames:
            break
        frame = img.array
        frameCount += 1
        out.write(frame)
        rawCapture.truncate(0)
