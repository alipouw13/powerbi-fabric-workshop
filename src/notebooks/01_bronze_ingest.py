# Fabric notebook - Bronze ingest (housing workshop)
# Reads the raw CSVs uploaded to the Lakehouse Files area and lands them as
# Bronze Delta tables, unchanged, with lineage columns. Run in a Fabric
# notebook attached to the Lakehouse `lh_housing`.
#
# Bronze rule: land raw, do not clean. Cleaning happens in Silver (notebook 02).

from pyspark.sql import functions as F

RAW = "Files/raw"  # where Lab 0 / Lab 5 lands the CSVs

SOURCES = {
    "bronze_market_tracker": f"{RAW}/redfin/market_tracker.csv",
    "bronze_listings": f"{RAW}/mls/listings.csv",
}


def ingest(table_name: str, path: str) -> None:
    df = (
        spark.read.option("header", True)
        .option("inferSchema", True)
        .csv(path)
        .withColumn("_ingested_at", F.current_timestamp())
        .withColumn("_source_file", F.input_file_name())
    )
    (df.write.mode("overwrite").format("delta").saveAsTable(table_name))
    print(f"{table_name}: {df.count()} rows")


for tbl, src in SOURCES.items():
    ingest(tbl, src)

print("Bronze ingest complete. Next: 02_silver_transform.py")
