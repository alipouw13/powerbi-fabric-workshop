# I&O current state, constraints, and what that means for this workshop

What the customer team told us in the pre-workshop agenda review. Every lab is
written against these facts. Cover this in the Day 1 kickoff so attendees know
what is feasible **today** versus what is on the roadmap.

> Treat this as a living document. Confirm each row the week of the workshop,
> because tenant settings and approvals change.

## Audience

| Item | What we know |
| --- | --- |
| Group | An enterprise **Infrastructure & Operations (I&O)** group |
| Size | 15-18 attendees |
| Locations | Two primary sites, some joining virtually |
| Background | Cross-functional, not a centralized reporting team. Most have **Tableau** experience. |
| Power BI experience | Assume none |
| Goal | **Retire Tableau in I&O** and form a **Community of Practice** for data visualization |

Implication: draw an explicit Tableau corollary in every teaching block. Do not
assume a shared toolchain, naming standard, or release process.

## The five I&O domains

Five breakout groups, five fact tables, one shared set of conformed dimensions.

| Group | Domain | Fact table | The flagship report answers |
| --- | --- | --- | --- |
| 1 | ITSM & Operational Reporting | `fact_incident` | Incident, change and problem trends with SLA attainment and MTTR |
| 2 | Capacity & Forecasting | `fact_capacity` | Utilization, demand and headroom with a simple forecast view |
| 3 | Mainframe Analytics | `fact_mainframe` | MIPS consumption, batch windows and throughput over time |
| 4 | Service Desk & Workforce | `fact_service_desk` | Ticket volumes, first-contact resolution and staffing coverage |
| 5 | Asset & Workplace Services | `fact_asset` | Inventory, configuration coverage and lifecycle status from the CMDB |

## Tooling and feature access

### In scope

| Capability | Status | Where it appears |
| --- | --- | --- |
| Power BI Desktop | Available | Every lab |
| Power Query | Available. **The only transformation layer.** | [Lab 0](../labs/lab-00-connect-and-shape/README.md) |
| DAX | Available | [Lab 3](../labs/lab-03-dax-measures/README.md) |
| **Import** storage mode | Available, and the default choice | [Lab 1](../labs/lab-01-semantic-model/README.md) |
| **DirectQuery** storage mode | Available, discouraged | Covered as a decision, not a default |
| On-premises data gateway | Available, centrally managed | [Day 1 setup](../labs/day-1-setup/README.md), [gateway-setup.md](gateway-setup.md) |
| Power BI Service workspaces | Available | [Lab 1](../labs/lab-01-semantic-model/README.md) onward |
| Row-level security | Available | Governance sessions |
| Endorsement (promoted, certified) | Available | [endorsement-certification.md](../governance/endorsement-certification.md) |
| Microsoft Purview sensitivity labels | Available | [workspace-governance.md](../governance/workspace-governance.md) |
| Deployment pipelines | Available | [workspace-governance.md](../governance/workspace-governance.md) |
| **M365 Copilot** | Available to some attendees | External drafting assistant only, copy and paste into Power BI. Pair licensed with unlicensed attendees. [copilot-in-power-bi.md](copilot-in-power-bi.md) |

### Not available

Do not demo any of these. A demo of something the team cannot use reads as a
sales pitch, not enablement.

| Capability | Status |
| --- | --- |
| Copilot **embedded in Power BI** Desktop or Service | Not available |
| Copilot Studio | Not available |
| Fabric Data Agent | Not available |
| Lakehouse, OneLake, Direct Lake | Not available |
| Medallion layering (bronze, silver, gold) | Not applicable, there is no lake layer |
| Dataflows Gen2, Data Factory pipelines, notebooks | Not available |
| Fabric capacity | Not provisioned |
| MCP servers | Not available |
| GitHub Copilot, PBIP source control, CI/CD for BI content | Not part of current practice |

Anything on this list is **future and approval-dependent**. It belongs in the Day
3 roadmap conversation, not in a lab. See
[sessions/day-3-showcase.md](../sessions/day-3-showcase.md).

**The practical consequence:** every transformation in this workshop happens by
hand in **Power Query**, and every calculation is written in **DAX**. There is no
lake layer to push work into and no AI inside Power BI to generate it. The only
AI assist is M365 Copilot in a separate window, used as a drafting tool with a
copy-and-paste handoff.

## Data architecture today

- The architecture is **very flat**. No layered refinement, no normalized
  dimensional structure in place.
- **Large Excel files** are a common source and a common pain point. Monthly
  extracts arrive as a folder of files with inconsistent column names.
- Most reports connect **directly to SQL databases** through a semantic model in
  **Import** mode.
- The **on-premises data gateway** brokers those connections. It is centrally
  managed, so assume attendees cannot create or repoint a gateway data source
  themselves. Detail in [gateway-setup.md](gateway-setup.md).
- There is **no lake layer**, so **all transformation happens in Power Query**.
- A move to a **snowflake** pattern is planned but not implemented. Covered
  honestly in [star-schema.md](star-schema.md), including why the Power BI engine
  prefers a star.

Implication: the workshop must be useful to someone who goes back to a
gateway-brokered Import model on Monday. Power Query skill and star-schema
modeling are the highest-leverage things we can teach.

## Import versus DirectQuery

The only two storage modes available, and the decision is per model.

| | Import | DirectQuery |
| --- | --- | --- |
| Where data lives | Cached in the model | Stays in the source |
| Query speed | Fast | Depends entirely on the source and the gateway |
| Data freshness | As of the last refresh | Live |
| Refresh needed | Yes, scheduled | No |
| Power Query transformations | Full library available | Only steps that fold back to the source |
| DAX available | All functions | A restricted subset |
| Model size limit | Applies | Not applicable |
| Load on the source system | Only at refresh | Every visual interaction |
| Best for | Almost everything in this environment today | Sources too large to cache, or where caching is not permitted |

**Default to Import.** Choose DirectQuery only when you can name the specific
requirement that rules Import out, and only after testing page performance with
the gateway in the path.

## Development practice constraints

- Gateway connections are centrally managed. Plan Day 1 setup accordingly.
- Tenant and workspace features are enabled selectively. Confirm before the
  workshop, and stay inside the **In scope** list.
- There is no shared source-control or CI/CD practice for Power BI content, and
  PBIP is not in use. Standards, naming, and review discipline are the substitute,
  and the Community of Practice sets them.
- Report development is decentralized. Naming, certification, and workspace
  standards are part of what the Community of Practice needs to define.
- No AI tool may receive real customer data, credentials, or ticket contents. M365
  Copilot is used for **schema, code and prose only**, never source records.

## Naming conventions

| Object | Pattern | Example |
| --- | --- | --- |
| Semantic model | `sm_io_<domain>` | `sm_io_itsm`, `sm_io_capacity` |
| Report | `rpt_io_<domain>_<subject>` | `rpt_io_itsm_sla` |
| Dimension table | `dim_<entity>` | `dim_service` |
| Fact table | `fact_<event>` | `fact_incident` |
| Key column | `<entity>_key`, integer, hidden | `service_key` |
| Measure | Business language, Title Case | `Total Incidents`, `SLA Met %` |
| Workspace | `IO-Analytics-<Environment>` | `IO-Analytics-Prod` |

## Facilitator labeling convention

Two badges, so attendees always know what applies to them:

- **In scope.** Attendees do this hands-on with the tools they have today.
- **Future, approval-dependent.** Reference reading about a capability the organization does
  not have. Not run, not demoed, not a prerequisite for anything.

If a question comes up about a future capability, answer it briefly and route the
request to the Day 3 roadmap. Do not detour into a live demo.

## Related

- [Star schema](star-schema.md)
- [Visual design](visual-design.md)
- [Tableau to Power BI](tableau-to-powerbi.md)
- [Migration approaches](migration-approaches.md)
- [M365 Copilot for Power BI work](copilot-in-power-bi.md)
- [Gateway setup](gateway-setup.md)
- [Workspace governance](../governance/workspace-governance.md)
- [Adoption roadmap](../governance/adoption-roadmap.md)
