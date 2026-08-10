# Lab 5 - Connect and transform in Power Query

**Duration:** ~120 min - **Deck:** "Connecting to data" - **Day 2**

**Scope:** In scope. Everything here uses Power BI Desktop, Power Query, the
on-premises data gateway, and Import or DirectQuery. Nothing else.

This is the longest teaching lab in the workshop, and the most directly useful.
Because there is no lake layer and no Dataflow to push work into, **Power Query
is where all of Schwab's transformation logic lives**. Getting good at it is the
single highest-leverage skill on offer here.

## Schwab context
Most Power BI reports at Schwab connect straight to SQL databases in Import mode,
brokered by the on-premises data gateway, and a lot of source data still arrives
as large Excel files. There is no Lakehouse, no OneLake, and no Dataflow Gen2 -
so every join, cleanup, and reshape happens by hand, in the model, in Power
Query. That makes three things matter more than they would elsewhere: **query
folding** (push work to the source), **reusable query structure** (so logic is
written once), and **discipline about what you import** (because the model is
the only place data lives).

## What you'll build
- A documented map of the current connection path and who owns each hop
- A reasoned Import vs DirectQuery decision for the insurance source
- A folding-verified connection that pushes work back to SQL
- A fact table shaped in Power Query from the wide source
- Conformed dimension queries built with reference queries, not copy-paste
- A parameterized, function-driven pattern for repeated transformations
- A hardened Excel ingestion pattern that survives someone adding a column
- A refresh and gateway troubleshooting checklist

## Prerequisites
- Completed [Lab 4 - Governance foundations](../lab-04-governance-foundations/README.md)
- Power BI Desktop
- The generated files under data/raw/contoso/ (they stand in for the SQL source)
- Reference docs: [current state](../../reference/schwab-current-state.md) and
  [Tableau to Power BI](../../reference/tableau-to-powerbi.md)

## Steps

### 1. Map the current Schwab pattern
- Draw it on the whiteboard: source SQL -> on-premises data gateway -> semantic
  model -> report.
- Note who owns each hop. At Schwab the gateway and its data sources are centrally
  managed, so an analyst usually cannot create or repoint a connection.
- List what that means in practice: connection requests have lead time, credentials
  are not yours to rotate, and a broken refresh is often a gateway conversation.
- Compare to Tableau: the gateway plays the role Tableau Bridge or a published
  data source connection plays for you today.
- Note what is **not** in the picture: no lake, no staging layer, no pipeline. If
  a transformation needs to happen, it happens in Power Query or in a view on the
  source. There is no third option.
- Write down the three sources your team would migrate first and who owns each.

### 2. Choose Import or DirectQuery, deliberately
These are the only two storage modes available. Decide per model, not by habit.

| | Import | DirectQuery |
| --- | --- | --- |
| Where data lives | Cached in the model | Stays in the source |
| Query speed | Fast, in-memory | As fast as the source is |
| Freshness | As of last refresh | Live |
| Refresh | Scheduled, via gateway | Not needed |
| Power Query | Full transformation library | **Only steps that fold** |
| Source load | Periodic, heavy | Continuous, per interaction |

- Load the insurance source in **Import** first. This is the default for a reason
  and matches most of what Schwab runs today.
- Now switch a copy to **DirectQuery** and notice what changes: transformation
  options grey out, some DAX functions become unavailable, and every visual
  interaction issues a query.
- Discuss which of your real sources would justify DirectQuery. Usually it is
  volume, volatility, or a policy that forbids caching - not preference.
- Record the decision and the reason. "We chose Import because the source is
  refreshed nightly and fits comfortably in memory" is a governance artifact.

### 3. Build the connection and verify folding
- In Power BI Desktop, choose Get data and connect to the insurance source.
- Use a **named view or query** on the source rather than a table with everything
  in it. The cheapest transformation is the one the database does for you.
- In Power Query, remove columns you will not use **before** any other step.
  Column removal is the single biggest performance win available to you.
- Filter rows to the reporting window the business actually needs.
- Right-click the last applied step and choose **View Native Query**. If it is
  available, your steps are folding back to SQL. If it is greyed out, find the
  step that broke folding.
- Folding-breakers to watch for: adding an index column, most custom columns
  using M-only functions, merging on a non-folding query, and changing types
  after a non-folding step.
- Reorder steps so folding survives as long as possible. Put filters and column
  removal first, custom logic last.
- Note the model size before and after your cleanup pass. Report the difference
  to your table.

### 4. Shape the fact table by hand
You are turning the wide extract into a proper fact table using only Power Query.

- Start from the wide source and create a query named `fact_premium`.
- Keep only the grain-defining keys and the additive measures: policy key, agent
  key, date key, `written_premium`, `earned_premium`.
- Remove descriptive attributes that belong in a dimension. If `product` and
  `region` describe the policy, they do not belong on the fact.
- Set explicit data types. Currency columns as Fixed decimal number, keys as
  whole number or text consistently.
- Confirm the grain in one sentence: "one row per policy, per agent, per period."
  If you cannot say it in one sentence, the grain is wrong.
- Repeat for `fact_claim`.
- Check the row count against the source. A shaped fact table should not gain rows.

### 5. Build conformed dimensions with reference queries
This is where most teams accidentally create duplicate logic. Do it properly once.

- Right-click your cleaned source query and choose **Reference** - not Duplicate.
  Reference reuses the upstream steps; Duplicate copies them and they drift apart.
- From the reference, build `dim_policy`: select the policy attributes, then
  **Remove duplicates** on the policy key.
- Repeat for `dim_customer`, `dim_agent`, and `dim_coverage`.
- Build `dim_date` from the provided date file, or generate it in M if your
  facilitator prefers. Every model needs exactly one date table.
- Set the source query to **Enable load = off** so it stays a staging query and
  does not become a table in the model. Right-click the query and untick
  **Enable load**.
- Group your queries in folders: `Staging`, `Dimensions`, `Facts`. A model with
  twenty ungrouped queries is unmaintainable within a month.
- Verify each dimension key is unique. A duplicate key here becomes a broken
  relationship in Lab 6.

### 6. Make the logic reusable: parameters and functions
Without Dataflows, reuse has to come from query structure. This is how.

- Create a **parameter** for the source server or file path. Manage Parameters ->
  New. Point your source query at the parameter instead of a hardcoded value.
- Explain why this matters at Schwab: promoting a model between environments, or
  handing it to a colleague, should not require editing M in six places.
- Create a second parameter for the reporting start date and use it in your row
  filter. Confirm the filter still folds.
- Turn a repeated cleanup into a **custom function**: right-click a query with
  the transformation and choose **Create Function**. Invoke it against another
  query.
- Open the **Advanced Editor** on one query and read the M. You do not need to
  write M fluently, but you must be able to read it - and in Lab 7 you will be
  pasting M into this window.
- Document the parameters and functions your team would standardize on. This is a
  community-of-practice deliverable, not a personal preference.

### 7. Tame the Excel sources
- Large Excel files are the most common source of surprise refresh failures.
- Connect to an Excel source and observe what happens when a column is renamed or
  inserted: the query breaks on position or name.
- Harden it: promote headers explicitly, reference columns by name, and set types
  by name rather than position.
- Add a guard step that fails loudly with a clear message rather than silently
  producing nulls. A wrong number that looks right is worse than an error.
- Where a folder of monthly workbooks exists, use **Get data > Folder** with a
  single transform function instead of one query per file. This is the function
  pattern from step 6, applied to a real problem.
- Remember Excel sources rarely fold. Everything you do to them happens in the
  mashup engine, so keep the steps few and the files small.
- Decide as a group which Excel files are genuinely a system of record and which
  are a symptom of a missing SQL source or a missing shared model. Capture the
  list - it is a direct input to the Lab 12 roadmap.
- Agree on a rule the community of practice can enforce: Excel is an input, not a
  destination.

### 8. Plan refresh and troubleshooting
- Set a refresh schedule appropriate to the source, not the maximum allowed.
- Know the three failure modes you will actually hit: expired gateway credentials,
  a source schema change, and a timeout on an over-wide import.
- Walk the path for each symptom: which hop do you check first, and who owns it?
- Write a one-page checklist your team follows before escalating to the gateway
  owners. Most escalations are avoidable with two minutes of triage.
- Discuss incremental refresh as the next step for large fact tables, and what it
  requires: a reliable date column, a folding query, and RangeStart/RangeEnd
  parameters - which you now know how to create.

## You'll know it worked when
- You can state your Import vs DirectQuery decision and the reason behind it.
- Your query folds back to the source, or you know exactly which step broke it
  and why you accepted that.
- `fact_premium` and `fact_claim` have a stated grain and no descriptive columns.
- Dimensions are built from **reference** queries with unique keys, and the
  staging query has Enable load switched off.
- Queries are grouped into folders and at least one parameter and one function
  are in use.
- The model is measurably smaller after the cleanup pass.
- You have a hardened Excel pattern and a list of Excel files that should become
  real sources.
- You have a refresh troubleshooting checklist your team would actually use.

## Next
[Lab 6 - The shared semantic model](../lab-06-semantic-model-directlake/README.md)
