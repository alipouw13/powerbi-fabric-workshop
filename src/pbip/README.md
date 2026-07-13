# PBIP + the shared semantic model (Contoso Insurance workshop)

The `sm_insurance` model is stored as a **PBIP** (Power BI Project): plain-text
**TMDL** and report JSON you can diff, review, and ship with Git and CI/CD,
exactly like application code. This is the "DevOps for BI" story a Tableau team
usually does not have (Tableau workbooks are opaque binaries).

## Save as PBIP
In Power BI Desktop: **File -> Options -> Preview features -> Power BI Project
(.pbip) save option**, then **File -> Save as -> .pbip**. You get:

```
sm_insurance.SemanticModel/   <- TMDL: tables, measures, relationships
rpt_insurance_executive.Report/   <- report pages as JSON
```

Commit the folders. Do not commit `.pbix`, caches, or local settings (see the
repo `.gitignore`).

## The model (star schema)
- Facts: `fact_premium` (grain: policy x month), `fact_claim` (grain: claim)
- Dimensions: `dim_customer`, `dim_agent`, `dim_policy`, `dim_coverage`, `dim_date`
- Storage mode: **Direct Lake** on the Lakehouse gold tables (no import, no refresh)
- Relationships: single direction, facts -> dims; mark `dim_date` as the date table
  on `period_begin`. Relate `fact_premium` and `fact_claim` to `dim_policy`,
  `dim_date`, and (for claims) `dim_coverage`.

## Core measures (defined ONCE, reused by every report)
Add these to a measures table. Loss ratio is the headline P&C metric.

```dax
Written Premium       = SUM(fact_premium[written_premium])
Earned Premium        = SUM(fact_premium[earned_premium])
Policies Written      = SUM(fact_premium[policies_written])
Policies In Force     = SUM(fact_premium[policies_inforce])
Incurred Losses       = SUM(fact_claim[incurred_loss])
Paid Losses           = SUM(fact_claim[paid_loss])
Claim Count           = COUNTROWS(fact_claim)
Loss Ratio            = DIVIDE([Incurred Losses], [Earned Premium])
Average Premium       = DIVIDE([Written Premium], [Policies Written])

Written Premium PY =
CALCULATE([Written Premium], DATEADD(dim_date[period_begin], -12, MONTH))

Written Premium YoY % =
DIVIDE([Written Premium] - [Written Premium PY], [Written Premium PY])
```

> Let **Copilot** draft these: in Power BI, use the DAX query view Copilot or the
> measure-description Copilot, then paste the verified measure here. See
> [Lab 7](../../labs/lab-07-copilot-reports/README.md).

## AI-ready metadata (so Copilot and the Data Agent answer well)
- Friendly table/column names; hide key columns (`policy_id`, `date_id`, ...).
- Measure descriptions (Copilot can generate these), e.g. "Loss Ratio = incurred
  losses divided by earned premium; lower is better."
- **Prep for AI** on the model: AI data schema, AI instructions, verified answers.
  This same metadata is what the **Power BI MCP server** returns from its "Get
  Semantic Model Schema" tool (see [Lab 9](../../labs/lab-09-mcp-github-copilot/README.md)).

## Consistency with the Contoso Insurance demo
These names align to the Contoso Insurance end-to-end Fabric demo
(github.com/alipouw13/fabric-test), so the workshop lab and that demo tell one
story. See [reference/reference-apps.md](../../reference/reference-apps.md).
