import matplotlib.pyplot as plt
import csv

frameNumber = 1
frames = []
numPoints = []
checking = []
tracking = []

with open('timingPoints.csv','r') as csvfile:
    readCSV = csv.reader(csvfile, delimiter=',')
    for row in readCSV:
        # print(row[0],row[1],row[2])
        # frames.append(frameNumber)
        # frameNumber += 1
        numPoints.append(float(row[0]))
        checking.append(float(row[1]))
        # tracking.append(float(row[2]))

# fig = plt.figure()
# ax1 = fig.add_subplot(111)

# plt.scatter(frames, sampling, s=10, c='b', marker="o", label='sampling')
plt.scatter(numPoints, checking, s=10, c='r', marker="o", label='checking')
# plt.scatter(frames, tracking, s=10, c='g', marker="o", label='tracking')
plt.xlabel("Frame")
plt.ylabel("Time")
plt.title("Checking time vs points")
plt.legend(loc='upper left');
plt.show()
