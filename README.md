# LVU_COMP
#### A tool for identifying potential bias in linked datasets

## This tool is in development and should not be used for the purpose of identifying potential bias

LVU_COMP, or linked versus unlinked comparisons contains two methods for identifying potential bias in linked data. The first tool is lvu_chi2, which compares the distribution of a categorical variable in linked data to its distribution in unlinked data. The second tool is lvu_effect, which looks at the magnitude of the difference between the proportion of a particular level of a categorical variable (relative to the total across all levels) in true matches compared to false or missed matches. These two methods are described in more detail below. 

#### lvu_chi2 performs Chi2 test on a contingency table created from specified input dataframe and categorical variables.

    Parameters:
    - input_dataframe (DataFrame): The input DataFrame.
    - input_file_name (str): Name of the input file used for output file naming.
    - category_1 (str): Name of the first categorical variable/column in the data.
    - category_2 (str): Name of the second categorical variable/column in the data.

    Returns:
    - chi2 (float): The Chi-squared statistic. 
    - p (float): The p-value of the test.
    - dof (int): Degrees of freedom.
    - expected (ndarray): The expected frequencies table.
    - contingency_table (DataFrame): The contingency table used in the test.

    Creates an output directory (<input_file_name>_output) and saves the following .csv files:
    - <input_file_name>_chi2_results: saves dataset, category_1, category_2, chi2, p-value, degrees of freedom
    - <input_file_name_category1_category2>_contingency_table: saves the contingency table
    - <input_file_name_category1_category2>_expected_frequencies: saves the expected frequencies table 

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

#### lvu_effect calculates standard difference (stdiff) effect sizes for false matches and missed matches compared to true matches.
      
    Parameters:
    - input_dataframe (str): Name of the dataframe containing the target variables for effect size calculation
    - input_data_name (str): Name of the input dataset for output file naming. 
    - category_name (int/str): The name of the categorical variable/column to analyze.
    - category_level (int/str): The specific category value to calculate effect sizes for.
        
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
    
    Creates an output directory (<input_data_name>_output) and saves the following .csv file:
    - <input_data_name>_effect_size_results: saves category, category level, counts, proportions, 
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
