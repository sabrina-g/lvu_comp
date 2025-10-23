import pandas as pd


input_file_name = 'effect_data1'
data = pd.read_csv('data/'+input_file_name+'.csv')
category = 1

# Function to create DataFrames needed for counts and proportions

def make_dfs(data, category):
    # Create separate df for linked and unlinked records
    df_linked = data[data['LinkedStatus'] == 1]
    df_unlinked = data[data['LinkedStatus'] == 0]

    # Create separate df of true matches assuming 1 = true
    df_linked_true = df_linked[df_linked['LinkTruth'] == 1]

    # Create separate df of missed matches assuming 0 = false 
    df_unlinked_false = df_unlinked[df_unlinked['LinkTruth'] == 0]

    # Create separate df of True matches within specified category
    df_linked_true_cat = df_linked_true[df_linked_true['Category'] == category]

    # Create separate df of Missed matches within specified category
    df_unlinked_false_cat = df_unlinked_false[df_unlinked_false['Category'] == category]

    return df_linked, df_unlinked, df_linked_true, df_unlinked_false, df_linked_true_cat, df_unlinked_false_cat

# Function to get counts needed for proportions
# Need to add a check so it doesn't try to divide by zero later

def get_counts(df_linked, df_unlinked, df_linked_true, df_unlinked_false, df_linked_true_cat, df_unlinked_false_cat):

    # Numbers of linked and unlinked records
    linked_n = len(df_linked)
    unlinked_n = len(df_unlinked)

    # Number of true matches overall
    linked_true_n = len(df_linked_true)

    # Number of missed matches overall
    unlinked_false_n = len(df_unlinked_false)

    # Number of true matches within specified category
    linked_true_cat_n = len(df_linked_true_cat)

    # Number of missed matches within specified category
    unlinked_false_cat_n = len(df_unlinked_false_cat)

    return linked_n, unlinked_n, linked_true_n, unlinked_false_n, linked_true_cat_n, unlinked_false_cat_n

# Function to get proportions needed for d statistic

def get_proportions(linked_true_n, unlinked_false_n, linked_true_cat_n, unlinked_false_cat_n):

    # Proportion of true matches within specified category / overall true matches
    prop_linked_true_cat = linked_true_cat_n / (linked_true_n)

    # Proportion of missed matches within specified category / overall missed matches
    prop_unlinked_false_cat = unlinked_false_cat_n / (unlinked_false_cat_n)

    return prop_linked_true_cat, prop_unlinked_false_cat
    

# Example usages of make_dfs, get_counts, and get_proportions functions

df_linked, df_unlinked, df_linked_true, df_unlinked_false, df_linked_true_cat, df_unlinked_false_cat = make_dfs(data, category)
linked_n, unlinked_n, linked_true_n, unlinked_false_n, linked_true_cat_n, unlinked_false_cat_n = get_counts(df_linked, df_unlinked, df_linked_true, df_unlinked_false, df_linked_true_cat, df_unlinked_false_cat)
prop_linked_true_cat, prop_unlinked_false_cat = get_proportions(linked_true_n, unlinked_false_n, linked_true_cat_n, unlinked_false_cat_n)

print(f"Number of true matches in category {category}: {linked_true_cat_n}")
print(f"Number of missed matches in category {category}: {unlinked_false_cat_n}")
print(f"Number of linked records: {linked_n}")
print(f"Proportion of true matches in category {category}: {prop_linked_true_cat}")