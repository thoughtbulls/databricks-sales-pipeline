dbutils.widgets.text("env", "dev")
env = dbutils.widgets.get("env")

from src.config_loader import load_config
from pyspark.sql.functions import sum, count

cfg = load_config(env)

silver_schema = cfg["schema_silver"]
gold_schema = cfg["schema_gold"]

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {gold_schema}")

df = spark.table(f"{silver_schema}.sales")

fact_sales = (
    df.groupBy("order_date")
      .agg(
          sum("amount").alias("total_sales"),
          count("order_id").alias("order_count")
      )
)

fact_sales.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable(f"{gold_schema}.fact_sales")

print(f"Gold aggregation completed for env={env}")
