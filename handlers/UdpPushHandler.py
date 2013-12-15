# -*-coding:Utf-8 -*

import ResourceManager

from UdpSocket import *
from handlers.UdpHandler import *

class UdpPushHandler(UdpHandler):
	"""
	This class is able to manage connections from clients who are interested in getting a UDP Push connection.
	"""
	def __init__(self, commandSocket, protocol):
		UdpHandler.__init__(self, commandSocket, protocol)
		print("UpdPushHandler OK")
