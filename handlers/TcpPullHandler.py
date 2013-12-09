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
		command = b''
		while command != b'e' and not self.interruptFlag:
			# TODO: send the catalog only one per message received (not per single caracter)
			command = self.socket.receive(1)
			
			if command != b'e':
				ignoredCharacters = (b'\n', b'\r', b'')
				if command not in ignoredCharacters:
					print(command, ' received, sending catalog.')
					self.socket.send(Catalog.asHttp())
			else:
				print(command, ' received, closing connection.')
				self.socket.send(b'The connection is going down now.')
				self.socket.close()