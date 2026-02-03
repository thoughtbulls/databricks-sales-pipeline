import sys
sys.path.append("/Workspace/Shared/databricks-sales-pipeline")

import argparse
from src.config_loader import load_config
from src.gold import aggregate_orders_gold
from pyspark.sql import SparkSession


parser = argparse.ArgumentParser()
parser.add_argument("--env", required=True)
args = parser.parse_args()
env = args.env

config_path = f"/Volumes/{env}_catalog/pipelines/configs/{env}.yaml"
cfg = load_config(config_path) 

catalog = cfg["catalog"]
silver_schema = cfg["schema_silver"]
gold_schema = cfg["schema_gold"]

spark = SparkSession.builder \
    .appName("Sales Data Analysis") \
    .getOrCreate()



spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{gold_schema}")

silver_df = spark.table(f"{catalog}.{silver_schema}.orders")

fact_orders = aggregate_orders_gold(silver_df)

fact_orders.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable(f"{catalog}.{gold_schema}.fact_orders")

print(f"Gold aggregation completed for env={env}")
