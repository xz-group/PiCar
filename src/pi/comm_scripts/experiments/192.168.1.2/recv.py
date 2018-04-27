import socket

UDP_IP = "255.255.255.255"
UDP_PORT = 5005

serial_number = "192.168.1.2"

sock = socket.socket(socket.AF_INET,	# Internet
		    socket.SOCK_DGRAM)	# UDP

sock.bind((UDP_IP, UDP_PORT))

while True:
	data, addr = sock.recvfrom(1024)
	if addr[0] != serial_number:
		print("received message: " + data + "\n")
