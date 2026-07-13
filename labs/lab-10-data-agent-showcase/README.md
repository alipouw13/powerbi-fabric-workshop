# Lab 10 - Data Agent Showcase

**Duration:** ~45 min - **Deck:** "Ask your data: the Fabric Data Agent"

You will create a Fabric Data Agent grounded on Housing-Market-Insights and test natural-language questions. The lab shows how the Prep-for-AI work from Lab 6 improves question answering.

## Schwab context
Tableau users may know Ask Data as a natural-language layer over published data sources. Fabric Data Agent fills a similar business need, but it benefits from Power BI semantic model metadata, measures, relationships, and verified answers.

For Schwab teams, the goal is governed self-service. Users should ask questions against certified models with Row-Level Security and clear ownership, not against unmanaged extracts.

## What you'll build
- A Fabric Data Agent connected to Housing-Market-Insights.
- Agent instructions that reuse the AI metadata from Lab 6.
- Verified natural-language answers for common housing market questions.
- A short RLS validation note.
- A comparison between Fabric Data Agent and Tableau Ask Data.

## Prerequisites
- Completed [Lab 9 - MCP + GitHub Copilot](../lab-09-mcp-github-copilot/README.md).
- Housing-Market-Insights with AI instructions and verified answers from Lab 6.
- Permission to create a Fabric Data Agent in Schwab-Analytics-Dev.
- Build permission on the semantic model.
- The Direct Lake model reference in [reference/direct-lake.md](../../reference/direct-lake.md).

## Steps
### 1. Open the Data Agent experience
In Fabric, open Schwab-Analytics-Dev and create a new Data Agent if the tenant has the feature enabled.

Name it Housing Market Data Agent. If the feature is not enabled, follow the facilitator demonstration and complete the prompt validation steps as a group.

### 2. Ground the agent on the semantic model
Select Housing-Market-Insights as the primary knowledge source.

Use the shared semantic model rather than raw files. This keeps answers aligned to governed measures such as Homes Sold, Avg Median Sale Price, and Months of Supply.

### 3. Reuse Prep-for-AI metadata
Review the AI instructions, synonyms, measure descriptions, and verified answers added in Lab 6.

Add or reference the same business context in the Data Agent instructions: 24 months of housing data, 12 metros, 4 property types, and Redfin plus MLS source patterns.

### 4. Ask a top metros question
Ask: "Which metros have the highest Homes Sold in the latest period?"

Confirm that the answer uses the Homes Sold measure and region values such as Seattle, WA, Denver, CO, Austin, TX, Phoenix, AZ, Chicago, IL, Atlanta, GA, Boston, MA, Nashville, TN, Charlotte, NC, Miami, FL, Portland, OR, and Dallas, TX.

### 5. Ask a YoY price question
Ask: "Which metros have the largest year-over-year change in Avg Median Sale Price?"

Check whether the answer uses the intended date context and measure logic. If it invents a calculation, refine the instruction or add a verified answer.

### 6. Ask a supply question
Ask: "Where is Months of Supply highest by property type?"

Confirm the answer respects property_type values: All Residential, Single Family Residential, Condo/Co-op, and Townhouse.

### 7. Inspect generated reasoning
Review any generated query, cited field, or source trace the Data Agent provides.

Look for model-aligned names. Good answers should refer to Housing-Market-Insights measures and dimensions, not raw CSV columns unless you asked for source lineage.

### 8. Validate Row-Level Security
If RLS roles are configured, test the agent as a restricted user or with a role view.

Confirm the answer only includes data the user is allowed to see. RLS should carry through the governed semantic model path.

### 9. Compare with Tableau Ask Data
Discuss what feels familiar and what feels different.

The familiar part is natural-language exploration. The different part is that the Fabric Data Agent should be grounded in a governed semantic model with descriptions, verified answers, and security controls.

### 10. Capture useful questions
Save three good prompts and one prompt that needs model improvement.

Use the weak prompt to decide whether you need a better measure description, synonym, verified answer, or security clarification.

## You'll know it worked when
- Housing Market Data Agent is grounded on Housing-Market-Insights.
- It answers questions about top metros, YoY price change, and Months of Supply.
- Answers use governed measure names where appropriate.
- RLS behavior has been checked or documented as a follow-up.
- You can contrast Fabric Data Agent with Tableau Ask Data.

## Next
Previous: [Lab 9 - MCP + GitHub Copilot](../lab-09-mcp-github-copilot/README.md). Continue to [Lab 11 - Showcase & Next Steps](../lab-11-showcase-next-steps/README.md).
