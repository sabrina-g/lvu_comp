
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
  
  # Performs Chi2 test
  chi2, p, dof, expected = chi2_contingency(contingency_table)

  # Creates output file for chi2 results
  lvu_chi2_output(chi2, p, dof, input_file_name, contingency_table, expected)

  return chi2, p, dof, expected, contingency_table

# example usage

chi2, p, dof, expected, contingency_table = lvu_chi2('data2', 'Category', 'LinkedStatus')

