Software
=============

The software section will document all the heavy duty programming
programming aspects of the project. There may be some overlap with
the Electronics section.

Socket File Transfer
--------------------

Server side
^^^^^^^^^^^

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
^^^^^^^^^^^

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


Sensors(Lidar,IMU) reading and writing
--------------------------------------

Setup:
^^^^^^
Make sure you have alreadly connect TFmini Lidar and IMU as
`TFmini Lidar <http://picar.readthedocs.io/en/latest/chapters/usage/electronics.html#pi-and-tfmini-lidar-communication>`_
, `IMU by LSM9DS1 <http://picar.readthedocs.io/en/latest/chapters/usage/electronics.html#pi-and-imu-communication>`_ did.
and download corresponding libraris.

source code:
Under Directory PiCar/src/pi/IMU_Lidar

steps:
^^^^^^
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

Data Logging
------------
To do

Data Analysis
-------------
To do
