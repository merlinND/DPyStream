#!/usr/local/bin/python3.3
# -*-coding:Utf-8 -*
import socket
import select

class HttpSocket:
	"""HttpSocket implémente nos méthodes de socket génériques."""
	
	def __init__(self, maxConnections = 5, s = None):
		if s is None:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.s = s
		# Ces options permettent notamment de réutiliser le même port plus tard
		# (par exemple, lors de deux exécutions consécutives)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.maxConnections = maxConnections
		self._selectTimer = 3
		self.interruptFlag = False
	
	def listen(self, host = '127.0.0.1', port = 15000):
		self.s.bind((host, port)) #self.s.gethostname()
		self.s.listen(self.maxConnections)
		print("HTTP server started, will accept ", self.maxConnections, " connections at most.")
	
	def connect(self, host, port):
		self.s.connect((host, port))

	def close(self):
		self.s.shutdown(1)
		self.s.close()
	
	def kill(self):
		self.interruptFlag = True

	def accept(self):
		(clientSocket, address) = self.s.accept()
		return HttpSocket(s = clientSocket)
	
	def send(self, message):
		totalSent = 0
		while totalSent < len(message):
			sent = self.s.send(message[totalSent:])
			if 0 == sent:
				raise RuntimeError("The HTTP Socket connection was broken while trying to send.")
			totalSent += sent
	
	def receive(self, n = 1):
		message = b''
		while len(message) < n and not self.interruptFlag:
			# TODO : rendre le receive non bloquant
			(readyToRead,rw,err) = select.select([self.s],[],[], self._selectTimer)
			if readyToRead:
				chunk = self.s.recv(n)
				if chunk == b'':
					raise RuntimeError("The HTTP Socket connection was broken while trying to receive.")
				message += chunk
		return message