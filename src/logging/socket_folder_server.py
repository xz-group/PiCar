import os
import socket                   # Import socket module

port = 60001                    # Reserve a port for your service.
s = socket.socket()             # Create a socket object
host = "localhost"     # Get local machine name
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.
root = "rt"
print ("begin")
folders = []
files = []

for dirname, dirnames, filenames in os.walk(root):
    # print path to all subdirectories first.
    for subdirname in dirnames:
        folders.append(os.path.join(dirname, subdirname))
    # print path to all filenames.
    for filename in filenames:
        files.append(os.path.join(dirname, filename))


conn, addr = s.accept()     # Establish connection with client.
print ('Got connection from', addr)
#transfer folder
folderstream = root+"!"+"".join([folder+"!" for folder in folders])
fl = len(folderstream)
conn.send(bytearray((fl).to_bytes(2,byteorder='big',signed='true'))+folderstream.encode('ascii')[0:]+bytearray(1022-fl)[0:])


for file in files:
    length = len(file)
    conn.send((-length).to_bytes(2,byteorder='big',signed='true'))
    conn.send(file.encode('ascii'))
    conn.send(bytes(1022-length))
    f = open(file,'rb')
    l = f.read(1022)
    while (l):
        k = len(l)
        conn.send(k.to_bytes(2,byteorder='big',signed='true'))
        conn.send(l)
        if 1022-k != 0:
            conn.send(bytes(1022-k))
        l = f.read(1022)          #alter this to control data sending rate
    f.close()

conn.close()