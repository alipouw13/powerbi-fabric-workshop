# Endorsement and certification

Endorsement helps users find trustworthy content. In this workshop, the main
candidate for certification is `sm_insurance`, because many reports should
reuse the same insurance measures instead of creating one model per workbook.

## Endorsement levels

| Level | Meaning | Who can use it | Workshop example |
| --- | --- | --- | --- |
| Promoted | The item is useful and recommended by its owner. | Content creators, depending on tenant settings. | A report page ready for broader testing. |
| Certified | The item meets organizational quality standards. | Approved certifiers only. | `sm_insurance` after validation and owner approval. |

See [sources.md](../reference/sources.md#governance-and-security) for Microsoft
Learn endorsement references.

## Why certification matters here

Without certification, every migrated Tableau workbook can become a new Power BI
semantic model. That recreates extract sprawl under a new name.

Certification should make the preferred path obvious:

1. Use the certified semantic model.
2. Build thin reports from it.
3. Request changes to shared measures instead of forking the model.
4. Retire duplicate private models.

## Certification criteria for `sm_insurance`

| Area | Criteria | Evidence |
| --- | --- | --- |
| Ownership | Business and technical owners are named. | Ownership table in workspace governance. |
| Data lineage | Sources and transformations are documented. | Lakehouse, Warehouse, and pipeline lineage. |
| Model design | Star schema with clear relationships. | Model diagram and table list. |
| Measures | Core measures are reviewed and described. | Measure list with definitions. |
| Tie-out | Key totals reconcile to the Tableau extract or approved source. | Validation workbook or DAX query results. |
| Security | RLS roles are tested. | Test user screenshots or query evidence. |
| Sensitivity | Labels are applied. | Power BI item label. |
| Performance | Key report pages meet target response times. | Test notes and capacity observation. |
| Support | Support contact and change process are documented. | Workspace description or support page. |

## Core measures requiring review

| Measure | Required validation |
| --- | --- |
| Written Premium | Ties by month, product, region, and channel. |
| Earned Premium | Ties by month and product. |
| Policies In Force | Ties to active policy counts by period. |
| Policies Written | Ties to policy write counts by period. |
| Incurred Losses | Ties by month, product, and region. |
| Paid Losses | Ties by month and status where available. |
| Claim Count | Ties to claim rows and distinct claim numbers. |
| Loss Ratio | Equals Incurred Losses divided by Earned Premium. |
| Average Premium | Equals Written Premium divided by Policies Written. |
| Written Premium YoY % | Uses the approved prior-year period logic. |

## Who certifies

| Role | Responsibility |
| --- | --- |
| Insurance analytics owner | Confirms business definitions and report use. |
| Semantic model owner | Confirms model structure, measures, and descriptions. |
| Data engineering lead | Confirms source, transformation, and refresh design. |
| Fabric platform owner | Confirms workspace, capacity, and tenant setting alignment. |
| Compliance or data governance reviewer | Confirms labels and access policy for production data. |
| Approved certifier | Applies certification after criteria are met. |

## Promotion path

| Stage | Endorsement status | Rule |
| --- | --- | --- |
| Development | None | Builders can iterate freely in Dev. |
| Test | Promoted | Promote only after initial owner review. |
| Production pilot | Promoted | Use during parallel run and business validation. |
| Production standard | Certified | Apply after tie-out, security, ownership, and support are complete. |

## Curbing model sprawl

Use these rules during Tableau migration:

- Do not publish a new semantic model for every workbook.
- Do not copy DAX measures into report-specific models without review.
- Do not certify reports that depend on private duplicated models.
- Do map each migrated report to a target semantic model in the assessment
  worksheet.
- Do create a change request when a certified measure needs to change.

## Discovery and reuse checklist

Before starting a new report, authors should confirm:

- Is `sm_insurance` already certified?
- Does it contain the needed Product, Region, Channel, Agent, and Date fields?
- Are the required measures already present?
- Does RLS support the intended audience?
- Is a thin report sufficient?
- If not, is the model gap documented for the owner?

## Related workshop files

- Workspace governance: workspace-governance.md
- Assessment worksheet: migration-assessment-worksheet.md
- Tableau translation: ../reference/tableau-to-powerbi.md
- Copilot reference: ../reference/copilot-in-power-bi.md
