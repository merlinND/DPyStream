# -*-coding:Utf-8 -*

from handlers.UdpPushHandler import *
from MultiCastUdpSocket import *

class MultiCastPushHandler(UdpPushHandler):
	"""
	A MultiCastPushHandler is almost identical to a normal UdpPushHandler except that when it continuously sends out its data through a MultiCastUdpSocket.
	"""

	def __init__(self):
		"""
		There is no command socket here, we simply continuously send out our data.
		"""
		UdpPushHandler.__init__(self, commandSocket)

		# We don't need any keep-alive mechanism
		self._aliveTimer.cancel()
		self._isAliveTimerRunning = False
		# But we start pushing the content immediately
		PushHandler.startPushing(self)

	def _sendCurrentFrame(self):
		"""
		Sends the current image (based on currentFrameId) to anyone who listens through a MultiCastUdpSocket.
		"""
		(image, nextFrameId) = ResourceManager.getFrame(self._mediaId, self._currentFrameId)
		
		print("Sending frame #{} next frame will be #{}.".format(self._currentFrameId, nextFrameId))
		messages = self._prepareMessages(self._currentFrameId, image)

		# We create a UDP socket just for this occasion
		socket = MultiCastUdpSocket(None, self._clientIp, self._clientListenPort)
		for fragment in messages:
			socket.send(fragment)
		
		self._currentFrameId = nextFrameId