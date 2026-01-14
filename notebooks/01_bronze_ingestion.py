# Databricks job parameter
dbutils.widgets.text("env", "dev")
env = dbutils.widgets.get("env")

from src.config_loader import load_config

cfg = load_config(env)

bronze_schema = cfg["schema_bronze"]
raw_path = cfg["raw_data_path"]

spark.sql(f"CREATE SCHEMA IF NOT EXISTS {bronze_schema}")

df = (
    spark.read
    .option("header", True)
    .csv(raw_path)
)

df.write.format("delta") \
  .mode("append") \
  .saveAsTable(f"{bronze_schema}.sales")

print(f"Bronze load completed for env={env}")
