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
               'E2': 1, 
               'F2': 2, 
               'G-2': 3, 
               'G2': 4, 
               'A-2': 5, 
               'A2': 6, 
               'B-2': 7, 
               'B2': 8, 
               'C3': 9, 
               'D-3': 10, 
               'D3': 11, 
               'E-3': 12, 
               'E3': 13, 
               'F3': 14, 
               'G-3': 15, 
               'G3': 16, 
               'A-3': 17, 
               'A3': 18, 
               'B-3': 19, 
               'B3': 20, 
               'C4': 21, 
               'D-4': 22, 
               'D4': 23, 
               'E-4': 24, 
               'E4': 25, 
               'F4': 26, 
               'G-4': 27, 
               'G4': 28, 
               'A-4': 29, 
               'A4': 30, 
               'B-4': 31, 
               'B4': 32, 
               'C5': 33, 
               'cont':34}


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

def extract_notes_and_durations_cont(score, time_step=0.25):
    """
    Extract aligned note and duration sequences from a music21 Score.
    Long notes are split into time_step units using 'cont<NoteName>' markers.

    Args:
        score (music21.stream.Score): Input Score.
        time_step (float): Temporal resolution (e.g., 0.5 = eighth notes).

    Returns:
        (note_dict, duration_dict): Dicts of aligned note names and durations.
    """
    note_dict = {}
    duration_dict = {}
    part_duration = {}
    min_dur = 100.

    for part in score.parts:
        part_id = part.id or f"Part{len(note_dict)+1}"
        note_dict[part_id] = []
        duration_dict[part_id] = []
        part_duration[part_id] = 0.
        
        
        cur_min_dur = min([s.quarterLength for s in part.recurse().notesAndRests])
        if cur_min_dur < min_dur:
            min_dur = cur_min_dur
            
        for n in part.recurse().notesAndRests:
                        
            dur = n.quarterLength
            if dur == 0.:
                continue
            
            part_duration[part_id] += dur
            steps = int(dur / time_step)
            if steps < 1:
                steps = 1

            if n.isRest:
                note_name = 'rest'
            elif n.isNote:
                if '#' in n.pitch.name:
                    n.pitch = n.pitch.getEnharmonic()
                if n.pitch.name == 'F-':
                    n.pitch.name = 'E'
                if n.pitch.name == 'C-':
                    n.pitch.name = 'B'
                note_name = n.nameWithOctave
            else:
                # print('What is this!')
                pass

            note_dict[part_id].append(note_name)
            duration_dict[part_id].append(time_step)

            for _ in range(1, steps):
                if n.isRest:
                    cont_token = note_name
                elif n.isNote:
                    cont_token = f"cont{note_name}"
                note_dict[part_id].append(cont_token)
                duration_dict[part_id].append(time_step)
                

    return note_dict, duration_dict, part_duration, min_dur



def reconstruct_score_cont(note_dict, time_step=0.25):
    """
    Reconstruct a music21 Score from note_dict with 'cont<Note>' tokens.

    Args:
        note_dict (dict): {part_name: [note names or 'rest' or 'cont<Note>']}
        time_step (float): Duration of each time step.

    Returns:
        music21.stream.Score
    """
    from music21 import stream, note

    score = stream.Score()

    for part_name in note_dict:
        p = stream.Part()
        p.id = part_name
        p.partName = part_name.capitalize()

        notes = note_dict[part_name]
        i = 0
        while i < len(notes):
            symbol = notes[i]
            if symbol.startswith('cont'):
                i += 1
                continue

            # Determine how long this note continues
            dur = time_step
            j = i + 1
            while j < len(notes) and notes[j] == f'cont{symbol}':
                dur += time_step
                j += 1

            if symbol == 'rest':
                p.append(note.Rest(quarterLength=dur))
            else:
                p.append(note.Note(symbol, quarterLength=dur))

            i = j

        score.append(p)

    return score


def get_normalized_note_names(low='E2', high='C7'):
    """
    Get all note names in the given range, replacing sharps/double-sharps
    with flat or natural equivalents.
    
    Args:
        low (str): Lowest note (e.g., 'E2')
        high (str): Highest note (e.g., 'C7')
    
    Returns:
        List of unique note names with flats/naturals only.
    """
    low_midi = pitch.Pitch(low).midi
    high_midi = pitch.Pitch(high).midi

    note_names = []

    for midi_num in range(low_midi, high_midi + 1):
        p = pitch.Pitch(midi=midi_num)
        # Convert sharp/double-sharp notes to their flat/natural enharmonic equivalent
        if '#' in p.name:
            p = p.getEnharmonic()

        note_names.append(p.nameWithOctave)
        note_names.append('cont'+p.nameWithOctave)
        

    # Remove duplicates and sort
    return sorted(set(note_names))




def get_total_duration_per_part(score):
    """
    Computes the total duration (in quarterLength) of all parts in a score.

    Args:
        score (music21.stream.Score)

    Returns:
        part_durations (dict): {part_id: total_duration}
        total_duration_all_parts (float): optional grand total
    """
    part_durations = {}

    for part in score.parts:
        part_id = part.id or f"Part{len(part_durations)+1}"
        total = 0.0

        for n in part.recurse().notesAndRests:
            total += n.quarterLength

        part_durations[part_id] = total

    total_duration_all_parts = sum(part_durations.values())
    return part_durations, total_duration_all_parts


def remove_substring_from_list_of_lists(data, substring):
    """
    Removes strings from a list of lists that contain a given substring.

    Args:
        data: A list of lists, where each inner list contains strings.
        substring: The substring to check for.

    Returns:
        A new list of lists with strings containing the substring removed.
    """

    result = []
    for inner_list in data:
        new_inner_list = []
        for string in inner_list:
            if substring not in string:  # Changed the logic to keep strings without the substring
                new_inner_list.append(string)
        result.append(new_inner_list)
    return result

