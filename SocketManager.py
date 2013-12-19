# -*-coding:Utf-8 -*
from threading import Thread
import select

from handlers import HandlerFactory
from handlers.HandlerFactory import Protocol
from TcpSocket import *
from UdpSocket import *
from UdpAccepter import *

class SocketManager(Thread):
	"""
	SocketManager represents the thread receiving the connection requests and creating
	a new socket (and associated thread) for each client.
	"""

	def __init__(self, host, port, protocol):
		Thread.__init__(self)
		self._interruptFlag = False

		self._selectTimer = 3

		self._host = host
		self._listeningPort = port
		self._protocol = protocol

		print('Listening on {}:{} ({})'.format(host, port, self._protocol))
		# We will maintain a list of all active connections
		self.clients = []
		self.accepter = None

	def run(self):
		if 		Protocol.CATALOG == self._protocol \
			or Protocol.TCP_PUSH == self._protocol \
			or Protocol.TCP_PULL == self._protocol:
			self.acceptTcp()
		elif	Protocol.UDP_PULL == self._protocol \
			or  Protocol.UDP_PUSH == self._protocol:
			self.acceptUdp()
		elif	Protocol.MCAST_PUSH == self._protocol:
			# MultiCast works very differently: we don't wait for anyone to ask for the content,
			# we just send it out continuously
			self.startHandler(None)
		else:
			raise Exception('Protocol {} not supported by SocketManager.'.format(self._protocol))

	def acceptTcp(self):
		serverSocket = TcpSocket()
		serverSocket.listen(self._host, self._listeningPort)
		clientSocket = None
		# One TCP Handler per client
		while not self._interruptFlag:
			(readyToRead,rw,err) = select.select([serverSocket.s], [], [], self._selectTimer)
			if readyToRead:
				clientSocket = serverSocket.accept()

				self.startHandler(clientSocket)

	def acceptUdp(self):
		self.accepter = UdpAccepter()
		self.accepter.listen(self._host, self._listeningPort)

		while not self._interruptFlag:
			(readyToRead,rw,err) = select.select([self.accepter.commonSocket], [], [], self._selectTimer)
			if readyToRead:
				# One UDP socket per client, knowing its client
				clientSocket = self.accepter.accept()
				if None != clientSocket:
					self.startHandler(clientSocket)


	def startHandler(self, clientSocket):
		try:
			clientThread = HandlerFactory.createAppropriateHandler(self._listeningPort, clientSocket)
			self.clients.append(clientThread)
			clientThread.start()
		except Exception:
			print('Could not instanciate an appropriate handler for port', self._listeningPort, '- ignoring request')

	def kill(self):
		print("Closing port {} : killing {} threads (going down in {} seconds or less).".format(self._listeningPort, len(self.clients), self._selectTimer))

		if None != self.accepter:
			self.accepter.kill()
		i = 0
		for client in self.clients:
			# If this thread is still running, we kindly ask it to die
			if client.is_alive():
				client.kill()
			i += 1
			print(( len(self.clients) - i), " clients still alive")
		
		# And we then kill ourself
		self._interruptFlag = True