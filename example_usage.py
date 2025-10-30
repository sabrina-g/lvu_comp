import pandas as pd
from lvu_comp import lvu_chi2, lvu_effect_size

# Example usage of lvu_chi2 function from lvu_comp 

#test_chi2 = lvu_chi2('data2', 'Category', 'LinkedStatus')
#print(test_chi2)

# Example usage of lvu_effect_size function from lvu_comp

input_file_name = 'effect_data1'
data = pd.read_csv('data/'+input_file_name+'.csv')
category = 1

(d, linked_n, unlinked_n, linked_true_n, unlinked_false_n, linked_true_cat_n, unlinked_false_cat_n, 
 prop_linked_true_cat, prop_unlinked_false_cat) = lvu_effect_size(data, category)

print(linked_true_n)
print(linked_true_cat_n)
print(f"d statistic: {d}")

