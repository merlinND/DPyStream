# -*-coding:Utf-8 -*

from handlers.UdpHandler import *
from handlers.PullHandler import *

class UdpPullHandler(UdpHandler, PullHandler):
	"""
	This class is able to manage connections from clients who are interested in getting a UDP_PULL connection.
	"""
	
	def __init__(self, commandSocket):
		UdpHandler.__init__(self, commandSocket)
		PullHandler.__init__(self, commandSocket)

	def _interpretCommand(self, command):
		"""
		Receive a command from the client on the control socket
		and interpret it.
		"""
		udpInterpreted = UdpHandler._interpretCommand(self, command)
		# If the UdpHandler cannot interpret this command
		if not udpInterpreted:
			pullIntrepreted = PullHandler._interpretCommand(self, command)

		# The parent says whether we interpreted the command
		return udpInterpreted or pullIntrepreted

	def kill(self):
		UdpHandler.kill(self)
		PullHandler.kill(self)