# Shape 4: the dirty exports

`data/raw/dirty/` holds four files that are **wrong on purpose**. Nothing in them
can be modelled until it has been cleaned, and every defect has one specific
Power Query fix.

This is the file set for showing what Power Query is actually for. The
`data/raw/sql/` tables are already clean, so they demonstrate modeling but not
transformation. These four demonstrate transformation.

## Synthetic data notice

Same as the rest of the dataset: every value here is generated. No customer,
account, position, trade, or market data. See [data/README.md](README.md).

## The files

| File | Rows | Headline problem | The Power Query answer |
| --- | ---: | --- | --- |
| `incident_export_dirty.csv` | ~305 | Junk preamble above the header | Remove Top Rows, Use First Row as Headers |
| `capacity_by_month_crosstab.csv` | ~25 | Months across the columns | Unpivot Other Columns, Fill Down |
| `asset_inventory_dirty.csv` | ~256 | Currency and dates stored as text | Replace Values, Split Column, typed conversion |
| `service_desk_daily_dirty.csv` | ~122 | A two-row header | Transpose, Fill Down, Merge, Transpose back |

Row counts move with `--months` and `--ci-count`. The *defects* do not.

> **Every one of these produces a plausible-looking wrong number if you skip the
> cleanup.** That is the point. A refresh that errors gets fixed on Monday; a
> refresh that quietly averages 40% of its rows gets presented to a steering
> committee.

---

## 1. `incident_export_dirty.csv`

A ServiceNow-style export, dumped straight from the UI.

| # | Defect | Fix |
| --- | --- | --- |
| 1 | Four preamble rows (title, run time, filter) above the real header | **Home → Remove Rows → Remove Top Rows** = 4, then **Use First Row as Headers** |
| 2 | Column names carry leading and trailing spaces: `Incident Number `, ` Opened Date` | **Transform → Rename**, or `Table.TransformColumnNames(Source, Text.Trim)` |
| 3 | `Opened Date` in three formats: `03/15/2026`, `2026-03-15`, `15-Mar-2026` | **Split** by format, or `Date.From` with a locale, or a `try ... otherwise` cascade |
| 4 | `Site / State` is two attributes in one column | **Split Column → By Delimiter** ` / ` |
| 5 | `SEVERITY` inconsistently cased and padded: `SEV3`, `sev3`, `Sev3`, ` SEV3`, `SEV3 ` | **Format → Trim**, then **Format → UPPERCASE** |
| 6 | `Resolve Minutes` has thousands separators (`1,325`) so it types as text | **Replace Values** `,` → nothing, then Whole Number |
| 7 | Open incidents show `N/A`, `-` or blank in the same column | **Replace Values** → `null` before the type change |
| 8 | `SLA Met` uses five different truth vocabularies: `Yes/No`, `Y/N`, `TRUE/FALSE`, `1/0`, `yes/no` | **Add Conditional Column**, or a `List.Contains` lookup |
| 9 | Blank rows scattered through the data | **Remove Rows → Remove Blank Rows** |
| 10 | Exact duplicate rows from a re-run append | **Remove Rows → Remove Duplicates** |
| 11 | A `Notes` column that is null on every row | **Remove Columns**, or `Table.SelectColumns` |
| 12 | A `TOTAL` row and two footer lines at the bottom | **Filter** `Incident Number` does not begin with `TOTAL` and is not null |

### Verify

- Row count after cleanup equals the incident count, with no blanks, no
  duplicates and no `TOTAL`.
- `Opened Date` is type Date, with **zero** errors. One error means a format was
  missed.
- `SLA Met` has exactly three distinct values: true, false, null.
- `Severity` has exactly four distinct values.

---

## 2. `capacity_by_month_crosstab.csv`

The report-writer output that arrives every month by email. Human-readable,
model-hostile.

| # | Defect | Fix |
| --- | --- | --- |
| 1 | Three preamble rows above the header | **Remove Top Rows** = 3, **Use First Row as Headers** |
| 2 | One column per month (`Feb-2026`, `Mar-2026`, ...) | Select `Business Unit`, `Service`, `CI Name` → **Unpivot Other Columns** |
| 3 | `Business Unit` and `Service` are blank on repeat rows | **Transform → Fill → Down**, *before* the unpivot. In M, replace `""` with `null` first — `Table.FillDown` only fills nulls |
| 4 | A `Total` column on the right | **Remove Columns** *before* the unpivot, or it becomes fake rows |
| 5 | A `Grand Total` row at the bottom | **Filter** `Business Unit` ≠ `Grand Total` |
| 6 | Values are text with a `%` suffix: `72.4%` | **Replace Values** `%` → nothing, type Decimal, divide by 100 if you want a true percentage |
| 7 | Scattered `n/a` cells | **Replace Values** → `null`, then decide whether to keep or filter the row |
| 8 | The unpivoted month is text `Feb-2026`, not a date | **Add Column → Column From Examples**, or `Date.FromText` with a custom format |

### The order that matters

Fill Down → remove the `Total` column → filter the `Grand Total` row → **then**
unpivot. Unpivot first and the total column turns into a thirteenth month, and
every blank group label becomes a null category.

### Verify

- Output is exactly `Business Unit`, `Service`, `CI Name`, `month`, `cpu_pct` —
  five columns, long and narrow.
- Row count = CIs × months, minus any `n/a` you chose to drop.
- No row where `Business Unit` is null.
- Average CPU is in the 30–70 range. In the thousands means the `%` was stripped
  without a type change; under 1 means it was divided twice.

---

## 3. `asset_inventory_dirty.csv`

An asset register exported by finance. Numbers that look like numbers, and are
not.

| # | Defect | Fix |
| --- | --- | --- |
| 1 | `Asset Tag` padded, or prefixed `'` (the Excel text marker), or ending in a non-breaking space | **Trim** does not remove U+00A0. `Text.Remove([Asset Tag], {"'", Character.FromNumber(160)})` then Trim |
| 2 | `Location` is `City, State, Country` in one cell | **Split Column → By Delimiter** `, ` into 3 |
| 3 | Dates in three formats: `2022-02-14`, `14-Feb-2023`, `March 15, 2024` | `try Date.FromText(...) otherwise` cascade, or split by pattern first |
| 4 | `Acquisition Cost` as `$12,450.00`, `USD 12,450.00`, or `12,450.00 ` | **Replace Values** for `$`, `USD `, `,` then Trim, then Decimal |
| 5 | `Annual Support Cost` uses accounting brackets for credits: `(1,382.85)` | Conditional column: brackets → negative. Typing it directly gives an error, not a minus |
| 6 | `Lifecycle Status` in five spellings: `In Service`, `in service`, `IN-SERVICE`, `InService`, ` In Service ` | Trim → Replace `-` with space → a mapping table, **not** a chain of nested ifs |
| 7 | `Under Warranty` uses `Yes/No`, `Y/N`, `TRUE/FALSE`, `1/0`, `yes/no` | Conditional column to a real logical |
| 8 | Missing costs shown as `NULL`, `#N/A`, `n/a`, `-` or blank | **Replace Values** → `null` for each token before typing |
| 9 | Exact duplicate rows, appended by a re-run | **Remove Duplicates** — but only after step 1, or the padding hides them |
| 10 | A footer note row at the bottom | Filter out rows where `CI Name` is null |

> **Step 9 is the trap.** ` AST000001 ` and `AST000001` are different strings.
> Remove Duplicates before you clean the whitespace and it removes nothing, and
> reports success while doing it.

### Verify

- `Lifecycle Status` has exactly four distinct values.
- `Under Warranty` is type True/False with no nulls.
- `Acquisition Cost` is Decimal, non-negative, with errors only where the source
  was genuinely blank.
- `Annual Support Cost` contains negatives — and they are the rows that were in
  brackets. Count them before and after.
- The distinct `Asset Tag` count equals the row count.

---

## 4. `service_desk_daily_dirty.csv`

The two-row header. Everyone has one of these, and almost nobody knows the fix.

| # | Defect | Fix |
| --- | --- | --- |
| 1 | Row 1 groups columns (`Tickets`, `Staffing`, `Quality`), row 2 names them | **Transpose → Fill Down → Merge Columns → Transpose → Use First Row as Headers** |
| 2 | Ticket counts have thousands separators and trailing spaces | Trim, **Replace Values** `,` → nothing, Whole Number |
| 3 | `First Contact` shows `-` where a zero belongs | **Replace Values** `-` → `0` before typing |
| 4 | A trailing `Notes` column, empty on every row. Fill Down gives it the `Quality` prefix, so it arrives as `Quality Notes` | **Remove Columns**, or `Table.SelectColumns` on the names you want |
| 5 | A `Totals` row at the bottom | Filter `Date` is not null, or `Team` ≠ `Totals` |
| 6 | `Date` as `12-Jul-2026` text | Type Date with locale English (United States) |

### The two-row header recipe

```powerquery
let
    Source     = Csv.Document(File.Contents(DirtyFolder & "\service_desk_daily_dirty.csv"),
                    [Delimiter = ",", Encoding = 65001, QuoteStyle = QuoteStyle.Csv]),

    // Work on the two header rows only, then put them back.
    HeaderRows = Table.FirstN(Source, 2),
    BodyRows   = Table.Skip(Source, 2),

    Flipped    = Table.Transpose(HeaderRows),
    // Csv.Document returns "" for an empty cell, and FillDown only fills nulls.
    Blanks     = Table.ReplaceValue(Flipped, "", null, Replacer.ReplaceValue, {"Column1"}),
    // The group label only appears on the first column of each group.
    Filled     = Table.FillDown(Blanks, {"Column1"}),
    Merged     = Table.CombineColumns(Filled, {"Column1", "Column2"},
                    each Text.Trim(Text.Combine(List.Select(_, (v) => v <> null and v <> ""), " ")),
                    "header"),
    NewHeaders = Table.Transpose(Merged),

    Rebuilt    = Table.Combine({NewHeaders, BodyRows}),
    Promoted   = Table.PromoteHeaders(Rebuilt, [PromoteAllScalars = true])
in
    Promoted
```

Result: `Date`, `Team`, `Site`, `Tickets Received`, `Tickets Resolved`,
`Tickets First Contact`, `Staffing Scheduled`, `Staffing Available`,
`Quality Avg Handle (min)`, and `Quality Notes` — which you then drop, because it
is empty on every row.

Note what Fill Down did to the last column. It had no group label of its own, so
it inherited `Quality` from its neighbour. That is Fill Down working correctly and
still giving you a column name nobody wants. Select the columns you need by name
rather than trying to guess which ones to remove.

### Verify

- Column names are unique and readable. No `Column1`.
- `Tickets Received` is Whole Number with zero errors.
- The `Totals` row is gone, and your own sum of `Tickets Received` matches the
  figure that was in it. If it does not, rows were dropped.

---

## Reconciliation

Every dirty file is derived from the clean tables in `data/raw/sql/`, so there is
a right answer to check against.

| Dirty file | Reconcile against | On what |
| --- | --- | --- |
| `incident_export_dirty.csv` | `fact_incident.csv` | Count of `incident_number`, sum of `time_to_resolve_minutes` |
| `capacity_by_month_crosstab.csv` | `fact_capacity.csv` | Average `cpu_utilization_pct` by `month_year` |
| `asset_inventory_dirty.csv` | `fact_asset.csv` | Count of `asset_tag`, sum of `acquisition_cost_usd` |
| `service_desk_daily_dirty.csv` | `fact_service_desk.csv` | Sum of `tickets_received` by date |

The dirty files are samples, not the full facts, so filter the clean table to the
same rows before comparing. The sample sizes are printed by the generator.

## How to use these in a session

1. **Ten-minute demo.** Open `incident_export_dirty.csv`, do defects 1, 2, 9, 10
   and 12 live. Five clicks, and the table becomes loadable. That is the pitch.
2. **Group exercise.** One file per group, 25 minutes, each group demos its
   applied-steps list. The lists will differ, and comparing them is the lesson.
3. **Copilot exercise.** Paste the defect list for one file into your Query
   Engineer tab and ask for the M. Then check row count, nulls, types and step
   names, as [Lab 0](../labs/lab-00-connect-and-shape/README.md) requires. This
   is the best available demonstration of why "verify the generated M" is not
   optional.
4. **Schema-guard follow-on.** Add the [schema guard](../src/powerquery/README.md#schema-guard)
   over the cleaned query, then edit the source file to rename a column and watch
   it fail loudly rather than silently.

## Related

- [Dataset documentation](README.md)
- [Lab 0 - Connect, shape, and load](../labs/lab-00-connect-and-shape/README.md)
- [Power Query snippet library](../src/powerquery/README.md) - working M for
  [dirty exports](../src/powerquery/README.md#cleaning-a-dirty-export),
  [cross-tabs](../src/powerquery/README.md#unpivot-a-cross-tab) and
  [two-row headers](../src/powerquery/README.md#two-row-headers)
- [Star schema](../reference/star-schema.md)
