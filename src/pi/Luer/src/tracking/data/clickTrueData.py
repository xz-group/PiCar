import cv2
import numpy as np



class CoordinateStore:
    def __init__(self):
        self.points = []
        self.img = None
        self.windowName = "Simulated Tracker"
        self.read = True

    def select_point(self,event,x,y,flags,param):
            # print("Selecting point")
            if event == cv2.EVENT_LBUTTONDOWN:
            # if event == cv2.EVENT_MOUSEMOVE:
                print("Adding frame")
                # self.img = np.zeros((512,512,3), np.uint8)
                cv2.rectangle(self.img, (x, y), (x+20, y+20), (255,0,0), 2)
                self.read = True
                self.points.append((x,y))
                # out.write(self.img)

fourcc = cv2.VideoWriter_fourcc('M','J','P','G')
out = cv2.VideoWriter("../simulatedtracker.avi",fourcc,10,(512,512))

#instantiate class
coordinateStore1 = CoordinateStore()


# Create a black image, a window and bind the function to window
cv2.namedWindow(coordinateStore1.windowName)
cv2.setMouseCallback(coordinateStore1.windowName,coordinateStore1.select_point)
source = cv2.VideoCapture("../bottle.mp4")

while True:
    # img = np.zeros((512,512,3), np.uint8)
    if coordinateStore1.read:
        coordinateStore1.read = False
        ret, frame = source.read()
        if not ret:
            break
        coordinateStore1.img = frame

    cv2.imshow(coordinateStore1.windowName,coordinateStore1.img)
    k = cv2.waitKey(20) & 0xFF
    if k == 27:
        out.release()
        break
cv2.destroyAllWindows()


# print ("Selected Coordinates: ", coordinateStore1.points)

#Save to CSV
trueData = ""

for x,y in coordinateStore1.points:
    trueData += str(x) + ", " + str(y) + "\n"

# print(trueData)
# Write trueData to csv
writeFile = open('trueBottleData.csv', "w")
writeFile.write(trueData)
writeFile.close()
