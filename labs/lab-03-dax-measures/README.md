# Lab 3 - Practice DAX measures

**Day 2, 1:00 and 2:30** (`Labs 3 and 4, DAX measures`) - **Deck slide 21**
**Applies the Day 1 session:** `DAX foundations for Tableau users` (slide 5, 1:00)

**Scope:** In scope. Power BI Desktop plus **M365 Copilot** in a separate window.

> **Goal, from the deck.** Write the DAX your Tableau calcs used to do, using the
> patterns from Day 1.

This lab pairs. One person drives Power BI Desktop, the other drives M365
Copilot and hands DAX across. Swap halfway.

## Why this matters
Deck slide 12 maps Tableau calculations to DAX, and names three golden rules:
**measures not columns**, **learn CALCULATE first**, **always use DIVIDE**.
Everything below is those three rules applied to your own data.

The harder shift is conceptual. A Tableau table calculation operates on the
result set in the view. A DAX measure is evaluated inside a filter context that
the visual creates. Same intent, completely different mechanics - which is why
generated DAX that *looks* right is so often wrong at a different grain.

---

## How to use M365 Copilot in this lab

M365 Copilot **cannot see your model**. It has no idea what your tables are
called. So the loop is:

1. **Context** - paste the schema block below.
2. **Ask** - state the measure in business terms.
3. **Read** - if you cannot explain the DAX, do not use it.
4. **Paste** - into Power BI Desktop.
5. **Verify at three grains** - total, by service, by month.

Step 5 is the one people skip, and it is the one that catches the errors.

### Your schema block

Save this. Paste it at the top of every Copilot prompt in this lab and Lab 4.

```
I am writing DAX for a Power BI semantic model in Import mode. Star schema:

FACT
  fact_incident(incident_key, incident_number, date_key, ci_key, service_key,
                team_key, location_key, severity_key, opened_at, resolved_at,
                incident_state, category, contact_type, time_to_resolve_minutes,
                reassignment_count, reopened_flag, sla_met_flag,
                major_incident_flag, incident_count)

DIMENSIONS (all one-to-many, single direction, filtering the fact)
  dim_date(date_key, date, year, quarter, month, month_name, month_year,
           day_of_week, is_weekend, week_of_year)
  dim_service(service_key, service_id, service_name, service_tier, business_unit)
  dim_configuration_item(ci_key, ci_id, ci_name, ci_type, environment, criticality)
  dim_team(team_key, team_id, team_name, assignment_group, shift_coverage)
  dim_location(location_key, site_name, city, state_province, region, datacenter)
  dim_severity(severity_key, severity_code, severity_name, priority,
               sla_target_hours, severity_sort)

dim_date is marked as the date table on [date].

Existing measures: Total Incidents

Rules: reuse existing measures rather than re-aggregating columns. Use DIVIDE for
any division. Prefer measures over calculated columns. Return only the DAX plus a
short explanation of the filter context.
```

Adjust the fact table for your group. Groups 2 to 5 swap in `fact_capacity`,
`fact_mainframe`, `fact_service_desk` or `fact_asset`.

> **Never paste real Schwab data, credentials, or ticket contents into Copilot.**
> You are pasting *schema and code*, never rows.

---

## Steps

### 1. Build the base measures first
Everything else composes from these. Write them by hand - they are short, and
you need the muscle memory.

```DAX
Total Incidents = COUNTROWS(fact_incident)

Resolved Incidents =
CALCULATE(
    [Total Incidents],
    NOT ISBLANK(fact_incident[resolved_at])
)

Avg Resolve Minutes = AVERAGE(fact_incident[time_to_resolve_minutes])
```

- Check each on a card before moving on.
- Note that `Resolved Incidents` uses `CALCULATE` to modify filter context. That
  is the function deck slide 12 tells you to learn first, and this is the
  simplest possible example of it.

### 2. Percent of total - the Tableau quick table calc
Deck slide 21 reference pattern:

```DAX
Percent of Total Incidents =
DIVIDE(
    [Total Incidents],
    CALCULATE([Total Incidents], ALL(dim_service))
)
```

- Put it in a table with `dim_service[Service]`. The column should sum to 100%.
- Now swap `ALL(dim_service)` for `ALLSELECTED(dim_service)` and slice by
  severity. Watch the denominator change. That difference is the whole lesson:
  `ALL` ignores every filter, `ALLSELECTED` respects what the user picked.
- **This is Tableau's "Percent of Total" quick table calc**, except you chose
  explicitly what it is a percent *of*. Tableau made that choice for you through
  "Compute Using"; DAX makes you say it.

### 3. Period over period
```DAX
Incidents PM =
CALCULATE(
    [Total Incidents],
    DATEADD(dim_date[date], -1, MONTH)
)

MoM Change % =
DIVIDE(
    [Total Incidents] - [Incidents PM],
    [Incidents PM]
)
```

- Format `MoM Change %` as a percentage with one decimal.
- Put `dim_date[month_year]`, `Total Incidents`, `Incidents PM` and `MoM Change %`
  in a table. The first month should be blank for the prior-month measures - that
  is correct, not a bug.
- If these return blank everywhere, `dim_date` is not marked as a date table.
  Go back to [Lab 1 step 3](../lab-01-semantic-model/README.md).

### 4. Running total
```DAX
Running Total Incidents =
CALCULATE(
    [Total Incidents],
    FILTER(
        ALLSELECTED(dim_date[date]),
        dim_date[date] <= MAX(dim_date[date])
    )
)
```

- Add it to your Lab 2 line chart as a second line.
- **Coming from Tableau:** this is the Running Sum table calc. Tableau computed
  it across the view; DAX computes it by expanding the filter context to all
  dates up to the current one. Read the `FILTER` inside out and it makes sense.

### 5. The measures your Lab 2 cards need
Now fill in the placeholder cards.

```DAX
SLA Met % =
DIVIDE(
    CALCULATE([Total Incidents], fact_incident[sla_met_flag] = TRUE()),
    [Resolved Incidents]
)

Major Incidents =
CALCULATE([Total Incidents], fact_incident[major_incident_flag] = TRUE())

Reopened Rate =
DIVIDE(
    CALCULATE([Total Incidents], fact_incident[reopened_flag] = TRUE()),
    [Total Incidents]
)
```

Other groups:

```DAX
-- Group 2, Capacity
CIs Over 80% CPU =
CALCULATE(
    DISTINCTCOUNT(fact_capacity[ci_key]),
    fact_capacity[cpu_utilization_pct] > 80
)

-- Group 3, Mainframe
MIPS Utilization % =
DIVIDE(SUM(fact_mainframe[mips_consumed]), SUM(fact_mainframe[mips_capacity]))

-- Group 4, Service Desk
First Contact Resolution % =
DIVIDE(
    SUM(fact_service_desk[first_contact_resolved]),
    SUM(fact_service_desk[tickets_resolved])
)

-- Group 5, Asset
Assets Out of Warranty =
CALCULATE([Total Assets], fact_asset[is_under_warranty] = FALSE())
```

> **M365 Copilot assist.** Now use Copilot for a measure you have *not* been
> given. Paste your schema block, then:
>
> *"Write a DAX measure for the average time to resolve, in hours, for major
> incidents only, excluding incidents that are still open. Explain the filter
> context."*
>
> Then **verify at three grains** before you keep it:
> - Total across the whole model
> - Split by `dim_service[Service]` - do the parts reconcile?
> - Split by `dim_date[month_year]` - is it sensible month to month?
>
> A measure that is right at the total and wrong by month is the classic failure
> mode, and it is invisible unless you look.

### 6. Break it on purpose
Worth ten minutes. It teaches more than five working measures.

- Run one of your prompts **without** the schema block. Copilot will invent table
  names. That contrast is why the block exists.
- Ask Copilot for "percent of total" without saying what it should be a percent
  of. Notice it picks for you - and picks differently than you would have.
- Write a deliberately wrong measure using a column instead of a measure:
  `DIVIDE(SUM(fact_incident[incident_count]), COUNTROWS(fact_incident))`. Look at
  what it does across grains.
- Take a measure Copilot produced, paste it back and ask *"what would make this
  measure return the wrong number?"* The answers are usually worth knowing.

### 7. Review filter context together
Deck slide 21: `Review the DAX and fix filter context together.`

As a table, put every measure into one matrix:
- Rows: `dim_service[Service]`
- Columns: `dim_severity[Severity]`
- Values: all your measures

Then check:
- Do percentages sum the way you expect at each level?
- Does the grand total make sense, or is it the sum of ratios? Averaging a ratio
  instead of recalculating it at the total is the most common reporting error in
  any domain, and it hides in plain sight.
- Does anything go blank where it should be zero, or zero where it should be
  blank?

Walk one measure through out loud with your pair, inside-out. If neither of you
can narrate it, do not ship it.

## You'll know it worked when
- Base measures, percent of total, period over period, and a running total all
  return numbers you have checked.
- Your Lab 2 KPI cards are populated with real measures.
- Every measure uses `DIVIDE` for division.
- No calculated columns were added.
- You used M365 Copilot for at least one measure and validated it at three grains.
- You can name one thing Copilot got wrong, and explain how you caught it.
- You can narrate what `CALCULATE` is doing in at least two of your measures.

## Next
[Lab 4 - Connect, shape, and load with Power Query](../lab-04-power-query/README.md)
