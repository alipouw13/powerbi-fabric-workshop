# Fabric notebook - Silver transform (housing workshop)
# Turns Bronze into a conformed star schema: clean types, build the dimensions
# and the fact at region x period x property_type grain. This is the "model the
# data as a star" step a Tableau extract usually skips.

from pyspark.sql import functions as F

# ---- dimensions ------------------------------------------------------------
mt = spark.table("bronze_market_tracker")

dim_region = (
    mt.select("region", "state", "region_type").dropDuplicates()
    .withColumn("region_id", F.monotonically_increasing_id() + 1)
)
dim_region.write.mode("overwrite").format("delta").saveAsTable("dim_region")

dim_property_type = (
    mt.select("property_type").dropDuplicates()
    .withColumn("property_type_id", F.monotonically_increasing_id() + 1)
)
dim_property_type.write.mode("overwrite").format("delta").saveAsTable("dim_property_type")

dim_date = (
    mt.select("period_begin", "period_end", "year", "month_name").dropDuplicates()
    .withColumn("date_id", F.monotonically_increasing_id() + 1)
    .withColumn("period_begin", F.to_date("period_begin"))
    .withColumn("period_end", F.to_date("period_end"))
)
dim_date.write.mode("overwrite").format("delta").saveAsTable("dim_date")

# ---- fact at region x period x property_type -------------------------------
fact = (
    mt.join(dim_region, ["region", "state", "region_type"])
    .join(dim_property_type, ["property_type"])
    .join(dim_date.select("period_begin", "date_id"),
          mt.period_begin == F.col("period_begin"))
    .select(
        "region_id", "date_id", "property_type_id",
        F.col("median_sale_price").cast("double"),
        F.col("homes_sold").cast("int"),
        F.col("new_listings").cast("int"),
        F.col("inventory").cast("int"),
        F.col("months_of_supply").cast("double"),
        F.col("median_days_on_market").cast("int"),
        F.col("median_ppsf").cast("double"),
        F.col("avg_sale_to_list").cast("double"),
        F.col("sold_above_list_share").cast("double"),
    )
)
fact.write.mode("overwrite").format("delta").saveAsTable("fact_home_sales")

print("Silver complete: dim_region, dim_property_type, dim_date, fact_home_sales")
print("Next: 03_gold_business.py")
