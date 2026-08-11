# Lab 2 - Build your first report page

**Day 2, 10:30** (`Labs 1 and 2, model and report`) - **Deck slide 20**
**Applies the Day 1 session:** `Visualization design and governance` (slide 5, 2:15)

**Scope:** In scope. Power BI Desktop, reading from the model you built in Lab 1.

> **Goal, from the deck.** Create a clean operational page: a trend, a breakdown,
> and a KPI, all reading from the shared model.

Three visuals. That is the whole page. The discipline is the point - most
migrated Tableau dashboards arrive with twenty visuals and answer no question
clearly.

## Why this matters
Deck slide 13: *every page answers one operational question.* A Tableau dashboard
often grew by accretion, one request at a time. A migration is your chance to ask
what the page is actually for, and to leave out everything that does not serve
that.

## What you'll build
- A line chart: your domain's primary measure over time
- A bar chart: the same measure broken down by service or team
- KPI cards for the headline numbers
- The workshop theme applied
- A page that answers one written question

## Prerequisites
- [Lab 1](../lab-01-semantic-model/README.md) complete, with a validated measure
- Your flagship report requirements from Lab 0 step 7
- Reference: [visual design](../../reference/visual-design.md), [Tableau to Power BI](../../reference/tableau-to-powerbi.md)

---

## Steps

### 1. Write the question down first
Before you place a single visual, write at the top of your notes:

> *This page answers: ______________________*

Examples by group:
- **ITSM:** "Which services are driving our incident volume, and is it improving?"
- **Capacity:** "Which CIs will run out of headroom first?"
- **Mainframe:** "Are we approaching our MIPS capacity, and when?"
- **Service Desk:** "Are we resolving on first contact, and is staffing matched to demand?"
- **Asset:** "What is out of warranty and still in service?"

If a visual you are about to add does not help answer that sentence, it belongs
on a different page. This single habit does more for report quality than any
formatting choice.

> **M365 Copilot assist.** If you drafted requirements in Lab 0, sharpen them now:
>
> *"Here are my draft requirements for an operational report: [paste]. Rewrite the
> core question this report answers as a single sentence a director would
> recognise. Then list the three visuals that would answer it, and three that
> people usually add but that do not help."*
>
> This is the use deck slide 24 describes. Take the sharpened sentence, not the
> whole answer.

### 2. Add the trend
A line chart, because the first question is always "is this getting better or
worse?"

- **Line chart**.
- X axis: `dim_date[month_year]` (or `dim_date[date]` for a daily view).
- Y axis: your Lab 1 measure - `Total Incidents`, `Total MIPS Consumed`,
  `Tickets Received`.
- Sort ascending by date. Power BI will sometimes sort by value; fix it.
- Title it as a statement, not a field list: **"Incident volume by month"**, not
  "Sum of incident_count by month_year".

**Coming from Tableau:** this is a Show Me line chart. The difference is that the
measure comes from the shared model, so every other report using it gets the same
number.

### 3. Add the breakdown
A bar chart, because the second question is always "where is it coming from?"

- **Clustered bar chart** (horizontal bars - service names are long and read
  better on the left).
- Y axis: `dim_service[Service]`, or `dim_team[Team]` for group 4.
- X axis: the same measure.
- **Sort descending by the measure**, not alphabetically. The eye should land on
  the biggest bar first.
- Consider **Top N** filtering to the top 10 - a bar chart with 40 categories is
  a table in disguise.

### 4. Add the KPI cards
Three cards, maximum. These are the numbers someone reads and then stops.

- Three **Card** visuals across the top.
- Suggested by group:

| Group | Card 1 | Card 2 | Card 3 |
| --- | --- | --- | --- |
| ITSM | Total Incidents | SLA Met % | Avg Time to Resolve |
| Capacity | Avg CPU Utilization | CIs Over 80% | Avg Headroom % |
| Mainframe | Total MIPS Consumed | Peak MIPS % of Capacity | Batch Jobs Failed |
| Service Desk | Tickets Received | First Contact Resolution % | Avg Handle Time |
| Asset | Total Assets | Assets Out of Warranty | CMDB Completeness % |

You may only have the first card's measure so far - that is fine. Lab 3 builds
the rest. Add placeholders and come back.

- Format properly: thousands separators, percentages to one decimal, minutes as
  whole numbers.
- Rename each card's label to business language. "Total Incidents", not
  "Count of incident_count".

### 5. Add slicers, sparingly
- One or two, no more. `dim_date[month_year]` and `dim_service[Service]` cover
  most needs.
- Put them together, top-left or in a right-hand rail. Consistent placement
  across reports means users stop hunting.
- **Coming from Tableau:** slicers are Power BI's quick filters. The Filters pane
  is the closer equivalent to Tableau's filter shelf, and it is where filters that
  users should not change belong.

### 6. Apply the workshop theme
Deck slide 20: `apply the workshop theme`. Deck slide 29 lists it as a reusable
pattern: `One JSON theme: colors, fonts, and spacing across every report.`

- **View** → **Themes** → **Browse for themes** → select
  [`src/theme/schwab-io-theme.json`](../../src/theme/schwab-io-theme.json).
- Confirm the visuals repaint. Colours, fonts and spacing now match every other
  group's report.
- Do not override theme colours on individual visuals. The moment one person
  does, the estate starts to drift.

### 7. Lay it out and tidy up
- Cards along the top, trend below-left, breakdown below-right.
- Align and distribute - **Format** → **Align**. Misaligned visuals read as
  careless even when the analysis is good.
- Turn off gridlines you do not need. Remove visual borders unless they group
  something.
- Add a page title text box that repeats the question from step 1.
- Rename the page tab to something meaningful, not "Page 1".

### 8. Review against the checklist
Deck slide 20's design checklist:

- [ ] The page answers one operational question, and you can state it.
- [ ] Three to five visuals, no more.
- [ ] Axes labelled, sorting intentional.
- [ ] The workshop theme is applied.
- [ ] Every visual reads from the shared model, not a local import.
- [ ] Titles are statements a business user understands.
- [ ] Numbers are formatted the way a human would write them.

Swap laptops with another pair and have them try to answer your question using
only your page. If they cannot, the page is not finished.

## You'll know it worked when
- The page answers one written question.
- A trend, a breakdown, and KPI cards are present, and nothing else.
- Sorting is deliberate everywhere.
- The workshop theme is applied and nothing is manually overridden.
- Another group can read your page and answer your question without you
  explaining it.

## Next
[Lab 3 - Practice DAX measures](../lab-03-dax-measures/README.md)
