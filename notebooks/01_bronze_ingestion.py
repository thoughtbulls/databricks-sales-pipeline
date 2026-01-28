# Databricks job parameter
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--env", required=True)
args = parser.parse_args()

env = args.env


import sys

sys.path.append("/Workspace/Shared/databricks-sales-pipeline")

from src.config_loader import load_config_from_string
from pyspark.sql.functions import current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType

config_path = f"/Volumes/{env}_catalog/pipelines/configs/{env}.yaml"

raw = spark.read.text(config_path)
raw_yaml = "\n".join([r.value for r in raw.collect()])
cfg = load_config_from_string(raw_yaml) 

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

df = (
 spark.read.schema(order_schema)
    .option("header", True)
    .csv(orders_file)
)

display(df)

df.withColumn("ingesttime", current_timestamp()) \
  .write.format("delta") \
  .mode("overwrite") \
  .saveAsTable(f"{catalog}.{bronze_schema}.orders")

print(f"Bronze load completed for env={env}")