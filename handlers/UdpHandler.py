# -*-coding:Utf-8 -*
from threading import Timer

import ResourceManager
from handlers.Handler import *
from UdpSocket import *

# Common vocabulary for UDP requests
# TODO: put all commands in an enum?
# TODO: create function to test for commands easily (rather than always use GET_COMMAND == command[:len(GET_COMMAND)])
GET_COMMAND = "GET "
LISTEN_COMMAND = "LISTEN_PORT "

FRAGMENT_COMMAND = "FRAGMENT_SIZE "

# Done for all UDP connections so that if the END command is not sent, the connection is closed at some point.
KEEP_ALIVE = "ALIVE "
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
		self._fragmentSize = None

		# If the keep-alive wasn't sent after 60 seconds, we commit suicide.
		self._aliveTimer = Timer(ALIVE_TIMEOUT, self.kill)
		self._isAliveTimerRunning = True

	def kill(self):
		"""
		Properly closes all sockets and interrupts the thread.
		"""
		self._interruptFlag = True
		# We inform the sockets that we want them to commit suicide
		self._commandSocket.kill()

	def restartTimer(self):
		self._aliveTimer.cancel()
		self._aliveTimer = Timer(ALIVE_TIMEOUT, self.kill)

	def _interpretCommand(self, command):
		"""
		Interpret the command received from the client and
		respond on the dataSocket.
		"""
		# The GET command could mean either "setup" or "send a frame"
		if None == self._fragmentSize and GET_COMMAND == command[:len(GET_COMMAND)]:
			self.setupClientContact()
			# If we needed to "send a frame", we let PushHandler or PullHandler take care of it
		# If we couldn't recognized this command, maybe one of
		# the parent class can
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
		if LISTEN_COMMAND == command[:len(LISTEN_COMMAND)]:
		   # No empty line sent ? and "" == self._commandSocket.nextLine():
			self._clientIp = self._commandSocket.getIp()
			self._clientListenPort = int(command[len(LISTEN_COMMAND):])

			command = self._commandSocket.nextLine()
			self._fragmentSize = int(command[len(FRAGMENT_COMMAND):])

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

		# TODO : prepare the message
		messages = []

		totalFrameSize = str(len(frameContent))
		remainingSize = len(frameContent)
		fragmentNumber = 0
		while remainingSize > 0:
			if remainingSize >= self._fragmentSize:
				thisFragmentSize = self._fragmentSize
			else:
				thisFragmentSize = remainingSize

			message = str(frameId) + END_LINE\
				 	+ totalFrameSize + END_LINE\
				 	+ str(fragmentNumber) + END_LINE\
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
		Sends the current image (based on currentFrameId) to the client through the dataSocket.
		"""
		(image, nextFrameId) = ResourceManager.getFrame(self._mediaId, self._currentFrameId)
		
		print("Sending frame #{} next frame will be #{}.".format(self._currentFrameId, nextFrameId))
		messages = self._prepareMessages(self._currentFrameId, image)

		# We create a UDP socket just for this occasion
		socket = UdpSocket(None, self._clientIp, self._clientListenPort)
		for fragment in messages:
			socket.send(fragment)

		self._currentFrameId = nextFrameId