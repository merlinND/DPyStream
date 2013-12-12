# -*-coding:Utf-8 -*
from threading import Timer
from handlers.Handler import *
import ResourceManager

# TODO : make this constant globally accessible across the application
ENDL = b'\n\r'

class TcpPushHandler(Handler):
	"""
	This class is able to manage connections from clients who are interested in getting a media via protocol TCP_PUSH.
	"""
	
	def __init__(self, socket):
		"""
		The parameter socket holds the TCP control connection with the client. The client will send commands via this connection and this is the handler's job to interpret them.
		"""
		Handler.__init__(self)
		# TODO : put most of the logic back up in the Handler parent class
		self.socket = socket

		# TODO : these properties should come from the catalog
		self._mediaId = 1
		self._currentFrameId = 0
		self._interval = 1 # Interval in seconds (replace with framerate from catalog?)
		
		# We create a new timer (no autostart)
		self._isTimerRunning = False
		self.restartTimer(False)
		
	def run(self):
		print("Running the new thread")
		self.receiveCommand()
	
	def kill(self):
		self.interruptFlag = True
		self.stopPushing()
		# We inform the socket that we want it to commit suicide
		self.socket.kill()

	def receiveCommand(self):
		command = b''
		while command != b'e' and not self.interruptFlag:
			# TODO: use common receiveCommand method from the parent Handler class instead
			command = self.socket.receive(1)
			
			if command != b'e':
				ignoredCharacters = (b'\n', b'\r', b'')
				if command not in ignoredCharacters:
					print('Command received, we should interpret it.')
					# TODO : create a new connection to the client, on the port it specified (content chanel)
					self.startPushing()
			else:
				print(command, ' received, closing connection.')
				self.socket.send(b'The connection is going down now.')
				self.socket.close()

	def startPushing(self):
		if not self._isTimerRunning:
			self._pushTimer.start()
			self._isTimerRunning = True

	def restartTimer(self, autostart):
		if self._isTimerRunning:
			self._pushTimer.cancel()
		self._pushTimer = Timer(self._interval, self.sendNextFrame)
		if autostart:
			self._pushTimer.start()
		self._isTimerRunning = autostart

	def stopPushing(self):
		self._pushTimer.cancel()
		self._isTimerRunning = False

	def sendNextFrame(self):
		# The timer just timed out (because we were just called)
		self._isTimerRunning = False

		frameId = self._currentFrameId
		(frame, self._currentFrameId) = ResourceManager.getFrame(self._mediaId, self._currentFrameId)
		frame = bytes(frame)

		# TODO : actually send the frame to the client *on the content chanel*, not the control chanel
		print("Sending frame {} next frame will be #{}.".format(frameId, self._currentFrameId))

		# We restart the timer
		self.restartTimer(True)

	def prepareMessage(self, frameId, frameContent):
		"""
		This function takes an image and adds surrounding information so that the client applications can interpret it.
		It returns a full message ready to be sent to the client via socket, containing:
		- This frame's id (followed by endline)
		- This frame's content size (followed by endline)
		- The actual frame content
		"""
		return bytes(str(frameId), 'Utf-8') + ENDL\
			 + bytes(str(len(frameContent)), 'Utf-8') + ENDL\
			 + frameContent
