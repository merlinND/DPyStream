﻿#!/usr/local/bin/python3.3
# -*-coding:Utf-8 -*

# Y:\3IF\RE\TP-1\src

import Catalog
from handlers import HandlerFactory
from TcpSocket import *
from SocketManager import *


(catalogAddress, catalogPort) = Catalog.parse('catalog/startup.txt') 
# connectionTypes = {}
# connectionTypes[catalogPort] = 'CATALOG'
# connectionTypes[42000] = 'TCP_PULL'

# testFactory = HandlerFactory(connectionTypes)
# testHandler = testFactory.getAppropriateHandler(catalogPort)
# print(testHandler)
# testHandler = testFactory.getAppropriateHandler(42000)
# print(testHandler)

# Start the server that will serve the catalog
catalogServerHandler = SocketManager(catalogAddress, catalogPort)
catalogServerHandler.start()

dummy = input("Press enter to shutdown server...")
# Once any input was given, we start closing down the connections
# The script will end when all the connections are released
# catalogServerHandler.kill()
