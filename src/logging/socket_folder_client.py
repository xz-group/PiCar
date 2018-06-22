# client.py
import os
import sys
import socket                   # Import socket module
import time
s = socket.socket()             # Create a socket object
host = 'localhost'     # Get local machine name
port = 60001                    # Reserve a port for your service.

s.connect((host, port))
data=s.recv(1024)
l=int.from_bytes(data[0:2],byteorder='big',signed='true')
flds = data[2:2+l].decode('ascii')
folders = flds.split("!")
for folder in folders:
    if folder!="" and " " not in folder:
        os.mkdir(folder)

file = ""

while True:
    get = s.recv(1024)
    if not get:
        break
    ll = int.from_bytes(get[0:2],byteorder='big',signed='true')
    if ll>=0 and file!="":
        f.write(get[2:2+ll])
    else:
        if file=="":
            ll=abs(ll)
            file=get[2:2+ll].decode('ascii')
            f = open(file,'wb')
        else:
            f.close()
            ll=abs(ll)
            file=get[2:2+ll].decode('ascii')
            f = open(file,'wb')


s.close()
print('connection closed')

