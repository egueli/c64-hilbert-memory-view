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

		self.promptRegex = "\(C:\$[0-9a-f]{4}\) " 
		self.firstTalk = True

	def talk(self, command):
		self.sock.send(command + "\n")
		if self.firstTalk == True:
			self.receive()
			self.firstTalk = False
			# print "tt", "skipped first talk"

		lines = self.receive()
		# for line in lines:
		#  	print "tt>>", line
		return lines

	def receive(self):
		data = True
		buffer = ""
		while data:
			# print "rr before recv, count:", self.count
			data = self.sock.recv(4096)
			buffer += data
			# print "rr", "|" + data + "|"

			promptMatches = [m for m in re.finditer(self.promptRegex, buffer)]
			if len(promptMatches) > 0:
				pos = promptMatches[-1].start()
				# print "rr", "prompt found at", pos
				output = buffer[:pos]
				lines = output.split("\n")

				return lines[:-1]
			# else:
			# 	print "rr", "prompt is not here"

directions = {
	'STA': 'w',
	'STX': 'w',
	'STY': 'w',
	'LDA': 'r',
	'LDX': 'r',
	'LDY': 'r',
	'CMP': 'r',
	'CPX': 'r',
	'CPY': 'r',
	'INC': 'rw',
	'ORA': 'r',
	'ADC': 'r',
	'AND': 'r',
	'ASL': 'rw',
	'DEC': 'rw',
	'EOR': 'r',
	'LSR': 'rw',
	'ROL': 'rw',
	'ROR': 'rw',
	'SBC': 'r',
	'JMP': None,
	'JSR': None,
	'BPL': None,
	'BMI': None,
	'BVC': None,
	'BVS': None,
	'BCC': None,
	'BCS': None,
	'BNE': None,
	'BEQ': None,
}
def direction(opcode):
	d = directions[opcode]
	return d

def processStepLines(lines):
	if (len(lines) != 1):
		raise Exception("... line?")

	line = lines[0]
	#print line
	m = re.search('...([0-9a-f]+).{14}(.+) - A:(..) X:(..) Y:(..).* ([0-9]+)', line)
	if not m:
		raise Exception("no match: \"" + line + "\"")

	groups = [m.group(i) for i in range(1, 7)]
	ipHex, instruction, aHex, xHex, yHex, time = groups
	print time, ipHex, "x", instruction

	# 1-byte instructions

	matchImplied = re.search('^...  ', instruction)
	if matchImplied:
		return

	matchAccumulator = re.search('^... A  ', instruction)
	if matchAccumulator:
		return

	# 2-byte instructions

	ip = int(ipHex, 16)
	print time, "%04x" % (ip + 1), "x"

	matchImmediate = re.search('^... #\$\S\S   ', instruction)
	if matchImmediate:
		return

	matchZeroPage = re.search('^(...) \$(\S\S)   ', instruction)
	if matchZeroPage:
		addressHex = matchZeroPage.group(2)
		print time, "00" + addressHex, direction(matchZeroPage.group(1))
		return

	matchIndirectIndexed = re.search('^(...) \(\$(\S\S)\),Y', instruction)
	if matchIndirectIndexed:
		zpAddressHex = matchIndirectIndexed.group(2)
		zpAddress = int(zpAddressHex, 16)
		print time, "%04x" % zpAddress, "r"
		print time, "%04x" % (zpAddress + 1), "r"
		memlines = talker.talk('mem %04x %04x' % (zpAddress, zpAddress + 1))
		memline = memlines[0]
		memMatch = re.match('.........(\S\S) (\S\S)', memline)
		if not memMatch:
			raise Exception('unrecognized memory dump output: ' + memline)
		lowHex = memMatch.group(1)
		highHex = memMatch.group(2)
		base = int(highHex + lowHex, 16)
		effective = base + int(yHex, 16)
		opcode = matchIndirectIndexed.group(1)
		print time, "%04x" % effective, direction(opcode)
		return

	# 3-byte instructions
	print time, "%04x" % (ip + 2), "x"

	matchAbsolute = re.search('^(...) \$(\S\S\S\S)    ', instruction)
	if matchAbsolute:
		opcode = matchAbsolute.group(1)
		direc = direction(matchAbsolute.group(1))
		if direc:
			print time, matchAbsolute.group(2), direc
		return

	matchAbsoluteIndexed = re.search('(...) \$(\S\S\S\S),([XY])', instruction)
	if matchAbsoluteIndexed:
		opcode, addressHex, register = [matchAbsoluteIndexed.group(i) for i in range(1, 4)]
		if register == 'X':
			address = int(addressHex, 16) + int(xHex, 16)
		else:
			address = int(addressHex, 16) + int(yHex, 16)


		print time, "%04x" % address, direction(opcode)
		return

	# im = re.search('... \(\$([^)]+)\)', instruction)
	# if not im:
	# 	print time, ip, instruction, a, x, y
	# else:
	# 	indirect = im.group(1)
	# 	print time, ip, instruction, a, x, y, indirect

	raise Exception("unrecognized instruction: " + instruction)


talker = ViceRemoteMonitorTalker()

# Triggers a soft reset.
# The "reset" command doesn't work reliably, as it messes with the monitor
# state. The "g" command to the reset routine makes the monitor leave, that's
# why it's preceded by a breakpoint on the same location.
# Note: the first "step" command will run the instruction after the first of
# the reset routine.
talker.talk("break $fce2")
talker.talk("g $fce2")

while True:
	lines = talker.talk("step")
	processStepLines(lines);	


sock.close()
