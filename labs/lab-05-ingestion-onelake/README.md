# Lab 5 - Getting data in: SQL, gateway, and OneLake

**Duration:** ~90 min - **Deck:** "OneLake ingestion"

You will start from the connectivity pattern used today, a SQL source reaching Power BI through the on-premises data gateway with an import semantic model, and then land Contoso Insurance data into OneLake, create Bronze tables, and run the notebooks that build Silver and Gold. The operational claims_intake feed is included because it has the same shape a Rayfin claims app would write.

## Schwab context
Today most Power BI reports connect directly to SQL databases with an import mode semantic model, refreshed through the on-premises data gateway, and a lot of data still arrives as large Excel files. OneLake and Lakehouse options are not fully approved yet. So step 1 is the pattern you can use on Monday, and the medallion steps show the target state and the preferred layering to adopt as approvals land. Introducing the pattern now is what avoids reworking a flat estate later.

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
### 1. Connect the way you connect today
- In Power BI Desktop, use Get data, SQL Server, and point at a source you already use, or use the Contoso CSVs if no SQL source is available in the room.
- Choose Import, which is the standard pattern today, and note what DirectQuery would change.
- In the Power BI Service, review the on-premises data gateway that the published semantic model would use, including who owns it and which connections it carries.
- List the refresh schedule, credentials, and failure notification owner for one existing report.
- Discuss where large Excel files are used as a source, and what breaks as they grow: refresh time, file locks, single-owner risk, and no lineage.
- Write down which of your current sources could move behind a shared gateway connection instead of one per report.
- Everything after this step is the target-state pattern: land the raw files once, then layer them as Bronze, Silver, and Gold, which step 3 explains. Treat it as a walkthrough of where this is going.

### 2. Confirm raw file layout
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

### 3. Choose your ingestion pattern
- Bronze holds the raw landing, Silver holds the conformed star, and Gold holds the business-ready tables reporting consumes. That layering is the medallion pattern, and it is the answer to logic being repeated in every report or Excel file.
- For workshop speed, you can run the provided notebook ingestion.
- For a production pattern, use a Data Factory pipeline or Dataflow Gen2 to land the same files.
- If sources are on-premises, plan an on-premises data gateway.
- If sources are private cloud resources, plan a VNet data gateway where appropriate.
- Keep folder names stable, because the notebooks expect contoso/ and ops/ under raw.
- Capture which pattern your team would use for real Tableau extract migration.
- Note that until OneLake and Lakehouse are approved, the same layering can be applied in SQL: a raw schema, a conformed schema, and a reporting schema feeding the import model.

### 4. Run the Bronze ingest notebook
- Open src/notebooks/01_bronze_ingest.py in Fabric.
- Attach it to lh_insurance.
- Run the notebook.
- Confirm it reads policy_claims_extract.csv from Files/raw/contoso/.
- Confirm it reads claims_intake.csv from Files/raw/ops/.
- Confirm it writes bronze_policy_claims.
- Confirm it writes bronze_claims_intake.
- Review row counts for both tables.

### 5. Run the Silver transform notebook
- Open src/notebooks/02_silver_transform.py.
- Attach it to lh_insurance.
- Run the notebook after Bronze completes.
- Confirm the Silver dimension tables exist: dim_customer, dim_agent, dim_policy, dim_coverage, and dim_date.
- Confirm the Silver fact tables exist: fact_premium and fact_claim.
- Check that products include Auto, Home, Renters, Life, and Umbrella.
- Check that regions include Northeast, Southeast, Midwest, Southwest, and West.
- Check that channels include Independent Agent, Captive Agent, Direct, and Online.

### 6. Run the Gold business notebook
- Open src/notebooks/03_gold_business.py.
- Attach it to lh_insurance.
- Run the notebook after Silver completes.
- Confirm gold_premium_summary exists.
- Confirm gold_loss_ratio exists.
- Confirm gold_agent_scorecard exists.
- Validate that gold_loss_ratio includes earned premium, incurred losses, and a loss ratio calculation.
- Validate that gold_agent_scorecard can support agent performance review.

### 7. Optional: create wh_insurance
- Create a Warehouse named wh_insurance in Schwab-Analytics-Dev.
- Open src/sql/warehouse_gold.sql.
- Run the SQL in the Warehouse editor if your facilitator includes the Warehouse path.
- Confirm the Warehouse exposes the gold tables needed by downstream tools.
- Keep the Lakehouse as the primary path for Direct Lake in Lab 6.
- Use the Warehouse path to discuss SQL analyst access and governed sharing.

### 8. Connect the Rayfin claims story
- Open Files/raw/ops/claims_intake.csv.
- Review columns such as claim_number, policy_number, product, region, coverage, loss_type, loss_date, reported_date, reserve_amount, paid_amount, severity, and adjuster.
- This file is shaped like the Rayfin Claim entity in the Contoso Claims Intake app.
- In a real deployment, a Rayfin app can write operational data into the same Fabric estate that analytics uses.
- In this workshop, claims_intake.csv represents that app-generated operational feed.
- Keep this connection in mind for Lab 11.

## You'll know it worked when
- You can describe the current path from a SQL source through the on-premises data gateway to an import semantic model, and who owns each part.
- bronze_policy_claims and bronze_claims_intake exist in lh_insurance.
- Silver dimension and fact tables exist with expected product, region, and channel values.
- gold_premium_summary, gold_loss_ratio, and gold_agent_scorecard exist.
- claims_intake.csv is included in the Bronze layer.
- You can explain how app data and analytics data share one Fabric estate.
- You can explain Bronze, Silver, and Gold, and how the same layering can start in SQL before OneLake is approved.

## Next
[Lab 6 - Semantic model and Direct Lake](../lab-06-semantic-model-directlake/README.md)
