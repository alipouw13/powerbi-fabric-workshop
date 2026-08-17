# Synthetic Banking and Capital Markets I&O dataset

The data behind every lab in this workshop. It models an enterprise
**Infrastructure & Operations** group: incidents, capacity, mainframe throughput,
service desk workload, and the asset estate for two fictional focus units:
**Banking** and **Capital Markets**.

## Synthetic data notice

Everything here is generated. Service names, CI names, incident numbers, sites,
teams, costs, and every metric are synthetic. There are no customers, account
balances, positions, orders, trades, or real market observations. **This is not
customer data.** Do not treat it as production, customer, or regulated data.

Groups are welcome to substitute their own sources. The labs are written against
this dataset because it is safe and consistent across five breakout groups, not
because the shapes are unusual. If your team has a real SQL view or a real
monthly extract folder, the same patterns apply unchanged.

## Generating the data

```powershell
python data\generate_data.py
python data\generate_data.py --months 12 --ci-count 200
```

| Argument | Default | Effect |
| --- | --- | --- |
| `--months` | 24 | Months of history. Drives every row count except the dimensions. |
| `--ci-count` | 400 | Number of configuration items. Drives `dim_configuration_item` and `fact_asset`. Minimum 30, because every service and both business units have to be covered by mainframe and capacity CIs whatever the estate size. |

The generator is seeded, so the same arguments and reporting period produce the
same data. Requires `pandas` and `numpy`.

Nothing is written until the whole dataset passes validation. The generator
checks that every surrogate key is unique, that **every foreign key on every
table resolves to a real dimension row**, that every fact carries at least one
date key and reaches both business units, and that every fact honours its
declared grain. A fact that loses a key fails generation rather than producing a
model with a silent blank member.

## Business scope

`dim_service` is the business lens shared by all five operational facts. It has
two reporting levels:

| Business unit | Business domains | Synthetic services |
| --- | --- | --- |
| **Banking** | Digital Banking, Deposits, Payments, Lending, Treasury Services | Digital Banking Portal, Mobile Banking, Core Deposits Platform, Payments Gateway, Consumer Lending Platform, Treasury Management |
| **Capital Markets** | Trading, Market Data, Brokerage, Post-Trade, Risk Management | Electronic Trading Platform, Order Management System, Market Data Distribution, Brokerage Account Platform, Clearing and Settlement, Market Risk Analytics |

`service_tier` grades criticality: **Tier 0** is mission-critical real-time or
system-of-record, **Tier 1** is customer-facing, **Tier 2** is important but tolerant of
a short outage. It gives every group a second, orthogonal way to slice the same data.

Every fact table contains `service_key`, so a `dim_service[business_unit]` slicer
works consistently for incidents, capacity, mainframe, service desk, and assets.
The generator fails before writing files if a fact loses that key, references an
unknown service, fails to cover both units, or if the service vocabulary drifts
beyond the two focus units.
## The four shapes

The dataset ships the same story in four deliberately different shapes, because
the migration lesson is in the contrast.

| Shape | Path | What it represents |
| --- | --- | --- |
| **1. SQL-style dims and facts** | `data/raw/sql/*.csv` | The SQL Server views you reach through the on-premises data gateway. Normalized, keyed, ready to model. This is the "after". |
| **2. Wide Tableau extract** | `data/raw/tableau_extract/incident_report_extract.csv` | One flat 39-column denormalized table, the way a `.hyper` extract looks today. This is the "before". |
| **3. Monthly Excel folder** | `data/raw/excel/capacity_YYYY_MM.csv` | The "large Excel files" pain point: one file per month, inconsistent column names. |
| **4. Dirty exports** | `data/raw/dirty/*.csv` | Four files that are wrong on purpose - junk headers, cross-tabs, currency as text, total rows. Each defect has one specific Power Query fix. See [power-query-cleanup.md](power-query-cleanup.md). |

Written as CSV throughout so the generator has no Excel dependency. The column
names and the inconsistencies are what matter, not the file format.

## Shape 1: SQL-style dimensions and facts

Six conformed dimensions shared by all five domain groups, one fact table per
group. Row counts scale with `--months` and `--ci-count`.

### Conformed dimensions

| File | Grain | Rows | Columns |
| --- | --- | ---: | --- |
| `dim_date.csv` | One row per day | Varies | `date_key`, `date`, `year`, `quarter`, `month`, `month_name`, `month_year`, `day_of_month`, `day_of_week`, `day_name`, `is_weekend`, `week_of_year`, `fiscal_year`, `fiscal_quarter`, `is_reporting_period` |
| `dim_service.csv` | One row per business service | 12 | `service_key`, `service_id`, `service_name`, `service_tier`, `business_unit`, `business_domain` |
| `dim_configuration_item.csv` | One row per CI | Varies | `ci_key`, `ci_id`, `ci_name`, `ci_type`, `environment`, `criticality`, `service_key`, `location_key`, `support_team_key`, `support_group` |
| `dim_team.csv` | One row per team | 10 | `team_key`, `team_id`, `team_name`, `assignment_group`, `shift_coverage` |
| `dim_location.csv` | One row per site | 8 | `location_key`, `location_id`, `site_name`, `city`, `state_province`, `country`, `region`, `datacenter` |
| `dim_severity.csv` | One row per severity | 4 | `severity_key`, `severity_code`, `severity_name`, `priority`, `sla_target_hours`, `severity_sort` |

`dim_configuration_item` carries `service_key`, `location_key` and
`support_team_key`, which makes it a mild snowflake. That is deliberate: it gives
Lab 1 a real modeling decision to make. See
[star-schema.md](../reference/star-schema.md). `support_group` is the owning
team's `assignment_group`, derived from `support_team_key` rather than invented,
so the two tables always agree.

`dim_severity` carries `severity_sort` so severity sorts Critical, High,
Moderate, Low instead of alphabetically.

### Why dim_date is wider than the reporting window

`dim_date` spans **whole calendar years**, from the year of the oldest asset
purchase to the year of the newest warranty expiry. Two reasons:

1. `fact_asset` keys into it on `purchase_date_key` and `warranty_end_date_key`,
   and those dates sit years either side of the reporting window. A narrower
   date table would leave those keys pointing at nothing.
2. **Mark as date table** requires contiguous days covering full calendar years.

`is_reporting_period` flags the window the event facts actually cover. Use it in
a filter or a slicer when a visual should not show empty years. It is a helper
column, so hide it in report view.

### Fact tables

Every fact carries a surrogate primary key, a date key, and one foreign key per
dimension that applies to its grain.

| File | Group | Grain | Rows | Key columns |
| --- | --- | --- | ---: | --- |
| `fact_incident.csv` | 1, ITSM | One row per incident | Varies | `incident_key`, `incident_number`, `date_key`, `ci_key`, `service_key`, `team_key`, `location_key`, `severity_key`, `opened_at`, `resolved_at`, `incident_state`, `category`, `contact_type`, `time_to_resolve_minutes`, `reassignment_count`, `reopened_flag`, `sla_met_flag`, `major_incident_flag`, `incident_count` |
| `fact_capacity.csv` | 2, Capacity | One row per CI per month | Varies | `capacity_key`, `date_key`, `ci_key`, `service_key`, `location_key`, `team_key`, `cpu_utilization_pct`, `memory_utilization_pct`, `storage_allocated_gb`, `storage_used_gb`, `headroom_pct` |
| `fact_mainframe.csv` | 3, Mainframe | One row per LPAR per day | Varies | `mainframe_key`, `date_key`, `ci_key`, `service_key`, `location_key`, `team_key`, `mips_consumed`, `mips_capacity`, `batch_jobs_completed`, `batch_jobs_failed`, `batch_window_minutes`, `transactions_processed` |
| `fact_service_desk.csv` | 4, Service Desk | One row per service per team per location per day | Varies | `service_desk_key`, `date_key`, `service_key`, `team_key`, `location_key`, `tickets_received`, `tickets_resolved`, `first_contact_resolved`, `calls_abandoned`, `agents_scheduled`, `agents_available`, `avg_handle_time_minutes`, `avg_speed_to_answer_seconds` |
| `fact_asset.csv` | 5, Assets | One row per asset | Varies | `asset_key`, `asset_tag`, `ci_key`, `service_key`, `location_key`, `team_key`, `purchase_date_key`, `warranty_end_date_key`, `purchase_date`, `warranty_end_date`, `lifecycle_status`, `acquisition_cost_usd`, `annual_support_cost_usd`, `is_under_warranty`, `cmdb_complete_flag`, `asset_count` |

### Which dimension joins which fact

| | `fact_incident` | `fact_capacity` | `fact_mainframe` | `fact_service_desk` | `fact_asset` |
| --- | :---: | :---: | :---: | :---: | :---: |
| `dim_date` | `date_key` | `date_key` | `date_key` | `date_key` | `purchase_date_key`, `warranty_end_date_key` |
| `dim_service` | yes | yes | yes | yes | yes |
| `dim_location` | yes | yes | yes | yes | yes |
| `dim_team` | yes | yes | yes | yes | yes |
| `dim_configuration_item` | yes | yes | yes | - | yes |
| `dim_severity` | yes | - | - | - | - |

`dim_service`, `dim_location` and `dim_team` are conformed across all five facts.
`dim_severity` applies only to incidents, because nothing else in the set has a
severity. `fact_service_desk` has no `ci_key` because its grain is the service,
not the machine.

On capacity, mainframe and asset rows, `team_key` is the CI's owning support
team, taken from `dim_configuration_item[support_team_key]`. On incident and
service-desk rows it is the team that handled the work. Same dimension, different
meaning - worth stating in the table description.

Deliberate characteristics worth knowing before you write measures:

- **`fact_asset` has two date keys.** `purchase_date_key` and
  `warranty_end_date_key` both point at `dim_date`, which makes it a
  **role-playing dimension**. Power BI allows one active relationship between a
  pair of tables, so the second one is inactive and needs `USERELATIONSHIP`.
  Group 5 has to decide which one is active. See
  [star-schema.md](../reference/star-schema.md#role-playing-dimensions).
- **Open incidents exist.** `resolved_at`, `time_to_resolve_minutes`, and
  `sla_met_flag` are blank for incidents still open. Any quality measure has to
  decide whether to include them. `SLA Met %` uses resolved incidents as its
  denominator for exactly this reason.
- **`mips_capacity` repeats** on every daily row for the same LPAR. Summing it
  across a month multiplies installed capacity by the number of days.
- **Percentage columns are percentages.** `cpu_utilization_pct` and
  `headroom_pct` must be averaged, never summed.
- **`incident_count` and `asset_count` are always 1.** They exist so a count
  survives being filtered and so the fact table has an obvious additive measure.
- **Month-end batch peaks** are built into `fact_mainframe`, and weekend dips
  into `fact_service_desk`. The seasonality is there to be found.

## Shape 2: the wide Tableau extract

`data/raw/tableau_extract/incident_report_extract.csv`

One table, **39 columns**, with a generated row count. Every service, CI, team,
site and severity attribute repeats on every incident row, plus two
pre-aggregated columns (`resolve_hours`, `is_breached`) baked in the way a
Tableau calculated field gets baked into an extract.

Columns: `incident_number`, `date`, `year`, `quarter`, `month_name`,
`month_year`, `is_weekend`, `service_name`, `service_tier`, `business_unit`,
`business_domain`,
`ci_name`, `ci_type`, `environment`, `criticality`, `team_name`,
`assignment_group`, `shift_coverage`, `site_name`, `city`, `state_province`,
`region`, `datacenter`, `severity_code`, `severity_name`, `priority`,
`sla_target_hours`, `category`, `contact_type`, `incident_state`, `opened_at`,
`resolved_at`, `time_to_resolve_minutes`, `resolve_hours`, `reassignment_count`,
`reopened_flag`, `sla_met_flag`, `is_breached`, `major_incident_flag`.

This is the "before". It is what Lab 0 reshapes into dimensions and a fact table,
and it is what the star-schema conversation is about. `site_name` appears once
per incident here and only 8 times in `dim_location`.

It is also the file to reconcile against: totals from the modelled star schema
must match totals from this extract, or something was dropped.

## Shape 3: the monthly Excel folder

`data/raw/excel/capacity_YYYY_MM.csv`, one file per generated month.

Each file holds one month of capacity readings with business-friendly headers:

`CI Name`, `Environment`, `CPU %`, `Memory %`, `Storage Used GB`,
`Storage Allocated GB`

120 data rows per file.

### The deliberate November anomaly

The most recent generated November file is different on purpose. Two changes:

1. The `CPU %` column is renamed to **`CPU Utilisation %`** (British spelling).
   A folder-combine query that references columns by position will not notice. A
   query that references them by name will produce nulls for that month, which
   silently drags every CPU average down.
2. A stray **`TOTAL`** row is appended, with `CI Name = "TOTAL"`, the mean CPU
   figure, and nulls everywhere else. Left in, it inflates the CI count by one
   and pulls the average toward a number that already contains itself.

The file has 121 rows instead of 120 for that reason.

This is not a bug in the generator. It is the exercise. Lab 0 builds a schema
guard that normalises the renamed column, strips the total row, and errors loudly
on a column that is genuinely missing. The pattern is in
[`src/powerquery/README.md`](../src/powerquery/README.md#schema-guard).

## Shape 4: the dirty exports

`data/raw/dirty/`, four files that are wrong on purpose.

| File | Headline problem | Power Query answer |
| --- | --- | --- |
| `incident_export_dirty.csv` | Junk preamble above the header, mixed date formats, duplicates, footer | Remove Top Rows, Promote Headers, Remove Duplicates, filter |
| `capacity_by_month_crosstab.csv` | Months across the columns, blanked group labels, `Total` column and row | Fill Down, then Unpivot Other Columns |
| `asset_inventory_dirty.csv` | Currency and dates stored as text, five spellings of one status | Replace Values, Split Column, mapping table |
| `service_desk_daily_dirty.csv` | A two-row header | Transpose, Fill Down, Merge, Transpose back |

Every defect maps to one specific transform, and every file reconciles back to a
clean table in `data/raw/sql/`, so there is a right answer to check against. The
full catalogue, the fixes, and the verification steps are in
[**power-query-cleanup.md**](power-query-cleanup.md).

These exist because `data/raw/sql/` is already clean. It demonstrates modeling
well and transformation not at all, and Power Query is the single
highest-leverage skill in this environment.

## Which lab uses what

| Lab | Uses | Why |
| --- | --- | --- |
| [Day 1 setup](../labs/day-1-setup/README.md) | Nothing, or one small file to test a connection | Gateway and environment check |
| [Lab 0 - Connect, shape, and load](../labs/lab-00-connect-and-shape/README.md) | `tableau_extract/incident_report_extract.csv`, `excel/`, and `dirty/` | Reshape the wide extract, combine the folder, guard the schema, clean a real mess |
| [Lab 1 - Build the semantic model](../labs/lab-01-semantic-model/README.md) | `data/raw/sql/` dims plus your group's fact table | Build the star, set relationships, mark the date table |
| [Lab 2 - Build your first report page](../labs/lab-02-report-page/README.md) | The model from Lab 1 | No new data |
| [Lab 3 - Practice DAX measures](../labs/lab-03-dax-measures/README.md) | The model from Lab 1 | Measures and validation queries |

Groups 2 to 5 swap their own fact table into Labs 1 to 3. The dimensions are
shared, which is the point of conformed dimensions.

## Sanity checks

Quick reasonableness checks, not exact test assertions. They shift with
`--months` and `--ci-count`.

| Check | Approximate expectation |
| --- | --- |
| Incidents per month | Roughly 2,500 |
| SLA Met % overall | Roughly 80 to 90 percent |
| Severity mix | SEV1 about 3%, SEV2 12%, SEV3 45%, SEV4 40% |
| Open incidents | A small share, concentrated in recent months |
| Avg CPU utilization | Roughly 45 to 70 percent, drifting upward over time |
| First contact resolution | Roughly 55 to 78 percent |
| Assets under warranty | Roughly 40 to 55 percent of the estate |
| CMDB completeness | Roughly 83 percent |

If a measure returns a utilization figure in the thousands, a percentage was
summed instead of averaged.

## Related

- [Power Query cleanup catalogue](power-query-cleanup.md)
- [Star schema](../reference/star-schema.md)
- [Power Query snippet library](../src/powerquery/README.md)
- [Measure definitions](../src/pbip/README.md)
- [Sample DAX and validation queries](../src/sql/sample_dax_queries.dax)
- [Tableau to Power BI](../reference/tableau-to-powerbi.md)
- [Migration assessment worksheet](../governance/migration-assessment-worksheet.md)
