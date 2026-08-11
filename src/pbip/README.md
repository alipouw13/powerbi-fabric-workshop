# Measure definitions - I&O semantic models

The source of truth for every measure used in the workshop labs. Type these into
Power BI Desktop. Keep them consistent with
[`src/sql/sample_dax_queries.dax`](../sql/sample_dax_queries.dax), which holds the
same definitions plus the validation queries.

## How to use this

1. Create a dedicated **Measures** table in your model: **Home -> Enter data**,
   one column, no rows, name it `_Measures`. Move every measure into it so the
   field list is readable.
2. Add measures in the order below. The base measures come first because the
   others reference them.
3. Set the **format string** from the table, in the model, not on the visual.
4. Paste the description into **Model view -> measure -> Description**. It is what
   a report author sees on hover, and it is what you paste into M365 Copilot when
   you want it to draft a measure that fits.

Rules that apply to every measure here:

- Reuse base measures. Never re-aggregate the underlying column.
- Every division uses `DIVIDE`, never `/`.
- Time intelligence requires `dim_date` marked as the date table on
  `dim_date[date]`.

---

## Group 1: ITSM and Operational Reporting

Model `sm_io_itsm`, fact table `fact_incident`, one row per incident.

### Base measures

| Measure | Description | Format |
| --- | --- | --- |
| Total Incidents | Count of incidents in the current filter context. | Whole number, thousands separator |
| Resolved Incidents | Incidents that reached Resolved or Closed. Open incidents have no resolve time or SLA outcome. | Whole number, thousands separator |
| Avg Resolve Minutes | Mean minutes from open to resolve. Open incidents are excluded automatically. | Whole number |
| SLA Met % | Share of resolved incidents that met the severity SLA target. | Percent, 1 decimal |
| Major Incidents | Incidents flagged as major. | Whole number |
| Reopened Rate | Share of incidents reopened after resolution. Rising means incidents are being closed, not fixed. | Percent, 1 decimal |

```dax
Total Incidents = SUM( fact_incident[incident_count] )

Resolved Incidents =
CALCULATE(
    [Total Incidents],
    fact_incident[incident_state] IN { "Resolved", "Closed" }
)

Avg Resolve Minutes = AVERAGE( fact_incident[time_to_resolve_minutes] )

SLA Met % =
VAR MetSLA =
    CALCULATE( [Total Incidents], fact_incident[sla_met_flag] = TRUE() )
RETURN
    DIVIDE( MetSLA, [Resolved Incidents] )

Major Incidents =
CALCULATE( [Total Incidents], fact_incident[major_incident_flag] = TRUE() )

Reopened Rate =
VAR Reopened =
    CALCULATE( [Total Incidents], fact_incident[reopened_flag] = TRUE() )
RETURN
    DIVIDE( Reopened, [Total Incidents] )
```

### Time intelligence

| Measure | Description | Format |
| --- | --- | --- |
| Incidents PM | Total Incidents for the previous month. | Whole number, thousands separator |
| MoM Change % | Month over month change in Total Incidents. Blank in the first month. | Percent, 1 decimal |
| Incidents PY | Total Incidents for the same period last year. | Whole number, thousands separator |
| YoY Change % | Year over year change in Total Incidents. | Percent, 1 decimal |
| Running Total Incidents | Cumulative incidents within the current year, resetting on 1 January. | Whole number, thousands separator |
| Cumulative Incidents | Cumulative incidents across the selected range, without a yearly reset. | Whole number, thousands separator |

```dax
Incidents PM =
CALCULATE( [Total Incidents], DATEADD( dim_date[date], -1, MONTH ) )

MoM Change % =
DIVIDE( [Total Incidents] - [Incidents PM], [Incidents PM] )

Incidents PY =
CALCULATE( [Total Incidents], SAMEPERIODLASTYEAR( dim_date[date] ) )

YoY Change % =
DIVIDE( [Total Incidents] - [Incidents PY], [Incidents PY] )

Running Total Incidents =
CALCULATE( [Total Incidents], DATESYTD( dim_date[date] ) )

Cumulative Incidents =
VAR MaxDate = MAX( dim_date[date] )
RETURN
    CALCULATE(
        [Total Incidents],
        dim_date[date] <= MaxDate,
        ALLSELECTED( dim_date )
    )
```

### Distribution

| Measure | Description | Format |
| --- | --- | --- |
| Percent of Total Incidents | Share of all incidents in the model. Ignores slicers, so percentages do not sum to 100 under a filter. | Percent, 1 decimal |
| Percent of Selected Incidents | Share of the current selection. Respects slicers, so the column sums to 100. Closest to Tableau's Percent of Total. | Percent, 1 decimal |
| Percent of Service Incidents | Share within the service dimension only. The DAX answer to a Tableau FIXED LOD. | Percent, 1 decimal |

```dax
Percent of Total Incidents =
DIVIDE(
    [Total Incidents],
    CALCULATE( [Total Incidents], ALL( fact_incident ) )
)

Percent of Selected Incidents =
DIVIDE(
    [Total Incidents],
    CALCULATE( [Total Incidents], ALLSELECTED() )
)

Percent of Service Incidents =
DIVIDE(
    [Total Incidents],
    CALCULATE( [Total Incidents], REMOVEFILTERS( dim_service ) )
)
```

Pick one of the first two deliberately and say which in the description. Shipping
both without explaining the difference is how two pages end up disagreeing.

---

## Group 2: Capacity and Forecasting

Model `sm_io_capacity`, fact table `fact_capacity`, one row per CI per month.

| Measure | Description | Format |
| --- | --- | --- |
| Avg CPU Utilization | Mean CPU utilization across the CIs in context. Never sum a percentage. | Percent, 1 decimal |
| Avg Memory Utilization | Mean memory utilization across the CIs in context. | Percent, 1 decimal |
| CIs Over 80% CPU | Distinct CIs running above 80% CPU. Distinct, because one CI has many monthly rows. | Whole number |
| Avg Headroom % | Mean remaining headroom. The forecasting headline. | Percent, 1 decimal |
| Storage Utilization % | Used storage as a share of allocated, computed from totals so large volumes weigh correctly. | Percent, 1 decimal |
| CI Count | Distinct CIs in context. Useful as a denominator and as a sanity check. | Whole number |

```dax
Avg CPU Utilization = AVERAGE( fact_capacity[cpu_utilization_pct] )

Avg Memory Utilization = AVERAGE( fact_capacity[memory_utilization_pct] )

CIs Over 80% CPU =
CALCULATE(
    DISTINCTCOUNT( fact_capacity[ci_key] ),
    fact_capacity[cpu_utilization_pct] > 80
)

Avg Headroom % = AVERAGE( fact_capacity[headroom_pct] )

Storage Utilization % =
DIVIDE(
    SUM( fact_capacity[storage_used_gb] ),
    SUM( fact_capacity[storage_allocated_gb] )
)

CI Count = DISTINCTCOUNT( fact_capacity[ci_key] )
```

---

## Group 3: Mainframe Analytics

Model `sm_io_mainframe`, fact table `fact_mainframe`, one row per LPAR per day.

| Measure | Description | Format |
| --- | --- | --- |
| Total MIPS Consumed | MIPS consumed in context. Additive across days and LPARs. | Whole number, thousands separator |
| MIPS Utilization % | Consumed against installed capacity. Dividing two sums cancels the daily repetition of capacity. | Percent, 1 decimal |
| Peak MIPS | Highest single-day consumption in context. Sizing is done against the peak, not the average. | Whole number, thousands separator |
| Batch Failure Rate | Failed batch jobs as a share of all batch jobs. | Percent, 2 decimals |
| Avg Batch Window Minutes | Mean nightly batch window length. | Whole number |
| Total Transactions | Transactions processed in context. | Whole number, thousands separator |

```dax
Total MIPS Consumed = SUM( fact_mainframe[mips_consumed] )

MIPS Utilization % =
DIVIDE(
    SUM( fact_mainframe[mips_consumed] ),
    SUM( fact_mainframe[mips_capacity] )
)

Peak MIPS = MAX( fact_mainframe[mips_consumed] )

Batch Failure Rate =
DIVIDE(
    SUM( fact_mainframe[batch_jobs_failed] ),
    SUM( fact_mainframe[batch_jobs_completed] ) + SUM( fact_mainframe[batch_jobs_failed] )
)

Avg Batch Window Minutes = AVERAGE( fact_mainframe[batch_window_minutes] )

Total Transactions = SUM( fact_mainframe[transactions_processed] )
```

`mips_capacity` repeats on every daily row for the same LPAR. Never put it on a
card as a SUM: across a 30 day month it reports 30 times the installed capacity.

---

## Group 4: Service Desk and Workforce

Model `sm_io_servicedesk`, fact table `fact_service_desk`, one row per team per
location per day.

| Measure | Description | Format |
| --- | --- | --- |
| Tickets Received | Tickets received in context. | Whole number, thousands separator |
| Tickets Resolved | Tickets resolved in context. | Whole number, thousands separator |
| First Contact Resolution % | Share of resolved tickets closed on first contact. The desk's primary quality metric. | Percent, 1 decimal |
| Avg Handle Time | Mean handle time in minutes. | 1 decimal |
| Avg Speed to Answer | Mean speed to answer in seconds. | Whole number |
| Abandon Rate | Calls abandoned before an agent answered, as a share of tickets received. | Percent, 1 decimal |
| Coverage % | Agents available against agents scheduled. | Percent, 1 decimal |
| Tickets per Agent | Workload per available agent. Divides two sums so busy days weigh correctly. | 1 decimal |

```dax
Tickets Received = SUM( fact_service_desk[tickets_received] )

Tickets Resolved = SUM( fact_service_desk[tickets_resolved] )

First Contact Resolution % =
DIVIDE(
    SUM( fact_service_desk[first_contact_resolved] ),
    [Tickets Resolved]
)

Avg Handle Time = AVERAGE( fact_service_desk[avg_handle_time_minutes] )

Avg Speed to Answer = AVERAGE( fact_service_desk[avg_speed_to_answer_seconds] )

Abandon Rate =
DIVIDE( SUM( fact_service_desk[calls_abandoned] ), [Tickets Received] )

Coverage % =
DIVIDE(
    SUM( fact_service_desk[agents_available] ),
    SUM( fact_service_desk[agents_scheduled] )
)

Tickets per Agent =
DIVIDE( [Tickets Received], SUM( fact_service_desk[agents_available] ) )
```

---

## Group 5: Asset and Workplace Services

Model `sm_io_assets`, fact table `fact_asset`, one row per asset.

| Measure | Description | Format |
| --- | --- | --- |
| Total Assets | Count of assets in context. | Whole number, thousands separator |
| Assets Out of Warranty | Assets whose warranty has lapsed. | Whole number |
| Out of Warranty % | Share of the estate out of warranty. | Percent, 1 decimal |
| CMDB Completeness % | Share of assets with a complete CMDB record. The group's headline governance metric. | Percent, 1 decimal |
| Total Acquisition Cost | Capital cost of the assets in context. | Currency, 0 decimals |
| Annual Support Cost | Annual run-rate support cost. | Currency, 0 decimals |
| Avg Acquisition Cost | Mean asset value. | Currency, 0 decimals |
| Assets Expiring in 90 Days | Assets whose warranty expires inside the next 90 days. Drives the renewal worklist. | Whole number |

```dax
Total Assets = SUM( fact_asset[asset_count] )

Assets Out of Warranty =
CALCULATE( [Total Assets], fact_asset[is_under_warranty] = FALSE() )

Out of Warranty % = DIVIDE( [Assets Out of Warranty], [Total Assets] )

CMDB Completeness % =
DIVIDE(
    CALCULATE( [Total Assets], fact_asset[cmdb_complete_flag] = TRUE() ),
    [Total Assets]
)

Total Acquisition Cost = SUM( fact_asset[acquisition_cost_usd] )

Annual Support Cost = SUM( fact_asset[annual_support_cost_usd] )

Avg Acquisition Cost = DIVIDE( [Total Acquisition Cost], [Total Assets] )

Assets Expiring in 90 Days =
CALCULATE(
    [Total Assets],
    fact_asset[warranty_end_date] >= TODAY(),
    fact_asset[warranty_end_date] <= TODAY() + 90
)
```

`Assets Expiring in 90 Days` uses `TODAY()`, so it moves with the report rather
than with the model refresh. That is intended here. Do not use `TODAY()` in a
measure that has to reconcile to a fixed reported figure.

---

## Naming and format conventions

| Thing | Convention |
| --- | --- |
| Measure name | Business language, Title Case: `Total Incidents`, not `count_inc` |
| Percentages | Name ends in `%`, format is Percent |
| Averages | Name starts with `Avg`, unit in the name if the format cannot carry it |
| Counts | Plural noun: `Total Incidents`, `Total Assets` |
| Prior period | Suffix `PM` for prior month, `PY` for prior year |
| Change | Suffix `Change %` |
| Measures table | `_Measures`, so it sorts to the top of the field list |

## Before you certify

- [ ] Every measure has a description filled in.
- [ ] Every measure has a format string set in the model.
- [ ] No measure divides with `/`.
- [ ] No percentage is summed anywhere.
- [ ] Validation queries V5 to V9 in
      [`sample_dax_queries.dax`](../sql/sample_dax_queries.dax) all return
      plausible numbers.
- [ ] Totals reconcile against the Tableau report being replaced.
- [ ] Underlying numeric columns that now have measures are hidden.

## Related

- [Sample DAX queries and validation](../sql/sample_dax_queries.dax)
- [Star schema](../../reference/star-schema.md)
- [Tableau to Power BI](../../reference/tableau-to-powerbi.md)
- [Lab 3 - Practice DAX measures](../../labs/lab-03-dax-measures/README.md)
- [Endorsement and certification](../../governance/endorsement-certification.md)
