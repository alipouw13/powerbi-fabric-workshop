# Day 3 reference apps gallery

Use these apps to show what teams can build once data, analytics, AI, and app
hosting are close together on Microsoft's platform. Keep demos high-level and
accurate. Do not imply features beyond what the repo or owner can show.

## Presenter framing

The workshop starts with Tableau to Power BI migration and governed Fabric data.
Day 3 can widen the aperture:

- Internal Fabric operations apps.
- Complete Fabric analytics estates.
- Applied AI apps.
- Fabric-native apps built with Rayfin.

## Gallery

| App | Repo or asset | What to show | Why it fits |
| --- | --- | --- | --- |
| Report Optimizer | `capacity-optimizer` | A Rayfin app for Microsoft Fabric and Power BI capacity optimization. | Shows an internal Fabric ops app built on Rayfin. |
| Contoso Insurance end-to-end Fabric demo | https://github.com/alipouw13/fabric-test | The finished target state for this workshop's insurance data. | Shows the medallion Lakehouse, Warehouse, notebooks, real-time analytics, Direct Lake model, report, and CI/CD pattern. |
| Language app | https://github.com/alipouw13/language-app | A voice and text translation app using Azure Language services. | Shows an applied AI app pattern. |
| AI Fitness Coach | https://github.com/alipouw13/ai-fitness-coach | An AI coaching app. | Shows another applied AI example beyond BI reporting. |

## Report Optimizer

Report Optimizer, also referred to by the `capacity-optimizer` repo or project
name, is a Rayfin app for Fabric and Power BI capacity optimization.

Use it to talk about:

- Capacity samples.
- Reports.
- Refresh runs.
- Duplicate models.
- Inactive reports.
- Adoption.
- Alerts.

The most important teaching point is that a BI platform often needs operational
apps around it. Rayfin is a credible pattern for building those apps close to
Fabric governance.

## Contoso Insurance Fabric demo

Repo: https://github.com/alipouw13/fabric-test

Show this as the finished target state for the workshop:

- Lakehouse `lh_insurance`.
- Warehouse `wh_insurance`.
- Medallion processing.
- Notebooks.
- Real-time telematics with Eventstream, Eventhouse, and KQL.
- Direct Lake semantic model `sm_insurance`.
- Executive report `rpt_insurance_executive`.
- Fabric CI/CD.

Position it carefully: the workshop dataset and docs align to this demo, but the
workshop does not need to recreate every asset in three days.

## Language app

Repo: https://github.com/alipouw13/language-app

Use this as a compact AI app example. The accurate high-level description is:

- Voice and text translation.
- Azure Language services.
- A practical user-facing AI workflow.

The teaching point is not translation itself. The teaching point is that teams
can build AI apps on the same broader Microsoft data and AI platform where
Fabric analytics lives.

## AI Fitness Coach

Repo: https://github.com/alipouw13/ai-fitness-coach

Use this as a second applied AI example. Keep the description high-level:

- AI coaching app.
- User-facing application pattern.
- Example of moving beyond dashboards into interactive assistance.

Do not invent model details, data stores, or product claims during the demo.

## Suggested Day 3 flow

| Segment | Demo | Point |
| --- | --- | --- |
| 1 | Contoso Insurance Fabric demo | "This is the full analytics target state." |
| 2 | Report Optimizer | "Fabric platforms need internal ops apps." |
| 3 | Rayfin Claims Intake skeleton | "Apps can be built on Fabric with governed auth and data." |
| 4 | Language app | "AI apps can sit beside analytics investments." |
| 5 | AI Fitness Coach | "The same platform supports multiple app patterns." |

## Connect back to the workshop

| Workshop lesson | Reference app connection |
| --- | --- |
| Semantic model reuse | Report Optimizer and Contoso Insurance both rely on shared data understanding. |
| Direct Lake and Fabric data | Contoso Insurance shows the Fabric target state. |
| Governance | Report Optimizer reinforces capacity and adoption management. |
| Rayfin app layer | Claims Intake and Report Optimizer show app patterns. |
| AI readiness | Language app and AI Fitness Coach show why clean data platforms matter. |

## Related workshop files

- Rayfin reference: rayfin.md
- Rayfin app skeleton: ../rayfin-app/README.md
- Rayfin lab: ../labs/lab-11-rayfin-insurance-app/README.md
- Direct Lake reference: direct-lake.md
- Governance roadmap: ../governance/adoption-roadmap.md
- Source list: sources.md
