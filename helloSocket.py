﻿#!/usr/local/bin/python3.3
# -*-coding:Utf-8 -*

# Y:\3IF\RE\TP-1\src

from HttpSocket import *
from HttpAcceptHandler import *

serverHandler = HttpAcceptHandler(HttpSocket(10))
serverHandler.start()

dummy = input("Press enter to shutdown server...")
# Après que l'administrateur du serveur ait appuyé sur une touche
# On ferme toutes les connexions et on quitte l'application
serverHandler.kill()