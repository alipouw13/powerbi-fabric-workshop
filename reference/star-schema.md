# Star schema for I&O reporting

Backs the Day 1 11:15 session, "Data modeling and star schema" (deck slides 9,
10, 11). Read this before Lab 1.

**None of this needs Fabric.** A star schema is a modeling choice, not a platform
feature. You build it with Power Query and Power BI Desktop against the SQL views
you already reach through the on-premises data gateway. There is no lake layer in
this workshop and none is required.

## Why a star, not a blend

Tableau lets you point a workbook at a wide extract, or blend two sources on the
fly, and it works. Power BI can do that too, and it also works, until it does
not. The failure modes are predictable:

| Wide extract or blend | What happens in Power BI |
| --- | --- |
| Every attribute repeated on every row | Model size grows, refresh slows, compression suffers |
| Business logic lives in the extract | Two extracts drift, two reports disagree, nobody can say which is right |
| Filters applied per visual | Same question answered differently on two pages |
| Adding a domain means a new extract | Five domains become five unrelated models |
| No shared dimension | You cannot put incidents and capacity on the same page by service |

A star schema fixes all five with one structural decision: separate the things
you **measure** from the things you **slice by**.

The Power BI engine (VertiPaq) is built for this shape. Columns compress better
when repeated values live in a small dimension table rather than a large fact
table. Relationships resolve faster than joins evaluated per visual.

## Facts and dimensions

| | Fact table | Dimension table |
| --- | --- | --- |
| Contains | Events and measurements | Descriptive attributes |
| Row count | Large, grows over time | Small, grows slowly |
| Typical columns | Foreign keys plus numbers you sum | A key plus text and dates you filter on |
| Example | `fact_incident` | `dim_service` |
| Naming | `fact_<event>`, singular event | `dim_<entity>`, singular entity |

Rule of thumb: **if you would put it on an axis or in a slicer, it is a
dimension. If you would sum, average, or count it, it is a fact.**

Not everything numeric belongs in the fact table. `sla_target_hours` is a number,
but it describes the severity, not the incident, so it lives in `dim_severity`.

## The grain question

Before you build anything, finish this sentence out loud:

> One row in this fact table is one ______.

If you cannot finish it in one short phrase, the grain is wrong and every measure
you write on top of it will be wrong in a way that is hard to see.

| Group | Domain | Fact table | One row is one... |
| --- | --- | --- | --- |
| 1 | ITSM & Operational Reporting | `fact_incident` | incident |
| 2 | Capacity & Forecasting | `fact_capacity` | configuration item, per month |
| 3 | Mainframe Analytics | `fact_mainframe` | LPAR, per day |
| 4 | Service Desk & Workforce | `fact_service_desk` | service, per team, per location, per day |
| 5 | Asset & Workplace Services | `fact_asset` | asset |

Grain drives what is additive. `incident_count` sums cleanly across any
dimension. `cpu_utilization_pct` does not: summing percentages is meaningless, so
you average it, and you average it at the declared grain. `mips_capacity` is
worse still, because it repeats on every daily row for the same LPAR, so summing
it across a month multiplies capacity by 30.

`fact_service_desk` is the sharpest example in the set. Its grain includes the
**service**, so `agents_scheduled` is the staffing allocated to one service on one day,
not a headcount. Sum it across the twelve services and you count the same agent twelve
times. And because `avg_handle_time_minutes` is already an average, taking `AVERAGE` of
it weights a quiet weekend row exactly the same as a peak trading morning. Both mistakes
produce numbers that look entirely plausible, which is what makes them dangerous. The
corrected, volume-weighted definitions are in
[`src/pbip/README.md`](../src/pbip/README.md#group-4-service-desk-and-workforce).

Write the grain into the table description in the model. It is the single most
useful piece of documentation you can leave behind.

## The star

`fact_incident` in the middle, the six conformed dimensions around it. One-to-many
relationships, all filtering **from** the dimension **to** the fact.

```
                        +----------------+
                        |    dim_date    |
                        |   date_key     |
                        +--------+-------+
                                 |
                                 v
  +--------------+      +--------+-------+      +------------------+
  |  dim_team    |      |                |      |   dim_service    |
  |  team_key    +----->|                |<-----+   service_key    |
  +--------------+      |                |      +------------------+
                        | fact_incident  |
  +--------------+      |                |      +------------------+
  | dim_location |      | (one row per   |      | dim_configuration|
  | location_key +----->|   incident)    |<-----+      _item       |
  +--------------+      |                |      |     ci_key       |
                        |                |      +------------------+
                        +--------+-------+
                                 ^
                                 |
                        +--------+-------+
                        |  dim_severity  |
                        |  severity_key  |
                        +----------------+
```

Swap `fact_incident` for your group's fact table and the picture is identical.
That is the point.

## Conformed dimensions

A **conformed dimension** is one dimension table shared by more than one fact
table, with the same keys and the same meaning in every one.

`dim_service` and `dim_location` are conformed across all five facts, and
`dim_service[business_unit]` therefore slices every domain report the same way. Because
the keys and meaning match, "Electronic Trading Platform" means the same thing on
the ITSM report as it does on the Capacity or Service Desk report.

Why that matters in practice:

- **Reports reconcile.** Two teams filtering to Tier 0 get the same set of
  services, because there is one definition of Tier 0.
- **One slicer drives several facts.** Put `dim_service[service_name]` on the
  page and it filters incidents and capacity together.
- **Business units reconcile.** `dim_service[business_unit]` contains Banking
  and Capital Markets, so the same executive slice works across every domain.
- **Definitions are maintained once.** A service renamed in `dim_service` is
  renamed everywhere.
- **New domains cost less.** Group 4 does not build its own location list.

The alternative, each domain shipping its own copy of the service list, is how
you end up in a meeting arguing about whether Clearing and Settlement is Tier 0 or
Tier 1.

## Keys

Use a **single-column integer surrogate key** on every dimension: `service_key`,
`ci_key`, `date_key`. Not the business identifier, not a composite of three
columns, not text.

| Why | Detail |
| --- | --- |
| Performance | Integer relationships are the fastest thing the engine does. Text keys are slower and compress worse. |
| Stability | `service_id` may be renumbered by the source system. The surrogate key does not have to move. |
| Simplicity | Power BI relationships are single-column. A composite key forces you to build a concatenated column, which is slower and easy to get wrong. |

Keep the business identifier as an ordinary column: `service_id` and
`service_name` stay in `dim_service`, they are just not the relationship key.

Every key must be **unique in the dimension** and **present in the fact**. Check
both before you build a single visual. A duplicate key breaks the relationship; a
fact key with no matching dimension row lands in a blank member and quietly
undercounts every sliced total.

## Relationships

Set every relationship the same way:

- **Cardinality:** one to many, dimension to fact.
- **Cross filter direction:** single, dimension filters fact.
- **Active:** one active relationship per pair of tables.

### Why bidirectional is a trap

Bidirectional cross filtering looks helpful. Turn it on and a filter travels from
the fact back up into the dimension, and from there down into every other fact
joined to that dimension.

Three concrete problems:

1. **Ambiguity.** With `dim_service` bidirectional to both `fact_incident` and
   `fact_capacity`, the engine has more than one path between tables and may
   refuse to resolve the model, or resolve it in a way you did not intend.
2. **Silent filtering.** Slicing by a service that has incidents but no capacity
   rows will filter the capacity visual to nothing, and it looks like missing
   data rather than a modeling choice.
3. **Row-level security holes.** Bidirectional filters can propagate around an
   RLS filter in ways that are hard to reason about and hard to test.

If you think you need bidirectional, you usually need a measure with
`CROSSFILTER` scoped to that one calculation, or a properly conformed dimension.
Start single-direction. Turn a specific one on only when you can explain why.

## Star or snowflake

Schwab has a stated plan to move to a snowflake pattern. Both shapes are
legitimate, and the honest answer is that they optimize for different things.

| | Star | Snowflake |
| --- | --- | --- |
| Shape | Dimension is one flat table | Dimension is normalized into related sub-tables |
| Example | `dim_configuration_item` carries service and location attributes | `dim_ci` -> `dim_service` -> `dim_business_unit` |
| Storage | Some redundancy | Less redundancy |
| Relationship hops | One | Two or more |
| Query speed in Power BI | Faster | Slower, the engine traverses more relationships |
| Report authoring | Simple, fields where you expect them | Fields scattered across several tables |
| Source system fit | Needs shaping | Often matches the warehouse already |

**Power BI's engine prefers a star.** VertiPaq compresses column data very well,
so the storage saving from normalizing is small, while every extra relationship
hop is real query work on every visual. Microsoft's own guidance for Power BI
modeling is star, not snowflake.

That does not mean the snowflake plan is wrong. It means the two live at
different layers:

- Normalize in the **source**, where write consistency and storage matter.
- Flatten into a **star in the semantic model**, where read performance and
  authoring clarity matter.

Power Query is where you do the flattening. Merge the sub-dimensions into one
dimension table on the way in. If a snowflake reaches the model, keep the hops
shallow and never make them bidirectional.

The dataset in this workshop is already a mild snowflake:
`dim_configuration_item` carries `service_key` and `location_key`. That is
deliberate, so you can see the tradeoff, and so Lab 1 has a real decision to
make.

## Mark the date table

One date table per model, and it must be marked.

1. Select `dim_date`.
2. **Table tools -> Mark as date table**, on the `date` column.

What marking buys you:

- Time intelligence functions (`DATEADD`, `SAMEPERIODLASTYEAR`, `TOTALYTD`)
  behave correctly instead of returning subtly wrong numbers at period edges.
- The engine can remove filters from the whole date table cleanly.
- Auto date/time hierarchies on other tables become unnecessary, and you should
  turn that feature off (**Options -> Data Load -> Time intelligence**). It
  silently creates a hidden date table per date column, and it bloats the model.

Requirements: `date` must be a date type, unique, contiguous with no gaps, and
cover full years from the first day of the first year to the last day of the last
year. `dim_date` in this dataset already satisfies this.

Also set **Sort by column** on `month_name` so it sorts by `month`, not
alphabetically. Otherwise April leads your trend line.

## Hide what report authors should not see

In Report view, hide:

- Every `*_key` column, in both facts and dimensions. Nobody builds a visual from
  `severity_key`.
- Raw numeric columns that already have a measure, for example
  `time_to_resolve_minutes` once `Avg Resolve Minutes` exists. Left visible, an
  author will drag the column in, get an implicit SUM, and publish it.
- Helper and sort columns such as `severity_sort`.

What is left should read like a business vocabulary: `Service Name`,
`Severity Name`, `Site Name`, plus your measures.

Add a description to every measure and every fact table. Two sentences each. It
is also exactly the text you paste into M365 Copilot when you want it to draft
DAX that fits your model.

## Checklist before you build a visual

- [ ] Grain is stated in one sentence, and written into the table description.
- [ ] Facts contain keys and numbers. Attributes live in dimensions.
- [ ] Every dimension has a unique single-column integer key.
- [ ] Every fact key matches a dimension row. No blank members.
- [ ] All relationships are one to many, single direction, dimension to fact.
- [ ] No bidirectional relationships, or one with a written reason.
- [ ] `dim_date` is marked as the date table on `date`.
- [ ] Auto date/time is turned off.
- [ ] `month_name` sorts by `month`.
- [ ] Keys and pre-aggregated columns are hidden.
- [ ] Table and measure descriptions are filled in.

## Related

- [Tableau to Power BI](tableau-to-powerbi.md)
- [Current state and constraints](schwab-current-state.md)
- [Visual design](visual-design.md)
- [Measure definitions](../src/pbip/README.md)
- [Power Query snippets](../src/powerquery/README.md)
- [Lab 1 - Build the semantic model](../labs/lab-01-semantic-model/README.md)
- [Sources](sources.md)
