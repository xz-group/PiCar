import socket

UDP_IP = "255.255.255.255"
UDP_PORT = 5005

sock = socket.socket(socket.AF_INET,	# Internet
		    socket.SOCK_DGRAM)	# UDP

sock.bind((UDP_IP, UDP_PORT))

while True:
	data = sock.recv(1024)
	print("received message: " + data)
