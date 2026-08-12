# Lab 3 - Practice DAX measures

**Day 2, 2:30** (`Lab 3, DAX measures`) - **Deck slide 24**
**Applies the Day 1 session:** `DAX foundations for Tableau users` (slide 5, 1:00)
**Copilot agent:** DAX Coach (tab 4 from [Day 1 setup](../day-1-setup/README.md#6-meet-m365-copilot-then-build-your-four-agents))

**Scope:** In scope. Power BI Desktop plus M365 Copilot in a separate window.

> **Goal, from the deck.** Write the DAX your Tableau calcs used to do, using the patterns
> from Day 1.

This lab pairs. One person drives Power BI Desktop, the other drives the DAX Coach tab and
hands DAX across. Swap halfway.

## Why this matters
Deck slide 12 maps Tableau calculations to DAX and names three golden rules: **measures
not columns**, **learn CALCULATE first**, **always use DIVIDE**.

The harder shift is conceptual. A Tableau table calculation operates on the result set in
the view. A DAX measure is evaluated inside a filter context the visual creates. Same
intent, completely different mechanics - which is why generated DAX that *looks* right is
so often wrong at a different grain.

## Prerequisites
- [Lab 1](../lab-01-semantic-model/README.md) and [Lab 2](../lab-02-report-page/README.md) complete
- Your DAX Coach tab open, primed with the model card and your fact table
- Reference: [measure definitions](../../src/pbip/README.md), [Copilot agents](../../reference/copilot-agents.md)

---

## Using the DAX Coach

Your agent tab already has the model card, so you can go straight to the question. The
loop is:

1. **Ask** in business terms.
2. **Read.** If you cannot explain the DAX, do not use it.
3. **Paste** into Power BI Desktop.
4. **Verify at three grains** - total, by business unit, by month.

Step 4 is the one people skip, and it is the one that catches the errors.

The brief already tells the agent to return one measure at a time, use `DIVIDE`, respect
your grain, and hand you a `SUMMARIZECOLUMNS` query to check the result. If it stops doing
those things, the conversation has drifted - start a fresh tab and paste the brief again.

> **Never paste rows, credentials or ticket contents into Copilot.** Schema and code only.

---

## Steps

### 1. Build the base measures
Everything else composes from these. Write them by hand - they are short, and you need the
muscle memory.

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
- `Resolved Incidents` uses `CALCULATE` to modify filter context. That is the function
  deck slide 12 tells you to learn first, and this is the simplest possible example.

### 2. Percent of total - and the choice Tableau made for you
Deck slide 24's reference pattern:

```DAX
Percent of Total Incidents =
DIVIDE(
    [Total Incidents],
    CALCULATE([Total Incidents], ALL(dim_service))
)
```

- Put it in a table with `dim_service[Business Unit]`. Two rows, and they should sum to
  100%.
- Now swap `ALL(dim_service)` for `ALLSELECTED(dim_service)` and click **Capital Markets**
  on your Lab 2 slicer. Watch the denominator change.

**That difference is the whole lesson.** `ALL` ignores every filter, so the percentages
stop summing to 100 once the reader slices. `ALLSELECTED` respects what the user picked, so
they always do. This is Tableau's "Percent of Total" quick table calc, except you choose
explicitly what it is a percent *of*. Tableau made that choice for you through "Compute
Using"; DAX makes you say it.

Pick one deliberately and write which, and why, into the measure description. Shipping both
without explaining the difference is how two pages end up disagreeing.

### 3. Time intelligence
Three measures, two patterns. All of them need `dim_date` marked as the date table - if
they return blank everywhere, go back to
[Lab 1 step 3](../lab-01-semantic-model/README.md#3-mark-the-date-table).

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

Running Total Incidents =
CALCULATE(
    [Total Incidents],
    FILTER(
        ALLSELECTED(dim_date[date]),
        dim_date[date] <= MAX(dim_date[date])
    )
)
```

- Format `MoM Change %` as a percentage with one decimal.
- Put `dim_date[month_year]`, `Total Incidents`, `Incidents PM` and `MoM Change %` in a
  table. The first month is blank for the prior-month measures - correct, not a bug.
- Add `Running Total Incidents` to your Lab 2 line chart as a second line.

> **Group 5**, these only work if you related `dim_date` to `fact_asset[purchase_date]` in
> Lab 1, and they then mean "by purchase date". If you chose no date relationship, skip
> this step and spend the time on step 4 instead - `Assets Expiring in 90 Days` is your
> time-based measure, and it uses `TODAY()` rather than the date table.

**Coming from Tableau:** the running total is the Running Sum table calc. Tableau computed
it across the view; DAX computes it by expanding the filter context to all dates up to the
current one. Read the `FILTER` inside out and it makes sense.

### 4. Fill in your Lab 2 cards
Now the placeholders get real measures.

```DAX
SLA Met % =
DIVIDE(
    CALCULATE([Total Incidents], fact_incident[sla_met_flag] = TRUE()),
    [Resolved Incidents]
)

Major Incidents =
CALCULATE([Total Incidents], fact_incident[major_incident_flag] = TRUE())
```

`SLA Met %` divides by **resolved** incidents, not all of them. An incident still open has
no SLA outcome yet, so including it in the denominator quietly drags the number down.
Deciding what a blank means is half of writing an honest measure.

Other groups - full definitions and descriptions are in
[`src/pbip/README.md`](../../src/pbip/README.md):

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

Three of these are ratios of two sums rather than averages of a ratio, and that is
deliberate. `MIPS Utilization %` works precisely because dividing two sums cancels the
daily repetition of `mips_capacity`. Averaging the per-row ratio would not.

> ### DAX Coach assist - the grain trap
> Ask your DAX Coach for a measure you have **not** been given:
>
> *"Write a measure for the average time to resolve, in hours, for major incidents only,
> excluding incidents that are still open. Explain the filter context, and tell me what
> would make it return the wrong number."*
>
> Then verify at three grains before you keep it:
> - **Total** across the whole model
> - By **`dim_service[Business Unit]`** - do Banking and Capital Markets sum back?
> - By **`dim_date[month_year]`** - is it sensible month to month?
>
> A measure that is right at the total and wrong by month is the classic failure mode, and
> it is invisible unless you look.
>
> **Group 4, ask this one instead - it is the sharpest lesson in the lab:**
> *"My fact is one row per service, per team, per location, per day. `agents_scheduled` is
> the agents allocated to one service on one day, and `avg_handle_time_minutes` is already
> an average. What goes wrong if I write `SUM(agents_scheduled)` and
> `AVERAGE(avg_handle_time_minutes)`, and what should I write instead?"*
>
> The answer should be that summing staffing counts the same agent once per service, and
> that averaging an average weights a quiet weekend the same as a peak trading morning.
> The corrected, volume-weighted measures are in
> [`src/pbip/README.md`](../../src/pbip/README.md#group-4-service-desk-and-workforce).

### 5. Review filter context together
Deck slide 24: `Review the DAX and fix filter context together.`

Build one matrix and put every measure in it:
- Rows: `dim_service[Business Unit]`, then drill to `business_domain`
- Columns: `dim_severity[Severity]`, or `dim_date[quarter]` if you have no severity
- Values: all your measures

Then check three things:
- Do percentages sum the way you expect at each level?
- Does the grand total make sense, or is it the sum of ratios? Averaging a ratio instead of
  recalculating it at the total is the most common reporting error in any domain, and it
  hides in plain sight.
- Does anything go blank where it should be zero, or zero where it should be blank?

Walk one measure through out loud with your pair, inside out. If neither of you can narrate
it, do not ship it.

> **Two minutes, worth it:** run one prompt in a **fresh** Copilot chat without the agent
> brief or the model card. It will invent table names. That contrast is the entire argument
> for setting the agents up on Day 1.

## You'll know it worked when
- Base measures, percent of total, time intelligence and your card measures all return
  numbers you have checked.
- Your Lab 2 KPI cards are populated.
- Every measure uses `DIVIDE` for division, and no calculated columns were added.
- You verified at least one Copilot-drafted measure at three grains, including by business
  unit.
- You can name one thing Copilot got wrong and explain how you caught it.
- You can narrate what `CALCULATE` is doing in at least two of your measures.

## Next
Day 2 closes with the 4:00 stand-up. Bring: what you built, what broke, one thing you would
tell the other groups, and your Lab 2 page for peer review.

Day 3 is [showcase and next steps](../../sessions/day-3-showcase.md).
