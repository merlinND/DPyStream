# -*-coding:Utf-8 -*
from GenericSocket import *

class UdpSocket(GenericSocket):
	"""
	UdpSocket implements our high level methods to send and
	receive information.
	Note: all UdpSocket instances share the same commonSocket
	"""

	def __init__(self, s, host, port):
		"""
		s is the underlying socket instance (given by the UdpAccepter)
		Note: all UdpSocket instances share the same commonSocket
		client is a simple object containing the client host address and its receive port.
		"""
		GenericSocket.__init__(self)
		if s is None:
			self.s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		else:
			self.s = s
		
		# Which client is allowed to communicate with us
		# (others are ignored)
		self.clientHost = host
		self.clientPort = port

	def receive(self, message):
		"""
		This receive method is called by the UdpAccepter, which forwards to us only the messages that come from our client.
		"""
		self._buffer += str(message, 'Utf-8')

	def send(self, message):
		totalSent = 0
		if str == type(message):
			message = message.encode('Utf-8')

		while totalSent < len(message) and not self._interruptFlag:
			(rr,readyToWrite,err) = select.select([],[self.s],[], self._selectTimer)
			if readyToWrite:
				sent = self.s.sendto(message, (self.clientHost, self.clientPort))
				if 0 == sent:
					raise RuntimeError("The UDP Socket was broken while trying to send.")
				totalSent += sent

	def nextLine(self, receiveBuffer=4096, delimiter="\r\n"):
		while not self._interruptFlag:
			if self._buffer.find(delimiter) != -1:
				(line, self._buffer) = self._buffer.split(\
								   delimiter, 1)
				return line

	def getIp(self):
		return self.clientHost