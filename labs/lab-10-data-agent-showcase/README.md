# Lab 10 - Data Agent showcase

**Duration:** ~30 min - **Deck:** "Data Agent showcase" - **Format:** facilitator demo

The facilitator creates a Fabric Data Agent grounded on sm_insurance and asks insurance questions in natural language. The goal is to show how governed semantic models make conversational analytics safer and more useful.

## Feature availability
Fabric Data Agents are not available to most attendees today, so this runs as a demo and a roadmap discussion, not a hands-on lab. The transferable lesson is the metadata work in step 2: descriptions, friendly names, and clear definitions improve report authoring and Microsoft 365 Copilot answers today, long before any agent is enabled. See [reference/schwab-environment-today.md](../../reference/schwab-environment-today.md).

## Schwab context
Business users often ask the same questions they tried in Tableau Ask Data, but they expect governed definitions and security. A Fabric Data Agent can answer from sm_insurance while honoring the same model, measures, and RLS choices used by reports.

## What you'll build
- A Fabric Data Agent grounded on sm_insurance
- Reused Prep-for-AI metadata from Lab 6
- A set of verified insurance questions and answers
- RLS validation for agent-book access
- A comparison between Data Agent and Tableau Ask Data

## Prerequisites
- Completed [Lab 9 - MCP and GitHub Copilot](../lab-09-mcp-github-copilot/README.md)
- sm_insurance with AI instructions, descriptions, and verified answers
- Facilitator access to create or configure a Fabric Data Agent in Schwab-Analytics-Dev
- RLS test user or View as role setup if available
- Reference docs: [Copilot in Power BI](../../reference/copilot-in-power-bi.md) and [Direct Lake](../../reference/direct-lake.md)

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
- The demo Data Agent is grounded on sm_insurance.
- It can answer top products by Written Premium.
- It can answer Loss Ratio by region YoY.
- It can identify worst-performing agents using a defined measure.
- RLS behavior is validated or documented for follow-up.
- You can explain how Data Agent differs from Tableau Ask Data in this Fabric migration story.
- The team captured the metadata improvements that pay off now, and whether Data Agent access is worth requesting.

## Next
[Lab 11 - Rayfin insurance app](../lab-11-rayfin-insurance-app/README.md)
