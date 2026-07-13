# Lab 6 - Semantic model and Direct Lake

**Duration:** ~90 min - **Deck:** "Semantic models + Direct Lake"

You will create sm_insurance as a Direct Lake semantic model on Fabric gold and star tables. The model becomes the governed foundation for reports, Copilot, MCP, Data Agent, and migration validation.

## Schwab context
The migration goal is not one report. The goal is a certified shared semantic model that Schwab teams can reuse across reports, Excel, Copilot, GitHub Copilot MCP workflows, and future Rayfin-connected operational analytics.

## What you'll build
- A Direct Lake semantic model named sm_insurance
- A star model using fact_premium, fact_claim, dim_customer, dim_agent, dim_policy, dim_coverage, and dim_date
- Core measures with exact names used throughout the workshop
- AI-ready metadata, AI instructions, and verified answers
- A promoted semantic model ready for rpt_insurance_executive

## Prerequisites
- Completed [Lab 5 - Ingestion to OneLake](../lab-05-ingestion-onelake/README.md)
- lh_insurance with Bronze, Silver, and Gold tables
- Power BI Desktop or Fabric semantic model authoring access
- Measure definitions in [src/pbip/README.md](../../src/pbip/README.md)
- Sample DAX in [src/sql/sample_dax_queries.dax](../../src/sql/sample_dax_queries.dax)
- Reference doc: [Direct Lake](../../reference/direct-lake.md)

## Steps
### 1. Create sm_insurance in Direct Lake mode
- In Schwab-Analytics-Dev, start from lh_insurance.
- Create a new semantic model named sm_insurance.
- Use Direct Lake storage mode.
- Select the tables needed for the star: fact_premium, fact_claim, dim_customer, dim_agent, dim_policy, dim_coverage, and dim_date.
- Include gold_premium_summary, gold_loss_ratio, and gold_agent_scorecard if your facilitator wants aggregate views available for exploration.
- Save the semantic model.
- Remember that Direct Lake loads OneLake Delta data into memory on demand, with no import and no scheduled refresh.

### 2. Build the model relationships
- Connect dim_policy[policy_id] to fact_premium[policy_id].
- Connect dim_policy[policy_id] to fact_claim[policy_id].
- Connect dim_customer[customer_id] to dim_policy[customer_id].
- Connect dim_agent[agent_id] to fact_premium[agent_id].
- Connect dim_coverage[coverage_id] to fact_claim[coverage_id].
- Connect dim_date[date_id] to fact_premium[date_id].
- Connect dim_date[date_id] to fact_claim[date_id].
- Keep filters single-direction from dimensions to facts.
- Confirm there are no ambiguous paths.
- Hide technical keys from report authors.

### 3. Mark and enrich the date table
- Mark dim_date as the date table.
- Use dim_date[period_begin] as the date column.
- Sort dim_date[month_name] by dim_date[month].
- Add descriptions to year, quarter, month, month_name, period_begin, and period_end.
- Confirm time intelligence measures can use dim_date consistently.
- Use dim_date in every time-based visual and DAX query.

### 4. Add the core measures
- Add the exact measure names used by the workshop.
- Use [src/pbip/README.md](../../src/pbip/README.md) as the source of truth for full definitions.
- Create Written Premium.
- Create Earned Premium.
- Create Policies In Force.
- Create Policies Written.
- Create Incurred Losses.
- Create Paid Losses.
- Create Claim Count.
- Create Loss Ratio with this definition.

```DAX
Loss Ratio = DIVIDE([Incurred Losses], [Earned Premium])
```

- Create Average Premium.
- Create Written Premium PY.
- Create Written Premium YoY %.
- Format each measure as currency, whole number, decimal, or percentage as appropriate.

### 5. Prepare the model for AI
- Use friendly table names or display folders if your team prefers them.
- Add descriptions to all core measures.
- Add descriptions to product, region, channel, agent_name, coverage, loss_type, severity, and status.
- Add AI instructions that tell Copilot and Data Agent to answer using the governed measures.
- Add verified answers for common questions, such as top products by written premium and loss ratio by region.
- Confirm that the AI data schema exposes business fields and hides technical keys.
- Good metadata is required for good Copilot output in Lab 7 and Data Agent output in Lab 10.

### 6. Validate with DAX
- Open a DAX query view or use another query surface available in your tenant.
- Run a query from src/sql/sample_dax_queries.dax.
- Validate total Written Premium.
- Validate Loss Ratio by product.
- Validate Written Premium YoY % by month or year.
- Compare a few totals to the Gold tables in lh_insurance.
- Fix relationship or measure issues before moving on.

### 7. Endorse and document ownership
- Set sm_insurance as Promoted if your tenant allows it.
- Do not certify until a business owner reviews the definitions.
- Record the model owner.
- Record the support contact.
- Record which workspace should host the production version.
- Keep Build permission limited to users who need it for reports, Excel, MCP, or validated downstream work.

## You'll know it worked when
- sm_insurance exists in Direct Lake mode.
- The star uses fact_premium, fact_claim, dim_customer, dim_agent, dim_policy, dim_coverage, and dim_date.
- The model contains all core measures with exact names from this lab.
- Loss Ratio uses DIVIDE([Incurred Losses], [Earned Premium]).
- dim_date is marked on period_begin.
- AI metadata, AI instructions, and verified answers are in place or documented for completion.

## Next
[Lab 7 - Copilot in reports](../lab-07-copilot-reports/README.md)
