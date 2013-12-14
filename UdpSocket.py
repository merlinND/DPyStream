# -*-coding:Utf-8 -*
import socket
import select

class UdpSocket:
	"""
	UdpSocket implements our high level methods to send and receive information.
	"""

	def enum(**enums):
		return type('Enum', (), enums)

	Type = enum(SENDING = 0, RECEIVING = 1)

	def __init__(self, maxConnections = 5, s = None):
		if s is None:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		else:
			self.s = s
		# These options enable the same address and port to be reused quickly
		# (for example, in two consecutive runs of the script)
		self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
		self.maxConnections = maxConnections
		# These options allow to interrupt the socket during a recv or send
		self._interruptFlag = False
		self._selectTimer = 3

		self.host = None
		self.port = None
	
	def listen(self, host, port):
		self.host = host
		self.port = port
		self.s.bind((host, port))

	def _close(self):
		self.s.sendto(b'The connection is going down NOW.\r\n', (self.host, self.port))
#		self.s.sendto(b'Bye.\r\n', (self.host, self.port))
	
	def kill(self):
		self._interruptFlag = True
		# No need to close a Udp Socket

	def send(self, message):
		totalSent = 0
		if str == type(message):
			message = message.encode('Utf-8')

		while totalSent < len(message) and not self._interruptFlag:
			(rr,readyToWrite,err) = select.select([],[self.s],[], self._selectTimer)
			if readyToWrite:
				sent = self.s.sendto(message[totalSent:], (self.host, self.port))
				if 0 == sent:
					raise RuntimeError("The TCP Socket connection was broken while trying to send.")
				totalSent += sent

	def nextLine(self, receiveBuffer=4096, delimiter="\r\n"):
		dataBuffer = ""
		data = b''
		while not self._interruptFlag:
			(readyToRead,rw,err) = select.select([self.s],[],[], self._selectTimer)
			if readyToRead:
				data, _ = self.s.recvfrom(receiveBuffer)
				dataBuffer += str(data, 'Utf-8')
			if dataBuffer.find(delimiter) != -1:
				(line, dataBuffer) = dataBuffer.split(delimiter, 1)
				return line

	def receive(self, n = 1):
		message = b''
		while len(message) < n and not self._interruptFlag:
			(readyToRead,rw,err) = select.select([self.s],[],[], self._selectTimer)
			if readyToRead:
				chunk = self.s.recv(n)
				if chunk == b'':
					raise RuntimeError("The TCP Socket connection was broken while trying to receive.")
				message += chunk
		return message