import pandas as pd


input_file_name = 'effect_data1'
data = pd.read_csv('data/'+input_file_name+'.csv')
category = 1

# Function to calculate counts needed for proportions and d statistic

def get_counts(data, category):

    # Calculate counts of linked/unlinked, true/missed matches, and category-specific counts
    linked_n = len(data[data['LinkedStatus'] == 1])
    unlinked_n = len(data[data['LinkedStatus'] == 0])

    linked_true_n = len(data[(data['LinkedStatus'] == 1) & (data['LinkTruth'] == 1)])
    unlinked_false_n = len(data[(data['LinkedStatus'] == 0) & (data['LinkTruth'] == 0)])


    linked_true_cat_n = len(data[(data['LinkedStatus'] == 1) & (data['LinkTruth'] == 1)
                              & (data['Category'] == category)])
    unlinked_false_cat_n = len(data[(data['LinkedStatus'] == 0) & (data['LinkTruth'] == 0)
                                 & (data['Category'] == category)])

    return (linked_n, unlinked_n, linked_true_n, unlinked_false_n,
            linked_true_cat_n, unlinked_false_cat_n)

# Function to calculate proportions needed for d statistic

def get_proportions(linked_true_n, unlinked_false_n, linked_true_cat_n,
                    unlinked_false_cat_n):

    # Calculate proportion of true matches in a category / all true matches
    prop_linked_true_cat = linked_true_cat_n / (linked_true_n)

    # Calculate proportion of missed matches in a category / all missed matches
    prop_unlinked_false_cat = unlinked_false_cat_n / (unlinked_false_n)

    return prop_linked_true_cat, prop_unlinked_false_cat

# Function to calculate d statistic

def calculate_d(prop_linked_true_cat, prop_unlinked_false_cat):
    # d = (p1 - p2) / sqrt((p1 * (1 - p1) + p2 * (1 - p2)) / 2)
    # where p1 = prop_linked_true_cat and p2 = prop_unlinked_false_cat
    d = (prop_linked_true_cat - prop_unlinked_false_cat) / \
    (( (prop_linked_true_cat * (1 - prop_linked_true_cat) + 
        prop_unlinked_false_cat * (1 - prop_unlinked_false_cat)) / 2) ** 0.5)
    
    return d

# Main function to get effect size d statistic

def lvu_effect_size(data, category):

    # Get counts
    (linked_n, unlinked_n, linked_true_n, unlinked_false_n,
     linked_true_cat_n, unlinked_false_cat_n) = get_counts(data, category)

    # Get proportions
    prop_linked_true_cat, prop_unlinked_false_cat = get_proportions(
        linked_true_n, unlinked_false_n, linked_true_cat_n, unlinked_false_cat_n)

    # Calculate d statistic
    d = calculate_d(prop_linked_true_cat, prop_unlinked_false_cat)

    return (d, linked_n, unlinked_n, linked_true_n, unlinked_false_n,
            linked_true_cat_n, unlinked_false_cat_n,
            prop_linked_true_cat, prop_unlinked_false_cat)

# Example usage
d, linked_n, unlinked_n, linked_true_n, unlinked_false_n, linked_true_cat_n, unlinked_false_cat_n, prop_linked_true_cat, prop_unlinked_false_cat = lvu_effect_size(data, category)

print(linked_true_n)
print(linked_true_cat_n)
print(f"d statistic: {d}")
