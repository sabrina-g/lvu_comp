import pandas as pd
from scipy.stats import chi2_contingency

# Creates a contingency table with specified input file and categorical variables
# To use in lvu_chi2 function
# may want to read in data in separate function later

def create_contingency_table(input_file_name, category_1, category_2):
  # Reads in data with specified file name
  data = pd.read_csv('data/'+input_file_name+'.csv') 
  
  # Creates contingency table with specified categorical variables
  contingency_table = pd.crosstab(data[category_1], data[category_2])
   
  return contingency_table


# Main function to run chi2 test on contingency table created from specified input 
# file and categorical variables
# would like users to be able to provide contigency table if they prefer to full data

def lvu_chi2(input_file_name, category_1, category_2): 
  # Creates contingency table
  contingency_table = create_contingency_table(input_file_name, category_1, category_2)
  
  # Prints contingency table. Will replace with print function for all output later
  print(contingency_table)
 
  # Performs Chi2 test
  chi2, p, dof, expected = chi2_contingency(contingency_table)
  
  #print(f"Chi2: {chi2}") # will replace with print function for all output later

  return chi2, p, dof, expected, contingency_table


# Function to calculate counts needed for proportions and effect size
# To use with lvu_effect_size function

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

# Function to calculate proportions needed for effect size
# To use with lvu_effect_size function

def get_proportions(linked_true_n, unlinked_false_n, linked_true_cat_n,
                    unlinked_false_cat_n):

    # Calculate proportion of true matches in a category / all true matches
    prop_linked_true_cat = linked_true_cat_n / \
        (linked_true_n) if linked_true_n > 0 else 0

    # Calculate proportion of missed matches in a category / all missed matches
    prop_unlinked_false_cat = unlinked_false_cat_n / \
        (unlinked_false_n) if unlinked_false_n > 0 else 0

    return prop_linked_true_cat, prop_unlinked_false_cat

# Function to calculate effect size
# To use with lvu_effect_size function

def calculate_d(prop_linked_true_cat, prop_unlinked_false_cat):
    # d = (p1 - p2) / sqrt((p1 * (1 - p1) + p2 * (1 - p2)) / 2)
    # where p1 = prop_linked_true_cat and p2 = prop_unlinked_false_cat
    d = (prop_linked_true_cat - prop_unlinked_false_cat) / \
    (( (prop_linked_true_cat * (1 - prop_linked_true_cat) + 
        prop_unlinked_false_cat * (1 - prop_unlinked_false_cat)) / 2) ** 0.5)
    
    return d

# Main function to get effect size 

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


