from pyspark.sql import DataFrame
from pyspark.sql.functions import count, col

def aggregate_orders_gold(df: DataFrame) -> DataFrame:
    """
    Silver → Gold aggregation
    """
    return (
        df
        .groupBy("order_date")
        .agg(
            count("order_id").alias("total_orders"),
            count(col("order_customer_id")).alias("total_customers")
        )
    )