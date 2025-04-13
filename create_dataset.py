import os
import sys
import random
import torch
import numpy as np
import pandas as pd
from tqdm import tqdm

from music21 import corpus

import util

#%% Paramters
time_step = 0.25
notes_vocab = util.get_normalized_note_names(low='C2', high='C6')
n_vocab = len(notes_vocab)

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
# paths = corpus.getComposer('bach')

# for path in paths:
   
#     sBach = corpus.parse(str(path))
#     if len(sBach.parts) == 4:
#         break

# # Show piece in MuseScore Studio
# # sBach.show()

# # Play in a media player
# sBach.show('midi')

# # Extract notes and durations
# note_dict, duration_dict = util.extract_notes_and_durations_cont(sBach)

# # Reconstruct the score from the notes and duration dicts
# new_score = util.reconstruct_score_cont(note_dict, )
# new_score.show('midi')

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




#%% All Bach Compositions encoded notes

# note to index
ntoi = {}
ntoi = {notes_vocab[i]:i+2 for i in range(len(notes_vocab))}
ntoi['.'] = 0
ntoi['rest'] = 1

# index to note
iton = {value:key for key, value in ntoi.items()}

# Get all bach chorales with four parts
paths = corpus.getComposer('bach')
chorale_parts = ['Soprano', 'Alto', 'Tenor', 'Bass']
all_bachs = {}

# paths = [r'C:/Users/14694/.pyenv/pyenv-win/versions/3.9.13/Lib/site-packages/music21/corpus/bach/bwv299.mxl']

for i, path in enumerate(paths):
    
    sBach = corpus.parse(str(path))
    sBach_parts = [s.partName for s in sBach.parts]
    
    has_parts = [s in sBach_parts for s in chorale_parts]
    
    if all(has_parts):
        
        # Extract all part notes and convert durations to 0.125
        note_dict, duration_dict, part_duration, min_dur = \
                    util.extract_notes_and_durations_cont(sBach, time_step=time_step)
                    
        # Skip if time_step is larger than minimum duration
        if min_dur < time_step:
            continue
        
        # Take only SATB parts
        note_dict = {key: note_dict[key] for key in chorale_parts}
        
        # Reconstruct the score back from note_dict
        # sBach_recon = util.reconstruct_score_cont(note_dict)
        
        # Make sure all parts have same length of 0.125 durations
        first_length = len(next(iter(note_dict.values())))
        assert all(len(lst) == first_length for lst in note_dict.values()) 
                
        all_bachs[i] = {}
        all_bachs[i]['note_dict'] = note_dict

# Convert notes in dictionary to indices
soprano_all = []
alto_all = []
tenor_all = []
bass_all = []

for key, value in all_bachs.items():
    
    cur_note_dict = value['note_dict']
    
    soprano_cur = [ntoi[s] for s in cur_note_dict['Soprano']]
    soprano_cur = [0] + soprano_cur + [0]
    
    alto_cur = [ntoi[s] for s in cur_note_dict['Alto']]
    alto_cur = [0] + alto_cur + [0]
    
    tenor_cur = [ntoi[s] for s in cur_note_dict['Tenor']]
    tenor_cur = [0] + tenor_cur + [0]
    
    bass_cur = [ntoi[s] for s in cur_note_dict['Bass']]
    bass_cur = [0] + bass_cur + [0]
    
    soprano_all.append(soprano_cur)
    alto_all.append(alto_cur)
    tenor_all.append(tenor_cur)
    bass_all.append(bass_cur)

#%% Create parts by sampling

# Soprano
N_soprano = torch.zeros((len(ntoi), len(ntoi)), dtype=torch.int32)
for sp_lst in soprano_all:
    for n1, n2 in zip(sp_lst, sp_lst[1:]):
        N_soprano[n1, n2] += 1

ix = 0
soprano_smp = []
while True:
    p = N_soprano[ix, :].float()
    p = p / sum(p)
    ix = torch.multinomial(p, num_samples=1, replacement=True).item()
    if ix == 0:
        break
    soprano_smp.append(ix)

# # Alto
# N_alto = torch.zeros((len(ntoi), len(ntoi)), dtype=torch.int32)
# for sp_lst in soprano_all:
#     for n1, n2 in zip(sp_lst, sp_lst[1:]):
#         N_alto[n1, n2] += 1

# ix = 0
# alto_smp = []
# while True:
#     p = N_alto[ix, :].float()
#     p = p / sum(p)
#     ix = torch.multinomial(p, num_samples=1, replacement=True).item()
#     alto_smp.append(ix)
    
# Convert back to note_dict
notes_dict_sampled = {'Soprano' : [iton[s] for s in soprano_smp],
                      }
sBach_smp = util.reconstruct_score_cont(notes_dict_sampled)
sBach_smp.show('midi')