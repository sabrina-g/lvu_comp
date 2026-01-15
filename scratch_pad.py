# d = (p1 - p2) / sqrt((p1 * (1 - p1) + p2 * (1 - p2)) / 2)

import pandas as pd
from lvu_comp import lvu_chi2, lvu_effect_size


import csv
import os
import pandas as pd
from scipy.stats import chi2_contingency

# Creates a contingency table with specified input file and categorical variables
# To use in lvu_chi2 function
# may want to read in data in separate function later

def create_contingency_table(input_dataframe, category_1, category_2):
 
  # Creates contingency table with specified categorical variables
  contingency_table = pd.crosstab(input_dataframe[category_1], input_dataframe[category_2])
   
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

def lvu_chi2(input_dataframe, input_file_name, category_1, category_2): 
  '''
  Performs Chi2 test on contingency table created from specified input dataframe and categorical variables.

  Parameters:
    input_dataframe (DataFrame): The input DataFrame.
    input_file_name (str): Name of the input file used for output file naming.
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
  contingency_table = create_contingency_table(input_dataframe, category_1, category_2)
  
  # Prints contingency table. Will replace with print function for all output later
  print(contingency_table)
 
  # Performs Chi2 test
  chi2, p, dof, expected = chi2_contingency(contingency_table)

  # Creates output file for chi2 results
  lvu_chi2_output(chi2, p, dof, input_file_name, contingency_table, expected)
  
  return chi2, p, dof, expected, contingency_table