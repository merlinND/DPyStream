# -*-coding:Utf-8 -*
from threading import Thread

# Common vocabulary for all requests
GET_COMMAND = "GET "
END_COMMAND = "END"
END_LINE = "\r\n"

def enum(**enums):
	return type('Enum', (), enums)

Protocol = enum(UDP = 'Udp', TCP = 'Tcp', MCAST = 'MultiCast')

class Handler(Thread):

	def __init__(self, protocol):
		Thread.__init__(self)
		self.protocol = protocol
		self._interruptFlag = False

		print("Initialized", self.protocol, "Handler.")
	
	def kill(self):
		self._interruptFlag = True

	def run(self):
		self.receiveCommand()

	def _interpretCommand(self, command):
		if END_COMMAND == command[:len(END_COMMAND)]:
			# Empty line necessary
			print("Waiting for blank line...")
			if "" == self.commandSocket.nextLine():
				self.kill()
				print("Connection closed.")