﻿# -*-coding:Utf-8 -*
import Catalog
from handlers.Handler import *

class CatalogHandler(Handler):
	"""
	This class is able to manage connections from clients who are
	interested in getting the catalog.
	"""
	
	def __init__(self, commandSocket, protocol):
		Handler.__init__(self, protocol)
		self._commandSocket = commandSocket
		
	def run(self):
		print("Running the new thread")
		self.receiveCommand()
	
	def kill(self):
		self._interruptFlag = True
		# We inform the commandSocket that we want it to commit
		# suicide
		self._commandSocket.kill()

	def receiveCommand(self):
		command = b''
		while command != b'e' and not self._interruptFlag:
			# TODO: send the catalog only one per message
			# received (not per single caracter)
			command = self._commandSocket.receive(1)
			
			if command != b'e':
				ignoredCharacters = (b'\n', b'\r', b'')
				if command not in ignoredCharacters:
					print(command, ' received, sending catalog.')
					self._commandSocket.send(Catalog.asHttp())
			else:
				print(command, ' received, closing connection.')
				self.kill()