# -*-coding:Utf-8 -*
from sockets.GenericSocket import *

class TcpSocket(GenericSocket):
	"""
	TcpSocket implements our high level methods to send and receive information.
	"""
	
	def __init__(self, maxConnections = 5, s = None):
		GenericSocket.__init__(self)

		if s is None:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		else:
			self.s = s
		# These options enable the same address and port to be reused quickly
		# (for example, in two consecutive runs of the script)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.maxConnections = maxConnections
	
	def listen(self, host = '127.0.0.1', port = 15000):
		self.s.bind((host, port))
		self.s.listen(self.maxConnections)
	
	def accept(self):
		(clientSocket, address) = self.s.accept()
		return TcpSocket(s = clientSocket)

	def getIp(self):
		(ip, port) = self.s.getsockname()
		return ip

	def connect(self, host, port):
		self.s.connect((host, port))

	def _close(self):
		GenericSocket._close(self)
		self.s.close()

	def receive(self, receiveBuffer = 1):
		self._blocked = True
		message = b''
		while len(message) < receiveBuffer and not self._interruptFlag:
			(readyToRead,rw,err) = select.select([self.s],[],[], self._selectTimer)
			if self._interruptFlag:
				self._close()
			if readyToRead:
				chunk = self.s.recv(receiveBuffer)
				if chunk == b'':
					raise RuntimeError("The TCP Socket connection was broken while trying to receive.")
				message += chunk
		self._blocked = False
		return message

	# TODO: how to keep large buffer size, but still be quick to return when a message only contains a few characters?
	def nextLine(self, receiveBuffer=2, delimiter="\r\n"):
		self._blocked = True
		while not self._interruptFlag:
			(readyToRead,rw,err) = select.select([self.s],[],[], self._selectTimer)
			if self._interruptFlag:
				self._close()
			if readyToRead:
				try:
					data = self.s.recv(receiveBuffer)
					self._buffer += str(data, 'Utf-8')
				except:
					continue
			if self._buffer.find(delimiter) != -1:
				(line, self._buffer) = self._buffer.split(delimiter, 1)
				self._blocked = False
				return line

	def send(self, message):
		self._blocked = True
		totalSent = 0
		if str == type(message):
			message = message.encode('Utf-8')
		while totalSent < len(message) and not self._interruptFlag:
			(rr,readyToWrite,err) = select.select([],[self.s],[], self._selectTimer)
			if self._interruptFlag:
				self._close()
			if readyToWrite:
				try:
					sent = self.s.send(message)
					totalSent += sent
					if 0 == sent:
						raise RuntimeError("The TCP Socket connection was broken while trying to send.")
				except:
					continue
		self._blocked = False