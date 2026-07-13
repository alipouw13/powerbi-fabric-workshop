# Migration assessment worksheet

Use this worksheet to inventory Tableau content before deciding what to migrate, consolidate, rebuild, or retire.
Copy the table into Excel, Power BI, or a planning board for migration wave management.

Related docs:

- [Tableau to Power BI concept translation](../reference/tableau-to-powerbi.md)
- [Migration approaches](../reference/migration-approaches.md)
- [Endorsement and certification](endorsement-certification.md)

## Inventory template

| Workbook | Owner | # sheets | Data sources | Extract vs Live | Complexity 1-5 | Business value 1-5 | Priority | Target semantic model | Approach rebuild/re-platform | Notes |
| --- | --- | ---: | --- | --- | ---: | ---: | --- | --- | --- | --- |
| Housing Market | Analytics Enablement | 12 | Redfin market tracker, MLS listings | Extract | 3 | 5 | Wave 1 | Housing-Market-Insights | Rebuild | Good POC. Convert wide extract into Fabric star schema and Direct Lake model. |
|  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |

## Field guidance

| Field | How to fill it |
| --- | --- |
| Workbook | Tableau workbook or project name. |
| Owner | Business owner, not only the publisher. |
| # sheets | Count worksheets, dashboards, and story points if useful. |
| Data sources | Published data sources, embedded connections, extracts, files, and custom SQL. |
| Extract vs Live | Note extract, live, mixed, or unknown. |
| Complexity 1-5 | Technical difficulty to migrate. Use the rubric below. |
| Business value 1-5 | Business criticality and adoption value. Use the rubric below. |
| Priority | Wave 1, Wave 2, backlog, retire, or investigate. |
| Target semantic model | Existing or planned Power BI semantic model. |
| Approach rebuild/re-platform | Rebuild, re-platform, consolidate, retire, or investigate. |
| Notes | Risks, dependencies, validation needs, and open questions. |

## Complexity scoring rubric

| Score | Description | Examples |
| --- | --- | --- |
| 1 | Simple workbook | One source, few visuals, limited calculations, no security logic. |
| 2 | Low complexity | Multiple pages, straightforward filters, common calculations. |
| 3 | Moderate complexity | Several sources, LOD expressions, parameters, or custom SQL. |
| 4 | High complexity | Heavy workbook logic, nested table calculations, entitlement rules, or performance issues. |
| 5 | Very high complexity | Regulated reporting, complex security, unclear ownership, or fragile source dependencies. |

## Business value scoring rubric

| Score | Description | Examples |
| --- | --- | --- |
| 1 | Low value | Low usage, duplicate report, no clear owner. |
| 2 | Limited value | Useful to a small team but not operationally critical. |
| 3 | Moderate value | Recurring business review or team planning input. |
| 4 | High value | Leadership reporting, revenue or risk decisions, broad adoption. |
| 5 | Critical value | Executive, regulatory, client-impacting, or operationally required. |

## Priority matrix

| Business value | Complexity | Priority recommendation |
| --- | --- | --- |
| 4-5 | 1-2 | Wave 1 quick win. |
| 4-5 | 3 | Wave 1 or Wave 2 with POC. |
| 4-5 | 4-5 | POC, then phased rebuild. |
| 2-3 | 1-3 | Backlog or self-service migration. |
| 1-2 | 4-5 | Retire, archive, or consolidate unless required. |

## Approach definitions

| Approach | Definition |
| --- | --- |
| Rebuild | Redesign the solution around a shared semantic model and Power BI report. |
| Re-platform | Move the workbook experience with minimal redesign for speed or parity. |
| Consolidate | Replace several Tableau workbooks with one model and one or more reports. |
| Retire | Decommission content because value is low or a replacement exists. |
| Investigate | Ownership, source, usage, or security is unclear. |

## Filled example

| Workbook | Owner | # sheets | Data sources | Extract vs Live | Complexity 1-5 | Business value 1-5 | Priority | Target semantic model | Approach rebuild/re-platform | Notes |
| --- | --- | ---: | --- | --- | ---: | ---: | --- | --- | --- | --- |
| Housing Market | Analytics Enablement | 12 | `market_tracker.csv`, `listings.csv` | Extract | 3 | 5 | Wave 1 | `Housing-Market-Insights` | Rebuild | Use Fabric `lh_housing`, Gold tables, Direct Lake, and certified semantic model. Validate `Homes Sold`, `Inventory`, and `Avg Median Sale Price`. |

## Assessment meeting agenda

1. Confirm owner and audience.
2. Identify the business decision supported by the workbook.
3. Review sources and refresh paths.
4. List calculations that must become model measures.
5. Score complexity and business value.
6. Pick approach and target semantic model.
7. Assign validation owner.
8. Decide whether to retire, consolidate, or migrate.
