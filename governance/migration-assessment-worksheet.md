# Migration assessment worksheet

Use this worksheet before rebuilding Tableau content in Power BI. The purpose is
to decide what to rebuild, what to retire, what to consolidate, and which
semantic model should become the governed target.

## Worksheet table

| Workbook | Owner | # sheets | Data sources | Extract vs Live | Complexity 1-5 | Business value 1-5 | Priority | Target semantic model | Approach | Notes |
| --- | --- | ---: | --- | --- | ---: | ---: | --- | --- | --- | --- |
| Insurance Executive | Executive Reporting Owner | 12 | `policy_claims_extract.csv`, Claims Intake | Extract | 4 | 5 | P1 | `sm_insurance` | Rebuild | Validate Written Premium, Loss Ratio, Claim Count, and Region filters. |
|  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |

## Complexity rubric

| Score | Description | Examples |
| --- | --- | --- |
| 1 | Simple | Few visuals, one clean source, minimal calculations. |
| 2 | Low | Several sheets, basic filters, standard aggregations. |
| 3 | Moderate | Multiple sources, calculated fields, moderate interactivity. |
| 4 | High | LOD expressions, table calculations, RLS, complex layout. |
| 5 | Very high | Many sources, custom extensions, heavy prep, critical operations use. |

## Business value rubric

| Score | Description | Examples |
| --- | --- | --- |
| 1 | Low | Rarely used, no clear owner, low decision impact. |
| 2 | Limited | Used by a small team for non-critical monitoring. |
| 3 | Moderate | Used monthly or by a department lead. |
| 4 | High | Used weekly for business reviews or operational action. |
| 5 | Critical | Executive, regulatory, financial, or daily decision support. |

## Priority rules

| Priority | Use when | Recommended path |
| --- | --- | --- |
| P1 | High value and feasible within the migration wave. | POC, rebuild, validate, certify. |
| P2 | Important but depends on model or data readiness. | Sequence after shared model gaps close. |
| P3 | Low value or duplicate content. | Consolidate or retire. |
| Hold | Owner, source, or requirement is unclear. | Resolve before build starts. |

## Approach options

| Approach | Definition | Use for |
| --- | --- | --- |
| Rebuild | Design the model and report using Power BI patterns. | High-value workbooks with duplicated Tableau logic. |
| Re-platform | Recreate the report experience with minimal logic change. | Simple workbooks on governed data. |
| Consolidate | Replace multiple workbooks with one report or app. | Duplicate product, region, or agent views. |
| Retire | Archive and remove from active navigation. | Low-use or ownerless content. |

## Data source assessment

Capture details for each source:

- Source system or file.
- Refresh cadence.
- Extract size.
- Live query dependency.
- Credential owner.
- Gateway requirement.
- Data classification.
- Known quality issues.
- Replacement Fabric table or model.

For the workshop, `policy_claims_extract.csv` represents the flat Tableau
extract. The target is the modeled star schema behind `sm_insurance`.

## Calculation assessment

For each workbook, list:

- Calculated fields.
- LOD expressions.
- Table calculations.
- Parameters.
- Sets and groups.
- Custom fiscal calendars.
- Security filters.
- Measures that should become shared DAX.

Any measure used by more than one report should be a candidate for the semantic
model, not a report-only calculation.

## Validation notes

| Metric | Tie-out grain | Expected source |
| --- | --- | --- |
| Written Premium | Month, Product, Region | Tableau extract and `fact_premium` |
| Earned Premium | Month, Product | Tableau extract and `fact_premium` |
| Incurred Losses | Month, Product, Region | Tableau extract and `fact_claim` |
| Claim Count | Month, Product, Severity | Tableau extract and `fact_claim` |
| Loss Ratio | Month, Product, Region | DAX measure validation |

## Exit criteria for a workbook

- Owner confirms the replacement scope.
- Target semantic model is named.
- Priority and approach are assigned.
- Required calculations are mapped to DAX measures.
- RLS and sensitivity needs are documented.
- Validation grain is agreed.
- Cutover and retirement path are known.

## Related workshop files

- Migration approaches: ../reference/migration-approaches.md
- Tableau translation: ../reference/tableau-to-powerbi.md
- Certification: endorsement-certification.md
- Adoption roadmap: adoption-roadmap.md
