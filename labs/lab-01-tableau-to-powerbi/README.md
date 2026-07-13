# Lab 1 - Tableau to Power BI

**Duration:** ~60 min - **Deck:** "How the concepts map"

You will tour Power BI Desktop and the Power BI Service through a Tableau lens. You will connect to the wide market_tracker.csv extract, build a simple first report page, and learn which Tableau concepts map directly to Power BI and which do not.

## Schwab context
A Tableau team at Schwab may think in terms of workbooks, dashboards, sheets, extracts, and published data sources. Power BI uses reports, report pages, semantic models, workspaces, and apps, so the first step is vocabulary and workflow alignment.

You will start with the wide extract because it feels familiar. Later labs will show why Power BI performs best when this extract is redesigned into a star schema and reused through a shared semantic model.

## What you'll build
- A Power BI Desktop file connected to [redfin/market_tracker.csv](../../data/raw/redfin/market_tracker.csv) in Import mode.
- A report page named Tableau Extract Quick View.
- A card showing average median sale price.
- A bar chart showing homes sold by region.
- A line chart showing median sale price by period.
- A published report in Schwab-Analytics-Dev.

## Prerequisites
- Completed [Lab 0 - Setup](../lab-00-setup/README.md).
- Power BI Desktop installed and signed in.
- The generated file data/raw/redfin/market_tracker.csv exists locally.
- Access to the Schwab-Analytics-Dev workspace.
- Skim [reference/tableau-to-powerbi.md](../../reference/tableau-to-powerbi.md) for concept mapping.

## Steps
### 1. Open Power BI Desktop
Start Power BI Desktop and sign in with your workshop account.

Notice the three major areas: Report view, Data view, and Model view. In Tableau terms, you are moving between sheet design, data preview, and relationship design.

### 2. Map the key Tableau terms
Open [reference/tableau-to-powerbi.md](../../reference/tableau-to-powerbi.md) beside Power BI Desktop.

Pay attention to the terminology difference: a Tableau dashboard maps most closely to a Power BI report page. A Power BI dashboard is a separate Service pin-board feature, not the main canvas for authoring visuals.

### 3. Connect to the wide extract
Select Get data -> Text/CSV and choose data/raw/redfin/market_tracker.csv.

Choose Import. This gives you an in-memory model similar to a Tableau extract, which is useful for the first tour even though it is not the final best practice.

### 4. Inspect the fields
Open Data view and scan the columns.

Find region, state, period_begin, month_name, property_type, median_sale_price, homes_sold, new_listings, inventory, months_of_supply, median_days_on_market, and sold_above_list_share.

### 5. Create the first report page
Rename the page to Tableau Extract Quick View.

Add a text box with the title "Housing Market Snapshot". Keep the page simple so you can focus on the mapping between Tableau and Power BI.

### 6. Add a card visual
Add a card and place median_sale_price in the data field.

Change the summarization to Average. Format the value as currency and title it "Avg Median Sale Price".

### 7. Add a bar chart by region
Add a clustered bar chart.

Place region on the y-axis and homes_sold on the x-axis. Sort descending by homes_sold and keep the top regions visible.

### 8. Add a line chart by month
Add a line chart.

Place period_begin on the x-axis and median_sale_price on the y-axis. Set summarization to Average and make sure the x-axis is treated as a continuous date axis.

### 9. Publish to the Service
Save the file locally with a clear name such as Housing-Tableau-Extract-Quick-View.pbix.

Publish it to Schwab-Analytics-Dev. Open the report in the Power BI Service and confirm the page looks like the Desktop version.

### 10. Compare the workflow to Tableau
Write down one familiar step and one different step.

A likely familiar step is dragging fields to a visual. A likely different step is that Power BI separates the reusable semantic model from report pages more explicitly than a single Tableau workbook often does.

## You'll know it worked when
- The report page Tableau Extract Quick View contains a card, bar chart, and line chart.
- The report uses data/raw/redfin/market_tracker.csv in Import mode.
- The published report opens in Schwab-Analytics-Dev.
- You can explain why a Tableau dashboard maps to a Power BI report page.
- You can explain why a shared semantic model is preferable to one model per report.

## Next
Previous: [Lab 0 - Setup](../lab-00-setup/README.md). Continue to [Lab 2 - Data Modeling](../lab-02-data-modeling/README.md).
