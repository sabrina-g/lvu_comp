import pandas as pd
from lvu_comp import lvu_chi2, lvu_effect_size

# Example usage of lvu_chi2 function from lvu_comp 

#test_chi2 = lvu_chi2('data2', 'Category', 'LinkedStatus')
#print(test_chi2)

# Example usage of lvu_effect_size function from lvu_comp

(stdiff_false, stdiff_missed, linked_n, unlinked_n, linked_true_n, linked_false_n, unlinked_true_n, 
    linked_true_cat_n, linked_false_cat_n, unlinked_true_cat_n,
    prop_linked_true_cat, prop_linked_false_cat, prop_unlinked_true_cat) = lvu_effect_size(
        input_file_name = "effect_data1", category = 1)

print(f"True matches: {linked_true_n}")
#print(f"True matches for Category = {category}: {linked_true_cat_n}")
print(f"Missed matches: {unlinked_true_n}")
#print(f"Missed matches for Category = {category}: {unlinked_true_cat_n}")
print(f"Standard difference between true matches and missed matches: {stdiff_missed}")

