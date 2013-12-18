# -*-coding:Utf-8 -*

import ResourceManager
from handlers.Handler import *
from TcpSocket import *

# Common vocabulary for TCP requests
LISTEN_COMMAND = "LISTEN_PORT "
NEXT_IMG = -1

class TcpHandler(Handler):
	"""
	This class implements the common elements for the TCP_PULL and TCP_PUSH connections.
	"""

	def __init__(self, commandSocket, protocol):
		"""
		Initializes all attributes
		"""
		Handler.__init__(self, protocol)
		self.commandSocket = commandSocket
		self._dataSocket = None
		self._clientIp = None
		self._clientListenPort = None

		# TODO : these properties should come from the catalog
		self._mediaId = 5
		self._currentFrameId = 0

	def kill(self):
		"""
		Properly closes all sockets and interrupts the thread.
		"""
		self._interruptFlag = True
		# We inform the sockets that we want them to commit suicide
		# Note: dataSocket must be closed first as the client closes the connection from its side
		if None != self._dataSocket:
			self._dataSocket.kill()
		self.commandSocket.kill()

	def receiveCommand(self):
		"""
		Receive a command from the client on the control socket and interpret it.
		"""
		while not self._interruptFlag:
			command = self.commandSocket.nextLine()
			print('"{}" received'.format(command))

			if None == command:
				continue
			else:
				self._interpretCommand(command)

	def _interpretCommand(self, command):
		"""
		Interpret the command received from the client and respond on the dataSocket.
		"""

		# The GET command could mean either "establish connection" or "send a frame"
		if GET_COMMAND == command[:len(GET_COMMAND)]:
			if None == self._dataSocket:
				self._establishMediaConnection()
			else:
				frameId = int(command[len(GET_COMMAND):])
				# Empty line necessary
				print("Waiting for blank line...")
				# TODO : fix waiting for blank line timing out ?
				if "" == self.commandSocket.nextLine():
					# If we were asked for a specific frameId (otherwise just send the next one)
					if (NEXT_IMG != frameId):
						self._currentFrameId = frameId

					self._sendCurrentFrame()
		# If we couldn't recognized this command, maybe one of the parent class can
		else:
			Handler._interpretCommand(self, command)

	def _establishMediaConnection(self):
		"""
		Connects the dataSocket to the port given via the commandSocket
		"""
		# Read the client listening port from the rest of the command
		command = self.commandSocket.nextLine()
		if LISTEN_COMMAND == command[:len(LISTEN_COMMAND)]\
		   and "" == self.commandSocket.nextLine():
			(self._clientIp, unused) = self.commandSocket.getIp()
			self._clientListenPort = int(command[len(LISTEN_COMMAND):])
			# We establish a new connection to the client to send the requested media
			# TODO : handle "connection refused" gracefully
			self._dataSocket = TcpSocket()
			self._dataSocket.connect(self._clientIp, self._clientListenPort)

	def _prepareMessage(self, frameId, frameContent):
		"""
		This function takes an image and adds surrounding information so that the client applications can interpret it.

		It returns a full message ready to be sent to the client via socket, containing:
		- This frame's id (followed by endline)
		- This frame's content size (followed by endline)
		- The actual frame content
		"""

		message = bytes(str(frameId) + END_LINE\
			 		  + str(len(frameContent)) + END_LINE, 'Utf-8')\
			 	+ frameContent
		return message

	def _sendCurrentFrame(self):
		"""
		Sends the current image (based on currentFrameId) to the client through the dataSocket.
		"""
		(image, nextFrameId) = ResourceManager.getFrame(self._mediaId, self._currentFrameId)
		# message = str(self._currentFrameId) + END_LINE
		# message += str(image['size']) + END_LINE
		# message = message.encode('Utf-8')
		# message += image['bytes']

		print("Sending frame {} next frame will be #{}.".format(self._currentFrameId, nextFrameId))
		message = self._prepareMessage(self._currentFrameId, image)
		self._dataSocket.send(message)

		self._currentFrameId = nextFrameId