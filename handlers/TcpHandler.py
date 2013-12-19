# -*-coding:Utf-8 -*

import ResourceManager
from handlers.Handler import *
from TcpSocket import *

# Common vocabulary for TCP requests
CONNECTION_COMMAND = "GET "
LISTEN_COMMAND = "LISTEN_PORT "

class TcpHandler(Handler):
	"""
	This class implements the common elements for the TCP_PULL and TCP_PUSH connections.
	"""

	def __init__(self, commandSocket):
		"""
		Initializes all attributes
		"""
		Handler.__init__(self, commandSocket)
		self._commandSocket = commandSocket
		self._dataSocket = None
		self._clientIp = None
		self._clientListenPort = None

	def kill(self):
		"""
		Properly closes all sockets and interrupts the thread.
		"""
		self._interruptFlag = True
		# We inform the sockets that we want them to commit suicide
		# Note: dataSocket must be closed first as the client closes the connection from its side
		if None != self._dataSocket:
			self._dataSocket.kill()
		self._commandSocket.kill()

	def _interpretCommand(self, command):
		"""
		Interpret the command received from the client and respond on the dataSocket.
		"""

		# The GET command could mean either "establish connection" or "send a frame"
		if None == self._dataSocket and self.isCommand(command, CONNECTION_COMMAND):
			self._establishMediaConnection()
		# If we couldn't recognized this command, maybe one of the parent class can
		else:
			# The parent says whether he interpreted the command
			return Handler._interpretCommand(self, command)

		# We say we interpreted the command
		return True

	def _establishMediaConnection(self):
		"""
		Connects the dataSocket to the port given via the commandSocket
		"""
		# Read the client listening port from the rest of the command
		command = self._commandSocket.nextLine()
		
		if self.isCommand(command, LISTEN_COMMAND)\
		   and "" == self._commandSocket.nextLine():
			self._clientIp = self._commandSocket.getIp()
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

		message = str(frameId) + END_LINE \
				+ str(len(frameContent)) + END_LINE
		message = message.encode('Utf-8')
		message += frameContent
		return message

	def _sendCurrentFrame(self):
		"""
		Sends the current image (based on currentFrameId) to the client through the dataSocket.
		"""
		(image, nextFrameId) = ResourceManager.getFrame(self._mediaId, self._currentFrameId)

		message = self._prepareMessage(self._currentFrameId, image)
		self._dataSocket.send(message)

		self._currentFrameId = nextFrameId