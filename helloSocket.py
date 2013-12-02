#!/usr/local/bin/python3.3
# -*-coding:Utf-8 -*

# Y:\3IF\RE\TP-1\src

from CatalogParser import *

import ResourceManager

from MySocket import *
from HttpAcceptHandler import *

ResourceManager.addResource(
	"ID1",
	(
		"resources/1/img1.bmp",
		"resources/1/img2.bmp",
		"resources/1/img3.bmp",
		"resources/1/img4.bmp",
		"resources/1/img5.bmp"
	)
)

#catalogParser = CatalogParser()
#(catalogAddress, catalogPort) = catalogParser.parse('catalog/startup.txt') 
#print(catalogAddress, catalogPort)
#serverHandler = HttpAcceptHandler(MySocket(2))
#serverHandler.start()

dummy = input("Press enter to shutdown server...")
# Après que l'administrateur du serveur ait appuyé sur une touche
# On ferme toutes les connexions et on quitte l'application
#serverHandler.kill()
