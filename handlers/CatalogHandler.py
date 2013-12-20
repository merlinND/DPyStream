# -*-coding:Utf-8 -*
import Catalog
from handlers.Handler import *

class CatalogHandler(Handler):
	"""
	This class is able to manage connections from clients who are
	interested in getting the catalog.
	"""
	
	def __init__(self, commandSocket):
		Handler.__init__(self, commandSocket)
		self._commandSocket = commandSocket
	
	def kill(self):
		self._interruptFlag = True
		# We inform the commandSocket that we want it to commit suicide
		if self._commandSocket is not None:
			self._commandSocket.kill()

	def setMediaProperties(self, properties):
		"""
		This function doesn't mean anything for a CatalogHandler, so we redefine it to make sure it doesn't break something.
		"""
		pass

	def receiveCommand(self):
		while not self._interruptFlag:
			self._commandSocket.send(Catalog.asHttp())
		self.kill()