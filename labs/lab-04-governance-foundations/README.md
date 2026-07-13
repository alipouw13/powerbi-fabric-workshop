# Lab 4 - Governance Foundations

**Duration:** ~45 min - **Deck:** "Governance & migration approaches"

You will define the governance basics for the workshop environment. The focus is practical: who can do what, where content moves, how users consume reports, and how trusted assets become Promoted or Certified.

## Schwab context
A Tableau migration is not only a rebuild of sheets and dashboards. Schwab teams also need a governed operating model so analytics content can move from development to production without losing ownership, security, or trust.

You will use Schwab-Analytics-Dev, Schwab-Analytics-Test, and Schwab-Analytics-Prod as the backbone for the rest of the workshop. The same pattern can scale to department, domain, or product analytics teams.

## What you'll build
- A basic role model for Admin, Member, Contributor, and Viewer.
- A Dev/Test/Prod content flow for the workshop assets.
- A workspace purpose statement for each workspace.
- A sensitivity label and endorsement checklist.
- A decision on workspaces versus apps for report distribution.
- A first look at deployment pipelines and migration approaches.

## Prerequisites
- Completed [Lab 3 - Visualization](../lab-03-visualization/README.md).
- Access to the three workshop workspaces.
- A published report or model from Day 1.
- Governance references: [workspace-governance.md](../../governance/workspace-governance.md), [endorsement-certification.md](../../governance/endorsement-certification.md), and [migration-approaches.md](../../reference/migration-approaches.md).

## Steps
### 1. Review workspace purposes
Open Schwab-Analytics-Dev, Schwab-Analytics-Test, and Schwab-Analytics-Prod.

Write a one-sentence purpose for each workspace. Dev is for authoring, Test is for validation, and Prod is for certified consumption.

### 2. Assign roles deliberately
Review the roles described in [governance/workspace-governance.md](../../governance/workspace-governance.md).

Use Admin for workspace owners, Member for trusted publishers, Contributor for builders who do not manage access, and Viewer for consumers. Avoid giving broad Admin access just to solve short-term access issues.

### 3. Separate build access from consume access
Discuss which users need to build reports and which users only need to view reports.

For report consumers, plan to distribute through an app from Schwab-Analytics-Prod instead of adding every user directly to the workspace.

### 4. Add or review sensitivity labels
Open a report or semantic model and review sensitivity label options.

If labels are enabled in the tenant, choose the workshop-approved label. If labels are not enabled, record that sensitivity labeling is a governance dependency for production rollout.

### 5. Plan endorsement
Open [governance/endorsement-certification.md](../../governance/endorsement-certification.md).

Use Promoted for content that the owning team recommends. Use Certified for content that meets a formal standard for ownership, documentation, data quality, support, and access review.

### 6. Compare workspaces and apps
Create a simple decision rule.

Use workspaces for collaboration among builders. Use apps for packaged consumption by business users, with navigation and permissions managed for the audience.

### 7. Introduce deployment pipelines
In Fabric, open Deployment pipelines if your tenant has the feature enabled.

Map Schwab-Analytics-Dev to the development stage, Schwab-Analytics-Test to the test stage, and Schwab-Analytics-Prod to the production stage. You will automate a version of this pattern in Lab 9.

### 8. Choose a migration approach
Read the migration approach options in [reference/migration-approaches.md](../../reference/migration-approaches.md).

For a Tableau workbook, decide whether the right approach is lift and shift, redesign into a shared model, or retire and replace. Most high-value Schwab assets should be redesigned around a shared semantic model.

### 9. Capture the governance checklist
Create a short checklist for any report before it moves to Prod.

Include owner, audience, data source, sensitivity label, endorsement status, validation evidence, support contact, and refresh or Direct Lake behavior.

## You'll know it worked when
- Each workspace has a clear purpose and role model.
- You can explain the difference between a workspace and an app.
- You know when Promoted and Certified should be used.
- You have a checklist for moving workshop content toward production.
- You understand why migration approach decisions affect governance.

## Next
Previous: [Lab 3 - Visualization](../lab-03-visualization/README.md). Continue to [Lab 5 - Ingestion to OneLake](../lab-05-ingestion-onelake/README.md).
