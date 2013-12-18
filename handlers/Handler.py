﻿# -*-coding:Utf-8 -*
from threading import Thread

# Common vocabulary for all requests
GET_COMMAND = "GET "
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

		# TODO : these properties should come from the catalog
		self._mediaId = 5
		self._currentFrameId = 0
	
	def kill(self):
		self._interruptFlag = True

	def run(self):
		self.receiveCommand()

	def _interpretCommand(self, command):
		if END_COMMAND == command[:len(END_COMMAND)]:
			# Empty line necessary
			print("Waiting for blank line...")
			if "" == self._commandSocket.nextLine():
				self.kill()
				print("Connection closed.")