# Lab 4 - Connect, shape, and load with Power Query

**Day 2, 1:00 and 2:30** (`Labs 3 and 4 continued, Power Query practice`) - **Deck slide 22**
**Applies the Day 1 session:** `Power Query: connect, shape, combine, load` (slide 5, 10:30)

**Scope:** In scope. Power BI Desktop, Power Query, the gateway, and **M365
Copilot** for drafting M.

> **Goal, from the deck.** Build a clean, reusable staging query from a flat file
> or SQL source, ready to model.

Deck slide 8 is blunt about why this matters: *Power Query is where migrations
succeed or stall. Get the query right once, and every refresh benefits.*

Because there is no Lakehouse and no Dataflow, **Power Query is the only place
Schwab's transformation logic can live**. That makes this the highest-leverage
skill in the workshop.

## What you'll build
- A folding-verified staging query against the source
- A star's worth of dimension queries built by **reference**, not copy-paste
- Parameters and a custom function, so logic is written once
- A hardened combine over the folder of monthly Excel-style extracts
- A refresh that you have proven works through the gateway

## Prerequisites
- [Lab 1](../lab-01-semantic-model/README.md) complete
- `data\raw\tableau_extract\incident_report_extract.csv` generated
- `data\raw\excel\` populated with monthly files
- Reference: [Power Query snippets](../../src/powerquery/README.md), [gateway setup](../../reference/gateway-setup.md)

---

## Steps

### 1. Start from the wide extract - the Tableau "before"
- **Get data** → **Text/CSV** → `data\raw\tableau_extract\incident_report_extract.csv`.
- Click **Transform Data**, do not load yet.
- Look at what you have: **38 columns in one table.** Service attributes, CI
  attributes, team attributes, location attributes and severity attributes all
  flattened onto every incident row, plus pre-calculated columns like
  `resolve_hours` and `is_breached`.
- This is what a `.hyper` extract looks like, and deck slide 28 names porting it
  as the number one migration pitfall: *Do not recreate one wide table. Model the
  star first.*
- Count the repetition: `site_name` is stored once per incident instead of once
  per location. That is the storage and refresh cost you are about to remove.

### 2. Build the staging query properly
Deck slide 22, step 1: `Connect, then filter rows and remove unused columns first`.

Order matters enormously here. Do it in this sequence:

1. **Filter rows first.** Filter `date` to the last 12 months. Fewer rows through
   every subsequent step.
2. **Remove columns next.** Right-click → **Remove Other Columns**, keeping only
   what you need. Column removal is the cheapest performance win available.
3. **Set data types explicitly.** Dates as Date, keys as Whole Number, percentages
   as Decimal. Do not leave anything as `any`.
4. **Rename to business-friendly labels** - deck slide 22, step 2.

Then:
- Rename the query `Staging Incidents`.
- Right-click it → untick **Enable load**. It is scaffolding, not a table.
- Right-click → **Move to Group** → new group `Staging`.

### 3. Check query folding
Deck slide 22, step 3: `Check query folding, then load only what the model needs`.

- Right-click the last applied step → **View Native Query**.
- Against a **CSV** it will be greyed out - CSVs cannot fold, there is no query
  engine behind them. That is expected.
- Against **SQL Server** it should show you generated SQL. Read it. That SQL is
  what actually runs on the source.

Now break it deliberately, on a SQL source:
- Add an **Index column**. Check **View Native Query** again - greyed out.
- Folding has stopped. Everything after that step runs in the mashup engine, on
  the **gateway server**, over data pulled across the wire.
- Undo it.

**Why this is a gateway conversation.** Deck slide 8: *Import-mode refresh runs
through the on-premises data gateway. Fewer, cleaner queries mean shorter refresh
windows.* A broken fold turns a two-minute refresh into an hour and puts the load
on the gateway box rather than on SQL Server, which is built for it. See
[gateway-setup.md](../../reference/gateway-setup.md#7-troubleshooting-in-the-order-to-check).

Folding breakers to recognise: index columns, most custom columns using M-only
functions, merges against a non-folding query, and type changes placed after a
non-folding step.

### 4. Carve out dimensions with reference queries
This is where teams accidentally create duplicate logic. Do it properly once.

- Right-click `Staging Incidents` → **Reference**. **Not Duplicate.**
  - *Reference* points at the upstream query, so a fix upstream flows everywhere.
  - *Duplicate* copies every step, and the copies drift apart within a month.
- On the new query: keep `site_name`, `city`, `state_province`, `region`,
  `datacenter` → **Remove duplicates** → rename `dim_location`.
- Repeat for `dim_service` and `dim_team`.
- Add an index column as the surrogate key on each dimension, starting from 1.
- Group these queries under `Dimensions`.

Verify each key is genuinely unique before you leave this step. A duplicate here
becomes a broken relationship in the model, and the symptom shows up somewhere
completely unrelated.

### 5. Parameterize it
Without Dataflows, reuse comes from query structure. This is how.

- **Home** → **Manage Parameters** → **New**:
  - `SourceFolder`, Text, current value = your `data\raw` path
  - `ReportingStartDate`, Date, current value = 12 months ago
- Edit `Staging Incidents` in the **Advanced Editor** and swap the hardcoded path
  and date filter for the parameters.
- Confirm the query still works, and that the date filter **still folds** against
  a SQL source.

Why it matters at Schwab: promoting a model between environments, or handing it
to a colleague, should not require editing M in six places. Deck slide 22:
`Use parameters for file paths or environments so the query is reusable.`

### 6. Combine the monthly Excel folder
The "large Excel files" problem from deck slide 7, solved once.

- **Get data** → **Folder** → point at `data\raw\excel`.
- **Transform Data**, then filter to `.csv` and exclude anything starting `~$`.
- Do **not** click Combine Files blindly. Build the transform function yourself so
  you know what it does.
- Create a query from one file, get it right, then right-click →
  **Create Function** → `fnTransformMonthlyFile`.
- Invoke it as a custom column across the folder, then expand.

Now hit the deliberate landmine: **the November file is different.** One column is
named `CPU Utilisation %` instead of `CPU %`, and there is a stray `TOTAL` row at
the bottom. This is not a trick - it is what monthly Excel extracts actually do.

Add a schema guard so it fails loudly instead of silently producing nulls:

```powerquery
let
    Source   = #"Combined Files",
    Expected = {"CI Name", "Environment", "CPU %", "Memory %"},
    Actual   = Table.ColumnNames(Source),
    Missing  = List.Difference(Expected, Actual),
    Checked  =
        if List.IsEmpty(Missing) then
            Source
        else
            error Error.Record(
                "Source schema changed",
                "Missing expected columns: " & Text.Combine(Missing, ", "),
                "Check the monthly extract before refreshing."
            )
in
    Checked
```

Then filter out the `TOTAL` row. A wrong number that looks right is worse than an
error - that is the whole argument for this step.

> **M365 Copilot assist.** This is where Copilot earns its place. Open the
> **Advanced Editor**, and prompt:
>
> *"Write Power Query M for this transformation. Source columns: `CI Name` (text),
> `Environment` (text), `CPU %` (decimal), `Memory %` (decimal), `Storage Used GB`
> (decimal). Some monthly files name the third column `CPU Utilisation %` instead.
> I need one query that: normalises either column name to `cpu_pct`, removes any
> row where `CI Name` is `TOTAL`, sets explicit data types, and returns a single
> let expression I can paste into the Advanced Editor."*
>
> Paste the result in and apply.
>
> **Then verify - this is not optional:**
> - **Row count** before and after. Did it silently drop rows?
> - **Nulls.** A type mismatch produces nulls, not an error.
> - **Data types** on every affected column. Generated M routinely omits them.
> - **Folding.** Right-click the last step → View Native Query.
> - **Step names.** Rename `#"Changed Type1"` to something readable.
>
> If it errors, paste the M **and the exact error text** back to Copilot. That
> loop debugs M faster than reading the docs.
>
> If the generated M is longer than the click-path would have been, use the
> click-path. Generated code nobody understands is a maintenance liability.

### 7. A native SQL query, when it earns its place
Deck slide 22: `A native SQL query can outperform many folded steps for a complex
source.`

- **Get data** → **SQL Server** → **Advanced options** → SQL statement.
- Use it when: the source has a tuned view or stored proc, the join logic is
  genuinely complex, or you need a hint the mashup engine will not generate.
- Do not use it as the default. Native queries are opaque to folding, harder for
  the next person to read, and they hide the transformation from the model.
- If you do use one, put the SQL in source control and comment why.

### 8. Load only what the model needs, then prove the refresh
- Review every query. **Enable load** should be **off** for staging and function
  queries, **on** only for the dimensions and facts the model uses.
- Check the field list after loading. Anything there that no visual will ever use
  is memory and refresh time you are paying for.
- Publish, then bind to the gateway connection from
  [Lab 0](../lab-00-setup-and-gateway/README.md).
- **Refresh now.** Watch how long it takes.
- Then break folding deliberately, republish, and refresh again. Compare. That
  number is the argument you will use next time someone asks why folding matters.
- Set the schedule after the upstream job lands, not on the hour out of habit.
  Set failure notifications to a group mailbox.

### 9. Save what worked
Add the M snippets that worked to [`src/powerquery/`](../../src/powerquery/README.md),
each with a one-line description. Without Dataflows, a shared snippet library is
how Schwab gets transformation reuse - low-tech, and it works.

Note which Copilot prompts produced good M. Standardising the prompt is as
valuable as standardising the code.

## You'll know it worked when
- Filtering and column removal happen **first** in the applied steps.
- You can point at the exact step where folding stops, and explain why.
- Dimensions are built by **Reference**, staging has Enable load off, queries are
  grouped in folders.
- At least one parameter and one custom function are in use.
- The monthly folder combines, the November file's renamed column is handled, and
  the `TOTAL` row is gone.
- The schema guard throws a readable error when a column goes missing.
- You used M365 Copilot to draft M, pasted it into Advanced Editor, and checked
  rows, nulls, types and folding afterwards.
- A scheduled refresh has run successfully through the gateway.

## Next
Day 2 closes with the 4:00 stand-up. Bring: what you built, what broke, and one
thing you would tell the other groups.

Day 3 is [showcase and next steps](../../sessions/day-3-showcase.md).
