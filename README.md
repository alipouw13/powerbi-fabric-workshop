# Schwab - From Tableau to Power BI on Microsoft Fabric

Workshop companion repo for **Charles Schwab, Infrastructure & Operations
Analytics Data Platforms Engineering**. Three days, August 18-20 2026.

This repo is the hands-on half of the deck
*"From Tableau to Power BI on Microsoft Fabric - Revised 2026-08-10"*. Every lab
maps to a numbered lab slide, and the agenda below mirrors the deck's run of show
exactly.

> **Scope.** Built for the tooling I&O has **today**: Power BI Desktop, Power
> Query, Import mode, the on-premises data gateway, and **M365 Copilot** as a
> drafting assistant. There is no Lakehouse, no OneLake, no Direct Lake, no
> Copilot inside Power BI, and no Fabric Data Agent. Those appear on Day 3 as
> *art of the possible*, clearly labelled future and approval-dependent.

## The story

```
Today:  Tableau workbooks + flat files + large Excel extracts
        -> SQL via Import mode, through the on-premises gateway
        -> one workbook, one version of truth

This workshop:
        Same sources, same gateway, same Import mode
        -> shaped deliberately in Power Query
        -> modeled as a star: one fact per domain, conformed dimensions
        -> one semantic model per domain, reused by every report
        -> M365 Copilot drafts the DAX and M; you review and paste it in

Later, approval-dependent (Day 3 preview only):
        OneLake, Lakehouse, medallion, Direct Lake, Copilot in Power BI,
        Fabric Data Agents
```

## Who it's for

- **Audience:** Infrastructure & Operations, across Austin and Phoenix.
  Cross-functional rather than a centralized reporting group. Most have Tableau
  experience. No Power BI experience assumed.
- **Format:** teaching blocks, then Day 2 breakouts where five domain groups build
  a flagship report with a Microsoft specialist coaching each table.
- **Goal:** retire Tableau in I&O and standardize on Power BI, with a shared
  modeling pattern, a certified semantic model per domain, and a committed 90-day
  roadmap.

## Three-day agenda

**All hands-on work is on Day 2.** Day 1 is foundation, Day 3 is showcase.

### Day 1 - Foundation & Alignment · 9:00 to 4:30
Full detail: [sessions/day-1-foundations.md](sessions/day-1-foundations.md)

| Time | Session | Material |
| --- | --- | --- |
| 9:00 | Welcome, goals, and the Tableau to Power BI mindset | [Tableau to Power BI](reference/tableau-to-powerbi.md) |
| 9:45 | Architecture: now, next, and later | [current state](reference/schwab-current-state.md) |
| 10:30 | Power Query: connect, shape, combine, load | [Power Query snippets](src/powerquery/README.md) |
| 11:15 | Data modeling and star schema | [star schema](reference/star-schema.md) |
| 1:00 | DAX foundations for Tableau users | [DAX patterns](src/sql/sample_dax_queries.dax) |
| 2:15 | Visualization design and governance | [visual design](reference/visual-design.md), [governance](governance/workspace-governance.md) |
| 3:30 | Domain alignment and Day 2 setup | **[Lab 0 - Setup and gateway](labs/lab-00-setup-and-gateway/README.md)** |

### Day 2 - Hands-On Build & Migration Lab · 9:00 to 4:30
Full detail: [labs/README.md](labs/README.md)

| Time | Session | Lab |
| --- | --- | --- |
| 9:00 | Migration methodology, assess to validate | [migration approaches](reference/migration-approaches.md) |
| 9:45 | Day 2 approach: modeling, reports, governance | [labs/README.md](labs/README.md) |
| 10:30 | Labs 1 and 2, model and report | **[Lab 1](labs/lab-01-semantic-model/README.md)** · **[Lab 2](labs/lab-02-report-page/README.md)** |
| 1:00 | Labs 3 and 4, DAX measures | **[Lab 3](labs/lab-03-dax-measures/README.md)** |
| 2:30 | Labs 3 and 4 continued, Power Query practice | **[Lab 4](labs/lab-04-power-query/README.md)** |
| 4:00 | Stand-up: what each group built | Readouts |

### Day 3 - Showcase, Lessons & Next Steps · 9:00 to 3:00
Full detail: [sessions/day-3-showcase.md](sessions/day-3-showcase.md)

| Time | Session |
| --- | --- |
| 9:00 | Group showcases, five domains |
| 10:30 | Lessons learned and pitfalls |
| 11:15 | Reusable patterns library |
| 11:45 | Art of the possible: Fabric, once approved |
| 1:00 | Adoption roadmap: now, next, later |
| 2:00 | Community of Practice and next steps |

## The labs

| Lab | Deck slide | Topic |
| --- | --- | --- |
| [0 - Setup and gateway](labs/lab-00-setup-and-gateway/README.md) | setup | Power BI Desktop, sample data, **gateway install, connection, test refresh** |
| [1 - Build the semantic model](labs/lab-01-semantic-model/README.md) | 19 | Import-mode star schema, relationships, date table, first measure |
| [2 - Build your first report page](labs/lab-02-report-page/README.md) | 20 | Trend, breakdown, KPI cards, workshop theme |
| [3 - Practice DAX measures](labs/lab-03-dax-measures/README.md) | 21 | Running total, percent of total, period over period, **M365 Copilot** |
| [4 - Connect, shape, and load](labs/lab-04-power-query/README.md) | 22 | Folding, reference queries, parameters, Excel folder combine, **M365 Copilot** |

## Domain breakout groups

Deck slide 23. Each group builds its own fact table onto the same conformed
dimensions.

| Group | Domain | Fact table |
| --- | --- | --- |
| 1 | ITSM & Operational Reporting | `fact_incident` |
| 2 | Capacity & Forecasting | `fact_capacity` |
| 3 | Mainframe Analytics | `fact_mainframe` |
| 4 | Service Desk & Workforce | `fact_service_desk` |
| 5 | Asset & Workplace Services | `fact_asset` |

Conformed dimensions shared by all five: `dim_date`,
`dim_configuration_item`, `dim_service`, `dim_team`, `dim_location`,
`dim_severity`.

## Quick start

```powershell
# 1. Generate the synthetic I&O dataset (Python 3.10+, pandas + numpy)
python data\generate_data.py

# 2. Open Lab 0 and set up Power BI Desktop and the gateway
#    labs\lab-00-setup-and-gateway\README.md
```

## What's in here

```
schwab-powerbi-fabric-workshop/
  data/            synthetic I&O data generator (CSV output, gitignored)
  labs/            lab-00 .. lab-04  - all hands-on, all Day 2
  sessions/        Day 1 and Day 3 facilitator guides
  src/
    powerquery/    reusable Power Query M snippets
    sql/           sample DAX measures and validation queries
    pbip/          measure definitions, the source of truth for Lab 3
    theme/         schwab-io-theme.json, applied in Lab 2
  reference/       current state, gateway setup, star schema, visual design,
                   Tableau mapping, M365 Copilot, migration approaches, sources
  governance/      workspace governance, endorsement, migration assessment, adoption
  images/          diagrams
```

## Prerequisites

**Every attendee:**
- Power BI Desktop (latest)
- Access to a Power BI workspace you can publish to
- Python 3.10+ with pandas and numpy, to generate the sample data
- **M365 Copilot** for Labs 3 and 4 - at minimum one licence per pair

**For the platform team:**
- An on-premises data gateway (standard mode) with a connection to the I&O SQL
  sources. See [reference/gateway-setup.md](reference/gateway-setup.md).

**Not required:** Fabric capacity, Lakehouse access, Node.js, VS Code, GitHub
Copilot.

## Using M365 Copilot

M365 Copilot is the only AI available for this work, and it **cannot see your
semantic model**. The labs use it as a drafting assistant with a copy-and-paste
handoff:

1. Paste the [schema block](labs/lab-03-dax-measures/README.md#your-schema-block)
2. Ask in business terms
3. Read the output - if you cannot explain it, do not use it
4. Paste into the DAX editor or the Power Query Advanced Editor
5. **Verify** - DAX at three grains; M for rows, nulls, types and folding

**Never paste real Schwab data, credentials, connection strings or ticket
contents into any AI tool.** Schema and code only.

> **Note on deck slide 24.** The slide currently says M365 Copilot `Does not draft
> DAX or write report visuals for you`. Labs 3 and 4 do use it to draft DAX and
> Power Query M, which is well within what M365 Copilot can do when you supply the
> schema as context. See
> [reference/copilot-in-power-bi.md](reference/copilot-in-power-bi.md#note-for-the-deck-slide-24)
> for suggested replacement wording.

## Grounding & safety

- Technical guidance is grounded in Microsoft Learn - see
  [reference/sources.md](reference/sources.md).
- The dataset is **synthetic and fictional**. Do not commit real Schwab data,
  credentials, workspace GUIDs, server names, or connection secrets.

## License / trademark

Sample code is provided as-is for enablement. "Microsoft", "Microsoft Copilot",
"Microsoft Fabric", "Microsoft Purview", "OneLake", "Power BI" and "Tableau" are
trademarks of their respective owners, referenced here for identification only.
