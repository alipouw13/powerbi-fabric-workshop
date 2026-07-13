# Fabric notebook - Silver transform (Contoso Insurance workshop)
# Turns Bronze into a conformed star schema: clean types, standard names, and
# the dimensions + facts the semantic model reads. This is the "model the data
# as a star" step a Tableau extract usually skips.

from pyspark.sql import functions as F

# ---- dimensions (typed + curated from the bronze source tables) ------------
dim_customer = (
    spark.table("bronze_dim_customer")
    .select(
        F.col("customer_id").cast("int"),
        F.col("customer_name").cast("string"),
        F.col("segment").cast("string"),
        F.col("region").cast("string"),
        F.col("tenure_years").cast("int"),
    )
)
dim_customer.write.mode("overwrite").format("delta").saveAsTable("dim_customer")

dim_agent = (
    spark.table("bronze_dim_agent")
    .select(
        F.col("agent_id").cast("int"),
        F.col("agent_name").cast("string"),
        F.col("agency").cast("string"),
        F.col("region").cast("string"),
        F.col("channel").cast("string"),
    )
)
dim_agent.write.mode("overwrite").format("delta").saveAsTable("dim_agent")

dim_coverage = (
    spark.table("bronze_dim_coverage")
    .select(
        F.col("coverage_id").cast("int"),
        F.col("product").cast("string"),
        F.col("coverage").cast("string"),
    )
)
dim_coverage.write.mode("overwrite").format("delta").saveAsTable("dim_coverage")

dim_policy = (
    spark.table("bronze_dim_policy")
    .select(
        F.col("policy_id").cast("int"),
        F.col("policy_number").cast("string"),
        F.col("product").cast("string"),
        F.col("customer_id").cast("int"),
        F.col("agent_id").cast("int"),
        F.col("region").cast("string"),
        F.col("channel").cast("string"),
        F.to_date("effective_date").alias("effective_date"),
        F.col("annual_premium").cast("double"),
        F.col("status").cast("string"),
    )
)
dim_policy.write.mode("overwrite").format("delta").saveAsTable("dim_policy")

dim_date = (
    spark.table("bronze_dim_date")
    .select(
        F.col("date_id").cast("int"),
        F.to_date("period_begin").alias("period_begin"),
        F.to_date("period_end").alias("period_end"),
        F.col("year").cast("int"),
        F.col("month").cast("int"),
        F.col("month_name").cast("string"),
        F.col("quarter").cast("string"),
    )
)
dim_date.write.mode("overwrite").format("delta").saveAsTable("dim_date")

# ---- facts -----------------------------------------------------------------
fact_premium = (
    spark.table("bronze_fact_premium")
    .select(
        F.col("policy_id").cast("int"),
        F.col("date_id").cast("int"),
        F.col("product").cast("string"),
        F.col("region").cast("string"),
        F.col("channel").cast("string"),
        F.col("agent_id").cast("int"),
        F.col("written_premium").cast("double"),
        F.col("earned_premium").cast("double"),
        F.col("policies_written").cast("int"),
        F.col("policies_inforce").cast("int"),
    )
)
fact_premium.write.mode("overwrite").format("delta").saveAsTable("fact_premium")

fact_claim = (
    spark.table("bronze_fact_claim")
    .select(
        F.col("claim_id").cast("int"),
        F.col("claim_number").cast("string"),
        F.col("policy_id").cast("int"),
        F.col("date_id").cast("int"),
        F.col("product").cast("string"),
        F.col("region").cast("string"),
        F.col("coverage_id").cast("int"),
        F.col("loss_type").cast("string"),
        F.col("severity").cast("string"),
        F.col("status").cast("string"),
        F.col("incurred_loss").cast("double"),
        F.col("paid_loss").cast("double"),
        F.col("fraud_flag").cast("int"),
    )
)
fact_claim.write.mode("overwrite").format("delta").saveAsTable("fact_claim")

print("Silver complete: dim_customer, dim_agent, dim_policy, dim_coverage, dim_date, fact_premium, fact_claim")
print("Next: 03_gold_business.py")
