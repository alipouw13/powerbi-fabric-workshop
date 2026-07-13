# Lab 6 - Semantic Model + Direct Lake

**Duration:** ~90 min - **Deck:** "Build the shared semantic model"

You will build the shared Housing-Market-Insights semantic model in Direct Lake mode. You will model the star, add governed measures, mark the date table, prepare the model for AI, and set endorsement expectations.

## Schwab context
Power BI adoption at Schwab should not create one private model per report. A certified shared semantic model lets many teams build reports on the same definitions while keeping performance, security, and governance in one place.

Direct Lake is a Fabric storage mode that loads Delta tables from OneLake into memory on demand. It avoids scheduled import refresh while aiming for Import-mode speed and DirectQuery-like freshness on Fabric capacity.

## What you'll build
- A Direct Lake semantic model named Housing-Market-Insights.
- A star model with fact_home_sales, dim_region, dim_date, and dim_property_type.
- Gold serving tables gold_market_summary and gold_region_latest available for summary scenarios.
- The exact core measures listed in [src/pbip/README.md](../../src/pbip/README.md).
- AI-ready metadata, AI instructions, and verified answers.
- A Promoted or Certified endorsement plan.

## Prerequisites
- Completed [Lab 5 - Ingestion to OneLake](../lab-05-ingestion-onelake/README.md).
- lh_housing contains Bronze, Silver, and Gold Delta tables.
- Fabric capacity is enabled for Direct Lake.
- Measure definitions are available in [src/pbip/README.md](../../src/pbip/README.md).
- Direct Lake reference: [reference/direct-lake.md](../../reference/direct-lake.md).

## Steps
### 1. Confirm the Lakehouse tables
Open lh_housing in Schwab-Analytics-Dev.

Confirm that fact_home_sales, dim_region, dim_date, dim_property_type, gold_market_summary, and gold_region_latest exist as Delta tables. Direct Lake requires Delta tables in a Lakehouse or Warehouse on Fabric capacity.

### 2. Create the semantic model
Create a new semantic model from lh_housing and name it Housing-Market-Insights.

Choose Direct Lake storage mode when prompted. Include the star tables and the Gold summary tables so authors can use both detailed and curated reporting patterns.

### 3. Model the star
Open the model designer and create relationships.

Connect fact_home_sales to dim_region, dim_date, and dim_property_type. Use many-to-one relationships, active relationships, and single direction filtering from dimensions to fact_home_sales.

### 4. Mark the date table
Mark dim_date as the date table and choose dim_date[period_begin] as the date column.

This supports time intelligence and helps Copilot understand calendar behavior.

### 5. Add the core measures
Create the measures exactly as named below, using the definitions in [src/pbip/README.md](../../src/pbip/README.md):

- Homes Sold
- New Listings
- Inventory
- Avg Median Sale Price
- Median Days on Market
- Avg Sale to List %
- Sold Above List %
- Months of Supply
- Homes Sold PY
- Homes Sold YoY %

Keep the names exact because later labs, Copilot prompts, and sample DAX expect them.

### 6. Format and organize the model
Apply currency, whole number, decimal, and percentage formats.

Hide technical keys, create display folders if available, and write clear descriptions for tables, columns, and measures. For example, describe Homes Sold as the count of homes sold in the selected filter context.

### 7. Prepare the model for AI
Add AI data schema metadata where available.

Add AI instructions that explain the grain: 24 months, 12 metros, 4 property types, and housing market metrics. Add synonyms such as metro for region, supply for inventory, and competitiveness for sale-to-list and sold-above-list metrics.

### 8. Add verified answers
Create a few verified answer examples for common questions.

Use questions such as "Which metros have the highest Homes Sold?", "What is Homes Sold YoY % by region?", and "Which property types have the highest Months of Supply?" Validate each answer against visuals or DAX.

### 9. Validate with sample DAX
Open [src/sql/sample_dax_queries.dax](../../src/sql/sample_dax_queries.dax).

Run at least one query against Housing-Market-Insights using DAX Query View or another approved tool. Confirm the results match your report visuals.

### 10. Plan endorsement
Use [governance/endorsement-certification.md](../../governance/endorsement-certification.md) to decide whether the model is Promoted or ready for Certified review.

For the lab, Promoted is enough. For production, Certified should require ownership, documentation, access review, validation evidence, and support process.

## You'll know it worked when
- Housing-Market-Insights exists in Direct Lake mode.
- fact_home_sales filters through dim_region, dim_date, and dim_property_type.
- All 10 core measures exist with exact names.
- dim_date is marked as the date table.
- Model descriptions, AI instructions, and verified answers are in place.
- The model has a clear Promoted or Certified path.

## Next
Previous: [Lab 5 - Ingestion to OneLake](../lab-05-ingestion-onelake/README.md). Continue to [Lab 7 - Copilot in Reports](../lab-07-copilot-reports/README.md).
