# Power Query M snippet library

There is no lake layer and no Dataflow in this environment, so **every
transformation in this workshop happens in Power Query**. Without a shared Dataflow
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
| [Cleaning a dirty export](#cleaning-a-dirty-export) | Preamble rows, text numbers, mixed dates, total rows | No |
| [Unpivot a cross-tab](#unpivot-a-cross-tab) | Months across the columns, blanked group labels | No |
| [Two-row headers](#two-row-headers) | The header split over two rows | No |
| [Incremental refresh parameters](#incremental-refresh-parameters) | RangeStart and RangeEnd for large facts | Must fold |

Parameters used throughout: `ServerName`, `DatabaseName`, `ReportingStartDate`,
`MonthlyExtractFolder`, `DirtyFolder`. Create them under
**Home -> Manage parameters** so nothing is hardcoded.

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

    // This fiscal year starts in January. Change the offset if that is wrong.
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
custom-function pattern applied to the most common real problem in this environment.

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

## Cleaning a dirty export

For `data/raw/dirty/incident_export_dirty.csv` and anything shaped like it: junk
rows above the header, numbers stored as text, several date formats in one
column, five vocabularies for true and false, duplicates, and a total row.

The full defect list per file is in
[`data/power-query-cleanup.md`](../../data/power-query-cleanup.md).

```powerquery
let
    Source     = Csv.Document(File.Contents(DirtyFolder & "\incident_export_dirty.csv"),
                    [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),

    // 1. Shape first, types last. Four preamble rows, then the real header.
    NoPreamble = Table.Skip(Source, 4),
    Promoted   = Table.PromoteHeaders(NoPreamble, [PromoteAllScalars = true]),

    // 2. Header names arrive padded and shouting.
    CleanNames = Table.TransformColumnNames(Promoted, Text.Trim),

    // 3. Drop the footer and the total row before anything reads the values.
    NoFooter   = Table.SelectRows(CleanNames, each
                    [Incident Number] <> null
                    and [Incident Number] <> ""
                    and not Text.StartsWith(Text.Upper(Text.Trim([Incident Number])), "TOTAL")
                    and not Text.StartsWith([Incident Number], "Generated by")
                    and not Text.StartsWith([Incident Number], "Confidential")),

    // 4. Trim every text cell once, rather than column by column.
    Trimmed    = Table.TransformColumns(NoFooter,
                    List.Transform(Table.ColumnNames(NoFooter),
                        (c) => {c, each if _ is text then Text.Trim(_) else _, type any})),

    // 5. Now the duplicates are actually detectable.
    NoDupes    = Table.Distinct(Trimmed),

    // 6. Every token that means "nothing" becomes null, in one pass.
    //    Csv.Document gives you "" not null, so "" has to be in the list.
    NullTokens = {"", "-", "N/A", "n/a", "NULL", "#N/A"},
    Nulls      = Table.TransformColumns(NoDupes,
                    List.Transform(Table.ColumnNames(NoDupes),
                        (c) => {c, each
                            if _ is text and List.Contains(NullTokens, _) then null else _,
                            type any})),

    // 7. Thousands separators are why this column is text.
    Numbers    = Table.TransformColumns(Nulls, {
                    {"Resolve Minutes", each if _ = null then null
                        else Text.Remove(Text.From(_), {","}), type nullable text}}),

    // 8. Five vocabularies, one logical. A list beats a nested if.
    Truthy     = {"Y", "YES", "TRUE", "1"},
    Falsy      = {"N", "NO", "FALSE", "0"},
    SlaFlag    = Table.TransformColumns(Numbers, {
                    {"SLA Met", each
                        if _ = null then null
                        else if List.Contains(Truthy, Text.Upper(Text.From(_))) then true
                        else if List.Contains(Falsy,  Text.Upper(Text.From(_))) then false
                        else null, type nullable logical}}),

    // 9. Severity: trim already done, so casing is all that is left.
    Severity   = Table.TransformColumns(SlaFlag, {{"SEVERITY", Text.Upper, type text}}),

    // 10. Two attributes in one column.
    SplitSite  = Table.SplitColumn(Severity, "Site / State",
                    Splitter.SplitTextByDelimiter(" / ", QuoteStyle.Csv),
                    {"site_name", "state_province"}),

    // 11. Three date formats, tried in order. try/otherwise beats guessing.
    Dates      = Table.TransformColumns(SplitSite, {
                    {"Opened Date", each
                        if _ = null then null else
                        try Date.FromText(Text.From(_), [Format = "MM/dd/yyyy", Culture = "en-US"])
                        otherwise try Date.FromText(Text.From(_), [Format = "yyyy-MM-dd", Culture = "en-US"])
                        otherwise try Date.FromText(Text.From(_), [Format = "dd-MMM-yyyy", Culture = "en-US"])
                        otherwise null,
                        type nullable date}}),

    // 12. The column that is null on every row.
    Dropped    = Table.RemoveColumns(Dates, {"Notes"}, MissingField.Ignore),

    Typed      = Table.TransformColumnTypes(Dropped, {
                    {"Incident Number", type text},
                    {"Resolve Minutes", Int64.Type},
                    {"Reassignments", Int64.Type}})
in
    Typed
```

**Folding:** no. It is a file source, and half these steps inspect values.

Three things this snippet is trying to teach:

- **Shape, then dedupe, then type.** Deduping padded text finds nothing, and
  typing before the total row is removed turns that row into an error cell that
  propagates.
- **`try ... otherwise` for date formats**, not a conditional column per format.
  Adding a fourth format later is one more line, in one place.
- **A list membership test for booleans**, not nested ifs. `Truthy` and `Falsy`
  are readable, and someone can extend them without re-reading the logic.

### Verify

```powerquery
// Throwaway checks. Each should return true.
Table.RowCount(Typed) = Table.RowCount(Table.Distinct(Typed))
List.Count(List.Select(Table.Column(Typed, "Opened Date"), each _ = null)) = 0
List.Count(List.Distinct(Table.Column(Typed, "SEVERITY"))) = 4
```

## Unpivot a cross-tab

For `data/raw/dirty/capacity_by_month_crosstab.csv`: one column per month, group
labels blanked on repeat rows, a `Total` column and a `Grand Total` row.

**The order is the whole snippet.** Fill down, remove the total column, filter the
total row, *then* unpivot.

```powerquery
let
    Source     = Csv.Document(File.Contents(DirtyFolder & "\capacity_by_month_crosstab.csv"),
                    [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),
    Promoted   = Table.PromoteHeaders(Table.Skip(Source, 3), [PromoteAllScalars = true]),

    // 1. Blank group labels first. Unpivot before this and they become nulls.
    //    Csv.Document returns "" rather than null, and FillDown only fills nulls.
    Blanks     = Table.ReplaceValue(Promoted, "", null, Replacer.ReplaceValue,
                    {"Business Unit", "Service"}),
    Filled     = Table.FillDown(Blanks, {"Business Unit", "Service"}),

    // 2. The Total column would unpivot into a thirteenth month.
    NoTotalCol = Table.RemoveColumns(Filled, {"Total"}, MissingField.Ignore),

    // 3. The Grand Total row would double the totals.
    NoTotalRow = Table.SelectRows(NoTotalCol, each
                    [Business Unit] <> "Grand Total" and [CI Name] <> null),

    // 4. Now, and only now, unpivot.
    Unpivoted  = Table.UnpivotOtherColumns(NoTotalRow,
                    {"Business Unit", "Service", "CI Name"}, "month", "cpu_pct_text"),

    // 5. "72.4%" is text. Strip the sign, then type it.
    NoPercent  = Table.TransformColumns(Unpivoted, {
                    {"cpu_pct_text", each
                        if _ = null or Text.Upper(Text.From(_)) = "N/A" then null
                        else Text.Remove(Text.From(_), {"%"}), type nullable text}}),

    // 6. "Feb-2026" is text too. Parse to the first of the month.
    MonthDate  = Table.AddColumn(NoPercent, "month_start", each
                    try Date.FromText("01-" & Text.From([month]),
                        [Format = "dd-MMM-yyyy", Culture = "en-US"])
                    otherwise null, type nullable date),

    Typed      = Table.TransformColumnTypes(MonthDate, {
                    {"Business Unit", type text}, {"Service", type text},
                    {"CI Name", type text}, {"cpu_pct_text", type number}}),
    Renamed    = Table.RenameColumns(Typed, {{"cpu_pct_text", "cpu_utilization_pct"}})
in
    Renamed
```

**Folding:** no.

**Verify:** row count = CIs × months, five columns out, no null `Business Unit`,
and an average CPU in the 30 to 70 range. In the thousands means the `%` was
stripped without a type change.

## Two-row headers

For `data/raw/dirty/service_desk_daily_dirty.csv`, and for every Excel export
where somebody merged cells across a group of columns.

Transpose the two header rows, fill the group label down, merge the pair, then
transpose back and promote.

```powerquery
let
    Source     = Csv.Document(File.Contents(DirtyFolder & "\service_desk_daily_dirty.csv"),
                    [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),

    HeaderRows = Table.FirstN(Source, 2),
    BodyRows   = Table.Skip(Source, 2),

    Flipped    = Table.Transpose(HeaderRows),
    // The group label appears only on the first column of each group, and
    // Csv.Document gives "" rather than null, which FillDown ignores.
    Blanks     = Table.ReplaceValue(Flipped, "", null, Replacer.ReplaceValue, {"Column1"}),
    Filled     = Table.FillDown(Blanks, {"Column1"}),
    Merged     = Table.CombineColumns(Filled, {"Column1", "Column2"},
                    each Text.Trim(Text.Combine(
                        List.Select(_, (v) => v <> null and v <> ""), " ")),
                    "header"),
    NewHeader  = Table.Transpose(Merged),

    Rebuilt    = Table.Combine({NewHeader, BodyRows}),
    Promoted   = Table.PromoteHeaders(Rebuilt, [PromoteAllScalars = true]),

    // Keep the columns you mean, by name. Fill Down gave the trailing Notes
    // column the "Quality" prefix it inherited from its neighbour; naming what
    // you want is safer than guessing what to drop.
    Named      = Table.SelectColumns(Promoted, {
                    "Date", "Team", "Site",
                    "Tickets Received", "Tickets Resolved", "Tickets First Contact",
                    "Staffing Scheduled", "Staffing Available",
                    "Quality Avg Handle (min)"}),

    // Totals row, then the text numbers.
    NoTotals   = Table.SelectRows(Named, each [Date] <> null and [Team] <> "Totals"),
    Numbers    = Table.TransformColumns(NoTotals,
                    List.Transform(
                        {"Tickets Received", "Tickets Resolved", "Tickets First Contact"},
                        (c) => {c, each
                            if _ = null or Text.Trim(Text.From(_)) = "-" then 0
                            else Number.FromText(Text.Remove(Text.Trim(Text.From(_)), {","})),
                            Int64.Type}))
in
    Numbers
```

**Folding:** no. `Table.Transpose` reads the whole table into memory, so run it
on the header rows alone, never on the full table.

**Verify:** every column name is unique and readable, no `Column1` survives, and
your own sum of `Tickets Received` matches the figure that was in the deleted
`Totals` row.

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
- [Dirty-file catalogue and fixes](../../data/power-query-cleanup.md)
- [Lab 1 - Build the semantic model](../../labs/lab-01-semantic-model/README.md)
- [Star schema](../../reference/star-schema.md)
- [M365 Copilot for Power BI work](../../reference/copilot-in-power-bi.md)
- [Dataset documentation](../../data/README.md)
- [Sources](../../reference/sources.md)
