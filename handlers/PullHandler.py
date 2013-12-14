# -*-coding:Utf-8 -*

from handlers.Handler import *
from TcpSocket import *
import ResourceManager

# TODO move to another file (protocol)
GET_COMMAND = "GET "
END_COMMAND = "END"
LISTEN_COMMAND = "LISTEN_PORT "
NEXT_IMG = -1
END_LINE = "\r\n"

class PullHandler(Handler):
	"""
	This class is able to manage connections from clients who are interested in getting a TCP Pull connection.
	"""
	
	def __init__(self, commandSocket, protocol):
		"""
		Initializes all attributes
		"""
		Handler.__init__(self, protocol)
		self.commandSocket = commandSocket
		self.dataSocket = None
		self.mediaId = None
		self.currentImageId = 0
		self.listenPort = None
		
	def run(self):
		print("{}PullHandler ready.".format(self.protocol))
		self.receiveCommand()
	
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

	def receiveCommand(self):
		"""
		Real work: interprets the commands emitted via the commandSocket
		and answers through the dataSocket
		"""
		while not self.interruptFlag:
			command = self.commandSocket.nextLine()
			print("\"{}\" received".format(command))

			if None == command:
				continue

			if END_COMMAND == command:
				# Empty line necessary
				print("Waiting for blank line...")
				if "" == self.commandSocket.nextLine():
					self.kill()
					print("Connection closed.")

			if GET_COMMAND == command[:len(GET_COMMAND)]:
				id = int(command[len(GET_COMMAND):])
				if None == self.dataSocket:
					# New connection required
					self.dataSocket = TcpSocket()
					self._connect(id)
				else:
					imageId = int(id)
					# Empty line necessary
					print("Waiting for blank line...")
					if "" == self.commandSocket.nextLine():
						if (NEXT_IMG == imageId):
							# Sends and increments the currentImageId
							self._sendCurrent()
						else:
							# Sets the right image ID
							self.currentImageId = imageId

							# Sends
							self._sendCurrent()

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

	def _connect(self, mediaId):
		"""
		Connects the dataSocket to the port given via the commandSocket
		"""
		self.mediaId = mediaId
		print("mediaId: {}".format(mediaId))
		command = self.commandSocket.nextLine()
		if LISTEN_COMMAND == command[:len(LISTEN_COMMAND)] and "" == self.commandSocket.nextLine():
			self.listenPort = int(command[len(LISTEN_COMMAND):])
			(self.clientIp, unused) = self.commandSocket.getIp()
			self.dataSocket.connect(self.clientIp, self.listenPort)