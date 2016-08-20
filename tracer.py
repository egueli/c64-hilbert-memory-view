#!/usr/bin/env python

import argparse
import socket
import re
from math import floor
import os

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

	def close(self):
		self.sock.close()

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
	'BIT': 'r',
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

def readMemory(address):
	memlines = talker.talk('mem %04x %04x' % (address, address + 1))
	memline = memlines[0]
	memMatch = re.match('.........([0-9a-f]{2}) ([0-9a-f]{2})', memline)
	if not memMatch:
		raise Exception('unrecognized memory dump output: ' + memline)
	lowHex = memMatch.group(1)
	highHex = memMatch.group(2)
	return int(highHex + lowHex, 16)

class Access:
	def __init__(self, address, direction):
		self.address = address;
		self.direction = direction;


def parseInstruction(instruction, ipHex, aHex, xHex, yHex, time):
	out = {"accesses": []}
	accesses = out["accesses"]

	# 1-byte instructions
	ip = int(ipHex, 16)
	accesses.append(Access(ip, 'x'))

	matchImplied = re.search('^...  ', instruction)
	if matchImplied:
		return out

	matchAccumulator = re.search('^... A  ', instruction)
	if matchAccumulator:
		return out

	# 2-byte instructions

	accesses.append(Access(ip + 1, 'x'))

	matchImmediate = re.search('^... #\$[0-9A-F]{2}   ', instruction)
	if matchImmediate:
		return out

	matchZeroPage = re.search('^(...) \$([0-9A-F]{2})   ', instruction)
	if matchZeroPage:
		addressHex = matchZeroPage.group(2)
		direc = direction(matchZeroPage.group(1))
		accesses.append(Access(int(addressHex, 16), direc))
		return out

	matchZeroPageIndexed = re.search('(...) \$([0-9A-F]{2}),([XY])', instruction)
	if matchZeroPageIndexed:
		opcode, addressHex, register = [matchZeroPageIndexed.group(i) for i in range(1, 4)]
		address = int(addressHex, 16)
		if register == 'X':
			address = address + int(xHex, 16)
		else:
			address = address + int(yHex, 16)

		accesses.append(Access(address, direction(opcode)))
		return out

	matchIndirectIndexed = re.search('^(...) \(\$([0-9A-F]{2})\),Y', instruction)
	if matchIndirectIndexed:
		zpAddressHex = matchIndirectIndexed.group(2)
		zpAddress = int(zpAddressHex, 16)
		accesses.append(Access(zpAddress, 'r'))
		accesses.append(Access(zpAddress + 1, 'r'))
		effective = readMemory(zpAddress) + int(yHex, 16)
		opcode = matchIndirectIndexed.group(1)
		accesses.append(Access(effective, direction(opcode)))
		return out

	matchIndexedIndirect = re.search('^(...) \(\$([0-9A-F]{2}),X\)', instruction)
	if matchIndexedIndirect:
		zpBaseAddressHex = matchIndirectIndexed.group(2)
		zpBaseAddress = int(zpBaseAddressHex, 16)
		zpAddress = (zpBaseAddress + int(xHex, 16) % 256)
		accesses.append(Access(zpAddress, 'r'))
		accesses.append(Access(zpAddress + 1, 'r'))
		effective = readMemory(zpAddress)
		opcode = matchIndexedIndirect.group(1)
		accesses.append(Access(effective, direction(opcode)))
		return out

	# 3-byte instructions
	accesses.append(Access(ip + 2, 'x'))

	matchAbsolute = re.search('^(...) \$([0-9A-F]{4})    ', instruction)
	if matchAbsolute:
		opcode = matchAbsolute.group(1)
		direc = direction(opcode)
		if direc:
			address = int(matchAbsolute.group(2), 16)
			accesses.append(Access(address, direc))
		return out

	matchAbsoluteIndexed = re.search('(...) \$([0-9A-F]{4}),([XY])', instruction)
	if matchAbsoluteIndexed:
		opcode, addressHex, register = [matchAbsoluteIndexed.group(i) for i in range(1, 4)]
		address = int(matchAbsoluteIndexed.group(2), 16)
		if register == 'X':
			address = address + int(xHex, 16)
		else:
			address = address + int(yHex, 16)

		accesses.append(Access(address, direction(opcode)))
		return out

	matchIndirectJMP = re.search('JMP \(\$([0-9A-F]{4})\)  ', instruction)
	if matchIndirectJMP:
		addressHex = matchIndirectJMP.group(1)
		address = int(addressHex, 16)
		accesses.append(Access(address, 'r'))
		return out

	
	raise Exception("unrecognized instruction: " + instruction)

def printInstructionAccesses(time, instruction):
	for access in instruction["accesses"]:
		print time, "%04x" % access.address, access.direction

def processStepLines(lines):
	if (len(lines) != 1):
		print len(lines), "lines??"
		for line in lines:
			print line
		raise Exception("... line?")

	line = lines[0]
	#print line
	m = re.search('...([0-9a-f]+).{14}(.+) - A:(..) X:(..) Y:(..).* ([0-9]+)', line)
	if not m:
		raise Exception("no match: \"" + line + "\"")

	groups = [m.group(i) for i in range(1, 7)]
	ipHex, instruction, aHex, xHex, yHex, time = groups

	parsed = parseInstruction(instruction, ipHex, aHex, xHex, yHex, time)
	printInstructionAccesses(time, parsed)

	return int(time)



parser = argparse.ArgumentParser(description="Traces all memory accesses of the emulated CPU in a VICE instance.")
parser.add_argument('-r', '--reset',
                    help='resets the C64 at start',
                    action='store_true')
parser.add_argument('-f', '--save-frames-fps')
parser.add_argument('-e', '--end-at')

talker = ViceRemoteMonitorTalker()

args = parser.parse_args()
if args.reset:
	# Triggers a soft reset.
	# The "reset" command doesn't work reliably, as it messes with the monitor
	# state. The "g" command to the reset routine makes the monitor leave, that's
	# why it's preceded by a breakpoint on the same location.
	# Note: the first "step" command will run the instruction after the first of
	# the reset routine.
	startAt = "$fce2"
	talker.talk("break " + startAt)
	talker.talk("g " + startAt)



if args.save_frames_fps:
	fps = int(args.save_frames_fps)
else:
	fps = None

if args.end_at:
	endAt = floor(float(args.end_at) * 1000000)
else:
	endAt = float("inf")

lastSavedFrame = None
firstInstructionAt = None
while True:
	lines = talker.talk("step")
	time = processStepLines(lines)
	if not firstInstructionAt:
		firstInstructionAt = time
	if (time - firstInstructionAt) > endAt:
		break

	if fps:
		frameNumber = floor(time / (1000000 / fps))
		if frameNumber != lastSavedFrame:
			fileName = "screenshot_" + str(time)
			filePath = os.getcwd() + "/" + fileName
			command = "screenshot \"" + filePath + "\" 2" # PNG format=2
			talker.talk(command)
			lastSavedFrame = frameNumber
			print time, "screenshot", fileName + ".png"



talker.close()
