﻿# -*-coding:Utf-8 -*
import Catalog
from handlers.Handler import *

class CatalogHandler(Handler):
	"""
	This class is able to manage connections from clients who are interested in getting the catalog via TCP.
	"""
	
	def __init__(self, commandSocket):
		Handler.__init__(self, commandSocket)
		self._commandSocket = commandSocket

	def setMediaProperties(self, properties):
		"""
		This function doesn't mean anything for a CatalogHandler, so we redefine it to make sure it doesn't break something.
		"""
		pass

	def receiveCommand(self):
		while not self._interruptFlag:
			# Waiting for any two lines (so that the VideoClient only gets one catalog per request)
			self._commandSocket.nextLine()
			self._commandSocket.nextLine()
			self._commandSocket.send(Catalog.asHttp())
		self.kill()