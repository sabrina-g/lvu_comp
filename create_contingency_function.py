# reads in a dataset from a CSV file and creates a contingency table based on two specified categorical variables.

import pandas as pd

def create_contingency_table(input_file_name, category_1, category_2):
    
    # Reads in data with specified file name
    data = pd.read_csv('data/'+input_file_name+'.csv')

    # Creates contingency table with specified categorical variables
    contingency_table = pd.crosstab(data[category_1], data[category_2])

    # Saves contingency table to CSV
    contingency_table.to_csv('data/'+input_file_name+'_contingency_table.csv')

    return contingency_table

# Example usage:

