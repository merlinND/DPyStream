# -*-coding:Utf-8 -*

import ResourceManager
from handlers.Handler import *
from UdpSocket import *

# Common vocabulary for TCP requests
LISTEN_COMMAND = "LISTEN_PORT "
NEXT_IMG = -1

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

		# TODO : keep-alive mechanism
		print("UdpHandler ready")

	def kill(self):
		"""
		Properly closes all sockets and interrupts the thread.
		"""
		self._interruptFlag = True
		# We inform the sockets that we want them to commit suicide
		# Note: dataSocket must be closed first as the client
		# closes the connection from its side
		if None != self._dataSocket:
			self._dataSocket.kill()
		self._commandSocket.kill()

	def receiveCommand(self):
		"""
		Receive a command from the client on the control socket
		and interpret it.
		"""
		while not self._interruptFlag:
			command = self._commandSocket.nextLine()
			print('"{}" received'.format(command))
			if None == command:
				continue
			else:
				self._interpretCommand(command)

	def _interpretCommand(self, command):
		"""
		Interpret the command received from the client and
		respond on the dataSocket.
		"""

		# TODO : interpret actual UDP commands
		if False:
			pass
		# If we couldn't recognized this command, maybe one of
		# the parent class can
		else:
			Handler._interpretCommand(self, command)

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

		message = b''
		return message

	def _sendCurrentFrame(self):
		"""
		Sends the current image (based on currentFrameId) to the client through the dataSocket.
		"""
		(image, nextFrameId) = ResourceManager.getFrame(self._mediaId, self._currentFrameId)
		

		print("Sending frame {} next frame will be #{}.".format(self._currentFrameId, nextFrameId))
		messages = self._prepareMessages(self._currentFrameId, image)
		for message in messages:
			self._dataSocket.send(message)

		self._currentFrameId = nextFrameId