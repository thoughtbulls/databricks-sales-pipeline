# Databricks job parameter
import argparse
from pyspark.sql import SparkSession
from src.config_loader import load_config
from src.bronze import transform_orders_bronze
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType

import sys
sys.path.append("/Workspace/Shared/databricks-sales-pipeline")

parser = argparse.ArgumentParser()
parser.add_argument("--env", required=True)
args = parser.parse_args()
env = args.env


config_path = f"/Volumes/{env}_catalog/pipelines/configs/{env}.yaml"
cfg = load_config(config_path)

spark = SparkSession.builder \
    .appName("Sales Data Analysis") \
    .getOrCreate()
 

catalog = cfg["catalog"]
bronze_schema = cfg["schema_bronze"]
raw_path = cfg["raw_data_path"]
orders_file = raw_path + "/orders"

order_schema = StructType([
    StructField("order_id", IntegerType(), True),
    StructField("order_date", DateType(), True),
    StructField("order_customer", IntegerType(), True),
    StructField("order_status", StringType(), True)
])

raw_df = (
 spark.read.schema(order_schema)
    .option("header", True)
    .csv(orders_file)
)

raw_df.show()
bronze_df = transform_orders_bronze(raw_df)

bronze_df.mode("overwrite") \
  .write.format("delta") \
  .saveAsTable(f"{catalog}.{bronze_schema}.orders")

print(f"Bronze load completed for env={env}")