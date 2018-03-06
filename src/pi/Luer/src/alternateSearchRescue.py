# USAGE
# python deep_learning_object_detection.py --image images/example_01.jpg \
#	--prototxt MobileNetSSD_deploy.prototxt.txt --model MobileNetSSD_deploy.caffemodel

# import the necessary packages
import numpy as np
import argparse
import cv2
from picamera.array import PiRGBArray
from picamera import PiCamera
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

out = cv2.VideoWriter("../media/bottle2.avi",cv2.VideoWriter_fourcc(*"MJPG"),10,(width,height))

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-c", "--confidence", type=float, default=0.2,
                help="minimum probability to filter weak detections")
ap.add_argument('-l','--list', nargs='+', help='specify items to track. usage: --list bottle dog horse',required=True)
args = vars(ap.parse_args())

itemsToTrack = args["list"]
# initialize the list of class labels MobileNet SSD was trained to
# detect, then generate a set of bounding box colors for each class
CLASSES = ["background", "aeroplane", "bicycle", "bird", "boat",
	"bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
	"dog", "horse", "motorbike", "person", "pottedplant", "sheep",
	"sofa", "train", "tvmonitor"]

for item in itemsToTrack:
    if item not in CLASSES:
        itemsToTrack.remove(item)
        print("[ERROR] Cannot track %s. Removing from list..." % item)

COLORS = np.random.uniform(0, 255, size=(len(CLASSES), 3))

count = 0
while True:
    count = count % len(itemsToTrack)
    itemInterest = itemsToTrack[count]
    count += 1
    for img in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            # Read a single frame
            image = img.array
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            image_gray = clahe.apply(image_gray)
            break

    rawCapture.truncate(0)
    # load our serialized model from disk
    #print("[INFO] loading model...")
    net = cv2.dnn.readNetFromCaffe("../model/MobileNetSSD_deploy.prototxt.txt", "../model/MobileNetSSD_deploy.caffemodel")

    # Construct an input blob for the image
    # by resizing to a fixed 300x300 pixels and then normalizing it
    # (note: normalization is done via the authors of the MobileNet SSD
    # implementation)
    (h, w) = image.shape[:2]
    blob = cv2.dnn.blobFromImage(cv2.resize(image, (300, 300)), 0.007843, (300, 300), 127.5)

    # pass the blob through the network and obtain the detections and
    # predictions
    ssdTime = time.time()
    print("[INFO] computing object detections...")
    net.setInput(blob)
    detections = net.forward()
    #bbox_ = [0,0,0,0]
    x1,y1,x2,y2 = 0,0,0,0
    for i in np.arange(0, detections.shape[2]):
            # extract the confidence (i.e., probability) associated with the
            # prediction
            confidence = detections[0, 0, i, 2]

    	# filter out weak detections by ensuring the `confidence` is
    	# greater than the minimum confidence
            if confidence > args["confidence"]:
                # extract the index of the class label from the `detections`,
                # then compute the (x, y)-coordinates of the bounding box for
                # the object
                idx = int(detections[0, 0, i, 1])
                box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
                (startX, startY, endX, endY) = box.astype("int")
                if CLASSES[idx] == itemInterest:
                #if True:
                    x1 = startX
                    y1 = startY
                    x2 = endX
                    y2 = endY
                    print("[INFO] Locking on to %s..." % itemInterest)

                    # display the prediction
                    label = "{}: {:.2f}%".format(CLASSES[idx], confidence * 100)
                    print("[INFO] {}".format(label))
                    cv2.rectangle(image, (startX, startY), (endX, endY), COLORS[idx], 2)
                    y = startY - 15 if startY - 15 > 15 else startY + 15
                    cv2.putText(image, label, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.5, COLORS[idx], 2)

    # show the output image
    ssdTime = time.time()-ssdTime
    print("[RESULTS] SSD took %f seconds..." % ssdTime)
    cv2.imwrite("../media/lockedOn.jpg",image)
    #cv2.imshow("Output", image)
    #cv2.waitKey(0)

    tracker = cv2.TrackerMedianFlow_create()
    bbox = (x1,y1,x2-x1,y2-y1)
    #bbox = (y1,x1,y2-y1,x2-x1)

    print("[INFO] Passing coordinates to tracking algorithm: ", bbox)
    ok = tracker.init(image_gray, bbox)

    timeInFailure = 0
    failureStartTime = 0
    failureInterval = 0.5           #How much time I want to be in a failure state until I recheck for item

    for img in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
            frame = img.array
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            frame_gray = clahe.apply(frame_gray)

            # Start timer
            timer = cv2.getTickCount()

            # Update tracker
            ok, bbox = tracker.update(frame_gray)

            # Calculate Frames per second (FPS)
            fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
            #print("BBOX: ", bbox)
            # Draw bounding box
            p1 = (int(x1), int(y1))
            p2 = (int(x2), int(y2))
            cv2.rectangle(frame, p1, p2, (255,255,255), 2, 1)

            if ok:
                # Tracking success
                failureStartTime = 0
                p1 = (int(bbox[0]), int(bbox[1]))
                p2 = (int(bbox[0] + bbox[2]), int(bbox[1]+bbox[3]))
                cv2.rectangle(frame, p1, p2, (255,0,0), 2, 1)
                cv2.line(frame,(int(x1),int(y1)),(int(bbox[0]),int(bbox[1])),(0,0,255),3)
                cv2.line(frame,(int(x1),int(y2)),(int(bbox[0]),int(bbox[1]+bbox[3])),(0,0,255),3)
                cv2.line(frame,(int(x2),int(y1)),(int(bbox[0]+bbox[2]),int(bbox[1])),(0,0,255),3)
                cv2.line(frame,(int(x2),int(y2)),(int(bbox[0]+bbox[2]),int(bbox[1]+bbox[3])),(0,0,255),3)
            else :
                # Tracking failure
                if failureStartTime == 0:
                    failureStartTime = time.time()
                else:
                    timeInFailure = time.time()-failureStartTime
                    if timeInFailure > failureInterval:
                        rawCapture.truncate(0)
                        print("[ERROR] Failure detected. Running SSD again...")
                        break

                cv2.putText(frame, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)

            # Display tracker type on frame
            cv2.putText(frame, "MEDIANFLOW Tracker", (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);

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
