def test_clean_sales(spark):
    data = [(1, "100"), (None, "200")]
    df = spark.createDataFrame(data, ["order_id", "amount"])

    from src.transformations import clean_sales
    result = clean_sales(df)
    assert result.count() == 1
    