# Tableau to Power BI migration approaches

Start migration work with inventory, not visuals. The fastest way to create a
new mess is to rebuild every Tableau workbook as a separate Power BI report and
semantic model.

## Workshop outcome

By the end of this workshop, the team should know how to move from a Tableau
extract-centered estate to a Fabric-centered estate:

- Lakehouse: `lh_insurance`
- Warehouse: `wh_insurance`
- Semantic model: `sm_insurance`
- Report: `rpt_insurance_executive`
- Environments: `Schwab-Analytics-Dev`, `Schwab-Analytics-Test`,
  `Schwab-Analytics-Prod`

Microsoft migration guidance is listed in [sources.md](sources.md#migration-and-delivery).

## Migration stages

| Stage | Output | Owner | Workshop artifact |
| --- | --- | --- | --- |
| Inventory | Workbook list, owners, data sources, usage | BI lead | ../governance/migration-assessment-worksheet.md |
| Assess | Complexity and value scoring | BI lead plus business owner | Worksheet rubric |
| Prioritize | Ranked backlog | Sponsor plus CoE | Adoption roadmap |
| Prove | POC with success criteria | Delivery squad | `rpt_insurance_executive` slice |
| Rebuild | Shared model, report pages, validation | Delivery squad | `sm_insurance` and report |
| Cut over | Published app, training, deprecation plan | Product owner | Governance checklist |

## Inventory fields to collect

Use the worksheet in ../governance/migration-assessment-worksheet.md. At a
minimum, capture:

- Workbook name
- Business owner
- Report audience
- Number of sheets and dashboards
- Tableau data sources
- Extract or live connection
- Refresh cadence
- Key metrics
- Row-level security needs
- Usage over the last 90 days
- Known pain points
- Target semantic model

## Value x complexity prioritization

| Category | Business value | Technical complexity | Action |
| --- | --- | --- | --- |
| Quick win | High | Low | Migrate early and use in enablement. |
| Strategic | High | High | Run a POC before full rebuild. |
| Commodity | Low | Low | Migrate only if still used. |
| Retire candidate | Low | High | Archive or replace with a shared report. |

For Contoso Insurance, the "Insurance Executive" workbook is a strategic early
candidate because it validates Written Premium, Earned Premium, Loss Ratio, and
Claim Count against executive expectations.

## Rebuild vs re-platform

| Approach | Use when | Avoid when |
| --- | --- | --- |
| Rebuild in Power BI | Business logic is duplicated, extracts are wide, or the target is a shared semantic model. | The workbook is a temporary one-off. |
| Re-platform layout first | The workbook is visually simple and already uses a clean governed source. | Tableau calculations are complex or undocumented. |
| Replace with existing report | Usage overlaps with another migration candidate. | The report serves a unique regulated workflow. |
| Retire | Usage is low and the owner agrees. | The workbook is tied to required reporting. |

## Model-based migration

Model-based migration creates the reusable layer first.

| Step | Contoso Insurance example |
| --- | --- |
| Identify facts | `fact_premium`, `fact_claim` |
| Identify dimensions | `dim_policy`, `dim_customer`, `dim_agent`, `dim_coverage`, `dim_date` |
| Define measures | Written Premium, Earned Premium, Incurred Losses, Loss Ratio |
| Validate totals | Compare the wide `policy_claims_extract.csv` to model totals |
| Build reports | Executive summary, product trends, agent scorecard |

This is the preferred path for high-value shared reporting.

## Report-based migration

Report-based migration starts with a workbook and rebuilds the user experience.

Use it when:

- The Tableau workbook has few calculations.
- The data source is already governed.
- The audience needs a like-for-like replacement.
- The report is not a candidate for a new enterprise semantic model.

Still avoid creating one semantic model per workbook. If two reports use the
same measures, they should share `sm_insurance` or another governed model.

## POC success criteria

The Microsoft proof-of-concept guidance recommends validating assumptions,
understanding product differences, and testing with real data. For this
workshop, a POC should prove:

| Area | Success criterion |
| --- | --- |
| Data | Written Premium ties to Tableau within agreed tolerance. |
| Model | Loss Ratio uses one certified DAX measure. |
| Performance | Executive page renders within the target service-level objective. |
| Security | Region or book-of-business RLS works for test users. |
| Delivery | Dev to Test to Prod movement is repeatable. |
| Adoption | At least one business owner signs off on the replacement. |

## Validation checklist

- Reconcile total Written Premium by month.
- Reconcile Earned Premium by product.
- Reconcile Incurred Losses by region.
- Reconcile Claim Count by severity and status.
- Confirm Loss Ratio equals `DIVIDE([Incurred Losses], [Earned Premium])`.
- Check blanks, zero denominators, and inactive policies.
- Validate filters for Product, Region, Channel, and Agent.
- Test RLS with a user who should see only one region or book.

## Cutover pattern

| Step | Action |
| --- | --- |
| Announce | Tell users which Tableau workbook is being replaced and why. |
| Parallel run | Keep both reports available for a defined validation window. |
| Train | Run a short session on filters, drill, export, and subscriptions. |
| Certify | Certify the semantic model after owner approval. |

## Related workshop files

- Translation guide: tableau-to-powerbi.md
- Direct Lake reference: direct-lake.md
- Governance worksheet: ../governance/migration-assessment-worksheet.md
