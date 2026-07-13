# Lab 7 - Copilot in Reports

**Duration:** ~75 min - **Deck:** "Build reports faster with Copilot"

You will use Copilot in Power BI to create and refine report content on top of Housing-Market-Insights. You will also test narrative summaries, DAX Copilot, and generated measure descriptions.

## Schwab context
Copilot can speed up report authoring, but it is not a substitute for a well-modeled semantic model. Schwab teams will get better results when measures are named clearly, fields are described, and AI metadata explains the business meaning.

In this lab, you will compare Copilot output before and after small metadata improvements. The goal is to learn how to guide Copilot with the model rather than fixing every report page manually.

## What you'll build
- A Copilot-generated report page for Housing-Market-Insights.
- A refined page that uses workshop visual design practices.
- A narrative/summary visual.
- A DAX query generated or assisted by DAX Copilot.
- Measure descriptions for the core measures.
- A short list of model metadata changes that improve Copilot output.

## Prerequisites
- Completed [Lab 6 - Semantic Model + Direct Lake](../lab-06-semantic-model-directlake/README.md).
- Copilot and Fabric enabled in the tenant.
- Build or edit access to Housing-Market-Insights.
- Review [reference/copilot-in-power-bi.md](../../reference/copilot-in-power-bi.md).
- Core measure definitions in [src/pbip/README.md](../../src/pbip/README.md).

## Steps
### 1. Confirm Copilot availability
Open Power BI Service or Power BI Desktop where Copilot is enabled.

Confirm the Copilot pane is available. If it is not available, record the tenant or capacity dependency and observe the facilitator demonstration.

### 2. Open the semantic model
Create a new report connected to Housing-Market-Insights.

Use the shared semantic model rather than importing CSV files. This gives Copilot the best chance to use governed measures, relationships, and descriptions.

### 3. Ask Copilot for a report page
In the Copilot pane, ask for a page that summarizes housing market performance by metro, property type, and month.

Review the visuals Copilot creates. Keep useful visuals, remove clutter, and make sure the page uses the exact measures from Lab 6.

### 4. Refine the generated page
Rename the page Copilot Market Summary.

Apply the same design rules from Lab 3: fewer visuals, clear titles, consistent formats, accessible colors, and no unexplained metrics.

### 5. Add a narrative visual
Add a narrative/summary visual to the page.

Ask it to summarize key changes in Homes Sold, Avg Median Sale Price, Inventory, and Months of Supply. Check every generated statement against the visuals before trusting it.

### 6. Use DAX Copilot
Open a DAX query experience and ask Copilot to write a query that returns top metros by Homes Sold and Avg Median Sale Price.

Compare the result to examples in [src/sql/sample_dax_queries.dax](../../src/sql/sample_dax_queries.dax). Adjust the query so it uses Housing-Market-Insights measures exactly.

### 7. Generate measure descriptions
Use Copilot to draft descriptions for Homes Sold, New Listings, Inventory, Avg Median Sale Price, and Homes Sold YoY %.

Edit the descriptions so they are accurate, concise, and written for report authors. Avoid marketing language.

### 8. Improve model metadata and retry
Add or revise field descriptions, synonyms, and AI instructions for one confusing field.

Ask Copilot to create or summarize the page again. Note whether the output improves after the metadata change.

### 9. Test inline edits
Use inline Copilot where available to change a visual title, add a slicer, or adjust a report page.

Treat each suggestion as a draft. Validate fields, aggregations, filters, and formatting before publishing.

### 10. Publish the report
Save and publish the report to Schwab-Analytics-Dev.

Use a name such as Housing Market Copilot Report. Add a note that the report is a lab artifact and not a production-certified report.

## You'll know it worked when
- Copilot created or edited at least one report page.
- The report uses Housing-Market-Insights, not a local CSV import.
- A narrative/summary visual appears and has been fact-checked.
- DAX Copilot produced a query that runs against the semantic model.
- Measure descriptions or metadata were improved based on Copilot output.

## Next
Previous: [Lab 6 - Semantic Model + Direct Lake](../lab-06-semantic-model-directlake/README.md). Continue to [Lab 8 - Migrate a Workbook](../lab-08-migrate-a-workbook/README.md).
