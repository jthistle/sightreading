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