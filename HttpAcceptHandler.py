#!/usr/local/bin/ python3.3
# -*-coding:Utf-8 -*
import select

from Handler import *
from ClientHandler import *

class HttpAcceptHandler(Handler):
	"""Cette classe représente le thread recevant les demandes de connexion et créant un nouveau socket (et thread associé) par client."""
	
	def __init__(self, serverSocket):
		Handler.__init__(self)
		self.serverSocket = serverSocket
		self._selectTimer = 3

		# Par défaut, le socket est bindé à 127.0.0.1 et écoute sur le port 15000 en TCP
		self.serverSocket.listen()
		
		# On maintiendra une liste de tous nos threads clients
		self.clients = []
		
	def run(self):
		while not self.interruptFlag:
			# Grâce à select.select, le interrupt flag peut arrêter l'attente
			(readyToRead,rw,err) = select.select([self.serverSocket.s],[],[], self._selectTimer)
			if readyToRead:
				clientSocket = self.serverSocket.accept()
				# A chaque nouvelle connexion, on crée un nouveau thread
				clientThread = ClientHandler(clientSocket)
				# On ajoute le thread à notre liste
				self.clients.append(clientThread)
				clientThread.start()
				print("Connection accepted (connection #", len(self.clients), ").")
	
	def kill(self):
		print("Killing all", len(self.clients) ,"client threads...")
		print("Server will go down in", self._selectTimer ,"seconds or less.")
		# TODO : purger la liste au fur et à mesure ? (pour ne pas occuper trop de mémoire pour rien)
		# Pour chaque thread client
		i = 0
		for client in self.clients:
			# Si le thread n'est pas déjà terminé, on le kill
			if client.is_alive():
				client.kill()
			i += 1
			print(( len(self.clients) - i), " clients still alive")
		
		# Puis on se suicide
		Handler.kill(self)
