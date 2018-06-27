# client.py

# for picar lab students use command "python3 socket_folder_client.py 172.16.10.208 31418"
import os
import sys
import socket                   # Import socket module
import time
s = socket.socket()             # Create a socket object
host = sys.argv[1]     # Get local machine name
port = int(sys.argv[2])                   # Reserve a port for your service.

s.connect((host, port))
data=s.recv(1024)
#print(len(data))
if len(data)!=1024:
    sup = s.recv(1024-len(data))
    data = bytearray(data)+sup[0:]
l=int.from_bytes(data[0:2],byteorder='big',signed='true')
flds = data[2:2+l].decode('ascii')
folders = flds.split("!")
for folder in folders:
    if folder!="":
        os.mkdir(folder)

file = ""

while True:
    get = s.recv(1024)
    if not get:
        break
    if len(get)!=1024:
        sup = s.recv(1024-len(get))
        while len(get)==0:
            sup = s.recv(1024-len(get))
        #print(str(len(sup))+"sup")
        get = bytearray(get)+sup[0:]
    #print(len(get))
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
