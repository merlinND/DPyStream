# -*-coding:Utf-8 -*

from handlers.UdpHandler import *
from handlers.PushHandler import *

class UdpPushHandler(UdpHandler, PushHandler):
	"""
	This class is able to manage connections from clients who are interested in getting a media via protocol UDP_PUSH.
	"""
	def __init__(self, commandSocket):
		"""
		The parameter 'commandSocket' holds the UDP control connection with the client.
		The client will send commands via this connection and this is the handler's job to interpret them.
		"""
		UdpHandler.__init__(self, commandSocket)
		PushHandler.__init__(self, commandSocket)

	def _interpretCommand(self, command):
		"""
		Receive a command from the client on the control socket and interpret it.
		"""
		udpInterpreted = UdpHandler._interpretCommand(self, command)
		# If the UdpHandler cannot interpret this command
		if not udpInterpreted:
			pushIntrepreted = PushHandler._interpretCommand(self, command)

		# The parent says whether we interpreted the command
		return udpInterpreted or pushIntrepreted

	def kill(self):
		UdpHandler.kill(self)
		PushHandler.kill(self)