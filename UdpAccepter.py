# -*-coding:Utf-8 -*
from UdpSocket import *

class UdpAccepter:
	"""
	UdpAccepter makes it possible to know when to create a new UdpSocket for a new client.
	It receives messages from all clients and redirects them to the appropriate UdpSocket.
	The UdpSocket adds the message to its buffer which is then read by its parent UdpHandler.
	"""

	def __init__(self, receiveBuffer = 4096, s = None):
		if s is None:
			self.commonSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		else:
			self.commonSocket = s
		self.receiveBuffer = receiveBuffer

		self._interruptFlag = False
		self._connectedClients = {}

	def listen(self, host, port):
		self.commonSocket.bind((host, port))

	def accept(self):
		client = ""
		newClient = False
		host = None
		port = None

		message, (host, port) = self.commonSocket.recvfrom(self.receiveBuffer)
		client = host + ":" + str(port)

		# If necessary, create a new UdpSocket instance for this client and add it to the list
		if client not in self._connectedClients:
			newClient = True
			self._connectedClients[client] = UdpSocket(self.commonSocket, host, port)

		# Forwards the received to the UdpSocket corresponding to this client
		self._connectedClients[client].receive(message)
		
		if newClient:
			# Returning a socket handling that client and the message received
			return self._connectedClients[client]
		else:
			return None
	
	def kill(self):
		self._interruptFlag = True