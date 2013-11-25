# -*-coding:Utf-8 -*
from threading import Thread

from Handler import *

class ClientHandler(Handler):
	"""Cette classe représente le thread recevant les commandes du client, et lui répondant. On a donc un thread par connexion active avec un client."""
	
	def __init__(self, clientSocket):
		Handler.__init__(self)
		self.clientSocket = clientSocket
		
		# On prépare le catalogue
		self.catalog = b''
		self.catalog += b'HTTP/1.1 200 OK\r\nServer: TP_3IF_PythonMediaServer\r\nConnection: Keep-Alive\r\nContent-Type: text/txt\r\nContent-Length: 100\r\n\r\n'
		self.catalog += b'Object ID=1 name=video1 type=BMP address=127.0.0.1 port=8088 protocol=TCP_PUSH ips=1.50\r\nObject ID=3 name=video3 type=BMP address=225.100.110.12 port=11111 protocol=MCAST_PUSH ips=0.50\r\n\r\n'
		
	def run(self):
		print("Running the new thread")
		self.receiveCommand()
		
	def receiveCommand(self):
		command = b''
		while command != b'e' and not self.interruptFlag:
			command = self.clientSocket.receive()
			
			if command != b'e':
				print(command, ' received, sending catalog.')
				self.clientSocket.send(self.catalog)
			else:
				print(command, ' received, closing connection.')
				self.clientSocket.send(b'The connection is going down now.')
				self.clientSocket.close()