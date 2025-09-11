# trying to make the chi2.py file more modular by putting the function in its own file

import pandas as pd

def create_contingency_table(input_file_name, category_1, category_2):
    
    # Reads in data with specified file name
    data = pd.read_csv('data/'+input_file_name+'.csv')

    # Creates contingency table with specified categorical variables
    contingency_table = pd.crosstab(data[category_1], data[category_2])

    return contingency_table