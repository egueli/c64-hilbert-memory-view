#!/usr/bin/env python

import socket
import re

def readMonitorLine(sock, recv_buffer=4096):
	buffer = ''
	data = True
	while data:
		data = sock.recv(recv_buffer)
		buffer += data

		while buffer.find(") ") != -1:
			output, buffer = buffer.split(") ", 1)
			lines = output.split("\n")
			yield lines[:-1]
	return


TCP_IP = '127.0.0.1'
TCP_PORT = 6510
MESSAGE = "\nreset\n"

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))
sock.send(MESSAGE)

for lines in readMonitorLine(sock):
	sock.send("step\n")
	if len(lines) != 1:
		continue

	line = lines[0]
	#print line
	m = re.search('...([0-9a-f]+).{14}([A-Z]{3}) ([^ ]+).*  ([0-9]+)', line)
	if not m:
		continue

	print m.group(4), m.group(1), m.group(2), m.group(3)


sock.close()
