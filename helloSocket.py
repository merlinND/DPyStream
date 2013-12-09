#!/usr/local/bin/python3.3
# -*-coding:Utf-8 -*

# Y:\3IF\RE\TP-1\src

import Catalog
from handlers import HandlerFactory
from TcpSocket import *
from SocketManager import *

(catalogAddress, catalogPort) = Catalog.parse('catalog/startup.txt')
connectionTypes = Catalog.getConnectionTypes()

HandlerFactory.setConnectionTypes(connectionTypes)

# TODO : instanciate one SocketManager per media (it will accept new connections)
# Start the server that will serve the catalog
catalogServer = SocketManager(catalogAddress, catalogPort)
catalogServer.start()

dummy = input("Press enter to shutdown server...")
# Once any input was given, we start closing down the connections
# The script will end when all the connections are released
catalogServer.kill()
