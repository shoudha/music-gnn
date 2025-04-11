import os
import sys
import numpy as np
import pandas as pd
from tqdm import tqdm
import random

from music21 import *

#%% All Bach Compositions summary
paths = corpus.getComposer('bach')


filepath = []
title = []
quarterlength = []
time_signature = []
measures = []
parts = []
offsets = []

for path in tqdm(paths):
   
    sBach = corpus.parse(str(path))
   
    filepath.append(str(path))
   
    title.append(sBach.getElementsByClass('Metadata')[0].title)
    offsets.append(sBach.getElementsByClass('Metadata')[0].offset)
   
    quarterlength.append(sBach.quarterLength)
   
    measures.append(len(sBach.parts[0].getElementsByClass('Measure')))
    parts.append(len(sBach.parts))
   
   
summary_df = pd.DataFrame()
summary_df['filepath'] = filepath
summary_df['title'] = title
summary_df['quarterlength'] = quarterlength
summary_df['measures'] = measures
summary_df['parts'] = parts
summary_df['offsets'] = offsets

summary_df.to_csv(r"bach_summary.csv")
