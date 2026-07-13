# Fabric notebook - Gold business tables (Contoso Insurance workshop)
# Small, report-ready aggregates the Direct Lake semantic model and Copilot sit
# on. Keep Gold intentionally thin: business-friendly grains, friendly names.

from pyspark.sql import functions as F

premium = spark.table("fact_premium")
claim = spark.table("fact_claim")
dim_date = spark.table("dim_date")
dim_agent = spark.table("dim_agent")

# gold_premium_summary: product x region x channel x month, written + earned
gold_premium_summary = (
    premium.join(dim_date, "date_id")
    .groupBy("year", "month", "month_name", "period_begin", "product", "region", "channel")
    .agg(
        F.sum("written_premium").alias("written_premium"),
        F.sum("earned_premium").alias("earned_premium"),
        F.sum("policies_written").alias("policies_written"),
        F.sum("policies_inforce").alias("policies_inforce"),
    )
)
gold_premium_summary.write.mode("overwrite").format("delta").saveAsTable("gold_premium_summary")

# gold_loss_ratio: product x region x month, earned premium vs incurred losses
prem_m = (
    premium.join(dim_date, "date_id")
    .groupBy("year", "month", "period_begin", "product", "region")
    .agg(F.sum("earned_premium").alias("earned_premium"))
)
loss_m = (
    claim.join(dim_date, "date_id")
    .groupBy("year", "month", "product", "region")
    .agg(
        F.sum("incurred_loss").alias("incurred_loss"),
        F.sum("paid_loss").alias("paid_loss"),
        F.count("claim_id").alias("claim_count"),
    )
)
gold_loss_ratio = (
    prem_m.join(loss_m, ["year", "month", "product", "region"], "left")
    .fillna(0, ["incurred_loss", "paid_loss", "claim_count"])
    .withColumn("loss_ratio", F.when(F.col("earned_premium") > 0,
                F.col("incurred_loss") / F.col("earned_premium")).otherwise(F.lit(0.0)))
)
gold_loss_ratio.write.mode("overwrite").format("delta").saveAsTable("gold_loss_ratio")

# gold_agent_scorecard: written premium, loss ratio and policy count per agent
prem_a = premium.groupBy("agent_id").agg(
    F.sum("written_premium").alias("written_premium"),
    F.sum("earned_premium").alias("earned_premium"),
    F.sum("policies_written").alias("policies_written"),
)
loss_a = (
    claim.join(premium.select("policy_id", "agent_id").dropDuplicates(), "policy_id", "left")
    .groupBy("agent_id").agg(F.sum("incurred_loss").alias("incurred_loss"))
)
gold_agent_scorecard = (
    prem_a.join(loss_a, "agent_id", "left")
    .join(dim_agent, "agent_id", "left")
    .fillna(0, ["incurred_loss"])
    .withColumn("loss_ratio", F.when(F.col("earned_premium") > 0,
                F.col("incurred_loss") / F.col("earned_premium")).otherwise(F.lit(0.0)))
    .select("agent_id", "agent_name", "agency", "region", "channel",
            "written_premium", "policies_written", "incurred_loss", "loss_ratio")
)
gold_agent_scorecard.write.mode("overwrite").format("delta").saveAsTable("gold_agent_scorecard")

print("Gold complete: gold_premium_summary, gold_loss_ratio, gold_agent_scorecard")
print("Build the Direct Lake semantic model sm_insurance on these in Lab 6.")
