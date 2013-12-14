# -*-coding:Utf-8 -*
from threading import Thread

def enum(**enums):
	return type('Enum', (), enums)

Protocol = enum(UDP = 'Udp', TCP = 'Tcp', MCAST = 'MultiCast')

class Handler(Thread):

	def __init__(self, protocol):
		Thread.__init__(self)
		self.protocol = protocol
		self.interruptFlag = False
		print("Initialized", self.protocol, "Handler.")

	def run(self):
		self.receiveCommand()
