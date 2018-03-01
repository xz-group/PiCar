import cv2
import sys
import time
from picamera.array import PiRGBArray
from picamera import PiCamera
import sys


if len(sys.argv) < 2:
    print("usage: python3 tracking.py <1,2,3,4>")
    sys.exit()
else:
    clArg = int(sys.argv[1])
width = 640
height = 480

# initialize the camera and grab a reference to the raw camera capture
camera = PiCamera()
camera.resolution = (width, height)
camera.framerate = 25
camera.shutter_speed = 5000
rawCapture = PiRGBArray(camera, size=(width, height))
time.sleep(1)

out = cv2.VideoWriter("kcf.avi",cv2.VideoWriter_fourcc(*"MJPG"),10,(width,height))
print("width: ", width)
print("Height: ",height)
(major_ver, minor_ver, subminor_ver) = (cv2.__version__).split('.')

if __name__ == '__main__' :

    # Set up tracker.
    # Instead of MIL, you can also use

    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW']
    tracker_type = tracker_types[clArg]

    if int(minor_ver) < 3:
        tracker = cv2.Tracker_create(tracker_type)
    else:
        if tracker_type == 'BOOSTING':
            tracker = cv2.TrackerBoosting_create()
        if tracker_type == 'MIL':
            tracker = cv2.TrackerMIL_create()
        if tracker_type == 'KCF':
            tracker = cv2.TrackerKCF_create()
        if tracker_type == 'TLD':
            tracker = cv2.TrackerTLD_create()
        if tracker_type == 'MEDIANFLOW':
            tracker = cv2.TrackerMedianFlow_create()

    # Read video
    #video = cv2.VideoCapture("bouncing.mp4")

    # Exit if video not opened.
  #  if not video.isOpened():
  #      print ("Could not open video")
  #      sys.exit()

    # Read first frame.
   # ok, frame = video.read()
   # if not ok:
   #     print ('Cannot read video file')
   #     sys.exit()
    rawCapture.truncate(0)

    for img in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        # Read a new frame
        frame = img.array
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        frame = clahe.apply(frame_gray)
        break
    
    # Define an initial bounding box
    bbox = (287, 23, 86, 320)

    # Uncomment the line below to select a different bounding box
    bbox = cv2.selectROI(frame, False)
    print("BOUNDING BOX: ",bbox)
    # Initialize tracker with first frame and bounding box
    ok = tracker.init(frame, bbox)
    
    rawCapture.truncate(0)
    for img in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):

        # Read a new frame
        frame = img.array

        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        frame_gray = clahe.apply(frame_gray)
        
        # Start timer
        timer = cv2.getTickCount()

        # Update tracker
        ok, bbox = tracker.update(frame_gray)
        #print("BOUNDING BOX: ",bbox)
        # Calculate Frames per second (FPS)
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);

        # Draw bounding box
        if ok:
            # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
        else :
            # Tracking failure
            cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

        # Display tracker type on frame
        cv2.putText(frame, tracker_type + " Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);

        # Display FPS on frame
        cv2.putText(frame, "FPS : " + str(int(fps)), (100,50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50), 2);

        #print("frame dimensions: ", frame.shape)
        
        # Display result
        cv2.imshow("Tracking", frame)
        out.write(frame)
        rawCapture.truncate(0)

        
        # Exit if ESC pressed
        k = cv2.waitKey(1) & 0xff
        if k == 27 :
            out.release()
            break
