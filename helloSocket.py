#!/usr/local/bin/python3.3
# -*-coding:Utf-8 -*

# Y:\3IF\RE\TP-1\src

import Catalog
from MySocket import *
from HttpAcceptHandler import *


(catalogAddress, catalogPort) = Catalog.parse('catalog/startup.txt') 

# Start the server that will serve the catalog
catalogServerHandler = HttpAcceptHandler(MySocket(10), catalogAddress, catalogPort)
catalogServerHandler.start()

dummy = input("Press enter to shutdown server...")
# Once any input was given, we start closing down the connections
# The script will end when all the connections are released
catalogServerHandler.kill()