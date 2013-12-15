# -*-coding:Utf-8 -*

from handlers.TcpHandler import *


class TcpPullHandler(TcpHandler):
	"""
	This class is able to manage connections from clients who are interested in getting a TCP_PULL connection.
	"""
	
	def __init__(self, commandSocket, protocol):
		TcpHandler.__init__(self, commandSocket, protocol)
