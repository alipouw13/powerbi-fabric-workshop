# Lab 5 - Ingestion to OneLake

**Duration:** ~90 min - **Deck:** "OneLake ingestion"

You will land Contoso Insurance data into OneLake, create Bronze tables, and run the notebooks that build Silver and Gold. The operational claims_intake feed is included because it has the same shape a Rayfin claims app would write.

## Schwab context
A Tableau migration often starts with extracts. A Fabric migration turns those extracts and operational feeds into governed Lakehouse and Warehouse assets so analytics, apps, and AI can reuse the same data estate.

## What you'll build
- Raw files in lh_insurance Files/raw
- Bronze tables bronze_policy_claims and bronze_claims_intake
- Silver tables dim_customer, dim_agent, dim_policy, dim_coverage, dim_date, fact_premium, and fact_claim
- Gold tables gold_premium_summary, gold_loss_ratio, and gold_agent_scorecard
- A Warehouse named wh_insurance populated by src/sql/warehouse_gold.sql if your group chooses the Warehouse path

## Prerequisites
- Completed [Lab 4 - Governance foundations](../lab-04-governance-foundations/README.md)
- lh_insurance in Schwab-Analytics-Dev
- data/raw/contoso/ and data/raw/ops/ uploaded to Files/raw
- Notebooks available: ../../src/notebooks/01_bronze_ingest.py, ../../src/notebooks/02_silver_transform.py, and ../../src/notebooks/03_gold_business.py
- SQL available: ../../src/sql/warehouse_gold.sql
- Reference docs: [architecture](../../reference/architecture.md), [sources](../../reference/sources.md), and [Rayfin](../../reference/rayfin.md)

## Steps
### 1. Confirm raw file layout
- Open lh_insurance.
- Open Files/raw.
- Confirm Files/raw/contoso/policy_claims_extract.csv exists.
- Confirm Files/raw/contoso/dim_policy.csv exists.
- Confirm Files/raw/contoso/dim_customer.csv exists.
- Confirm Files/raw/contoso/dim_agent.csv exists.
- Confirm Files/raw/contoso/dim_coverage.csv exists.
- Confirm Files/raw/contoso/dim_date.csv exists.
- Confirm Files/raw/contoso/fact_premium.csv exists.
- Confirm Files/raw/contoso/fact_claim.csv exists.
- Confirm Files/raw/ops/claims_intake.csv exists.

### 2. Choose your ingestion pattern
- For workshop speed, you can run the provided notebook ingestion.
- For a production pattern, use a Data Factory pipeline or Dataflow Gen2 to land the same files.
- If sources are on-premises, plan an on-premises data gateway.
- If sources are private cloud resources, plan a VNet data gateway where appropriate.
- Keep folder names stable, because the notebooks expect contoso/ and ops/ under raw.
- Capture which pattern your team would use for real Tableau extract migration.

### 3. Run the Bronze ingest notebook
- Open src/notebooks/01_bronze_ingest.py in Fabric.
- Attach it to lh_insurance.
- Run the notebook.
- Confirm it reads policy_claims_extract.csv from Files/raw/contoso/.
- Confirm it reads claims_intake.csv from Files/raw/ops/.
- Confirm it writes bronze_policy_claims.
- Confirm it writes bronze_claims_intake.
- Review row counts for both tables.

### 4. Run the Silver transform notebook
- Open src/notebooks/02_silver_transform.py.
- Attach it to lh_insurance.
- Run the notebook after Bronze completes.
- Confirm the Silver dimension tables exist: dim_customer, dim_agent, dim_policy, dim_coverage, and dim_date.
- Confirm the Silver fact tables exist: fact_premium and fact_claim.
- Check that products include Auto, Home, Renters, Life, and Umbrella.
- Check that regions include Northeast, Southeast, Midwest, Southwest, and West.
- Check that channels include Independent Agent, Captive Agent, Direct, and Online.

### 5. Run the Gold business notebook
- Open src/notebooks/03_gold_business.py.
- Attach it to lh_insurance.
- Run the notebook after Silver completes.
- Confirm gold_premium_summary exists.
- Confirm gold_loss_ratio exists.
- Confirm gold_agent_scorecard exists.
- Validate that gold_loss_ratio includes earned premium, incurred losses, and a loss ratio calculation.
- Validate that gold_agent_scorecard can support agent performance review.

### 6. Optional: create wh_insurance
- Create a Warehouse named wh_insurance in Schwab-Analytics-Dev.
- Open src/sql/warehouse_gold.sql.
- Run the SQL in the Warehouse editor if your facilitator includes the Warehouse path.
- Confirm the Warehouse exposes the gold tables needed by downstream tools.
- Keep the Lakehouse as the primary path for Direct Lake in Lab 6.
- Use the Warehouse path to discuss SQL analyst access and governed sharing.

### 7. Connect the Rayfin claims story
- Open Files/raw/ops/claims_intake.csv.
- Review columns such as claim_number, policy_number, product, region, coverage, loss_type, loss_date, reported_date, reserve_amount, paid_amount, severity, and adjuster.
- This file is shaped like the Rayfin Claim entity in the Contoso Claims Intake app.
- In a real deployment, a Rayfin app can write operational data into the same Fabric estate that analytics uses.
- In this workshop, claims_intake.csv represents that app-generated operational feed.
- Keep this connection in mind for Lab 11.

## You'll know it worked when
- bronze_policy_claims and bronze_claims_intake exist in lh_insurance.
- Silver dimension and fact tables exist with expected product, region, and channel values.
- gold_premium_summary, gold_loss_ratio, and gold_agent_scorecard exist.
- claims_intake.csv is included in the Bronze layer.
- You can explain how app data and analytics data share one Fabric estate.

## Next
[Lab 6 - Semantic model and Direct Lake](../lab-06-semantic-model-directlake/README.md)
