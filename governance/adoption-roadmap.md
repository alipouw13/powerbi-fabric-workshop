# Adoption roadmap

The migration succeeds only if users trust the new reports and builders reuse
the governed model. This roadmap turns the workshop into a 30, 60, and 90 day
operating plan.

## Adoption stages

| Stage | Goal | What good looks like |
| --- | --- | --- |
| Crawl | Establish a governed pilot. | One validated semantic model, one executive report, named owners. |
| Walk | Expand reuse and migration throughput. | Multiple Tableau workbooks mapped to shared models and deployment gates. |
| Run | Operate as a Fabric analytics product. | Certified models, active champions, capacity monitoring, and regular releases. |

## Operating model

| Group | Responsibilities |
| --- | --- |
| Executive sponsor | Sets priority, removes blockers, and reinforces migration outcomes. |
| Center of Excellence | Defines standards, certification criteria, enablement, and reusable patterns. |
| Fabric platform team | Manages capacity, tenant settings, workspace policy, gateways, and monitoring. |
| Data engineering team | Owns Lakehouse, Warehouse, pipelines, and data quality. |
| Semantic model owners | Own model design, DAX measures, descriptions, RLS, and certification evidence. |
| Report authors | Build thin reports, test usability, and submit model enhancement requests. |
| Champions | Help teams adopt Power BI practices and collect feedback. |

## Enablement plan

| Audience | Enablement | Format |
| --- | --- | --- |
| Executives | What changed, where to find certified reports, how to subscribe. | 30 minute briefing. |
| Analysts | Tableau to Power BI translation, DAX basics, model reuse. | Hands-on workshop. |
| Report authors | Thin reports, field parameters, Copilot authoring, validation. | Lab plus office hours. |
| Model owners | Star schema, measure definitions, RLS, endorsement. | Working session. |
| Platform admins | Workspaces, capacity, labels, tenant settings, deployment. | Governance review. |

## Success metrics

| Metric | Definition | Target direction |
| --- | --- | --- |
| Certified models | Count of certified semantic models with named owners. | Increase. |
| Report consolidation ratio | Retired Tableau workbooks or duplicate Power BI reports divided by migrated reports. | Increase. |
| Active users | Monthly active viewers of certified reports. | Increase. |
| Build permission coverage | Authors using governed models rather than private datasets. | Increase. |
| Capacity health | Throttling, high CU items, and refresh contention. | Improve. |
| Validation pass rate | Migrated reports that pass tie-out on first or second review. | Increase. |
| Support tickets | Repeated data definition questions or broken refreshes. | Decrease. |
| Champion participation | Active champions attending office hours or community sessions. | Increase. |

## 30 day plan

| Workstream | Owner | Deliverable |
| --- | --- | --- |
| Migration backlog | BI lead | Completed assessment worksheet for top Tableau workbooks. |
| Pilot model | Semantic model owner | `sm_insurance` reviewed with core measures and descriptions. |
| Executive report | Report author | `rpt_insurance_executive` rebuilt and ready for validation. |
| Governance | CoE lead | Workspace roles, naming, labels, and endorsement criteria approved. |
| Platform | Fabric admin | Capacity Metrics app installed and reviewed weekly. |
| Enablement | Champions lead | Tableau to Power BI translation session delivered. |

## 60 day plan

| Workstream | Owner | Deliverable |
| --- | --- | --- |
| Migration wave 1 | BI lead | First P1 workbooks migrated or retired. |
| Certification | Approved certifier | `sm_insurance` certified if criteria are met. |
| Deployment | Release owner | Dev to Test to Prod process documented and used. |
| RLS | Security owner | Region or book-of-business RLS tested with business users. |
| Copilot | CoE lead | Copilot authoring guidance and prompt examples published. |
| Office hours | Champions lead | Weekly support channel with captured FAQs. |

## 90 day plan

| Workstream | Owner | Deliverable |
| --- | --- | --- |
| Migration wave 2 | BI lead | Additional high-value workbooks moved to shared models. |
| Consolidation | Analytics product owner | Duplicate models and reports retired or merged. |
| Capacity operations | Fabric platform team | Monthly capacity health review with action log. |
| Data products | Data engineering lead | Gold table contracts documented for insurance analytics. |
| Rayfin exploration | App engineering lead | Claims Intake or ops app path evaluated for production fit. |
| Community | Champions lead | Internal showcase featuring model reuse and app examples. |

## Champion network

| Champion type | Focus |
| --- | --- |
| Business champion | Validates definitions and encourages report adoption. |
| Analyst champion | Helps translate Tableau patterns to Power BI patterns. |
| Technical champion | Supports DAX, semantic model, and PBIP questions. |
| Governance champion | Reinforces certification, labels, and workspace practices. |

## Communication rhythm

| Cadence | Meeting | Purpose |
| --- | --- | --- |
| Weekly | Migration standup | Backlog, blockers, validation, and cutover status. |
| Weekly | Office hours | Help authors and collect recurring issues. |
| Biweekly | CoE review | Standards, certification candidates, and pattern updates. |
| Monthly | Capacity review | Capacity health, adoption, and optimization actions. |
| Quarterly | Executive readout | Migration progress, value delivered, and next priorities. |

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Users distrust numbers | Run parallel validation and publish tie-out evidence. |
| Authors create private models | Certify shared models and require assessment mapping. |
| Capacity issues appear during rollout | Monitor with Capacity Metrics app and tune high-use reports. |
| Tableau logic is undocumented | Inventory calculations and validate with business owners. |
| Copilot gives weak results | Improve model names, descriptions, and star schema quality. |
| Governance slows delivery | Use clear gates and lightweight templates. |

## Related workshop files

- Workspace governance: workspace-governance.md
- Certification: endorsement-certification.md
- Migration worksheet: migration-assessment-worksheet.md
- Reference apps: ../reference/reference-apps.md
- Source list: ../reference/sources.md
