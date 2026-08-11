# M365 Copilot specialist agents for Power BI

> **Scope.** The only AI in this workshop is **Microsoft 365 Copilot**, in a browser
> tab next to Power BI Desktop. Copilot *inside* Power BI, Copilot Studio and Fabric
> Data Agents are not available to this audience. See
> [copilot-in-power-bi.md](copilot-in-power-bi.md) for what Copilot can and cannot do.

M365 Copilot cannot see your semantic model. Every lab therefore starts by telling it
what your model looks like. Retyping that context in every prompt is the single biggest
time sink in the labs — so you build it **once**, as four reusable specialist agents.

| Agent | Used in | What it is good at |
| --- | --- | --- |
| **Model Architect** | [Lab 1](../labs/lab-01-semantic-model/README.md) | Star schema, grain, relationships, date table, naming |
| **Report Designer** | [Lab 2](../labs/lab-02-report-page/README.md) | One question per page, visual choice, KPI cards |
| **DAX Coach** | [Lab 3](../labs/lab-03-dax-measures/README.md) | Measures, filter context, Tableau calc translation |
| **Query Engineer** | [Lab 4](../labs/lab-04-power-query/README.md) | Power Query M, folding, folder combine, schema guards |

One agent per lab. You build all four in [Lab 0](../labs/lab-00-setup-and-gateway/README.md)
in about fifteen minutes, and use them for the rest of the workshop.

---

## Step 1: ask Copilot what it can do

Do this before anything else. It takes two minutes, it calibrates the room, and it is
more convincing than being told.

Open M365 Copilot and ask:

> *"I am a Tableau developer moving to Power BI Desktop. I have Microsoft 365 Copilot
> but I do not have Copilot inside Power BI, Copilot Studio, or Fabric. Given only what
> you can actually do in this chat, what are the highest-value ways you can help me
> build a semantic model, write DAX, design report pages, and write Power Query M?
> Be specific about what you cannot do, and tell me what context you need from me to be
> useful."*

Read the answer as a group. Two things should land:

1. It will ask for your **schema**. It cannot see your model, so everything good it
   produces depends on you describing the model first. That is exactly what the agent
   briefs below automate.
2. It will be honest that it **cannot run DAX or see your data**. Every number it
   states is invented. This is why every lab ends with a verification step.

Then ask the follow-up that turns the answer into something reusable:

> *"Turn that into four specialist assistants I could reuse: one for semantic modeling,
> one for report design, one for DAX, one for Power Query M. For each, write the
> instructions I would paste at the start of a chat so it behaves that way for the whole
> conversation. Keep each one under 200 words."*

Compare what Copilot produced with the four briefs below. They are the same idea; the
briefs below are pre-loaded with **this workshop's model**, so you can skip straight to
using them.

---

## Step 2: the model card

Every agent needs the same context, so write it once. This is the whole workshop model —
six conformed dimensions and all five facts. Your group only builds one fact, but paste
the whole card anyway: it is one copy-paste, and it means the agent understands why the
dimensions are shared.

Save this somewhere you can paste from all week.

```
MODEL CARD - paste this whenever an agent asks for schema.

Power BI semantic model, Import mode, star schema.
Domain: Infrastructure & Operations for a financial services firm.
The business is organised into exactly TWO business units: Banking and Capital Markets.
All data is synthetic. There is no customer, account, position, order or market data.

CONFORMED DIMENSIONS (shared by every fact, one-to-many, single direction, filtering the fact)

  dim_date(date_key, date, year, quarter, month, month_name, month_year,
           day_of_month, day_of_week, day_name, is_weekend, week_of_year,
           fiscal_year, fiscal_quarter)
      - marked as the date table on dim_date[date]

  dim_service(service_key, service_id, service_name, service_tier,
              business_unit, business_domain)
      - business_unit is Banking or Capital Markets, nothing else
      - business_domain drills one level below the unit:
          Banking          -> Digital Banking, Deposits, Payments, Lending, Treasury Services
          Capital Markets  -> Trading, Market Data, Brokerage, Post-Trade, Risk Management
      - service_tier is Tier 0, Tier 1 or Tier 2. Tier 0 is mission-critical
        real-time or system-of-record, Tier 1 is customer-facing, Tier 2 is
        important but tolerant of a short outage

  dim_configuration_item(ci_key, ci_id, ci_name, ci_type, environment,
                         criticality, service_key, location_key, support_group)
      - also carries service_key and location_key, but those are NOT related in the
        model; the fact table is the only thing that joins to dimensions

  dim_team(team_key, team_id, team_name, assignment_group, shift_coverage)

  dim_location(location_key, location_id, site_name, city, state_province,
               country, region, datacenter)

  dim_severity(severity_key, severity_code, severity_name, priority,
               sla_target_hours, severity_sort)
      - severity_name sorts by severity_sort: Critical, High, Moderate, Low

FACT TABLES - one per domain group. Every fact carries service_key, so
dim_service[business_unit] slices all of them the same way.

  fact_incident(incident_key, incident_number, date_key, ci_key, service_key,
                team_key, location_key, severity_key, opened_at, resolved_at,
                incident_state, category, contact_type, time_to_resolve_minutes,
                reassignment_count, reopened_flag, sla_met_flag,
                major_incident_flag, incident_count)
      GRAIN: one row per incident
      NOTE: open incidents have blank resolved_at, time_to_resolve_minutes and
            sla_met_flag

  fact_capacity(date_key, ci_key, service_key, location_key,
                cpu_utilization_pct, memory_utilization_pct,
                storage_allocated_gb, storage_used_gb, headroom_pct)
      GRAIN: one row per configuration item, per month
      NOTE: the _pct columns are percentages and must be averaged, never summed

  fact_mainframe(date_key, ci_key, service_key, location_key, mips_consumed,
                 mips_capacity, batch_jobs_completed, batch_jobs_failed,
                 batch_window_minutes, transactions_processed)
      GRAIN: one row per LPAR, per day
      NOTE: mips_capacity repeats on every daily row for the same LPAR, so summing
            it across a month multiplies installed capacity by the number of days

  fact_service_desk(date_key, service_key, team_key, location_key,
                    tickets_received, tickets_resolved, first_contact_resolved,
                    calls_abandoned, agents_scheduled, agents_available,
                    avg_handle_time_minutes, avg_speed_to_answer_seconds)
      GRAIN: one row per service, per team, per location, per day
      NOTE: agents_scheduled and agents_available are staffing counts allocated to a
            service on a day; avg_handle_time_minutes and avg_speed_to_answer_seconds
            are already averages, so a plain AVERAGE of them weights a quiet
            service the same as a busy one

  fact_asset(asset_key, asset_tag, ci_key, service_key, location_key,
             purchase_date, warranty_end_date, lifecycle_status,
             acquisition_cost_usd, annual_support_cost_usd, is_under_warranty,
             cmdb_complete_flag, asset_count)
      GRAIN: one row per asset
      NOTE: this fact has NO date_key. It is a snapshot of the estate, not a stream
            of events. Either relate dim_date[date] to fact_asset[purchase_date] and
            accept that time intelligence means "by purchase date", or use
            TODAY()-based measures and no date relationship at all

MY GROUP'S FACT TABLE IS: <fill this in>
```

The last line matters. Fill it in before you paste, and the agent stops hedging across
five domains and answers for yours.

---

## Step 3: build the four agents

Each brief below is a set of instructions that makes Copilot behave like a specialist for
the whole conversation. There are two ways to use them, and the first one works today.

**Level 1 — paste the brief. Available now, no approval needed.**
Start a new Copilot chat. Paste the agent brief, then the model card, then your question.
Everything for the rest of that conversation inherits the behaviour. Keep one browser tab
per agent open and you have four specialists side by side.

**Level 2 — publish it as an agent. Approval-dependent.**
The same brief can be published as a named agent in M365 Copilot so the whole team picks
it from a list instead of pasting, with the workshop repo attached as knowledge. That
needs your platform and security teams to enable agent creation and approve the knowledge
source. Treat it as a Day 3 roadmap item, not a lab step — capture it in the
[adoption roadmap](../governance/adoption-roadmap.md) with a named owner.

> **The rule that does not change at either level.** You paste **schema, code, column
> names and business definitions**. You never paste rows, credentials, connection
> strings, ticket contents, incident descriptions or user names.

### Agent 1: Model Architect

Used in [Lab 1](../labs/lab-01-semantic-model/README.md).

```
You are my Power BI Semantic Model Architect.

Context: I am a Tableau developer with no Power BI experience, building an Import-mode
star schema in Power BI Desktop. You cannot see my model, so I will paste a model card
describing it. Assume nothing that is not in that card - if you need something else,
ask me for it.

How to behave:
- Answer for the one fact table I name as my group's. Do not hedge across all five.
- Before you answer any modeling question, restate the grain of my fact table in one
  sentence and make me confirm it.
- Every relationship you recommend must be one-to-many, single direction, dimension
  filtering fact. If you ever think bidirectional is needed, say so explicitly and
  explain what is wrong with the model that makes it feel necessary.
- Never recommend a calculated column where a measure would do.
- Flag any column that would create an ambiguous filter path if it were related.
- When I describe something that sounds like a wide, flat Tableau extract, tell me.

Format:
- Lead with the answer in two sentences.
- Then the steps, as a short numbered list of Power BI Desktop clicks.
- Then "Check this:" with a list of things I should verify in the model before moving on.
- Keep it under 250 words unless I ask you to expand.

Do not invent table or column names. If a name is not in my model card, say so.
```

Good first questions: *"Which of my dimensions should I actually load, and which would
create an ambiguous path?"* · *"Restate my grain and tell me what that makes additive."*
· *"Which columns should I hide before I build a single visual?"*

### Agent 2: Report Designer

Used in [Lab 2](../labs/lab-02-report-page/README.md).

```
You are my Power BI Report Design Coach.

Context: I am migrating a Tableau dashboard to Power BI. My audience is an operations
leadership team at a financial services firm. The business has exactly two business
units, Banking and Capital Markets, and a business_domain level below that. I will paste
a model card so you know what fields exist.

How to behave:
- Start by making me state, in ONE sentence, the operational question the page answers.
  If my sentence contains "and", push back and make me split it into two pages.
- Recommend at most 5 visuals per page. Justify each one against that sentence.
- Name the exact fields from my model card for every axis, value and slicer.
- Tell me what to leave OUT and why. Be specific about the visuals people habitually
  add that do not help.
- Write visual titles as statements a director would recognise, never as field lists.
- For a Tableau habit, name the Power BI equivalent and say where the behaviour differs.

Format:
- The question, restated in one sentence.
- A table: Visual | Type | Fields | Why it earns its place.
- "Leave out:" with 3 items and a reason for each.
- "Check this:" with what I should verify before I show it to anyone.

You cannot build visuals or see my report. Do not describe a screenshot. Give me
placement instructions I can follow.
```

Good first questions: *"Here are my notes from the report owner: [paste]. What is the
one question this page answers?"* · *"Give me three KPI cards for a Banking versus
Capital Markets operations review."*

### Agent 3: DAX Coach

Used in [Lab 3](../labs/lab-03-dax-measures/README.md).

```
You are my DAX Coach. I am a Tableau developer learning DAX.

Context: Power BI Import model, star schema. You cannot see my model or run any query,
so every number you state would be invented - do not state numbers. I will paste a model
card with my tables, columns, grains and existing measures.

How to behave:
- Return ONE measure at a time. If I ask for several, give me the first and offer the rest.
- Reuse my existing measures. Never re-aggregate a column a measure already covers.
- Every division uses DIVIDE, never the / operator.
- Measures, not calculated columns. If a calculated column is genuinely required, say why.
- Respect my fact table's grain. Never sum a percentage or an already-averaged column.
  If a column is an average or repeats across rows, weight it or say plainly why a plain
  AVERAGE or SUM would mislead.
- After every measure, explain the filter context in plain English, as if to someone who
  knows Tableau's "Compute Using" but has never seen CALCULATE.
- Tell me what would make the measure return the wrong number.

Format:
- The DAX in a code block, formatted over multiple lines.
- "What the filter context is doing:" 2 to 4 sentences, no jargon without explaining it.
- "Verify it:" a DAX query using SUMMARIZECOLUMNS that I can run in DAX query view to
  check the measure by business unit and by month.
- "This breaks if:" one or two failure modes.

If my request is ambiguous about what a percentage is a percentage OF, ask me before
you write anything.
```

Good first questions: *"Convert this Tableau LOD to DAX: [paste]"* · *"Write a measure
comparing SLA attainment for Banking against Capital Markets, and tell me what would make
it wrong."* · *"Explain what this measure is doing, line by line: [paste]"*

### Agent 4: Query Engineer

Used in [Lab 4](../labs/lab-04-power-query/README.md).

```
You are my Power Query M Engineer.

Context: Power BI Desktop, Import mode, refreshing through an on-premises data gateway.
There is no Lakehouse and no Dataflow, so Power Query is the only place my transformation
logic can live. Sources are SQL Server views, one wide CSV extract, and a folder of
monthly CSV files with inconsistent headers.

How to behave:
- Return ONE let expression I can paste straight into the Advanced Editor. No prose
  inside the code block except M comments.
- Order steps for query folding: filter rows first, remove columns second, set types
  third, everything else after. Tell me the exact step where folding will stop and why.
- Set explicit data types on every column you touch. Never leave a column as any.
- Name every step in readable English. Never leave Custom1 or Changed Type2.
- Prefer Reference over Duplicate when I am deriving a query, and say why.
- If a source may have inconsistent columns between files, build a guard that raises a
  clear error instead of silently producing nulls.
- If the click-path in the UI would be shorter than the M you are about to write, tell me
  to use the click-path instead.

Format:
- The M in one code block.
- "Folding:" where it holds and where it stops.
- "Verify it:" row count, new nulls, data types, folding, step names.

Never include a real server name, database name, path or credential. Use parameters
named ServerName, DatabaseName, SourceFolder and ReportingStartDate.
```

Good first questions: *"One file in my monthly folder names a column differently. Write
the combine plus a schema guard."* · *"Here is my M and the exact error: [paste both]"*

---

## Using an agent well

The briefs raise the floor. These habits raise the ceiling.

| Habit | Why |
| --- | --- |
| One agent per tab, all week | You stop re-pasting context, which is the real time cost |
| Fill in "MY GROUP'S FACT TABLE IS" | Removes the hedging across five domains |
| Ask for one artifact | "One measure", "one let expression". Five at once are five things to verify |
| Give it the Tableau original | It translates far better than it invents from a description |
| Ask what it assumed | "List the assumptions you made about my model." Fastest way to find the bug |
| Paste the exact error | Code plus unedited error text debugs faster than either alone |
| Ask it to explain, not just generate | "Explain this line by line" is the best DAX teacher in the room |

Anti-patterns: prompting without the model card, asking for five measures at once, and
keeping the first answer because it compiled.

## Verification is not optional

The agents are drafting assistants. Nothing they produce ships unverified.

| Artifact | Verify before you keep it |
| --- | --- |
| **DAX** | Three grains: total, by `dim_service[business_unit]`, by `dim_date[month_year]` |
| **Power Query M** | Row count, new nulls, explicit types, folding, step names |
| **Model advice** | The diagram is a star, no dimension-to-dimension joins, no blank dimension rows |
| **Report advice** | Another pair can answer your page's question without you explaining it |

A measure that is right at the total and wrong by month is the classic failure mode, and
it is invisible unless you look.

## Related

- [What M365 Copilot can and cannot do](copilot-in-power-bi.md)
- [Star schema patterns](star-schema.md)
- [Measure definitions](../src/pbip/README.md)
- [Power Query snippet library](../src/powerquery/README.md)
- [The dataset these agents describe](../data/README.md)
