# -*-coding:Utf-8 -*
import socket
import select

class GenericSocket:
	"""
	GenericSocket implements our high level methods to send and receive information with a TCP or UDP socket.
	"""
	
	def __init__(self, maxConnections = 5, s = None):
		# These options allow to interrupt the socket during a recv or send
		self._interruptFlag = False
		self._blocked = False
		self._selectTimer = 3
		self._buffer = ""

	def _close(self):
		pass
	
	def kill(self):
		self._interruptFlag = True
		if not self._blocked:
			self._close()
		else:
			# Otherwise, self._close() is called automatically after the timeout
			pass
