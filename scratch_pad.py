# d = (p1 - p2) / sqrt((p1 * (1 - p1) + p2 * (1 - p2)) / 2)

import pandas as pd
from lvu_comp import lvu_chi2, lvu_effect_size


def create_contingency_table(input_dataframe, category_1, category_2):
 
  # Creates contingency table with specified categorical variables
  contingency_table = pd.crosstab(input_dataframe[category_1], input_dataframe[category_2])
   
  return contingency_table



data2 = pd.read_csv('data/data2.csv') 
test_contingency_table = create_contingency_table(data2, 'Grade', 'LinkedStatus')
print(test_contingency_table)

# Example usage of lvu_chi2 function from lvu_comp 

#test_chi2 = lvu_chi2(data2, 'data2', 'Grade', 'LinkedStatus')
#print(test_chi2)