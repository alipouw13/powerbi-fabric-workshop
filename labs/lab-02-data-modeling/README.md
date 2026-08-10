# Lab 2 - Data modeling and architecture patterns

**Duration:** ~75 min - **Deck:** "Data modeling best practices" - **Day 1**

**Scope:** In scope. A star schema needs nothing but Power BI Desktop and
gateway-brokered SQL. No Fabric, no lake, no approval required.

You will replace the wide Tableau-style extract with an insurance star schema,
and you will leave with shared vocabulary for the modeling words that keep coming
up: **flat**, **star**, and **snowflake**. This is the biggest quality lever in
the whole workshop.

## Schwab context
Schwab's current analytics architecture is very flat, and a move to a snowflake
pattern is planned but not implemented. That makes this the right moment to agree
on the vocabulary, because the cost of getting model shape wrong compounds with
every workbook migrated. A Tableau workbook can hide a lot of business logic
inside one extract. A Power BI migration works best when the team agrees on a
shared semantic model that separates customer, agent, policy, coverage, date,
premium, and claim concepts - and it requires **no approval and no new tooling**.
You will build this shape by hand in Power Query in Lab 5.

## What you'll build
- A star model using dim_customer, dim_agent, dim_policy, dim_coverage, dim_date, fact_premium, and fact_claim
- Single-direction filtering from dimensions to facts
- A marked date table based on dim_date[period_begin]
- Friendly names, hidden keys, and starter measures for insurance reporting
- A snowflake variant of one dimension, and a decision about whether to keep it
- A list of modeling improvements to carry into sm_insurance in Lab 6

## Prerequisites
- Completed [Lab 1 - Tableau to Power BI](../lab-01-tableau-to-powerbi/README.md)
- Power BI Desktop with access to data/raw/contoso/
- The wide file policy_claims_extract.csv from Lab 1 for comparison
- Reference docs: [Tableau to Power BI](../../reference/tableau-to-powerbi.md) and [current state](../../reference/schwab-current-state.md)

## The vocabulary, before you build

These terms get used interchangeably and they should not be.

| Term | What it describes | Decided by | Available to Schwab today? |
| --- | --- | --- | --- |
| **Flat / wide** | One table with everything, logic baked in | Whoever built the extract | Yes - this is the current state |
| **Star** | Facts plus conformed dimensions, single-direction filters | The modeler | **Yes** - and it is the goal |
| **Snowflake** | Star, with dimensions normalized into sub-dimensions | The modeler | Yes |

One more term you will hear, so that it does not cause confusion later:
**medallion** (Bronze/Silver/Gold) describes how raw data is progressively refined
*on the way in*, in a data lake. It is **not** an alternative to a star schema,
and it is **not available to Schwab today** because there is no lake layer. Star
and snowflake describe how the semantic model is shaped for analysis. You can -
and here, must - adopt a star schema with nothing but Power Query and
gateway-brokered SQL. Mention it once, then move on.

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

### 7. Try the snowflake variant, then decide
- Schwab has stated a plan to move to a snowflake pattern, so test it here rather
  than discovering the tradeoffs in production.
- Split a descriptive attribute out of dim_policy into its own table - product is
  a good candidate. Create dim_product with product and any product attributes,
  and relate dim_product to dim_policy.
- Rebuild one visual that slices Written Premium by product and note whether
  anything changed for the report author.
- Now weigh it up as a group:

| Snowflake helps when | Star helps when |
| --- | --- |
| A sub-dimension is genuinely shared across several dimensions | Report authors need a short, obvious field list |
| Attributes change on a different cadence than the parent | Query performance matters and joins should be minimal |
| Source systems already maintain the hierarchy separately | Report authors and self-service users need to reason over the model |
| Storage of very wide dimensions is a real problem | The team is new to dimensional modeling |

- Power BI's engine is optimized for star schemas. Snowflake where the business
  genuinely requires it, not by default.
- Record your team's decision and the reason. That reasoning is more valuable to
  the community of practice than the decision itself.

### 8. Document modeling decisions
- Capture which fields are hidden.
- Capture which relationships use single-direction filters.
- Capture where you chose star over snowflake, and why.
- Capture the measure names that should become standard in sm_insurance.
- Note any fields that need business definitions from product, claims, or finance owners.
- This model becomes sm_insurance in Lab 6, built on the Power Query work in Lab 5.

## You'll know it worked when
- The model has two facts, fact_premium and fact_claim.
- The shared dimensions are dim_customer, dim_agent, dim_policy, dim_coverage, and dim_date.
- dim_date is marked as the date table on period_begin.
- Keys are hidden from report authors.
- Written Premium, Earned Premium, Incurred Losses, Claim Count, and Loss Ratio return expected values.
- You can explain the difference between flat, star, and snowflake without
  reaching for a slide, and say which one Schwab should tackle first.
- You can explain why this star model produces better performance and more
  reusable reporting than the wide extract.

## Next
[Lab 3 - Visualization](../lab-03-visualization/README.md)
