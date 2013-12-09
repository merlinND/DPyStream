#!/usr/local/bin/ python3.3
# -*-coding:Utf-8 -*
from threading import Thread
import select

from CatalogHandler import *
from TcpSocket import *

class SocketManager(Thread):
	"""
	HttpAcceptHandler represents the thread receiving the connection requests and creating
	a new socket (and associated thread) for each client.
	"""
	
	def __init__(self, host = '127.0.0.1', port = 15000):
		Thread.__init__(self)
		self.interruptFlag = False

		self.serverSocket = TcpSocket()
		self._selectTimer = 3

		# By default, the socket is bound to 127.0.0.1 on port 15000
		self.serverSocket.listen(host, port)
		print('Listening on', host, ':', port)
		# We will maintain a list of all active connections
		self.clients = []
		
	def run(self):
		while not self.interruptFlag:
			# Thanks to select.select, the read operation regularly times out
			(readyToRead,rw,err) = select.select([self.serverSocket.s],[],[], self._selectTimer)
			if readyToRead:
				clientSocket = self.serverSocket.accept()
				# At each new connection, we create a new handler, which runs in a new thread
				# TODO : use a HandlerFactory to instanciate the right kind of handler depending on the type of socket that we are managing
				clientThread = CatalogHandler(clientSocket)

				self.clients.append(clientThread)
				clientThread.start()
				print("Connection accepted (connection #", len(self.clients), ").")
	
	def kill(self):
		print("Killing all", len(self.clients) ,"client threads...")
		print("Server will go down in", self._selectTimer ,"seconds or less.")

		# TODO : sometimes client connections go down even if we do not kill them. Purge the clients list regularly ?

		i = 0
		for client in self.clients:
			# If this thread is still running, we kindly ask it to die
			if client.is_alive():
				client.kill()
			i += 1
			print(( len(self.clients) - i), " clients still alive")
		
		# And we then kill ourself
		Handler.kill(self)
