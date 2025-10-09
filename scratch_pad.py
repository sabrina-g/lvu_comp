# d = (p1 - p2) / sqrt((p1 * (1 - p1) + p2 * (1 - p2)) / 2)
# where p1 and p2 are proportions
# e.g., p of true matches from linked data nad p of missed matches from unlinked data

# recode y and n into 1 and 0 if needed?
# df['Response'] = df['Response'].map({'yes': 1, 'no': 0})

# below is copied from co-pilot as suggested code to split dataframes

import pandas as pd
input_file_name = 'effect_data1'
data = pd.read_csv('data/'+input_file_name+'.csv') # may want to read in data in separate function later

# Split DataFrame into two NumPy arrays based on the 'label' column
def split_dataframe_by_label(df, label_column):
    # Validate input
    if label_column not in df.columns:
        raise ValueError(f"Column '{label_column}' not found in DataFrame.")
    if not set(df[label_column].unique()).issubset({0, 1}):
        raise ValueError(f"Column '{label_column}' must be dichotomous (contain only 0 and 1).")
    
    # Split into two DataFrames
    df_0 = df[df[label_column] == 0].drop(columns=[label_column])
    df_1 = df[df[label_column] == 1].drop(columns=[label_column])
    
    # Convert to NumPy arrays
    array_0 = df_0.to_numpy()
    array_1 = df_1.to_numpy()
    
    return array_0, array_1

# Usage
array_0, array_1 = split_dataframe_by_label(df, 'label')

# Output the results
print("Array for label=0:")
print(array_0)
print("\nArray for label=1:")
print(array_1)