# -*-coding:Utf-8 -*
from UdpSocket import *

class UdpAccepter:
	"""
	UdpAccepter makes it possible to know when to create
	a new UdpSocket for a new client.
	"""

	def __init__(self, receiveBuffer = 4096, s = None):
		if s is None:
			self.commonSocket = socket.socket(socket.AF_INET,\
											  socket.SOCK_DGRAM)
		else:
			self.commonSocket = s
		self.receiveBuffer = receiveBuffer

		self.interruptFlag = False
		self._connectedClients = {}

	def listen(self, host, port):
		self.commonSocket.bind((host, port))

	def accept(self):
		client = ""
		newClient = False
		host = None
		port = None

		message, (host, port) = self.commonSocket.recvfrom	\
								  (self.receiveBuffer)

		client = host + ":" + str(port)

		# Adding client socket to the list
		if client not in self._connectedClients:
			newClient = True
			self._connectedClients[client] = \
					UdpSocket(self.commonSocket, client)

		self._connectedClients[client].receive(message)
		
		if newClient:
			# Returning a socket handling that client
			# and the message received
			return self._connectedClients[client]
		else:
			return None
	
	def kill(self):
		self.interruptFlag = True