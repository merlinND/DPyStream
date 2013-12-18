# -*-coding:Utf-8 -*

from UdpSocket import *
from handlers.UdpHandler import *

class UdpPushHandler(UdpHandler):
	"""
	This class is able to manage connections from clients who are interested in getting a UDP_PUSH connection.
	"""
	def __init__(self, commandSocket):
		UdpHandler.__init__(self, commandSocket)
		print("UpdPushHandler OK")
