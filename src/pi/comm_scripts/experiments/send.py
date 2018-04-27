import socket

UDP_IP = "255.255.255.255"
UDP_PORT = 5005

MESSAGE = "HELLO WORLD"

print("UDP target: " + UDP_IP)
print("UDP target port: " + str(UDP_PORT))
print("")

sock = socket.socket(socket.AF_INET,	# Internet
		    socket.SOCK_DGRAM)	# UDP

sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1) # see pubs.opengroup.org/onlinepubs/009695399/functions/setsockopt.html for docs

while True:
	sock.sendto(MESSAGE, (UDP_IP, UDP_PORT))
	MESSAGE = raw_input("Enter a message: ")
