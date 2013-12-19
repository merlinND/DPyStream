# -*-coding:Utf-8 -*

from handlers.UdpPushHandler import *
from MultiCastUdpSocket import *

class MultiCastPushHandler(UdpPushHandler):
	"""
	A MultiCastPushHandler is almost identical to a normal UdpPushHandler except that when it continuously sends out its data through a MultiCastUdpSocket.
	"""

	def __init__(self, commandSocket):
		"""
		There is no need for a command socket here, we simply continuously send out our data.
		"""
		UdpPushHandler.__init__(self, commandSocket)
		self._dataSocket = None

		# We don't need any keep-alive mechanism
		self._aliveTimer.cancel()
		self._isAliveTimerRunning = False
		# We can choose our own fragment size
		self._fragmentSize = 512 - MAX_HEADER_SIZE

	
	def setMediaProperties(self, properties):
		UdpPushHandler.setMediaProperties(self, properties)
		# The "client" ip and port are actually the destination described in the catalog
		self._clientIp = properties['address']
		self._clientListenPort = properties['port']

		# Now that we know where to send the stuff, we can create a socket
		self._dataSocket = MultiCastUdpSocket(None, self._clientIp, self._clientListenPort)
		# And we can start pushing the content immediately
		PushHandler.startPushing(self)

	def kill(self):
		UdpPushHandler.kill(self)

	def receiveCommand(self):
		"""
		MultiCast threads do not receive anything.
		"""
		pass

	def _interpretCommand(self, command):
		"""
		MultiCast threads do not receive anything.
		"""
		pass