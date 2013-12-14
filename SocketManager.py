﻿# -*-coding:Utf-8 -*
from threading import Thread
import select

from handlers import HandlerFactory
from handlers import Handler
from TcpSocket import *
from UdpSocket import *

class SocketManager(Thread):
	"""
	SocketManager represents the thread receiving the connection requests and creating
	a new socket (and associated thread) for each client.
	"""

	def __init__(self, host, port):
		Thread.__init__(self)
		self.interruptFlag = False

		self._selectTimer = 3

		self._host = host
		self._listeningPort = port
		self._protocol = HandlerFactory.getProtocol(port)

		print('Will listen on', host, ':', port, '(', self._protocol, ')')
		# We will maintain a list of all active connections
		self.clients = []

	def run(self):
		clientSocket = None
		if   Handler.Protocol.TCP == self._protocol:
			clientSocket = self.startTcpHandler()
		elif Handler.Protocol.UDP == self._protocol:
			clientSocket = self.startUdpHandler()

	def startTcpHandler(self):
		serverSocket = TcpSocket()
		serverSocket.listen(self._host, self._listeningPort)
		clientSocket = None
		# One TCP Handler per client
		while not self.interruptFlag:
			clientSocket = serverSocket.accept()

			self.startHandler(clientSocket)

	def startUdpHandler(self):
		# One UDP Handler for all of the clients
		clientSocket = UdpSocket()
		clientSocket.listen(self._host, self._listeningPort)

		self.startHandler(clientSocket)

	def startHandler(self, clientSocket):
		clientThread = HandlerFactory.createAppropriateHandler(self._listeningPort, clientSocket)

		self.clients.append(clientThread)
		clientThread.start()

		print("Handler #{} started.".format(len(self.clients)))
		print('Listening on', self._host, ':', self._listeningPort, "({})".format(self._protocol))

	def kill(self):
		print("Closing port {} : killing {} client threads (will go down in {} seconds or less).".format(self._listeningPort, len(self.clients), self._selectTimer))

		# TODO : sometimes client connections go down even if we do not kill them. Purge the clients list regularly ?

		i = 0
		for client in self.clients:
			# If this thread is still running, we kindly ask it to die
			if client.is_alive():
				client.kill()
			i += 1
			print(( len(self.clients) - i), " clients still alive")
		
		# And we then kill ourself
		self.interruptFlag = True