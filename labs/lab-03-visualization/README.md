# Lab 3 - Visualization

**Duration:** ~75 min - **Deck:** "Visualization best practices" - **Day 1**

**Scope:** In scope.

You will rebuild the first executive-ready insurance view on the star model. The page focuses on premium production, loss ratio, product mix, and regional performance.

## Schwab context
A migration succeeds when business users see familiar insights in a cleaner, more governed experience. For the Contoso Insurance story, executives need to understand written premium, earned premium, claims, and loss ratio by product, region, and channel.

## What you'll build
- A report page named Insurance Executive Overview
- KPI cards for Written Premium, Earned Premium, Policies In Force, and Loss Ratio
- Product mix and regional performance visuals
- A loss ratio trend using dim_date
- A clean visual layout that can become rpt_insurance_executive

## Prerequisites
- Completed [Lab 2 - Data modeling](../lab-02-data-modeling/README.md)
- A Power BI file with the Contoso Insurance star schema
- Starter measures for Written Premium, Earned Premium, Incurred Losses, Claim Count, and Loss Ratio
- Reference docs: [architecture](../../reference/architecture.md) and [sources](../../reference/sources.md)

## Steps
### 1. Create the executive page frame
- Open contoso-insurance-star.pbix.
- Rename the first page to Insurance Executive Overview.
- Set the page size to 16:9.
- Add a title text box: Contoso Insurance Executive Overview.
- Add a subtitle with the filters in scope, such as Products, Regions, Channels, and Last 24 Months.
- Use a simple theme with high contrast and readable labels.
- Keep the page to one executive screen.

### 2. Add the KPI row
- Add a card for Written Premium.
- Add a card for Earned Premium.
- Add a card for Policies In Force if you created the measure in Lab 2.
- Add a card for Loss Ratio.
- Format premium as currency.
- Format Loss Ratio as a percentage with one decimal place.
- Use conditional formatting for Loss Ratio if your team has a target threshold.
- Keep card titles business-friendly and consistent with the semantic model.

### 3. Build product and region views
- Add a stacked bar chart for Written Premium by product.
- Add a column chart for Earned Premium by channel.
- Add a matrix with region on rows and these values: Written Premium, Earned Premium, Incurred Losses, Claim Count, and Loss Ratio.
- Sort the matrix by Loss Ratio descending for risk review.
- Add data bars or background color to the Loss Ratio column.
- Confirm that Auto, Home, Renters, Life, and Umbrella appear as products.
- Confirm that Northeast, Southeast, Midwest, Southwest, and West appear as regions.

### 4. Add the loss ratio trend
- Add a line chart with dim_date[period_begin] on the x-axis.
- Use Loss Ratio as the y-axis value.
- Add product as a legend only if the chart stays readable.
- If the legend is too crowded, create a product slicer instead.
- Use a continuous date axis if it improves readability.
- Add a reference line if your group has a target loss ratio.
- Explain that this trend is the insurance equivalent of a finance margin or risk trend.

### 5. Add slicers and interactions
- Add slicers for product, region, channel, and year.
- Use dropdown slicers if space is limited.
- Edit interactions so KPI cards respond to slicers.
- Confirm the matrix, trend, and product visuals all filter consistently.
- Avoid slicers that duplicate what is already obvious in the visual.
- Keep all filters visible to avoid hidden context.

### 6. Apply report design best practices
- Align visuals to a grid.
- Use short titles that state the business question.
- Remove unnecessary borders, gridlines, and legends.
- Put the most important numbers in the top-left scan path.
- Use tooltips for detail rather than crowding the page.
- Add alt text for key visuals.
- Use consistent number formats across all visuals.

### 7. Validate the page
- Compare Written Premium total to the Lab 2 measure result.
- Slice to Auto and confirm all visuals respond.
- Slice to one region and confirm the matrix and trend respond.
- Check that Loss Ratio stays as a percentage, not a decimal.
- Save the file.
- Publish to Schwab-Analytics-Dev if your facilitator asks for a checkpoint.

## You'll know it worked when
- The page is named Insurance Executive Overview.
- The KPI row shows Written Premium, Earned Premium, Policies In Force, and Loss Ratio.
- Product, region, channel, and date filters work across the page.
- The regional matrix surfaces loss ratio differences clearly.
- The page can be reused as the first page of rpt_insurance_executive.
- You can explain which choices make the page easier to govern and certify later.

## Next
[Lab 4 - Governance foundations](../lab-04-governance-foundations/README.md)
