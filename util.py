import random
from music21 import stream, note, converter, pitch

# def extract_notes_and_durations(score):
#     note_dict = {'soprano': [], 'alto': [], 'tenor': [], 'bass': []}
#     duration_dict = {'soprano': [], 'alto': [], 'tenor': [], 'bass': []}

#     for part in score.parts:
#         part_id = part.id.lower()
#         for n in part.recurse().notesAndRests:
#             if n.isRest:
#                 note_dict[part_id].append('rest')
#             else:
#                 note_dict[part_id].append(n.nameWithOctave)
#             duration_dict[part_id].append(n.quarterLength)
    
#     return note_dict, duration_dict

# def reconstruct_score(note_dict, duration_dict):
#     sc = stream.Score()
#     for voice in ['soprano', 'alto', 'tenor', 'bass']:
#         p = stream.Part()
#         p.id = voice
#         p.partName = voice.capitalize()
#         notes = note_dict[voice]
#         durations = duration_dict[voice]
#         for n, d in zip(notes, durations):
#             if n == 'rest':
#                 p.append(note.Rest(quarterLength=d))
#             else:
#                 p.append(note.Note(n, quarterLength=d))
#         sc.append(p)
#     return sc

pitch_vocab = {'rest': 0, 
               'E2': 1, 'F2': 2, 'G-2': 3, 'G2': 4, 'A-2': 5, 'A2': 6, 
               'B-2': 7, 'B2': 8, 'C3': 9, 'D-3': 10, 'D3': 11, 'E-3': 12, 
               'E3': 13, 'F3': 14, 'G-3': 15, 'G3': 16, 'A-3': 17, 'A3': 18, 
               'B-3': 19, 'B3': 20, 'C4': 21, 'D-4': 22, 'D4': 23, 'E-4': 24, 
               'E4': 25, 'F4': 26, 'G-4': 27, 'G4': 28, 'A-4': 29, 'A4': 30, 
               'B-4': 31, 'B4': 32, 'C5': 33}


def generate_random_note_and_duration_dicts(parts, note_counts):
    """
    Generate random notes and durations for given parts, each with custom number of notes.

    Args:
        parts (list): List of part names (e.g., ['soprano', 'alto', 'tenor', 'bass'])
        note_counts (dict): Mapping of part name to number of notes (e.g., {'soprano': 8, 'bass': 12})

    Returns:
        tuple: (note_dict, duration_dict)
    """
    pitch_ranges = {
        'soprano': ['C4', 'D-4', 'D4', 'E-4', 'E4', 'F4', 'G-4', 'G4', 'A-4', 'A4', 
                    'B-4', 'B4', 'C5'],
        'alto':    ['F3', 'G-3', 'G3', 'A-3', 'A3', 'B-3', 'B3', 'C4', 'D-4', 'D4'],
        'tenor':   ['C3', 'D-3', 'D3', 'E-3', 'E3', 'F3', 'G-3', 'G3', 'A-3', 'A3'],
        'bass':    ['E2', 'F2', 'G-2', 'G2', 'A-2', 'A2', 'B-2', 'B2', 'C3']
    }

    default_range = ['C4', 'D4', 'E4', 'F4', 'G4']  # Used if part is not in pitch_ranges
    durations_pool = [0.5, 1.0, 1.5, 2.0]
    rest_prob = 0.1

    note_dict = {}
    duration_dict = {}

    for part in parts:
        count = note_counts.get(part, 0)
        pitch_range = pitch_ranges.get(part.lower(), default_range)
        notes = []
        durations = []
        for _ in range(count):
            pitch = 'rest' if random.random() < rest_prob else random.choice(pitch_range)
            dur = random.choice(durations_pool)
            notes.append(pitch)
            durations.append(dur)
        note_dict[part] = notes
        duration_dict[part] = durations

    return note_dict, duration_dict

def extract_notes_and_durations(score):
    """
    Extract note names and durations from a music21 Score.
    Automatically detects and uses part IDs.

    Args:
        score (music21.stream.Score): The input Score object.

    Returns:
        tuple: (note_dict, duration_dict) where keys are part IDs
    """
    note_dict = {}
    duration_dict = {}

    for part in score.parts:
        part_id = part.id or f"Part{len(note_dict)+1}"
        note_dict[part_id] = []
        duration_dict[part_id] = []

        for n in part.recurse().notesAndRests:
            if n.isRest:
                note_dict[part_id].append('rest')
            else:
                note_dict[part_id].append(n.nameWithOctave)
            duration_dict[part_id].append(n.quarterLength)

    return note_dict, duration_dict


def reconstruct_score(note_dict, duration_dict):
    """
    Reconstruct a music21 Score from note and duration dictionaries.

    Args:
        note_dict (dict): {part_name: list of note names or 'rest'}
        duration_dict (dict): {part_name: list of durations}

    Returns:
        music21.stream.Score: A Score object containing all parts
    """
    score = stream.Score()

    for part_name in note_dict:
        p = stream.Part()
        p.id = part_name
        p.partName = part_name.capitalize()

        notes = note_dict[part_name]
        durations = duration_dict[part_name]

        for n, d in zip(notes, durations):
            if n == 'rest':
                p.append(note.Rest(quarterLength=d))
            else:
                p.append(note.Note(n, quarterLength=d))

        score.append(p)

    return score


def build_pitch_vocab(low='E2', high='C5'):
    """
    Builds a pitch vocabulary from low to high (inclusive),
    including accidentals (sharps and flats) without duplicates.
    Also includes a 'rest' token.
    """
    low_midi = pitch.Pitch(low).midi
    high_midi = pitch.Pitch(high).midi

    seen = set()
    pitches = []

    for midi_num in range(low_midi, high_midi + 1):
        p = pitch.Pitch(midi=midi_num)
        name = p.nameWithOctave
        if name not in seen:
            seen.add(name)
            pitches.append(name)

    # Add 'rest' token at the start
    pitch_vocab = ['rest'] + pitches
    return pitch_vocab


def encode_sequences(note_dict, duration_dict):
    """
    Encodes note names and durations to integer sequences.

    Args:
        note_dict (dict): {part: [note_name or 'rest']}
        duration_dict (dict): {part: [duration as float]}

    Returns:
        pitch2idx (dict), duration2idx (dict),
        encoded_notes (dict), encoded_durations (dict)
    """
    # Build full pitch vocabulary
    pitch2idx = {p: i for i, p in enumerate(pitch_vocab)}

    # Build unique duration vocabulary from all parts
    all_durations = set()
    for dlist in duration_dict.values():
        all_durations.update(dlist)
    duration_vocab = sorted(all_durations)
    duration2idx = {d: i for i, d in enumerate(duration_vocab)}

    # Encode sequences
    encoded_notes = {}
    encoded_durations = {}

    for part in note_dict:
        encoded_notes[part] = [pitch2idx.get(n, 0) for n in note_dict[part]]
        encoded_durations[part] = [duration2idx[d] for d in duration_dict[part]]

    return pitch2idx, duration2idx, encoded_notes, encoded_durations

