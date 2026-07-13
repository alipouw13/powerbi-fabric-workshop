# Lab 11 - Showcase & Next Steps

**Duration:** ~45 min - **Deck:** "Showcase, lessons learned, reusable patterns"

You will present what your team built and turn the workshop work into reusable next steps. The lab closes with patterns, owners, and commitments that help Schwab teams keep momentum after the three-day workshop.

## Schwab context
A workshop only matters if teams leave with repeatable patterns and clear ownership. Schwab Tableau teams should be able to identify which assets to migrate, which models to certify, and which developer workflows to standardize.

You will connect the hands-on outputs back to governance, adoption, and delivery. The goal is a practical plan, not a generic transformation slide.

## What you'll build
- A 5-minute team showcase.
- A lessons learned list for Tableau-to-Power BI migration.
- A reusable pattern catalog for future Schwab projects.
- A first adoption roadmap using [governance/adoption-roadmap.md](../../governance/adoption-roadmap.md).
- A commitment table with owners and dates.
- A clear list of follow-up risks and dependencies.

## Prerequisites
- Completed [Lab 10 - Data Agent Showcase](../lab-10-data-agent-showcase/README.md).
- A report, semantic model, or Data Agent artifact to demonstrate.
- Access to [governance/adoption-roadmap.md](../../governance/adoption-roadmap.md).
- Notes from [governance/workspace-governance.md](../../governance/workspace-governance.md) and [reference/migration-approaches.md](../../reference/migration-approaches.md).
- Team agreement on who will present.

## Steps
### 1. Prepare your showcase package
Choose one report page, one semantic model decision, and one governance decision to show.

Use the assets from prior labs: Housing Market Overview, Housing-Market-Insights, the migrated workbook pages, the MCP workflow, or the Housing Market Data Agent.

### 2. Use a simple presentation flow
Keep the showcase to 5 minutes.

Use this flow: business question, original Tableau pattern, Power BI or Fabric design, validation evidence, and what the team would do next.

### 3. Demonstrate a reusable model pattern
Show how Housing-Market-Insights separates facts, dimensions, and measures.

Explain why the star model and shared semantic model are reusable beyond the housing dataset. This is the pattern most Tableau migrations should evaluate first.

### 4. Demonstrate a reusable report pattern
Show one report page that uses clear KPI cards, trend visuals, slicers, and drill-through.

Call out what you would turn into a template report for future Schwab teams.

### 5. Demonstrate a reusable delivery pattern
Show how Dev/Test/Prod workspaces, endorsement, PBIP, and CI/CD fit together.

Reference [src/cicd/parameter.yml](../../src/cicd/parameter.yml) and [src/cicd/.github/workflows/fabric-cicd.yml](../../src/cicd/.github/workflows/fabric-cicd.yml) if your team reached Lab 9.

### 6. Capture lessons learned
Create a shared list of what surprised the team.

Prompts: What changed from Tableau? Which model choices improved report quality? Where did Copilot help? Which governance decisions need to be made earlier?

### 7. Build the reusable pattern catalog
List the patterns the group wants to reuse.

Include template report, shared certified model, measure library, deployment pipeline, MCP developer loop, migration assessment worksheet, and Data Agent prompt validation.

### 8. Walk the adoption roadmap
Open [governance/adoption-roadmap.md](../../governance/adoption-roadmap.md).

Map the next 30, 60, and 90 days. Include pilot workbooks, certified semantic models, workspace governance, training, support model, and success metrics.

### 9. Assign commitments and owners
Create a commitment table with item, owner, due date, dependency, and success signal.

Examples: identify top Tableau workbooks for assessment, select a certified model owner, define workspace role policy, pilot PBIP workflow, and schedule office hours.

### 10. Close with risks and follow-ups
List the risks that could slow adoption.

Common risks include unclear ownership, missing capacity settings, weak model documentation, unmanaged extracts, lack of Build permission process, and no certification review path.

## You'll know it worked when
- Each team presented a concrete artifact or decision.
- The group captured lessons learned from the migration labs.
- Reusable patterns are listed with enough detail to apply again.
- The adoption roadmap has 30, 60, and 90 day actions.
- Commitments have named owners, dates, dependencies, and success signals.

## Next
Previous: [Lab 10 - Data Agent Showcase](../lab-10-data-agent-showcase/README.md). Continue with [the adoption roadmap](../../governance/adoption-roadmap.md).
