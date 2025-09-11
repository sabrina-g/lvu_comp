import pandas as pd

# Specifcy the file name 
input_file_name = 'data'

# Specify two categorical variable column names for contingency table
Category_1 = 'Category'
Category_2 = 'LinkedStatus'

# Reads in data with specified file name
data = pd.read_csv('data/'+input_file_name+'.csv')

# Creates contingency table with specified categorical variables
contingency_table = pd.crosstab(data[Category_1], data[Category_2])

# Prints contingency table
print(contingency_table)

# Saves contingency table to CSV
#contingency_table.to_csv('data/'+input_file_name+'_contingency_table.csv')