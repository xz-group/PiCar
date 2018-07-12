import os
import re
import csv

dataTimes = []
dataList = []
photoTimes = []
#path where you save data and photo
dataCSVPath = 'data_photo/Lidar_IMU_Data.csv'
AllPhotoPath = "data_photo/camera"

#some constant based on data format
#The Length* will be updated in readData() based on data format
LengthWithoutTime = 11
LengthWithTime = LengthWithoutTime + 1
dataTimePos = 0

#match a photo to a set of data based on best-fit on time
def findBestFit(imageTime,dataList,startIndex):
    global LengthWithoutTime
    global dataTimePos
    difference = abs(imageTime - (float)(dataList[startIndex][dataTimePos]))
    currentIndex = startIndex

    #go through datalist, extract time, and compare the difference
    #we want to find the closest one for this imageTime
    for index in range(startIndex,len(dataList)):
        dataTime = (float)(dataList[index][dataTimePos])
        newDiffer = abs(imageTime - dataTime)
        if newDiffer < difference:
            difference = newDiffer
            currentIndex = index

    #push file name to dataList
    imageName = str(imageTime) + ".jpg"
    if len(dataList[currentIndex]) == LengthWithoutTime:
        dataList[currentIndex].append(imageName)


#if a photo is not matched, we try to find the previous matched one
def findPrevImage(dataList,index):
    global LengthWithTime
    aIndex = index
    FindImage = 1
    while len(dataList[index]) != LengthWithTime:
        index = index - 1
        if index < 0:
            FindImage = 0
            break;

    if FindImage:
        ImageName = dataList[index][LengthWithTime - 1]
        #add it to orignial element
        dataList[aIndex].append(ImageName)
        return 1
    elif not FindImage:
        return 0


#we try to find the next matched photo
def findNextImage(dataList,index):
    global LengthWithTime
    aIndex = index
    FindImage = 1
    while len(dataList[index]) != LengthWithTime:
        index = index + 1
        if index > len(dataList) - 1:
            FindImage = 0
            break;

    if FindImage:
        ImageName = dataList[index][LengthWithTime - 1]
        #add it to orignial element
        dataList[aIndex].append(ImageName)
        return 1
    elif not FindImage:
        return 0


def read_photo_times():
    global AllPhotoPath
    global photoTimes
    fileNames = os.listdir(AllPhotoPath)

    imageTime = re.compile(r"^.*(?=(\.jpg))")

    #extract photo time from its name,
    #which is in the format: time.jpg
    #and save it as a float for future comparison
    for file in fileNames:
        theTime = imageTime.match(file)
        photoTimes.append((float)(theTime.group(0)))

    photoTimes = sorted(photoTimes)


def readData():
    global dataTimes
    global dataList
    global dataTimePos
    global LengthWithoutTime
    global LengthWithTime
    #read all data, which in the format [time,lidar,imu]
    with open(dataCSVPath,newline = '') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        updateLength = 0
        for row in spamreader:
            if not updateLength:
                LengthWithoutTime = len(row)
                LengthWithTime = LengthWithoutTime + 1
                updateLength = 1
            dataTimes.append(row[dataTimePos])
            dataList.append(row)


def sync():
    global photoTimes
    global dataList
    #sychrnoize image and data based on time
    for index in range(len(photoTimes)):
        findBestFit(photoTimes[index],dataList,index)


    #now give un-matched data a time
    for index in range(len(dataList)):
        if len(dataList[index]) == LengthWithoutTime:
            result = findPrevImage(dataList,index)
            if result == 0:
                findNextImage(dataList,index)


def write_sync_data():
    global dataList
    print("start writing csv file")
    with open('sync_data_712.csv',"a",newline = '') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        for data in dataList:
            spamwriter.writerow(data)


if __name__ == '__main__':
   try:
       read_photo_times()
       readData()
       sync()
       write_sync_data()
   except Exception as e:
      print("error message: " + str(e))
      print("end")
