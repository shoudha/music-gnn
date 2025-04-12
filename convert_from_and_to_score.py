from music21 import stream, note, converter

def extract_notes_and_durations(score):
    note_dict = {'soprano': [], 'alto': [], 'tenor': [], 'bass': []}
    duration_dict = {'soprano': [], 'alto': [], 'tenor': [], 'bass': []}

    for part in score.parts:
        part_id = part.id.lower()
        for n in part.recurse().notesAndRests:
            if n.isRest:
                note_dict[part_id].append('rest')
            else:
                note_dict[part_id].append(n.nameWithOctave)
            duration_dict[part_id].append(n.quarterLength)
    
    return note_dict, duration_dict

def reconstruct_score(note_dict, duration_dict):
    sc = stream.Score()
    for voice in ['soprano', 'alto', 'tenor', 'bass']:
        p = stream.Part()
        p.id = voice
        p.partName = voice.capitalize()
        notes = note_dict[voice]
        durations = duration_dict[voice]
        for n, d in zip(notes, durations):
            if n == 'rest':
                p.append(note.Rest(quarterLength=d))
            else:
                p.append(note.Note(n, quarterLength=d))
        sc.append(p)
    return sc

# Load the original score (from MusicXML, corpus, etc.)
score = converter.parse(r'C:/Users/14694/.pyenv/pyenv-win/versions/3.9.13/Lib/site-packages/music21/corpus/bach/bwv10.7.mxl')  # Or use your loaded score

# Step 1: Extract
note_dict, duration_dict = extract_notes_and_durations(score)

# Step 2: Reconstruct
new_score = reconstruct_score(note_dict, duration_dict)

# View or export
new_score.show('text')  # Or .show() to view in notation software



 