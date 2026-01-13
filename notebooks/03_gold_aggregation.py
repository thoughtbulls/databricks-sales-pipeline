from pyspark.sql.functions import sum

df = spark.table("silver.sales")

fact = df.groupBy("order_date") \
         .agg(sum("amount").alias("total_sales"))

fact.write.format("delta").mode("overwrite").saveAsTable("gold.fact_sales")
