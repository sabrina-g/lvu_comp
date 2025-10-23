import pandas as pd


input_file_name = 'effect_data1'
data = pd.read_csv('data/'+input_file_name+'.csv')
category = 1

# Calculate counts of linked/unlinked, true/missed matches, and category-specific counts
linked_n = len(data[data['LinkedStatus'] == 1])
unlinked_n = len(data[data['LinkedStatus'] == 0])

linked_true_n = len(data[(data['LinkedStatus'] == 1) & (data['LinkTruth'] == 1)])
unlinked_false_n = len(data[(data['LinkedStatus'] == 0) & (data['LinkTruth'] == 0)])


linked_true_cat_n = len(data[(data['LinkedStatus'] == 1) & (data['LinkTruth'] == 1)
                              & (data['Category'] == category)])
unlinked_false_cat_n = len(data[(data['LinkedStatus'] == 0) & (data['LinkTruth'] == 0)
                                 & (data['Category'] == category)])

# Calculate proportion of true matches in a category / all true matches
prop_linked_true_cat = linked_true_cat_n / (linked_true_n)

# Calculate proportion of missed matches in a category / all missed matches
prop_unlinked_false_cat = unlinked_false_cat_n / (unlinked_false_n)

# Calculate d statistic
# d = (p1 - p2) / sqrt((p1 * (1 - p1) + p2 * (1 - p2)) / 2)
# where p1 = prop_linked_true_cat and p2 = prop_unlinked_false_cat

d = (prop_linked_true_cat - prop_unlinked_false_cat) / \
    (( (prop_linked_true_cat * (1 - prop_linked_true_cat) + 
        prop_unlinked_false_cat * (1 - prop_unlinked_false_cat)) / 2) ** 0.5)

print(linked_true_n)
print(linked_true_cat_n)
print(f"d statistic: {d}")
