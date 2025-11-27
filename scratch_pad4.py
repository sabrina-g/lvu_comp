
# suggestions from co-pilot about extending output to multiple analyses

import csv
import os
import pandas as pd
from scipy.stats import chi2_contingency

def create_contingency_table(input_file_name, category_1, category_2):
    # Reads in data with specified file name
    data = pd.read_csv('data/' + input_file_name + '.csv')
    
    # Creates contingency table with specified categorical variables
    contingency_table = pd.crosstab(data[category_1], data[category_2])
    
    return contingency_table


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

def lvu_chi2(input_file_name, category_1=None, category_2=None, contingency_table=None):
    '''
    Performs Chi2 test on contingency table or creates one from specified input file and categorical variables.
    '''
    # Use provided contingency table or create one
    if contingency_table is None:
        contingency_table = create_contingency_table(input_file_name, category_1, category_2)

    # Perform Chi2 test
    chi2, p, dof, expected = chi2_contingency(contingency_table)

    # Save outputs
    lvu_chi2_output(chi2, p, dof, input_file_name, category_1, category_2, contingency_table, expected)

    return chi2, p, dof, expected, contingency_table

test_chi2 = lvu_chi2('data2', 'Grade', 'LinkedStatus')
