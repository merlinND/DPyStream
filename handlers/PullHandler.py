# -*-coding:Utf-8 -*

from handlers.Handler import *

# Vocabulary for PUll requests
GET_COMMAND = "GET "
NEXT_IMAGE = -1

class PullHandler(Handler):
	"""
	This class is able to manage connections from clients who are interested in getting a media via protocol TCP_PUll or UDP_PULL.
	"""
	
	def __init__(self, commandSocket):
		"""
		The parameter 'commandSocket' holds the control connection with the client.
		The client will send commands via this connection and this is the handler's job to interpret them.
		"""
		Handler.__init__(self, commandSocket)
		
		self._mediaId = 1
		self._currentFrameId = 0

	def _interpretCommand(self, command):
		"""
		Interpret the command received from the client and respond on the dataSocket.
		"""
		if self.isCommand(command, GET_COMMAND):
			frameId = int(command[len(GET_COMMAND):])
			# There should be an empty line (but it's not that important)
			self._commandSocket.nextLine()
			
			# If we were asked for a specific frameId (otherwise just send the next one)
			if (NEXT_IMAGE != frameId):
				self._currentFrameId = frameId

			self._sendCurrentFrame()
		# If we couldn't recognized this command, maybe one of the parent class can
		else:
			# The parent says whether he interpreted the command
			return Handler._interpretCommand(self, command)

		# We say we interpreted the command
		return True