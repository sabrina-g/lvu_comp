import pandas as pd
from scipy.stats import chi2_contingency

# Creates a contingency table with specified input file and categorical variables

def create_contingency_table(input_file_name, category_1, category_2):
  # Reads in data with specified file name
  data = pd.read_csv('data/'+input_file_name+'.csv')
  
  # Creates contingency table with specified categorical variables
  contingency_table = pd.crosstab(data[category_1], data[category_2])

  # Drops unecessary columns if any (e.g., category labels)
  #contingency_table = data.drop(columns=['Category']).values
   
  return contingency_table

#example_contingency = create_contingency_table('data', 'Category', 'LinkedStatus')

#print(example_contingency)

def lvu_chi2(input_file_name, category_1, category_2):
  # Creates contingency table
  contingency_table = create_contingency_table(input_file_name, category_1, category_2)
  
  print(contingency_table)
  # this contigency table part is working fine as can print it out

  # Performs Chi2 test
  # This bit is causing a type error when I try to call the lvu_chi2 function
  # problem was dropping columns in contingency table creation

  chi2, p, dof, expected = chi2_contingency(contingency_table)
  
  print(f"Chi2: {chi2}")

  return chi2, p, dof, expected

test_chi2 = lvu_chi2('data', 'Category', 'LinkedStatus')
#print(test_chi2)