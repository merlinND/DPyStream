# -*-coding:Utf-8 -*

# Y:\3IF\RE\TP-1\src

import Catalog
from handlers import HandlerFactory
from TcpSocket import *
from SocketManager import *

(serverAddress, catalogPort) = Catalog.parse('catalog/startup.txt')
Catalog.addMediaToResourceManager()
connectionTypes = Catalog.getConnectionTypes()

HandlerFactory.setConnectionTypes(connectionTypes)

# Instanciate one SocketManager per media + one for the catalog
# (these will accept all new TCP control connections)
servers = []
for port in connectionTypes:
	server = SocketManager(serverAddress, port)
	server.start()
	servers.append(server)

dummy = input("Press enter to shutdown server...")
# Once any input was given, we start closing down the connections
# The script will end when all the connections are released
for server in servers:
	server.kill()