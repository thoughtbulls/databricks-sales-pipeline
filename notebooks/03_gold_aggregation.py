import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--env", required=True)
args = parser.parse_args()

env = args.env


import sys

sys.path.append("/Workspace/Shared/databricks-sales-pipeline")

from src.config_loader import load_config_from_string
from pyspark.sql.functions import sum, count

config_path = f"/Volumes/{env}_catalog/pipelines/configs/{env}.yaml"

raw = spark.read.text(config_path)
raw_yaml = "\n".join([r.value for r in raw.collect()])
cfg = load_config_from_string(raw_yaml) 

catalog = cfg["catalog"]
silver_schema = cfg["schema_silver"]
gold_schema = cfg["schema_gold"]

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{gold_schema}")

df = spark.table(f"{catalog}.{silver_schema}.orders")

fact_orders = (
    df.groupBy("order_date")
      .agg(
          count("order_id").alias("order_count")
      )
)

fact_orders.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable(f"{catalog}.{gold_schema}.fact_orders")

print(f"Gold aggregation completed for env={env}")
