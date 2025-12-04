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

def lvu_chi2_output(chi2, p, dof, input_file_name, category_1, category_2, contingency_table, expected):
    # Output folder
    output_folder = input_file_name + '_output'
    os.makedirs(output_folder, exist_ok=True)

    # Chi2 results file path
    chi2_results_path = os.path.join(output_folder, input_file_name + '_chi2_results.csv')

    # Prepare row for results
    result_row = [input_file_name, category_1, category_2, chi2, p, dof]

    # Check if file exists
    file_exists = os.path.exists(chi2_results_path)

    # Read existing rows to check for duplicates
    existing_rows = set()
    if file_exists:
        with open(chi2_results_path, mode='r', newline='') as file:
            reader = csv.reader(file)
            next(reader, None)  # Skip header
            for row in reader:
                if len(row) >= 3:
                    existing_rows.add((row[0], row[1], row[2]))  # Dataset, Category 1, Category 2

    # Only write a new row if this combination doesn't exist
    if (input_file_name, category_1, category_2) not in existing_rows:
        with open(chi2_results_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            if not file_exists: # create the file if it doesn't already exist
                writer.writerow(["Dataset", "Category 1", "Category 2", "Chi Square", "P value", "Degrees of Freedom"])
            writer.writerow(result_row)


    # Save contingency and expected tables with descriptive names
    contingency_filename = f"contingency_{input_file_name}_{category_1}_{category_2}.csv"
    expected_filename = f"expected_{input_file_name}_{category_1}_{category_2}.csv"

    contingency_table.to_csv(os.path.join(output_folder, contingency_filename))
    pd.DataFrame(expected, index=contingency_table.index, columns=contingency_table.columns).to_csv(
        os.path.join(output_folder, expected_filename)
    )
    
    return

# Main function to run chi2 test on contingency table created from specified input 
# file and categorical variables
# would like users to be able to provide contigency table if they prefer to full data

def lvu_chi2(input_file_name, category_1, category_2): 
  '''
  Performs Chi2 test on contingency table created from specified input file and categorical variables.

  Parameters:
    input_file_name (str): Name of the input CSV file (without .csv extension) located in the 'data' directory.
    category_1 (str): Name of the first categorical variable/column in the data.
    category_2 (str): Name of the second categorical variable/column in the data.

  Returns:
    - chi2 (float): The Chi-squared statistic.
    - p (float): The p-value of the test.
    - dof (int): Degrees of freedom.
    - expected (ndarray): The expected frequencies table.
    - contingency_table (DataFrame): The contingency table used in the test.

  Creates an output directory (<input_file_name>_output) and saves the following .csv files:
    <input_file_name>_chi2_results: saves dataset, category_1, category_2, chi2, p-value, degrees of freedom
    <input_file_name_category1_category2>_contingency_table: saves the contingency table
    <input_file_name_category1_category2>_expected_frequencies: saves the expected frequencies table 

    - Multiple analyses run on the same dataset will be saved as new rows in chi2_results
    - Multiple analyses will generate separate contingency and expected frequencies tables .csv files

  Input data should have at least 2 categorical variables/columns for analysis.
    - Input data can be int (e.g., 0/1) or string (e.g., 'Linked'/'Unlinked').
    - One of the columns should represent the linked status (whether the data in that
    row were linked or not linked). 
    - The other column(s) should represent categorical variables of interest to
    investigate for potential bias.
    - The method will ignore any columns not specified in the function call.

   Method assumes no missing values in the specified categorical variables/columns.

    '''
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
        - <input_file_name>_effect_size_results: saves category, category level, counts, proportions, 
        and effect sizes.
        - Multiple analyses run on the same dataset will be saved as new rows in effect_size_results.
        
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


