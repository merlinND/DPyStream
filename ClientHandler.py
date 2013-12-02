#!/usr/local/bin/python3.3
# -*-coding:Utf-8 -*
import Catalog
from Handler import *

class ClientHandler(Handler):
	"""Cette classe représente le thread recevant les commandes du client, et lui répondant. On a donc un thread par connexion active avec un client."""
	
	def __init__(self, clientSocket):
		Handler.__init__(self)
		self.clientSocket = clientSocket
		
	def run(self):
		print("Running the new thread")
		self.receiveCommand()
	
	def kill(self):
		self.interruptFlag = True
		# On informe aussi le socket qu'il doit se tuer
		self.clientSocket.kill()

	def receiveCommand(self):
		command = b''
		while command != b'e' and not self.interruptFlag:
			command = self.clientSocket.receive()
			
			if command != b'e':
				ignoredCharacters = (b'\n', b'\r', b'')
				if command not in ignoredCharacters:
					print(command, ' received, sending catalog.')
					self.clientSocket.send(Catalog.asHttp())
			else:
				print(command, ' received, closing connection.')
				self.clientSocket.send(b'The connection is going down now.')
				self.clientSocket.close()