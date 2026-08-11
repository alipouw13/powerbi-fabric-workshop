# Lab 4 - Connect, shape, and load with Power Query

**Day 2, 2:30** (`Labs 3 and 4 continued, Power Query practice`) - **Deck slide 22**
**Applies the Day 1 session:** `Power Query: connect, shape, combine, load` (slide 5, 10:30)
**Copilot agent:** Query Engineer (tab 4 from [Lab 0](../lab-00-setup-and-gateway/README.md#6-meet-m365-copilot-then-build-your-four-agents))

**Scope:** In scope. Power BI Desktop, Power Query, the gateway, and M365 Copilot.

> **Goal, from the deck.** Build a clean, reusable staging query from a flat file or SQL
> source, ready to model.

Deck slide 8 is blunt about why this matters: *Power Query is where migrations succeed or
stall. Get the query right once, and every refresh benefits.* Because there is no
Lakehouse and no Dataflow, **Power Query is the only place transformation logic can
live** - which makes this the highest-leverage skill in the workshop.

## What you'll build
- A staging query built in the order that lets it fold
- Dimensions carved out by **reference**, not copy-paste
- A hardened combine over the folder of monthly extracts, with a schema guard
- A refresh you have proven works through the gateway

## Prerequisites
- [Lab 1](../lab-01-semantic-model/README.md) complete
- `data\raw\tableau_extract\incident_report_extract.csv` and `data\raw\excel\` generated
- Your Query Engineer tab open
- Reference: [Power Query snippets](../../src/powerquery/README.md), [gateway setup](../../reference/gateway-setup.md)

---

## Steps

### 1. Open the Tableau "before"
- **Get data** → **Text/CSV** → `data\raw\tableau_extract\incident_report_extract.csv`.
- Click **Transform Data**. Do not load.
- Look at what you have: **39 columns in one table.** Every service, CI, team, location and
  severity attribute flattened onto every incident row, plus pre-calculated columns like
  `resolve_hours` and `is_breached` baked in the way a Tableau calculated field gets baked
  into an extract.
- Count the repetition. `site_name` is stored once per incident here - tens of thousands of
  times - and 8 times in `dim_location`. `business_unit` holds one of two values and is
  repeated on every single row. That is the storage and refresh cost you are about to
  remove.

Deck slide 28 names porting this shape as the number one migration pitfall: *Do not
recreate one wide table. Model the star first.*

### 2. Build the staging query in the right order
Deck slide 22, step 1: `Connect, then filter rows and remove unused columns first`.

Order matters enormously. Do exactly this sequence:

1. **Filter rows first.** Filter `date` to the last 12 months. Fewer rows through every
   subsequent step.
2. **Remove columns next.** Right-click → **Remove Other Columns**. Column removal is the
   cheapest performance win available.
3. **Set data types explicitly.** Dates as Date, keys as Whole Number, percentages as
   Decimal. Nothing left as `any`.
4. **Rename to business-friendly labels** - deck slide 22, step 2.

Then:
- Rename the query `Staging Incidents`.
- Right-click → untick **Enable load**. It is scaffolding, not a table.
- Right-click → **Move to Group** → new group `Staging`.

### 3. Check query folding
Deck slide 22, step 3: `Check query folding, then load only what the model needs`.

- Right-click the last applied step → **View Native Query**.
- Against a **CSV** it is greyed out. CSVs cannot fold - there is no query engine behind
  them. That is expected, not a failure.

> **SQL-source groups only.** Against SQL Server it shows generated SQL. Read it - that is
> what actually runs on the source. Now break it on purpose: add an **Index column**, check
> **View Native Query** again, and watch it grey out. Everything after that step now runs
> in the mashup engine on the **gateway server**, over data pulled across the wire. Undo it.
>
> That is why folding is a gateway conversation, not a Power Query one. A broken fold turns
> a two-minute refresh into an hour and puts the load on the gateway box instead of on SQL
> Server, which is built for it.

Folding breakers to recognise: index columns, most custom columns using M-only functions,
merges against a non-folding query, and type changes placed after a non-folding step.

### 4. Carve out dimensions with reference queries
This is where teams accidentally create duplicate logic. Do it properly once.

- Right-click `Staging Incidents` → **Reference**. **Not Duplicate.**
  - *Reference* points at the upstream query, so a fix upstream flows everywhere.
  - *Duplicate* copies every step, and the copies drift apart within a month.
- On the new query: keep `site_name`, `city`, `state_province`, `region`, `datacenter` →
  **Remove duplicates** → rename `dim_location`. Tens of thousands of rows become 8.
- Repeat for `dim_team`, and for `dim_service` - keep `service_name`, `service_tier`,
  `business_unit` and `business_domain`, and you should land on exactly **12 rows across
  two business units**. If you get more, a distinct is missing; if you get fewer, you
  dropped a column.
- Add an index column as the surrogate key on each dimension, starting from 1.
- Group these under `Dimensions`.

Verify each key is genuinely unique before you move on. A duplicate here becomes a broken
relationship in the model, and the symptom shows up somewhere completely unrelated.

### 5. Combine the monthly folder, and survive the November file
The "large Excel files" problem from deck slide 7, solved once. **This is the step that
matters most in this lab - protect time for it.**

- **Get data** → **Folder** → point at `data\raw\excel`.
- **Transform Data**, then filter to `.csv` and exclude anything starting `~$`.
- Do **not** click Combine Files blindly. Create a query from one file, get it right, then
  right-click → **Create Function** → `fnTransformMonthlyFile`. Invoke it as a custom
  column across the folder, then expand.

Now hit the deliberate landmine: **one November file is different.** Its `CPU %` column is
named `CPU Utilisation %`, and it has a stray `TOTAL` row at the bottom. This is not a
trick - it is what monthly extracts actually do when a different person produces one.

Left alone, neither breaks the refresh. That is the problem:
- Referenced by name, the renamed column produces **nulls for that whole month**, silently
  dragging every CPU average down.
- The `TOTAL` row inflates the CI count by one and pulls the average toward a number that
  already contains itself.

Add a schema guard so it fails loudly instead:

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

Then normalise the renamed column and filter out the `TOTAL` row. **A wrong number that
looks right is worse than an error** - that is the whole argument for this step.

> ### Query Engineer assist
> This is where the agent earns its place. Open the **Advanced Editor** and ask your Query
> Engineer tab:
>
> *"Write one let expression for my folder combine. Source columns: `CI Name` (text),
> `Environment` (text), `CPU %` (decimal), `Memory %` (decimal), `Storage Used GB`
> (decimal), `Storage Allocated GB` (decimal). One monthly file names the third column
> `CPU Utilisation %` instead. I need it to normalise either name to `cpu_pct`, remove any
> row where `CI Name` is `TOTAL`, set explicit data types, and raise a clear error if a
> column is genuinely missing."*
>
> Paste the result in and apply. **Then verify - not optional:**
> - **Row count** before and after. Did it silently drop rows?
> - **Nulls.** A type mismatch produces nulls, not an error.
> - **Data types** on every affected column. Generated M routinely omits them.
> - **Step names.** Rename `#"Changed Type1"` to something readable.
>
> If it errors, paste the M **and the exact error text** back. That loop debugs M faster
> than reading the docs. If the generated M is longer than the click-path would have been,
> use the click-path - generated code nobody understands is a maintenance liability.

### 6. Load only what the model needs, then prove the refresh
- Review every query. **Enable load** off for staging and function queries, on only for the
  dimensions and facts the model uses.
- Check the field list after loading. Anything there that no visual will use is memory and
  refresh time you are paying for.
- Publish, bind to the gateway connection from
  [Lab 0](../lab-00-setup-and-gateway/README.md#4-prove-the-gateway-path-end-to-end), and
  **Refresh now**. Watch how long it takes.
- Set the schedule after the upstream job lands, not on the hour out of habit. Send failure
  notifications to a group mailbox, not a person.

### 7. Save what worked
Add the M snippets that worked to [`src/powerquery/`](../../src/powerquery/README.md), each
with a one-line description. Without Dataflows, a shared snippet library is how you get
transformation reuse - low-tech, and it works.

Note which Copilot prompts produced good M. Standardising the prompt is as valuable as
standardising the code.

---

## Demo, not exercise

Two topics the facilitator shows on screen. Both matter; neither survives contact with the
clock as a typed exercise on day one. Read them, watch them, come back to them next week.

**Parameters.** Without Dataflows, reuse comes from query structure. **Home** → **Manage
Parameters** → create `SourceFolder` and `ReportingStartDate`, then swap the hardcoded path
and date filter in `Staging Incidents` for them. Promoting a model between environments
should not require editing M in six places. Deck slide 22: `Use parameters for file paths
or environments so the query is reusable.` The pattern is in
[`src/powerquery/README.md`](../../src/powerquery/README.md).

**Native SQL queries.** **Get data** → **SQL Server** → **Advanced options** → SQL
statement. Use one when the source has a tuned view, the join logic is genuinely complex,
or you need a hint the mashup engine will not generate. Do not use it as the default -
native queries are opaque to folding and hide the transformation from the model. If you do
use one, put the SQL in source control and comment why.

## You'll know it worked when
- Filtering and column removal happen **first** in the applied steps.
- You can point at the exact step where folding stops, and explain why.
- Dimensions are built by **Reference**, staging has Enable load off, queries are grouped.
- `dim_service` came out at 12 rows across two business units.
- The monthly folder combines, the renamed column is handled, and the `TOTAL` row is gone.
- The schema guard throws a readable error when a column goes missing.
- You used the Query Engineer to draft M and checked rows, nulls, types and step names
  afterwards.
- A refresh has run successfully through the gateway.

## Next
Day 2 closes with the 4:00 stand-up. Bring: what you built, what broke, one thing you would
tell the other groups, and your Lab 2 page for peer review.

Day 3 is [showcase and next steps](../../sessions/day-3-showcase.md).
