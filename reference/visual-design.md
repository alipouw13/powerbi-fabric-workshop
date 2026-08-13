# Visual design for I&O reports

Backs the Day 1 2:15 session, "Visualization design and governance" (deck slide
13). Read this before Lab 2.

The Tableau skills in the room transfer almost completely. What changes is where
the choices live: Tableau puts them in the worksheet, Power BI puts them in the
model and the theme. Design once, reuse everywhere.

## Show Me to the Visualizations pane

| Tableau | Power BI | Notes |
| --- | --- | --- |
| Horizontal bar, vertical bar | Clustered bar chart, clustered column chart | Bar for categories with long names, column for time |
| Stacked bar | Stacked bar chart, stacked column chart | Use 100% stacked when the mix matters more than the total |
| Line | Line chart | The default for anything over time |
| Area, stacked area | Area chart, stacked area chart | Hard to read past three series |
| Text table (crosstab) | Matrix | Matrix, not Table. Matrix gives rows, columns, subtotals and expand/collapse |
| Highlight table | Matrix with conditional formatting | Format -> Cell elements -> Background color |
| Heat map | Matrix with conditional formatting, or a scatter chart | Power BI has no dedicated heat map |
| Symbol map | Azure Map, or Map | Azure Map is the current visual and handles bubble sizing well |
| Filled map | Filled map (choropleth) | Set the data category on `state_province` and `city` or it will guess badly |
| Density map | Azure Map with the heat map layer | |
| Pie | Pie chart, donut chart | Two or three slices only. Beyond that, use a bar chart |
| Scatter | Scatter chart | Play axis replaces the Tableau pages shelf |
| Histogram | Column chart on a binned column | Create the bin in Power Query or as a grouping |
| Box-and-whisker | No native visual | Use a custom visual, or compute quartiles as measures |
| Bullet graph | KPI visual, or a bar with an error/target line | |
| Gantt | No native visual | Use a stacked bar with a transparent first segment |
| Dual axis | Line and clustered column chart, or line and stacked column chart | Y-axis and secondary Y-axis. This is the combo chart |
| Packed bubbles | No native visual | Usually a sign a bar chart is the better answer |
| Treemap | Treemap | |
| Big number | Card, or KPI visual | Card for a value, KPI for value plus target and trend |

Two things with no Tableau equivalent, worth knowing on day one:

- **Decomposition tree.** Interactive drill through dimensions, driven by a
  measure. Very good for "why did incidents spike" conversations.
- **Key influencers.** Ranks which attribute values move a metric. Useful for
  SLA breach analysis.

## Four principles

### 1. Lead with the question

Every page answers one question, and the page title says what it is. "Where are
we breaching SLA?" is a page title. "Incident Analysis" is not, and it invites
another eight visuals.

Write the question first. If a visual does not help answer it, it belongs on
another page.

### 2. Reduce chart junk

Everything on the canvas costs the reader attention. Remove anything that is not
carrying information.

- Turn off gridlines when the data labels already give the value.
- Turn off the legend when there is one series, or when the series is already
  labelled.
- Drop the axis title when the axis is obviously "months".
- Do not use 3D, shadows, or gradient fills.
- Use one accent colour for the point you are making and grey for context. Six
  colours means six things competing to be the point.
- Do not repeat the same number as a card and as a chart label.

### 3. Design for the model

The report should be thin. Logic belongs in the model.

- Build visuals from **measures**, not from dragging numeric columns in and
  accepting the implicit SUM. Hide those columns so nobody can.
- If two pages need the same calculation, it is a measure, not two visual-level
  calculations.
- Rename fields in the model, not in the visual. A field renamed in the visual is
  renamed on that visual only, and the next author is confused.
- Set the format string on the measure so every visual formats consistently.

This is the same discipline as a published Tableau data source, applied harder.

### 4. Use themes

A theme file sets the colour palette, fonts, and default visual formatting for
the whole report. Apply it first, then build, so you are not restyling twenty
visuals later.

Use [`src/theme/io-workshop-theme.json`](../src/theme/io-workshop-theme.json) on
every report in this workshop. **View -> Themes -> Browse for themes**.

Five reports built by five groups with one theme look like one product. Five
reports with five palettes look like five projects.

## Page layout

Three to five visuals per page. Not eight.

A layout that works for almost every I&O page:

```
+---------------------------------------------------------------+
|  Page title: the question this page answers                   |
+---------------+---------------+---------------+---------------+
|   KPI card    |   KPI card    |   KPI card    |   KPI card    |
+---------------+---------------+---------------+---------------+
|                               |                               |
|   Trend over time             |   Breakdown by dimension      |
|   (line chart)                |   (bar chart, sorted)         |
|                               |                               |
+-------------------------------+-------------------------------+
|  Detail (matrix), or a second breakdown                       |
+---------------------------------------------------------------+
```

Why this order: cards give the headline, the trend answers "is it getting
better", the breakdown answers "where", and the detail is there for the person
who asks for it. Readers scan top-left to bottom-right, so put the most important
thing top-left.

Practical rules:

- Align and size visuals with **Format -> Align** and the gridlines. Misaligned
  edges read as carelessness even when the numbers are right.
- Do not make the reader scroll. If it does not fit on one screen, it is two
  pages.
- Give every visual a title that states what it shows, not the field names.
- Use white space. A crowded page is not a dense page, it is an unreadable one.

## Sort intentionally

Power BI's default sort is descending by the first measure. That is often right
and sometimes badly wrong.

| Data | Sort by |
| --- | --- |
| Categories being ranked | The measure, descending. This is the point of a bar chart |
| Time | The date, ascending. Never by the measure |
| Ordered categories (severity, tier) | A dedicated sort column, ascending |
| Alphabetical lists people look things up in | The name |

Severity is the classic trap. Sorted alphabetically you get Critical, High, Low,
Moderate, which is nonsense. `dim_severity` carries `severity_sort` for exactly
this reason: select `severity_name`, then **Column tools -> Sort by column ->
severity_sort**. Same pattern for `month_name` sorted by `month`.

Sorting is a model setting, applied once, inherited by every visual.

## Format numbers

Set the format string on the **measure**, in the model, not on each visual.

| Measure type | Format | Example |
| --- | --- | --- |
| Counts | Whole number, thousands separator | `Total Incidents` -> `65,869` |
| Percentages | Percent, 1 decimal | `SLA Met %` -> `94.2%` |
| Durations | Whole number or 1 decimal, with the unit in the name | `Avg Resolve Minutes` -> `312` |
| Currency | Currency, 0 decimals for totals | `Acquisition Cost` -> `$1,284,000` |
| Utilization | Percent, 1 decimal | `Avg CPU Utilization` -> `67.4%` |

Rules:

- Do not show more precision than the data supports. `94.23847%` implies an
  accuracy the sample size does not have.
- Put the unit in the measure name when the format cannot carry it:
  `Avg Resolve Minutes`, not `Avg Resolve`.
- Use the display units setting (K, M) on axes, not on cards where readers need
  the exact figure.
- Be consistent across pages. One page in minutes and one in hours guarantees an
  argument.

## Slicers and the Filters pane

Tableau has one filter shelf. Power BI has two mechanisms, and choosing wrongly
is the most common layout mistake in a first report.

| | Slicer | Filters pane |
| --- | --- | --- |
| Where it lives | On the canvas, costs page space | In the right-hand pane |
| Who uses it | The reader, obviously | The reader, if you leave it visible |
| Scope | The page, or the whole report via sync | Visual, page, or all pages |
| Best for | Two or three dimensions readers change constantly | Everything else, plus author-set constraints |

Guidance:

- Put **at most three slicers** on a page, for the dimensions readers genuinely
  change: date, service, severity.
- Everything else goes in the Filters pane. It is discoverable, it does not eat
  canvas, and readers can be shown it once.
- Use **Sync slicers** (**View -> Sync slicers**) so a service picked on page one
  is still picked on page two. This is what Tableau's "apply to all worksheets"
  does.
- Set filters you never want changed to **hidden** and **locked** in the Filters
  pane, for example excluding Development environments.
- Prefer the date **slider** or **relative date** slicer over a long dropdown of
  months.
- Always show the reader what is filtered. A card with the active selection, or
  simply leaving the Filters pane visible, prevents the screenshot that gets
  emailed around with no context.

Compared to Tableau: the filter shelf is closest to the Filters pane, quick
filters are closest to slicers, and context filters have no direct equivalent
because filter propagation is handled by the model relationships instead.

## Accessibility

Not optional, and mostly cheap.

- **Colour is never the only signal.** Red bars for breached and green for met
  fails for roughly 8% of men. Add a label, an icon, a shape, or sort order so
  the meaning survives without colour.
- **Contrast.** Aim for at least 4.5:1 between text and background. Light grey on
  white fails.
- **Alt text.** Set it on every visual: **Format -> General -> Alt text**. One
  sentence saying what the visual shows and what the takeaway is.
- **Tab order.** **View -> Selection pane -> Tab order**. Set it to match reading
  order and remove decorative shapes from the order.
- **Font size.** 10pt minimum for data labels, 12pt for body text. Do not shrink
  the font to fit more in, cut content instead.
- **Do not rely on hover.** Anything only visible in a tooltip is invisible to
  keyboard users and to anyone reading a printed copy.
- Run **View -> Accessibility checker** before publishing.

## Before you publish

- [ ] The page title states the question.
- [ ] Three to five visuals, no scrolling.
- [ ] The workshop theme is applied.
- [ ] Every visual is built from measures, not raw columns.
- [ ] Every measure has a format string set in the model.
- [ ] Categorical sorts are intentional, ordered dimensions use a sort column.
- [ ] Three slicers maximum, the rest in the Filters pane, slicers synced.
- [ ] Every visual has a title and alt text.
- [ ] Colour is not the only signal for any status.
- [ ] Accessibility checker is clean.
- [ ] Report is named `rpt_io_<domain>_<subject>`.
- [ ] It is saved in a real workspace, not My workspace.

## Related

- [Star schema](star-schema.md)
- [Tableau to Power BI](tableau-to-powerbi.md)
- [Workshop theme](../src/theme/io-workshop-theme.json)
- [Measure definitions](../src/pbip/README.md)
- [Lab 2 - Build your first report page](../labs/lab-02-report-page/README.md)
- [Workspace governance](../governance/workspace-governance.md)
