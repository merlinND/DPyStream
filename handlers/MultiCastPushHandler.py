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

		# We don't need any keep-alive mechanism
		self._aliveTimer.cancel()
		self._isAliveTimerRunning = False
		# But we start pushing the content immediately
		PushHandler.startPushing(self)
		# We can choose our own fragment size
		self._fragmentSize = 512 - MAX_HEADER_SIZE
	
	def setMediaProperties(self, properties):
		UdpPushHandler.setMediaProperties(self, properties)
		# The "client" ip and port are actually the destination described in the catalog
		self._clientIp = properties['address']
		self._clientListenPort = properties['port']

	def _sendCurrentFrame(self):
		"""
		Sends the current image (based on currentFrameId) to anyone who listens through a MultiCastUdpSocket.
		"""
		(image, nextFrameId) = ResourceManager.getFrame(self._mediaId, self._currentFrameId)
		
		messages = self._prepareMessages(self._currentFrameId, image)

		# We create a UDP socket just for this occasion
		socket = MultiCastUdpSocket(None, self._clientIp, self._clientListenPort)
		for fragment in messages:
			socket.send(fragment)
		
		self._currentFrameId = nextFrameId

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