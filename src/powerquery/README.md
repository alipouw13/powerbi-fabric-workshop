# Power Query M snippet library

There is no lake layer and no Dataflow in this environment, so **every
transformation at Schwab I&O happens in Power Query**. Without a shared Dataflow
to inherit logic from, the practical substitute is a shared snippet library.

This is that library. It is deliberately low-tech: paste into the **Advanced
Editor**, adjust the names, verify the result. It is used in
[Lab 0](../../labs/lab-00-connect-and-shape/README.md) and referenced by
[Lab 1](../../labs/lab-01-semantic-model/README.md).

> **Before you paste anything.** Check row count, new nulls, explicit data types,
> and whether query folding survived. Then rename the generated steps so a
> colleague can read them.

## Contents

| Snippet | Use | Folds? |
| --- | --- | --- |
| [Staging query](#staging-query) | The one source query everything else references | Yes, if you keep the order |
| [Dimension from a reference query](#dimension-from-a-reference-query) | Build conformed dimensions without duplicating logic | Partly |
| [Fact table shaping](#fact-table-shaping) | Reduce a wide source to a proper fact grain | Yes |
| [Date table](#date-table) | Generate `dim_date` in M | No, it is generated |
| [Excel folder combine](#excel-folder-combine) | One query for a folder of monthly extracts | No |
| [Schema guard](#schema-guard) | Fail loudly instead of producing silent nulls | No |
| [Incremental refresh parameters](#incremental-refresh-parameters) | RangeStart and RangeEnd for large facts | Must fold |

Parameters used throughout: `ServerName`, `DatabaseName`, `ReportingStartDate`,
`MonthlyExtractFolder`. Create them under **Home -> Manage parameters** so
nothing is hardcoded.

---

## Staging query

Load this once, disable load, and reference it everywhere else. This is the
single most important structural habit in the library.

```powerquery
let
    Source = Sql.Database(ServerName, DatabaseName),
    Data   = Source{[Schema = "dbo", Item = "vw_incident"]}[Data],

    // Filter and remove columns FIRST so these steps fold back to SQL.
    Filtered = Table.SelectRows(Data, each [opened_at] >= ReportingStartDate),
    Trimmed  = Table.SelectColumns(Filtered, {
        "incident_key", "incident_number", "date_key", "ci_key", "service_key",
        "team_key", "location_key", "severity_key",
        "opened_at", "resolved_at", "incident_state", "category", "contact_type",
        "time_to_resolve_minutes", "reassignment_count", "reopened_flag",
        "sla_met_flag", "major_incident_flag", "incident_count"
    }),
    Typed = Table.TransformColumnTypes(Trimmed, {
        {"incident_key", Int64.Type},
        {"incident_number", type text},
        {"date_key", Int64.Type},
        {"ci_key", Int64.Type},
        {"service_key", Int64.Type},
        {"team_key", Int64.Type},
        {"location_key", Int64.Type},
        {"severity_key", Int64.Type},
        {"opened_at", type datetime},
        {"resolved_at", type datetime},
        {"time_to_resolve_minutes", Int64.Type},
        {"reassignment_count", Int64.Type},
        {"reopened_flag", type logical},
        {"sla_met_flag", type logical},
        {"major_incident_flag", type logical},
        {"incident_count", Int64.Type}
    })
in
    Typed
```

Right-click the query and untick **Enable load**. It is scaffolding, not a table.

**Folding:** yes, through `Filtered` and `Trimmed`, and usually through `Typed`.
Confirm with **View Native Query** on the last step. Order matters: filter and
remove columns before you add anything, or folding stops at the first
non-foldable step and everything after it runs locally.

If your group is working from the CSV files instead of a SQL view, swap the first
two lines. Nothing else changes, but nothing folds:

```powerquery
    Source = Csv.Document(
                File.Contents(SourceFolder & "\sql\fact_incident.csv"),
                [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Data   = Table.PromoteHeaders(Source, [PromoteAllScalars = true]),
```

## Dimension from a reference query

Right-click the staging query and choose **Reference**, not Duplicate. Reference
reuses the upstream steps. Duplicate copies them, and they drift apart inside a
month.

This example carves `dim_location` out of the wide Tableau extract, which is the
real Lab 0 exercise: the extract repeats site, city, state, region and datacenter
on every incident row (65,869 of them at the 24-month default), and you need 8
distinct rows.

```powerquery
let
    Source   = Staging_IncidentExtract,

    Columns  = Table.SelectColumns(Source,
                    {"site_name", "city", "state_province", "region", "datacenter"}),

    // site_name is the natural key. Distinct on it, not on the whole row,
    // or one inconsistent city spelling gives you two rows for one site.
    Distinct = Table.Distinct(Columns, {"site_name"}),

    Sorted   = Table.Sort(Distinct, {{"site_name", Order.Ascending}}),

    // Surrogate key. Index from 1, not 0, so it reads like a business key.
    Indexed  = Table.AddIndexColumn(Sorted, "location_key", 1, 1, Int64.Type),

    Reordered = Table.ReorderColumns(Indexed,
                    {"location_key", "site_name", "city", "state_province",
                     "region", "datacenter"}),

    Typed    = Table.TransformColumnTypes(Reordered, {
        {"location_key", Int64.Type},
        {"site_name", type text},
        {"city", type text},
        {"state_province", type text},
        {"region", type text},
        {"datacenter", type text}
    })
in
    Typed
```

**Folding:** `Table.SelectColumns` and `Table.Distinct` fold against SQL.
`Table.AddIndexColumn` does not, so folding stops there. That is acceptable on a
small dimension. It is not acceptable on a fact table.

Verify the key is genuinely unique before you build a relationship:

```powerquery
// Throwaway check. Paste as a new query, confirm it returns true, then delete.
Table.RowCount(dim_location) = Table.RowCount(Table.Distinct(dim_location, {"site_name"}))
```

A duplicate key here becomes a broken relationship in Lab 1.

## Fact table shaping

State the grain, then keep only the keys and the additive measures that belong at
that grain. Nothing else.

> **Grain: one row per incident.**

```powerquery
let
    Source = Staging_Incident,

    Keep   = Table.SelectColumns(Source, {
        // Keys, one per dimension
        "incident_key", "date_key", "ci_key", "service_key",
        "team_key", "location_key", "severity_key",
        // Degenerate dimension: identifies the row, has no dimension table
        "incident_number",
        // Attributes of the event itself, not of any dimension
        "incident_state", "category", "contact_type",
        // Measures
        "time_to_resolve_minutes", "reassignment_count",
        "reopened_flag", "sla_met_flag", "major_incident_flag", "incident_count"
    }),

    Typed  = Table.TransformColumnTypes(Keep, {
        {"incident_key", Int64.Type},
        {"date_key", Int64.Type},
        {"ci_key", Int64.Type},
        {"service_key", Int64.Type},
        {"team_key", Int64.Type},
        {"location_key", Int64.Type},
        {"severity_key", Int64.Type},
        {"incident_number", type text},
        {"incident_state", type text},
        {"category", type text},
        {"contact_type", type text},
        {"time_to_resolve_minutes", Int64.Type},
        {"reassignment_count", Int64.Type},
        {"reopened_flag", type logical},
        {"sla_met_flag", type logical},
        {"major_incident_flag", type logical},
        {"incident_count", Int64.Type}
    })
in
    Typed
```

**Folding:** yes, all the way, provided the staging query folded.

`service_name` describes the service, not the incident, so it belongs in
`dim_service` and is dropped here. `sla_target_hours` describes the severity, so
it belongs in `dim_severity`. If you cannot say "one row is one ______" in a short
phrase, the grain is wrong and every measure on top of it will be too.

## Date table

Every model needs exactly one date table, and it must be marked as the date table
on the `date` column.

```powerquery
let
    StartDate = #date(2024, 1, 1),
    EndDate   = #date(2026, 12, 31),
    DayCount  = Duration.Days(EndDate - StartDate) + 1,

    Dates  = List.Dates(StartDate, DayCount, #duration(1, 0, 0, 0)),
    Table_ = Table.FromList(Dates, Splitter.SplitByNothing(), {"date"}),
    Typed  = Table.TransformColumnTypes(Table_, {{"date", type date}}),

    DateKey   = Table.AddColumn(Typed, "date_key",
                    each Date.Year([date]) * 10000
                       + Date.Month([date]) * 100
                       + Date.Day([date]), Int64.Type),
    Year      = Table.AddColumn(DateKey,   "year",         each Date.Year([date]), Int64.Type),
    Quarter   = Table.AddColumn(Year,      "quarter",      each "Q" & Text.From(Date.QuarterOfYear([date])), type text),
    Month     = Table.AddColumn(Quarter,   "month",        each Date.Month([date]), Int64.Type),
    MonthName = Table.AddColumn(Month,     "month_name",   each Date.MonthName([date]), type text),
    MonthYear = Table.AddColumn(MonthName, "month_year",   each Date.ToText([date], "yyyy-MM"), type text),
    DayOfMth  = Table.AddColumn(MonthYear, "day_of_month", each Date.Day([date]), Int64.Type),
    DayOfWk   = Table.AddColumn(DayOfMth,  "day_of_week",  each Date.DayOfWeek([date], Day.Monday) + 1, Int64.Type),
    DayName   = Table.AddColumn(DayOfWk,   "day_name",     each Date.DayOfWeekName([date]), type text),
    Weekend   = Table.AddColumn(DayName,   "is_weekend",   each Date.DayOfWeek([date], Day.Monday) >= 5, type logical),
    WeekOfYr  = Table.AddColumn(Weekend,   "week_of_year", each Date.WeekOfYear([date]), Int64.Type),

    // Schwab fiscal year starts in January. Change the offset if that is wrong.
    FiscalYr  = Table.AddColumn(WeekOfYr,  "fiscal_year",    each Date.Year([date]), Int64.Type),
    FiscalQtr = Table.AddColumn(FiscalYr,  "fiscal_quarter", each "FY" & Text.End(Text.From(Date.Year([date])), 2)
                                                                & " Q" & Text.From(Date.QuarterOfYear([date])), type text)
in
    FiscalQtr
```

**Folding:** no. The table is generated in M, there is no source to fold to. That
is fine, it is a few hundred rows.

In the model: **Table tools -> Mark as date table** on `date`, and set
**Sort by column** so `month_name` sorts by `month`. Then turn off
**Options -> Data Load -> Auto date/time**.

## Excel folder combine

One query for the whole folder, instead of one query per file. This is the
custom-function pattern applied to the most common real problem at Schwab.

The workshop folder is `data/raw/excel/`, one capacity extract per generated month
(24 at the default). Point `MonthlyExtractFolder` at it.

```powerquery
let
    Source    = Folder.Files(MonthlyExtractFolder),

    // Only the files you mean. Extension and prefix filters both matter:
    // ~$ files are Excel lock files and will break the refresh.
    OnlyData  = Table.SelectRows(Source, each
                    (Text.EndsWith(Text.Lower([Extension]), ".csv")
                     or Text.EndsWith(Text.Lower([Extension]), ".xlsx"))
                    and not Text.StartsWith([Name], "~$")
                    and Text.StartsWith(Text.Lower([Name]), "capacity_")),

    // Derive the month from the file name: capacity_2025_11.csv -> 2025-11
    WithMonth = Table.AddColumn(OnlyData, "month_year", each
                    Text.Replace(
                        Text.BetweenDelimiters([Name], "capacity_", "."),
                        "_", "-"),
                    type text),

    Invoked   = Table.AddColumn(WithMonth, "Data",
                    each fnTransformMonthlyFile([Content], [Extension])),

    KeepCols  = Table.SelectColumns(Invoked, {"Name", "month_year", "Data"}),

    Expanded  = Table.ExpandTableColumn(KeepCols, "Data",
                    {"ci_name", "environment", "cpu_utilization_pct",
                     "memory_utilization_pct", "storage_used_gb",
                     "storage_allocated_gb"}),

    Typed     = Table.TransformColumnTypes(Expanded, {
        {"Name", type text},
        {"month_year", type text},
        {"ci_name", type text},
        {"environment", type text},
        {"cpu_utilization_pct", type number},
        {"memory_utilization_pct", type number},
        {"storage_used_gb", type number},
        {"storage_allocated_gb", type number}
    })
in
    Typed
```

**Folding:** no. File and folder sources do not fold. Keep the steps few and the
files small, and prefer a SQL source when one exists.

### The companion function

Create this with **New Query -> Blank Query -> Advanced Editor**, and name it
`fnTransformMonthlyFile`. Every column is referenced **by name**, never by
position, because a source that adds a column in the middle would silently shift
every positional reference.

```powerquery
(FileContent as binary, optional FileExtension as text) as table =>
let
    Ext = Text.Lower(FileExtension ?? ".csv"),

    Raw =
        if Ext = ".csv" then
            Table.PromoteHeaders(
                Csv.Document(FileContent,
                    [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
                [PromoteAllScalars = true])
        else
            let
                Workbook = Excel.Workbook(FileContent, null, true),
                // By sheet name, not by index. Index breaks when a tab is added.
                Sheet    = Workbook{[Item = "Data", Kind = "Sheet"]}[Data]
            in
                Table.PromoteHeaders(Sheet, [PromoteAllScalars = true]),

    Guarded  = fnGuardCapacitySchema(Raw),

    // Rename to model names. Reference columns BY NAME.
    Renamed  = Table.RenameColumns(Guarded, {
        {"CI Name",              "ci_name"},
        {"Environment",          "environment"},
        {"CPU %",                "cpu_utilization_pct"},
        {"Memory %",             "memory_utilization_pct"},
        {"Storage Used GB",      "storage_used_gb"},
        {"Storage Allocated GB", "storage_allocated_gb"}
    }),

    Selected = Table.SelectColumns(Renamed, {
        "ci_name", "environment", "cpu_utilization_pct",
        "memory_utilization_pct", "storage_used_gb", "storage_allocated_gb"
    })
in
    Selected
```

## Schema guard

A wrong number that looks right is worse than an error. Make the query fail
loudly when the source changes shape, and handle the changes you already know
about.

The November file in `data/raw/excel/` is deliberately different. It renames
`CPU %` to `CPU Utilisation %` and appends a stray `TOTAL` row with a null
`CI Name` for every other column. Left alone, that row inflates your CI count by
one and drags the average CPU figure toward the mean it already contains.

Name this query `fnGuardCapacitySchema`:

```powerquery
(Source as table) as table =>
let
    Actual = Table.ColumnNames(Source),

    // 1. Known alias. The November extract renamed one column. Normalise it,
    //    do not error on it.
    Aliases = {
        {"CPU Utilisation %", "CPU %"},
        {"CPU Utilization %", "CPU %"},
        {"Mem %",             "Memory %"}
    },
    ApplicableAliases = List.Select(Aliases, each List.Contains(Actual, _{0})),
    Normalised = Table.RenameColumns(Source, ApplicableAliases),

    // 2. Hard requirement. Anything still missing is a real breaking change.
    Expected = {"CI Name", "Environment", "CPU %", "Memory %",
                "Storage Used GB", "Storage Allocated GB"},
    Missing  = List.Difference(Expected, Table.ColumnNames(Normalised)),

    Checked =
        if List.IsEmpty(Missing) then
            Normalised
        else
            error Error.Record(
                "Capacity extract schema changed",
                "Missing expected columns: " & Text.Combine(Missing, ", "),
                "Found: " & Text.Combine(Table.ColumnNames(Normalised), ", ")
                    & ". Fix the source file or add an alias to fnGuardCapacitySchema."
            ),

    // 3. Strip the stray total row. Detected two ways, so a renamed marker or a
    //    blank CI Name is both caught.
    NoTotals = Table.SelectRows(Checked, each
                    [CI Name] <> null
                    and Text.Trim(Text.Upper(Text.From([CI Name]))) <> "TOTAL"
                    and [Environment] <> null)
in
    NoTotals
```

**Folding:** no. Both branches inspect the table, which forces local evaluation.
Run it against the already-small per-file table, as the function above does, not
against a combined multi-million-row table.

Three habits worth keeping from this snippet:

- **Normalise what you know, error on what you do not.** Aliasing every unknown
  column defeats the purpose.
- **Put the actual column list in the error message.** Whoever hits this at 6am
  should not have to open the file to see what changed.
- **Remove total rows explicitly.** They are the single most common cause of a
  double-counted extract.

## Incremental refresh parameters

Required for incremental refresh on large fact tables. The names must be exactly
`RangeStart` and `RangeEnd`, and both must be type `datetime`.

Create them under **Home -> Manage parameters**, then apply the filter to the
staging source so it folds:

```powerquery
let
    Source   = Sql.Database(ServerName, DatabaseName),
    Data     = Source{[Schema = "dbo", Item = "vw_incident"]}[Data],

    // RangeStart is inclusive, RangeEnd is exclusive. Getting this wrong
    // double-counts or drops the boundary rows.
    Windowed = Table.SelectRows(Data, each
                    [opened_at] >= RangeStart and [opened_at] < RangeEnd)
in
    Windowed
```

**Folding:** this step must fold. Verify with **View Native Query** before you
configure the policy. Without folding, incremental refresh will pull the whole
table on every partition and be slower than a full refresh.

Then right-click the table in Power BI Desktop, choose **Incremental refresh**,
and set the archive and refresh windows. Requirements: a foldable query, a
reliable date or datetime column, and a source that supports query folding.

---

## Contributing

This library belongs to the Community of Practice. When you add a snippet:

- Say what it does in one line, and when to use it.
- Use parameters, not hardcoded servers or paths.
- Set explicit data types on every column you touch.
- State whether it folds.
- Reference columns by name, never by position.
- Keep it short enough that a reviewer can read it in a minute.

## Related

- [Lab 0 - Connect, shape, and load with Power Query](../../labs/lab-00-connect-and-shape/README.md)
- [Lab 1 - Build the semantic model](../../labs/lab-01-semantic-model/README.md)
- [Star schema](../../reference/star-schema.md)
- [M365 Copilot for Power BI work](../../reference/copilot-in-power-bi.md)
- [Dataset documentation](../../data/README.md)
- [Sources](../../reference/sources.md)
