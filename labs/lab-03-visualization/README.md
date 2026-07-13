# Lab 3 - Visualization

**Duration:** ~75 min - **Deck:** "Visualization design best practices"

You will build a polished Housing Market Overview page on the star model. The lab focuses on practical report design choices that help a Tableau audience build Power BI pages that are clear, accessible, and easy to reuse.

## Schwab context
Tableau teams often create rich dashboards with many sheets, filters, and actions. In Power BI, the same business intent works best when you use fewer, better visuals on a report page backed by a trusted semantic model.

You will rebuild a familiar housing market view with Power BI patterns: KPI cards, trend lines, small multiples, drill-through, tooltips, bookmarks, and accessibility checks.

## What you'll build
- A report page named Housing Market Overview.
- KPI cards for Homes Sold, Avg Median Sale Price, Inventory, and Months of Supply.
- A trend visual for median sale price over time.
- A regional comparison visual for market activity.
- A small multiples view by property_type.
- A tooltip page, a drill-through page, and a basic bookmark pattern.

## Prerequisites
- Completed [Lab 2 - Data Modeling](../lab-02-data-modeling/README.md).
- Housing-Star-Model.pbix with the star schema relationships working.
- Draft measures for Homes Sold and Avg Median Sale Price, or access to the definitions in [src/pbip/README.md](../../src/pbip/README.md).
- Familiarity with the Tableau concept mapping in [reference/tableau-to-powerbi.md](../../reference/tableau-to-powerbi.md).

## Steps
### 1. Open the star model
Open Housing-Star-Model.pbix in Power BI Desktop.

Confirm you are using fact_home_sales, dim_region, dim_date, and dim_property_type. Do not return to the wide market_tracker.csv extract for this report page.

### 2. Create the overview page
Add a new page and name it Housing Market Overview.

Set the page size to 16:9. Add a title and a small subtitle that says the data covers 24 months, 12 metros, and 4 property types.

### 3. Add the core KPI row
Add four card visuals across the top of the page.

Use Homes Sold, Avg Median Sale Price, Inventory, and Months of Supply. Keep labels short and use consistent number formats.

### 4. Build the price trend
Add a line chart with dim_date[period_begin] on the x-axis.

Use Avg Median Sale Price as the y-axis. Add property_type as small multiples so users can compare All Residential, Single Family Residential, Condo/Co-op, and Townhouse without overcrowding the chart.

### 5. Build the regional activity view
Add a clustered bar chart with dim_region[region] on the axis.

Use Homes Sold as the value and sort descending. Add state as a tooltip so users can see the metro and state together.

### 6. Add a market competitiveness visual
Add a scatter chart or combo chart for Avg Sale to List %, Sold Above List %, and Median Days on Market.

If the exact measures are not yet formalized, use the formatted fields from fact_home_sales. You will replace them with governed measures in Lab 6.

### 7. Create a custom tooltip page
Add a new page named Region Tooltip and turn Tooltip on in page settings.

Place region, Avg Median Sale Price, Homes Sold, Inventory, and Median Days on Market on the tooltip page. Attach this tooltip to the regional activity visual.

### 8. Add drill-through to region detail
Create a page named Region Detail.

Add dim_region[region] to the drill-through field well. Add a trend visual, property type breakdown, and summary cards so a user can right-click a metro and inspect it in detail.

### 9. Add a bookmark pattern
Create two bookmarks on Housing Market Overview: Price Focus and Activity Focus.

Use buttons to switch between the price trend and activity view. Keep the pattern simple so the page remains understandable for new Power BI authors.

### 10. Check accessibility and polish
Open View -> Selection and View -> Tab order.

Set descriptive titles, alt text, a logical tab order, and sufficient color contrast. Use a consistent theme and avoid relying on color alone to communicate status.

## You'll know it worked when
- Housing Market Overview has a clear KPI row, trend, regional comparison, and competitiveness visual.
- Small multiples show property_type without requiring four separate report pages.
- A tooltip page appears when hovering over a regional visual.
- Region Detail opens through drill-through.
- The page is readable, accessible, and not overloaded with visuals.

## Next
Previous: [Lab 2 - Data Modeling](../lab-02-data-modeling/README.md). Continue to [Lab 4 - Governance Foundations](../lab-04-governance-foundations/README.md).
