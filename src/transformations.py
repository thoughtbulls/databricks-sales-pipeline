from pyspark.sql.functions import col

def clean_sales(df):
    return df.dropna(subset=["order_id"]) \
             .withColumn("amount", col("amount").cast("double"))
