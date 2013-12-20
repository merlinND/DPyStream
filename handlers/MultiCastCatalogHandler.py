# -*-coding:Utf-8 -*
from threading import Timer

import Catalog
from handlers.Handler import *
from sockets.MultiCastUdpSocket import *

DEFAULT_CATALOG_SEND_INTERVAL = 3

class MultiCastCatalogHandler(Handler):
	"""
	This class is able to manage connections from clients who are interested in getting the catalog via multicast.
	"""
	
	def __init__(self, address, port, interval = DEFAULT_CATALOG_SEND_INTERVAL):
		# Actually we don't use any command socket, since we're doing multicast
		Handler.__init__(self, None)
		self._destinationAddress = address
		self._destinationPort = port

		# Interval (in seconds) at which we will send out the catalog
		self._interval = interval
		self._sendTimer = None
		self._isTimerRunning = True

	def run(self):
		self._dataSocket = MultiCastUdpSocket(None, self._destinationAddress, self._destinationPort)
		self.startTimer()
		
	def kill(self):
		Handler.kill(self)
		if self._sendTimer is not None:
			self._sendTimer.cancel()

	def startTimer(self):
		if self._sendTimer is not None and self._isTimerRunning:
			self._sendTimer.cancel
		self._sendTimer = Timer(self._interval, self.sendCatalog)
		if not self._interruptFlag:
			self._sendTimer.start()
			self._isTimerRunning = True

	def setMediaProperties(self, properties):
		"""
		This function doesn't mean anything for a CatalogHandler, so we redefine it to make sure it doesn't break something.
		"""
		pass

	def sendCatalog(self):
		self._isTimerRunning = False
		self._dataSocket.send(Catalog.asText())
		self.startTimer()