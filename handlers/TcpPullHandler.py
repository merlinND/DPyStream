# -*-coding:Utf-8 -*

from handlers.Handler import *

class TcpPullHandler(Handler):
	"""
	This class is able to manage connections from clients who are interested in getting a TCP Pull connection.
	"""
	
	def __init__(self, socket):
		Handler.__init__(self)
		self.socket = socket
		self.mediaId = None
		self.listenPort = None
		
	def run(self):
		print("TcpPullHandler ready.")
		self.receiveCommand()
	
	def kill(self):
		self.interruptFlag = True
		# We inform the socket that we want it to commit suicide
		self.socket.kill()

	def receiveCommand(self):
		while not self.interruptFlag:
			command = self.socket.nextLine()
			print("\"{}\" received".format(command))

			if "END" == command:
				if "" == self.socket.nextLine():
					self.kill()
					print("Connection closed.")

#			if "GET " == command[:4]:
#				if None == self.mediaId:
#					# New connection required
#					self._connect(int(command[4:]))
#				else:


#	def _connect(self, mediaId):
#		self.mediaId = mediaId
#		print("mediaId: {}".format(mediaId))
#		command = self.socket.nextLine()
#		if "LISTEN_PORT " == command[:12] and "" == self.socket.nextLine():
#			self.listenPort = int(command[12:])
#			(self.clientIp, unused) = self.socket.s.getsockname()
#			s = socket.socket()
#			s.connect((self.clientIp, self.listenPort))
#		else:
