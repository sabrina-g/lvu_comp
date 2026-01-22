# co pilot example of psypark crosstabs

from pyspark.sql import SparkSession
from pyspark.sql.utils import AnalysisException

def create_contingency_table(df, col1, col2):
    """
    Create a contingency table (crosstab) between two categorical columns in a PySpark DataFrame.

    Args:
        df (DataFrame): Input PySpark DataFrame.
        col1 (str): First column name (rows).
        col2 (str): Second column name (columns).

    Returns:
        DataFrame: Contingency table with counts.
    """
    # Validate inputs
    if not col1 or not col2:
        raise ValueError("Both column names must be provided.")
    if col1 not in df.columns or col2 not in df.columns:
        raise ValueError(f"Columns '{col1}' and/or '{col2}' not found in DataFrame.")

    try:
        # Create contingency table
        contingency_df = df.crosstab(col1, col2)
        return contingency_df
    except AnalysisException as e:
        raise RuntimeError(f"Error creating contingency table: {e}")

# ------------------ Example Usage ------------------
if __name__ == "__main__":
    spark = SparkSession.builder \
        .appName("ContingencyTableExample") \
        .getOrCreate()

    # Sample data
    data = [
        ("A", "X"),
        ("A", "Y"),
        ("B", "X"),
        ("B", "X"),
        ("A", "X"),
        ("C", "Y"),
    ]
    columns = ["Category1", "Category2"]

    df = spark.createDataFrame(data, columns)

    # Create contingency table
    contingency_df = create_contingency_table(df, "Category1", "Category2")

    # Show result
    contingency_df.show()

    spark.stop()
