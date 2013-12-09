#!/usr/local/bin/ python3.3
# -*-coding:Utf-8 -*

from handlers import *

class HandlerFactory:
	"""
	HandlerFactory is responsible to deliver an instance of the right Handler class when given a connection port.
	Indeed, each media parsed by Catalog has its own connection type (TCP_PULL, UDP_PUSH, etc) and its own listening port. Thus for each connection port, we must use an appropriate Handler object.
	Example: a media declares to use port 42000 for an UDP_PULL connection. HandlerFactory.getAppropriateHandler(42000) should thus return a new instance of UdpPullHandler.
	"""
	def __init__(self, connectionTypes):
		"""
		connectionTypes should be a dictionnary associating each used port to its connection type, expressed as a string ('TCP_PULL', 'UDP_PULL', etc).
		"""
		# We map the given strings to the actual Handler classes
		self._connectionTypes = {};
		for connection in connectionTypes:
			if connection.type == 'CATALOG':
				self._connectionTypes[connection.port] = CatalogHandler;
			elif connection.type == 'TCP_PULL':
				self._connectionTypes[connection.port] = TcpPullHandler;
			else:
				raise Exception("The connection type {} is not supported.".format(connection.type))

	def getAppropriateHandler(self, port):
		"""
		Returns a new instance of the right kind of Handler for this port, as specified by self._connectionTypes.
		Example: a media declares to use port 42000 for an UDP_PULL connection. HandlerFactory.getAppropriateHandler(42000) should thus return a new instance of UdpPullHandler.
		"""
		return self._connectionTypes[port]()