# -*-coding:Utf-8 -*

from handlers.TcpHandler import *
from handlers.PullHandler import *

class TcpPullHandler(TcpHandler, PullHandler):
	"""
	This class is able to manage connections from clients who are interested in getting a TCP_PULL connection.
	"""
	
	def __init__(self, commandSocket):
		"""
		The parameter 'commandSocket' holds the TCP control connection with the client.
		The client will send commands via this connection and this is the handler's job to interpret them.
		"""
		TcpHandler.__init__(self, commandSocket)
		PullHandler.__init__(self, commandSocket)

	def _interpretCommand(self, command):
		"""
		Receive a command from the client on the control socket
		and interpret it.
		"""
		tcpInterpreted = TcpHandler._interpretCommand(self, command)
		# If the TcpHandler cannot interpret this command
		if not tcpInterpreted:
			pullIntrepreted = PullHandler._interpretCommand(self, command)

		# The parent says whether we interpreted the command
		return tcpInterpreted or pullIntrepreted

	def kill(self):
		TcpHandler.kill(self)
		PullHandler.kill(self)