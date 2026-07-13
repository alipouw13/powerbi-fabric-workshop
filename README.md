# Schwab x Microsoft - Power BI & Fabric Workshop (3 days)

A hands-on, three-day workshop that helps a **Tableau** team learn **Power BI and
Microsoft Fabric** by rebuilding a familiar analysis end to end: a **property &
casualty (P&C) insurance** book, "Contoso Insurance". Every lab maps to the
on-site deck and runs on a small, fully **synthetic** dataset (no real Schwab
data) so you can follow along in your own Fabric tenant. The workshop also weaves
in **Rayfin**, a Backend-as-a-Service on Fabric, as a hands-on thread: everyone
installs it on Day 1 and builds a small insurance app on it on Day 3.

> **What this is:** a guided walk-through you run in your own Fabric tenant, built
> for people who know Tableau and are new to Power BI / Fabric.
> **What this isn't:** a connection to any real Schwab system. The sample data is
> generated locally and aligned to the Contoso Insurance Fabric demo
> ([alipouw13/fabric-test](https://github.com/alipouw13/fabric-test)).

## The story

```
Tableau workbooks + many .hyper extracts
   ->  Sources land once in OneLake (Bronze / Silver / Gold)
   ->  One shared semantic model (sm_insurance, Direct Lake, star schema)
   ->  Power BI reports + Copilot + Fabric Data Agent + GitHub Copilot & MCP
        + a Rayfin app on the same governed estate, all shipped via PBIP + CI/CD
```

See [reference/architecture.md](reference/architecture.md) for the target picture,
[reference/tableau-to-powerbi.md](reference/tableau-to-powerbi.md) for the
concept-by-concept translation from Tableau, and
[reference/rayfin.md](reference/rayfin.md) for the Rayfin thread.

## Who it's for and how it runs

- **Audience:** 10-30 people who use Tableau today. No Power BI experience assumed.
- **Format:** a conference room with short teaching blocks, then breakouts where
  small groups do the hands-on labs with a Microsoft specialist coaching each table.
- **Goal:** see, hands-on, why Power BI + Fabric is a strong home for your
  analytics (and apps), and leave with a concrete adoption plan.

## Labs

The labs are the hands-on core. Run them in order, or jump to a topic.

| # | Lab | Topic | Time |
| --- | --- | --- | --- |
| 0 | [Setup & orientation](labs/lab-00-setup/README.md) | Fabric workspace, insurance data, install Rayfin | 40m |
| 1 | [Tableau to Power BI](labs/lab-01-tableau-to-powerbi/README.md) | How the concepts map; first report | 60m |
| 2 | [Data modeling](labs/lab-02-data-modeling/README.md) | Star schema vs a flat extract | 75m |
| 3 | [Visualization design](labs/lab-03-visualization/README.md) | Rebuild a Tableau view the Power BI way | 75m |
| 4 | [Governance foundations](labs/lab-04-governance-foundations/README.md) | Workspaces, roles, RLS, endorsement | 50m |
| 5 | [Ingestion to OneLake](labs/lab-05-ingestion-onelake/README.md) | Data Factory, Dataflows, gateway, medallion | 90m |
| 6 | [Semantic model + Direct Lake](labs/lab-06-semantic-model-directlake/README.md) | sm_insurance, core DAX, AI-ready | 90m |
| 7 | [Copilot in reports](labs/lab-07-copilot-reports/README.md) | Build, narrate & write DAX with Copilot | 75m |
| 8 | [Migrate a workbook](labs/lab-08-migrate-a-workbook/README.md) | A full Tableau-to-Power BI use case | 90m |
| 9 | [MCP + GitHub Copilot](labs/lab-09-mcp-github-copilot/README.md) | Power BI MCP servers, PBIP, CI/CD | 75m |
| 10 | [Fabric Data Agent](labs/lab-10-data-agent-showcase/README.md) | Natural-language Q&A on the model | 45m |
| 11 | [Rayfin insurance app](labs/lab-11-rayfin-insurance-app/README.md) | Build a claims-intake app on Fabric with Rayfin | 75m |
| 12 | [Showcase & next steps](labs/lab-12-showcase-next-steps/README.md) | Reusable patterns, example apps, adoption | 45m |

## Three-day agenda -> labs

**Day 1 - Power BI Foundations & Best Practices**

| Session | Lab(s) |
| --- | --- |
| Kickoff + goals (from Tableau to Power BI, why now) + install Rayfin | [Lab 0](labs/lab-00-setup/README.md) |
| How the concepts map (worksheets, dashboards, LOD, extracts) | [Lab 1](labs/lab-01-tableau-to-powerbi/README.md) |
| Data modeling: the star schema (the biggest quality lever) | [Lab 2](labs/lab-02-data-modeling/README.md) |
| Visualization design best practices | [Lab 3](labs/lab-03-visualization/README.md) |
| Governance, RLS & migration approaches | [Lab 4](labs/lab-04-governance-foundations/README.md) + [migration-approaches](reference/migration-approaches.md) |

**Day 2 - Hands-On Migration Lab**

| Session | Lab(s) |
| --- | --- |
| Get the data into OneLake (real-world ingestion) | [Lab 5](labs/lab-05-ingestion-onelake/README.md) |
| Build the shared semantic model (Direct Lake) | [Lab 6](labs/lab-06-semantic-model-directlake/README.md) |
| Build reports faster with Copilot | [Lab 7](labs/lab-07-copilot-reports/README.md) |
| Migrate a real workbook, end to end (coached breakout) | [Lab 8](labs/lab-08-migrate-a-workbook/README.md) |

**Day 3 - Showcase & Next Steps**

| Session | Lab(s) |
| --- | --- |
| Developer workflow: GitHub Copilot + Power BI MCP servers | [Lab 9](labs/lab-09-mcp-github-copilot/README.md) |
| Ask your data: the Fabric Data Agent | [Lab 10](labs/lab-10-data-agent-showcase/README.md) |
| Build a data app on Fabric with Rayfin | [Lab 11](labs/lab-11-rayfin-insurance-app/README.md) |
| Showcase, example apps, adoption & commitments | [Lab 12](labs/lab-12-showcase-next-steps/README.md) + [adoption-roadmap](governance/adoption-roadmap.md) |

## Quick start

```bash
# 1. Generate the synthetic Contoso Insurance dataset (Python 3.10+, pandas + numpy)
python data/generate_data.py

# 2. Open Lab 0 and follow along in your Fabric tenant
#    labs/lab-00-setup/README.md
```

## What's in here

```
schwab-powerbi-workshop/
  data/            synthetic Contoso Insurance data generator (CSV output, gitignored)
  labs/            lab-00 .. lab-12  (the walk-throughs - start here)
  rayfin-app/      Rayfin insurance app skeleton (Contoso Claims Intake) for Lab 11
  src/
    notebooks/     PySpark medallion notebooks (Bronze/Silver/Gold)
    sql/           Warehouse gold + sample DAX queries
    pbip/          how the shared model is stored as PBIP (+ measures)
    cicd/          fabric-cicd parameter.yml + GitHub Actions workflow
  governance/      workspace governance, endorsement, migration assessment, adoption
  reference/       architecture, Tableau mapping, Copilot, MCP, Direct Lake, Rayfin, sources
  images/          rendered architecture diagrams
```

## Prerequisites

- A Microsoft Fabric capacity (a trial works for most labs; a dev **F** SKU is ideal).
- Power BI Desktop (latest) for the modeling and report labs.
- Python 3.10+ locally (pandas, numpy) to generate the sample data.
- **Node.js 20+**, VS Code, and the GitHub Copilot extension for the MCP (Lab 9)
  and Rayfin (Lab 11) labs.
- A Git repo (GitHub or Azure DevOps) for the PBIP + CI/CD lab.

## How to use this as Schwab's own repo

This folder is self-contained. To hand it to the Schwab team as a standalone repo,
copy `schwab-powerbi-workshop/` out, `git init`, and push. Nothing here depends on
the parent repository.

## Grounding & safety

- Technical guidance is grounded in Microsoft Learn - see
  [reference/sources.md](reference/sources.md).
- The dataset is **synthetic and fictional**. Do not commit real Schwab data,
  credentials, workspace GUIDs, or connection secrets (see `.gitignore`).

## License / trademark

Sample code in this workshop is provided as-is for enablement. "Microsoft",
"Fabric", "Power BI", "OneLake", "Rayfin" and "Tableau" are trademarks of their
respective owners, referenced here for identification only.
