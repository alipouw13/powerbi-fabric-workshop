# Lab 8 - Migrate a Workbook

**Duration:** ~90 min - **Deck:** "Migrate a real workbook, end to end"

You will migrate a described Tableau Housing Market workbook to Power BI. The workbook has three sheets built on a .hyper extract: price trends, market competitiveness, and inventory.

## Schwab context
A successful migration is not a screenshot copy. Schwab teams need to decide which Tableau assets should be retired, rebuilt quickly, or redesigned around a shared semantic model.

This lab gives you a coached breakout. You will map workbook content to Housing-Market-Insights, rebuild visuals, validate numbers, and add a second use case from MLS listings.

## What you'll build
- A migration inventory for the Tableau Housing Market workbook.
- A field mapping from the .hyper extract to Housing-Market-Insights.
- Three rebuilt Power BI visuals: price trends, market competitiveness, and inventory.
- A listing and agent performance page using mls/listings.csv.
- A validation checklist that proves the Power BI report matches the intended Tableau logic.
- Notes for the migration assessment worksheet.

## Prerequisites
- Completed [Lab 7 - Copilot in Reports](../lab-07-copilot-reports/README.md).
- Housing-Market-Insights semantic model available.
- Access to [reference/migration-approaches.md](../../reference/migration-approaches.md).
- Access to [governance/migration-assessment-worksheet.md](../../governance/migration-assessment-worksheet.md).
- The raw file [mls/listings.csv](../../data/raw/mls/listings.csv) for the second use case.

## Steps
### 1. Inventory the described workbook
Create a quick inventory with three Tableau sheets: Price Trends, Market Competitiveness, and Inventory.

For each sheet, list the fields, filters, calculations, sort order, and user interactions. Include source type: .hyper extract based on the wide market_tracker shape.

### 2. Map the extract to the semantic model
Map Tableau extract fields to Housing-Market-Insights tables and measures.

Examples: region maps to dim_region[region], property_type maps to dim_property_type[property_type], period_begin maps to dim_date[period_begin], homes_sold maps to Homes Sold, and median_sale_price maps to Avg Median Sale Price.

### 3. Rebuild Price Trends
Create a Power BI page named Migrated Price Trends.

Add a line chart with dim_date[period_begin] on the x-axis and Avg Median Sale Price as the value. Add slicers for dim_region[region] and dim_property_type[property_type].

### 4. Rebuild Market Competitiveness
Add a page section or separate page named Market Competitiveness.

Use Avg Sale to List %, Sold Above List %, and Median Days on Market. Choose visuals that explain competitiveness clearly, such as a combo chart, scatter chart, or KPI cards by metro.

### 5. Rebuild Inventory
Add an Inventory view.

Use Inventory and Months of Supply by region, month, and property type. Use a bar chart for latest inventory and a line chart for Months of Supply over time.

### 6. Add the MLS second use case
Use [mls/listings.csv](../../data/raw/mls/listings.csv) to create a listing and agent performance page.

If your model already includes bronze_listings or a curated listings table, use that source. Otherwise, import mls/listings.csv for the lab and build visuals for list_agent, office, status, list_price, sale_price, beds, baths, and sqft.

### 7. Validate filters and interactions
Apply the same region, date, and property type filters used in the Tableau workbook.

Confirm that the migrated visuals respond consistently. Check that slicers filter the intended visuals and do not create confusing cross-highlighting.

### 8. Validate numbers
Create a validation table with Tableau value, Power BI value, filter context, and status.

Validate at least five metrics: Homes Sold, Avg Median Sale Price, Inventory, Months of Supply, and Sold Above List %. Differences should be explained by aggregation, date range, or source mapping.

### 9. Complete the assessment worksheet
Open [governance/migration-assessment-worksheet.md](../../governance/migration-assessment-worksheet.md).

Record whether the workbook should be redesigned, rebuilt as-is, merged into an existing report, or retired. Include owner, audience, data source, refresh pattern, and governance notes.

### 10. Prepare a migration readout
Summarize what changed from Tableau to Power BI.

Include the model decision, visuals rebuilt, validation result, MLS second use case, and any gaps that require follow-up after the workshop.

## You'll know it worked when
- The three Tableau workbook sheets have clear Power BI replacements.
- Each replacement uses Housing-Market-Insights where possible.
- The MLS page uses mls/listings.csv or a table derived from it.
- At least five metrics have been validated against the expected Tableau logic.
- The migration assessment worksheet has notes for next steps.

## Next
Previous: [Lab 7 - Copilot in Reports](../lab-07-copilot-reports/README.md). Continue to [Lab 9 - MCP + GitHub Copilot](../lab-09-mcp-github-copilot/README.md).
