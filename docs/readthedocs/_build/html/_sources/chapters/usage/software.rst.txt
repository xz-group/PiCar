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



Data Logging
------------
To do

Data Analysis
-------------
To do
