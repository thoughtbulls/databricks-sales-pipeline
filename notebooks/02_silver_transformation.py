dbutils.widgets.text("env", "dev")
env = dbutils.widgets.get("env")

from src.config_loader import load_config
from pyspark.sql.functions import col, row_number
from pyspark.sql.window import Window

cfg = load_config(env)

bronze_schema = cfg["schema_bronze"]
silver_schema = cfg["schema_silver"]

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {silver_schema}")

df = spark.table(f"{bronze_schema}.sales")

clean_df = (
    df.dropna(subset=["order_id"])
      .withColumn("amount", col("amount").cast("double"))
)

window = Window.partitionBy("order_id").orderBy(col("updated_at").desc())

dedup_df = (
    clean_df
    .withColumn("rn", row_number().over(window))
    .filter("rn = 1")
    .drop("rn")
)

dedup_df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable(f"{silver_schema}.sales")

print(f"Silver transformation completed for env={env}")
