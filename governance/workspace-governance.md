# Workspace governance

This page defines how Schwab workshop content should be organized, secured, and promoted across Fabric workspaces.
It applies to reports, semantic models, lakehouses, notebooks, dataflows, and deployment pipelines created for the workshop.

Microsoft references:

- [Roles in workspaces in Microsoft Fabric](https://learn.microsoft.com/en-us/fabric/fundamentals/roles-workspaces)
- [About tenant settings](https://learn.microsoft.com/en-us/fabric/admin/about-tenant-settings)
- [Overview of Fabric deployment pipelines](https://learn.microsoft.com/en-us/fabric/cicd/deployment-pipelines/intro-to-deployment-pipelines)
- [Microsoft Fabric Capacity Metrics app](https://learn.microsoft.com/en-us/fabric/enterprise/metrics-app)

## Workspace layout

| Environment | Workspace | Purpose |
| --- | --- | --- |
| Dev | `Schwab-Analytics-Dev` | Build, experiment, test notebooks, create models, and author reports. |
| Test | `Schwab-Analytics-Test` | Validate promoted content with controlled users and test data checks. |
| Prod | `Schwab-Analytics-Prod` | Host approved, supported content for business users. |

Do not publish workshop production content directly from Desktop to Prod.
Use Dev first, validate in Test, then promote to Prod.

## Workspace role model

| Role | Can do | Workshop assignment guidance |
| --- | --- | --- |
| Admin | Manage workspace settings, access, items, and app publishing | Limited to platform owners and workshop admins. |
| Member | Publish, update, share, and manage content | Use for lead BI engineers and model owners. |
| Contributor | Create and edit content in the workspace | Use for report authors in Dev. Avoid in Prod unless operationally required. |
| Viewer | View content and interact with reports | Use for consumers and UAT participants. |

Least privilege is the default.
Grant users the role they need for the current environment, not the highest role they might need later.

## Naming standards

| Item type | Standard | Example |
| --- | --- | --- |
| Workspace | `Schwab-Analytics-<Env>` | `Schwab-Analytics-Dev` |
| Lakehouse | `lh_<domain>` | `lh_housing` |
| Bronze table | `bronze_<source_or_entity>` | `bronze_market_tracker` |
| Silver dimension | `dim_<entity>` | `dim_region` |
| Silver fact | `fact_<process>` | `fact_home_sales` |
| Gold table | `gold_<business_subject>` | `gold_market_summary` |
| Semantic model | Business name plus storage mode when helpful | `Housing-Market-Insights (Direct Lake)` |
| Report | Decision or audience name | `Housing Market Executive Overview` |
| Deployment pipeline | `<domain>-analytics-pipeline` | `housing-analytics-pipeline` |

## Sensitivity labels

Use sensitivity labels when content leaves a personal sandbox or contains business data.
Workshop synthetic data can be labeled as internal training content if required by tenant policy.
When replacing it with real Redfin or Schwab data, choose the approved enterprise label.

Reference:

- [Information protection in Fabric](https://learn.microsoft.com/en-us/fabric/governance/information-protection)
- [Enable sensitivity labels in Fabric and Power BI](https://learn.microsoft.com/en-us/fabric/enterprise/powerbi/service-security-enable-data-sensitivity-labels)

## Key tenant settings to review

| Setting area | Why it matters |
| --- | --- |
| Workspace creation | Controls who can create new workspaces and prevents unmanaged sprawl. |
| Publish to web | Should be restricted for enterprise data. |
| Export data | Controls data exfiltration paths from reports. |
| Build permission | Controls who can build new reports or query semantic models. |
| Copilot | Required for Copilot authoring labs when capacity and region requirements are met. |
| Service principal access | Needed only for approved automation scenarios. |
| Sensitivity labels | Enables Microsoft Purview labels in Fabric and Power BI. |
| Endorsement certification | Controls who can certify content. |

## Capacity monitoring

Use the Fabric Capacity Metrics app to monitor capacity health.
During the workshop, review capacity if users see slow report rendering, Direct Lake fallback concerns, or queued operations.

Track:

- CU usage by workload
- Interactive vs background operations
- Throttling indicators
- Copilot usage if enabled
- Peak periods during labs
- Long-running notebook or dataflow operations

## Ownership model

| Asset | Owner | Backup owner | Support expectation |
| --- | --- | --- | --- |
| `lh_housing` | Data engineering lead | Fabric platform lead | Data load and table health |
| Bronze and Silver tables | Data engineering lead | Workshop technical lead | Schema, transformations, and data quality |
| Gold tables | Analytics engineering lead | Model owner | Business-ready aggregates |
| `Housing-Market-Insights` semantic model | BI model owner | BI engineering lead | Measures, relationships, RLS, descriptions |
| Reports | Report owner | Business product owner | Visual design, usability, adoption |
| Deployment pipeline | Release owner | Platform lead | Promotion, approvals, rollback |
| Sensitivity labels | Compliance owner | Fabric admin | Label policy and enforcement |

## Operating rules

1. Dev is for iteration.
2. Test is for validation.
3. Prod is for supported content.
4. Certified models must have an owner and backup owner.
5. Reports should connect to shared semantic models where possible.
6. Do not create one semantic model per report unless there is a documented exception.
7. Use deployment pipelines for controlled promotion.
8. Review workspace access monthly during the migration program.
9. Remove inactive contributors after each migration wave.
10. Track exceptions in the adoption backlog.
