import pandas as pd
from lvu_comp import lvu_chi2, lvu_effect_size

data2 = pd.read_csv('data/data2.csv') 

# Example usage of lvu_chi2 function from lvu_comp 

test_chi2 = lvu_chi2(data2, 'data2', 'Grade', 'LinkedStatus')
print(test_chi2)



