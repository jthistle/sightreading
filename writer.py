#!/usr/bin/env python3

from xml.etree.ElementTree import Element, ElementTree, SubElement, Comment
from dataStructs import SEMIQUAVER, QUAVER, CROTCHET, MINIM, SEMIBREVE, DURATION_NAMES

class MusicWriter:
	def __init__(self):
		None

	def write(self, location, data):
		self.divisions = 4

#		start = '''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
#<!DOCTYPE score-partwise PUBLIC "-//Recordare//DTD MusicXML 3.1 Partwise//EN" 
#"http://www.musicxml.org/dtds/partwise.dtd">'''
		root = Element("score-partwise", {"version": "3.1"})
		tree = ElementTree(root)

		partList = SubElement(root, "part-list")
		scorePart = SubElement(partList, "score-part", {"id": "P1"})
		partName = SubElement(scorePart, "part-name")
		partName.text = "Music"

		part1 = SubElement(root, "part", {"id": "P1"})

		firstBar = SubElement(part1, "measure", {"number": "1"})
		attributes = SubElement(firstBar, "attributes")
		divisionsElement = SubElement(attributes, "divisions")
		divisionsElement.text = str(self.divisions)

		# KEY SIG HANDLING
		key = SubElement(attributes, "key")
		keyFifths = SubElement(key, "fifths")

		default = True
		if "keySig" in data.keys():
			keySigData = data["keySig"]
			if type(keySigData) == int:
				default = False
				keyFifths.text = str(keySigData)
		
		if default:
			keyFifths.text = "0"

		# TIME SIG HANDLING
		time = SubElement(attributes, "time")
		beats = SubElement(time, "beats")
		beatType = SubElement(time, "beat-type")

		default = True
		if "timeSig" in data.keys():
			timeSigData = data["timeSig"]
			if len(timeSigData) == 2:
				default = False
				beats.text = str(timeSigData[0])
				beatType.text = str(timeSigData[1])
				self.barDivisions = int(self.divisions * timeSigData[0] * (4/timeSigData[1]))
		
		if default:
			beats.text = "4"
			beatType.text = "4"
			self.barDivisions = 4*4

		# CLEF HANDLING
		clef = SubElement(attributes, "clef")
		sign = SubElement(clef, "sign")
		line = SubElement(clef, "line")

		default = True
		if "clef" in data.keys():
			clefData = data["clef"]
			default = False
			if clefData == "treble":
				sign.text = "G"
				line.text = "2"
			elif clefData == "bass":
				sign.text = "F"
				line.text = "4"
			elif clefData == "tenor":
				sign.text = "C"
				line.text = "4"
			elif clefData == "alto":
				sign.text = "C"
				line.text = "3"
			else:
				default = True
		
		if default:
			sign.text = "G"
			line.text = "2"

		# TEMPO HANDLING
		default = True
		if "tempo" in data.keys():
			default = False
			tempoValue = str(data["tempo"])

		if default:
			tempoValue = "100"

		direction = SubElement(firstBar, "direction")
		directionType = SubElement(direction, "direction-type")
		metronome = SubElement(directionType, "metronome")
		beatUnit = SubElement(metronome, "beat-unit")
		beatUnit.text = "quarter"
		perMin = SubElement(metronome, "per-minute")
		perMin.text = tempoValue

		soundElement = SubElement(direction, "sound", {"tempo": tempoValue})

		# NOTE HANDLING
		if "bars" in data.keys():
			barNum = 1
			for b in data["bars"]:
				if barNum == 1:
					barElement = firstBar
				else:
					barElement = SubElement(part1, "measure", {"number": str(barNum)})

				totalDuration = 0

				for c in b["chords"]:
					duration = c["duration"]
					totalDuration += duration
					first = True
					if "notes" in c.keys():
						for n in c["notes"]:
							tempNote = SubElement(barElement, "note")
							if first:
								first = False
							else:
								# Mark as a chord
								SubElement(tempNote, "chord")

							pitch = SubElement(tempNote, "pitch")
							# Pitch needs to have an alter tag if step is # or b
							alter = 0
							noteName = n["name"]
							if noteName[-1] == "#":
								alter = 1
								noteName = noteName[:-1]
							elif noteName[-1] == "b":
								alter = -1
								noteName = noteName[:-1]

							step = SubElement(pitch, "step")
							step.text = noteName
							alterElement = SubElement(pitch, "alter")
							alterElement.text = str(alter)
							octave = SubElement(pitch, "octave")
							octave.text = str(n["octave"])

							durationElement = SubElement(tempNote, "duration")
							durationElement.text = str(duration)

							writeDot = False
							if duration not in DURATION_NAMES:
								i = duration
								while i > 0 and i not in DURATION_NAMES:
									i -= 1
								durName = DURATION_NAMES[i]
								writeDot = True
							else:
								durName = DURATION_NAMES[duration]

							typeElement = SubElement(tempNote, "type")
							typeElement.text = durName

							# Dots must be written after type tag, for some reason.
							if writeDot:
								SubElement(tempNote, "dot")  # add dot
					else:
						# Assume rest
						tempNote = SubElement(barElement, "note")
						SubElement(tempNote, "rest")

						durationElement = SubElement(tempNote, "duration")
						durationElement.text = str(duration)

				if totalDuration < self.barDivisions:
					tempNote = SubElement(barElement, "note")
					SubElement(tempNote, "rest")
					durationElement = SubElement(tempNote, "duration")
					durationElement.text = str(self.barDivisions-totalDuration)

				barNum += 1

		tree.write(location)