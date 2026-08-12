# Lab 2 - Build your first report page

**Day 2, 1:00** (`Labs 1 and 2, model & report`) - **Deck slide 23**
**Applies the Day 1 session:** `Visualization design and governance` (slide 5, 2:15)
**Copilot agent:** Report Designer (tab 3 from [Day 1 setup](../day-1-setup/README.md#6-meet-m365-copilot-then-build-your-four-agents))

**Scope:** In scope. Power BI Desktop, reading from the model you built in Lab 1.

> **Goal, from the deck.** Create a clean operational page: a trend, a breakdown, and a
> KPI, all reading from the shared model.

A trend, a breakdown, KPI cards and one slicer. That is the whole page. The discipline is
the point - most migrated Tableau dashboards arrive with twenty visuals and answer no
question clearly.

## Why this matters
Deck slide 13: *every page answers one operational question.* A Tableau dashboard often
grew by accretion, one request at a time. A migration is your chance to ask what the page
is actually for, and to leave out everything that does not serve it.

## What you'll build
- A page that answers one written question
- A trend, a breakdown that drills Banking / Capital Markets → domain → service, and KPI cards
- A business unit slicer
- The workshop theme applied

## Prerequisites
- [Lab 1](../lab-01-semantic-model/README.md) complete, with a validated measure
- Your requirements draft from [Day 1 setup step 6d](../day-1-setup/README.md#6-meet-m365-copilot-then-build-your-four-agents)
- Reference: [visual design](../../reference/visual-design.md)

---

## Steps

### 1. Write the question down first
Before you place a single visual, write at the top of your notes:

> *This page answers: ______________________*

One sentence. If it contains the word "and", you have two pages.

Your model now carries a real business split - Banking versus Capital Markets - so make
the question use it:

| Group | A question worth answering |
| --- | --- |
| **ITSM** | "Is Capital Markets running more major incidents per service than Banking, and which domain is driving it?" |
| **Capacity** | "Which business unit runs out of headroom first, and in which domain?" |
| **Mainframe** | "How is MIPS split between Banking Deposits and Capital Markets Post-Trade, and who is closest to capacity?" |
| **Service Desk** | "Are we hitting first-contact resolution on Capital Markets Trading tickets, where downtime costs most?" |
| **Asset** | "Where is the out-of-warranty risk concentrated - Banking Payments or Capital Markets Trading?" |

If a visual you are about to add does not help answer your sentence, it belongs on a
different page. This single habit does more for report quality than any formatting choice.

> ### Report Designer assist
> Switch to your Report Designer tab and paste the requirements draft you wrote during
> Day 1 setup:
>
> *"Here are my draft requirements: [paste]. Rewrite the core question this page answers
> as a single sentence a director would recognise. Then give me the table of visuals that
> would answer it, and three visuals people usually add that would not help."*
>
> Take the sharpened sentence and the "leave out" list. Do not take the whole answer.

### 2. Add the trend
A line chart, because the first question is always "is this getting better or worse?"

- **Line chart**.
- X axis: `dim_date[month_year]`.
- Y axis: your Lab 1 measure.
- Legend: `dim_service[Business Unit]`. Two lines, Banking and Capital Markets. That one
  field turns a generic IT trend into a business conversation.
- Sort ascending by date. Power BI will sometimes sort by value; fix it.
- Title it as a statement: **"Incident volume by month, Banking vs Capital Markets"**, not
  "Sum of incident_count by month_year".

**Coming from Tableau:** this is a Show Me line chart. The difference is that the measure
comes from the shared model, so every other report using it gets the same number.

### 3. Add the breakdown, with a drill hierarchy
A bar chart, because the second question is always "where is it coming from?"

- **Clustered bar chart** - horizontal, because service names are long and read better on
  the left.
- Y axis: add three fields **in this order** to build a drill hierarchy:
  `dim_service[Business Unit]` → `dim_service[business_domain]` → `dim_service[Service]`.
- X axis: the same measure.
- **Sort descending by the measure**, not alphabetically. The eye should land on the
  biggest bar first.
- Turn on the drill-down arrows in the visual header and click through all three levels.
  Two bars become ten, then twelve.

That drill path is the whole reason `business_unit` and `business_domain` exist in the
model. An executive starts at two bars; the service owner drills to their own service.

> **Alternative worth trying if you have time:** a **decomposition tree** with the same
> three fields. It does the same job and lets the reader choose the path.

### 4. Add the KPI cards
Three cards, maximum. These are the numbers someone reads and then stops.

| Group | Card 1 | Card 2 | Card 3 |
| --- | --- | --- | --- |
| ITSM | Total Incidents | SLA Met % | Major Incidents |
| Capacity | Avg CPU Utilization | CIs Over 80% CPU | Avg Headroom % |
| Mainframe | Total MIPS Consumed | MIPS Utilization % | Batch Failure Rate |
| Service Desk | Tickets Received | First Contact Resolution % | Avg Handle Time |
| Asset | Total Assets | Out of Warranty % | CMDB Completeness % |

You probably only have the first card's measure so far. That is fine - **Lab 3 builds the
rest.** Add the card, leave it blank, come back.

- Format properly: thousands separators, percentages to one decimal, minutes as whole
  numbers.
- Rename each card's label to business language. "Total Incidents", not "Count of
  incident_count".

> **Group 4, read this before you put a number on a card.** Your fact is one row per
> *service* per team per location per day, so the staffing columns are allocations, not
> people. Do not put `SUM(agents_scheduled)` on a card labelled "Agents" - it counts the
> same agent once per service. Lab 3 gives you `Agent Days Scheduled` and `Coverage %`,
> which are named for what they actually measure.

### 5. Add the business unit slicer
- One slicer: `dim_service[Business Unit]`. Two buttons, Banking and Capital Markets.
- Set it to **Tile** style so it reads as a toggle rather than a dropdown.
- Put it top-left, and keep that position on every page your group builds. Consistent
  placement means users stop hunting.
- Click each one. Every visual on the page should respond, because every fact carries
  `service_key`.

Resist adding more. One or two slicers is plenty; the Filters pane is where filters users
should *not* change belong.

### 6. Apply the theme and tidy up
Deck slide 23: `apply the workshop theme`. Slide 31 lists it as a reusable pattern: *One
JSON theme: colors, fonts, and spacing across every report.*

- **View** → **Themes** → **Browse for themes** → select
  [`src/theme/schwab-io-theme.json`](../../src/theme/schwab-io-theme.json).
- Confirm the visuals repaint. Do not override theme colours on individual visuals - the
  moment one person does, the estate starts to drift.
- Layout: cards along the top, slicer top-left, trend below-left, breakdown below-right.
- **Format** → **Align** to align and distribute. Misaligned visuals read as careless even
  when the analysis is good.
- Add a page title text box that repeats your sentence from step 1, and rename the page
  tab to something meaningful.

### 7. Check it against the list
Deck slide 23's design checklist:

- [ ] The page answers one operational question, and you can state it.
- [ ] Three to five visuals, no more.
- [ ] The breakdown drills Business Unit → domain → service.
- [ ] Axes labelled, sorting intentional.
- [ ] The workshop theme is applied, nothing manually overridden.
- [ ] Every visual reads from the shared model, not a local import.
- [ ] Titles are statements a business user understands.
- [ ] Numbers are formatted the way a human would write them.

Peer review happens at the 4:00 stand-up - bring the page and have another group try to
answer your question using only your screen. If they cannot, the page is not finished.

## You'll know it worked when
- The page answers one written question.
- Clicking Banking or Capital Markets changes every visual.
- The breakdown drills three levels and the parts sum back to the total at each one.
- KPI cards are present, formatted, and labelled in business language.
- The workshop theme is applied.

## Next
[Lab 3 - Practice DAX measures](../lab-03-dax-measures/README.md)
