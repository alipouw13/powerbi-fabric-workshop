# Workspace governance for Schwab Analytics

Workspace governance keeps the workshop pattern production-ready. The goal is
simple: separate environments, assign least-privilege roles, publish reusable
content, and monitor capacity before users feel pain.

## Environment layout

| Environment | Workspace | Purpose | Who gets write access |
| --- | --- | --- | --- |
| Development | `Schwab-Analytics-Dev` | Build Lakehouse, Warehouse, semantic model, reports, and Rayfin app changes. | Delivery squad and approved developers. |
| Test | `Schwab-Analytics-Test` | Validate data, security, performance, and deployment steps. | Delivery squad plus test leads. |
| Production | `Schwab-Analytics-Prod` | Serve certified content to business users. | Few admins, release owners, and controlled service principals. |

Use deployment pipelines or source-controlled deployment automation to promote
content instead of manual recreation.

## Workspace role guidance

| Role | Practical meaning | Workshop rule |
| --- | --- | --- |
| Admin | Full workspace management, access control, and item control. | Limit to platform owners and backup admins. |
| Member | Can publish, manage content, and collaborate broadly. | Use for trusted delivery leads, not every report author. |
| Contributor | Can create and edit workspace content. | Use in Dev for builders who do not manage access. |
| Viewer | Can view content. | Use for most consumers in Test and Prod. |

For semantic model reuse, grant Build permission deliberately. Viewer access to
a workspace is not the same as permission to build new reports from a model.

## Naming standards

| Item type | Pattern | Example |
| --- | --- | --- |
| Workspace | `Schwab-Analytics-{Environment}` | `Schwab-Analytics-Prod` |
| Lakehouse | `lh_{domain}` | `lh_insurance` |
| Warehouse | `wh_{domain}` | `wh_insurance` |
| Semantic model | `sm_{domain}` | `sm_insurance` |
| Report | `rpt_{domain}_{audience}` | `rpt_insurance_executive` |
| Data pipeline | `pl_{domain}_{purpose}` | `pl_insurance_gold_refresh` |
| Notebook | `nb_{domain}_{layer}_{purpose}` | `nb_insurance_silver_transform` |
| Rayfin app | `app_{domain}_{workflow}` | `app_insurance_claims_intake` |

Names should make lineage obvious. Avoid personal names in production content.

## Item ownership

| Item | Business owner | Technical owner | Review cadence |
| --- | --- | --- | --- |
| `lh_insurance` | Analytics product owner | Data engineering lead | Monthly |
| `wh_insurance` | Analytics product owner | Data engineering lead | Monthly |
| `sm_insurance` | Insurance analytics owner | Semantic model owner | Monthly and before certification |
| `rpt_insurance_executive` | Executive reporting owner | BI lead | Quarterly |
| Rayfin Claims Intake | Claims operations owner | App engineering lead | Monthly |

Every production item needs an accountable owner before certification.

## Sensitivity labels

Use Microsoft Purview sensitivity labels consistently across reports, semantic
models, and exported content.

| Data class | Example workshop fields | Label guidance |
| --- | --- | --- |
| Public | Product names and synthetic region labels | Public or internal policy default. |
| Internal | Aggregated premium and claim trends | Internal analytics label. |
| Confidential | Customer, policy, claim, agent, and reserve details | Confidential or regulated data label. |
| Restricted | Real PII, claims notes, payment data | Restricted label and additional access review. |

The workshop data is synthetic. Production governance should assume real
insurance data is regulated and label accordingly.

## Key tenant settings to review

| Setting area | Governance question |
| --- | --- |
| Copilot | Which security groups can use Copilot in Fabric and Power BI? |
| Export data | Who can export summarized or underlying data? |
| Publish to web | Is public publishing disabled except for approved groups? |
| Service principals | Which service principals can use Fabric APIs? |
| XMLA endpoint | Which groups can read or write semantic models through XMLA? |
| External sharing | Can content be shared outside the tenant? |
| Certified content | Who can certify Power BI and Fabric items? |
| Sensitivity labels | Are required labels enforced for production content? |

Review tenant settings before moving migrated reports to production.

## Capacity monitoring

Use the Microsoft Fabric Capacity Metrics app to watch:

- Capacity utilization.
- CU consumption by item.
- Throttling and overage indicators.
- Refresh and query patterns.
- Long-running reports.
- Noisy development workloads.

For the workshop, the Report Optimizer reference app in
../reference/reference-apps.md provides a Day 3 example of building additional
ops tooling around Fabric capacity data.

## Dev to Test to Prod checklist

| Gate | Required evidence |
| --- | --- |
| Dev complete | Model builds, report renders, and source control diff is reviewed. |
| Test data | Written Premium, Earned Premium, Incurred Losses, and Claim Count tie out. |
| Test security | RLS and workspace permissions are validated with test users. |
| Test performance | Key pages meet target load expectations. |
| Prod release | Owner approves release notes and support path. |
| Post-release | Usage, refresh, query, and capacity metrics are reviewed. |

## Related workshop files

- Endorsement: endorsement-certification.md
- Adoption roadmap: adoption-roadmap.md
- Direct Lake reference: ../reference/direct-lake.md
- Source list: ../reference/sources.md
