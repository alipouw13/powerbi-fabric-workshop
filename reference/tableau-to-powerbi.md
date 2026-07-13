# Tableau to Power BI translation guide

Use this guide when a Tableau term comes up in the workshop and the team needs
the closest Power BI or Fabric concept. The goal is not a one-to-one copy. The
goal is a governed semantic model, reusable measures, and fewer duplicated
extracts.

## Workshop context

- Theme: Contoso Insurance, a P&C carrier with Auto, Home, Renters, Life, and
  Umbrella products.
- Regions: Northeast, Southeast, Midwest, Southwest, West.
- Channels: Independent Agent, Captive Agent, Direct, Online.
- Target model: `sm_insurance` in Direct Lake mode on Gold tables in
  `lh_insurance`.
- Lab path: ../labs/lab-06-semantic-model-directlake/README.md
- Core source: [Understand star schema and the importance for Power BI](sources.md#power-bi-and-fabric-modeling)

## Concept translation table

| Tableau concept | Power BI or Fabric concept | Workshop guidance |
| --- | --- | --- |
| Worksheet | Report visual | A worksheet that shows Loss Ratio by Product becomes one visual on a report page. |
| Dashboard | Report page | Warning: a Power BI dashboard is a different Service pin-board made from pinned visuals. |
| Story | Report navigation or PowerPoint export | Use pages, bookmarks, buttons, and narrative summaries. |
| Published data source | Shared semantic model | Use `sm_insurance` as the certified reusable model for reports. |
| Extract `.hyper` | Import mode or Direct Lake | Flat extracts map to Import. Fabric Delta tables can map to Direct Lake. |
| Live connection | DirectQuery or Direct Lake | Use Direct Lake for OneLake Delta freshness with Import-like speed. |
| Data pane fields | Model fields and measures | Hide technical columns and expose business names. |
| Calculated field | DAX measure or calculated column | Prefer measures for aggregations such as Loss Ratio. |
| LOD `FIXED` | `CALCULATE` with explicit filter context | Create a measure that ignores visual granularity where needed. |
| LOD `INCLUDE` | `CALCULATE`, iterators, or grouping tables | Add grain to the measure logic, not to every visual. |
| LOD `EXCLUDE` | `CALCULATE` with `REMOVEFILTERS` | Remove Product, Region, or Agent filters intentionally. |
| Table calculation | DAX time intelligence or visual calculation | Use model measures for YoY, running totals, and prior period logic. |
| Parameter | Field parameter or what-if parameter | Let users switch Product, Region, Channel, or metric. |
| Set | Group, calculated table, or calculation group | Use groups for static cohorts and calculation groups for metric logic. |
| Group | Power BI group or dimension attribute | Keep reusable insurance groupings in dimension tables when possible. |
| Tableau Prep | Dataflow Gen2 or notebook | Use visual Power Query for simple prep, notebooks for medallion transforms. |
| Tableau Server or Cloud | Power BI Service and Microsoft Fabric | Fabric hosts Lakehouse, Warehouse, semantic model, reports, pipelines, and apps. |
| Row-level security | Power BI RLS | Secure region, agency, or book of business in the semantic model. |
| VizQL | Power BI engine and DAX | DAX measures plus filter context drive query behavior. |

## Key mindset shifts

| Shift | What changes | Insurance example |
| --- | --- | --- |
| Workbook-first to model-first | Business logic moves out of each workbook and into `sm_insurance`. | Define Loss Ratio once as `DIVIDE([Incurred Losses], [Earned Premium])`. |
| Extract sprawl to one governed copy | Replace many `.hyper` extracts with Gold Delta tables and a semantic model. | `gold_loss_ratio` supports executive, product, and agent reports. |
| Sheet logic to reusable measures | Measures are shared across pages and reports. | Written Premium YoY % is consistent for Auto and Home. |
| Wide table to star schema | Facts and dimensions separate grain and descriptive attributes. | `fact_premium` joins to `dim_agent`, `dim_policy`, and `dim_date`. |
| Dashboard as artifact to dashboard as pin-board | A Power BI report page is the design surface. | The executive view is a report page, not a Service dashboard. |

## Insurance examples

### Tableau LOD example

Tableau idea:

```text
{ FIXED [Region] : SUM([Written Premium]) }
```

Power BI measure pattern:

```DAX
Written Premium by Region =
CALCULATE(
    [Written Premium],
    ALLEXCEPT('dim_agent', 'dim_agent'[Region])
)
```

Use this when the page has Product, Channel, or Agent filters, but the business
question is explicitly regional.

### Tableau table calculation example

Tableau idea:

```text
LOOKUP(SUM([Written Premium]), -12)
```

Power BI measure pattern:

```DAX
Written Premium PY =
CALCULATE(
    [Written Premium],
    SAMEPERIODLASTYEAR('dim_date'[period_begin])
)
```

The measure belongs in `sm_insurance` so every report page uses the same YoY
definition.

## Model-first checklist

- Confirm the grain of each fact table before building visuals.
- Use `fact_premium` for premium and policy counts.
- Use `fact_claim` for incurred losses, paid losses, and claim counts.
- Use `dim_date` for month, quarter, and prior year logic.
- Use `dim_agent` for agency, channel, and book of business analysis.
- Hide surrogate keys from report authors.
- Name fields in business language, for example `Written Premium`, not
  `written_premium`.
- Add descriptions to key measures so Copilot and authors understand intent.
- Certify `sm_insurance` only after tie-out and owner review.

## Migration rule of thumb

| If the Tableau workbook has... | Start with... | Reason |
| --- | --- | --- |
| One flat extract and many calculated fields | Star schema rebuild | The model will be cleaner than copying sheet logic. |
| A stable certified data source | Shared semantic model | Reuse the same business layer. |
| Heavy custom visuals and layout | Report rebuild | Recreate the experience using Power BI-native visuals. |
| Complex prep logic | Dataflow Gen2 or notebook | Keep transformation code outside the report. |
| Live operational queries | Direct Lake or DirectQuery assessment | Match freshness needs before choosing storage mode. |

## Related workshop files

- Migration plan: migration-approaches.md
- Governance worksheet: ../governance/migration-assessment-worksheet.md
- Direct Lake reference: direct-lake.md
- Copilot authoring: copilot-in-power-bi.md
- Source list: sources.md
