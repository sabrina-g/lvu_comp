import pandas as pd
from scipy.stats import chi2_contingency

# Creates a contingency table with specified input file and categorical variables
# may want to read in data in separate function later

def create_contingency_table(input_file_name, category_1, category_2):
  # Reads in data with specified file name
  data = pd.read_csv('data/'+input_file_name+'.csv') 
  
  # Creates contingency table with specified categorical variables
  contingency_table = pd.crosstab(data[category_1], data[category_2])
   
  return contingency_table


# Runs chi2 test on contingency table created from specified input file and categorical variables
# would like users to be able to provide contigency table if they prefer to full data

def lvu_chi2(input_file_name, category_1, category_2): 
  # Creates contingency table
  contingency_table = create_contingency_table(input_file_name, category_1, category_2)
  
  # Prints contingency table. Will replace with print function for all output later
  print(contingency_table)
 
  # Performs Chi2 test
  chi2, p, dof, expected = chi2_contingency(contingency_table)
  
  #print(f"Chi2: {chi2}") # will replace with print function for all output later

  return chi2, p, dof, expected, contingency_table

# Example usage:

test_chi2 = lvu_chi2('data2', 'Category', 'LinkedStatus')
print(test_chi2)


