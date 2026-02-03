import sys
sys.path.append("/Workspace/Shared/databricks-sales-pipeline")

import argparse
from src.config_loader import load_config
from src.silver import clean_orders_silver, de_duplication_orders_silver, transform_orders_silver
from pyspark.sql import SparkSession

parser = argparse.ArgumentParser()
parser.add_argument("--env", required=True)
args = parser.parse_args()
env = args.env
config_path = f"/Volumes/{env}_catalog/pipelines/configs/{env}.yaml"
cfg = load_config(config_path)

catalog = cfg["catalog"]
bronze_schema = cfg["schema_bronze"]
silver_schema = cfg["schema_silver"]

spark = SparkSession.builder \
    .appName("Sales Data Analysis") \
    .getOrCreate()


spark.sql(f"CREATE SCHEMA IF NOT EXISTS {catalog}.{silver_schema}")

bronze_df = spark.table(f"{catalog}.{bronze_schema}.orders")

clean_df = clean_orders_silver(bronze_df)
dedup_df = de_duplication_orders_silver(clean_df)

silver_df = transform_orders_silver(dedup_df)

silver_df.write.format("delta") \
    .mode("overwrite") \
    .saveAsTable(f"{catalog}.{silver_schema}.orders")

print(f"Silver transformation completed for env={env}")
