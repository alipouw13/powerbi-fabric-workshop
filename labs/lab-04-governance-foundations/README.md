# Lab 4 - Governance foundations

**Duration:** ~50 min - **Deck:** "Governance foundations" - **Day 1**

**Scope:** In scope. Workspace roles, RLS, sensitivity, and endorsement are
standard Power BI capabilities and need no enablement.

You will apply the governance pattern that makes the insurance migration safe to scale: workspace roles, sensitivity, endorsement, and row-level security for an agent's book of business.

## Schwab context
Schwab teams need more than a good-looking report. They need clear workspace roles, promotion paths, sensitivity labels, certified shared models, and access rules that match the way agents and teams are allowed to see insurance business data.

## What you'll build
- A governance checklist for Schwab-Analytics-Dev, Schwab-Analytics-Test, and Schwab-Analytics-Prod
- A draft RLS rule where agents see only their own book of business
- A written business rule for book-of-business access that any system could implement
- Endorsement guidance for promoted and certified semantic models
- A deployment pipeline path for rpt_insurance_executive and sm_insurance

## Prerequisites
- Completed [Lab 3 - Visualization](../lab-03-visualization/README.md)
- Access to the three workshop workspaces
- A star model with dim_agent, dim_policy, fact_premium, and fact_claim
- Reference docs: [workspace governance](../../governance/workspace-governance.md) and [endorsement certification](../../governance/endorsement-certification.md)
- Reference doc: [current state](../../reference/schwab-current-state.md)

## Steps
### 1. Review workspace roles
- Open Schwab-Analytics-Dev in the Power BI Service.
- Review workspace access.
- Use Admin only for workspace owners.
- Use Member or Contributor for builders who need to publish or edit content.
- Use Viewer for consumers who only need to read reports.
- Repeat the review for Schwab-Analytics-Test and Schwab-Analytics-Prod.
- Record any role assignments that should be changed after the workshop.

### 2. Define the dev, test, and prod path
- Treat Schwab-Analytics-Dev as the build workspace.
- Treat Schwab-Analytics-Test as the validation workspace.
- Treat Schwab-Analytics-Prod as the consumer workspace.
- Connect the three workspaces in a deployment pipeline if your tenant allows it.
- Promote content from Dev to Test only after measures and visuals tie out.
- Promote content from Test to Prod only after ownership, sensitivity, and endorsement are clear.
- Keep experimental extracts out of Prod.

### 3. Apply sensitivity and endorsement thinking
- Discuss which sensitivity label fits insurance policy and claim data.
- Apply a label if your tenant has labels configured for the workshop.
- Mark the Lab 1 extract model as not endorsed.
- Plan to promote sm_insurance after Lab 6 when it has clean measures and descriptions.
- Plan to certify sm_insurance only after business owner review.
- Use [endorsement certification](../../governance/endorsement-certification.md) as the checklist.

### 4. Create a Power BI RLS role
- In Power BI Desktop, open the star model.
- Select Manage roles.
- Create a role named Agent Book.
- Add a filter on dim_agent for the current user's identity if your data includes a user mapping field.
- For the lab, you can simulate the rule by filtering dim_agent[agent_name] to one sample agent.
- Confirm fact_premium and fact_claim filter through the model relationships.
- Use View as to test the role.
- Record what additional identity mapping would be required for production.

### 5. Write the rule down, once
- State the access rule as a plain business sentence: "an agent sees only policies
  and claims in their own book."
- Note that you just implemented that sentence as a Power BI RLS role.
- The same sentence would need implementing again in any other system that touches
  the same data - an operational app, an export, a downstream feed.
- Design the rule once, centrally, and implement it consistently. A rule that
  exists in three places with three slightly different definitions is a finding
  waiting to happen.
- Record where the authoritative version of this rule lives and who owns it.

### 6. Confirm least-privilege access
- Limit Build permission on semantic models to users and groups that need to create reports or connect Excel.
- Limit workspace Admin roles.
- Use deployment pipelines instead of direct edits in Prod, where your tenant supports them.
- Document who owns sm_insurance.
- Document who owns rpt_insurance_executive.

### 7. Capture the governance decision log
- Write down the workspace role pattern.
- Write down the endorsement path for sm_insurance.
- Write down the RLS approach for agents, and where the authoritative rule lives.
- Write down the deployment path from Dev to Test to Prod.
- Keep this decision log with the team, not inside the lab files.

## You'll know it worked when
- You can describe the difference between Admin, Member, Contributor, and Viewer for the workshop workspaces.
- You have a deployment path from Schwab-Analytics-Dev to Schwab-Analytics-Test to Schwab-Analytics-Prod.
- You have a draft Agent Book RLS role or a documented simulation.
- The book-of-business access rule is written down as a business sentence with a named owner.
- You know when to use Promoted and Certified endorsement for sm_insurance.

## Next
[Lab 5 - Connect and transform in Power Query](../lab-05-ingestion-onelake/README.md)
