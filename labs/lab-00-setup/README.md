# Lab 0 - Setup

**Duration:** ~30 min - **Deck:** "Kickoff + goals"

You will set up the workshop environment, generate the synthetic housing dataset, and place the raw files in OneLake. By the end, you have the workspaces, Lakehouse, data, and local tools needed for the remaining labs.

## Schwab context
Schwab Tableau teams often start with a flat extract and a workbook. In this workshop, you will keep that familiar starting point while building the Power BI and Fabric foundation that supports governed, shared analytics.

You will use synthetic housing data so everyone can practice safely without customer or account data. The pattern maps to real Schwab analytics work: source data lands in OneLake, is shaped into governed tables, and is reused through a shared semantic model.

## What you'll build
- Three Fabric workspaces named Schwab-Analytics-Dev, Schwab-Analytics-Test, and Schwab-Analytics-Prod.
- A generated dataset under data/raw/ with Redfin and MLS CSV files.
- A Lakehouse named lh_housing in Schwab-Analytics-Dev.
- A Files/raw landing zone that preserves the redfin/ and mls/ subfolders.
- A local authoring setup with VS Code and the GitHub Copilot extension for Day 3.
- A mental map of the workshop architecture using [reference/architecture.md](../../reference/architecture.md#how-each-lab-maps-onto-this-picture).

## Prerequisites
- Access to a Fabric tenant with a confirmed Fabric capacity.
- Permission to create workspaces or a facilitator-created workspace assignment.
- Power BI Desktop installed and signed in.
- Python available on your path for `python data/generate_data.py`.
- VS Code installed with the GitHub Copilot extension available.
- This repository cloned locally at the workshop root.

## Steps
### 1. Confirm your Fabric capacity
Open the Fabric portal and confirm that a Fabric capacity is available for the workshop.

If your tenant shows multiple capacities, use the one assigned by the facilitator. Record the capacity name because you will use it again when creating or assigning workspaces.

### 2. Create the Dev, Test, and Prod workspaces
Create three workspaces named Schwab-Analytics-Dev, Schwab-Analytics-Test, and Schwab-Analytics-Prod.

Assign each workspace to the confirmed Fabric capacity. Keep yourself as Admin for the lab, then use Viewer or Contributor for other attendees unless the facilitator gives different guidance.

### 3. Generate the synthetic dataset
From the workshop root, run:

```powershell
python data/generate_data.py
```

Confirm that data/raw/ now contains redfin/market_tracker.csv, redfin/fact_home_sales.csv, redfin/dim_region.csv, redfin/dim_date.csv, redfin/dim_property_type.csv, and mls/listings.csv.

### 4. Inspect the Tableau-style extract
Open [data/raw/redfin/market_tracker.csv](../../data/raw/redfin/market_tracker.csv) in a text editor or Excel.

Notice that it is a wide shape with columns such as region, state, period_begin, property_type, median_sale_price, homes_sold, inventory, and months_of_supply. This is the shape many Tableau extracts use, and you will redesign it later.

### 5. Create the Lakehouse
In Schwab-Analytics-Dev, create a Lakehouse named lh_housing.

Open the Lakehouse and locate the Files area. This is where raw CSV files land before they become Bronze, Silver, and Gold tables.

### 6. Upload the raw files to OneLake
Create a Files/raw folder in lh_housing.

Upload data/raw/redfin/** into Files/raw/redfin/ and data/raw/mls/** into Files/raw/mls/. Keep the subfolders exactly named redfin and mls so the notebooks can find the files.

### 7. Install and verify local tools
Open VS Code and confirm that the GitHub Copilot extension is installed and signed in.

You will not use GitHub Copilot until Day 3, but verifying it now avoids delays during Lab 9. Also confirm Power BI Desktop opens and can sign in to the same tenant.

### 8. Skim the architecture reference
Read the "How each lab maps onto this picture" section of [reference/architecture.md](../../reference/architecture.md#how-each-lab-maps-onto-this-picture).

Trace the path from data/raw/ to OneLake Files/raw, then to Bronze tables, Silver star tables, Gold summary tables, the Housing-Market-Insights semantic model, and reports.

### 9. Record your setup status
Create a short note for yourself with the capacity name, workspace names, and the lh_housing Lakehouse URL.

Do not store credentials in the note. You only need enough information to return to the right Fabric items during the workshop.

## You'll know it worked when
- Schwab-Analytics-Dev, Schwab-Analytics-Test, and Schwab-Analytics-Prod exist on the Fabric capacity.
- `python data/generate_data.py` completed without errors.
- lh_housing contains Files/raw/redfin/ and Files/raw/mls/.
- The files include redfin/market_tracker.csv and mls/listings.csv.
- VS Code, GitHub Copilot, and Power BI Desktop are installed and signed in.

## Next
This is the first lab. Continue to [Lab 1 - Tableau to Power BI](../lab-01-tableau-to-powerbi/README.md).
