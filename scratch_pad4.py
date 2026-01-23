from pyspark.sql import SparkSession

def create_local_spark_session(app_name="LocalSparkApp", master="local[*]"):
    """
    Creates and returns a local SparkSession.
    
    Parameters:
        app_name (str): Name of the Spark application.
        master (str): Spark master URL. 'local[*]' uses all available CPU cores.
    
    Returns:
        SparkSession: Configured Spark session object.
    """
    try:
        spark = (
            SparkSession.builder
            .appName(app_name)
            .master(master)
            # Optional configurations
            .config("spark.sql.shuffle.partitions", "4")  # Reduce shuffle partitions for local mode
            .config("spark.driver.memory", "2g")          # Set driver memory
            .getOrCreate()
        )
        print(f"✅ Spark session started: {spark.version}")
        return spark
    except Exception as e:
        print(f"❌ Failed to start Spark session: {e}")
        raise

if __name__ == "__main__":
    # Create Spark session
    spark = create_local_spark_session()

    # Example: Create a DataFrame
    data = [("Alice", 25), ("Bob", 30), ("Charlie", 35)]
    df = spark.createDataFrame(data, ["Name", "Age"])
    df.show()

    # Stop Spark session
    spark.stop()
    print("🛑 Spark session stopped.")




# Read a CSV file
#data2 = spark.read.option("header", True).option("inferSchema", True).csv("file:///data/data2.csv")