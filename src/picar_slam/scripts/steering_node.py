#!/usr/bin/env python

# Created by Ethan Snow - 2018
# enivium@gmail.com

#Python libraries
import math
import serial
import os

#ROS imports
import rospy
from geometry_msgs.msg import PoseStamped
from tf.transformations import euler_from_quaternion

#Import Pyplot for plotting trajectory
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

#Define a class for storing the information about the target coordinates
class target(object):
	def __init__(self, x=0.0, y=0.0, finalTargetReached=False):
		self.x = x
		self.y = y
		self.finalTargetReached = finalTargetReached

#Define a class for storing the number of initial scans
class initScanCounter(object):
	def __init__(self, count=0):
		self.count = count

#Initialize arrays for storing trajectory data
trajectoryX = []
trajectoryY = []
yawData = []

#Open the coordinates file
scriptPath = os.path.dirname(__file__)
relCoordFilePath = "Coordinates.txt"
coordFilePath = os.path.join(scriptPath, relCoordFilePath)
coordFile = open(coordFilePath, "r")

#Attach the arduino serial port
port = '/dev/ttyACM0' #May need to be changed, depending on your USB devices
arduino = serial.Serial(port, 9600, timeout=5)

#Callback functions for ROS subscriber
def callback(data):
	#If the navigation is complete, do nothing
	if target.finalTargetReached:
		return

	#Throw away the first 10 scans, bad data
	if initScanCounter.count < 10:
		initScanCounter.count += 1
		return

	#Get pose
	x = data.pose.position.x
	y = data.pose.position.y
	explicit_quat = [data.pose.orientation.x, data.pose.orientation.y, data.pose.orientation.z, data.pose.orientation.w]
	(roll,pitch,yaw) = euler_from_quaternion(explicit_quat)

	#Add coordinates to trajectory arrays
	trajectoryX.append(x)
	trajectoryY.append(y)
	yawData.append(yaw)

	#Calculate distance and angle relative to target
	deltaX = target.x - (x)
	deltaY = target.y - (y)
	distance = math.sqrt(math.pow(deltaX, 2) + math.pow(deltaY, 2))
	targetTheta = math.atan2(deltaY, deltaX)

	#Print out position info
	rospy.loginfo(rospy.get_caller_id() + " Distance: " + str(distance) + " deltaX: " + str(deltaX) + " deltaY: " + str(deltaY) + " x: " + str(x) + " y: " + str(y) + " Angle: " + str(targetTheta) + " Yaw: " + str(yaw))

	#If we're within 20 cm, consider say that we've reached the target coordinates
	if (distance < 0.2):
		rospy.loginfo(rospy.get_caller_id() + " Coordinates reached! (" + str(target.x) + "," + str(target.y) +")")

		#Get the next set of coordinates from the file
		targetCoords = coordFile.readline()
		
		#If there we've reached the last target: remain still, print a done message, and save graphs
		if (targetCoords == ""):
			target.finalTargetReached = True
			arduino.write('4')
			rospy.loginfo(rospy.get_caller_id() + " SLAM navigation complete!")
			plt.plot(trajectoryX, trajectoryY)
			plt.savefig('/opt/ros/kinetic/share/hector_geotiff/maps/trajectory.tif')
			plt.figure()
			plt.plot(yawData)
			plt.savefig('/opt/ros/kinetic/share/hector_geotiff/maps/yaw.tif')
			return
		#Otherwise, input the next set of coordinates to the target object
		else:
			targetCoords.rstrip('\n')
			targetCoordsSplit = targetCoords.split(',')
			target.x = float(targetCoordsSplit[0])
			target.y = float(targetCoordsSplit[1])

	#Send movement commands
		# 1: Go straight forward
		# 2: Go forward while turning left
		# 3: Go forward while turning right
		# 4: Stop
	if (targetTheta - yaw > 0):
		arduino.write('2')
	elif (targetTheta - yaw < -0):
		arduino.write('3')
	else:
		arduino.write('1')

#Shutdown function, tell car to stop and close serial connection
def shutdownHook():
	arduino.write('4')
	arduino.close()

#Function to set up and run the ROS subscriber
def listener():
	rospy.init_node('ydslam', anonymous=True)
	rospy.on_shutdown(shutdownHook)
	rospy.Subscriber("slam_out_pose", PoseStamped, callback)
	rospy.spin()

if __name__ == '__main__':
	target = target()
	initScanCounter = initScanCounter()
	listener()
