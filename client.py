#!/usr/bin/env python

import socket
import re

class ViceRemoteMonitorTalker:
	def __init__(self):
		TCP_IP = '127.0.0.1'
		TCP_PORT = 6510

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
		self.sock.connect((TCP_IP, TCP_PORT))

		self.buffer = ''
		self.promptEnd = ") " 
		self.firstTalk = True

	def talk(self, command):
		self.sock.send(command + "\n")
		if self.firstTalk == True:
			self.receive()
			self.firstTalk = False

		return self.receive();

	def receive(self):
		data = True
		while data:
			data = self.sock.recv(4096)
			self.buffer += data

			if self.buffer.find(self.promptEnd) != -1:
				output, self.buffer = self.buffer.split(self.promptEnd, 1)
				lines = output.split("\n")
				return lines[:-1]


def processStepLines(lines):
	if (len(lines) != 1):
		return
		
	line = lines[0]
	#print line
	m = re.search('...([0-9a-f]+).{14}(.+) - A:(..) X:(..) Y:(..).* ([0-9]+)', line)
	if not m:
		return

	groups = [m.group(i) for i in range(1, 7)]
	ip, instruction, a, x, y, time = groups

	im = re.search('... \(\$([^)]+)\),Y', instruction)
	flags = ""
	if not im:
		print time, ip, instruction, a, x, y, flags
	else:
		flags = flags + "I"
		print time, ip, instruction, a, x, y, flags


talker = ViceRemoteMonitorTalker()

while True:
	lines = talker.talk("step")
	processStepLines(lines);	


sock.close()
