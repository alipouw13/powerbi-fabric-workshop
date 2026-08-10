# Lab 7 - Copilot options for report authors

**Duration:** ~45 min - **Deck:** "Copilot in Power BI"

You will see what Copilot embedded in Power BI does for report authors, and then
do the hands-on part with **Microsoft 365 Copilot**, which is the option this
audience is more likely to have today. The lab shows why clean star modeling and
friendly metadata matter for either path.

## Feature availability
Copilot embedded in Power BI is locked down for most attendees, and Copilot
Studio is not available. A few attendees have Microsoft 365 Copilot. So:

- **Sections 1 to 3 are a facilitator demo.** Watch and discuss; do not expect the
  Copilot pane in your own tenant.
- **Sections 4 to 6 are hands-on** with Microsoft 365 Copilot, or with a partner
  who has it if you do not.
- See [reference/schwab-environment-today.md](../../reference/schwab-environment-today.md)
  for the full picture and [Copilot in Power BI](../../reference/copilot-in-power-bi.md)
  for both option sets.

## Schwab context
Copilot can help Schwab analysts move faster, but it is not a substitute for governed data. The better sm_insurance is modeled, named, described, and secured, the more useful any Copilot becomes for insurance reporting. Until embedded Copilot is enabled, Microsoft 365 Copilot covers a lot of the same author tasks from outside the report canvas.

## What you'll build
- A shared view of what Copilot in Power BI generates from sm_insurance (demo)
- A Microsoft 365 Copilot prompt set for documenting and explaining the model
- A DAX draft for a Loss Ratio YoY measure, produced outside Power BI and tested inside it
- Measure descriptions for the core insurance measures
- A review checklist for AI-generated content before publishing
- A short list of the Copilot capabilities worth requesting for enablement

## Prerequisites
- Completed [Lab 6 - Semantic model and Direct Lake](../lab-06-semantic-model-directlake/README.md)
- sm_insurance with core measures and descriptions
- Microsoft 365 Copilot for the hands-on sections, if you have it
- Facilitator access to Copilot in Power BI for the demo sections
- Reference doc: [Copilot in Power BI](../../reference/copilot-in-power-bi.md)

## Steps
### 1. Confirm the model is Copilot-ready
- Open sm_insurance.
- Confirm the core measures are present: Written Premium, Earned Premium, Policies In Force, Policies Written, Incurred Losses, Paid Losses, Claim Count, Loss Ratio, Average Premium, Written Premium PY, and Written Premium YoY %.
- Confirm business columns have friendly names and descriptions.
- Confirm technical keys are hidden.
- Confirm dim_date is marked as the date table.
- Fix metadata gaps now, because they help report authors whether or not Copilot is enabled.

### 2. Demo: Copilot drafts report pages
- Facilitator: open rpt_insurance_executive in Schwab-Analytics-Dev.
- Use Copilot to create a page for executive insurance performance with Written Premium, Earned Premium, Loss Ratio, premium by product, and loss ratio by region.
- Review the proposed visuals as a group.
- Point out where Copilot used the governed measures and where it guessed.
- Discuss what would have to be true in the model for the output to be trustworthy.
- Note this as a capability to request rather than something to plan around today.

### 3. Demo: narrative visual and DAX assist
- Facilitator: add a narrative visual to the executive page and ask it to summarize premium growth, loss ratio, and regional outliers.
- Slice to one product and one region and show the summary update.
- Show DAX Copilot drafting a Loss Ratio YoY measure in DAX query view.
- Show the review step: correct date logic, correct use of dim_date, and a tie-out test.
- Emphasize that nothing generated is published without review.

### 4. Hands-on: use Microsoft 365 Copilot to explain the model
- Export or copy the sm_insurance table, column, and measure list into a document, or open the model documentation you captured in Lab 6.
- In Microsoft 365 Copilot chat, ask it to summarize the insurance model for a new analyst.
- Ask it to explain Loss Ratio, Earned Premium, and Written Premium YoY % in business terms.
- Ask it to list the questions this model can and cannot answer.
- Correct anything that is wrong, because Copilot only sees what you pasted.
- Keep the result as draft model documentation for the community of practice.

### 5. Hands-on: draft DAX and descriptions with Microsoft 365 Copilot
- Ask Microsoft 365 Copilot to draft a measure named Loss Ratio YoY, giving it the existing Loss Ratio, Written Premium PY, and Written Premium YoY % definitions as context.
- Paste the draft into Power BI Desktop and test it by year and month.
- Keep the measure only if the numbers tie out; otherwise keep it as a draft note outside the certified model.
- Ask Copilot to draft descriptions for Written Premium, Earned Premium, Incurred Losses, Paid Losses, Claim Count, Loss Ratio, and Average Premium.
- Review every description for insurance accuracy and avoid implied lineage you have not validated.
- Add approved descriptions to sm_insurance.

### 6. Hands-on: build the page yourself, Copilot-free
- Create or open rpt_insurance_executive in Schwab-Analytics-Dev.
- Build the executive page manually: Written Premium, Earned Premium, Loss Ratio, premium by product, and loss ratio by region.
- Add slicers for product, region, and severity.
- Confirm the report uses sm_insurance rather than a local extract.
- Compare your page to the Copilot demo output and note what Copilot saved and what it got wrong.
- Save the report as rpt_insurance_executive.

### 7. Review AI output before sharing
- Check visual titles and axes.
- Check measure choices.
- Check filters.
- Check narrative or generated text.
- Check that RLS still applies for users who should see only their book.
- Agree a rule for the community of practice: AI-generated DAX and text are reviewed by the model owner before publishing.

## You'll know it worked when
- You saw what Copilot in Power BI produces from a governed model and can explain the value.
- You used Microsoft 365 Copilot to summarize the model, draft DAX, or draft descriptions.
- A Loss Ratio YoY draft was tested before it was kept or discarded.
- Measure descriptions are improved for the core insurance measures.
- You built the executive page without depending on embedded Copilot.
- The team has a short list of Copilot capabilities to raise in the enablement conversation.

## Next
[Lab 8 - Migrate a workbook](../lab-08-migrate-a-workbook/README.md)
