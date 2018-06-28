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

*Creator: Jerry Kong

To meet our need of a neat and organized data structure, this script is created.
It has the capability to transfer the entire folder to another remote desktop, no matter it is on a Windows System or Unix system.
The script rests in PiCar/src/Logging
To use the script, first setup the ip addresses like in the basic version, change the root variable to the root folder name.
Place the script at the same level as the root folder. Start the server script and then start the client script. The folder would then be transferred.
A better protocol could be implemented, since the protocol now being used is not really efficient though fulfill the need of our experiment for now.


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

Using -i command line input, we could run the script in endless mode (i.e. the duration would be set to 1000 seconds, we could stop the program by using KeyboardInterrupt(Ctrl + C), the pictures and logging data would be save up until the stopping point)

**A great part of the codes are from Josh Jin's sensor/camera reading code**



Data Analysis
-------------
To do
