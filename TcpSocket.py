#!/usr/local/bin/python3.3
# -*-coding:Utf-8 -*
import socket
import select

class TcpSocket:
	"""
	TcpSocket implements our high level methods to send and receive information.
	"""
	
	def __init__(self, maxConnections = 5, s = None):
		if s is None:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.s = s
		# These options enable the same address and port to be reused quickly
		# (for example, in two consecutive runs of the script)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.maxConnections = maxConnections
		self._interruptFlag = False
		self._blocked = False
		self._selectTimer = 3
		self._buffer = ""
	
	def listen(self, host = '127.0.0.1', port = 15000):
		self.s.bind((host, port))
		self.s.listen(self.maxConnections)
	
	def connect(self, host, port):
		self.s.connect((host, port))

	def _close(self):
		self.s.send(b'The connection is going down NOW.\r\n')
		#self.s.send(b'Bye.\r\n')
		self.s.shutdown(1)
		self.s._close()
	
	def kill(self):
		self._interruptFlag = True
		if not self._blocked:
			self._close()
		#else: self._close() called automatically after the timeout

	def accept(self):
		(clientSocket, address) = self.s.accept()
		return TcpSocket(s = clientSocket)
	
	def send(self, message):
		self._blocked = True
		totalSent = 0
		while totalSent < len(message) and not self._interruptFlag:
			(rr,readyToWrite,err) = select.select([],[self.s],[], self._selectTimer)
			if self._interruptFlag:
				self._close()
			if readyToWrite:
				sent = self.s.send(message[totalSent:])
				if 0 == sent:
					raise RuntimeError("The TCP Socket connection was broken while trying to send.")
				totalSent += sent
		self._blocked = False

	def nextLine(self, receiveBuffer=4, delimiter="\r\n"):
		self._blocked = True
		while not self._interruptFlag:
			(readyToRead,rw,err) = select.select([self.s],[],[], self._selectTimer)
			if self._interruptFlag:
				self._close()
			if readyToRead:
				data = self.s.recv(receiveBuffer)
				self._buffer += str(data, 'Utf-8')
			if self._buffer.find(delimiter) != -1:
				(line, self._buffer) = self._buffer.split(delimiter, 1)
				self._blocked = False
				return line

	def receive(self, n = 1):
		self._blocked = True
		message = b''
		while len(message) < n and not self._interruptFlag:
			(readyToRead,rw,err) = select.select([self.s],[],[], self._selectTimer)
			if self._interruptFlag:
				self._close()
			if readyToRead:
				chunk = self.s.recv(n)
				if chunk == b'':
					raise RuntimeError("The TCP Socket connection was broken while trying to receive.")
				message += chunk
		self._blocked = False
		return message














