# Endorsement and certification

Endorsement helps people find content they can trust. In I&O the main
certification candidates are the five domain semantic models, `sm_io_itsm`,
`sm_io_capacity`, `sm_io_mainframe`, `sm_io_servicedesk` and `sm_io_assets`,
because many reports should reuse the same measures rather than each defining
their own.

## Endorsement levels

| Level | Meaning | Who can apply it | I&O example |
| --- | --- | --- | --- |
| None | Default. Work in progress. | Anyone | Anything in `IO-Analytics-Dev` |
| Promoted | The owner recommends it. | Content owners, subject to tenant settings | A report ready for wider testing |
| Certified | It meets the organization's quality bar. | Approved certifiers only | `sm_io_itsm` after tie-out and owner approval |

Certification is applied to the **semantic model** first. Reports built on a
certified model inherit the trust; certifying a report that sits on an
uncertified private model is backwards.

## Why this matters here

Without certification, every migrated Tableau workbook becomes a new Power BI
semantic model, and the estate recreates extract sprawl under a new name. Five
groups, five domains, and no certification produces fifteen models within a
quarter.

Certification should make the preferred path obvious:

1. Use the certified semantic model for your domain.
2. Build a thin report on top of it.
3. Request a change to a shared measure instead of forking the model.
4. Retire duplicate private models.

## Certification criteria

Apply these to any `sm_io_<domain>` model before certifying.

| Area | Criteria | Evidence |
| --- | --- | --- |
| Ownership | Business and technical owners are named. | Ownership table in [workspace-governance.md](workspace-governance.md) |
| Lineage | Sources and transformations are documented. | Source list plus the Power Query steps, with named steps |
| Model design | Star schema, single-direction one-to-many relationships, `dim_date` marked. | Model diagram and the checklist in [star-schema.md](../reference/star-schema.md) |
| Grain | The grain of the fact table is stated. | Table description in the model |
| Measures | Every measure is named in business language, described, and formatted. | Measure list, see [measure definitions](../src/pbip/README.md) |
| Tie-out | Totals reconcile to the Tableau report being replaced, at the agreed grain. | Validation query output, see [sample_dax_queries.dax](../src/sql/sample_dax_queries.dax) |
| Data quality | No orphaned fact keys, no duplicate dimension keys, no gaps in `dim_date`. | Validation queries V1 to V4 |
| Security | RLS roles tested with a real test user in the Service. | Test evidence |
| Sensitivity | A Purview label is applied. | Item label |
| Refresh | Scheduled refresh succeeds, failure alerts go to a monitored mailbox. | Refresh history |
| Performance | Key pages render within the agreed target, with the gateway in the path. | Test notes |
| Support | Support contact and change request process are documented. | Workspace description |

## Measures requiring review before certification

The validation grain for the domain measures. Nothing is certified until its
totals tie out.

### ITSM, `sm_io_itsm`

| Measure | Required validation |
| --- | --- |
| Total Incidents | Ties by month, service, severity and team against the Tableau extract |
| Resolved Incidents | Ties by month and incident state |
| Avg Resolve Minutes | Ties by severity, and open incidents are demonstrably excluded |
| SLA Met % | Denominator is resolved incidents, and the owner agrees that is right |
| Major Incidents | Ties to the major incident log |
| Reopened Rate | Ties by month and team |
| Incidents PM, PY, MoM Change %, YoY Change % | Blank in the first period, correct at period boundaries |
| Percent of Total Incidents | The ALL versus ALLSELECTED choice is documented in the description |

### Capacity, `sm_io_capacity`

| Measure | Required validation |
| --- | --- |
| Avg CPU Utilization, Avg Memory Utilization | Averaged, never summed. Plausible range on sight |
| CIs Over 80% CPU | Counts distinct CIs, not monthly rows |
| Avg Headroom % | Ties by service and environment |
| Storage Utilization % | Computed from summed totals, not as an average of ratios |

### Mainframe, `sm_io_mainframe`

| Measure | Required validation |
| --- | --- |
| Total MIPS Consumed | Ties by month and LPAR |
| MIPS Utilization % | Capacity is not summed across days |
| Peak MIPS | Reflects the month-end peak, not the average |
| Batch Failure Rate | Denominator includes completed and failed jobs |

### Service desk, `sm_io_servicedesk`

| Measure | Required validation |
| --- | --- |
| Tickets Received, Tickets Resolved | Tie by month, team and location |
| First Contact Resolution % | Denominator is resolved, not received, and the owner agrees |
| Avg Handle Time, Avg Speed to Answer | Units stated in the measure name |
| Coverage % | Ties to the published staffing roster |

### Assets, `sm_io_assets`

| Measure | Required validation |
| --- | --- |
| Total Assets | Ties to the CMDB asset count |
| Assets Out of Warranty, Out of Warranty % | Tie by lifecycle status and site |
| CMDB Completeness % | The definition of complete is documented |
| Total Acquisition Cost, Annual Support Cost | Tie to the finance figure at the agreed grain |

## Who certifies

| Role | Responsibility |
| --- | --- |
| Domain reporting owner | Confirms the business definitions and the intended use |
| Semantic model owner | Confirms model structure, measures, descriptions and formats |
| I&O platform owner | Confirms workspace, gateway, refresh and tenant setting alignment |
| Data governance reviewer | Confirms sensitivity labels and access policy |
| Approved certifier | Applies certification once the criteria are met |

The certifier is not the builder. That separation is most of the value.

## Promotion path

| Stage | Endorsement | Rule |
| --- | --- | --- |
| Development | None | Builders iterate freely in `IO-Analytics-Dev` |
| Test | Promoted | Promote only after the owner's first review |
| Production pilot | Promoted | Use during parallel running against Tableau |
| Production standard | Certified | Apply after tie-out, security, ownership, labels and support are all complete |

Certification is not permanent. Re-review on the cadence in
[workspace-governance.md](workspace-governance.md), and pull certification if the
owner leaves and is not replaced.

## Discovery and reuse checklist

Before starting a new report, the author confirms:

- Is a certified `sm_io_<domain>` model already available?
- Does it contain the service, CI, team, location, severity and date fields
  needed?
- Are the required measures already defined?
- Does RLS support the intended audience?
- Is a thin report on the existing model sufficient?
- If not, is the gap written down and sent to the model owner?

If the answer to the last one is no, the author is about to build model number
sixteen.

## Related

- [Workspace governance](workspace-governance.md)
- [Migration assessment worksheet](migration-assessment-worksheet.md)
- [Adoption roadmap](adoption-roadmap.md)
- [Star schema](../reference/star-schema.md)
- [Measure definitions](../src/pbip/README.md)
- [Sample DAX and validation queries](../src/sql/sample_dax_queries.dax)
