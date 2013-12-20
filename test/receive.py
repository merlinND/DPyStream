# -*-coding:Utf-8 -*
import socket
from sockets.TcpSocket import *

protocol = input("protocol = ")
host = "127.0.0.1"
port = int(input("receiving port = "))

if "udp" == protocol:
	recevingSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	recevingSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	recevingSocket.bind((host, port))
elif "tcp" == protocol:
	receivingSocket = TcpSocket()
	receivingSocket.listen(host, port)
	receivingSocket = receivingSocket.accept()

message = ""

while "STOP" != message:
	if "udp" == protocol:
		message, (clientIp, clientPort) = recevingSocket.recvfrom(4096)
	elif "tcp" == protocol:
		message = receivingSocket.receive(4096)

#	message = str(message, 'Utf-8')

	print("message: {}".format(message))