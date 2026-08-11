# Day 2 labs

All hands-on work in this workshop happens on **Day 2**. Day 1 is teaching and
alignment; Day 3 is showcase and roadmap. That mirrors the deck exactly - the
four numbered labs appear on slides 19 to 22, and every one of them is a Day 2
session on the slide 16 run of show.

| Lab | Deck slide | Day 2 slot | Applies the Day 1 session |
| --- | --- | --- | --- |
| [Lab 0 - Setup and gateway](lab-00-setup-and-gateway/README.md) | n/a (setup) | Day 1, 3:30 | Prep, not a numbered lab |
| [Lab 1 - Build the semantic model](lab-01-semantic-model/README.md) | 19 | 10:30 | Data modeling and star schema |
| [Lab 2 - Build your first report page](lab-02-report-page/README.md) | 20 | 10:30 | Visualization design and governance |
| [Lab 3 - Practice DAX measures](lab-03-dax-measures/README.md) | 21 | 1:00 | DAX foundations for Tableau users |
| [Lab 4 - Connect, shape, and load with Power Query](lab-04-power-query/README.md) | 22 | 2:30 | Power Query: connect, shape, combine, load |

Run them in order. Labs 1 and 2 build the thing; Labs 3 and 4 make it good.

> **Do Lab 0 on Day 1 afternoon.** It covers the gateway, and a gateway problem
> discovered at 10:30 on Day 2 costs the room an hour.

## Domain breakout groups

Deck slide 23. Five groups, five business units, one shared modeling pattern.

| Group | Domain | Fact table | The flagship report answers |
| --- | --- | --- | --- |
| 1 | ITSM & Operational Reporting | `fact_incident` | Incident, change and problem trends with SLA attainment and MTTR |
| 2 | Capacity & Forecasting | `fact_capacity` | Utilization, demand and headroom with a simple forecast view |
| 3 | Mainframe Analytics | `fact_mainframe` | MIPS consumption, batch windows and throughput over time |
| 4 | Service Desk & Workforce | `fact_service_desk` | Ticket volumes, first-contact resolution and staffing coverage |
| 5 | Asset & Workplace Services | `fact_asset` | Inventory, configuration coverage and lifecycle status from the CMDB |

**Reuse, do not restart.** Every group builds on the same conformed dimensions,
the same staging query patterns and the same workshop theme. A measure one group
writes is a pattern the others lift straight into their report. That is the whole
point of slide 10: *one model, many domains*.

## Shared conventions

Agree these before you start, so five groups produce five reports that look like
they came from one team.

| Thing | Convention |
| --- | --- |
| Semantic model | `sm_io_<domain>` - `sm_io_itsm`, `sm_io_capacity` |
| Report | `rpt_io_<domain>_<subject>` |
| Measure names | Business language, title case: `Total Incidents`, not `count_inc` |
| Dimension tables | `dim_<entity>`, singular entity name |
| Fact tables | `fact_<event>`, singular event name |
| Keys | `<entity>_key`, integer, hidden in report view |
| Theme | [`src/theme/schwab-io-theme.json`](../src/theme/schwab-io-theme.json) on every report |
| Workspace | Never My workspace |

## Using M365 Copilot in the labs

M365 Copilot is the only AI available for this work, and it **cannot see your
model**. Every lab that uses it follows the same loop:

1. **Context** - paste the schema block from [Lab 3](lab-03-dax-measures/README.md#your-schema-block)
2. **Ask** - state what you want in business terms
3. **Read** - if you cannot explain the output, do not use it
4. **Paste** - into the DAX editor or the Power Query Advanced Editor
5. **Verify** - DAX at three grains; M for rows, nulls, types and folding

Step 5 is the one people skip, and it is the one that catches the errors.

**Never paste real Schwab data, credentials, connection strings or ticket
contents into any AI tool.** You paste schema and code, never rows.

## What is not in these labs

Deliberately absent, because Schwab does not have them today:

- Copilot embedded in Power BI Desktop or the service
- Fabric Data Agent, Copilot Studio
- Lakehouse, OneLake, Direct Lake, medallion layering
- Dataflows Gen2, Data Factory pipelines
- MCP servers, PBIP source control, CI/CD

Deck slides 30 to 32 cover these as **future, approval-dependent** on Day 3. They
are a readiness conversation, not an exercise. See
[sessions/day-3-showcase.md](../sessions/day-3-showcase.md).
