# Lab 10 - Fabric Data Agent (appendix)

**Deck:** "Data Agent showcase" - **Appendix reading, not run**

> **Not in scope for this workshop.** Fabric Data Agents and Copilot Studio are
> not available to this audience, and neither is the Lakehouse this pattern
> assumes. This page is kept as reference only. It is **not demoed and not a
> prerequisite for anything**. See
> [reference/schwab-current-state.md](../../reference/schwab-current-state.md).
>
> **The part you can act on today:** everything that would make a Data Agent good
> is metadata work you can do right now - clear names, descriptions, governed
> measures, and a star schema. That work is in
> [Lab 6](../lab-06-semantic-model-directlake/README.md) and it pays off
> immediately, whether or not an agent ever exists.

A Fabric Data Agent grounded on a governed semantic model answers business
questions in natural language while honoring the same measures and RLS used by
reports - the successor to what Tableau Ask Data attempted.

## What it would look like
- A Fabric Data Agent grounded on sm_insurance
- Reused metadata and descriptions from Lab 6
- A set of verified insurance questions and answers
- RLS validation for agent-book access

## Reference docs
[M365 Copilot for Power BI work](../../reference/copilot-in-power-bi.md),
[current state](../../reference/schwab-current-state.md)

## Steps
### 1. Create the Data Agent
- In Fabric, create a Data Agent in Schwab-Analytics-Dev.
- Name it Contoso Insurance Data Agent or follow the facilitator naming standard.
- Ground it on sm_insurance.
- Include the certified or promoted version of the model if available.
- Confirm the agent can see the core measures and business columns.
- Do not ground the agent on the Lab 1 wide extract.

### 2. Reuse Prep-for-AI metadata
- Review the descriptions added in Lab 6.
- Confirm product, region, channel, agent_name, coverage, loss_type, severity, and status are understandable.
- Confirm the core measures have business descriptions.
- Add or refine AI instructions so the agent uses governed measures.
- Add verified answers for common questions if your tenant supports them.
- Keep instructions short, specific, and tied to sm_insurance.

### 3. Ask premium questions
- Ask: Which products have the highest Written Premium?
- Ask: What is Written Premium by region for the last 24 months?
- Ask: Which channel has the highest Average Premium?
- Ask: How did Written Premium YoY % change by product?
- Check whether the agent uses Written Premium, Average Premium, and Written Premium YoY % correctly.
- If the answer is vague, improve descriptions or verified answers rather than adding report-specific logic.

### 4. Ask claims and loss questions
- Ask: What is Loss Ratio by region year over year?
- Ask: Which products have the highest Incurred Losses?
- Ask: Which coverage areas have the highest Claim Count?
- Ask: Who are the worst-performing agents by Loss Ratio?
- Confirm the agent explains the basis for worst-performing, such as high Loss Ratio or high Incurred Losses.
- Check that Loss Ratio is calculated from governed measures, not by averaging row-level ratios.

### 5. Validate RLS behavior
- Test with View as role if available.
- Test with a user or group that should be limited to one agent book.
- Ask a question that would reveal another agent's book.
- Confirm the answer respects the RLS filter.
- Remember that Execute Query through MCP also enforces RLS.
- Record any gap between expected and observed access.

### 6. Compare with Tableau Ask Data
- Tableau Ask Data starts from a Tableau data source experience.
- The Fabric Data Agent starts from governed Fabric semantic models and AI metadata.
- The quality of both depends on names, synonyms, and clear definitions.
- In this workshop, sm_insurance provides a reusable model for reports, Copilot, MCP, and Data Agent.
- This reduces the number of one-off extracts and workbook-specific calculations.
- Capture which business questions should become verified answers.

### 7. Prepare the showcase question set
- Pick three premium questions.
- Pick three claims questions.
- Pick one RLS validation question.
- Pick one question that failed and explain how metadata would improve it.
- Save the question set for Lab 12.
- Keep answers tied to the data visible in your workspace.

## You'll know it worked when
- The Data Agent is grounded on sm_insurance.
- It can answer top products by Written Premium.
- It can answer Loss Ratio by region YoY.
- It can identify worst-performing agents using a defined measure.
- RLS behavior is validated or documented for follow-up.
- You can explain how Data Agent differs from Tableau Ask Data in this Fabric migration story.

## Back to the workshop
[Lab 12 - Community of practice and next steps](../lab-12-showcase-next-steps/README.md)
