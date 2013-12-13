# -*-coding:Utf-8 -*
from threading import Timer
from handlers.TcpHandler import *

# Vocabulary for TCP_PUSH requests
START_COMMAND = "START"
PAUSE_COMMAND = "PAUSE"

class TcpPushHandler(TcpHandler):
	"""
	This class is able to manage connections from clients who are interested in getting a media via protocol TCP_PUSH.
	"""
	
	def __init__(self, commandSocket):
		"""
		The parameter 'socket' holds the TCP control connection with the client. The client will send commands via this connection and this is the handler's job to interpret them.
		"""
		TcpHandler.__init__(self, commandSocket)
		
		self._mediaId = 1
		self._currentFrameId = 0
		self._interval = 1 # Interval in seconds (replace with framerate from catalog?)
		
		# We create a new timer (no autostart)
		self._isTimerRunning = False
		self._pushTimer = None

	def kill(self):
		self.stopPushing()
		TcpHandler.kill(self)

	def startPushing(self):
		self._pushTimer = Timer(self._interval, self._sendCurrentFrame)
		self._pushTimer.start()
		self._isTimerRunning = True

	def restartTimer(self, autostart):
		if self._isTimerRunning:
			self._pushTimer.cancel()

		self.startPushing()

	def stopPushing(self):
		if self._pushTimer is not None:
			self._pushTimer.cancel()
		self._isTimerRunning = False

	def _sendCurrentFrame(self):
		# The timer just timed out (thus this function was called)
		self._isTimerRunning = False

		TcpHandler._sendCurrentFrame(self)

		# We restart the timer
		self.restartTimer(True)

	def _interpretCommand(self, command):
		"""
		Interpret the command received from the client and respond on the dataSocket.
		"""

		print("TcpPushHandler trying to interpret", command)

		# The GET command could only mean "establish connection"
		if GET_COMMAND == command[:len(GET_COMMAND)]:
			if None == self._dataSocket:
				self._establishMediaConnection()
			
		if START_COMMAND == command[:len(START_COMMAND)]:
			# Empty line necessary
			print("Waiting for blank line...")
			if "" == self.commandSocket.nextLine():
				self.startPushing()

		if PAUSE_COMMAND == command[:len(PAUSE_COMMAND)]:
			# Empty line necessary
			print("Waiting for blank line...")
			if "" == self.commandSocket.nextLine():
				self.stopPushing()

		else:
			# If we couldn't recognized this command, maybe one of the parent class can
			TcpHandler._interpretCommand(self, command)

