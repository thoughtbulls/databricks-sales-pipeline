df = spark.read.option("header", True).csv("/mnt/raw/sales/")
df.write.format("delta").mode("append").saveAsTable("bronze.sales")
