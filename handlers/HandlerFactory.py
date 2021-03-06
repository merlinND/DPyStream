# -*-coding:Utf-8 -*
"""
HandlerFactory is responsible to deliver an instance of the right Handler class when given a connection port.
Indeed, each media parsed by Catalog has its own connection type (TCP_PULL, UDP_PUSH, etc) and its own listening port. Thus for each connection port, we must use an appropriate Handler object.
Example: a media declares to use port 42000 for an UDP_PULL connection. HandlerFactory.createAppropriateHandler(42000) should thus return a new instance of UdpPullHandler.
"""
from handlers.Handler import *
from handlers.CatalogHandler import *
from handlers.TcpPullHandler import *
from handlers.TcpPushHandler import *
from handlers.UdpPullHandler import *
from handlers.UdpPushHandler import *
from handlers.MultiCastPushHandler import *


def enum(**enums):
	return type('Enum', (), enums)

Protocol = enum(CATALOG = 'CATALOG', TCP_PULL = 'TCP_PULL', TCP_PUSH = 'TCP_PUSH', UDP_PULL = 'UDP_PULL', UDP_PUSH = 'UDP_PUSH', MCAST_PUSH = 'MCAST_PUSH')

_connectionDescriptors = { };

def setConnectionProperties(connectionProperties):
	"""
	connectionTypes should be a dictionnary associating each used port to its connection type, expressed as a string ('TCP_PULL', 'UDP_PULL', etc).
	"""
	for properties in connectionProperties:
		port = properties['port']
		protocol = properties['protocol']

		# We map the given strings to the actual Handler classes
		handlerClass = None
		if protocol == Protocol.CATALOG:
			handlerClass = CatalogHandler
		elif protocol == Protocol.TCP_PULL:
			handlerClass = TcpPullHandler
		elif protocol == Protocol.TCP_PUSH:
			handlerClass = TcpPushHandler
		elif protocol == Protocol.UDP_PULL:
			handlerClass = UdpPullHandler
		elif protocol == Protocol.UDP_PUSH:
			handlerClass = UdpPushHandler
		elif protocol == Protocol.MCAST_PUSH:
			handlerClass = MultiCastPushHandler
		else:
			print("The connection type {} described in the catalog is not supported.".format(protocol))
			print("Server will not run.")
			exit()

		properties['handlerClass'] = handlerClass
		_connectionDescriptors[port] = properties

def createAppropriateHandler(port, socket):
	"""
	Returns a new instance of the right kind of Handler for this port, as specified by _connectionDescriptors.
	Example: a media declares to use port 42000 for an UDP_PULL connection. HandlerFactory.createAppropriateHandler(42000) should thus return a new instance of UdpPullHandler.
	"""
	try:
		theHandler = _connectionDescriptors[port]['handlerClass'](socket)
		theHandler.setMediaProperties(_connectionDescriptors[port])
		return theHandler
	except KeyError:
		# This exception is handled in SocketManager
		raise Exception("No connection is available on this port.")