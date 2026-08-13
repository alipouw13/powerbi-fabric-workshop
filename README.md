# From Tableau to Power BI on Microsoft Fabric

Workshop companion repo for an enterprise **Infrastructure & Operations (I&O)
analytics** team moving off Tableau. Three days, hands-on.

This repo is the hands-on half of the workshop deck
*"From Tableau to Power BI on Microsoft Fabric"*. Every lab maps to a numbered lab
slide, and the agenda below mirrors the deck's run of show exactly.

> **Scope.** Built for the tooling this team has **today**: Power BI Desktop, Power
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

- **Audience:** Infrastructure & Operations, spread across several sites.
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
| 9:45 | Architecture: now, next, and later | [current state](reference/current-state.md) |
| 10:30 | Power Query: connect, shape, combine, load | [Power Query snippets](src/powerquery/README.md) |
| 11:15 | Data modeling and star schema | [star schema](reference/star-schema.md) |
| 1:00 | DAX foundations for Tableau users | [DAX patterns](src/sql/sample_dax_queries.dax) |
| 2:15 | Visualization design and governance | [visual design](reference/visual-design.md), [governance](governance/workspace-governance.md) |
| 3:30 | Future vision, domain alignment and Day 2 setup | **[Day 1 setup](labs/day-1-setup/README.md)** |

### Day 2 - Hands-On Build & Migration Lab · 9:00 to 4:30
Full detail: [labs/README.md](labs/README.md)

| Time | Session | Lab |
| --- | --- | --- |
| 9:00 | Migration methodology, assess to validate | [migration approaches](reference/migration-approaches.md) |
| 9:45 | Day 2 approach: build with proven practices | [labs/README.md](labs/README.md) |
| 10:30 | Lab 0, data source connection, Power Query | **[Lab 0](labs/lab-00-connect-and-shape/README.md)** |
| 1:00 | Labs 1 and 2, model & report | **[Lab 1](labs/lab-01-semantic-model/README.md)** · **[Lab 2](labs/lab-02-report-page/README.md)** |
| 2:30 | Lab 3, DAX measures | **[Lab 3](labs/lab-03-dax-measures/README.md)** |
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

Labs run in **deck order**, which is also build order and the order Day 1 teaches in.
Lab 0 connects and shapes, then Lab 1 models, Lab 2 reports, Lab 3 measures. Setup and the
gateway connection happen on Day 1 afternoon, so they are prep rather than a numbered lab.

| Lab | Deck slide | Topic |
| --- | --- | --- |
| [Day 1 setup](labs/day-1-setup/README.md) | 5 (3:30 slot) | Power BI Desktop, sample data, **gateway install and test refresh**, **build four M365 Copilot agents** |
| [0 - Connect, shape, and load](labs/lab-00-connect-and-shape/README.md) | 21 | Folding, reference queries, folder combine, schema guard, **M365 Copilot** |
| [1 - Build the semantic model](labs/lab-01-semantic-model/README.md) | 22 | Import-mode star schema, relationships, date table, first measure, gateway refresh |
| [2 - Build your first report page](labs/lab-02-report-page/README.md) | 23 | Trend, business-unit drill breakdown, KPI cards, workshop theme |
| [3 - Practice DAX measures](labs/lab-03-dax-measures/README.md) | 24 | Percent of total, time intelligence, filter context, **M365 Copilot** |

## Domain breakout groups

Deck slide 25. Each group builds its own fact table onto the same conformed
dimensions.

All five groups analyze I&O outcomes for the same two fictional business units:
**Banking** and **Capital Markets**. The shared `dim_service` dimension contains
domain-specific services such as Digital Banking, Payments, Electronic Trading,
Market Data, and Clearing and Settlement. Every fact carries `service_key`, so
the same business-unit slicer works in every group's report.

| Group | Domain | Fact table |
| --- | --- | --- |
| 1 | ITSM & Operational Reporting | `fact_incident` |
| 2 | Capacity & Forecasting | `fact_capacity` |
| 3 | Mainframe Analytics | `fact_mainframe` |
| 4 | Service Desk & Workforce | `fact_service_desk` |
| 5 | Asset & Workplace Services | `fact_asset` |

The six conformed dimensions are `dim_date`, `dim_service`, `dim_configuration_item`,
`dim_team`, `dim_location` and `dim_severity`. `dim_service` and `dim_location` are
shared by all five facts; the rest apply to the groups whose fact carries that key.
`fact_asset` has no `date_key`, which gives group 5 a real modeling decision to make in
Lab 1.

## Quick start

```powershell
# 1. Generate the synthetic I&O dataset (Python 3.10+, pandas + numpy)
python data\generate_data.py

# 2. Do the Day 1 setup: Power BI Desktop, workspace, gateway, Copilot agents
#    labs\day-1-setup\README.md
#
# 3. Day 2 starts with the connection lab
#    labs\lab-00-connect-and-shape\README.md
```

## What's in here

```
powerbi-fabric-workshop/
  data/            synthetic I&O data generator (CSV output, gitignored)
  labs/            day-1-setup, then lab-00 .. lab-03 - all hands-on, all Day 2
  sessions/        Day 1 and Day 3 facilitator guides
  src/
    powerquery/    reusable Power Query M snippets
    sql/           sample DAX measures and validation queries
    pbip/          measure definitions, the source of truth for Lab 3
    theme/         io-workshop-theme.json, applied in Lab 2
  reference/       current state, gateway setup, star schema, visual design,
                   Tableau mapping, M365 Copilot, Copilot agents, migration
                   approaches, sources
  governance/      workspace governance, endorsement, migration assessment, adoption
  images/          diagrams
```

## Prerequisites

**Every attendee:**
- Power BI Desktop (latest)
- Access to a Power BI workspace you can publish to
- Python 3.10+ with pandas and numpy, to generate the sample data
- **M365 Copilot** for Labs 0 and 3 - at minimum one licence per pair

**For the platform team:**
- An on-premises data gateway (standard mode) with a connection to the I&O SQL
  sources. See [reference/gateway-setup.md](reference/gateway-setup.md).

**Not required:** Fabric capacity, Lakehouse access, Node.js, VS Code, GitHub
Copilot.

## Using M365 Copilot

M365 Copilot is the only AI available for this work, and it **cannot see your
semantic model**. The Day 1 setup turns that constraint into a setup step: attendees ask
Copilot what it can genuinely do for Power BI, then build **four specialist agents** - one
per lab - primed with the workshop's model card.

| Agent | Lab | Job |
| --- | --- | --- |
| Query Engineer | 0 | Power Query M, folding, folder combine, schema guards |
| Model Architect | 1 | Star schema, grain, relationships, date table |
| Report Designer | 2 | One question per page, visual choice, KPI cards |
| DAX Coach | 3 | Measures, filter context, Tableau calc translation |

Briefs are in [reference/copilot-agents.md](reference/copilot-agents.md). From there every
lab runs the same loop:

1. Ask your lab's agent in business terms
2. Read the output - if you cannot explain it, do not use it
3. Paste into the DAX editor or the Power Query Advanced Editor
4. **Verify** - DAX at three grains (total, business unit, month); M for rows, nulls,
   types and folding

**Never paste real data, credentials, connection strings or ticket contents into any AI
tool.** Schema and code only.

Deck slide 26 scopes this the same way, including *"Draft Power Query M to paste into the
Advanced Editor, but cannot see your model or run queries"* - which is exactly how Labs 0
and 3 use it. See
[reference/copilot-in-power-bi.md](reference/copilot-in-power-bi.md).

## Grounding & safety

- Technical guidance is grounded in Microsoft Learn - see
  [reference/sources.md](reference/sources.md).
- The dataset is **synthetic and fictional**. Do not commit real customer data,
  credentials, workspace GUIDs, server names, or connection secrets.

## License / trademark

Sample code is provided as-is for enablement. "Microsoft", "Microsoft Copilot",
"Microsoft Fabric", "Microsoft Purview", "OneLake", "Power BI" and "Tableau" are
trademarks of their respective owners, referenced here for identification only.
