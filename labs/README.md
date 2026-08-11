# Day 2 labs

All hands-on work in this workshop happens on **Day 2**. Day 1 is teaching and
alignment; Day 3 is showcase and roadmap. That mirrors the deck exactly - the
four numbered labs appear on slides 19 to 22, and every one of them is a Day 2
session on the slide 16 run of show.

| Lab | Deck slide | Day 2 slot | Copilot agent | Applies the Day 1 session |
| --- | --- | --- | --- | --- |
| [Lab 0 - Setup and gateway](lab-00-setup-and-gateway/README.md) | n/a (setup) | Day 1, 3:30 | *builds all four* | Prep, not a numbered lab |
| [Lab 1 - Build the semantic model](lab-01-semantic-model/README.md) | 19 | 10:30 | Model Architect | Data modeling and star schema |
| [Lab 2 - Build your first report page](lab-02-report-page/README.md) | 20 | 10:30 | Report Designer | Visualization design and governance |
| [Lab 3 - Practice DAX measures](lab-03-dax-measures/README.md) | 21 | 1:00 | DAX Coach | DAX foundations for Tableau users |
| [Lab 4 - Connect, shape, and load with Power Query](lab-04-power-query/README.md) | 22 | 2:30 | Query Engineer | Power Query: connect, shape, combine, load |

Run them in order. Labs 1 and 2 build the thing; Labs 3 and 4 make it good.

> **Do Lab 0 on Day 1 afternoon.** It covers the gateway, and a gateway problem discovered
> at 10:30 on Day 2 costs the room an hour. It also sets up the four Copilot agents, which
> every lab after it assumes you have open.

## Domain breakout groups

Deck slide 23. Five I&O domain groups supporting two business units, one shared
modeling pattern.

| Group | Domain | Fact table | The flagship report answers |
| --- | --- | --- | --- |
| 1 | ITSM & Operational Reporting | `fact_incident` | Incident and SLA trends, and whether Banking or Capital Markets is carrying more risk |
| 2 | Capacity & Forecasting | `fact_capacity` | Utilization, demand and headroom, and which business unit runs out first |
| 3 | Mainframe Analytics | `fact_mainframe` | MIPS consumption and batch windows, split across Deposits and Post-Trade |
| 4 | Service Desk & Workforce | `fact_service_desk` | Ticket volumes, first-contact resolution and staffing coverage per service |
| 5 | Asset & Workplace Services | `fact_asset` | Inventory, lifecycle and where the out-of-warranty risk is concentrated |

**Reuse, do not restart.** Every group builds on the same conformed dimensions, the same
staging query patterns and the same workshop theme. A measure one group writes is a
pattern the others lift straight into their report. That is the whole point of slide 10:
*one model, many domains*.

**Every fact carries `service_key`**, so `dim_service[business_unit]` slices all five the
same way, and `business_unit` → `business_domain` → `service_name` is a drill hierarchy
every group can put on its flagship page. Two business units, Banking and Capital Markets;
five domains under each.

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

M365 Copilot is the only AI available for this work, and it **cannot see your model**. So
in [Lab 0](lab-00-setup-and-gateway/README.md#6-meet-m365-copilot-then-build-your-four-agents)
you do two things: ask Copilot what it can genuinely do for Power BI, then set up four
specialist agents - one per lab - primed with this workshop's model card.

After that, every lab follows the same loop:

1. **Ask** your lab's agent, in business terms
2. **Read** - if you cannot explain the output, do not use it
3. **Paste** into the DAX editor or the Power Query Advanced Editor
4. **Verify** - DAX at three grains (total, business unit, month); M for rows, nulls,
   types and folding

Step 4 is the one people skip, and it is the one that catches the errors.

The briefs are in [reference/copilot-agents.md](../reference/copilot-agents.md). Keep one
browser tab open per agent and you have four specialists beside you all day.

**Never paste real data, credentials, connection strings or ticket contents into any AI
tool.** You paste schema and code, never rows.

## What is not in these labs

Deliberately absent, because this environment does not have them today:

- Copilot embedded in Power BI Desktop or the service
- Fabric Data Agent, Copilot Studio
- Lakehouse, OneLake, Direct Lake, medallion layering
- Dataflows Gen2, Data Factory pipelines
- MCP servers, PBIP source control, CI/CD

Deck slides 30 to 32 cover these as **future, approval-dependent** on Day 3. They are a
readiness conversation, not an exercise. Publishing the Lab 0 agent briefs as *named,
shared* M365 Copilot agents belongs in the same category - the briefs work today as
pasted instructions, and turning them into published agents needs platform and security
approval. See [sessions/day-3-showcase.md](../sessions/day-3-showcase.md).
