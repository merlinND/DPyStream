# -*-coding:Utf-8 -*
from threading import Timer

from handlers.Handler import *

# Vocabulary for PUSH requests
START_COMMAND = "START"
PAUSE_COMMAND = "PAUSE"
NEXT_IMAGE = -1

class PushHandler(Handler):
	"""
	This class is able to manage connections from clients who are interested in getting a media via protocol TCP_PUSH.
	"""
	
	def __init__(self, commandSocket):
		"""
		The parameter 'commandSocket' holds the control connection with the client.
		The client will send commands via this connection and this is the handler's job to interpret them.
		"""
		Handler.__init__(self, commandSocket)
		
		self._mediaId = 1
		self._currentFrameId = 0
		self._interval = 1 # Interval in seconds (replace with framerate from catalog?)
		
		# We create a new timer (no autostart)
		self._isTimerRunning = False
		self._pushTimer = None

	def kill(self):
		self.stopPushing()
		Handler.kill(self)

	def startPushing(self):
		self._pushTimer = Timer(self._interval, self._sendCurrentPushFrame)
		self._pushTimer.start()
		self._isTimerRunning = True

	def restartPushTimer(self, autostart):
		if self._isTimerRunning:
			self._pushTimer.cancel()

		self.startPushing()

	def stopPushing(self):
		if self._pushTimer is not None:
			self._pushTimer.cancel()
		self._isTimerRunning = False

	def _sendCurrentPushFrame(self):
		"""
		This method only delegates the work to the real sending method (every time the timer times out).
		"""
		# The timer just timed out (thus this function was called)
		self._isTimerRunning = False

		# Asks to the real sending method to send
		self._sendCurrentFrame()

		# We restart the timer
		self.restartPushTimer(True)

	def _interpretCommand(self, command):
		"""
		Interpret the command received from the client and respond on the dataSocket.
		"""

		# The GET command could only mean "establish connection"
		if START_COMMAND == command[:len(START_COMMAND)]:
			# Empty line necessary
#			print("Waiting for blank line...")
			if "" == self._commandSocket.nextLine():
				self.startPushing()
		elif PAUSE_COMMAND == command[:len(PAUSE_COMMAND)]:
			# Empty line necessary
#			print("Waiting for blank line...")
			if "" == self._commandSocket.nextLine():
				self.stopPushing()
		# If we couldn't recognized this command, maybe one of the parent class can
		else:
			# The parent says whether he interpreted the command
			return Handler._interpretCommand(self, command)

		# We say we interpreted the command
		return True