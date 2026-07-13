# Tableau to Power BI migration approaches

This guide describes how Schwab teams should migrate Tableau content into Power BI and Microsoft Fabric.
The goal is not to clone every workbook.
The goal is to preserve trusted decisions, consolidate repeated logic, and reduce workbook sprawl.

Related workshop assets:

- Inventory template: [migration assessment worksheet](../governance/migration-assessment-worksheet.md)
- Direct Lake model lab: [lab 06](../labs/lab-06-semantic-model-directlake/README.md)
- PBIP reference: [src/pbip](../src/pbip/README.md)

## Grounding guidance

Microsoft frames migration as a staged program: set up and evaluate, create new solutions, migrate selected assets, then adopt, govern, and monitor.
See [Power BI migration overview](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-migration-overview).
For technical risk reduction, use a proof of concept.
See [Conduct proof of concept to migrate to Power BI](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-migration-proof-of-concept).

## Migration flow

| Step | Output | Schwab workshop action |
| --- | --- | --- |
| 1. Inventory | List of workbooks, owners, sources, usage, extracts, live connections, and calculations | Start with the [assessment worksheet](../governance/migration-assessment-worksheet.md). |
| 2. Assess | Complexity score and business value score | Score from 1 to 5, then classify into waves. |
| 3. Prioritize | Value x complexity matrix | Move high-value, low-complexity reports first. |
| 4. Choose approach | Rebuild, re-platform, retire, or consolidate | Avoid copying a workbook if a shared model can replace it. |
| 5. Build POC | Small validated solution | Use the housing model to test Direct Lake, DAX, RLS, and report parity. |
| 6. Validate | Reconciled metrics and user acceptance | Numbers must tie out before cutover. |
| 7. Cut over | Production report and adoption plan | Publish to `Schwab-Analytics-Prod` and communicate the new certified source. |
| 8. Monitor | Usage, refresh, capacity, and defect tracking | Review adoption and capacity health weekly during launch. |

## Inventory and assess workbooks

Capture each Tableau workbook before making design decisions.
Do not start by recreating tabs.
Start by asking what decisions the workbook supports.

Minimum inventory fields:

- Workbook name
- Business owner
- Technical owner
- Data sources
- Extract or live connection
- Number of sheets
- Custom SQL
- Calculated fields
- LOD expressions
- Table calculations
- Parameters
- RLS or entitlement rules
- Refresh or publishing cadence
- Business criticality
- Known data quality issues

Use the worksheet: [migration-assessment-worksheet.md](../governance/migration-assessment-worksheet.md).

## Prioritize by value x complexity

| Category | What it means | Recommended action |
| --- | --- | --- |
| High value, low complexity | Important report, simple sources, few calculations | First migration wave. |
| High value, high complexity | Executive or regulated report, heavy logic | POC first, then rebuild with governed model. |
| Low value, low complexity | Useful but not critical | Backlog or self-service rebuild. |
| Low value, high complexity | Expensive to migrate and low usage | Retire, archive, or consolidate. |

## Choose rebuild or re-platform

| Approach | Use when | Avoid when |
| --- | --- | --- |
| Rebuild | Logic should move into a shared semantic model, visuals can be improved, or data needs Fabric governance | Users require pixel-perfect temporary parity. |
| Re-platform | Workbook is stable, scoped, and needed quickly with minimum redesign | The workbook embeds duplicated metrics or fragile custom SQL. |
| Consolidate | Several workbooks answer the same question with different extracts | One team still owns a legitimate specialized workflow. |
| Retire | Usage is low, owner is gone, or source is superseded | The report is required for audit, legal, or operational continuity. |

## Model-based vs report-based migration

Tableau estates often grow one workbook at a time.
Power BI works better when reusable logic lives in a semantic model.

For this workshop:

1. Build `lh_housing` in Fabric.
2. Promote raw data from Bronze to Silver to Gold.
3. Build `Housing-Market-Insights (Direct Lake)` on Gold tables.
4. Create thin reports against that model.
5. Certify the model once it meets governance criteria.

## POC success criteria

Use the housing market use case as the POC pattern.

| Area | Success criterion |
| --- | --- |
| Data parity | `Homes Sold`, `Inventory`, and `Avg Median Sale Price` reconcile to the Tableau extract. |
| Model design | Dimensions filter facts correctly by date, region, and property type. |
| Performance | Primary report pages open and filter interactively for 24 months x 12 metros x 4 property types. |
| Security | Test users see only the intended region or role scope when RLS is enabled. |
| Authoring | Report authors can build pages without copying DAX from another report. |
| Governance | Owners, endorsements, sensitivity labels, and deployment path are assigned. |

## Validation

Numbers must tie out before users switch tools.
Validate at multiple grains:

- Total `Homes Sold` by month
- Total `Inventory` by metro
- `Avg Median Sale Price` by property type
- `Homes Sold PY` for prior-year comparison
- `Homes Sold YoY %` against the Tableau workbook logic
- Row counts from Bronze, Silver, and Gold tables

When numbers differ, document whether the cause is source filtering, date logic, aggregation grain, null handling, or an intentional business-rule change.

## Cutover and adoption

1. Publish the validated report to `Schwab-Analytics-Prod`.
2. Endorse or certify the semantic model before broad rollout.
3. Announce the new report, owner, support path, and retirement date for the old workbook.
4. Keep the Tableau version read-only during the parallel run if policy allows it.
5. Monitor usage, defects, and data refresh or Direct Lake behavior.
6. Retire duplicated extracts once adoption is stable.

## Microsoft Learn anchors

- [Power BI migration overview](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-migration-overview)
- [Conduct proof of concept to migrate to Power BI](https://learn.microsoft.com/en-us/power-bi/guidance/powerbi-migration-proof-of-concept)
- [Overview of Fabric deployment pipelines](https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/intro-to-deployment-pipelines)
