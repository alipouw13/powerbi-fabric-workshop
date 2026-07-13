# Direct Lake for the Contoso Insurance semantic model

Direct Lake is the storage mode used for `sm_insurance`. It lets Power BI load
OneLake Delta data into memory on demand without importing a scheduled copy into
the semantic model.

## Lab connection

- Lab: ../labs/lab-06-semantic-model-directlake/README.md
- Lakehouse: `lh_insurance`
- Warehouse: `wh_insurance`
- Semantic model: `sm_insurance`
- Source: [Direct Lake overview](sources.md#power-bi-and-fabric-modeling)

## What Direct Lake means

| Idea | Practical meaning |
| --- | --- |
| Data stays in OneLake | Tables are stored as Delta data in Fabric. |
| No scheduled import refresh | The model does not need a separate import refresh cycle for those tables. |
| Loaded into memory on demand | Power BI loads column data as needed for queries. |
| Import-like performance goal | Queries can run fast because data is cached in memory. |
| Fresher than Import | Data can be available after upstream Delta tables are updated. |

Direct Lake is often the easiest bridge for Tableau users who like the idea of a
live connection but want the performance profile of an in-memory model.

## Requirements to confirm

| Requirement | Workshop setting |
| --- | --- |
| Fabric capacity | Workspaces run on Fabric capacity. |
| Supported storage | Gold tables are Delta tables in OneLake. |
| Fabric item | Tables come from a Lakehouse or Warehouse. |
| Semantic model | `sm_insurance` is configured in Direct Lake mode. |
| Permissions | Users have appropriate workspace and model access. |
| Governance | Sensitivity labels and endorsement are applied after validation. |

## Storage mode comparison

| Mode | Data movement | Refresh model | Query behavior | Good fit |
| --- | --- | --- | --- | --- |
| Import | Data is copied into the semantic model. | Scheduled refresh. | Fast in-memory queries. | Small to medium stable models. |
| DirectQuery | Queries are sent to the source. | No import refresh. | Depends on source query performance. | Operational sources requiring source-time freshness. |
| Direct Lake | Delta data is loaded from OneLake into memory on demand. | No scheduled import refresh for Direct Lake tables. | Import-like speed with OneLake data freshness. | Fabric Lakehouse or Warehouse analytics. |

## DirectQuery fallback

Direct Lake models can fall back to DirectQuery in some situations. Treat
fallback as a design signal, not just an implementation detail.

| Signal | Action |
| --- | --- |
| Query unexpectedly behaves like DirectQuery | Review model features and table support. |
| Performance changes after a model edit | Check if the edit introduced fallback behavior. |
| Users report slow visuals | Test DAX, visual grain, and table eligibility. |
| Security design changed | Re-test RLS and permissions. |

For a workshop, document any fallback observed during setup. Do not surprise
participants during a live demo.

## Insurance table mapping

| Layer | Table | Direct Lake role |
| --- | --- | --- |
| Bronze | `bronze_policy_claims` | Landing copy of the flat Tableau-style extract. |
| Bronze | `bronze_claims_intake` | Operational intake feed for claims. |
| Silver | `dim_policy` | Policy attributes and product mapping. |
| Silver | `dim_customer` | Customer segment and region. |
| Silver | `dim_agent` | Agent, agency, channel, and region. |
| Silver | `dim_coverage` | Coverage names by product. |
| Silver | `dim_date` | Calendar and period logic. |
| Silver | `fact_premium` | Premium, policy written, and in-force facts. |
| Silver | `fact_claim` | Claim, loss, severity, and fraud facts. |
| Gold | `gold_premium_summary` | Aggregated premium reporting. |
| Gold | `gold_loss_ratio` | Loss ratio reporting. |
| Gold | `gold_agent_scorecard` | Agent performance reporting. |

## Measures on Direct Lake tables

| Measure | Table grain to validate |
| --- | --- |
| Written Premium | `fact_premium` by policy, date, product, region, channel, agent |
| Earned Premium | `fact_premium` by policy and date |
| Policies In Force | `fact_premium` by policy and date |
| Incurred Losses | `fact_claim` by claim and coverage |
| Paid Losses | `fact_claim` by claim and coverage |
| Claim Count | `fact_claim` by claim |
| Loss Ratio | Incurred Losses divided by Earned Premium |

## Tableau live connection comparison

| Tableau live idea | Direct Lake distinction |
| --- | --- |
| Query the source at interaction time | Direct Lake reads OneLake Delta and loads data into memory on demand. |
| Source performance controls the report | Capacity, model design, and Delta layout all matter. |
| No extract refresh | Also no scheduled import refresh for Direct Lake tables. |
| Workbook owns calculations | Measures should live in the shared semantic model. |

## Design checklist

- Keep Gold tables report-friendly.
- Use a star schema with clear relationships.
- Avoid duplicating the same measure in multiple reports.
- Validate Direct Lake behavior before executive demos.
- Monitor capacity during concurrent use.
- Certify the semantic model only after tie-out.

## Related workshop files

- Tableau translation: tableau-to-powerbi.md
- Copilot authoring: copilot-in-power-bi.md
- Governance: ../governance/workspace-governance.md
- Source list: sources.md
