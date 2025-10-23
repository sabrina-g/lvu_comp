import pandas as pd


input_file_name = 'effect_data1'
data = pd.read_csv('data/'+input_file_name+'.csv')
category = 1

linked_n = len(data[data['LinkedStatus'] == 1])
print(linked_n)

linked_true_n = len(data[(data['LinkedStatus'] == 1) & (data['LinkTruth'] == 1)])

linked_true_cat_n = len(data[(data['LinkedStatus'] == 1) & (data['LinkTruth'] == 1) & (data['Category'] == category)])

print(linked_true_n)
print(linked_true_cat_n)