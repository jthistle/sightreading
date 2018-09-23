#!/usr/bin/env python3

import random
from dataStructs import note

def path(via, weight=1):
	return {"path": via, "weight": weight}

def link(chord, weight, *paths):
	return {"chord": chord, "weight": weight, "paths": paths}

def chord(chord, duration):
	return {"chord": chord, "duration": duration}

class ProgressionGen:
	def __init__(self):
		self.semitoneMap = {
			"I": 0,
			"II": 2,
			"III": 4,
			"IV": 5,
			"V": 7,
			"BVI": 8,
			"VI": 9,
			"VII": 11,
		}

		self.semitoneToStep = {
			0: "C",
			1: "C#",
			2: "D",
			3: "Eb",
			4: "E",
			5: "F",
			6: "F#",
			7: "G",
			8: "Ab",
			9: "A",
			10: "Bb",
			11: "B"
		}

		self.intervals = {
			"major": [0, 4, 7],
			"minor": [0, 3, 7],
			"dom": [0, 4, 7, 10],
			"dim": [0, 3, 6, 9],
		}

		self.links = {
			"I": [
				link("IV", 2, path("d")),
				link("V", 1, path("d")),
				link("V7", 1, path("d")),
				link("vi", 1, path("bvio", 1), path("d", 2))
			],
			"ii": [
				link("III", 1, path("d"))
			],
			"iii": [
				link("vi", 2, path("III", 2), path("d", 1)),
				link("IV", 1, path("d"))
			],
			"IV": [
				link("I", 2, path("d")),
				link("V", 1, path("d")),
				link("V7", 1, path("d")),
				link("vi", 1, path("bvio", 2), path("d", 1))
			],
			"V": [
				link("I", 2, path("d")),
				link("IV", 2, path("d")),
				link("vi", 1, path("bvio", 2), path("d", 1))
			],
			"vi": [
				link("III", 2, path("d")),
				link("iii", 1, path("d")),
				link("ii", 2, path("d")),
				link("IV", 2, path("d", 1), path("V", 2)),
				link("V", 1, path("d")),
				link("V7", 1, path("d")),
				link("I", 1, path("d")),
				link("II", 2, path("d"))
			],
			"II": [
				link("V", 1, path("d")),
				link("V7", 1, path("d")),
			],
			"III": [
				link("vi", 2, path("d")),
				link("IV", 1, path("d"))
			],
			"V7": [
				link("I", 2, path("d")),
				link("vi", 1, path("d", 2), path("bvio", 1)),  # these weightings are correct.
			]
		}

	def new(self):
		# 7 is temporary, can be randomized phrase length
		prog = []
		prog.append(chord("I", 8))
		lastChord = "I"
		for i in range(7):
			force = None
			if i == 5:
				force = ["IV", "V", "III"]
			elif i == 6:
				if lastChord == "III":
					force = ["vi"]
				else:
					force = ["I"]

			link = self.chooseFromLinks(self.links[lastChord], force)
			path = self.chooseFromPaths(link["paths"])

			if path["path"] == "d":
				prog.append(chord(link["chord"], 8))
			else:
				# Go back and make last chord half length
				prog[-1]["duration"] = 4
				prog.append(chord(path["path"], 4))
				prog.append(chord(link["chord"], 8))

			lastChord = link["chord"]

		return prog

	def chooseFromLinks(self, links, forceChoose=None):
		'''
		Returns a link data struct
		forceChoose should be a list of chord strings.
		'''
		if forceChoose is not None:
			newLinks = []
			for l in links:
				if l["chord"] in forceChoose:
					newLinks.append(l)
			
			if len(newLinks) > 0:
				links = newLinks

		totalWeight = sum([l["weight"] for l in links])
		chosenNum = random.randint(1,totalWeight)
		currentNum = 0
		for l in links:
			if currentNum+l["weight"] >= chosenNum:
				return l
			currentNum += l["weight"]

		return False

	def chooseFromPaths(self, paths):
		'''
		Returns a path.
		'''
		totalWeight = sum([p["weight"] for p in paths])
		chosenNum = random.randint(1,totalWeight)
		currentNum = 0
		for p in paths:
			if currentNum+p["weight"] >= chosenNum:
				return p
			currentNum += p["weight"]

		return False

	def progToWriterStruct(self, prog):
		toReturn = {
			"timeSig": [4, 4],
			"keySig": 0,
			"clef": "treble"
		}

		bars = []

		currentChords = []
		totalBarDuration = 0
		for chord in prog:
			if totalBarDuration >= 16:
				totalBarDuration = 0
				bars.append({"chords": currentChords})
				currentChords = []

			totalBarDuration += chord["duration"]

			chordToAdd = {
				"duration": chord["duration"]
			}

			chordNumeral = chord["chord"]
			chordLookup = chordNumeral
			chordMood = "major"
			if chordNumeral[-1] == "o":
				chordLookup = chordNumeral[:-1]
				chordMood = "dim"
			elif chordNumeral[-1] == "7":
				chordLookup = chordNumeral[:-1]
				chordMood = "dom"

			if chordMood not in ("dim", "dom"):
				if any(x.isupper() for x in chordLookup):
					chordMood = "major"
				else:
					chordMood = "minor"

			startSemitone = self.semitoneMap[chordLookup.upper()]
			notesToAdd = []
			for i in self.intervals[chordMood]+[12]:
				currentSemitone = (startSemitone + i) % 12
				if i == 0:
					octave = 3
				else:
					octave = 4
				step = self.semitoneToStep[currentSemitone]
				notesToAdd.append(note(step, octave))

			chordToAdd["notes"] = notesToAdd

			currentChords.append(chordToAdd)

		if len(currentChords) > 0:
			bars.append({"chords": currentChords})

		toReturn["bars"] = bars

		return toReturn