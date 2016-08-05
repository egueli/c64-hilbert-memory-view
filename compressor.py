#!/usr/bin/env python

import sys

class FrameData:
	def __init__(self, sequence, time):
		self.addresses = {}
		self.sequence = sequence
		self.time = time

	def output(self):
		s = []
		s.append(self.time)
		for direction in self.addresses:
			s.append(direction)
			accesses = list(set(self.addresses[direction]))
			accesses.sort()

			rangeStart = None
			rangeLen = 0
			for access in accesses:
				if rangeStart is None:
					rangeStart = access
					rangeLen = 1
				else:
					if access == rangeStart + rangeLen:
						rangeLen = rangeLen + 1
					else:
						s.append(rangeStart)
						s.append(rangeLen)
						rangeStart = access
						rangeLen = 1
			s.append(rangeStart)
			s.append(rangeLen)
		print " ".join([str(n) for n in s])


	def parse(self, fields):
		address = int(fields[1], 16)
		direction = fields[2]
		if not direction in self.addresses:
			self.addresses[direction] = []

		self.addresses[direction].append(address)


f = FrameData(0, 0)

frameDuration = 10
currentFrame = 0
startTime = None
for line in sys.stdin:
	try:
		fields = line.split()
		time = int(fields[0])

		if not startTime:
			startTime = time
		else:
			time = time - startTime

		sequence = int(time / frameDuration)
		if sequence != f.sequence:
			f.output()
			f = FrameData(sequence, time)

		f.parse(fields)
	except:
		print "error while processing line " + line
		raise

f.output()
