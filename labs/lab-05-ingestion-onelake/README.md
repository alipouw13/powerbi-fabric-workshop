# Lab 5 - Ingestion to OneLake

**Duration:** ~90 min - **Deck:** "Get the data into OneLake"

You will replace the manual upload from Lab 0 with a repeatable ingestion pattern. You will land Redfin and MLS files in OneLake, run the Bronze, Silver, and Gold notebooks, and discuss incremental loading and schema drift.

## Schwab context
Manual uploads are fine for a kickoff lab, but Schwab analytics teams need repeatable pipelines with ownership, lineage, and operations. Fabric gives you Data Factory pipelines, Dataflow Gen2, notebooks, Lakehouses, and Warehouse options in the same workspace.

You will use lh_housing as the lakehouse for the workshop. The pattern is source files to Files/raw, Bronze tables, Silver star tables, Gold business tables, then a shared semantic model.

## What you'll build
- A repeatable ingestion path for redfin/ and mls/ data into Files/raw.
- Bronze tables named bronze_market_tracker and bronze_listings.
- Silver tables named dim_region, dim_date, dim_property_type, and fact_home_sales.
- Gold tables named gold_market_summary and gold_region_latest.
- A notes section on gateway selection, incremental load, and schema drift.
- Optional Warehouse SQL output using [src/sql/warehouse_gold.sql](../../src/sql/warehouse_gold.sql).

## Prerequisites
- Completed [Lab 4 - Governance Foundations](../lab-04-governance-foundations/README.md).
- Schwab-Analytics-Dev workspace with lh_housing.
- Raw files from data/raw/ available locally and in OneLake.
- Notebook files: [01_bronze_ingest.py](../../src/notebooks/01_bronze_ingest.py), [02_silver_transform.py](../../src/notebooks/02_silver_transform.py), and [03_gold_business.py](../../src/notebooks/03_gold_business.py).
- Source reference: [reference/sources.md](../../reference/sources.md).

## Steps
### 1. Review the current raw landing zone
Open lh_housing and inspect Files/raw.

Confirm that Files/raw/redfin/ contains market_tracker.csv, fact_home_sales.csv, dim_region.csv, dim_date.csv, and dim_property_type.csv. Confirm that Files/raw/mls/ contains listings.csv.

### 2. Create a repeatable ingestion option
Create either a Data Factory pipeline or a Dataflow Gen2 named ingest_housing_raw.

Use the option your facilitator recommends. The goal is to copy or refresh the raw Redfin and MLS files into the same Files/raw layout used by the notebooks.

### 3. Apply the gateway rule
Discuss which gateway would be used for real Schwab sources.

Use an on-premises data gateway for on-prem sources. Use a VNet data gateway for supported cloud sources that need private network access. Do not embed credentials in notebooks or files.

### 4. Run the Bronze notebook
Create or upload a Fabric notebook using [src/notebooks/01_bronze_ingest.py](../../src/notebooks/01_bronze_ingest.py).

Attach it to lh_housing and run it. Confirm it creates bronze_market_tracker from redfin/market_tracker.csv and bronze_listings from mls/listings.csv.

### 5. Inspect Bronze outputs
Open the Tables area of lh_housing.

Preview bronze_market_tracker and bronze_listings. Check row counts, columns, and data types. The Bronze layer should preserve source shape with light standardization.

### 6. Run the Silver transform notebook
Create or upload the notebook from [src/notebooks/02_silver_transform.py](../../src/notebooks/02_silver_transform.py).

Run it against lh_housing. Confirm it creates dim_region, dim_date, dim_property_type, and fact_home_sales.

### 7. Validate the Silver star
Preview fact_home_sales and each dimension.

Confirm that keys are populated and that the 12 metros and 4 property types appear as expected: Seattle, WA, Denver, CO, Austin, TX, Phoenix, AZ, Chicago, IL, Atlanta, GA, Boston, MA, Nashville, TN, Charlotte, NC, Miami, FL, Portland, OR, and Dallas, TX.

### 8. Run the Gold business notebook
Create or upload the notebook from [src/notebooks/03_gold_business.py](../../src/notebooks/03_gold_business.py).

Run it and confirm gold_market_summary and gold_region_latest are created. These tables simplify common reporting and executive summary scenarios.

### 9. Review the SQL alternative
Open [src/sql/warehouse_gold.sql](../../src/sql/warehouse_gold.sql).

Discuss when a Warehouse SQL approach may be preferred, such as SQL-first teams, existing stored procedure patterns, or stronger separation between lake engineering and warehouse serving layers.

### 10. Discuss incremental load and schema drift
Identify the natural incremental column for this dataset, such as period_begin or list_date.

Discuss how schema drift should be handled: alert on unexpected columns, document accepted changes, and avoid silently breaking downstream semantic models.

## You'll know it worked when
- Files/raw/redfin/ and Files/raw/mls/ can be refreshed by a repeatable ingestion option.
- bronze_market_tracker and bronze_listings exist in lh_housing.
- dim_region, dim_date, dim_property_type, and fact_home_sales exist and join cleanly.
- gold_market_summary and gold_region_latest exist.
- You can explain which gateway pattern applies to on-prem and cloud sources.

## Next
Previous: [Lab 4 - Governance Foundations](../lab-04-governance-foundations/README.md). Continue to [Lab 6 - Semantic Model + Direct Lake](../lab-06-semantic-model-directlake/README.md).
