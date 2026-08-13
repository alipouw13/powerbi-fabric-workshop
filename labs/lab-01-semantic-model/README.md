# Lab 1 - Build the semantic model

**Day 2, 1:00** (`Labs 1 and 2, model & report`) - **Deck slide 22**
**Applies the Day 1 session:** `Data modeling and star schema` (slide 5, 11:15)
**Copilot agent:** Model Architect (tab 2 from [Day 1 setup](../day-1-setup/README.md#6-meet-m365-copilot-then-build-your-four-agents))

**Scope:** In scope. Power BI Desktop, Import mode. No Lakehouse, no Direct Lake.

> **Goal, from the deck.** Turn your current source extract into a star-schema semantic
> model with relationships and a first measure.

Get this lab right and Labs 2 and 3 are straightforward. Get it wrong and you will
spend Day 3 explaining why two reports disagree.

## Why this matters
Deck slide 6 names the one shift that matters: *Tableau blends data inside each workbook.
Power BI models data once, then every report reuses it.* You are not building a report
yet - you are building the thing every report will sit on.

## What you'll build
- An Import-mode star schema: your fact table joined to the conformed dimensions
- A marked date table
- A clean field list with the keys hidden
- Your first measure, validated against the source
- A published model that refreshes through the gateway

## Prerequisites
- [Lab 0](../lab-00-connect-and-shape/README.md) complete - you will reuse its habits on
  every query you load here
- `data\raw\sql\` generated, or access to your own source
- Reference: [star schema patterns](../../reference/star-schema.md), [Copilot agents](../../reference/copilot-agents.md)

> **Start a clean file.** Lab 0 was the Power Query practice file. This is the model, and
> it reads the already-conformed tables in `data\raw\sql\` rather than the wide Tableau
> extract. What carries over from Lab 0 is the discipline: filter and remove columns first,
> set every data type explicitly, and turn **Enable load** off for anything that is
> scaffolding.

---

## The model you are building

From deck slides 9 and 10. Every group builds the same shape, with a different fact table
in the middle.

```
                    dim_date
                        |
  dim_service ---  FACT (your domain)  --- dim_team
                    /       |       \
       dim_configuration_item  |   dim_location
                        dim_severity
```

| Group | Your fact table | One row is one... |
| --- | --- | --- |
| 1 ITSM & Operations | `fact_incident` | incident |
| 2 Capacity & Forecasting | `fact_capacity` | configuration item, per month |
| 3 Mainframe Analytics | `fact_mainframe` | LPAR, per day |
| 4 Service Desk & Workforce | `fact_service_desk` | service, per team, per location, per day |
| 5 Asset & Workplace Services | `fact_asset` | asset |

Being able to say your grain in one sentence is the test of whether you understand your
fact table. If you cannot, stop and work it out before building relationships.

**Every fact carries `service_key`**, which is what lets all five groups slice by
`dim_service[business_unit]` - Banking or Capital Markets - and get numbers that
reconcile. That is the payoff of conformed dimensions, and it is the thing to protect in
this lab.

---

## Steps

### 1. Load the tables
- **Get data** → **Text/CSV** (or **SQL Server** if you are using your own source).
- Load your fact table plus the dimensions it actually joins to:

| Group | Load these dimensions |
| --- | --- |
| 1 ITSM | all six |
| 2 Capacity | `dim_date`, `dim_service`, `dim_configuration_item`, `dim_location` |
| 3 Mainframe | `dim_date`, `dim_service`, `dim_configuration_item`, `dim_location` |
| 4 Service Desk | `dim_date`, `dim_service`, `dim_team`, `dim_location` |
| 5 Asset | `dim_service`, `dim_configuration_item`, `dim_location`, and `dim_date` *(see note)* |

- Choose **Import**. Deck slide 11: `Prefer Import mode for now`.
- Save as `sm_io_<yourdomain>.pbix`, for example `sm_io_itsm.pbix`.

> **Group 5, you have a real modeling decision.** `fact_asset` has **no `date_key`**. It
> is a snapshot of the estate, not a stream of events, so there is no single date that
> describes a row - there is `purchase_date` and `warranty_end_date`. You have two honest
> options: relate `dim_date[date]` to `fact_asset[purchase_date]` and accept that all time
> intelligence then means "by purchase date", or load no date dimension and answer your
> questions with `TODAY()`-based measures instead. Decide as a group, write down which you
> chose and why, and say it out loud at the stand-up. Facts without a natural date are
> common and this is the right conversation to have about them.

> **Do not** load `incident_report_extract.csv` here. That wide file is the Tableau
> "before" you took apart in [Lab 0](../lab-00-connect-and-shape/README.md), and its
> carved-out dimensions live in that practice file. Loading them alongside the
> `data\raw\sql\` dimensions would give you two `dim_service` tables and an argument about
> which is right.

### 2. Create the relationships, then hide the keys
Model view → drag key to key, or **Manage relationships** → **New**.

Relate your fact to **every dimension you loaded**, on the matching `_key` column. For
`fact_incident` that is six relationships:

| From | To | Cardinality | Direction |
| --- | --- | --- | --- |
| `dim_date[date_key]` | `fact_incident[date_key]` | One to many | Single |
| `dim_service[service_key]` | `fact_incident[service_key]` | One to many | Single |
| `dim_configuration_item[ci_key]` | `fact_incident[ci_key]` | One to many | Single |
| `dim_team[team_key]` | `fact_incident[team_key]` | One to many | Single |
| `dim_location[location_key]` | `fact_incident[location_key]` | One to many | Single |
| `dim_severity[severity_key]` | `fact_incident[severity_key]` | One to many | Single |

Rules, from deck slide 11:
- **Single-column integer keys.** All the `_key` columns already are.
- **One-to-many, single direction**, dimension filtering fact. Always.
- **Avoid bidirectional by default.** If a visual seems to need it, the model is usually
  wrong somewhere else.
- A dotted line means Power BI found ambiguity and made the relationship inactive.
  Resolve it rather than leaving it.

> **The one modeling decision in this lab.** `dim_configuration_item` also carries
> `service_key` and `location_key`. Do **not** relate those. The fact table is the only
> thing that joins to dimensions; relating them too gives Power BI two paths to the same
> filter and it will refuse, or worse, pick one. This is the snowflake-versus-star
> tradeoff from Day 1, and here the answer is star.

Now hide the plumbing, while you are still in Model view. Deck slide 22: `Hide keys and
technical columns immediately, before you build a single visual.`

- Right-click each `_key` column → **Hide in report view**, on both sides.
- Hide anything a report author will never drag onto a canvas.
- Keep `incident_number` visible - people genuinely search on it.
- Rename to business labels: `service_name` → `Service`, `business_unit` → `Business
  Unit`, `severity_name` → `Severity`, `time_to_resolve_minutes` → `Time to Resolve
  (Minutes)`.

A field list a business user can read without a translator is the difference between a
model people adopt and one they work around.

### 3. Mark the date table
Every group except group 5, and group 5 too if you chose to relate `dim_date` to
`purchase_date`.

- Select `dim_date` → **Table tools** → **Mark as date table**.
- Choose the `date` column, **not** `date_key`.
- Power BI validates it: unique, no blanks, contiguous days.

Skip this and every time-intelligence measure in Lab 3 will either fail or silently
return the wrong number. Thirty seconds of work; an entire category of bug prevented.

### 4. Sort severity properly
Only groups that loaded `dim_severity`.

Select `dim_severity[severity_name]` → **Sort by column** → `severity_sort`. Severity now
sorts Critical, High, Moderate, Low instead of alphabetically. Do this in the model once,
and every visual in every report inherits it.

### 5. Add your first measure
One measure, now, before any calculated columns. Deck slide 22: `Create your first
measure before adding any calculated columns.`

```DAX
Total Incidents = COUNTROWS(fact_incident)
```

Or for your domain:

```DAX
-- Group 2, Capacity
Avg CPU Utilization = AVERAGE(fact_capacity[cpu_utilization_pct])

-- Group 3, Mainframe
Total MIPS Consumed = SUM(fact_mainframe[mips_consumed])

-- Group 4, Service Desk
Tickets Received = SUM(fact_service_desk[tickets_received])

-- Group 5, Asset
Total Assets = COUNTROWS(fact_asset)
```

- Put it in a dedicated `_Measures` table so it does not get lost among columns.
- Format it: whole number with a thousands separator, or one decimal for a percentage.
- Drop it on a card and sanity-check the number against the source.

> ### Model Architect assist
> Switch to your Model Architect tab. You already pasted the model card during
> [Day 1 setup](../day-1-setup/README.md), so ask
> directly:
>
> *"Restate my fact table's grain in one sentence. Then tell me which measures are safe to
> SUM at that grain and which would mislead if I summed them, and why."*
>
> This is a better first question than "write me a measure", because the answer tells you
> something about your data that you will need in Lab 3. Group 3 should get a warning
> about `mips_capacity` repeating daily; group 2 about summing percentages; group 4 about
> the staffing columns being per-service allocations rather than headcount.
>
> Then paste your measure back and ask *"what would make this return the wrong number?"*

### 6. Validate before you build anything on it
Five minutes here saves an hour on Day 3.

- Drop your measure on a card. Does it match a `COUNT(*)` against the source?
- Add `dim_service[Business Unit]` to a table with the measure. You should see exactly
  two rows, **Banking** and **Capital Markets**, and they should sum to the card total.
- Add `dim_service[business_domain]`, then `dim_service[Service]`. Each level should still
  sum back to the total. That three-level hierarchy is what your Lab 2 report will drill.
- Add `dim_date[month_year]`. Is every month present, with no blank row? *(Group 5: only
  if you related `dim_date` to `purchase_date` - otherwise skip this one.)*
- A **blank row** in a dimension means referential integrity is broken: the fact has a key
  the dimension does not. Find it now, not on Day 3.

> **If you finish early**, switch one relationship to bidirectional, look at what changes
> in the business-unit table, then switch it back. Understanding why it is wrong beats
> being told. Skip this if the room is still working - it is a bonus, not a step.

### 7. Publish and prove the refresh through the gateway
Lab 0 left you with a Desktop refresh time. Now prove the same thing happens unattended,
because a model that only refreshes on your laptop has not been migrated.

- **Publish** to the workspace you confirmed in
  [Day 1 setup step 3](../day-1-setup/README.md#3-confirm-your-workspace).
- In the service, open the semantic model → **Settings** → **Gateway and cloud
  connections**, and bind it to the connection you proved in
  [Day 1 setup step 4](../day-1-setup/README.md#4-prove-the-gateway-path-end-to-end).
- **Refresh now.** Time it, and compare with the Desktop baseline from
  [Lab 0 step 6](../lab-00-connect-and-shape/README.md#6-load-only-what-a-model-will-need).
  If it is dramatically slower, a fold you were relying on is breaking on the gateway.
- Set the schedule **after** the upstream job lands, not on the hour out of habit. Send
  failure notifications to a group mailbox, not a person.

> **CSV-sourced groups:** the gateway needs a path it can reach, so a file on your desktop
> will fail here. Either point at a share the gateway machine can see, or note the failure,
> read the reason in the error, and move on - understanding *why* it fails is the learning.

## You'll know it worked when
- The model diagram is a star: one fact in the middle, dimensions around it, no
  dimension-to-dimension joins.
- Every relationship is one-to-many, single direction.
- `dim_date` is marked as the date table on `date`.
- No `_key` column is visible in report view.
- Slicing by `Business Unit` gives exactly two rows that sum to the total.
- Your first measure returns a number you have checked against the source.
- You can state your fact table's grain in one sentence.
- The model is published, bound to the gateway, and has refreshed - or you can say
  precisely why it did not.

## Next
[Lab 2 - Build your first report page](../lab-02-report-page/README.md)
