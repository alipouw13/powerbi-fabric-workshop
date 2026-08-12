# Tableau to Power BI migration approaches

Deck slide 19, *A method, not a rewrite*. Four steps, in order: **Assess**,
**Rationalize**, **Rebuild**, **Validate**.

Start with inventory, not visuals. The fastest way to create a new mess is to
rebuild every Tableau workbook as its own Power BI report and its own semantic
model.

> **Rule of thumb: do not port a bad model.**
>
> If the Tableau workbook is a wide extract with forty calculated fields, do not
> translate the calculated fields. Model the data properly and rewrite the
> calculations as measures. Translation preserves the problem. Rebuilding removes
> it, and usually takes less time.

## Where this lands

| | Today | After migration |
| --- | --- | --- |
| Logic | In each workbook | In `sm_io_<domain>` as DAX measures |
| Data | One `.hyper` extract per workbook | One certified semantic model per domain, Import mode |
| Prep | Baked into the extract | Power Query staging queries, named steps |
| Reports | One workbook, many sheets | `rpt_io_<domain>_<subject>`, thin, on a shared model |
| Environments | Ad hoc | `IO-Analytics-Dev`, `-Test`, `-Prod`, with a deployment pipeline |

No Lakehouse, no Dataflow, no pipeline layer. Power Query, DAX, the gateway, and
the Power BI Service.

---

## Step 1: Assess

Inventory what exists before deciding anything. Use
[migration-assessment-worksheet.md](../governance/migration-assessment-worksheet.md).

### Inventory the workbooks

One row per Tableau workbook, including the ones you already intend to retire.
Capture:

- Workbook name and domain
- Business owner, and whether they still exist in the org
- Number of sheets and dashboards
- Audience
- Usage over the last 90 days
- Known pain points

### Inventory the data sources

For every source behind every workbook:

- Source system, view or file path
- Extract or live connection
- Refresh cadence, and the actual business requirement for it
- Extract size
- Credential owner and gateway requirement
- Data classification
- Known quality issues, including schema drift across monthly files

Two I&O-specific things that come up every time:

- **Monthly file folders.** Column names are rarely stable across months. Assume
  a schema guard will be needed.
- **Live connections that do not need to be live.** Most exist because someone
  once asked for intraday data. Confirm the requirement before carrying
  DirectQuery into the new estate.

### Inventory the calculations

Per workbook: calculated fields, LOD expressions, table calculations, parameters,
sets, groups, custom fiscal calendars, security filters.

**Anything used by more than one workbook is a shared DAX measure.** That list is
the starting backlog for [the measure library](../src/pbip/README.md).
Translation patterns are in [tableau-to-powerbi.md](tableau-to-powerbi.md).

### Rank by usage and business value

Score complexity 1 to 5 and business value 1 to 5, using the rubrics in the
worksheet. Score value from usage and decision impact, not from build effort.
Sunk cost is not business value.

| Category | Value | Complexity | Action |
| --- | --- | --- | --- |
| Quick win | High | Low | Migrate first, and use it for enablement |
| Strategic | High | High | Prove the model on a slice, then rebuild |
| Commodity | Low | Low | Migrate only if it is genuinely still used |
| Retire candidate | Low | High | Archive, or fold into a shared report |

For the workshop, the ITSM incident SLA workbook is the strategic early candidate:
high usage, high complexity, and it exercises `Total Incidents`, `SLA Met %`, and
`Avg Resolve Minutes` against real stakeholder expectations.

---

## Step 2: Rationalize

The step teams skip, and the one that decides whether the new estate is smaller
than the old one.

### Consolidate duplicates

Three workbooks showing incident volume by service, one per audience, are one
report with a slicer and possibly a bookmark. Look for:

- The same measure computed in several workbooks, slightly differently
- The same view filtered to different services, teams or sites
- A "management version" and a "detailed version" of the same thing
- Workbooks whose only difference is a date range

### Retire the unused

Anything with low usage and no owner comes out. This is easier during a migration
than at any other time, because the default answer is "we are not rebuilding it".

Get the retirement decision in writing from the owner, or from the absence of an
owner. Record the retirement date.

### Decide shared model versus report

For every survivor, decide whether it needs anything new in the model, or whether
it is a report on an existing one.

| Situation | Decision |
| --- | --- |
| Uses measures that already exist in a certified model | Thin report on the existing model |
| Needs one or two new measures | Request them from the model owner, then thin report |
| Needs a new fact table at a different grain | New model, with a written reason |
| Needs a new conformed dimension | Add it to the existing model, do not fork |

**Default to reuse.** A new semantic model needs a stated reason recorded in the
worksheet. Without that rule, five domains become fifteen models in a quarter.

### Output of this step

A ranked backlog with, for each workbook: rebuild, re-platform, consolidate or
retire, plus a named target semantic model. Nothing gets built until this exists.

---

## Step 3: Rebuild

Model first, report second. Always.

### Model in a star schema

1. **State the grain.** "One row is one incident." If you cannot say it in a
   short phrase, stop and fix the grain.
2. **Separate facts from dimensions.** Numbers you aggregate go in the fact.
   Attributes you slice by go in dimensions.
3. **Build conformed dimensions.** `dim_date`, `dim_service`, `dim_location` are
   shared across domains. One definition, used everywhere.
4. **Single-column integer keys.** One-to-many relationships, single direction,
   dimension filtering fact.
5. **Mark the date table**, turn off auto date/time, set the sort columns.
6. **Hide keys and raw numeric columns** that now have measures.

Full detail in [star-schema.md](star-schema.md).

### Shape in Power Query

- One **staging query** per source, load disabled, referenced by everything else.
- Filter and remove columns **first**, so the steps fold.
- Build dimensions with **Reference**, never Duplicate.
- Reference columns **by name**, never by position.
- Set explicit data types on every column.
- Add a **schema guard** on any file-based source.
- Name the steps.

Snippets in [`src/powerquery/README.md`](../src/powerquery/README.md).

### Write measures once

- Business language, Title Case: `Total Incidents`, not `count_inc`.
- `DIVIDE`, never `/`.
- Reuse base measures instead of re-aggregating columns.
- Description and format string set in the model, not on the visual.

Definitions in [`src/pbip/README.md`](../src/pbip/README.md).

### Build the report

Three to five visuals per page, one question per page, the shared theme applied,
built from measures rather than raw columns. See
[visual-design.md](visual-design.md).

M365 Copilot can draft DAX and Power Query M during this step, given your schema.
It cannot see your model, so verify everything. See
[copilot-in-power-bi.md](copilot-in-power-bi.md).

---

## Step 4: Validate

Nothing is done until it ties out, performs, and is endorsed.

### Reconcile the numbers against Tableau

Agree the grain and the tolerance with the business owner **before** you build.
"Within 0.5 percent, explained" is workable. "Exact" usually is not, because the
Tableau extract and the source have different cut-off times.

| Check | Grain |
| --- | --- |
| Total incidents | Month, service, severity |
| SLA attainment | Month, severity |
| Average resolve time | Severity, team |
| Capacity utilization | Month, environment |
| Ticket volume | Month, team, location |
| Asset count | Site, lifecycle status |

Run validation queries V1 to V9 in
[`src/sql/sample_dax_queries.dax`](../src/sql/sample_dax_queries.dax). V1 to V4
catch structural problems (orphaned keys, duplicate keys, date gaps). V5 to V9
check every measure at three grains.

Where a number does not match, explain the difference before you change anything.
A discrepancy is often the Tableau workbook being wrong, and finding that is part
of the value.

### Confirm performance

- Key pages render within the agreed target, **with the gateway in the path**.
  Testing on a laptop against a local file proves nothing.
- Scheduled refresh completes inside its window.
- Query folding survived where it matters. Check **View Native Query**.
- Consider incremental refresh on large fact tables, and verify folding first.

### Test security

- RLS tested with **View as** in Desktop, and again with a real test user in the
  Service. Desktop testing does not cover Service role membership, which is where
  the mistakes are.
- Sensitivity label applied to the model and to every report.

### Endorse

Certify the semantic model once the criteria in
[endorsement-certification.md](../governance/endorsement-certification.md) are
met. Certify the model, not the report: reports built on a certified model
inherit the trust.

### Then cut over

| Step | Action |
| --- | --- |
| Announce | Tell users which Tableau workbook is being replaced, and when |
| Parallel run | Keep both available for a defined, dated window |
| Train | A short session on slicers, drill, export and subscriptions |
| Retire | Archive the Tableau workbook on the agreed date |

**Set the retirement date when the migration starts, not when it finishes.** An
undated parallel run becomes permanent, and then you are maintaining both tools.

---

## Rebuild versus re-platform

| Approach | Use when | Avoid when |
| --- | --- | --- |
| Rebuild the model | Logic is duplicated, the extract is wide, or the target is a shared model | The workbook is a genuine one-off with a known end date |
| Re-platform the layout | The workbook is simple and already sits on a clean governed source | The Tableau calculations are complex or undocumented |
| Replace with an existing report | Usage overlaps another migration candidate | The report serves a unique regulated or audit workflow |
| Retire | Low usage and the owner agrees | It feeds a required control or report |

## Related

- [Migration assessment worksheet](../governance/migration-assessment-worksheet.md)
- [Tableau to Power BI](tableau-to-powerbi.md)
- [Star schema](star-schema.md)
- [Visual design](visual-design.md)
- [Endorsement and certification](../governance/endorsement-certification.md)
- [Adoption roadmap](../governance/adoption-roadmap.md)
- [Sources](sources.md)
