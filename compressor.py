#!/usr/bin/env python

import sys

class FrameData:
	def __init__(self, sequence, time):
		self.addresses = {}
		self.sequence = sequence
		self.time = time

	def output(self):
		s = []
		for direction in self.addresses:
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
						s.append("%s:%d:%d" % (direction, rangeStart, rangeLen))
						rangeStart = access
						rangeLen = 1
			s.append("%s:%d:%d" % (direction, rangeStart, rangeLen))
		print str(self.time) + " " + " ".join(s)


	def parse(self, fields):
		address = int(fields[1], 16)
		direction = fields[2]
		if not direction in self.addresses:
			self.addresses[direction] = []

		self.addresses[direction].append(address)

f = None
frameDuration = 10
for line in sys.stdin:
	try:
		fields = line.split()
		time = int(fields[0])

		sequence = int(time / frameDuration)
		if not f:
			f = FrameData(sequence, time)
		else:
			if f.sequence != sequence:
				f.output()
				f = FrameData(sequence, time)

		f.parse(fields)
	except:
		print "error while processing line " + line
		raise

f.output()
