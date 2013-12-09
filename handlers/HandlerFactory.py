#!/usr/local/bin/ python3.3
# -*-coding:Utf-8 -*
"""
HandlerFactory is responsible to deliver an instance of the right Handler class when given a connection port.
Indeed, each media parsed by Catalog has its own connection type (TCP_PULL, UDP_PUSH, etc) and its own listening port. Thus for each connection port, we must use an appropriate Handler object.
Example: a media declares to use port 42000 for an UDP_PULL connection. HandlerFactory.createAppropriateHandler(42000) should thus return a new instance of UdpPullHandler.
"""
from handlers.CatalogHandler import *

_connectionTypes = {};

def setConnectionTypes(connectionTypes):
	"""
	connectionTypes should be a dictionnary associating each used port to its connection type, expressed as a string ('TCP_PULL', 'UDP_PULL', etc).
	"""
	# We map the given strings to the actual Handler classes
	for port in connectionTypes:
		thisType = connectionTypes[port]

		if thisType == 'CATALOG':
			_connectionTypes[port] = CatalogHandler;
		elif thisType == 'TCP_PULL':
			_connectionTypes[port] = None; #TcpPullHandler;
		elif thisType == 'TCP_PUSH':
			_connectionTypes[port] = None; #TcpPushHandler;
		elif thisType == 'UDP_PULL':
			_connectionTypes[port] = None; #UdpPullHandler;
		elif thisType == 'UDP_PUSH':
			_connectionTypes[port] = None; #UdpPushHandler;
		elif thisType == 'MCAST_PUSH':
			_connectionTypes[port] = None; #MulticastPushHandler;
		else:
			raise Exception("The connection type {} is not supported.".format(thisType))

def createAppropriateHandler(port, socket):
	"""
	Returns a new instance of the right kind of Handler for this port, as specified by _connectionTypes.
	Example: a media declares to use port 42000 for an UDP_PULL connection. HandlerFactory.createAppropriateHandler(42000) should thus return a new instance of UdpPullHandler.
	"""
	try:
	 	return _connectionTypes[port](socket)
	except KeyError:
		# TODO : fail gracefully
		raise Exception("No connection is available on this port.")