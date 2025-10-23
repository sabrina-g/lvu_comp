import pandas as pd


input_file_name = 'effect_data1'
data = pd.read_csv('data/'+input_file_name+'.csv')
category = 1

linked_n = len(data[data['LinkedStatus'] == 1])
print(linked_n)

linked_true_n = len(data[(data['LinkedStatus'] == 1) & (data['LinkTruth'] == 1)])
unlinked_false_n = len(data[(data['LinkedStatus'] == 0) & (data['LinkTruth'] == 0)])


linked_true_cat_n = len(data[(data['LinkedStatus'] == 1) & (data['LinkTruth'] == 1)
                              & (data['Category'] == category)])
unlinked_false_cat_n = len(data[(data['LinkedStatus'] == 0) & (data['LinkTruth'] == 0)
                                 & (data['Category'] == category)])

prop_linked_true_cat = linked_true_cat_n / (linked_true_n)
prop_unlinked_false_cat = unlinked_false_cat_n / (unlinked_false_n)

print(linked_true_n)
print(linked_true_cat_n)