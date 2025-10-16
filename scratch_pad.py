# d = (p1 - p2) / sqrt((p1 * (1 - p1) + p2 * (1 - p2)) / 2)
# where p1 and p2 are proportions
# e.g., p of true matches from linked data nad p of missed matches from unlinked data

# recode y and n into 1 and 0 if needed?
# df['Response'] = df['Response'].map({'yes': 1, 'no': 0})

# below is copied from co-pilot as suggested code to split dataframes

import pandas as pd


input_file_name = 'effect_data1'
data = pd.read_csv('data/'+input_file_name+'.csv')

# Split DataFrame into two based on the 'label' column

def split_dataframe_by_label(df, label_column):
    if label_column not in df.columns:
        raise ValueError(f"Column '{label_column}' not found in DataFrame.")
    #if not set(df[label_column].unique()).issubset({0, 1}): # uncomment if want to enforce dichotomous
       # raise ValueError(f"Column '{label_column}' must be dichotomous (contain only 0 and 1).")
    
    df_0 = df[df[label_column] == 0] #could drop label column but like it for validation purposes now
    df_1 = df[df[label_column] == 1]    
    
    
    return df_0, df_1

df_0, df_1 = split_dataframe_by_label(data, 'LinkedStatus')

print(df_0)

def create_all_splits(df, linked_column, truth_column, category_column):

    # First split by linked status
    df_unlinked, df_linked = split_dataframe_by_label(df, linked_column)

    # Then split each of those by truth status

    df_unlinked_false, df_unlinked_true = split_dataframe_by_label(df_unlinked, truth_column)
    df_linked_false, df_linked_true = split_dataframe_by_label(df_linked, truth_column)

    # Finally split each of those by category status - currently only works for dichotomous categories
    df_unlinked_false_cat_0, df_unlinked_false_cat_1 = split_dataframe_by_label(df_unlinked_false, category_column)
    df_unlinked_true_cat_0, df_unlinked_true_cat_1 = split_dataframe_by_label(df_unlinked_true, category_column)
    df_linked_false_cat_0, df_linked_false_cat_1 = split_dataframe_by_label(df_linked_false, category_column)
    df_linked_true_cat_0, df_linked_true_cat_1 = split_dataframe_by_label(df_linked_true, category_column)


    # Return all eight DataFrames
    return (df_unlinked, df_linked, df_unlinked_false, df_unlinked_true, df_linked_false, df_linked_true, df_unlinked_false_cat_0, 
            df_unlinked_false_cat_1, df_unlinked_true_cat_0, df_unlinked_true_cat_1, 
            df_linked_false_cat_0, df_linked_false_cat_1, df_linked_true_cat_0, df_linked_true_cat_1
    )

df_unlinked, df_linked, df_unlinked_false, df_unlinked_true, df_linked_false, df_linked_true, df_unlinked_false_cat_0, df_unlinked_false_cat_1, df_unlinked_true_cat_0, df_unlinked_true_cat_1, df_linked_false_cat_0, df_linked_false_cat_1, df_linked_true_cat_0, df_linked_true_cat_1 = create_all_splits(data, 'LinkedStatus', 'LinkTruth', 'Category')

print(df_linked_true.value_counts())


"""""
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
print(array_1) """
