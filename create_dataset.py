import os
import sys
import random
import numpy as np
import pandas as pd
from tqdm import tqdm

from music21 import *

import util

#%% All Bach Compositions summary
# paths = corpus.getComposer('bach')

# filepath = []
# title = []
# quarterlength = []
# time_signature = []
# measures = []
# parts = []
# offsets = []

# for path in tqdm(paths):
   
#     sBach = corpus.parse(str(path))
   
#     filepath.append(str(path))
   
#     title.append(sBach.getElementsByClass('Metadata')[0].title)
#     offsets.append(sBach.getElementsByClass('Metadata')[0].offset)
   
#     quarterlength.append(sBach.quarterLength)
   
#     measures.append(len(sBach.parts[0].getElementsByClass('Measure')))
#     parts.append(len(sBach.parts))
   
   
# summary_df = pd.DataFrame()
# summary_df['filepath'] = filepath
# summary_df['title'] = title
# summary_df['quarterlength'] = quarterlength
# summary_df['measures'] = measures
# summary_df['parts'] = parts
# summary_df['offsets'] = offsets

# summary_df.to_csv(r"bach_summary.csv")

#%% Play a 4-part Bach chorale
paths = corpus.getComposer('bach')

for path in paths:
   
    sBach = corpus.parse(str(path))
    if len(sBach.parts) == 4:
        break

# Show piece in MuseScore Studio
# sBach.show()

# Play in a media player
sBach.show('midi')

# Extract notes and durations
note_dict, duration_dict = util.extract_notes_and_durations_cont(sBach)

# Reconstruct the score from the notes and duration dicts
new_score = util.reconstruct_score_cont(note_dict, )
new_score.show('midi')

#%% Create a 4 part chorale and play it
# note_dict_rnd, duration_dict_rnd = util.generate_random_note_and_duration_dicts(
#     ['soprano', 'alto', 'tenor', 'bass'],
#     {'soprano': 10, 'bass': 10, 'tenor': 10, 'alto': 10}
#     )

# # Reconstruct the score from the notes and duration dicts
# new_score_rnd = util.reconstruct_score(note_dict_rnd, duration_dict_rnd)
# new_score_rnd.show('midi')

# # Encode the notes and durations dictionaries
# pitch2idx, duration2idx, enc_notes, enc_durations = util.encode_sequences(note_dict, duration_dict)

# print("Pitch Vocabulary:", pitch2idx)
# print("Duration Vocabulary:", duration2idx)
# print("Encoded Notes:", enc_notes)
# print("Encoded Durations:", enc_durations)



































