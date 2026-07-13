# Adoption roadmap

This roadmap turns the 3-day workshop into a repeatable Tableau to Power BI and Fabric adoption program.
It assumes Schwab wants governed self-service, shared semantic models, and a practical migration path.

Related docs:

- [Workspace governance](workspace-governance.md)
- [Endorsement and certification](endorsement-certification.md)
- [Migration assessment worksheet](migration-assessment-worksheet.md)
- [Migration approaches](../reference/migration-approaches.md)

## Adoption phases

| Phase | Goal | Typical activities | Exit criteria |
| --- | --- | --- | --- |
| Crawl | Establish foundations | Inventory Tableau content, define workspaces, train first authors, build POC | First validated model and report in Test. |
| Walk | Scale governed reuse | Create certified models, migrate priority reports, build champions network | Report authors reuse shared semantic models. |
| Run | Operate as a product | Monitor usage, optimize capacity, automate deployment, mature CoE | Certified models cover major analytical domains. |

## Center of Excellence model

| Role | Responsibility |
| --- | --- |
| Executive sponsor | Sets priority, removes blockers, and reinforces the migration outcome. |
| Power BI CoE lead | Owns standards, enablement, backlog, and adoption metrics. |
| Fabric platform owner | Owns capacity, tenant settings, workspace policy, and monitoring. |
| Data engineering lead | Owns Lakehouse, Bronze/Silver/Gold patterns, and data quality. |
| Semantic model owner | Owns measures, relationships, RLS, model descriptions, and certification readiness. |
| Business product owner | Owns requirements, acceptance criteria, and user communications. |
| Champions | Help teams migrate, answer peer questions, and surface friction. |
| Support lead | Owns intake, triage, known issues, and service expectations. |

## Champions network

Champions should be close to the work.
Pick Tableau power users, analysts, and report consumers who can translate business questions.

Champion responsibilities:

- Attend migration office hours.
- Test migrated reports before broad release.
- Collect user feedback.
- Identify duplicate workbooks.
- Encourage use of certified semantic models.
- Share successful report patterns.
- Escalate missing data or metric definitions.

## Enablement plan

| Audience | Enablement | Outcome |
| --- | --- | --- |
| Tableau authors | Tableau to Power BI concept mapping, DAX basics, report design | Authors can rebuild reports without cloning old workbook patterns. |
| BI model owners | Star schema, Direct Lake, measure governance, certification | Owners can create trusted shared semantic models. |
| Data engineers | Fabric Lakehouse, medallion tables, Dataflow Gen2, notebooks | Engineers can land and curate analytics-ready data. |
| Business consumers | Report navigation, slicers, subscriptions, export policy | Consumers trust and use the new reports. |
| Admins | Workspace roles, tenant settings, capacity metrics, deployment pipelines | Admins can operate safely at scale. |

## Success metrics

| Metric | Definition | Target direction |
| --- | --- | --- |
| Certified models | Count of certified semantic models with owners and descriptions | Increase |
| Report consolidation ratio | Tableau workbooks retired per new Power BI report or model | Increase |
| Active users | Monthly active viewers and authors in approved workspaces | Increase |
| Capacity health | Throttling, queued operations, and sustained high CU periods | Improve |
| Model reuse | Reports connected to shared semantic models | Increase |
| Duplicate model count | Models with overlapping metric definitions | Decrease |
| Validation defects | Number of metric tie-out issues found after release | Decrease |
| Adoption satisfaction | Survey or office-hour sentiment | Improve |

## 30/60/90 day plan

| Timeframe | Owner | Actions | Deliverables |
| --- | --- | --- | --- |
| First 30 days | CoE lead and platform owner | Stand up workspaces, confirm tenant settings, inventory top Tableau assets, run housing POC | Dev/Test/Prod workspaces, initial inventory, validated POC report |
| First 30 days | BI model owner | Build `Housing-Market-Insights`, document core measures, test Direct Lake | Shared model with measure descriptions |
| First 30 days | Business product owner | Pick first migration wave and define acceptance criteria | Wave 1 backlog and sign-off checklist |
| Days 31-60 | Data engineering lead | Stabilize Bronze/Silver/Gold pattern and data quality checks | Repeatable Fabric data pipeline pattern |
| Days 31-60 | BI model owner | Prepare first model for promotion or certification | Endorsement request and validation evidence |
| Days 31-60 | Champions | Run UAT sessions and collect feedback | UAT findings and adoption FAQ |
| Days 61-90 | CoE lead | Publish standards, train authors, and launch office hours | Standards pack and enablement calendar |
| Days 61-90 | Platform owner | Monitor capacity and workspace access | Capacity review and access review |
| Days 61-90 | Business owners | Retire or freeze replaced Tableau workbooks | Retirement list and communication plan |

## Operating cadence

| Cadence | Meeting | Purpose |
| --- | --- | --- |
| Weekly | Migration wave standup | Track blockers, validation, and cutover status. |
| Weekly | Office hours | Help authors and champions with Power BI and Fabric questions. |
| Biweekly | Governance review | Review endorsement, access, labels, and exceptions. |
| Monthly | Capacity and adoption review | Review Fabric metrics, usage, certified models, and active users. |
| Quarterly | Roadmap planning | Prioritize domains, retire legacy content, and update standards. |

## Adoption risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Authors recreate workbook sprawl | Certify shared models and train authors to connect to them. |
| Users distrust numbers | Require tie-out evidence before cutover and publish metric definitions. |
| Capacity issues hurt confidence | Monitor with the Fabric Capacity Metrics app and schedule heavy workloads. |
| Ownership is unclear | Require owner and backup owner before endorsement. |
| Copilot gives weak output | Improve model names, descriptions, relationships, and AI metadata. |
| Migration feels like tool replacement only | Anchor every wave to a business decision and retirement plan. |
