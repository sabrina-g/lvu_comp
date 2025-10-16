import pandas as pd


input_file_name = 'effect_data1'
data = pd.read_csv('data/'+input_file_name+'.csv')

# Create separate df for linked and unlinked records
df_linked = data[data['LinkedStatus'] == 1]
df_unlinked = data[data['LinkedStatus'] == 0]

# Create separate df of true matches assuming 1 = true
df_linked_true = df_linked[df_linked['LinkTruth'] == 1]

# Create separate df of missed matches assuming 0 = false 
df_unlinked_false = df_unlinked[df_unlinked['LinkTruth'] == 0]

# Create separate df of True matches within specified category, e.g., Category = 1
df_linked_true_cat_1 = df_linked_true[df_linked_true['Category'] == 1]

# Create separate df of Missed matches within specified category, e.g., Category = 1
df_unlinked_false_cat_1 = df_unlinked_false[df_unlinked_false['Category'] == 1]

# Numbers of linked and unlinked records
linked_n = len(df_linked)
unlinked_n = len(df_unlinked)

# Number of true matches within specified category
linked_true_cat_1_n = len(df_linked_true_cat_1)

# Number of missed matches within specified category
unlinked_false_cat_1_n = len(df_unlinked_false_cat_1)


print(f"Number of true matches in category 1: {linked_true_cat_1_n}")
print(f"Number of missed matches in category 1: {unlinked_false_cat_1_n}")
print(f"Number of linked records: {linked_n}")