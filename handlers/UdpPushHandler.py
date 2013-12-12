# -*-coding:Utf-8 -*

from handlers.Handler import *

from TcpSocket import *
import ResourceManager

class UdpPushHandler(Handler):
	"""
	This class is able to manage connections from clients who are interested in getting a UDP Push connection.
	"""