from music21 import stream, note, chord, key, meter

# Create a Stream for the chorale
chorale = stream.Score()

# Define key signature and time signature
chorale.append(key.KeySignature(0))  # C Major
chorale.append(meter.TimeSignature('4/4'))

# Create the four parts (Soprano, Alto, Tenor, Bass)
soprano = stream.Part()
alto = stream.Part()
tenor = stream.Part()
bass = stream.Part()

# Define the chords for the harmonization
chords = [
    chord.Chord(["C4", "E4", "G4"]),  # C major
    chord.Chord(["F4", "A4", "C5"]),  # F major
    chord.Chord(["G4", "B4", "D5"]),  # G major
    chord.Chord(["C4", "E4", "G4"])   # C major
]

# Define each part (soprano, alto, tenor, bass) as simple chord voicings
soprano_notes = ["E5", "F5", "G5", "E5"]
alto_notes = ["C5", "A4", "B4", "G4"]
tenor_notes = ["G4", "F4", "D4", "E4"]
bass_notes = ["C4", "F4", "G4", "C4"]

# Add the notes to each part
for i in range(4):  # Loop through each chord in the chorale
    soprano.append(note.Note(soprano_notes[i], quarterLength=4))
    alto.append(note.Note(alto_notes[i], quarterLength=4))
    tenor.append(note.Note(tenor_notes[i], quarterLength=4))
    bass.append(note.Note(bass_notes[i], quarterLength=4))

# Add the parts to the score
chorale.append(soprano)
chorale.append(alto)
chorale.append(tenor)
chorale.append(bass)

# Show the chorale in a music notation format (MIDI or musicXML)
# Needs installation of Music Core software
# chorale.show()

# Alternatively, you can generate a MIDI file for playback
chorale.write('midi', fp='four_part_chorale.mid')
chorale.show('midi', )
