# Day 1 - Foundation & Alignment

**Day 1 · 9:00 to 4:30 · Deck slides 4 to 16**

> **Outcome:** A shared blueprint for how I&O models data.

Day 1 is teaching and alignment. **There are no numbered labs.** The only
hands-on activity is [Day 1 setup](../labs/day-1-setup/README.md) in the
3:30 slot, which is setup for Day 2 rather than an exercise.

## Run of show

Deck slide 5. Times are indicative and adjust to the room.

| Time | Session | Lead | Focus | Material |
| --- | --- | --- | --- | --- |
| 9:00 | Welcome, goals, and the Tableau to Power BI mindset | Customer lead | Why we are moving, what good looks like | Slides 2, 3, 6 · [Tableau to Power BI](../reference/tableau-to-powerbi.md) |
| 9:45 | Architecture: now, next, and later | Microsoft | Today's platform, and a realistic path to Fabric | Slide 7 · [current state](../reference/current-state.md) |
| 10:30 | Power Query: connect, shape, combine, load | Microsoft | Best practices for clean, fast-refreshing queries | Slide 8 · [Power Query snippets](../src/powerquery/README.md) |
| 11:15 | Data modeling and star schema | Microsoft | Relationships, keys, storage modes | Slides 9, 10, 11 · [star schema](../reference/star-schema.md) |
| 1:00 | DAX foundations for Tableau users | Microsoft | Calculated fields to measures | Slide 12 · [DAX patterns](../src/sql/sample_dax_queries.dax) |
| 2:15 | Visualization design and governance | Microsoft | Show Me to visuals, ownership, Purview | Slides 13, 14 · [visual design](../reference/visual-design.md), [governance](../governance/workspace-governance.md) |
| 3:30 | Future vision, domain alignment and Day 2 setup | Customer lead, platform team | Pick flagship reports by LOB, confirm the gateway connection | Slides 15, 16 · [Day 1 setup](../labs/day-1-setup/README.md) |

## What each session needs to land

### 9:00 - The mindset shift
Slide 6 carries the whole day: *Tableau blends data inside each workbook. Power BI
models data once, then every report reuses it.*

Everything else on Day 1 is a consequence of that sentence. If the room leaves
still thinking of a semantic model as "the extract", Day 2 will produce five wide
tables with different numbers on them.

Use the translation table on slide 6, but say the caveat out loud: it is a
translation guide, **not an exact substitution**. The engines genuinely differ,
and pretending otherwise sets people up to be surprised in Lab 3.

### 9:45 - Architecture
Slide 7's four columns are the honest picture: **Now** (flat files, SQL via
Import, the gateway), **Next** (star modeling, certified sources, refresh
discipline), **Later, approval-dependent** (OneLake, medallion, Direct Lake), and
**Always** (Purview, workspace roles, named owners).

Be explicit that **Later** is not on the agenda this week. It appears again on
Day 3 as art of the possible. Naming that now prevents three days of people
waiting for a capability that is not coming.

### 10:30 - Power Query
Because there is no Lakehouse and no Dataflow, **Power Query is the only place
transformation logic can live**. That makes this session more load-bearing here
than it would be at a customer with a lake.

Cover connect / shape / combine / load from slide 8, and land two things hard:
- **Filter and remove columns first.** Cheapest performance win available.
- **Query folding decides refresh time**, and a broken fold pushes work onto the
  gateway server. Tie it to [gateway setup](../reference/gateway-setup.md).

This session is also the one Day 2 opens on:
[Lab 0](../labs/lab-00-connect-and-shape/README.md) is the connect-and-shape lab, and it
runs before any modeling. Say that here, so the room knows this material is used first
rather than last.

### 11:15 - Data modeling
Slides 9, 10 and 11. The star diagram on slide 9 is the picture the room should
be able to draw from memory by lunch.

Slide 10 is the one that makes it concrete for this audience: five fact tables,
one per domain, all joining the **same conformed dimensions**. That is the
mechanism by which two groups' reports reconcile.

Slide 11's "unlearn this" callout deserves airtime: *Do not recreate a giant flat
extract in Power BI.*

### 1:00 - DAX
Slide 12's mapping table, then the three golden rules: measures not columns,
learn `CALCULATE` first, always use `DIVIDE`.

The hardest idea is filter context versus Tableau's compute-using. Do not rush
it - Lab 3 depends entirely on this landing.

### 2:15 - Visualization and governance
Slide 13's Show Me mapping, then slide 14's six governance pillars.

Governance is not a Day 3 topic. Slide 7 says Purview labels, workspace roles and
named ownership apply **now**. Set the expectation that every Day 2 report gets an
owner before it gets an audience.

### 3:30 - Future vision, domain alignment and Day 2 setup
Two halves. First the **future vision**: slides 15 and 16, embedded Copilot and
natural-language assistance, then Fabric, OneLake and governed agents. Both are labelled
*future, approval-dependent* on the slide, and both should be framed that way out loud -
what becomes possible once licensing and governance are approved, not something anyone can
use tomorrow.

Then run [Day 1 setup](../labs/day-1-setup/README.md). By the end of it:

- Power BI Desktop installed and signed in for everyone
- Sample data generated, or source access confirmed
- **The gateway proven with a test refresh**, or a request in flight with an owner
- Five groups formed, each with a named flagship report and the question it answers
- M365 Copilot pairs agreed for Day 2
- Four M365 Copilot specialist agents set up, one per lab, primed with the
  [model card](../reference/copilot-agents.md#step-2-the-model-card)

Deck slide 18 makes this non-optional: *Lab 0 setup and the gateway connection are
completed on Day 1 afternoon.*

## Facilitator notes

- **The gateway is the risk.** Everything on Day 2 refreshes through it. Do not
  let the 3:30 session end without either a successful test refresh or a named
  owner and a due date on the request.
- **Do not demo what they cannot use.** No embedded Copilot, no Data Agent, no
  Lakehouse. Slides 15 and 16 exist to name these as future, not to demo them. A demo of
  an unavailable capability reads as a sales pitch, not enablement.
- **M365 Copilot is fair game**, and slide 26 scopes it, including drafting DAX and
  Power Query M from schema you paste in. See
  [reference/copilot-in-power-bi.md](../reference/copilot-in-power-bi.md).

## Next
[Day 2 labs](../labs/README.md)
