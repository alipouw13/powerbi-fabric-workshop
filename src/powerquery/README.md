# Power Query M snippet library

Because there is no Lakehouse, no Dataflow Gen2, and no pipeline layer, **every
transformation at Schwab happens in Power Query**. Without a shared Dataflow to
inherit logic from, the practical substitute is a shared snippet library.

This is that library. It is deliberately low-tech: paste into the **Advanced
Editor**, adjust the names, verify the result. It is used in
[Lab 5](../../labs/lab-05-ingestion-onelake/README.md) and extended in
[Lab 7](../../labs/lab-07-copilot-reports/README.md).

> **Before you paste anything.** Check row count, new nulls, explicit data types,
> and whether query folding survived. Then rename the generated steps so a
> colleague can read them.

## Contents

| Snippet | Use |
| --- | --- |
| [Staging query](#staging-query) | The one source query everything else references |
| [Dimension from a reference query](#dimension-from-a-reference-query) | Build conformed dimensions without duplicating logic |
| [Fact table shaping](#fact-table-shaping) | Reduce a wide source to a proper fact grain |
| [Date table](#date-table) | Generate dim_date in M |
| [Excel folder combine](#excel-folder-combine) | One query for a folder of monthly workbooks |
| [Schema guard](#schema-guard) | Fail loudly instead of producing silent nulls |
| [Incremental refresh parameters](#incremental-refresh-parameters) | RangeStart / RangeEnd for large facts |

---

## Staging query

Load this once, disable load, and reference it everywhere else. This is the
single most important structural habit in the library.

```powerquery
let
    Source = Sql.Database(ServerName, DatabaseName),
    Data   = Source{[Schema = "dbo", Item = "vw_policy_claims"]}[Data],

    // Filter and remove columns FIRST so these steps fold back to SQL.
    Filtered = Table.SelectRows(Data, each [period_begin] >= ReportingStartDate),
    Trimmed  = Table.SelectColumns(Filtered, {
        "policy_id", "policy_number", "customer_id", "agent_id", "coverage_id",
        "date_id", "period_begin", "product", "region", "channel",
        "written_premium", "earned_premium", "incurred_loss", "paid_loss", "claim_id"
    }),
    Typed = Table.TransformColumnTypes(Trimmed, {
        {"policy_id", Int64.Type},
        {"period_begin", type date},
        {"written_premium", Currency.Type},
        {"earned_premium", Currency.Type},
        {"incurred_loss", Currency.Type},
        {"paid_loss", Currency.Type}
    })
in
    Typed
```

Right-click the query and untick **Enable load**. It is scaffolding, not a table.

`ServerName`, `DatabaseName`, and `ReportingStartDate` are parameters - see
[Lab 5 step 6](../../labs/lab-05-ingestion-onelake/README.md).

## Dimension from a reference query

Right-click the staging query and choose **Reference**, not Duplicate. Reference
reuses the upstream steps; Duplicate copies them and they drift apart within a
month.

```powerquery
let
    Source   = Staging_PolicyClaims,
    Columns  = Table.SelectColumns(Source, {"policy_id", "policy_number", "product", "customer_id"}),
    Distinct = Table.Distinct(Columns, {"policy_id"}),
    Typed    = Table.TransformColumnTypes(Distinct, {
        {"policy_id", Int64.Type},
        {"policy_number", type text},
        {"product", type text}
    })
in
    Typed
```

Verify the key is genuinely unique before you move on. A duplicate key here
becomes a broken relationship in Lab 6.

```powerquery
// Throwaway check - paste as a new query, confirm it returns true, then delete.
Table.RowCount(dim_policy) = Table.RowCount(Table.Distinct(dim_policy, {"policy_id"}))
```

## Fact table shaping

Keep the grain keys and the additive measures. Nothing else.

```powerquery
let
    Source = Staging_PolicyClaims,
    Keep   = Table.SelectColumns(Source, {
        "policy_id", "agent_id", "date_id", "written_premium", "earned_premium"
    }),
    Typed  = Table.TransformColumnTypes(Keep, {
        {"policy_id", Int64.Type},
        {"agent_id", Int64.Type},
        {"date_id", Int64.Type},
        {"written_premium", Currency.Type},
        {"earned_premium", Currency.Type}
    })
in
    Typed
```

If a column describes the policy rather than measuring the event, it belongs in
`dim_policy`. State the grain in one sentence: *one row per policy, per agent,
per period.* If you cannot, the grain is wrong.

## Date table

Every model needs exactly one date table, marked as the date table.

```powerquery
let
    StartDate = #date(2019, 1, 1),
    EndDate   = #date(2026, 12, 31),
    DayCount  = Duration.Days(EndDate - StartDate) + 1,

    Dates  = List.Dates(StartDate, DayCount, #duration(1, 0, 0, 0)),
    Table_ = Table.FromList(Dates, Splitter.SplitByNothing(), {"period_begin"}),
    Typed  = Table.TransformColumnTypes(Table_, {{"period_begin", type date}}),

    Added = Table.AddColumn(Typed, "date_id",    each Date.Year([period_begin]) * 10000
                                                    + Date.Month([period_begin]) * 100
                                                    + Date.Day([period_begin]), Int64.Type),
    Year  = Table.AddColumn(Added, "year",       each Date.Year([period_begin]), Int64.Type),
    Qtr   = Table.AddColumn(Year,  "quarter",    each "Q" & Text.From(Date.QuarterOfYear([period_begin])), type text),
    Mth   = Table.AddColumn(Qtr,   "month",      each Date.Month([period_begin]), Int64.Type),
    MName = Table.AddColumn(Mth,   "month_name", each Date.MonthName([period_begin]), type text)
in
    MName
```

In the model: mark as date table on `period_begin`, and sort `month_name` by
`month`.

## Excel folder combine

One query for a folder of monthly workbooks, instead of one query per file. This
is the custom-function pattern applied to the most common real problem.

```powerquery
let
    Source     = Folder.Files(MonthlyExtractFolder),
    OnlyExcel  = Table.SelectRows(Source, each Text.EndsWith([Extension], ".xlsx")),
    NotTemp    = Table.SelectRows(OnlyExcel, each not Text.StartsWith([Name], "~$")),

    Invoked    = Table.AddColumn(NotTemp, "Data", each fnTransformMonthlyFile([Content])),
    KeepCols   = Table.SelectColumns(Invoked, {"Name", "Data"}),
    Expanded   = Table.ExpandTableColumn(KeepCols, "Data",
                    {"policy_number", "product", "region", "written_premium"}),
    Typed      = Table.TransformColumnTypes(Expanded, {
        {"policy_number", type text},
        {"written_premium", Currency.Type}
    })
in
    Typed
```

The companion function, created with **Create Function** from a working query:

```powerquery
(FileContent as binary) as table =>
let
    Workbook  = Excel.Workbook(FileContent, null, true),
    Sheet     = Workbook{[Item = "Data", Kind = "Sheet"]}[Data],
    Promoted  = Table.PromoteHeaders(Sheet, [PromoteAllScalars = true]),
    // Reference columns by NAME, never by position.
    Selected  = Table.SelectColumns(Promoted,
                    {"policy_number", "product", "region", "written_premium"})
in
    Selected
```

Excel sources rarely fold. Keep the steps few and the files small.

## Schema guard

A wrong number that looks right is worse than an error. Make the query fail
loudly when the source changes shape.

```powerquery
let
    Source   = Excel_Monthly,
    Expected = {"policy_number", "product", "region", "written_premium"},
    Actual   = Table.ColumnNames(Source),
    Missing  = List.Difference(Expected, Actual),

    Checked =
        if List.IsEmpty(Missing) then
            Source
        else
            error Error.Record(
                "Source schema changed",
                "Missing expected columns: " & Text.Combine(Missing, ", "),
                "Check the source file before refreshing."
            )
in
    Checked
```

## Incremental refresh parameters

Required for incremental refresh on large fact tables. The names must be exactly
`RangeStart` and `RangeEnd`, and both must be `datetime`.

```powerquery
// In the fact query, applied to the staging source so the filter folds.
Table.SelectRows(
    Source,
    each [period_begin] >= RangeStart and [period_begin] < RangeEnd
)
```

Incremental refresh also needs a folding query and a reliable date column. Verify
folding with **View Native Query** before configuring the policy - without it,
incremental refresh will not behave as expected.

---

## Contributing

This library belongs to the community of practice chartered in
[Lab 12](../../labs/lab-12-showcase-next-steps/README.md). When you add a snippet:

- Say what it does in one line, and when to use it.
- Use parameters, not hardcoded servers or paths.
- Set explicit data types.
- Note whether it folds.
- Keep it short enough that a reviewer can read it in a minute.
