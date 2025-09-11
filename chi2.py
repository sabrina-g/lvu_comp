import pandas as pd
from scipy.stats import chi2_contingency

# Reads in data with the specified file name. 
# Ensure data is in a contingency table format. 
# If there is a column for category labels, name it 'Category' 
input_file_name = 'contingency_table'
data = pd.read_csv('data/'+input_file_name+'.csv')


# Drops unecessary columns if any (e.g., category labels)
contingency_table = data.drop(columns=['Category']).values


# Performs Chi-squared test
chi2, p, dof, expected = chi2_contingency(contingency_table)

# Outputs results
print(f"Chi-squared Statistic: {chi2}")
print(f"P-value: {p}")
print(f"Degrees of Freedom: {dof}")
print("Expected Frequencies:")
print(expected)