import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--env", required=True)
args = parser.parse_args()

env = args.env


import sys

sys.path.append("/Workspace/Shared/databricks-sales-pipeline")

from src.config_loader import load_config_from_string
from pyspark.sql.functions import col, row_number
from pyspark.sql.window import Window

config_path = f"/Volumes/{env}_catalog/pipelines/configs/{env}.yaml"

raw = spark.read.text(config_path)
raw_yaml = "\n".join([r.value for r in raw.collect()])
cfg = load_config_from_string(raw_yaml) 

catalog = cfg["catalog"]
bronze_schema = cfg["schema_bronze"]
silver_schema = cfg["schema_silver"]

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{silver_schema}")

df = spark.table(f"{catalog}.{bronze_schema}.orders")

clean_df = (
    df.dropna(subset=["order_id"])
    #   .withColumn("amount", col("amount").cast("double"))
)

window = Window.partitionBy("order_id").orderBy(col("order_date").desc())

dedup_df = (
    clean_df
    .withColumn("rn", row_number().over(window))
    .filter("rn = 1")
    .drop("rn")
)

dedup_df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable(f"{catalog}.{silver_schema}.orders")

print(f"Silver transformation completed for env={env}")
