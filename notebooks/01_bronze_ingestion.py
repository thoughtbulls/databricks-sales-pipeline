# Databricks job parameter
dbutils.widgets.text("env", "dev")
env = dbutils.widgets.get("env")

import sys

sys.path.append("/Workspace/Shared/databricks-sales-pipeline")

from src.config_loader import load_config
from pyspark.sql.functions import current_timestamp
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, DateType


# load_config = dbutils.import_notebook('src.config_loader').load_config  // for notebook only
cfg = load_config(env) 

catalog = cfg["catalog"]
bronze_schema = cfg["schema_bronze"]
raw_path = cfg["raw_data_path"]
orders_file = raw_path + "/orders"

order_schema = StructType(
    StructField("order_id", IntegerType),
    StructField("order_date", DateType),
    StructField("order_customer", IntegerType),
    StructField("order_status", StringType)
)

df = (
 spark.read.schema(order_schema)
    .option("header", True)
    .csv(orders_file)
)

display(df)

df.withColumn("ingesttime", current_timestamp()) \
  .write.format("delta") \
  .mode("append") \
  .saveAsTable(f"{catalog}.{bronze_schema}.orders")

print(f"Bronze load completed for env={env}")