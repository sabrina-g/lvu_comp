import pandas as pd
from lvu_comp import lvu_chi2, lvu_effect_size

# Example usage of lvu_chi2 function from lvu_comp 

#test_chi2 = lvu_chi2('data2', 'Category', 'LinkedStatus')
#print(test_chi2)

# Example usage of lvu_effect_size function from lvu_comp

input_file_name = 'effect_data1'
data = pd.read_csv('data/'+input_file_name+'.csv')
category = 1

(stdiff_missed, stdiff_false, linked_n, unlinked_n, linked_true_n, unlinked_true_n, linked_true_cat_n, unlinked_true_cat_n, 
 prop_linked_true_cat, prop_unlinked_true_cat) = lvu_effect_size(data, category)

print(f"True matches: {linked_true_n}")
print(f"True matches for Category = {category}: {linked_true_cat_n}")
print(f"Missed matches: {unlinked_true_n}")
print(f"Missed matches for Category = {category}: {unlinked_true_cat_n}")
print(f"Standard difference between true matches and missed matches: {stdiff_missed}")

