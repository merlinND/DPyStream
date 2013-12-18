# -*-coding:Utf-8 -*
import socket

commandSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
commandSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Listening at this address
#commandSocket.bind(("0.0.0.0", 13000))

# Sending to this address
host = "127.0.0.1"
port = int(input("sending port = "))

message = ""

while b'STOP' != message:

	message = input("message: ")

	message += "\r\n"

	message = message.encode('Utf-8')

	commandSocket.sendto(message, (host, port))





#command = None
#answer  = None

#command = b'GET 5\r\n#LISTEN_PORT 13000\r\nFRAGMENT_SIZE 512\r\n\r\n'
#print("sending: {}".format(command))
#commandSocket.sendto(command, (host, port))


#command = b'GET -1\r\n\r\n'
#print("sending: {}".format(command))
#commandSocket.sendto(command, (host, port))

#while "STOP_SENDING" != command:

#	answer, (serverIp, serverPort) = commandSocket.recvfrom(4096)

#	print("answer: {}".format(answer))
#	print("(from {}:{})".format(serverIp, serverPort))

#	command = input("command: ")
