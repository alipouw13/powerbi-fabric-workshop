# Tableau to Power BI translation guide

Use this when a Tableau term comes up and you need the closest Power BI concept.

**This is a translation guide, not a substitution table.** Tableau's VizQL and
Power BI's DAX engine work differently. VizQL builds a query from the visual's
shelves, so a calculation is evaluated in the context of the sheet that contains
it. DAX evaluates a measure in a filter context assembled from the visual, the
page, the report, and the model relationships. Most Tableau logic has a good
Power BI equivalent, some has a better one, and a few things do not translate at
all and should be redesigned rather than ported. Where that is true, this page
says so.

## Workshop context

- Domain: Charles Schwab **Infrastructure & Operations**.
- Five domain groups: ITSM, Capacity & Forecasting, Mainframe, Service Desk &
  Workforce, Asset & Workplace Services.
- Target model: `sm_io_<domain>`, for example `sm_io_itsm`, in **Import** mode.
- Target report: `rpt_io_<domain>_<subject>`.
- Source shapes: a wide Tableau-style extract
  (`data/raw/tableau_extract/incident_report_extract.csv`), SQL-style dimensions
  and facts (`data/raw/sql/`), and a folder of monthly extracts
  (`data/raw/excel/`).

There is no Lakehouse, no Direct Lake, and no Dataflow in this workshop. Every
translation below lands in Power Query, DAX, or the Power BI Service.

## Concept mapping (deck slide 6)

| Tableau | Power BI | What actually changes |
| --- | --- | --- |
| Workbook | Report | One `.pbix` can hold many pages. The data no longer travels inside it if you use a shared model. |
| Data source / extract (`.hyper`) | Semantic model, **Import** mode | The model is a separate, reusable, governable object. |
| Live connection | **DirectQuery** | Available, but discouraged. Slower, and most Power Query steps are unavailable. Use only where caching is not permitted or the source is too large. |
| Calculated field | **DAX measure** | Write it once in the model, use it on every page and in every report built on that model. |
| Table calculation | **DAX with `CALCULATE` and filter modifiers** | The biggest conceptual jump. Tableau computes along a table layout; DAX manipulates filter context. |
| LOD expression | **Measure with context transition** | `FIXED`, `INCLUDE`, `EXCLUDE` all become `CALCULATE` plus the right filter modifier. |
| Dashboard | **Report page** | Careful: a Power BI "dashboard" is a different thing, a Service pin-board of tiles from several reports. |
| Published data source | **Shared semantic model** | Certify it, grant Build permission, and build thin reports on top. |
| Show Me | **Visualizations pane** | Same idea, different list. See [visual-design.md](visual-design.md). |

Additional mappings that come up constantly:

| Tableau | Power BI | Note |
| --- | --- | --- |
| Worksheet | A single visual on a page | A worksheet showing SLA by service is one bar chart. |
| Story | Report pages plus bookmarks and buttons | Or export to PowerPoint. |
| Data pane fields | Model fields and measures | Hide keys, expose business names. |
| Parameter | Field parameter, or what-if parameter | Field parameters let readers swap the metric or the dimension. |
| Set | Group, calculated table, or calculation group | Static cohorts become groups. |
| Group | Grouping, or an attribute in a dimension | Prefer putting reusable groupings in the dimension table. |
| Context filter | No equivalent needed | Filter propagation is handled by model relationships. |
| Tableau Prep | Power Query | All prep is Power Query here. |
| Tableau Server / Cloud | Power BI Service | Workspaces, apps, RLS, endorsement, deployment pipelines. |
| Row-level security | Power BI RLS | Defined in the model with DAX, roles assigned in the Service. |
| VizQL | DAX plus filter context | Query generation moves from the sheet to the model. |

## DAX mapping (deck slide 12)

| Tableau calculation | DAX equivalent | Comment |
| --- | --- | --- |
| `SUM([Sales])` | `SUM(fact_incident[incident_count])` | Direct. In practice write `Total Incidents = SUM(...)` once and reuse it. |
| `COUNTD([Order ID])` | `DISTINCTCOUNT(fact_incident[incident_number])` | Direct, but expensive on high-cardinality columns. |
| `AVG([Profit])` | `AVERAGE(fact_incident[time_to_resolve_minutes])` | `AVERAGE` ignores blanks. Decide whether open incidents should count. |
| `IF [x] > 0 THEN ... END` | `IF(...)`, or `SWITCH(TRUE(), ...)` for several branches | `SWITCH(TRUE(), ...)` is far more readable than nested `IF`. |
| `{ FIXED [Region] : SUM([Sales]) }` | `CALCULATE([Measure], ALLEXCEPT(table, table[column]))` | See the worked example below. |
| `{ EXCLUDE [Region] : SUM([Sales]) }` | `CALCULATE([Measure], REMOVEFILTERS(table[column]))` | Removes one filter, keeps the rest. |
| `{ INCLUDE [Order ID] : SUM([Sales]) }` | `SUMX(VALUES(table[column]), [Measure])` | Adds grain inside the measure using an iterator. |
| `RUNNING_SUM(SUM([Sales]))` | `CALCULATE([Measure], DATESYTD(dim_date[date]))` or a filtered `ALL` pattern | See the running total example. |
| `LOOKUP(SUM([Sales]), -12)` | `CALCULATE([Measure], SAMEPERIODLASTYEAR(dim_date[date]))` | Requires a marked date table. |
| `WINDOW_AVG(SUM([Sales]), -2, 0)` | `AVERAGEX` over a `DATESINPERIOD` window | Moving averages are an iterator plus a date window. |
| `TOTAL(SUM([Sales]))` | `CALCULATE([Measure], ALLSELECTED(...))` | `ALLSELECTED` respects slicers, `ALL` does not. |
| `INDEX()`, `RANK()` | `RANKX(ALL(table[column]), [Measure])` | |
| `[Sales] / TOTAL([Sales])` | `DIVIDE([Measure], CALCULATE([Measure], ALL(...)))` | Always `DIVIDE`, never `/`. It handles the zero denominator. |
| `ZN([x])` | `COALESCE([Measure], 0)` | |
| `DATEDIFF('day', [a], [b])` | `DATEDIFF([a], [b], DAY)` | Argument order differs. |
| `DATETRUNC('month', [d])` | Use `dim_date[month_year]` | Do not truncate in a measure. Put the grain in the date table. |

## Worked translations

All three use `fact_incident` and the conformed dimensions. Base measures first:

```DAX
Total Incidents = SUM(fact_incident[incident_count])
Resolved Incidents = CALCULATE([Total Incidents], fact_incident[incident_state] = "Resolved")
```

### 1. LOD `FIXED`: incidents per service, ignoring the visual's grain

Tableau:

```text
{ FIXED [Service Name] : SUM([Incident Count]) }
```

The intent is "give me the service total, whatever else is on the sheet". A
visual broken out by severity and team still shows the service-level number.

DAX:

```DAX
Incidents by Service =
CALCULATE(
    [Total Incidents],
    ALLEXCEPT( dim_service, dim_service[service_name] )
)
```

`ALLEXCEPT` clears every filter on `dim_service` except `service_name`. Filters
on `dim_severity` or `dim_team` are unaffected, because they sit on different
tables. If you need those cleared too, add them:

```DAX
Incidents by Service Only =
CALCULATE(
    [Total Incidents],
    ALLEXCEPT( dim_service, dim_service[service_name] ),
    REMOVEFILTERS( dim_severity ),
    REMOVEFILTERS( dim_team )
)
```

**What does not translate cleanly.** Tableau's LOD applies to whatever is on the
sheet. DAX filter removal is per table and per column, and you have to name what
you are removing. That is more verbose and considerably more predictable. Do not
try to write one measure that behaves like every LOD; write the one you need.

### 2. Running sum: cumulative incidents through the year

Tableau:

```text
RUNNING_SUM(SUM([Incident Count]))
```

DAX, year to date:

```DAX
Running Total Incidents =
CALCULATE(
    [Total Incidents],
    DATESYTD( dim_date[date] )
)
```

DAX, cumulative across the entire visible range rather than resetting each year:

```DAX
Cumulative Incidents =
VAR MaxDate = MAX( dim_date[date] )
RETURN
    CALCULATE(
        [Total Incidents],
        dim_date[date] <= MaxDate,
        ALLSELECTED( dim_date )
    )
```

**The difference that catches people.** Tableau's running sum accumulates along
the table layout, so re-sorting the sheet changes the answer. The DAX version
accumulates along the date, so it is stable regardless of how the visual is
sorted. That is a better default, but it does mean a "running sum" over a
non-date dimension needs a deliberately chosen ordering column.

### 3. Percent of total: each service's share of incidents

Tableau, quick table calculation "Percent of Total":

```text
SUM([Incident Count]) / TOTAL(SUM([Incident Count]))
```

DAX, share of the grand total in the model:

```DAX
Percent of Total Incidents =
DIVIDE(
    [Total Incidents],
    CALCULATE( [Total Incidents], ALL( fact_incident ) )
)
```

DAX, share of what the reader has currently selected:

```DAX
Percent of Selected Incidents =
DIVIDE(
    [Total Incidents],
    CALCULATE( [Total Incidents], ALLSELECTED() )
)
```

**The distinction matters.** `REMOVEFILTERS` and `ALL` ignore slicers, so the
denominator is every incident in the model and the visible percentages will not
sum to 100 when a slicer is applied. `ALLSELECTED` respects slicers, so the
column sums to 100. Tableau's "Percent of Total" behaves closest to
`ALLSELECTED`. Decide which one the business is asking for, and put the answer in
the measure description.

### 4. Table calculation over time: month over month

Tableau:

```text
(SUM([Incident Count]) - LOOKUP(SUM([Incident Count]), -1))
/ LOOKUP(SUM([Incident Count]), -1)
```

DAX:

```DAX
Incidents PM =
CALCULATE(
    [Total Incidents],
    DATEADD( dim_date[date], -1, MONTH )
)

MoM Change % =
DIVIDE( [Total Incidents] - [Incidents PM], [Incidents PM] )
```

This needs `dim_date` marked as the date table. Without that, the time
intelligence functions return values that look plausible and are wrong at period
boundaries.

## Mindset shifts

| Shift | What changes | I&O example |
| --- | --- | --- |
| Workbook-first to model-first | Logic moves out of each workbook into `sm_io_itsm`. | `SLA Met %` is defined once, not in six workbooks. |
| Extract sprawl to one governed model | Many `.hyper` files become one certified semantic model per domain. | One ITSM model serves the exec page, the SLA page and the team scorecard. |
| Sheet logic to reusable measures | Measures are shared across pages and reports. | `Avg Resolve Minutes` means the same thing everywhere. |
| Wide table to star schema | Facts and dimensions separate grain from description. | `fact_incident` joins `dim_service`, `dim_severity`, `dim_date` and three more. |
| Dashboard as artifact to page as design surface | You build report pages. | The Service Desk view is a report page, not a Service dashboard. |
| Per-workbook filters to model relationships | Filters propagate through the model. | One `dim_service` slicer filters incidents and capacity together. |

## Migration rule of thumb

| If the Tableau workbook has... | Start with... | Reason |
| --- | --- | --- |
| One wide extract and many calculated fields | Star schema rebuild | Porting the sheet logic reproduces the problem in a new tool. |
| A stable, trusted published data source | Shared semantic model | Reuse the business layer, rebuild the pages. |
| Heavy custom layout or extensions | Report rebuild using native visuals | Recreate the outcome, not the pixels. |
| Complex prep logic upstream | Power Query staging queries | Keep transformation out of the visuals. |
| Live operational queries | An honest Import vs DirectQuery decision | Confirm the freshness requirement before choosing DirectQuery. |
| Low usage and no owner | Retirement | Do not port a bad model. |

## Model-first checklist

- State the grain of the fact table in one sentence before building visuals.
- Use `fact_incident` for incident counts, resolve time and SLA attainment.
- Use `fact_capacity` for utilization and headroom.
- Use `dim_date` for month, quarter and prior-period logic, and mark it.
- Use `dim_service` and `dim_location` as conformed dimensions across domains.
- Hide surrogate keys from report authors.
- Name fields in business language: `Service Name`, not `service_name`.
- Add a description to every measure. It is also your Copilot prompt context.
- Certify `sm_io_<domain>` only after tie-out and owner review.

## Related

- [Star schema](star-schema.md)
- [Visual design](visual-design.md)
- [Migration approaches](migration-approaches.md)
- [Current state and constraints](schwab-current-state.md)
- [M365 Copilot for Power BI work](copilot-in-power-bi.md)
- [Migration assessment worksheet](../governance/migration-assessment-worksheet.md)
- [Measure definitions](../src/pbip/README.md)
- [Sources](sources.md)
