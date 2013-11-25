#!/usr/local/bin/python3.3
# -*-coding:Utf-8 -*
from threading import Thread

class Handler(Thread):
	
	def __init__(self):
		Thread.__init__(self)
		self.interruptFlag = False
	
	def kill(self):
		self.interruptFlag = True
