# Lab 1 - Build the semantic model

**Day 2, 10:30** (`Labs 1 and 2, model and report`) - **Deck slide 19**
**Applies the Day 1 session:** `Data modeling and star schema` (slide 5, 11:15)

**Scope:** In scope. Power BI Desktop, Import mode. No Lakehouse, no Direct Lake.

> **Goal, from the deck.** Turn your current source extract into a star-schema
> semantic model with relationships and a first measure.

This is the lab that makes every later lab possible. Get the model right and
Labs 2, 3 and 4 are straightforward. Get it wrong and you will spend Day 3
explaining why two reports disagree.

## Why this matters
Deck slide 6 names the one shift that matters: *Tableau blends data inside each
workbook. Power BI models data once, then every report reuses it.* This lab is
where that shift becomes real. You are not building a report yet - you are
building the thing every report will sit on.

## What you'll build
- An Import-mode semantic model from your domain's source data
- A star schema: your fact table joined to the six conformed dimensions
- A marked date table
- Hidden keys and a clean field list
- Your first measure

## Prerequisites
- [Lab 0](../lab-00-setup-and-gateway/README.md) complete
- `data\raw\sql\` generated, or access to your own source
- Reference: [star schema patterns](../../reference/star-schema.md), [Tableau to Power BI](../../reference/tableau-to-powerbi.md)

---

## The model you are building

From deck slides 9 and 10. Every group builds the same shape, with a different
fact table in the middle.

```
                    dim_date
                        |
  dim_service ---  FACT (your domain)  --- dim_team
                    /       |       \
       dim_configuration_item  |   dim_location
                        dim_severity
```

| Group | Your fact table | Grain, in one sentence |
| --- | --- | --- |
| 1 ITSM & Operations | `fact_incident` | One row per incident |
| 2 Capacity & Forecasting | `fact_capacity` | One row per CI, per month |
| 3 Mainframe Analytics | `fact_mainframe` | One row per LPAR, per day |
| 4 Service Desk & Workforce | `fact_service_desk` | One row per team, per location, per day |
| 5 Asset & Workplace Services | `fact_asset` | One row per asset |

Being able to say your grain in one sentence is the test of whether you
understand your fact table. If you cannot, stop and work it out before building
relationships.

---

## Steps

### 1. Load the tables
- **Get data** → **Text/CSV** (or **SQL Server** if you are using your own source).
- Load your fact table plus all six dimensions:
  `dim_date`, `dim_configuration_item`, `dim_service`, `dim_team`,
  `dim_location`, `dim_severity`.
- Choose **Import**. Deck slide 11: `Prefer Import mode for now`.
- Load only the dimensions your fact actually joins to. Group 4 (Service Desk)
  has no CI or severity key, so skip those two.
- Save as `sm_io_<yourdomain>.pbix`, for example `sm_io_itsm.pbix`.

> **Do not** load `incident_report_extract.csv` here. That wide file is the
> Tableau "before", and it is Lab 4's raw material.

### 2. Create the relationships
Model view → drag key to key, or **Manage relationships** → **New**.

For `fact_incident`:

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
- **Avoid bidirectional by default.** If a visual seems to need it, the model is
  usually wrong somewhere else.
- Watch for the dotted line - an inactive relationship means Power BI found
  ambiguity. Resolve it rather than leaving it.

> `dim_configuration_item` also carries `service_key` and `location_key`. Do
> **not** relate those - it would create ambiguous filter paths. The fact table
> is the only thing that joins to dimensions. This is the snowflake-versus-star
> tradeoff from Day 1, and here the answer is star.

### 3. Mark the date table
- Select `dim_date` → **Table tools** → **Mark as date table**.
- Choose the `date` column, not `date_key`.
- Power BI validates it: unique, no blanks, contiguous days.

Skip this and every time-intelligence measure in Lab 3 will either fail or
silently return the wrong number. It is thirty seconds of work and it prevents
an entire category of bug.

### 4. Hide the plumbing
Deck slide 19: `Hide keys and technical columns immediately, before you build a
single visual.`

- Right-click each `_key` column → **Hide in report view**. Hide them on both the
  fact and the dimension side.
- Hide anything a report author will never drag onto a canvas: `incident_key`,
  `sort` helper columns, internal IDs.
- Keep `incident_number` visible - people genuinely search on it.
- Rename to business-friendly labels: `service_name` → `Service`,
  `severity_name` → `Severity`, `time_to_resolve_minutes` →
  `Time to Resolve (Minutes)`.
- Set `dim_severity[severity_name]` to **Sort by column** →
  `dim_severity[severity_sort]`, so Critical sorts before Low instead of
  alphabetically.

A field list a business user can read without a translator is the difference
between a model people adopt and one they work around.

### 5. Add your first measure
One measure, now, before any calculated columns. Deck slide 19: `Create your
first measure before adding any calculated columns.`

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

- Put it in a display folder or a dedicated `_Measures` table so it does not get
  lost among columns.
- Format it: whole number with a thousands separator, or one decimal place for a
  percentage.
- Drop it into a card visual and sanity-check the number against the source.

> **M365 Copilot assist.** Copilot cannot see your model, so give it the schema
> first. Paste this, adjusting for your domain:
>
> *"I have a Power BI Import model with a star schema. Fact table
> `fact_incident(date_key, ci_key, service_key, team_key, location_key,
> severity_key, time_to_resolve_minutes, sla_met_flag, incident_count)`.
> Dimensions: `dim_date`, `dim_configuration_item`, `dim_service`, `dim_team`,
> `dim_location`, `dim_severity`, each joined one-to-many on its key.
> `dim_date` is marked as the date table on `date`.
> Write a DAX measure that counts incidents. Explain why you chose that function."*
>
> Then read the explanation and check it against what you built. **Paste the DAX
> into Power BI and verify the number before you keep it.** Save this schema
> block - you will reuse it in every Copilot prompt in Labs 3 and 4.

### 6. Validate before you build anything on it
Five minutes here saves an hour on Day 3.

- Drop `Total Incidents` on a card. Does it match a `COUNT(*)` against the source?
- Add `dim_service[Service]` to a table with the measure. Do the values split
  sensibly, and do they sum back to the total?
- Add `dim_date[month_year]`. Is every month present, with no blank row?
- A **blank row** appearing in a dimension means referential integrity is broken:
  the fact has a key the dimension does not. Find it now.
- Switch one relationship to bidirectional, look at what changes, then switch it
  back. Understanding why it is wrong beats being told.

## You'll know it worked when
- The model diagram is a star: one fact in the middle, dimensions around it, no
  dimension-to-dimension joins.
- Every relationship is one-to-many, single direction.
- `dim_date` is marked as the date table on `date`.
- No `_key` column is visible in report view.
- `Severity` sorts Critical → Low, not alphabetically.
- Your first measure returns a number you have checked against the source.
- You can state your fact table's grain in one sentence.

## Next
[Lab 2 - Build your first report page](../lab-02-report-page/README.md)
