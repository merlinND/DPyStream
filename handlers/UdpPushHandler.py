# -*-coding:Utf-8 -*

import ResourceManager

from UdpSocket import *
from handlers.Handler import *
#from handlers.UdpHandler import *

class UdpPushHandler(Handler):
	"""
	This class is able to manage connections from clients who are interested in getting a UDP Push connection.
	"""
	def __init__(self):
		print("UpdPushHandler OK")
