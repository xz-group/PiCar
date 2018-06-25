import os
import sys
import socket                   # Import socket module

#pi tarzan 192.168.1.121

def send(host,port,root):
                            # Reserve a port for your service.
    s = socket.socket()             # Create a socket object
                                        # Get local machine name
    s.bind((host, port))            # Bind to the port
    s.listen(5)                     # Now wait for client connection.
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
        conn.send(bytearray((-length).to_bytes(2,byteorder='big',signed='true'))+file.encode('ascii')[0:]+bytes(1022-length)[0:])
        f = open(file,'rb')
        l = f.read(1022)
        while (l):
            k = len(l)
            conn.send(bytearray(k.to_bytes(2,byteorder='big',signed='true'))+l[0:]+bytes(1022-k)[0:])
            l = f.read(1022)          #alter this to control data sending rate
        f.close()

    conn.close()

if __name__=='__main__':
    send(sys.argv[1],int(sys.argv[2]),sys.argv[3])

