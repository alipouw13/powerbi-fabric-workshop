# Lab 12 - Showcase and next steps

**Duration:** ~45 min - **Deck:** "Showcase + next steps"

You will present what your team built, connect the pieces into reusable patterns, and leave with owners for the next migration wave. This lab closes the workshop and replaces the old showcase-only ending.

## Schwab context
The workshop only matters if teams leave with repeatable patterns. Schwab can reuse the certified semantic model pattern, migration checklist, MCP developer loop, governance path, and Rayfin app template for the next set of Tableau and Fabric modernization work.

## What you'll build
- A team showcase that connects data, model, report, AI, MCP, and Rayfin
- A reusable pattern inventory for future insurance and enterprise analytics work
- An inspiration review using real example apps from reference/reference-apps.md
- An adoption roadmap with owners, commitments, and dates
- A closeout summary for the 3-day workshop

## Prerequisites
- Completed [Lab 11 - Rayfin insurance app](../lab-11-rayfin-insurance-app/README.md)
- Final or draft versions of lh_insurance, sm_insurance, rpt_insurance_executive, Data Agent, and rayfin-app/
- Validation notes from Labs 6, 8, 9, 10, and 11
- Reference docs: [reference apps](../../reference/reference-apps.md) and [adoption roadmap](../../governance/adoption-roadmap.md)

## Steps
### 1. Prepare the team showcase
- Pick one presenter for the data estate.
- Pick one presenter for the semantic model and report.
- Pick one presenter for Copilot, MCP, or Data Agent.
- Pick one presenter for the Rayfin app.
- Keep each segment to three minutes.
- Focus on what changed for you as you moved from Tableau to Power BI and Fabric.
- Use exact object names when presenting.

### 2. Present the Fabric data estate
- Show Schwab-Analytics-Dev, Schwab-Analytics-Test, and Schwab-Analytics-Prod.
- Show lh_insurance.
- Show Files/raw/contoso/ and Files/raw/ops/.
- Show bronze_policy_claims and bronze_claims_intake.
- Show dim_customer, dim_agent, dim_policy, dim_coverage, dim_date, fact_premium, and fact_claim.
- Show gold_premium_summary, gold_loss_ratio, and gold_agent_scorecard.
- Explain why claims_intake.csv is the bridge between operational apps and analytics.

### 3. Present the model and report pattern
- Show sm_insurance in Direct Lake mode.
- Show the star model relationships.
- Show core measures such as Written Premium, Earned Premium, Incurred Losses, Claim Count, Loss Ratio, Written Premium PY, and Written Premium YoY %.
- Show rpt_insurance_executive.
- Show the Insurance Executive Overview page.
- Show one migrated workbook page from Lab 8.
- Explain how a Tableau dashboard maps to a Power BI report page.
- Explain why shared semantic models reduce duplicate calculations.

### 4. Present AI and developer workflows
- Show one Copilot-generated report improvement from Lab 7.
- Show one Data Agent question and answer from Lab 10.
- Show one MCP schema or DAX query result from Lab 9.
- Mention that Execute Query enforces RLS and requires Build permission.
- Show how PBIP and src/cicd/ support source control and deployment.
- Explain when a team would use the remote Power BI MCP server and when it would use the local MCP server.

### 5. Present the Rayfin app pattern
- Show the running Contoso Claims Intake app if available.
- Show the Customer, Agent, Policy, and Claim entities.
- Show a saved policy and claim.
- Explain how Claim matches the shape of ops/claims_intake.csv.
- Explain the @role policy: an agent sees only their own book.
- Tie that directly back to the Power BI RLS role from Lab 4.
- Explain how Rayfin provides an operational app template on the same Fabric estate.

### 6. Review reusable patterns
- Certified shared model: sm_insurance.
- Measure library: Written Premium, Earned Premium, Policies In Force, Policies Written, Incurred Losses, Paid Losses, Claim Count, Loss Ratio, Average Premium, Written Premium PY, and Written Premium YoY %.
- Template report: rpt_insurance_executive.
- Deployment pipeline: Schwab-Analytics-Dev to Schwab-Analytics-Test to Schwab-Analytics-Prod.
- MCP developer loop: GitHub Copilot, Power BI MCP, PBIP, and Fabric CI/CD.
- Rayfin app template: rayfin-app/ for Fabric-backed operational apps.
- Governance checklist: workspace roles, sensitivity, RLS, endorsement, and ownership.

### 7. Get inspired by reference apps
- Open [reference/reference-apps.md](../../reference/reference-apps.md).
- Review the Report Optimizer, a capacity-optimizer Rayfin Fabric-capacity app.
- Review the Contoso Insurance end-to-end Fabric demo from fabric-test.
- Review the Language app for Azure Language voice and text translation.
- Review the AI Fitness Coach.
- For each app, identify the reusable pattern rather than copying the app directly.
- Decide which patterns fit Schwab's next migration or app modernization wave.

### 8. Build the adoption roadmap
- Open [governance/adoption-roadmap.md](../../governance/adoption-roadmap.md).
- Pick the first Tableau workbook wave to assess.
- Pick the first shared semantic model candidate.
- Pick the first report template candidate.
- Pick one operational app candidate where Rayfin could help.
- Assign an owner for governance.
- Assign an owner for data engineering.
- Assign an owner for semantic modeling.
- Assign an owner for report migration.
- Assign an owner for AI and MCP enablement.
- Assign an owner for Rayfin app evaluation.
- Add target dates for the next 30, 60, and 90 days.

## You'll know it worked when
- Each team can show at least one working artifact from the workshop.
- The team can explain the end-to-end flow from raw files to reports, AI, MCP, and Rayfin.
- Reusable patterns are captured with owners.
- The adoption roadmap has concrete 30, 60, and 90 day commitments.
- The group agrees which workbook, semantic model, and app pattern should be tackled next.

## Adoption close
Use the Contoso Insurance work as the reference pattern. Start with governed data, build a clean star, certify shared measures, migrate reports onto the shared model, add AI only after metadata is ready, use MCP for a reviewable developer loop, and use Rayfin when the business needs a Fabric-backed operational app.
