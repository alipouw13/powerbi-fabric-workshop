# Direct Lake in Fabric and Power BI

Direct Lake is a Power BI semantic model storage mode for Microsoft Fabric.
It loads OneLake Delta tables into memory on demand.
It avoids scheduled import refresh while preserving interactive, in-memory query performance.

Workshop lab:

- [Lab 06: Direct Lake semantic model](../labs/lab-06-semantic-model-directlake/README.md)

Microsoft overview: [Direct Lake overview](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview).

## What Direct Lake means

| Concept | Practical meaning |
| --- | --- |
| OneLake Delta tables | The semantic model reads Delta tables from Fabric Lakehouse or Warehouse storage. |
| On-demand loading | Data is loaded into memory when needed by queries. |
| No import refresh | The model does not require a scheduled import refresh to copy data into Power BI. |
| Import-like speed | Queries can use in-memory VertiPaq performance after data is loaded. |
| DirectQuery-like freshness | Data can reflect current Delta table state without a traditional import refresh cycle. |

For Tableau authors, Direct Lake feels closest to a live connection with cached, optimized analytical performance.
It is not the same as Tableau live.
The storage layer is OneLake Delta tables, and the semantic layer still controls relationships, measures, RLS, and metadata.

## Requirements

Use Direct Lake when these are true:

1. Data is stored as Delta tables in Fabric.
2. Tables are in a Lakehouse or Warehouse.
3. The workspace is backed by Fabric capacity.
4. The semantic model is built on tables that are intended for analytics.
5. Model authors can define relationships, measures, and security in Power BI.

In the workshop, the Direct Lake path is:

1. `lh_housing`
2. Files in `Files/raw`
3. Bronze tables: `bronze_market_tracker`, `bronze_listings`
4. Silver tables: `dim_region`, `dim_date`, `dim_property_type`, `fact_home_sales`
5. Gold tables: `gold_market_summary`, `gold_region_latest`
6. Semantic model: `Housing-Market-Insights (Direct Lake)` on gold

## Import vs DirectQuery vs Direct Lake

| Storage mode | How data is queried | Strengths | Tradeoffs | Workshop fit |
| --- | --- | --- | --- | --- |
| Import | Data is copied into the semantic model during refresh | Fast, mature, predictable | Needs refresh, duplicates data | Good for small curated extracts or snapshots |
| DirectQuery | Queries are sent to the source at interaction time | Fresh source data, no import copy | Depends on source performance and query folding | Useful for sources that must stay live |
| Direct Lake | Delta tables are loaded from OneLake into memory on demand | No import refresh, fast interactive analysis, Fabric-native | Requires Fabric and Delta tables | Preferred path for `Housing-Market-Insights` |

## DirectQuery fallback

Direct Lake can fall back to DirectQuery in some cases.
Fallback means a query is sent through a SQL endpoint rather than served fully from Direct Lake in-memory structures.
This can affect performance and should be monitored during model testing.

Common reasons to watch for fallback:

- Unsupported model or table features.
- Security or permission paths that require a different query route.
- Model design that does not align with Direct Lake constraints.
- Large or complex queries that need careful validation.

Use performance testing before certifying a Direct Lake model.

## When to use Direct Lake

| Use Direct Lake when | Consider another mode when |
| --- | --- |
| Data is already curated in Fabric Lakehouse or Warehouse. | The source is outside Fabric and cannot be landed in OneLake. |
| Users need current analytics without waiting for import refresh. | A small static dataset is easier to manage as Import. |
| The team wants one governed OneLake copy. | The source system must handle row-by-row operational lookups. |
| Multiple reports reuse the same semantic model. | A one-off prototype does not justify Fabric setup. |
| Model authors can invest in star schema design. | The data is not modeled and needs heavy preparation first. |

## Tableau mental model

If a Tableau workbook uses a live connection for freshness, map the requirement before choosing Power BI storage.

Ask:

1. Does the business need fresh data or just frequent refresh?
2. Can data be landed in OneLake as Delta tables?
3. Is the analytical grain stable enough for a shared semantic model?
4. Can one certified model replace several workbook extracts?
5. Are performance and RLS validated against realistic user roles?

For the workshop, the answer is yes.
The synthetic housing data is curated into Gold tables, then modeled once for reuse.

## Microsoft Learn anchors

- [Direct Lake overview](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview)
- [DirectQuery in Power BI](https://learn.microsoft.com/en-us/power-bi/connect-data/desktop-directquery-about)
- [Understand star schema and the importance for Power BI](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema)
