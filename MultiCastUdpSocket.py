# -*-coding:Utf-8 -*
from GenericSocket import *
from UdpSocket import *

class MultiCastUdpSocket(UdpSocket):
	"""
	MultiCastUdpSocket implements our high level methods to send and
	receive information.
	Note: all MultiCastUdpSocket instances share the same commonSocket
	Most methods are exactly the same as for a standard UdpSocket except for the initialization.
	"""

	def __init__(self, s, host, port):
		"""
		s is the underlying socket instance (given by the UdpAccepter)
		Note: all MultiCastUdpSocket instances share the same commonSocket
		client is a simple object containing the client host address and its receive port.
		"""
		GenericSocket.__init__(self)
		if s is None:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
			self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
			self.s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
		else:
			self.s = s
		
		# Which client is allowed to communicate with us
		# (others are ignored)
		self.clientHost = host
		self.clientPort = port