# -*-coding:Utf-8 -*
from threading import Thread

class Handler(Thread):

	def __init__(self):
		Thread.__init__(self)
		self.interruptFlag = False
	
	def kill(self):
		"""
		Properly closes all sockets and interrupts the thread
		"""
		self.interruptFlag = True
		# We inform the sockets that we want them to commit suicide
		# Note: dataSocket must be closed first as the client closes it first
		if None != self.dataSocket:
			self.dataSocket.kill()
		self.commandSocket.kill()

	def __init__(self, commandSocket):
		"""
		Initializes all attributes
		"""
		Handler.__init__(self, self.Protocol.TCP)
		self.commandSocket = commandSocket
		self.dataSocket = None
		self.mediaId = None
		self.currentImageId = 0
		self.clientListenPort = None

	def run(self):
		print("Generic Handler ready.")
		self.receiveCommand()
