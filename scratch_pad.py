# d = (p1 - p2) / sqrt((p1 * (1 - p1) + p2 * (1 - p2)) / 2)
# where p1 and p2 are proportions
# e.g., p of true matches from linked data nad p of missed matches from unlinked data

# recode y and n into 1 and 0 if needed?
# df['Response'] = df['Response'].map({'yes': 1, 'no': 0})

import pandas as pd
from scipy.stats import chi2_contingency

# Creates a contingency table with specified input file and categorical variables

def create_contingency_table(input_file_name, category_1, category_2):
  # Reads in data with specified file name
  data = pd.read_csv('data/'+input_file_name+'.csv') # may want to read in data in separate function later
  
  # Creates contingency table with specified categorical variables
  contingency_table = pd.crosstab(data[category_1], data[category_2])
   
  return contingency_table

contingency_table = create_contingency_table('data3', 'Category', 'LinkedStatus')
print(contingency_table)