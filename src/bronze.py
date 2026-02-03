from pyspark.sql import DataFrame
from pyspark.sql.functions import col, current_timestamp

def transform_orders_bronze(df: DataFrame)-> DataFrame:
    """
    RAW -> bronze transformation
    """
    bronze_df = df.dropDuplicates(["order_id"]) \
    .withColumn("order_id", col("order_id").cast("int")) \
    .withColumn("order_date", col("order_date").cast("date"))\
    .withColumn("order_customer_id", col("order_customer_id").cast("int")) \
    .withColumn("order_status", col("order_status").cast("string")) \
    .withColumn("ingested_at", current_timestamp())
    
    return bronze_df