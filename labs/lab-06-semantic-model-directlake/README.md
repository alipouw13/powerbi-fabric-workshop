# Lab 6 - The shared semantic model

**Duration:** ~90 min - **Deck:** "Semantic models" - **Day 2**

**Scope:** In scope. Built in Power BI Desktop on the Import or DirectQuery
connection from Lab 5. No Lakehouse, no Direct Lake.

You will turn the queries you shaped in Lab 5 into `sm_insurance` - the governed
foundation every report builds on. This is the asset that replaces "one extract
per workbook", and it is entirely achievable with the tools Schwab has today.

## Schwab context
The migration goal is not one report. The goal is a shared, certified semantic
model that Schwab teams reuse across reports and Excel, instead of one model per
workbook. Every report built on `sm_insurance` inherits the same definition of
Written Premium and Loss Ratio - which is the actual fix for "three dashboards,
three different numbers". None of this requires Fabric. It requires agreement,
and the modeling discipline in this lab.

## What you'll build
- A semantic model named `sm_insurance` in Import or DirectQuery mode
- A star model using fact_premium, fact_claim, dim_customer, dim_agent,
  dim_policy, dim_coverage, and dim_date
- Core measures with the exact names used throughout the workshop
- Clean metadata: friendly names, descriptions, hidden keys, formatted values
- A published, endorsed model that other reports can connect to as a live connection

## Prerequisites
- Completed [Lab 5 - Connect and transform in Power Query](../lab-05-ingestion-onelake/README.md)
- Your shaped fact and dimension queries from Lab 5
- Power BI Desktop
- Measure definitions in [src/pbip/README.md](../../src/pbip/README.md)
- Sample DAX in [src/sql/sample_dax_queries.dax](../../src/sql/sample_dax_queries.dax)
- Reference doc: [current state](../../reference/schwab-current-state.md)

## Steps
### 1. Create sm_insurance
- Continue in the Power BI Desktop file from Lab 5, or start a new file pointing
  at the same source.
- Confirm the loaded tables are exactly the ones you shaped: fact_premium,
  fact_claim, dim_customer, dim_agent, dim_policy, dim_coverage, and dim_date.
- Confirm your staging queries have **Enable load** switched off. They should not
  appear in the model.
- Save the file as `sm_insurance.pbix`.
- Note your storage mode from Lab 5 step 2, and confirm it is applied consistently
  across tables. A model that mixes Import and DirectQuery without a reason is a
  troubleshooting problem waiting to happen.
- You will publish this to a workspace - not My workspace - in step 7.

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

### 5. Clean the metadata
This is the difference between a model people adopt and a model people work around.

- Hide every technical key from report view: policy_id, customer_id, agent_id,
  coverage_id, date_id, claim_id.
- Use friendly names. "Written Premium" reads better than `written_premium` in a
  field list and in every visual title that inherits it.
- Add descriptions to all core measures. A report author hovering over a field
  should not have to ask what it means.
- Add descriptions to product, region, channel, agent_name, coverage, loss_type,
  severity, and status.
- Use display folders to group measures by subject: Premium, Claims, Time
  Intelligence.
- Set data categories where they help - dates, geography, and URLs behave better
  in visuals when categorized.
- Remove ambiguous duplicates. Two fields with the same business meaning is how a
  shared model loses trust.
- You will use these descriptions again in Lab 7 - they are the context you paste
  into M365 Copilot so it can help you without seeing your model.

### 6. Validate with DAX
- Open **DAX query view** in Power BI Desktop.
- Run a query from [src/sql/sample_dax_queries.dax](../../src/sql/sample_dax_queries.dax).
- Validate total Written Premium against the source.
- Validate Loss Ratio by product.
- Validate Written Premium YoY % by month and by year.
- Confirm Loss Ratio is calculated from the measures, not by averaging row-level
  ratios. This is the single most common insurance reporting error.
- Fix relationship or measure issues before moving on. Every report you build
  after this inherits whatever is wrong here.

### 7. Publish, endorse, and document ownership
- Publish to a workspace - not My workspace.
- If the source is on-premises, confirm the gateway data source is bound and the
  credentials are set.
- Set a refresh schedule if the model is Import.
- Set sm_insurance as **Promoted**.
- Do not **Certify** until a business owner reviews the definitions. Certification
  is a statement about the business meaning, not about the technical build.
- Record the model owner and the support contact.
- Record which workspace hosts the production version.
- Keep **Build** permission limited to users who need it for reports or Excel.
- Demonstrate the payoff: create a new report with **Get data > Power BI semantic
  models**, connect live to sm_insurance, and build a visual without importing
  anything. That is the pattern that replaces one-extract-per-workbook.

## You'll know it worked when
- sm_insurance is published to a shared workspace and endorsed as Promoted.
- The star uses fact_premium, fact_claim, dim_customer, dim_agent, dim_policy, dim_coverage, and dim_date.
- The model contains all core measures with exact names from this lab.
- Loss Ratio uses DIVIDE([Incurred Losses], [Earned Premium]).
- dim_date is marked as the date table on period_begin.
- Technical keys are hidden and every core measure has a description.
- A second report connects live to sm_insurance without importing data.
- You can state the model owner, the support contact, and who holds Build permission.

## Next
[Lab 8 - Migrate a workbook](../lab-08-migrate-a-workbook/README.md)
