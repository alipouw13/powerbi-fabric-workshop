# Lab 7 - Copilot in reports

**Duration:** ~75 min - **Deck:** "Copilot in Power BI"

You will use Copilot in Power BI to create report pages, summarize the insurance model, draft DAX, and generate measure descriptions. The lab shows why clean star modeling and friendly metadata matter.

## Schwab context
Copilot can help Schwab analysts move faster, but it is not a substitute for governed data. The better sm_insurance is modeled, named, described, and secured, the more useful Copilot becomes for insurance reporting.

## What you'll build
- Copilot-generated report page ideas for rpt_insurance_executive
- A narrative visual that summarizes premium and loss ratio performance
- A DAX draft for a Loss Ratio YoY measure
- Measure descriptions for the core insurance measures
- A review checklist for AI-generated content before publishing

## Prerequisites
- Completed [Lab 6 - Semantic model and Direct Lake](../lab-06-semantic-model-directlake/README.md)
- sm_insurance with core measures and descriptions
- Access to Copilot in Power BI in a supported Fabric capacity
- Reference doc: [Copilot in Power BI](../../reference/copilot-in-power-bi.md)

## Steps
### 1. Confirm the model is Copilot-ready
- Open sm_insurance.
- Confirm the core measures are present: Written Premium, Earned Premium, Policies In Force, Policies Written, Incurred Losses, Paid Losses, Claim Count, Loss Ratio, Average Premium, Written Premium PY, and Written Premium YoY %.
- Confirm business columns have friendly names and descriptions.
- Confirm technical keys are hidden.
- Confirm dim_date is marked as the date table.
- Confirm AI instructions and verified answers are available or documented.
- Fix metadata gaps before asking Copilot to build report content.

### 2. Ask Copilot to draft report pages
- Create or open rpt_insurance_executive in Schwab-Analytics-Dev.
- Use Copilot to create a page for executive insurance performance.
- Ask for a page that includes Written Premium, Earned Premium, Loss Ratio, premium by product, and loss ratio by region.
- Review the proposed visuals.
- Keep useful visuals and remove anything that duplicates Lab 3 without improvement.
- Rename the page if needed to Insurance Executive Overview.
- Check all measures for correct aggregation and formatting.

### 3. Create a claims perspective page
- Ask Copilot to create a claims performance page.
- Include Incurred Losses, Paid Losses, Claim Count, severity, loss_type, coverage, and region.
- Validate that Copilot uses fact_claim and dim_coverage correctly.
- Add slicers for product, region, and severity.
- Confirm loss_type values make sense in the insurance context.
- Use this page to discuss claim operations and reserve review.

### 4. Add a narrative or summary visual
- Add a narrative visual to the executive page.
- Ask it to summarize premium growth, loss ratio, and regional outliers.
- Slice to one product and confirm the summary updates.
- Slice to one region and confirm the summary updates.
- Rewrite any vague or unsupported sentence.
- Keep the narrative short enough for an executive reader.
- Do not publish AI-generated language without review.

### 5. Use Copilot for DAX drafting
- Ask Copilot or DAX Copilot to draft a measure named Loss Ratio YoY.
- Use the existing Loss Ratio, Written Premium PY, and Written Premium YoY % patterns as guidance.
- Review the DAX for correct date logic and use of dim_date.
- Test the measure by year and month.
- Keep the measure only if the numbers tie out.
- If it is not ready, save it as a draft note outside the certified model.

### 6. Generate measure descriptions
- Use Copilot to draft descriptions for Written Premium, Earned Premium, Incurred Losses, Paid Losses, Claim Count, Loss Ratio, and Average Premium.
- Review every description for insurance accuracy.
- Avoid descriptions that imply data lineage you have not validated.
- Add approved descriptions to sm_insurance.
- Confirm the descriptions improve field selection in Copilot prompts.
- Capture any measure that needs finance or claims owner review.

### 7. Review AI output before sharing
- Check visual titles and axes.
- Check measure choices.
- Check filters.
- Check narrative text.
- Check that RLS still applies for users who should see only their book.
- Confirm the report uses sm_insurance rather than a local extract.
- Save the report as rpt_insurance_executive.

## You'll know it worked when
- Copilot created at least one useful report page connected to sm_insurance.
- A narrative visual summarizes premium and loss ratio without unsupported claims.
- You reviewed a DAX draft for Loss Ratio YoY before keeping it.
- Measure descriptions are improved for the core insurance measures.
- You can explain that Copilot quality depends on clean star modeling, friendly names, descriptions, and governed measures.

## Next
[Lab 8 - Migrate a workbook](../lab-08-migrate-a-workbook/README.md)
