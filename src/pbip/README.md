# PBIP + the shared semantic model (housing workshop)

The `Housing-Market-Insights` model is stored as a **PBIP** (Power BI Project):
plain-text **TMDL** and report JSON you can diff, review, and ship with Git and
CI/CD, exactly like application code. This is the "DevOps for BI" story a Tableau
team usually does not have (Tableau workbooks are opaque binaries).

## Save as PBIP
In Power BI Desktop: **File -> Options -> Preview features -> Power BI Project
(.pbip) save option**, then **File -> Save as -> .pbip**. You get:

```
Housing-Market-Insights.SemanticModel/   <- TMDL: tables, measures, relationships
Housing-Market-Insights.Report/          <- report pages as JSON
```

Commit the folder. Do not commit `.pbix`, caches, or local settings (see the
repo `.gitignore`).

## The model (star schema)
- Fact: `fact_home_sales` (grain: region x month x property type)
- Dimensions: `dim_region`, `dim_date`, `dim_property_type`
- Storage mode: **Direct Lake** on the Lakehouse gold tables (no import, no refresh)
- Relationships: single direction, `fact_home_sales` -> each dim; mark `dim_date`
  as the date table on `period_begin`.

## Core measures (defined ONCE, reused by every report)
Add these to `fact_home_sales`. A note on price: the fact stores a **median**
per region/period/type, so we average those medians across the filter context.
That is fine for a workshop headline; for exact medians, model at the sale grain.

```dax
Homes Sold             = SUM(fact_home_sales[homes_sold])
New Listings           = SUM(fact_home_sales[new_listings])
Inventory              = SUM(fact_home_sales[inventory])
Avg Median Sale Price  = AVERAGE(fact_home_sales[median_sale_price])
Median Days on Market  = AVERAGE(fact_home_sales[median_days_on_market])
Avg Sale to List %     = AVERAGE(fact_home_sales[avg_sale_to_list])
Sold Above List %      = AVERAGE(fact_home_sales[sold_above_list_share])
Months of Supply       = DIVIDE([Inventory], [Homes Sold])

Homes Sold PY =
CALCULATE([Homes Sold], DATEADD(dim_date[period_begin], -12, MONTH))

Homes Sold YoY % =
DIVIDE([Homes Sold] - [Homes Sold PY], [Homes Sold PY])
```

> Let **Copilot** draft these: in Power BI, use the DAX query view Copilot or the
> measure-description Copilot, then paste the verified measure here. See
> [Lab 7](../../labs/lab-07-copilot-reports/README.md).

## AI-ready metadata (so Copilot and the Data Agent answer well)
- Friendly table/column names; hide key columns (`region_id`, `date_id`, ...).
- Measure descriptions (Copilot can generate these).
- **Prep for AI** on the model: AI data schema, AI instructions, verified answers.
  This same metadata is what the **Power BI MCP server** returns from its "Get
  Semantic Model Schema" tool (see [Lab 9](../../labs/lab-09-mcp-github-copilot/README.md)).
