# -*-coding:Utf-8 -*

from handlers.Handler import *

from TcpSocket import *
import ResourceManager

class UdpPushHandler(Handler):
	"""
	This class is able to manage connections from clients who are interested in getting a UDP Push connection.
	"""

	def __init__(self, commandSocket):
		"""
		Initializes all attributes
		"""
		Handler.__init__(self, self.SocketType.UDP)
		self.commandSocket = commandSocket
		self.dataSocket = None
		self.mediaId = None
		self.currentImageId = 0
		self.listenPort = None

	def run(self):
		print("UdpPushHandler ready.")
		self.receiveCommand()
	
	def kill(self):
		"""
		Properly closes all sockets and interrupts the thread
		"""
		self.interruptFlag = True
		# Interrupts the sockets:
		if None != dataSocket:
			self.dataSocket.kill()
		self.commandSocket.kill()

	def receiveCommand(self):
		"""
		Real work: interprets the commands emitted via the commandSocket
		and answers through the dataSocket
		"""
		while not self.interruptFlag:
			command = self.commandSocket.nextLine()
			print("Received: {}".format(command))
			if "END" == command:
				print("Waiting for blank line...")
				if "" == self.commandSocket.nextLine():
					self.kill()


	def _sendCurrent(self):
		"""
		Sends the current image (based on currentImageId) via the dataSocket
		"""
		# Getting the image
		image = ResourceManager.getFrame(self.mediaId, self.currentImageId)

		# Prepares the message to send
		message = str(self.currentImageId) + END_LINE
		message += str(image['size']) + END_LINE
		message = message.encode('Utf-8')
		message += image['bytes']

		# Sends it
		self.dataSocket.send(message)

		# Gets the next image id to send
		self.currentImageId = image['nextId']
