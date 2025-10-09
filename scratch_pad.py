# d = (p1 - p2) / sqrt((p1 * (1 - p1) + p2 * (1 - p2)) / 2)
# where p1 and p2 are proportions
# e.g., p of true matches from linked data nad p of missed matches from unlinked data

# recode y and n into 1 and 0 if needed?
# df['Response'] = df['Response'].map({'yes': 1, 'no': 0})

import pandas as pd
input_file_name = 'effect_data'
data = pd.read_csv('data/'+input_file_name+'.csv') # may want to read in data in separate function later