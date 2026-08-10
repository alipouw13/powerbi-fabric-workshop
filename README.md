# Schwab x Microsoft - Power BI Workshop (3 days)

A hands-on, three-day workshop that helps a **Tableau** team learn **Power BI** by
rebuilding a familiar analysis end to end: a **property & casualty (P&C)
insurance** book, "Contoso Insurance". Every lab maps to the on-site deck and runs
on a small, fully **synthetic** dataset (no real Schwab data), using only what the
team can actually use today: **Power BI Desktop, Power Query, Import or
DirectQuery, and M365 Copilot** as a writing assistant.

> **Scope note.** This workshop is deliberately constrained to match Schwab's
> current tooling. There is **no Lakehouse, no OneLake, no Direct Lake, no Copilot
> embedded in Power BI, and no Fabric Data Agent.** All transformation work is
> done manually in **Power Query**. M365 Copilot is used the only way it can be
> used here - draft in Copilot, review, then **copy and paste** into Power Query
> or the DAX editor. Fabric material is retained as [appendix reference](#appendix---not-in-scope-today)
> only, so the team can see where the path leads without being blocked.

> **What this is:** a guided walk-through you run in Power BI Desktop and your own
> Power BI workspace, built for people who know Tableau and are new to Power BI.
> **What this isn't:** a connection to any real Schwab system. The sample data is
> generated locally.

## The story

```
Today:  Tableau workbooks + large Excel files + flat SQL sources
        -> one Import model per workbook, logic buried in extracts

This workshop:
        Same sources, same gateway, same Import/DirectQuery connections
        -> transformations done deliberately in Power Query
        -> shaped into a star schema
        -> one shared semantic model (sm_insurance) reused by many reports
        -> M365 Copilot drafts the M and DAX; you review and paste it in

Later (appendix, not covered hands-on):
        OneLake, medallion layering, Direct Lake, Copilot in Power BI,
        Data Agents, and Fabric-backed apps
```

Days 1-3 are entirely about what works **today**. See
[reference/schwab-current-state.md](reference/schwab-current-state.md) for the
constraints every lab is written against and
[reference/tableau-to-powerbi.md](reference/tableau-to-powerbi.md) for the
concept-by-concept translation from Tableau.

## Who it's for and how it runs

- **Audience:** 15-18 people across Austin and Phoenix, cross-functional rather
  than a centralized reporting group. Most have Tableau experience. No Power BI
  experience assumed. Some Schwab Data team members may join virtually.
- **Format:** a conference room with short teaching blocks, then breakouts where
  small groups do the hands-on labs with a Microsoft specialist coaching each table.
- **Goal:** leave able to build governed Power BI content with the connections and
  tooling available **today**, with a shared architecture vocabulary, a concrete
  migration plan, and the start of a community of practice for data visualization.

### What we use, and what we don't

| Capability | Status | How the workshop handles it |
| --- | --- | --- |
| Power BI Desktop, Power Query, DAX | **In scope** | Every hands-on lab |
| Import and DirectQuery storage modes | **In scope** | Lab 5 and Lab 6 |
| On-premises data gateway | **In scope** | Lab 5, as the connection broker |
| Power BI Service: workspaces, RLS, endorsement, apps | **In scope** | Lab 4 |
| **M365 Copilot** | **In scope** | Lab 7 - draft, review, copy/paste into Power Query and DAX |
| Copilot embedded in Power BI | Not available | Not covered |
| Fabric Data Agent, Copilot Studio | Not available | Not covered |
| Lakehouse, OneLake, Direct Lake, Dataflows Gen2 | Not available | Appendix reference only |
| MCP servers, PBIP + CI/CD, Rayfin | Not available | Appendix reference only |

Every lab carries an **In scope** or **Appendix** badge so nobody is ever blocked
by a feature they do not have. Full detail is in
[reference/schwab-current-state.md](reference/schwab-current-state.md).

## Labs

The labs are the hands-on core. Run them in order, or jump to a topic.

| # | Lab | Topic | Time | Scope |
| --- | --- | --- | --- | --- |
| 0 | [Setup & orientation](labs/lab-00-setup/README.md) | Power BI Desktop, insurance data, current-state framing | 40m | In scope |
| 1 | [Tableau to Power BI](labs/lab-01-tableau-to-powerbi/README.md) | How the concepts map; first report | 60m | In scope |
| 2 | [Data modeling](labs/lab-02-data-modeling/README.md) | Flat vs star vs snowflake | 75m | In scope |
| 3 | [Visualization design](labs/lab-03-visualization/README.md) | Rebuild a Tableau view the Power BI way | 75m | In scope |
| 4 | [Governance foundations](labs/lab-04-governance-foundations/README.md) | Workspaces, roles, RLS, endorsement | 50m | In scope |
| 5 | [Connect & transform in Power Query](labs/lab-05-ingestion-onelake/README.md) | Gateway, Import vs DirectQuery, folding, Excel, M | 120m | In scope |
| 6 | [The shared semantic model](labs/lab-06-semantic-model-directlake/README.md) | sm_insurance, core DAX, storage mode choice | 90m | In scope |
| 7 | [M365 Copilot for DAX and M](labs/lab-07-copilot-reports/README.md) | Draft, review, copy/paste - the only AI path available | 90m | In scope |
| 8 | [Migrate a workbook](labs/lab-08-migrate-a-workbook/README.md) | A full Tableau-to-Power BI use case | 120m | In scope |
| 12 | [Community of practice & next steps](labs/lab-12-showcase-next-steps/README.md) | CoE charter, reusable patterns, adoption | 60m | In scope |

### Appendix - not in scope today

Kept for reference so the team can see the roadmap and make informed requests.
None of these are run hands-on, and none are prerequisites for anything above.

| # | Lab | Why it's not in scope |
| --- | --- | --- |
| 9 | [MCP + GitHub Copilot](labs/lab-09-mcp-github-copilot/README.md) | MCP servers not available |
| 10 | [Fabric Data Agent](labs/lab-10-data-agent-showcase/README.md) | Data Agents not available |
| 11 | [Rayfin insurance app](labs/lab-11-rayfin-insurance-app/README.md) | Requires Fabric |

## Three-day agenda -> labs

**Day 1 - Power BI foundations, Tableau corollaries & modeling vocabulary**

| Session | Lab(s) |
| --- | --- |
| Kickoff: where Schwab is today, and what this workshop will and will not cover | [Lab 0](labs/lab-00-setup/README.md) + [current state](reference/schwab-current-state.md) |
| How the concepts map (worksheets, dashboards, LOD, extracts, .hyper) | [Lab 1](labs/lab-01-tableau-to-powerbi/README.md) |
| Modeling patterns: flat vs star vs snowflake | [Lab 2](labs/lab-02-data-modeling/README.md) |
| Visualization design best practices | [Lab 3](labs/lab-03-visualization/README.md) |
| Governance, RLS & migration approaches | [Lab 4](labs/lab-04-governance-foundations/README.md) + [migration-approaches](reference/migration-approaches.md) |

**Day 2 - Hands-on Power BI: connect, transform, model, migrate**

No AI content on Day 2. This is the practical build day, and the longest one.

| Session | Lab(s) |
| --- | --- |
| Connect the way Schwab connects: gateway, Import vs DirectQuery | [Lab 5](labs/lab-05-ingestion-onelake/README.md), steps 1-3 |
| Transform by hand in Power Query: folding, shaping facts and dimensions | [Lab 5](labs/lab-05-ingestion-onelake/README.md), steps 4-7 |
| Taming large Excel sources | [Lab 5](labs/lab-05-ingestion-onelake/README.md), step 8 |
| Build the shared semantic model | [Lab 6](labs/lab-06-semantic-model-directlake/README.md) |
| Migrate a real workbook, end to end (extended coached breakout) | [Lab 8](labs/lab-08-migrate-a-workbook/README.md) |

**Day 3 - M365 Copilot, optimization & the community of practice**

| Session | Lab(s) |
| --- | --- |
| M365 Copilot for DAX: explain, translate from Tableau, draft, review, paste | [Lab 7](labs/lab-07-copilot-reports/README.md), Part A |
| M365 Copilot for Power Query M: draft a transformation, paste into Advanced Editor | [Lab 7](labs/lab-07-copilot-reports/README.md), Part B |
| Documentation and review workflows with M365 Copilot | [Lab 7](labs/lab-07-copilot-reports/README.md), Part C |
| Performance, refresh, and troubleshooting clinic | [Lab 8](labs/lab-08-migrate-a-workbook/README.md), step 9 |
| Where this leads: a short look at Fabric, Direct Lake and Copilot in Power BI | [Appendix labs 9-11](#appendix---not-in-scope-today) |
| Community of practice: charter, standards, adoption & commitments | [Lab 12](labs/lab-12-showcase-next-steps/README.md) + [adoption-roadmap](governance/adoption-roadmap.md) |

## Quick start

```bash
# 1. Generate the synthetic Contoso Insurance dataset (Python 3.10+, pandas + numpy)
python data/generate_data.py

# 2. Open Lab 0 and follow along in Power BI Desktop
#    labs/lab-00-setup/README.md
```

## What's in here

```
schwab-powerbi-workshop/
  data/            synthetic Contoso Insurance data generator (CSV output, gitignored)
  labs/            lab-00 .. lab-12  (the walk-throughs - start here)
  src/
    powerquery/    reusable Power Query M snippets used in Lab 5
    sql/           source views + sample DAX queries
    pbip/          measure definitions used across the labs
  governance/      workspace governance, endorsement, migration assessment, adoption
  reference/       current state & constraints, Tableau mapping, M365 Copilot,
                   migration approaches, sources
  images/          diagrams

  # Appendix only - not used in any hands-on lab:
  rayfin-app/      Rayfin app skeleton (Fabric)
  src/notebooks/   PySpark medallion notebooks (Fabric)
  src/cicd/        fabric-cicd parameter.yml + GitHub Actions workflow
```

## Prerequisites

**Required for every attendee (Days 1-2):**

- Power BI Desktop (latest) for every hands-on lab.
- Access to a Power BI workspace where you can publish.
- Python 3.10+ locally (pandas, numpy) to generate the sample data.
- **M365 Copilot** for Lab 7. Attendees without a license pair with someone who
  has one - Lab 7 is designed for pairs.

**Not required.** No Fabric capacity, no Lakehouse, no Node.js, no VS Code, no
GitHub Copilot. The appendix labs are reading material, not exercises.

## How to use this as Schwab's own repo

This folder is self-contained. To hand it to the Schwab team as a standalone repo,
copy `schwab-powerbi-workshop/` out, `git init`, and push. Nothing here depends on
the parent repository.

## Grounding & safety

- Technical guidance is grounded in Microsoft Learn - see
  [reference/sources.md](reference/sources.md).
- The dataset is **synthetic and fictional**. Do not commit real Schwab data,
  credentials, workspace GUIDs, or connection secrets (see `.gitignore`).
- **Do not paste real Schwab data, credentials, or customer information into
  M365 Copilot or any other AI tool.** Lab 7 uses synthetic data and pasted code
  only - never source records.

## License / trademark

Sample code in this workshop is provided as-is for enablement. "Microsoft",
"Fabric", "Power BI", "OneLake", "Rayfin" and "Tableau" are trademarks of their
respective owners, referenced here for identification only.
