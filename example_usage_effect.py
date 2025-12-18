import pandas as pd
from lvu_comp import lvu_effect_size

# Read in example data

effect_data1 = pd.read_csv('data/effect_data1.csv')

# Example usage of lvu_effect_size function from lvu_comp

(stdiff_false, stdiff_missed, linked_n, unlinked_n, linked_true_n, linked_false_n, unlinked_true_n, 
    linked_true_cat_n, linked_false_cat_n, unlinked_true_cat_n,
    prop_linked_true_cat, prop_linked_false_cat, prop_unlinked_true_cat) = lvu_effect_size(
        effect_data1, input_data_name = "effect_data1", category_name = "Marital_status", category_level = 0)

print(f"True matches: {linked_true_n}")
#print(f"True matches for Category = {category}: {linked_true_cat_n}")
print(f"Missed matches: {unlinked_true_n}")
#print(f"Missed matches for Category = {category}: {unlinked_true_cat_n}")
print(f"Standard difference between true matches and missed matches: {stdiff_missed}")

