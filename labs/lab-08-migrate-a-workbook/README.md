# Lab 8 - Migrate a workbook

**Duration:** ~120 min - **Deck:** "Migration breakout" - **Day 2**

**Scope:** In scope. This is the longest hands-on block in the workshop and the
one that most closely matches Monday-morning work.

You will migrate a Tableau Insurance workbook pattern onto sm_insurance. The coached breakout focuses on preserving business intent, validating totals, and adding a second operational claims triage use case.

## Schwab context
Real Tableau migrations are not copy and paste exercises. Schwab teams need to identify what each workbook is trying to answer, move calculations into a shared semantic model, and validate that business users can trust the Power BI version.

## What you'll build
- A migration plan for a Tableau Insurance workbook with three sheets
- A Power BI report connected to sm_insurance
- Pages for premium production, loss-ratio trend, and agent scorecard
- A claims triage page using ops/claims_intake.csv concepts
- A validation checklist that proves the numbers tie out

## Prerequisites
- Completed [Lab 6 - The shared semantic model](../lab-06-semantic-model-directlake/README.md)
- sm_insurance published to a workspace you can reach
- Core measures from Lab 6
- Access to the Tableau workbook description from the facilitator
- Reference docs: [migration approaches](../../reference/migration-approaches.md) and [migration assessment worksheet](../../governance/migration-assessment-worksheet.md)

## Steps
### 1. Assess the Tableau workbook
- Review the workbook description: Tableau Insurance workbook.
- Treat the source as a .hyper extract built from policy and claims data.
- Identify the three sheets: premium production, loss-ratio trend, and agent scorecard.
- For each sheet, write the business question in one sentence.
- Identify the filters used by the workbook, such as product, region, channel, year, and agent.
- Identify calculations that should move into sm_insurance.
- Mark any calculation that already exists as a core measure.

### 2. Map Tableau concepts to Power BI
- Map each Tableau sheet to a Power BI report page or visual group.
- Map Tableau dashboard layout to a Power BI report page, not a Power BI Service dashboard.
- Map Tableau extract fields to sm_insurance fields.
- Map Tableau calculated fields to measures in sm_insurance.
- Map Tableau filters to slicers, page filters, or report filters.
- Map Tableau actions to cross-filtering, drill-through, bookmarks, or buttons.
- Use [reference/tableau-to-powerbi.md](../../reference/tableau-to-powerbi.md) if your team needs a concept refresher.

### 3. Build the premium production page
- Create a new Power BI report connected to sm_insurance.
- Name the first page Premium Production.
- Add cards for Written Premium, Earned Premium, Policies Written, and Policies In Force.
- Add a bar chart for Written Premium by product.
- Add a line chart for Written Premium by dim_date[period_begin].
- Add a matrix for region and channel.
- Add slicers for product, region, channel, and year.
- Compare totals to the Tableau workbook notes or the Lab 6 DAX validation output.

### 4. Build the loss-ratio trend page
- Add a page named Loss Ratio Trend.
- Add a line chart for Loss Ratio over dim_date[period_begin].
- Add small multiples or a legend by product if it stays readable.
- Add a matrix for product, region, Earned Premium, Incurred Losses, Paid Losses, Claim Count, and Loss Ratio.
- Add conditional formatting to highlight high Loss Ratio.
- Validate that Loss Ratio uses DIVIDE([Incurred Losses], [Earned Premium]).
- Check one product and one region against expected values.

### 5. Build the agent scorecard page
- Add a page named Agent Scorecard.
- Use dim_agent[agent_name] and dim_agent[agency] as the row context.
- Add Written Premium, Policies Written, Incurred Losses, Claim Count, and Loss Ratio.
- Add a slicer for channel.
- Add a slicer for region.
- Sort agents by Loss Ratio descending for risk review, then by Written Premium for production review.
- Discuss how Power BI RLS would limit an agent to their own book.
- This is the same business rule you wrote down in Lab 4. Confirm the wording matches.

### 6. Add the claims triage use case
- Bring data/raw/ops/claims_intake.csv into the model through Power Query, using
  the shaping patterns from Lab 5.
- The feed includes claim_number, policy_number, product, region, coverage, loss_type, loss_date, reported_date, status, reserve_amount, paid_amount, severity, and adjuster.
- Decide where it belongs: does it extend fact_claim, or is it a separate operational fact?
- Add a Claims Triage page.
- Show open claims by severity and status.
- Show reserve_amount and paid_amount by region or adjuster.
- Add a table of high-severity open claims.
- Use this to discuss what operational reporting needs that executive reporting does not.

### 7. Validate the migration
- Validate Written Premium total.
- Validate Earned Premium total.
- Validate Incurred Losses total.
- Validate Claim Count.
- Validate Loss Ratio by product.
- Validate Loss Ratio by region.
- Validate that slicers match the Tableau workbook intent.
- Validate that RLS behavior is documented.
- Validate that no report-specific measure duplicates a governed measure in sm_insurance.

### 8. Capture migration decisions
- List fields that mapped cleanly.
- List calculations moved into sm_insurance.
- List visuals redesigned rather than copied.
- List validation gaps that need business owner input.
- List opportunities to replace workbook-specific extracts with shared semantic models.
- Save the report to your workspace.

### 9. Performance and troubleshooting clinic
This closes Day 2. Bring the problems you actually hit today.

- Open Performance Analyzer on your slowest page. Record the slowest visual and
  whether the time went to DAX query, visual display, or other.
- Common causes, in the order you should check them: too many visuals on one page,
  a measure that iterates a large table, a bidirectional relationship, a
  calculated column that should be a measure, and an import that is far wider
  than the report needs.
- Compare against the Tableau version. Where Power BI is slower, it is usually a
  model shape problem, not an engine problem.
- Walk the refresh path: source, gateway, credentials, schedule. Write down which
  hop you would check first for each failure symptom.
- Add the fixes you found to your team's checklist. This checklist is a Lab 12
  deliverable for the community of practice.

## You'll know it worked when
- The report connects to sm_insurance, not a local extract.
- Premium Production, Loss Ratio Trend, and Agent Scorecard pages exist.
- The claims triage use case is prototyped or documented against ops/claims_intake.csv.
- Core measures tie out to the agreed validation source.
- You can explain which Tableau logic moved into the shared semantic model.

## Next
That closes Day 2. Day 3 starts with
[Lab 7 - M365 Copilot for DAX and Power Query](../lab-07-copilot-reports/README.md).
