# -*-coding:Utf-8 -*
from threading import Thread

# Common vocabulary for all requests
END_COMMAND = "END"
END_LINE = "\r\n"

class Handler(Thread):

	def __init__(self, commandSocket):
		Thread.__init__(self)
		self._interruptFlag = False

		self._commandSocket = commandSocket
		self._dataSocket = None
		self._clientIp = None
		self._clientListenPort = None

		self._currentFrameId = 0
		# These properties will be set with values coming from the catalog
		self._mediaId = None
		self._ips = None
	
	def setMediaProperties(self, properties):
		self._mediaId = properties['id']
		self._ips = properties['ips']

	def kill(self):
		self._interruptFlag = True

	def receiveCommand(self):
		"""
		Receive a command from the client on the control socket and interpret it.
		"""
		while not self._interruptFlag:
			command = self._commandSocket.nextLine()

			if None == command:
				continue
			else:
				self._interpretCommand(command)

	def isCommand(self, text, command):
		"""
		Tests if the text passed starts with the given command.
		This is a simple helper function.
		"""
		return (command == text[:len(command)])

	def run(self):
		self.receiveCommand()

	def _interpretCommand(self, command):
		if self.isCommand(command, END_COMMAND):
			# Empty line necessary
			if "" == self._commandSocket.nextLine():
				self.kill()
				print("Connection with client {}:{} closed.".format(self._clientIp, self._clientListenPort))
				return True
		return False # We couldn't interpret the command