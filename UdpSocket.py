# -*-coding:Utf-8 -*
import socket
import select

class UdpSocket:
	"""
	UdpSocket implements our high level methods to send and
	receive information.
	"""

	def __init__(self, s, client):
		# Which client is allowed to communicate
		# (others are ignored)
		self.client = client

		# Given by the UdpAccepter
		self.s = s

		# These options allow to interrupt the socket during a
		# recv or send
		self.interruptFlag = False
		self._selectTimer = 3
		self._buffer = ""

	def _close(self):
		self.send(b'The connection is going down NOW.\r\n')
		# No need to close a Udp Socket
	
	def kill(self):
		self.interruptFlag = True
		self._close()

	def receive(self, message):
		self._buffer += str(message, 'Utf-8')

	def send(self, message):
		totalSent = 0
		if str == type(message):
			message = message.encode('Utf-8')

		while totalSent < len(message) and not self.interruptFlag:
			(rr,readyToWrite,err) = select.select([],[self.s],[], self._selectTimer)
			if readyToWrite:
				sent = self.s.sendto(message[totalSent:], (self.host, self.port))
				if 0 == sent:
					raise RuntimeError("The UDP Socket connection was broken while trying to send.")
				totalSent += sent

	def nextLine(self, receiveBuffer=4096, delimiter="\r\n"):
		while not self.interruptFlag:
			if self._buffer.find(delimiter) != -1:
				(line, self._buffer) = self._buffer.split(\
								   delimiter, 1)
				return line