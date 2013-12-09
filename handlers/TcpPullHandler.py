# -*-coding:Utf-8 -*

from handlers.Handler import *

class TcpPullHandler(Handler):
	"""
	This class is able to manage connections from clients who are interested in getting a TCP Pull connection.
	"""
	
	def __init__(self, socket):
		Handler.__init__(self)
		self.socket = socket
		
	def run(self):
		print("Running the new thread")
		self.receiveCommand()
	
	def kill(self):
		self.interruptFlag = True
		# We inform the socket that we want it to commit suicide
		self.socket.kill()

	def receiveCommand(self):
		for l in self.socket.readlines():
			if ("GET " == l[:4]):
				print ("Receive a GET command!!!")
