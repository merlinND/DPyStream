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
			print("Command:", command)

			if None == command:
				continue
			else:
				self._interpretCommand(command)

	def run(self):
		self.receiveCommand()

	def _interpretCommand(self, command):
		if END_COMMAND == command[:len(END_COMMAND)]:
			# Empty line necessary
#			print("Waiting for blank line...")
			if "" == self._commandSocket.nextLine():
				self.kill()
				print("Connection closed.")
				return True
		return False # We couldn't interpret the command