Software
========

The software section will document all the heavy duty programming
programming aspects of the project. There may be some overlap with
the Electronics section.

Socket File Transfer
--------------------

Basic File Transfer
^^^^^^^^^^^^^^^^^^^

Server side
###########

.. code-block:: python
  :linenos:

  import socket                   # Import socket module

  port = 60000                    # Reserve a port for your service.
  s = socket.socket()             # Create a socket object
  host = socket.gethostbyaddr("your IP static IP if under same WIFI")[0]     # Get local machine name
  s.bind((host, port))            # Bind to the port
  s.listen(5)                     # Now wait for client connection.

  print ('Server listening....'.encode('ascii'))

  while True:
      conn, addr = s.accept()     # Establish connection with client.
      print ('Got connection from', addr)
      data = conn.recv(1024)
      print('Server received', repr(data))

      filename='your file name'
      f = open(filename,'rb')
      l = f.read(1024)
      while (l):
         conn.send(l)
         print('Sent ',repr(l))
         l = f.read(1024)          #alter this to control data sending rate
      f.close()

      print('Done sending')
      conn.close()

Client side
###########

.. code-block:: python
  :linenos:

  import socket                   # Import socket module

  s = socket.socket()             # Create a socket object
  host = 'your ip address'     # Get local machine name
  port = 60000                    # Reserve a port for your service.

  s.connect((host, port))
  s.send("Hello server!".encode('ascii'))

  with open('received_file', 'wb') as f:
      print ('file opened')
      while True:
          print('receiving data...')
          data = s.recv(1024)          #must be identical to the data rate at server side
          print('data=%s', (data))
          if not data:
              break
          # write data to a file
          f.write(data)

  f.close()
  print('Successfully get the file')
  s.close()
  print('connection closed')

Advanced Folder Transfer
^^^^^^^^^^^^^^^^^^^^^^^^

*Creator: Jerry Kong*

To meet our need of a neat and organized data structure, this script is created.
It has the capability to transfer the entire folder to another remote desktop, no matter it is on a Windows System or Unix system.
The script rests in ``PiCar/src/Logging``
To use the script, first setup the ip addresses like in the basic version, change the root variable to the root folder name.
Place the script at the same level as the root folder. Start the server script and then start the client script. The folder would then be transferred.
A better protocol could be implemented, since the protocol now being used is not really efficient though fulfill the need of our experiment for now.


WIFI Router setting
^^^^^^^^^^^^^^^^^^^

*Creator: Jerry Kong*

*This section is dedicated to users who are not familiar with WIFI network setting, TCP protocol and wireless connection*

To establish communication between two machine we need to know their address. Moreover, to provide a consistent and save network experience, a machine would have many ports to receive connections with different forms,
thus we also need to agree on the port that two machine establish the connection on. However, depending on different internet environment and different ways of connection (wifi or ethernet), the IP address would also vary.
Read through this section, you would get a sense of how this astonishingly complicated system works and hopefully learn how to cope with "Connection fails" error when you are using the script I wrote in the repo or any kind of
Internet application.

IP
###

IP's full name is Internet Protocol. It's a scheme that specifies how computers find each other in the pool of Internet. The rules behind it is complicated, but the most important thing is that it is a identification
for modern computer wired to Internet and is universally used as the synonym of IP address.

IPv4? IPv6?
###########

As a protocal, IP would have different versions, the latest version is version 6 and thus called IPv6. While IPv6 is stronger and has a larger pool of Internet, the older version IPv4 is not obsoleted.
The logic behind the two protocals are the same, hence we would now stick with IPv4, since it has a more concise format. (XXX.XX.XX.XXX)

WIFI vs ethernet
################

You must be familiar with this topic. WIFI is more convenient while wired connection (ethernet) offer steadiness and low latency. However, it is important to note that a computer connected to wifi does not have an IP, or at least, an acknowledged IP.
Wifi or the router serves as a broadcaster and spread the connection from the ethernet to multiple machines, but they have the same IP address. The router can identify each machine by the IP address it assigns to the machine, but the machine can't use
that address as the identification on the internet. Conclusively, machines under the same WIFI build up a small Internet where these machines can identify each other by the address they are assigned, but once outside WIFI network they are no longer acknowledged.

See
`Setup static IP address for RaspberryPi <https://www.raspberrypi.org/forums/viewtopic.php?t=191140>`_
, so a machine would be assigned the same IP address when connected to the WIFI.

TCP
###

TCP, transmission Control Protocol, is a higher level protocol that enables data sending via the connection established by IP. Socket, a method based on TCP is prevailing on data transfer.

Port and Port forwarding
########################

With the knowledge about address in mind we could start the connection once we have the right port. It is easy to do so if both machines are on Internet or under the same WIFI, since they can identify with each other. Just pick up an empty port and they are good to go.
However, we do want to establish connection between two machines even if one is on WIFI and the other is on Internet. To do so, these smart people invented port forwarding. With port forwarding, a client can find the address of the router and use the port that is forwarded to connect with the machine.

For example, the address of the router is 172.10.10.111, and a machine under the WIFI is assigned static IP 192.168.1.188. The routher and the machine agree on that the connection to the port 30000 of the routher would be forwarded to the port 6000 of the machine and vice versa.
Thus a laptop could setup a connection with 172.10.10.111 on port 30000 to connect the port 6000 on machine with static IP 192.168.1.188.

See
`How to setup port forwarding <https://www.howtogeek.com/66214/how-to-forward-ports-on-your-router/>`_



Sensors(Lidar,IMU) reading and writing
--------------------------------------

Setup
^^^^^
Make sure you have alreadly connect TFmini Lidar and IMU as
`TFmini Lidar <http://picar.readthedocs.io/en/latest/chapters/usage/electronics.html#pi-and-tfmini-lidar-communication>`_
, `IMU by LSM9DS1 <http://picar.readthedocs.io/en/latest/chapters/usage/electronics.html#pi-and-imu-communication>`_ did.
and download corresponding libraris.

Code
^^^^

Under Directory ``PiCar/src/pi/IMU_Lidar``

Steps
^^^^^
1.Download the repository and connect sensors correctly

2.run the python script Lidar_IMU_read_optimize.py

3.After the program ends, you should see two csv files under the same directory.One records
the time between two consecutive reads, and the other one contains data from sensors in the format:
timestamp, distance, accelaration in x,y,z, angular velocity in x,y,z



Camera(picture) data by rapid capturing
---------------------------------------
Connection
^^^^^^^^^^
Connect the camera correctly

Code
^^^^

.. code-block:: python
  :linenos:

  import time
  import picamera
  import datetime

  frames = 20

  def filenames():
      frame = 0
      while frame < frames:
          current = datetime.datetime.now()
          yield '%s.jpg' % current
          frame += 1

  with picamera.PiCamera(resolution=(480,480), framerate=100) as camera:
      camera.start_preview()
      # Give the camera some warm-up time
      time.sleep(2)
      start = time.time()
      camera.capture_sequence(filenames(), use_video_port=True)
      finish = time.time()
  print('Captured %d frames at %.2ffps, in %f seconds' % (
      frames,
      frames / (finish - start), (finish - start)))

This will give you real time and fps.

Resources
^^^^^^^^^
`rapid capture and processing <https://picamera.readthedocs.io/en/release-1.13/recipes2.html#rapid-capture-and-processing>`_



Sensors/Camera concurrent reading by Timer(Version1)
----------------------------------------------------
Connection
^^^^^^^^^^
Connect IMU,TFmini Lidar, and Pi Camera correctly as previous tutorial did.

Code
^^^^
The code for this part is under directory ``PiCar/src/pi/pythonTimer``

I put most of the explanation in the code.

Resources
^^^^^^^^^
  * `Python multiprocessing--Process-based Parallelism <https://docs.python.org/3.4/library/multiprocessing.html?highlight=process>`_

  * `Python threading timer object <https://docs.python.org/3/library/threading.html#timer-objects>`_

Data Logging
------------

Version Alpha (Camera data, IMU data, LiDar Data)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Creator : Jerry Kong*

(Be sure to correctly wire all electronics, the wiring method could be found in the corresponding section of this doc site.)

The code could be found in PiCar/src/pi/IMU_Lidar, you can find the method to enable IMU library `here <http://picar.readthedocs.io/en/latest/chapters/usage/electronics.html#pi-and-imu-communication>`_

**IMPORTANT: If you have gone through the process before 06/18/2018, make sure you execute all steps again, few more functions and wrappers are added to the library**

Run the script, a folder under the same directory would be generated, its name would be the starting timestamp of the script.

The file itself contains several straight forward methods that can be used to get data from IMU LiDar. The method it uses to take pictures is currently only viable within the script.

The imu setting functions can't be used outside the script.

If called from command line or python shell, the script would put picture taking job and data logging job into two different cores on RaspberryPi

Use the command line option, you can bring up the usage page

.. code-block:: bash

   python Lidar_IMU_data_optimize_delta.py -h

The script is based on delta timing method. A constant value of 0.0007 is subtracted from the period to maintain a consistent reading frequency.

Precision defines the minimum time that the script goes to check the diffrence between the last time and current time and consequently defines within what time difference that measures of LiDar and IMU occur simultaneously.


**A great part of the codes are from Josh Jin's sensor/camera reading code**

Version Beta (Magnetic reading added to IMU)
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

*Creator : Jerry Kong*

*The code could be found in PiCar/src/pi/IMU_Lidar, the  socket_server_client.py file is a integrated and important part of this data logging script, to learn more about socket folder sending, take a look at* ` socket based file sending <http://picar.readthedocs.io/en/latest/chapters/usage/software.html#advanced-folder-transfer>`_

Endless mode is implemented. User could stop the experiment with KeyboardInterrupt, the logging file and camera file would still be saved

Using -i command line input, we could run the script in endless mode (i.e. the duration would be set to 1000 seconds, we could stop the program by using KeyboardInterrupt(Ctrl + C))

Logging file sending module is integarted into the logging script. After the multiprocessing finished (loggind and filming), the script would start a raw socket server and a client on another computer could use the client side script to receive the logging file.

The script could either be called from the terminal or from other script by calling the funtion getSensorAndCamera.

'-s' command line argument and save parameter for getSensorAndCamera is implemented so that users can decide whether they want the logging file to be saved locally.

For installation and usage see the previous section

Data Analysis
-------------
To do
