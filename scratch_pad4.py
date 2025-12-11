
# suggestions from co-pilot about extending output to multiple analyses

import csv
import os
import pandas as pd

def get_counts(data, category_name, category_level):

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
                              & (data[category_name] == category_level)])
    
    # false matches in category
    linked_false_cat_n = len(data[(data['LinkedStatus'] == 1) & (data['LinkTruth'] == 0)
                              & (data[category_name] == category_level)])    
    
    # missed matches in category
    unlinked_true_cat_n = len(data[(data['LinkedStatus'] == 0) & (data['LinkTruth'] == 1)
                                 & (data[category_name] == category_level)])

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

# Function to create and save output .csv file for effect size results

def lvu_effect_output(input_file_name, category_name, category_level, linked_n, unlinked_n, linked_true_n, linked_false_n,
                      unlinked_true_n, linked_true_cat_n, linked_false_cat_n, unlinked_true_cat_n,
                      prop_linked_true_cat, prop_linked_false_cat, prop_unlinked_true_cat,
                      stdiff_false, stdiff_missed):
    
    # Define output file name
    lvu_effect_results_file_name = input_file_name + '_effect_size_results.csv'

    # Make a directory for specified data set if it does not exist already
    output_folder = input_file_name + '_output'
    os.makedirs(output_folder, exist_ok=True)

    # Define file path for effect size results
    lvu_effect_results_path = os.path.join(output_folder, lvu_effect_results_file_name)

    # Define headers and values
    headers = [
        "Dataset", "Category", "Category_level", "Linked_Records", "Unlinked_Records", 
        "Correct_Matches", "False_Matches", "Missed_Matches", "Correct_in_Category",
        "False_in_Category", "Missed_in_Category", "Prop_Correct_in_Category",
        "Prop_False_in_Category", "Prop_Missed_in_Category", "Std_Diff_False",
        "Std_Diff_Missed"
    ]
    
    values = [
        input_file_name, category_name, category_level, linked_n, unlinked_n, linked_true_n, linked_false_n,
        unlinked_true_n, linked_true_cat_n, linked_false_cat_n, unlinked_true_cat_n,
        prop_linked_true_cat, prop_linked_false_cat, prop_unlinked_true_cat,
        stdiff_false, stdiff_missed
    ]
    
    # Round numeric values to 6 decimal places
    values = [round(v, 6) if isinstance(v, float) else v for v in values]

    # Check if file exists for this dataset
    if os.path.exists(lvu_effect_results_path):
        # Load existing file
        existing_df = pd.read_csv(lvu_effect_results_path)
        
        # Check for duplicates based on Category and Category_level
        duplicate = ((existing_df["Category"] == category_name) & 
                     (existing_df["Category_level"] == category_level)).any()
        
        if duplicate:
            print(f"Row with Category '{category_name}' and Category_level '{category_level}' already exists.")
            return
        
        # Append new row
        new_row_df = pd.DataFrame([values], columns=headers)
        updated_df = pd.concat([existing_df, new_row_df], ignore_index=True)
        updated_df.to_csv(lvu_effect_results_path, index=False)
    
    else:
        # Create new file with header
        new_df = pd.DataFrame([values], columns=headers)
        new_df.to_csv(lvu_effect_results_path, index=False)


# Main function to get effect sizes 

def lvu_effect_size(input_file_name, category_name, category_level):

    '''
    Calculates the standard difference (stdiff) effect sizes for false matches and missed matches.
      
    Parameters:
        input_file_name (str): Name of the input CSV file (without .csv extension) located in the
          data directory.
        category (int/str): The specific category value to calculate effect sizes for.
        
    Returns:
        - stdiff_false (float) : Standard difference effect size for false matches.
        - stdiff_missed (float) : Standard difference effect size for missed matches.
        - linked_n (int): Total number of linked records.
        - unlinked_n (int): Total number of unlinked records.
        - linked_true_n (int): Total number of correct (true) matches.
        - linked_false_n (int): Total number of false matches.
        - unlinked_true_n (int): Total number of missed matches.
        - linked_true_cat_n (int): Number of correct matches in the specified category.
        - linked_false_cat_n (int): Number of false matches in the specified category.
        - unlinked_true_cat_n (int): Number of missed matches in the specified category.
        - prop_linked_true_cat (float): Proportion of correct matches in the specified category.
        - prop_linked_false_cat (float): Proportion of false matches in the specified category.
        - prop_unlinked_true_cat (float): Proportion of missed matches in the specified category.
    
    Creates an output directory (<input_file_name>_output) and saves the following .csv file:
        <input_file_name>_effect_size_results: saves counts, proportions, and effect sizes.
        
    Input data should have the following columns:
        - LinkedStatus indicates whether the record was linked (1) or unlinked (0).
        - LinkTruth indicates whether the record is a true match (1) or not (0).
        - Category indicates the categorical variable of interest for effect size calculation.
            - Integers represent different categories (e.g., 1, 2, 3) 
        - Method will ignore all other columns. 

    Method assumes no missing values in the specified columns.

    Standard difference (stdiff) is calculated as:

    stdiff = (p1 - p2) / sqrt((p1 * (1 - p1) + p2 * (1 - p2)) / 2)
    where p1 = prop_linked_true_cat and p2 = EITHER prop_linked_false_cat (for comparing
    to false matches) OR prop_unlinked_true_cat (for comparing to missed matches)
    
            '''

    # Reads in data with specified file name
    # For multiple data sets plan to add flags to each and then combine to create 
    # suitable combined dataset
    # Can handle this with if statements to cope with different numbers of input datasets

    data = pd.read_csv('data/'+input_file_name+'.csv') 

    # Get counts
    (linked_n, unlinked_n, linked_true_n, linked_false_n, unlinked_true_n,
        linked_true_cat_n, linked_false_cat_n, unlinked_true_cat_n) = get_counts(data, category_name, category_level)

    # Get proportions
    prop_linked_true_cat, prop_linked_false_cat, prop_unlinked_true_cat = get_proportions(
        linked_true_n, linked_false_n, unlinked_true_n, linked_true_cat_n, linked_false_cat_n, 
        unlinked_true_cat_n)

    # Calculate effect size
    stdiff_false = calculate_stdiff(prop_linked_true_cat, prop_linked_false_cat)
    stdiff_missed = calculate_stdiff(prop_linked_true_cat, prop_unlinked_true_cat)

    # Create output for effect size
    lvu_effect_output(input_file_name, category_name, category_level, linked_n, unlinked_n, linked_true_n, linked_false_n,
              unlinked_true_n, linked_true_cat_n, linked_false_cat_n, unlinked_true_cat_n,
              prop_linked_true_cat, prop_linked_false_cat, prop_unlinked_true_cat,
              stdiff_false, stdiff_missed
             )

    return (stdiff_false, stdiff_missed, linked_n, unlinked_n, linked_true_n, linked_false_n, unlinked_true_n,
            linked_true_cat_n, linked_false_cat_n, unlinked_true_cat_n,
            prop_linked_true_cat, prop_linked_false_cat, prop_unlinked_true_cat)


(stdiff_false, stdiff_missed, linked_n, unlinked_n, linked_true_n, linked_false_n, unlinked_true_n, 
    linked_true_cat_n, linked_false_cat_n, unlinked_true_cat_n,
    prop_linked_true_cat, prop_linked_false_cat, prop_unlinked_true_cat) = lvu_effect_size(
        input_file_name = "effect_data1", category_name = "Marital_status", category_level = 0)