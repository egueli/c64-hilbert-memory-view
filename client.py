#!/usr/bin/env python

import socket
import re


def readMonitorLine(sock, recv_buffer=4096):
	buffer = ''
	data = True
	promptEnd = ") "
	while data:
		data = sock.recv(recv_buffer)
		buffer += data

		while buffer.find(promptEnd) != -1:
			output, buffer = buffer.split(promptEnd, 1)
			lines = output.split("\n")
			yield lines[:-1]
	return


def processLines(lines):
	if len(lines) != 1:
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


TCP_IP = '127.0.0.1'
TCP_PORT = 6510
MESSAGE = "\nreset\n"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
sock.connect((TCP_IP, TCP_PORT))
sock.send(MESSAGE)

for lines in readMonitorLine(sock):
	processLines(lines);	
	sock.send("step\n")


sock.close()
