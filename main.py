#!/usr/bin/env python3

from chordProg import ProgressionGen
from writer import MusicWriter
from dataStructs import *

def main():
	gen = ProgressionGen()
	test = gen.new()
	print(" ".join([c["chord"] for c in test]))
	toWrite = gen.progToWriterStruct(test)

	writer = MusicWriter()
	writer.write("test.musicxml", toWrite)

if __name__ == "__main__":
	main()