# -*-coding:Utf-8 -*
import socket

recevingSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
recevingSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

host = "127.0.0.1"
port = int(input("receiving port = "))

recevingSocket.bind((host, port))

message = ""

while "STOP" != message:
	message, (clientIp, clientPort) = recevingSocket.recvfrom(4096)

#	message = str(message, 'Utf-8')

	print("message: {}".format(message))