# -*-coding:Utf-8 -*
import os
import socket

class HttpSocket:
	"""HttpSocket implémente nos méthodes de socket génériques."""
	
	def __init__(self, maxConnections = 5, s = None):
		if s is None:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.s = s
		self.maxConnections = maxConnections
	
	def listen(self, host = '127.0.0.1', port = 15000):
		self.s.bind((host, port)) #self.s.gethostname()
		self.s.listen(self.maxConnections)
		print("HTTP server started, will accept ", self.maxConnections, " connections at most.")
	
	def connect(self, host, port):
		self.s.connect((host, port))
	
	def close(self):
		self.s.close()
	
	def accept(self):
		(clientSocket, address) = self.s.accept()
		return HttpSocket(s = clientSocket)
	
	def send(self, message):
		totalSent = 0
		while totalSent < len(message):
			sent = self.s.send(message[totalSent:])
			if 0 == sent:
				raise RuntimeError("The HTTP Socket connection was broken.")
			totalSent += sent
	
	def receive(self):
		message = b''
		while len(message) < 1:
			# TODO : rendre le receive non bloquant
			chunk = self.s.recv(1)
			if chunk == b'':
				raise RuntimeError("The HTTP Socket connection was broken.")
			message += chunk
		return message