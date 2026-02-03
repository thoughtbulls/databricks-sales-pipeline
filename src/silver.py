from pyspark.sql import DataFrame
from pyspark.sql.functions import col, to_date, row_number
from pyspark.sql.window import Window

VALID_STATUSES = ["COMPLETE", "CLOSED"]

def transform_orders_silver(df: DataFrame) -> DataFrame:
    """
    Bronze → Silver transformation
    """
    
    silver_df = df \
        .filter(col("order_status").isin(VALID_STATUSES)) \
        .withColumn("order_date", to_date(col("order_date"))) \
        .filter(col("order_date").isNotNull())
    
    return silver_df

def clean_orders_silver(df: DataFrame)-> DataFrame:
    clean_df = (
    df.dropna(subset=["order_id"])
    )

    return clean_df
    
def de_duplication_orders_silver(clean_df: DataFrame)-> DataFrame:
    window = Window.partitionBy("order_id").orderBy(col("order_date").desc())

    dedup_df = (
    clean_df
    .withColumn("rn", row_number().over(window))
    .filter("rn = 1")
    .drop("rn")
    )

    return dedup_df
    
