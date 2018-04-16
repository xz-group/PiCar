import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
from math import sqrt

import csv

def getDist(pt1,pt2):
    x1,y1 = pt1
    x2,y2 = pt2
    return sqrt((x2-x1)*(x2-x1) + (y2-y1)*(y2-y1))

frameNumber = 1
frames = []
true = []
calculated = []

trueFile = "trueBottleData.csv"
calculatedDataFile = "foundMid.csv"

with open(trueFile,'r') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for x,y in readCSV:
        x = int(x)
        y = int(y)
        true.append([x,y])

with open(calculatedDataFile,'r') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for x,y in readCSV:
        x = float(x)
        y = float(y)
        calculated.append([x,y])

true = true[2:]
print(len(calculated))
print(len(true))
print(len(calculated))

dist = []
y_actual = [0 for i in range(len(true))]
# Calculate Euclidian Distance between points
for i in range(len(true)):
    dist.append(getDist(true[i],calculated[i]))
    # print(y_predicted)
    # y_actual = 0 # Distance should be 0

rms = (sqrt(mean_squared_error(y_actual, dist)))
print("Root mean square = ", rms)

plt.scatter(range(len(true)), dist, s=10, c='b', marker="o", label='sampling')
plt.xlabel("Frame Number")
plt.ylabel("Pixel distance error")
plt.title("Distance from calculated to true value")
plt.show()
