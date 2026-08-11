# Workspace governance for I&O analytics

Governance keeps the workshop pattern usable in production. The goal is simple:
separate environments, assign least-privilege roles, publish reusable content,
and agree names before five groups invent five conventions.

Everything here works with Power BI Desktop, the Power BI Service, and the
on-premises data gateway. Nothing on this page requires Fabric capacity, a
Lakehouse, or a pipeline layer.

## Environment layout

| Environment | Workspace | Purpose | Who gets write access |
| --- | --- | --- | --- |
| Development | `IO-Analytics-Dev` | Build and change semantic models and reports. | Domain builders and the CoE. |
| Test | `IO-Analytics-Test` | Validate numbers, security, and performance before release. | Builders plus the domain owner. |
| Production | `IO-Analytics-Prod` | Serve certified content to I&O and its stakeholders. | A small number of admins and release owners. |

Promote content with **deployment pipelines**, not by republishing a `.pbix` from
a laptop. A pipeline gives you a repeatable Dev to Test to Prod movement and a
record of what moved.

**Nobody publishes to My workspace.** Content in My workspace has no owner, no
backup path, and disappears when the person leaves.

## Workspace roles

| Role | Practical meaning | Rule for I&O |
| --- | --- | --- |
| Admin | Full workspace management, access control, item control. | Platform owners and one backup, no more. |
| Member | Publish, manage content, and share broadly. | Domain owners, not every report author. |
| Contributor | Create and edit workspace content. | The default for builders in Dev. |
| Viewer | View content. | Most consumers in Test and Prod. |

**Build permission is separate.** Viewer access to a workspace does not let
someone create a new report from a semantic model. Grant Build deliberately, and
grant it on the certified model so authors have an obvious right answer.

## Naming standards

| Item type | Pattern | Example |
| --- | --- | --- |
| Workspace | `IO-Analytics-{Environment}` | `IO-Analytics-Prod` |
| Semantic model | `sm_io_{domain}` | `sm_io_itsm`, `sm_io_capacity` |
| Report | `rpt_io_{domain}_{subject}` | `rpt_io_itsm_sla`, `rpt_io_assets_lifecycle` |
| App | `app_io_{domain}` | `app_io_itsm` |
| Dimension table | `dim_{entity}` | `dim_service` |
| Fact table | `fact_{event}` | `fact_incident` |
| Key column | `{entity}_key`, integer, hidden | `service_key` |
| Measure | Business language, Title Case | `Total Incidents`, `SLA Met %` |
| Measures table | `_Measures` | Sorts to the top of the field list |

Names should make lineage obvious. Keep personal names out of production content.

## Item ownership

Every production item needs a named business owner and a named technical owner
before it can be certified.

| Item | Business owner | Technical owner | Review cadence |
| --- | --- | --- | --- |
| `sm_io_itsm` | ITSM reporting owner | Semantic model owner | Monthly, and before certification |
| `sm_io_capacity` | Capacity planning owner | Semantic model owner | Monthly |
| `sm_io_mainframe` | Mainframe operations owner | Semantic model owner | Monthly |
| `sm_io_servicedesk` | Service desk manager | Semantic model owner | Monthly |
| `sm_io_assets` | Asset and CMDB owner | Semantic model owner | Monthly |
| `rpt_io_{domain}_{subject}` | The domain's reporting owner | Report author | Quarterly |
| Gateway data sources | I&O platform owner | Gateway admin | Quarterly |
| Shared theme and measure library | CoE lead | CoE lead | Quarterly |

Fill this table in with real names during the Day 3 roadmap session. An empty
owner column is the most common reason a migration stalls.

## Sensitivity labels

Apply Microsoft Purview sensitivity labels consistently across semantic models,
reports, and exports.

| Data class | Example I&O fields | Label guidance |
| --- | --- | --- |
| Public | Nothing in this estate | Not applicable |
| Internal | Aggregated incident trends, capacity utilization, MIPS totals | Internal analytics label |
| Confidential | CI names, site and datacenter detail, asset costs, team and staffing detail | Confidential |
| Restricted | Incident descriptions, security event detail, anything naming a person | Restricted, plus an access review |

Two rules specific to I&O:

- **Infrastructure detail is not low sensitivity.** A report that names every
  production CI, its criticality and its site is a map of the estate. Label and
  scope it accordingly.
- Labels inherit downstream from the semantic model to the report and to
  exported files, so label the model first.

The workshop data is synthetic. Production governance should assume real I&O data
is at least Confidential.

## Row-level security

Define RLS in the semantic model with a DAX filter, assign members to roles in
the Service, and test both.

| Pattern | Filter | Use when |
| --- | --- | --- |
| By region | `dim_location[region] = USERPRINCIPALNAME()` lookup | Regional operations leads see their own sites |
| By business unit | `dim_service[business_unit]` lookup | Service owners see their own services |
| By team | `dim_team[team_name]` lookup | Team leads see their own queue |

Test RLS with **Model view -> View as** in Desktop, and again with a real test
user in the Service. Desktop testing does not cover the Service role membership,
which is where the mistakes usually are.

Keep relationships single-direction. Bidirectional cross filtering can propagate
around an RLS filter in ways that are difficult to reason about and to test.

## Tenant settings to confirm

Confirm these with the platform team before publishing anything to Prod. Answer
each as a question, not as a default.

| Setting area | Governance question |
| --- | --- |
| Export data | Who can export summarized data, and underlying data? |
| Publish to web | Disabled, except for an explicitly approved group? |
| External sharing | Can I&O content be shared outside the tenant? |
| Sensitivity labels | Are labels required on new content, and enforced on export? |
| Certified content | Which group is allowed to certify? |
| Service principals | Which service principals can call Power BI APIs? |
| XMLA endpoint | Which groups can read or write semantic models through XMLA? |
| Gateway administration | Who administers the gateway cluster and its data sources? |
| Workspace creation | Who can create a workspace? Uncontrolled creation is how sprawl starts. |

## Refresh and gateway operations

| Item | Practice |
| --- | --- |
| Refresh schedule | Set it to the business need, not to the maximum allowed. Every refresh is load on the source. |
| Refresh window | Stagger models so five domains do not hit the gateway at the same minute. |
| Failure alerts | Send refresh failure notifications to a monitored group mailbox, never to one person. |
| Credentials | Stored on the gateway data source, owned by the platform team, not by an individual. |
| Incremental refresh | Use it on large fact tables, and verify the query folds first. |
| Gateway capacity | Watch it. A single overloaded gateway node degrades every model behind it. |

Detail in [gateway-setup.md](../reference/gateway-setup.md).

## Dev to Test to Prod checklist

| Gate | Required evidence |
| --- | --- |
| Dev complete | Model builds, refresh succeeds, report renders, naming standards met. |
| Test data | Totals reconcile against the Tableau report being replaced, at the agreed grain. |
| Test security | RLS validated with a real test user in the Service, not only in Desktop. |
| Test performance | Key pages render within the agreed target with the gateway in the path. |
| Labels | Sensitivity label applied to the model and to every report. |
| Ownership | Business and technical owner named and recorded. |
| Prod release | Owner approves, release note published, support path documented. |
| Post-release | Usage and refresh history reviewed after the first two weeks. |

## Avoiding sprawl

The failure mode for this migration is one semantic model per report, which is
extract sprawl with a new name.

- One certified semantic model per domain. Reports are thin and build on it.
- A new model requires a stated reason, recorded in the assessment worksheet.
- Changes to a certified measure go through the model owner as a request, not as
  a fork.
- Retire the Tableau workbook once the Power BI replacement is validated.
  Parallel running forever is how you end up maintaining both.

## Related

- [Endorsement and certification](endorsement-certification.md)
- [Migration assessment worksheet](migration-assessment-worksheet.md)
- [Adoption roadmap](adoption-roadmap.md)
- [Current state and constraints](../reference/schwab-current-state.md)
- [Gateway setup](../reference/gateway-setup.md)
- [Sources](../reference/sources.md)
