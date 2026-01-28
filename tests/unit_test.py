def test_clean_sales(spark):
    data = [
        (1, "2024-01-01", 100),
        (None, "2024-01-02", 200)
    ]

    df = spark.createDataFrame(
        data, ["order_id", "order_date", "amount"]
    )

    cleaned = df.filter("order_id IS NOT NULL")

    assert cleaned.count() == 1
