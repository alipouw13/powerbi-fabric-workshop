# Lab 2 - Data modeling

**Duration:** ~75 min - **Deck:** "Data modeling best practices"

You will replace the wide Tableau-style extract with an insurance star schema, and compare star, snowflake, and flat patterns. This is the biggest quality lever for performance, governance, and reusable reporting.

## Schwab context
Reporting today is very flat: wide tables and large Excel files, with logic repeated per report or workbook. A snowflake pattern is planned but not implemented, and there is no medallion structure yet. This lab introduces the preferred pattern early, on purpose, so new Power BI content is built on it instead of being reworked later.

## What you'll build
- A star model using dim_customer, dim_agent, dim_policy, dim_coverage, dim_date, fact_premium, and fact_claim
- Single-direction filtering from dimensions to facts
- A marked date table based on dim_date[period_begin]
- Friendly names, hidden keys, and starter measures for insurance reporting
- A list of modeling improvements to carry into sm_insurance in Lab 6
- A team decision on the preferred pattern: flat, star, or snowflake

## Prerequisites
- Completed [Lab 1 - Tableau to Power BI](../lab-01-tableau-to-powerbi/README.md)
- Power BI Desktop with access to data/raw/contoso/
- The wide file policy_claims_extract.csv from Lab 1 for comparison
- Reference docs: [Tableau to Power BI](../../reference/tableau-to-powerbi.md) and [architecture](../../reference/architecture.md)

## Steps
### 1. Review the wide extract as the Tableau way
- Open the Lab 1 PBIX.
- Go to Data view and inspect policy_claims_extract.
- Notice that policy_number, agent_name, customer_segment, product, region, premium, and claim fields are in one table.
- This is easy for a single workbook.
- It becomes brittle when multiple teams need one definition of Written Premium or Loss Ratio.
- Keep the file for comparison, but do not extend it.

### 2. Start a new star model file
- Create a new Power BI Desktop file.
- Use Get data, Text/CSV for each of these files.
- Load data\raw\contoso\dim_customer.csv.
- Load data\raw\contoso\dim_agent.csv.
- Load data\raw\contoso\dim_policy.csv.
- Load data\raw\contoso\dim_coverage.csv.
- Load data\raw\contoso\dim_date.csv.
- Load data\raw\contoso\fact_premium.csv.
- Load data\raw\contoso\fact_claim.csv.
- Save the file as contoso-insurance-star.pbix.

### 3. Create the relationships
- Open Model view.
- Connect dim_policy[policy_id] to fact_premium[policy_id].
- Connect dim_policy[policy_id] to fact_claim[policy_id].
- Connect dim_agent[agent_id] to fact_premium[agent_id].
- Connect dim_customer[customer_id] to dim_policy[customer_id].
- Connect dim_coverage[coverage_id] to fact_claim[coverage_id].
- Connect dim_date[date_id] to fact_premium[date_id].
- Connect dim_date[date_id] to fact_claim[date_id].
- Use one-to-many relationships where dimensions are on the one side.
- Keep cross-filter direction single.
- Avoid many-to-many relationships and bidirectional shortcuts.

### 4. Mark the date table
- Select dim_date.
- Choose Mark as date table.
- Select dim_date[period_begin] as the date column.
- Confirm year, month, month_name, and quarter are available for reporting.
- Sort month_name by month if needed.
- Use dim_date fields for all time visuals.

### 5. Clean the field list
- Hide technical keys such as policy_id, customer_id, agent_id, coverage_id, date_id, claim_id, and claim_number from report view when they are not useful to authors.
- Keep business identifiers such as policy_number visible only if report authors need drill-through.
- Rename tables to friendly names if your team wants spaces, such as Customer, Agent, Policy, Coverage, Date, Premium, and Claim.
- Add descriptions for important fields.
- Format written_premium, earned_premium, incurred_loss, and paid_loss as currency.
- Format ratios as percentages.

### 6. Add starter measures
- Create Written Premium from fact_premium[written_premium].
- Create Earned Premium from fact_premium[earned_premium].
- Create Incurred Losses from fact_claim[incurred_loss].
- Create Claim Count as a distinct count of fact_claim[claim_id] or a row count, based on your loaded data.
- Create Loss Ratio as DIVIDE([Incurred Losses], [Earned Premium]).
- Compare Written Premium totals against the Lab 1 extract page.
- Differences should be explainable by grain, date filters, or relationship filters.

### 7. Compare star, snowflake, and flat
- Flat, what you have today: one wide table per report or a large Excel file. Fast to start, but definitions drift, files grow, and refreshes get slower.
- Star, the Power BI default: facts joined to denormalized dimensions. Best query performance, simplest field list, and the pattern the engine is optimized for.
- Snowflake, the planned Schwab pattern: dimensions normalized into related tables, for example dim_policy referring to a separate product table. Supported by Power BI, and reasonable when the source is already normalized, but it adds joins and makes the field list harder to navigate.
- Practical guidance: normalize in the source or the transformation layer, then present a star to report authors.
- Note that the same layering idea appears again in Lab 5 as Bronze, Silver, and Gold, where Gold is the star that reporting consumes.
- Write down which pattern your team will require for new content, and what happens to the existing flat assets.

### 8. Document modeling decisions
- Capture which fields are hidden.
- Capture which relationships use single-direction filters.
- Capture the measure names that should become standard in sm_insurance.
- Note any fields that need business definitions from product, claims, or finance owners.
- This model will be rebuilt on Fabric gold tables in Lab 6.

## You'll know it worked when
- The model has two facts, fact_premium and fact_claim.
- The shared dimensions are dim_customer, dim_agent, dim_policy, dim_coverage, and dim_date.
- dim_date is marked as the date table on period_begin.
- Keys are hidden from report authors.
- Written Premium, Earned Premium, Incurred Losses, Claim Count, and Loss Ratio return expected values.
- You can explain why this star model performs and governs better than the wide extract or a large Excel file.
- Your team can state when a snowflake dimension is acceptable and when it should be flattened for reporting.

## Next
[Lab 3 - Visualization](../lab-03-visualization/README.md)
