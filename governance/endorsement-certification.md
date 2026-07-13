# Endorsement and certification

Endorsement helps users find trusted Power BI and Fabric content.
For a Tableau migration, it is one of the main controls that prevents "one model per workbook" sprawl from reappearing in Power BI.

Microsoft reference:

- [Promote and certify Power BI content with endorsement](https://learn.microsoft.com/en-us/power-bi/collaborate-share/service-endorsement-overview)

## Promoted vs Certified

| Endorsement | Meaning | Who can apply | Use in this workshop |
| --- | --- | --- | --- |
| Promoted | The owner believes the content is useful, maintained, and ready for broader discovery | Content owners, based on tenant settings | Use for promising reports and models after owner review. |
| Certified | The organization has reviewed and approved the content as authoritative | Approved certifiers only | Use for governed semantic models and production reports. |

Promoted means "useful and visible."
Certified means "authoritative and governed."

## Why endorsement matters during migration

Tableau estates often accumulate repeated extracts and workbook-specific calculations.
Power BI can repeat the same pattern if every migrated report gets its own model.
Endorsement steers authors toward shared, trusted models.

For the housing workshop:

1. `market_tracker.csv` is the familiar flat extract.
2. Silver and Gold tables become governed Fabric data products.
3. `Housing-Market-Insights (Direct Lake)` becomes the reusable semantic model.
4. Reports should connect to that model instead of creating new model copies.
5. Certification tells authors which model is the source of truth.

## Certification criteria for a semantic model

| Area | Criteria |
| --- | --- |
| Ownership | Named business owner, technical owner, and backup owner. |
| Business definition | Core measures are documented in business language. |
| Data lineage | Source tables and transformation path are known. |
| Model design | Star schema or justified alternative, clear relationships, hidden technical fields. |
| Measures | Shared measures exist for common metrics and are not duplicated in reports. |
| Security | RLS roles are tested if the model contains restricted data. |
| Sensitivity | Correct sensitivity label is applied. |
| Quality | Reconciled totals and row counts are documented. |
| Performance | Key report pages meet agreed performance expectations. |
| Support | Support channel, SLA expectation, and change process are known. |
| Deployment | Dev/Test/Prod path is defined and repeatable. |

## Certification criteria for a report

| Area | Criteria |
| --- | --- |
| Source model | Uses a certified or approved semantic model where possible. |
| Purpose | Clear audience and decision supported by the report. |
| Usability | Pages are named, filters are clear, and default views are useful. |
| Accessibility | Colors, labels, and visual choices support broad use. |
| Validation | Numbers tie out to the certified model or approved source. |
| Ownership | Report owner and backup owner are assigned. |
| Lifecycle | Report is deployed through the approved workspace path. |
| Support | Users know where to request help or changes. |

## Certifier roles

| Role | Responsibility |
| --- | --- |
| Business data owner | Confirms definitions, audience, and decision relevance. |
| BI model owner | Confirms measures, relationships, and model usability. |
| Data engineering owner | Confirms Fabric table lineage and load health. |
| Security or compliance reviewer | Confirms labels, RLS, and sharing constraints. |
| Fabric or Power BI admin | Confirms workspace, tenant, and capacity policy alignment. |

Certifiers should be named in the migration wave plan.
Avoid anonymous approval queues.

## Endorsement workflow

1. Author builds in `Schwab-Analytics-Dev`.
2. Owner reviews business definitions and source lineage.
3. Technical reviewer validates model relationships, measures, and performance.
4. Content moves to `Schwab-Analytics-Test`.
5. UAT users validate key numbers and report usability.
6. Owner requests promoted or certified status.
7. Approved certifier applies certification in Prod.
8. Adoption communications point users to the endorsed artifact.

## Anti-sprawl rules

- Do not certify two semantic models that define the same metric differently unless the difference is intentional and documented.
- Do not certify report-level measures as enterprise definitions.
- Do not certify a model without a named owner.
- Do not promote a model that lacks measure descriptions for core metrics.
- Retire duplicate models when a certified replacement exists.
- Use endorsement status in training so authors learn where to start.

## Workshop certification target

The first certification candidate is `Housing-Market-Insights (Direct Lake)`.
Certification is appropriate only after:

- Gold tables are stable.
- Core measures are validated.
- Relationships are reviewed.
- Descriptions are added.
- Sensitivity label decision is recorded.
- Report authors confirm the model supports the required pages.
