# -*-coding:Utf-8 -*

# Y:\3IF\RE\TP-1\src

import Catalog
from handlers import HandlerFactory
from handlers.MultiCastCatalogHandler import *
from sockets.TcpSocket import *
from sockets.SocketManager import *

(serverAddress, catalogPort) = Catalog.parse('catalog/startup.txt')
Catalog.addMediaToResourceManager()

connectionProperties = Catalog.getConnectionProperties()
HandlerFactory.setConnectionProperties(connectionProperties)

# Instanciate one SocketManager per media + one for the catalog
# (these will accept all new control connections)
servers = []
for properties in connectionProperties:
	server = SocketManager(serverAddress, properties['port'], properties['protocol'])
	server.start()
	servers.append(server)

# Instanciate one more to serve the catalog via multicast
multiCastCatalogHandler = MultiCastCatalogHandler('225.6.7.8', 4567)
multiCastCatalogHandler.start()

input("Press enter to shutdown server...\r\n")
# Once any input was given, we start closing down the connections
# The script will end when all the connections are released
multiCastCatalogHandler.kill()
for server in servers:
	server.kill()