import csv
import os
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

# Creates a directory and output files for chi2 test results
# To use in lvu_chi2 function

def lvu_chi2_output(chi2, p, dof, input_file_name, contingency_table, expected):  

    # Define output file name
    chi2_results_file_name = input_file_name+'_chi2_results.csv'
    contingency_table_file_name = input_file_name+'_contingency_table.csv'
    expected_frequencies_file_name = input_file_name+'_expected_frequencies.csv'
    output_folder = input_file_name+'_output'

    # Make a directory for specified data set if it does not exist already
    os.makedirs(output_folder, exist_ok=True)

    # Define file path for chi2 results
    chi2_results_path = os.path.join(output_folder, chi2_results_file_name)

    # Define the headers and corresponding values for chi2 results
    headers = ["Chi Square", "P value", "Degrees of Freedom"]
    values = [chi2, p, dof]

    # Write chi2 results to CSV    
    with open(chi2_results_path, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerow(values)

    # Define file path for contingency table
    contingency_table_path = os.path.join(output_folder, contingency_table_file_name)

    # Write contingency table to CSV
    contingency_table.to_csv(contingency_table_path)

    # Define file path for expected frequencies
    expected_frequencies_path = os.path.join(output_folder, expected_frequencies_file_name)

    # Write expected frequencies to CSV
    pd.DataFrame(expected).to_csv(expected_frequencies_path)
    

    return

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

  # Creates output file for chi2 results
  lvu_chi2_output(chi2, p, dof, input_file_name, contingency_table, expected)
  
  return chi2, p, dof, expected, contingency_table


# Function to calculate counts needed for proportions and effect size
# To use with lvu_effect_size function
# The data will likely come from 2 separate files for each error type bc of how the clerical review happens

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

    return (stdiff_false, stdiff_missed, linked_n, unlinked_n, linked_true_n, linked_false_n, unlinked_true_n,
            linked_true_cat_n, linked_false_cat_n, unlinked_true_cat_n,
            prop_linked_true_cat, prop_linked_false_cat, prop_unlinked_true_cat)


    