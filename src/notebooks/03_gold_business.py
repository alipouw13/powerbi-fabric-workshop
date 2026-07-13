# Fabric notebook - Gold business tables (housing workshop)
# Small, report-ready aggregates the Direct Lake semantic model and Copilot sit
# on. Keep Gold intentionally thin: business-friendly grains, friendly names.

from pyspark.sql import functions as F

fact = spark.table("fact_home_sales")
dim_region = spark.table("dim_region")
dim_date = spark.table("dim_date")
dim_ptype = spark.table("dim_property_type")

base = (
    fact.join(dim_region, "region_id")
    .join(dim_date, "date_id")
    .join(dim_ptype, "property_type_id")
)

# gold_market_summary: metro x month x property type, the headline grid
gold_market_summary = base.select(
    "region", "state", "period_begin", "year", "month_name", "property_type",
    "median_sale_price", "homes_sold", "new_listings", "inventory",
    "months_of_supply", "median_days_on_market", "avg_sale_to_list",
    "sold_above_list_share",
)
gold_market_summary.write.mode("overwrite").format("delta").saveAsTable("gold_market_summary")

# gold_region_latest: most recent month per metro (All Residential) for ranking
latest = base.filter(F.col("property_type") == "All Residential")
maxdate = latest.agg(F.max("period_begin")).first()[0]
gold_region_latest = (
    latest.filter(F.col("period_begin") == maxdate)
    .select("region", "state", "median_sale_price", "homes_sold",
            "months_of_supply", "median_days_on_market", "sold_above_list_share")
)
gold_region_latest.write.mode("overwrite").format("delta").saveAsTable("gold_region_latest")

print("Gold complete: gold_market_summary, gold_region_latest")
print("Build the Direct Lake semantic model on these in Lab 6.")
