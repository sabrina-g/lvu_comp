
import csv
import os
import pandas as pd
from scipy.stats import chi2_contingency


def get_counts(data, category):

    # Calculate counts of linked/unlinked, true/missed matches, and category-specific counts
    linked_n = len(data[data['LinkedStatus'] == 1])
    unlinked_n = len(data[data['LinkedStatus'] == 0])

    # true matches
    linked_true_n = len(data[(data['LinkedStatus'] == 1) & (data['LinkTruth'] == 1)])

    # false matches: did link (LinkStatus = 1) but should not have (LinkTruth = 0)
    linked_false_n = len(data[(data['LinkedStatus'] == 1) & (data['LinkTruth'] == 0)])
    
    # missed matches: did not link (LinkStatus = 0) but should have (LinkTruth = 1)
    unlinked_true_n = len(data[(data['LinkedStatus'] == 0) & (data['LinkTruth'] == 1)])

    # true matches in category
    linked_true_cat_n = len(data[(data['LinkedStatus'] == 1) & (data['LinkTruth'] == 1)
                              & (data['Category'] == category)])
    
    # false matches in category
    linked_false_cat_n = len(data[(data['LinkedStatus'] == 1) & (data['LinkTruth'] == 0)
                              & (data['Category'] == category)])    
    
    # missed matches in category
    unlinked_true_cat_n = len(data[(data['LinkedStatus'] == 0) & (data['LinkTruth'] == 1)
                                 & (data['Category'] == category)])

    return (linked_n, unlinked_n, linked_true_n, linked_false_n, unlinked_true_n,
            linked_true_cat_n, linked_false_cat_n, unlinked_true_cat_n)

# Function to calculate proportions needed for effect size
# To use with lvu_effect_size function

def get_proportions(linked_true_n, linked_false_n, unlinked_true_n, linked_true_cat_n, linked_false_cat_n,
                    unlinked_true_cat_n):

    # Calculate proportion of true matches in a category / all true matches
    prop_linked_true_cat = linked_true_cat_n / \
        (linked_true_n) if linked_true_n > 0 else 0
    
    # Calculate proportion of false matches in a category / all false matches
    prop_linked_false_cat = linked_false_cat_n / \
        (linked_false_n) if linked_false_n > 0 else 0
    

    # Calculate proportion of missed matches in a category / all missed matches
    prop_unlinked_true_cat = unlinked_true_cat_n / \
        (unlinked_true_n) if unlinked_true_n > 0 else 0

    return prop_linked_true_cat, prop_linked_false_cat, prop_unlinked_true_cat

# Function to calculate effect size
# To use with lvu_effect_size function

def calculate_stdiff(p1, p2):

    # stdiff = (p1 - p2) / sqrt((p1 * (1 - p1) + p2 * (1 - p2)) / 2)
    # where p1 = prop_linked_true_cat and p2 = EITHER prop_linked_false_cat 
    # OR prop_unlinked_true_cat

    # Calculate standard difference
    stdiff = (p1 - p2) / (( (p1 * (1 - p1) + \
        p2 * (1 - p2)) / 2) ** 0.5)
     
    return stdiff

def lvu_effect_output():
    
    #replace with actual output code later
    descriptions = ["Item A", "Item B", "Item C"]
    values = [10, 20, 30]

    # Create DataFrame
    df = pd.DataFrame({
        "Description": descriptions,
        "Value": values
    })


    return

# Main function to get effect sizes 

def lvu_effect_size(data, category):

    # Get counts
    (linked_n, unlinked_n, linked_true_n, linked_false_n, unlinked_true_n,
        linked_true_cat_n, linked_false_cat_n, unlinked_true_cat_n) = get_counts(data, category)

    # Get proportions
    prop_linked_true_cat, prop_linked_false_cat, prop_unlinked_true_cat = get_proportions(
        linked_true_n, linked_false_n, unlinked_true_n, linked_true_cat_n, linked_false_cat_n, 
        unlinked_true_cat_n)

    # Calculate effect size

    stdiff_false = calculate_stdiff(prop_linked_true_cat, prop_linked_false_cat)
    stdiff_missed = calculate_stdiff(prop_linked_true_cat, prop_unlinked_true_cat)

    # Create output for effect size

    return (stdiff_false, stdiff_missed, linked_n, unlinked_n, linked_true_n, linked_false_n, unlinked_true_n,
            linked_true_cat_n, linked_false_cat_n, unlinked_true_cat_n,
            prop_linked_true_cat, prop_linked_false_cat, prop_unlinked_true_cat)
