# M365 Copilot for Power BI work

> **Scope.** The only AI in this workshop is **Microsoft 365 Copilot**, used in a
> separate window as a drafting assistant, with a copy-and-paste handoff into
> Power BI Desktop. Copilot **inside Power BI Desktop or the Power BI Service**,
> Copilot Studio, and Fabric Data Agents are **not available** to this audience.
> They are not demoed and not required by any lab. See
> [schwab-current-state.md](schwab-current-state.md).

M365 Copilot cannot see your semantic model, your data, or your queries. Treat it
as a fast colleague who knows DAX and Power Query M well but has never seen your
work. That one fact drives everything below: **the quality of the output is the
quality of the context you supply.**

## What it can and cannot do

| Task | M365 Copilot | Notes |
| --- | --- | --- |
| Explain a DAX measure you paste in | Yes | The best entry point. Excellent for teaching filter context to Tableau users. |
| Convert a Tableau calculated field or LOD to DAX | Yes | Supply your table and column names or it will invent them. |
| Draft a new DAX measure | Yes | Then test it at three grains before keeping it. |
| Draft Power Query M | Yes | Then verify row counts, nulls, types and folding. |
| Debug an M or DAX error | Yes | Paste the code and the exact error text together. |
| Draft measure and table descriptions | Yes | Review each one for I&O accuracy. |
| Draft model documentation | Yes | Feed it your table and measure list. |
| Draft report requirements from meeting notes | Yes | Deck slide 24 lists this as an in-scope use. |
| See your model schema | **No** | You describe it in every prompt. |
| Run DAX and return real numbers | **No** | Every number it produces is invented. |
| Build a report page or place visuals | **No** | You build the page. |
| Read your data | **No** | And it must not. See below. |

**Data handling rule.** You paste **schema, code, column names and business
definitions**. You never paste rows, credentials, connection strings, ticket
contents, incident descriptions, user names, or anything from a production
system. Synthetic example rows for shape are fine. This is not a guideline, it is
the condition on which the tool is used.

## The copy-paste loop

1. **Context.** Paste the schema block below.
2. **Ask.** State the business question and the single artifact you want back.
3. **Read.** If you cannot explain the output line by line, do not use it.
4. **Paste.** DAX into the measure editor or DAX query view. M into the Power
   Query **Advanced Editor**.
5. **Verify.** DAX at three grains. M for rows, nulls, types and folding.
6. **Name it.** Rename generated Power Query steps so a colleague can read them.

Step 5 is the one people skip, and it is the one that catches the errors.

## The schema block

Write this once, save it where the team can reach it, and paste it at the top of
every prompt. It is the difference between usable output and invented table
names. This is the ITSM version; swap the fact table for your group's.

```
I am writing DAX for a Power BI semantic model in Import mode.
The model is a star schema for Charles Schwab Infrastructure & Operations.

Fact table (grain: one row per incident):
  fact_incident(
    incident_key, incident_number, date_key, ci_key, service_key, team_key,
    location_key, severity_key, opened_at, resolved_at, incident_state,
    category, contact_type, time_to_resolve_minutes, reassignment_count,
    reopened_flag, sla_met_flag, major_incident_flag, incident_count )

Conformed dimensions:
  dim_date(date_key, date, year, quarter, month, month_name, month_year,
           day_of_month, day_of_week, day_name, is_weekend, week_of_year,
           fiscal_year, fiscal_quarter)
  dim_service(service_key, service_id, service_name, service_tier, business_unit)
  dim_configuration_item(ci_key, ci_id, ci_name, ci_type, environment,
                         criticality, service_key, location_key, support_group)
  dim_team(team_key, team_id, team_name, assignment_group, shift_coverage)
  dim_location(location_key, location_id, site_name, city, state_province,
               country, region, datacenter)
  dim_severity(severity_key, severity_code, severity_name, priority,
               sla_target_hours, severity_sort)

dim_date is marked as the date table on dim_date[date].
All relationships are one-to-many, single direction, dimension filtering fact.

Existing measures:
  Total Incidents, Resolved Incidents, Avg Resolve Minutes, SLA Met %,
  Major Incidents, Reopened Rate, Incidents PM, MoM Change %,
  Incidents PY, YoY Change %, Running Total Incidents

Rules:
- Reuse the existing measures. Do not re-aggregate the underlying columns.
- Use DIVIDE for every division.
- Return one measure at a time, with a comment explaining the filter context.
```

For the other domain groups, replace the fact table block:

```
fact_capacity(date_key, ci_key, service_key, location_key,
  cpu_utilization_pct, memory_utilization_pct, storage_allocated_gb,
  storage_used_gb, headroom_pct)                    -- one row per CI per month

fact_mainframe(date_key, ci_key, location_key, mips_consumed, mips_capacity,
  batch_jobs_completed, batch_jobs_failed, batch_window_minutes,
  transactions_processed)                           -- one row per LPAR per day

fact_service_desk(date_key, team_key, location_key, tickets_received,
  tickets_resolved, first_contact_resolved, calls_abandoned, agents_scheduled,
  agents_available, avg_handle_time_minutes,
  avg_speed_to_answer_seconds)          -- one row per team per location per day

fact_asset(asset_key, asset_tag, ci_key, service_key, location_key,
  purchase_date, warranty_end_date, lifecycle_status, acquisition_cost_usd,
  annual_support_cost_usd, is_under_warranty, cmdb_complete_flag,
  asset_count)                                             -- one row per asset
```

## Prompt patterns that work

| Pattern | Example |
| --- | --- |
| Lead with the schema block | Paste it first, every time. Without it, every table name is a guess. |
| Explain before you generate | "Explain what the filter context is doing in this measure, line by line." |
| Name the measures to reuse | "Use the existing Total Incidents measure. Do not re-aggregate incident_count." |
| Give it the Tableau original | "Here is the Tableau LOD. Convert it to DAX and flag anything that will not translate cleanly." |
| Ask for one artifact | "Return a single DAX measure" or "Return one let expression I can paste into Advanced Editor." |
| State the grain | "fact_capacity is one row per CI per month. The measure must not sum a percentage." |
| Supply synthetic sample rows for M | Three fake rows tell it more about shape than a paragraph does. |
| Debug with the exact error | Paste the code and the full error text together, unedited. |
| Ask for the validation too | "Give me a DAX query I can run to tie this out by month and by service." |
| Ask what it assumed | "List the assumptions you made about my model." Often the fastest way to find the bug. |

Anti-patterns: asking for five measures at once, asking without the schema block,
and accepting the first answer because it compiles.

## Validating generated DAX

Compiling is not correct. Check the number at **three grains**, every time.

```DAX
// 1. Total. Does the grand total match what you expect?
EVALUATE
ROW(
    "Total Incidents", [Total Incidents],
    "SLA Met %",       [SLA Met %]
)

// 2. By service. Do the parts sum to the total?
EVALUATE
SUMMARIZECOLUMNS(
    dim_service[service_name],
    "Total Incidents", [Total Incidents],
    "SLA Met %",       [SLA Met %]
)
ORDER BY [Total Incidents] DESC

// 3. By month. Does it behave at period boundaries?
EVALUATE
SUMMARIZECOLUMNS(
    dim_date[year],
    dim_date[month_name],
    "Total Incidents",  [Total Incidents],
    "Incidents PM",     [Incidents PM],
    "MoM Change %",     [MoM Change %]
)
ORDER BY dim_date[year], dim_date[month_name]
```

Three failures this catches, all of which look fine on a card:

- Right at the total, wrong by service. Usually a missing or misdirected filter.
- Right by service, wrong by month. Usually missing time intelligence, or an
  unmarked date table.
- A percentage that does not sum to 100 across a column. Usually `ALL` where
  `ALLSELECTED` was meant, or the reverse.

More queries in [`src/sql/sample_dax_queries.dax`](../src/sql/sample_dax_queries.dax).

## Validating generated Power Query M

After pasting into Advanced Editor, check all five:

| Check | How | Why it matters |
| --- | --- | --- |
| Row count | Compare before and after the new steps | Generated M silently drops rows on a bad join or filter more often than it errors. |
| Nulls | Scan the column quality bar for new nulls | A type mismatch usually produces nulls, not an error. |
| Explicit types | Every affected column has a type set | Generated M frequently omits `Table.TransformColumnTypes`. Untyped columns break relationships and measures later. |
| Query folding | Right-click the last step, look for **View Native Query** | Generated M often breaks folding and turns a two-minute refresh into a twenty-minute one. |
| Step names | Rename `Custom1`, `Filtered Rows2` and friends | The next person to open this has to read it. |

If the generated M is longer than the click-path would have been, use the
click-path.

## What this is for, and what it is not

In scope, from deck slide 24:

- **Draft requirements.** Turn meeting notes into a report requirements list.
- **Summarize notes.** Condense a workshop or stakeholder session.
- **Refine communications.** Tighten a rollout email or a change announcement.
- **Draft DAX and M**, given your schema, then verified by you. Labs 3 and 4 both
  use this.

Not in scope:

- It cannot see, query, or validate your model. Every number it states is
  invented.
- It is not a substitute for Copilot inside Power BI Desktop or the Service,
  which this audience does not have.
- It does not build report pages or place visuals.
- It does not replace review. Code you cannot explain does not ship.

## Note for the deck, slide 24

Slide 24 currently lists this bullet under **What this is not**:

> Does not draft DAX or write report visuals for you

The first half of that bullet is inaccurate. M365 Copilot drafts DAX and Power
Query M well when you give it schema context, and **Labs 3 and 4 both rely on
that**. The second half is correct: it does not build visuals.

Suggested replacement bullets, ready to paste into the slide:

- Drafts DAX and M when you paste in your schema, but cannot see your model or
  run queries
- Not a substitute for Copilot inside Power BI Desktop or the service

Keep the rest of the slide as it stands.

## Guardrails

- Never paste real data, credentials, connection strings, or ticket contents.
- Never accept generated DAX without testing it at three grains.
- Never accept generated M without checking rows, nulls, types and folding.
- Never commit code you cannot explain to a colleague.
- Route anything entering a certified `sm_io_<domain>` model through the model
  owner.
- Every number Copilot states about your data is invented. Verify in Power BI.

## Why model quality still matters

Everything that makes a model good also makes it describable, and a describable
model is one Copilot can help with.

| Model preparation | Why it matters |
| --- | --- |
| Use a star schema | A star fits in a paragraph. A wide extract does not. |
| Hide technical columns | Nobody should see `severity_key` or `date_key`. |
| Use friendly names | "Service Name" is better than `service_name`. |
| Add measure descriptions | They become the definitions you paste into prompts. |
| Define each measure once | One right answer for Copilot to reference. |
| Set data categories | Dates and geography behave better in visuals. |
| Remove ambiguous duplicates | Two fields with one meaning produce two wrong answers. |

## Related

- [Current state and constraints](schwab-current-state.md)
- [Star schema](star-schema.md)
- [Tableau to Power BI](tableau-to-powerbi.md)
- [Power Query snippets](../src/powerquery/README.md)
- [Sample DAX queries](../src/sql/sample_dax_queries.dax)
- [Lab 3 - Practice DAX measures](../labs/lab-03-dax-measures/README.md)
- [Lab 4 - Power Query](../labs/lab-04-power-query/README.md)
- [Sources](sources.md)
