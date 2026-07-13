# Tableau to Power BI concept translation

This guide gives Tableau authors a practical translation layer for the 3-day Schwab Power BI and Fabric workshop.
Use it when you hear a familiar Tableau term and need the closest Power BI or Fabric concept.

Related workshop assets:

- Direct Lake model lab: [lab 06](../labs/lab-06-semantic-model-directlake/README.md)
- PBIP project reference: [src/pbip](../src/pbip/README.md)
- Governance worksheet: [migration assessment worksheet](../governance/migration-assessment-worksheet.md)

## Quick translation table

| Tableau concept | Power BI or Fabric concept | What changes for Schwab teams |
| --- | --- | --- |
| Worksheet | Report visual | Build visuals on a report canvas. Visuals query the semantic model. |
| Dashboard | Report page | Warning: a Power BI "dashboard" is a different Service pin-board feature, not the main authoring canvas. |
| Story | Bookmarks / report | Use bookmarks, buttons, drillthrough, and report page navigation for guided narratives. |
| Published data source | Shared semantic model | Create one governed semantic model, then connect many thin reports to it. |
| Extract (.hyper) | Import mode or Direct Lake | Import stores compressed data in the model. Direct Lake loads Delta tables from OneLake on demand. |
| Live connection | DirectQuery or Direct Lake | DirectQuery sends queries to the source. Direct Lake reads OneLake Delta tables into memory without scheduled import refresh. |
| Calculated field | Measure or calculated column | Use measures for aggregations and reusable business logic. Use calculated columns for row-level attributes. |
| LOD expression (FIXED/INCLUDE/EXCLUDE) | DAX with CALCULATE + filter context | Recreate the grain explicitly with measures, relationships, and filter modifiers. |
| Table calculation | DAX (for example, time intelligence) | Move percent change, prior period, rank, and running totals into model measures. |
| Parameter | Field parameter / what-if parameter | Field parameters swap dimensions or measures. What-if parameters support scenario input. |
| Set / Group | Group / calculation group | Groups can be created in Power BI. Calculation groups centralize reusable measure logic. |
| Tableau Prep | Dataflow Gen2 or Fabric notebook | Dataflow Gen2 handles low-code shaping. Notebooks handle repeatable Spark transformations. |
| Tableau Server / Cloud | Power BI Service / Microsoft Fabric | Workspaces hold reports, semantic models, lakehouses, warehouses, notebooks, and pipelines. |
| Row-level security | Power BI RLS | Define security roles in the semantic model, then test and deploy with workspace controls. |
| VizQL | The Power BI query engine (VertiPaq/DAX) | DAX queries run against a semantic model. Import and Direct Lake can use in-memory storage. |

## Key mindset shifts

1. Start with the model, not the report page.
2. In Tableau, workbook authors often repeat logic in each workbook.
3. In Power BI, create measures once in `Housing-Market-Insights` and reuse them everywhere.
4. Treat the semantic model as the governed product.
5. The workshop model uses gold tables from `lh_housing` as the presentation layer.
6. The target model grain is clear: date, region, property type, and home sales metrics.
7. Use a star schema where facts hold measures and dimensions hold filter attributes.
8. Microsoft guidance: [Understand star schema and the importance for Power BI](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema).
9. Put reusable metrics in measures: `Homes Sold`, `Inventory`, `Avg Median Sale Price`, and `Homes Sold YoY %`.
10. Avoid copying DAX into every report.
11. Build thin reports on the shared semantic model.
12. Certify the shared model after data quality, ownership, and performance checks.
13. Use Dev/Test/Prod workspaces for lifecycle control.
14. In this workshop those workspaces are `Schwab-Analytics-Dev`, `Schwab-Analytics-Test`, and `Schwab-Analytics-Prod`.
15. Use deployment pipelines when content is ready to move across environments.
16. Keep one governed copy of logic instead of one copy per workbook.
17. If a Tableau workbook has a local extract and many workbook-only calculations, it is a consolidation candidate.

## Where Power BI is genuinely different

| Difference | What to watch |
| --- | --- |
| Dashboard terminology | A Power BI dashboard is a Service artifact made from pinned tiles. Most workshop work happens in reports. |
| Model-based analytics | The semantic model can be reused by reports, Excel, Copilot, and MCP tools. |
| Measures as contracts | A measure is a governed calculation. Changing it affects every connected report. |
| Storage choices | Import, DirectQuery, and Direct Lake are model storage patterns, not workbook publishing options. |
| Fabric workspace scope | A workspace can contain lakehouse, notebook, semantic model, report, dataflow, and pipeline items. |
| Certification | Certified content is discoverable and trusted across the tenant. |

## Workshop example

The Tableau-like extract is `data/raw/redfin/market_tracker.csv`.
It is intentionally wide so Tableau authors can recognize the shape.

The modeled Power BI path is the star schema:

1. `dim_region`
2. `dim_date`
3. `dim_property_type`
4. `fact_home_sales`
5. Gold summaries: `gold_market_summary` and `gold_region_latest`

In the Direct Lake lab, those gold tables support the `Housing-Market-Insights` semantic model.

## Practical translation rule

If the Tableau item answers a business question, migrate the question first.
If the Tableau item encodes shared business logic, migrate the logic into the semantic model.
If the Tableau item is a one-off visual layout, rebuild it as a report page only after the model is stable.

## Microsoft Learn anchors

- [Power BI migration overview](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-migration-overview)
- [Understand star schema and the importance for Power BI](https://learn.microsoft.com/en-us/power-bi/guidance/star-schema)
- [Direct Lake overview](https://learn.microsoft.com/en-us/fabric/fundamentals/direct-lake-overview)
- [Row-level security with Power BI](https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security)
