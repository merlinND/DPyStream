#!/usr/local/bin/python3.3
# -*-coding:Utf-8 -*

# Y:\3IF\RE\TP-1\src

from MySocket import *
from HttpAcceptHandler import *

serverHandler = HttpAcceptHandler(MySocket(2))
serverHandler.start()

dummy = input("Press enter to shutdown server...")
# Après que l'administrateur du serveur ait appuyé sur une touche
# On ferme toutes les connexions et on quitte l'application
serverHandler.kill()