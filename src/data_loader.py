from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import pandas as pd
import os

def get_spark_session():
    """Initializes and returns a PySpark session."""
    return SparkSession.builder \
        .appName("IPL Stats Analyser") \
        .master("local[*]") \
        .getOrCreate()

def load_with_pyspark(data_path):
    """Loads and cleans data using PySpark for Big Data processing."""
    try:
        spark = get_spark_session()
        df = spark.read.csv(data_path, header=True, inferSchema=True)
        # Drop rows with missing critical information
        df_clean = df.na.drop(subset=["winner", "team1", "team2", "toss_winner"])
        return df_clean
    except Exception as e:
        print(f"PySpark Loading Failed (Java may not be installed). Error: {e}")
        return None

def load_with_pandas(data_path):
    """Fallback method to load data using Pandas when PySpark is unavailable."""
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at {data_path}")
    df = pd.read_csv(data_path)
    df_clean = df.dropna(subset=["winner", "team1", "team2", "toss_winner"])
    return df_clean

if __name__ == "__main__":
    # Test loading
    data_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "matches.csv")
    print("Attempting to load data with Pandas (Fallback mode)...")
    df = load_with_pandas(data_file)
    print(f"Successfully loaded {len(df)} rows.")
