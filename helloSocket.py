#!/usr/local/bin/python3.3
# -*-coding:Utf-8 -*

# Y:\3IF\RE\TP-1\src
import os

from HttpSocket import *
from HttpAcceptHandler import *

serverHandler = HttpAcceptHandler(HttpSocket(10))
serverHandler.start()

os.system("pause")
# Après que l'administrateur du serveur ait appuyé sur une touche
# On ferme toutes les connexions et on quitte l'application
serverHandler.kill()