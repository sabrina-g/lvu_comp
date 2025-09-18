# reads in contingency table from a CSV file and performs a Chi-squared test of independence.

import pandas as pd
from scipy.stats import chi2_contingency

def perform_chi2_test(input_file_name):

    # Reads in data with the specified file name. 
    # Ensure data is in a contingency table format. 
    # If there is a column for category labels, name it 'Category' 
    data = pd.read_csv('data/'+input_file_name+'.csv')

    # Drops unnecessary columns if any (e.g., category labels)
    contingency_table = data.drop(columns=['Category']).values

    # Performs Chi-squared test
    chi2, p, dof, expected = chi2_contingency(contingency_table)

    
    return chi2, p, dof, expected

#Example usage:

chi2, p, dof, expected = perform_chi2_test('contingency_table')

print(f"Chi-squared Statistic: {chi2}")
print(f"P-value: {p}")
print(f"Degrees of Freedom: {dof}")
print("Expected Frequencies:")
print(expected)
