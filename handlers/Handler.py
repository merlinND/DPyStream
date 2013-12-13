# -*-coding:Utf-8 -*
from threading import Thread

# Common vocabulary for all requests
GET_COMMAND = "GET "
END_COMMAND = "END"
END_LINE = "\r\n"

class Handler(Thread):
	
	def __init__(self):
		Thread.__init__(self)
		self.interruptFlag = False
	
	def kill(self):
		self.interruptFlag = True

	def run(self):
		print("Handler ready.")
		self.receiveCommand()

	def _interpretCommand(self, command):

		# TODO : fix connection closing
		if END_COMMAND == command:
			# Empty line necessary
			print("Waiting for blank line...")
			if "" == self.commandSocket.nextLine():
				self.kill()
				print("Connection closed.")