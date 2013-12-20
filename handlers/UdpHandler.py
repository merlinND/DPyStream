# -*-coding:Utf-8 -*
from threading import Timer

import ResourceManager
from handlers.Handler import *
from UdpSocket import *

# Common vocabulary for UDP requests
# TODO: put all commands in an enum?
# TODO: create function to test for commands easily (rather than always use GET_COMMAND == command[:len(GET_COMMAND)])

CONNECTION_COMMAND = "GET "
LISTEN_COMMAND = "LISTEN_PORT "

FRAGMENT_COMMAND = "FRAGMENT_SIZE "

# Used for the java client, which does recvfrom(FRAGMENT_SIZE) instead of recvfrom(FRAGMENT_SIZE + MAX_HEADER_SIZE):
MAX_HEADER_SIZE = 25

# Done for all UDP connections so that if the END command is not sent, the connection is closed at some point.
KEEP_ALIVE_COMMAND = "ALIVE "
ALIVE_TIMEOUT = 60

class UdpHandler(Handler):
	"""
	This class implements the common elements for the UDP_PULL and UDP_PUSH connections.
	"""

	def __init__(self, commandSocket):
		"""
		Initializes all attributes
		"""
		Handler.__init__(self, commandSocket)
		self._dataSocket = None
		self._fragmentSize = None

		# If the keep-alive wasn't sent after ALIVE_TIMEOUT seconds, we commit suicide.
		self._aliveTimer = Timer(ALIVE_TIMEOUT, self.kill)
		self._aliveTimer.start()
		self._isAliveTimerRunning = True

	def kill(self):
		"""
		Properly closes all sockets and interrupts the thread.
		"""
		Handler.kill(self)

		self._aliveTimer.cancel()
		self._isAliveTimerRunning = False

	def restartKeepAliveTimer(self):
		self._aliveTimer.cancel()
		self._aliveTimer = Timer(ALIVE_TIMEOUT, self.kill)
		self._aliveTimer.start()

	def _interpretCommand(self, command):
		"""
		Interpret the command received from the client and
		respond on the dataSocket.
		"""

		# The GET command could mean either "setup" or "send a frame"
		if None == self._fragmentSize and self.isCommand(command, CONNECTION_COMMAND):
			self.setupClientContact()
			# If we needed to "send a frame", we let PushHandler or PullHandler take care of it
		elif self.isCommand(command, KEEP_ALIVE_COMMAND):
			self._commandSocket.nextLine() # Pass empty line
			self.restartKeepAliveTimer()
		# If we couldn't recognized this command, maybe one of the parent class can
		else:
			# The parent says whether he interpreted the command
			return Handler._interpretCommand(self, command)
		
		# We say we interpreted the command
		return True

	def setupClientContact(self):
		"""
		Remembers the client listen port given via the commandSocket
		"""
		# Read the client listening port from the rest of the command
		command = self._commandSocket.nextLine()
		if self.isCommand(command, LISTEN_COMMAND):
			self._clientIp = self._commandSocket.getIp()
			self._clientListenPort = int(command[len(LISTEN_COMMAND):])

			command = self._commandSocket.nextLine()
			self._fragmentSize = int(command[len(FRAGMENT_COMMAND):]) - MAX_HEADER_SIZE

			# We create a UDP socket to send out the data
			self._dataSocket = UdpSocket(None, self._clientIp, self._clientListenPort)

	def _prepareMessages(self, frameId, frameContent):
		"""
		Chops the frame in fragments of size _fragmentSize and create one message per fragment.
		Returns a list of messages ready to be sent to the client via socket, containing:
		- This frame's id (followed by endline)
		- This frame's content size (followed by endline)
		- This fragment's position (followed by endline)
		- This fragment's size (followed by endline)
		- The actual fragment content
		"""
		messages = []

		totalFrameSize = str(len(frameContent))
		frameIdString = str(frameId)
		remainingSize = len(frameContent)
		fragmentNumber = 0
		while remainingSize > 0:
			if remainingSize >= self._fragmentSize:
				thisFragmentSize = self._fragmentSize
			else:
				thisFragmentSize = remainingSize

			message = frameIdString + END_LINE\
				 	+ totalFrameSize + END_LINE\
				 	+ str(fragmentNumber * self._fragmentSize) + END_LINE\
				 	+ str(thisFragmentSize) + END_LINE
			message = message.encode('Utf-8')

			begin = self._fragmentSize * fragmentNumber
			end = begin + thisFragmentSize
			message += frameContent[begin:end]

			messages.append(message)
			remainingSize -= self._fragmentSize
			fragmentNumber += 1

		return messages

	def _sendCurrentFrame(self):
		"""
		Sends the current image (based on currentFrameId) to the client through a socket created for the occasion.
		"""
		(image, nextFrameId) = ResourceManager.getFrame(self._mediaId, self._currentFrameId)
		
		messages = self._prepareMessages(self._currentFrameId, image)

		for fragment in messages:
			try:
				self._dataSocket.send(fragment)
			# Sometimes a 'no route to host' error happens, but we can just ignore it and keep trying again
			except OSError:
				pass
		
		self._currentFrameId = nextFrameId