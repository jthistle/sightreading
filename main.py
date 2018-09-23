#!/usr/bin/env python3

from chordProg import ProgressionGen
from writer import MusicWriter
from dataStructs import *

def main():
	gen = ProgressionGen()
	test = gen.new()
	print(" ".join([c["chord"] for c in test]))
	toWrite = gen.progToWriterStruct(test)

	# Duration of 1 is a semiquaver

	testData = {
		"timeSig": [4, 4],
		"keySig": 0,
		"clef": "treble",
		"bars": [
			{
				"chords": [
					{
						"duration": MINIM,
						"notes": [
							note("C", 4),
							note("E", 4)
						]
					},
					{
						"duration": MINIM,
						"notes": [
							note("G", 4),
							note("E", 4)
						]
					}
				]
			},
			{
				"chords": [
					{
						"duration": CROTCHET,
						"notes": [
							note("A", 4),
							note("C", 4)
						]
					},
					{
						"duration": CROTCHET,
						"rest": True
					},
					{
						"duration": SEMIQUAVER,
						"notes": [
							note("D", 4)
						]
					}
				]
			}
		]
	}

	writer = MusicWriter()
	writer.write("test.musicxml", toWrite)

if __name__ == "__main__":
	main()