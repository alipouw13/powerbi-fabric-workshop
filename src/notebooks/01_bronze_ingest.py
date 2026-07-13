# Fabric notebook - Bronze ingest (Contoso Insurance workshop)
# Reads the raw CSVs uploaded to the Lakehouse Files area and lands them as
# Bronze Delta tables, unchanged, with lineage columns. Run in a Fabric
# notebook attached to the Lakehouse `lh_insurance`.
#
# Bronze rule: land raw, do not clean. Cleaning happens in Silver (notebook 02).

from pyspark.sql import functions as F

RAW = "Files/raw"  # where Lab 0 / Lab 5 lands the CSVs

# Headline operational feeds plus the normalized source tables.
SOURCES = {
    # denormalized policy admin extract (the "Tableau .hyper" shape)
    "bronze_policy_claims": f"{RAW}/contoso/policy_claims_extract.csv",
    # claims system feed (same shape the Rayfin claims-intake app writes)
    "bronze_claims_intake": f"{RAW}/ops/claims_intake.csv",
    # normalized source tables from the policy + claims systems
    "bronze_dim_customer": f"{RAW}/contoso/dim_customer.csv",
    "bronze_dim_agent": f"{RAW}/contoso/dim_agent.csv",
    "bronze_dim_policy": f"{RAW}/contoso/dim_policy.csv",
    "bronze_dim_coverage": f"{RAW}/contoso/dim_coverage.csv",
    "bronze_dim_date": f"{RAW}/contoso/dim_date.csv",
    "bronze_fact_premium": f"{RAW}/contoso/fact_premium.csv",
    "bronze_fact_claim": f"{RAW}/contoso/fact_claim.csv",
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
