def note(name, octave):
	return {"name": name, "octave": octave}

SEMIQUAVER = 1
QUAVER = 2
CROTCHET = 4
MINIM = 8
SEMIBREVE = 16

DURATION_NAMES = {
	SEMIBREVE: "whole",
	MINIM: "half",
	CROTCHET: "quarter",
	QUAVER: "eighth",
	SEMIQUAVER: "16th"
}

EXAMPLE_DATA = {
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