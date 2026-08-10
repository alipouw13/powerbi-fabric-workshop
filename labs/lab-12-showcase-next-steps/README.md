# Lab 12 - Community of practice and next steps

**Duration:** ~60 min - **Deck:** "Showcase + next steps" - **Day 3**

**Scope:** In scope. This is the most important session of the workshop.

You will present what your team built, charter the **community of practice** for
data visualization, and leave with named owners for the next migration wave. The
workshop only pays off if this session produces commitments.

## Schwab context
The stated goal for this group is to form a community of practice and stand up a
center of excellence for data visualization inside the infrastructure team. This
room is cross-functional and decentralized - there is no shared naming standard,
no shared certification process, and no shared release practice yet. That is the
gap to close, and none of it requires a feature request. Reusable patterns from
this workshop - the star schema, the shared model, the migration checklist, the
governance path - are all available today.

## What you'll build
- A team showcase of what you built on Days 1 and 2
- A **community of practice charter**: purpose, membership, cadence, and standards
- A reusable pattern inventory for future migration work
- A ranked enablement request list for capabilities the team does not have
- An adoption roadmap with owners, commitments, and dates

## Prerequisites
- Completed Labs 0-8
- Your team's model, report, Power Query patterns, and Lab 7 documentation
- Reference docs: [current state](../../reference/schwab-current-state.md), [workspace governance](../../governance/workspace-governance.md), and [adoption roadmap](../../governance/adoption-roadmap.md)

## Steps
### 1. Prepare the team showcase
- Pick one presenter for how you connected to data.
- Pick one presenter for the semantic model.
- Pick one presenter for the migrated report.
- Keep each segment to three minutes.
- Focus on what changed for you as you moved from Tableau to Power BI.
- Use exact object names when presenting.

### 2. Present the connection and modeling decisions
- Show how you connected, and state your Import vs DirectQuery decision and why.
- Show your Power Query work: what folds, what you removed, how dimensions were
  built from reference queries, and any parameter or function you standardized.
- Show what you cut from the import and what that did to model size.
- Show your star model relationships.
- Say whether you snowflaked anything, and why or why not.
- Explain why shared semantic models reduce duplicate calculations.

### 3. Present the model and report pattern
- Show sm_insurance.
- Show core measures such as Written Premium, Earned Premium, Incurred Losses, Claim Count, Loss Ratio, Written Premium PY, and Written Premium YoY %.
- Show rpt_insurance_executive and the Insurance Executive Overview page.
- Show one migrated workbook page from Lab 8.
- Explain how a Tableau dashboard maps to a Power BI report page.
- Show the model documentation you drafted in Lab 7.

### 4. Charter the community of practice
This is the core of the session. Write it down, in the room.

- **Purpose.** One sentence. What does this group exist to do that no individual
  team can do alone?
- **Membership.** Who is in it, from which teams, and who is the accountable lead?
  Include the Austin and Phoenix split and how remote members participate.
- **Cadence.** How often does it meet, for how long, and in what format? A short
  recurring meeting that happens beats a long one that gets cancelled.
- **Scope.** Start narrow. Suggested first three: naming standards, a certification
  path, and a shared measure library.
- **First deliverables.** Pick two things this group will publish within 30 days.
  The model documentation template from Lab 7 and the naming standard are good
  candidates.
- **Escalation path.** How does the group raise a tooling or enablement request,
  and to whom? Use the path in
  [reference/schwab-current-state.md](../../reference/schwab-current-state.md).
- **How new members join.** A community of practice that has no on-ramp becomes a
  committee.

### 5. Agree the standards you can set today
None of these need a feature request. Decide as a group, and record the decision:

| Standard | Decision to make now |
| --- | --- |
| Workspace naming and structure | Dev/Test/Prod? By domain? By team? |
| Semantic model naming | Prefix convention, and who can create one |
| Measure naming | Business language, and where the definition lives |
| Certification | Who can certify, and what the bar is |
| Excel sources | When is Excel acceptable as a source, and when is it a ticket |
| Report review | What must be checked before a report is shared broadly |
| Shared vs. personal models | When is a new model justified |

- Compare your answers to
  [governance/workspace-governance.md](../../governance/workspace-governance.md)
  and [governance/endorsement-certification.md](../../governance/endorsement-certification.md).
- Assign one owner per standard. A standard with no owner does not exist.

### 6. Review reusable patterns
**Built in this workshop, usable Monday:**
- Shared, endorsed semantic model: sm_insurance, with live-connected reports.
- Measure library: Written Premium, Earned Premium, Policies In Force, Policies Written, Incurred Losses, Paid Losses, Claim Count, Loss Ratio, Average Premium, Written Premium PY, and Written Premium YoY %.
- Power Query patterns from [Lab 5](../lab-05-ingestion-onelake/README.md): folding checks, reference-query dimensions, staging queries with load disabled, parameters, custom functions, and the hardened Excel pattern.
- The M snippet library in `src/powerquery/`.
- Template report: rpt_insurance_executive.
- Migration checklist from [Lab 8](../lab-08-migrate-a-workbook/README.md) and [governance/migration-assessment-worksheet.md](../../governance/migration-assessment-worksheet.md).
- Governance checklist: workspace roles, sensitivity, RLS, endorsement, and ownership.
- The **M365 Copilot model context block** and the AI code review standard from [Lab 7](../lab-07-copilot-reports/README.md).

**Not available today - roadmap only:**
- Lakehouse, OneLake, medallion layering, Direct Lake, and Dataflows Gen2.
- Copilot embedded in Power BI, and Fabric Data Agents.
- MCP servers, PBIP source control, and CI/CD.

### 7. Build the prioritized enablement ask
- List the capabilities the team wants that it does not have.
- For each: who benefits, what it replaces, and what it would save.
- Rank them. A ranked list of three gets acted on; an unranked list of ten does not.
- Note what modeling and metadata work must happen first regardless of enablement -
  because that work is on you, not on the tenant admins. Almost everything that
  would make Copilot or a Data Agent useful is work you already know how to do.
- Name the owner who carries the ask forward.

### 8. Build the adoption roadmap
- Open [governance/adoption-roadmap.md](../../governance/adoption-roadmap.md).
- Pick the first Tableau workbook wave to assess.
- Pick the first shared semantic model candidate.
- Pick the first report template candidate.
- Pick the Excel sources that should become real SQL sources or shared models.
- Assign an owner for governance and standards.
- Assign an owner for connections and gateway coordination.
- Assign an owner for Power Query patterns and the M snippet library.
- Assign an owner for semantic modeling.
- Assign an owner for report migration.
- Assign an owner for the enablement asks.
- Assign the community of practice lead.
- Add target dates for the next 30, 60, and 90 days.

## You'll know it worked when
- Each team showed at least one working artifact from Days 1 and 2.
- The community of practice has a written charter with a named lead and a meeting
  on the calendar before everyone leaves the room.
- At least three standards are decided and each has an owner.
- The enablement ask is a ranked list of three, with an owner.
- The adoption roadmap has concrete 30, 60, and 90 day commitments with names on them.
- **Nothing on the 30-day list is blocked by a feature Schwab does not have.**

## Adoption close
Everything that matters most here is already within reach. Shape the data in Power
Query, model it as a star, certify shared measures, migrate reports onto the
shared model, and set the standards the community of practice will enforce - none
of that needs an approval or a new licence. Do the metadata and documentation work
now, because it is both immediately useful and the prerequisite for anything that
gets enabled later. Then make the enablement ask from a position of readiness
rather than curiosity.
