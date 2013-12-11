# -*-coding:Utf-8 -*

from handlers.Handler import *
from TcpSocket import *

class TcpPullHandler(Handler):
	"""
	This class is able to manage connections from clients who are interested in getting a TCP Pull connection.
	"""
	
	def __init__(self, commandSocket):
		Handler.__init__(self)
		self.commandSocket = commandSocket
		self.dataSocket = None
		self.mediaId = None
		self.listenPort = None
		
	def run(self):
		print("TcpPullHandler ready.")
		self.receiveCommand()
	
	def kill(self):
		self.interruptFlag = True
		# We inform the sockets that we want it to commit suicide
		self.commandSocket.kill()
		if None != self.dataSocket:
			self.dataSocket.kill()

	def receiveCommand(self):
		while not self.interruptFlag:
			command = self.commandSocket.nextLine()
			print("\"{}\" received".format(command))

			if None == command:
				continue

			if "END" == command:
				if "" == self.commandSocket.nextLine():
					self.kill()
					print("Connection closed.")

			if "GET " == command[:4]:
				if None == self.dataSocket:
					# New connection required
					self._connect(int(command[4:]))
#				else:
#					self.imageId = int(command[4:])

	def _connect(self, mediaId):
		self.mediaId = mediaId
		print("mediaId: {}".format(mediaId))
		command = self.commandSocket.nextLine()
		if "LISTEN_PORT " == command[:12] and "" == self.commandSocket.nextLine():
			self.listenPort = int(command[12:])
			(self.clientIp, unused) = self.commandSocket.getIp()
			self.dataSocket = TcpSocket()
			self.dataSocket.connect(self.clientIp, self.listenPort)
#		else:
