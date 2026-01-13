from src.transformations import clean_sales

df = spark.table("bronze.sales")
df_clean = clean_sales(df)
df_clean.write.format("delta").mode("overwrite").saveAsTable("silver.sales")
