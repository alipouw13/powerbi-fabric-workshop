# Adoption roadmap

Deck slide 33. Three horizons, and one rule that keeps the first one honest.

> **The rule: nothing on the 30-day list may be blocked by a capability the organization
> does not have.**
>
> If an item needs Fabric capacity, a Lakehouse, OneLake, Direct Lake, embedded
> Copilot, a Data Agent, or a tenant setting that is not yet approved, it is not
> a NOW item. Move it to LATER and name the approval it is waiting on. A 30-day
> plan with a dependency on an unapproved capability is not a plan, it is a
> request.

Everything in NOW and NEXT is achievable with Power BI Desktop, Power Query, DAX,
the on-premises data gateway, and the Power BI Service.

---

## NOW: 0 to 30 days

| Item | What done looks like | Owner |
| --- | --- | --- |
| **Finish the five flagship reports** | One report per domain group, built on a star schema, themed, published to a real workspace, numbers reconciled to the Tableau original. | Each domain group |
| **Certify the shared semantic model** | At least one `sm_io_<domain>` model meets the certification criteria and is certified by an approved certifier. | Semantic model owner plus certifier |
| **Stand up dev, test and prod workspaces** | `IO-Analytics-Dev`, `IO-Analytics-Test`, `IO-Analytics-Prod` exist with roles assigned, and a deployment pipeline connects them. | I&O platform owner |
| **Name an owner per domain** | Business owner and technical owner recorded for all five domains, in the ownership table. | CoE lead |

Why these four: they are the smallest set that turns a workshop into an operating
practice. Reports prove it works, certification makes reuse the default,
workspaces make promotion repeatable, and named owners make everything else
possible.

### Success criteria at day 30

- Five reports exist, are published, and reconcile.
- One certified model, minimum.
- Three workspaces exist, and nobody is publishing to My workspace.
- Ten names in the ownership table, no blanks.

---

## NEXT: 30 to 90 days

| Item | What done looks like | Owner |
| --- | --- | --- |
| **Migrate the next tier of Tableau reports** | The P1 rows from the [assessment worksheet](migration-assessment-worksheet.md) are rebuilt, validated and published. | Domain owners |
| **Roll out the measure and theme library** | The [measure definitions](../src/pbip/README.md), the [Power Query snippets](../src/powerquery/README.md), and `io-workshop-theme.json` are in a shared location, and new reports use them by default. | CoE lead |
| **Propose Fabric capacity for leadership approval** | A written proposal covering the business case, cost, what it unlocks, and what stays the same without it. A proposal, not a dependency. | I&O platform owner plus CoE lead |
| **Run the first quarterly review** | Adoption, certification status, refresh health, migration progress, and a decision log. | CoE lead |

Note the shape of the Fabric item: **propose**, not adopt. Nothing in NOW or NEXT
waits on the outcome. If the proposal is approved, the LATER list opens up. If it
is not, the estate still works.

### Success criteria at day 90

- The P1 backlog is cleared or has an explicit reason per row.
- A new report author can find the theme, the snippets and the measure list
  without asking anyone.
- The capacity proposal is submitted, with a decision date.
- The first quarterly review has happened and produced a written action log.

---

## LATER: 90 days and beyond

| Item | Depends on | Note |
| --- | --- | --- |
| **Retire migrated Tableau workbooks** | Validated replacements and an owner sign-off per workbook | The point of the whole exercise. Set retirement dates during migration, not after |
| **Expand to adjacent I&O domains** | The five flagship models being stable and reused | Network, security operations, change management, vendor management |
| **Adopt OneLake, Lakehouse and Copilot once approved** | Fabric capacity approval, tenant settings, and a security review | **Future, approval-dependent.** Not usable now. Do not design toward it in a way that blocks current work |
| **Scale the Community of Practice** | Enough practitioners to sustain it | Office hours, a shared channel, a pattern library, an internal showcase |

Anything in this column is a candidate, not a commitment. Review it at each
quarterly session and move items up only when the dependency actually clears.

---

## Operating model

| Group | Responsibility |
| --- | --- |
| Executive sponsor | Sets priority, removes blockers, funds the capacity decision |
| Community of Practice | Standards, certification criteria, enablement, reusable patterns |
| I&O platform owner | Workspaces, gateway, tenant settings, refresh health |
| Domain owners (five) | Their semantic model, its measures, its RLS, its certification evidence |
| Report authors | Thin reports on certified models, and model enhancement requests |
| Champions | Help colleagues adopt the practice, and feed problems back to the CoE |

Keep it this small. A larger structure than the work requires is its own kind of
blocker.

## Enablement

| Audience | What they need | Format |
| --- | --- | --- |
| I&O leadership | What changed, where the certified reports are, how to subscribe | 30 minute briefing |
| Tableau analysts | The translation guide, DAX basics, model reuse | Hands-on session, this workshop |
| Report authors | Thin reports, slicers, field parameters, validation | Lab plus office hours |
| Model owners | Star schema, measures, RLS, certification | Working session |
| Platform admins | Workspaces, gateway, labels, tenant settings, pipelines | Governance review |

## Success metrics

| Metric | Definition | Direction |
| --- | --- | --- |
| Certified models | Models certified with a named owner | Increase |
| Tableau workbooks retired | Workbooks archived after a validated replacement | Increase |
| Consolidation ratio | Tableau workbooks retired divided by Power BI reports built | Increase, above 1 is good |
| Model reuse | Reports built on a certified model as a share of all reports | Increase |
| Reports in My workspace | Content with no owner and no backup path | Decrease to zero |
| Refresh success rate | Scheduled refreshes succeeding first time | Increase |
| Validation pass rate | Migrated reports tying out on first or second review | Increase |
| Definition questions | Repeated "why do these two reports disagree" tickets | Decrease |
| CoE participation | People attending office hours or contributing patterns | Increase |

Track the first four monthly. The rest quarterly.

## Communication rhythm

| Cadence | Session | Purpose |
| --- | --- | --- |
| Weekly | Migration standup | Backlog, blockers, validation, cutover status |
| Weekly | Office hours | Help authors, capture recurring problems |
| Monthly | CoE review | Standards, certification candidates, pattern library updates |
| Quarterly | Leadership readout | Progress, value delivered, capacity decision, next priorities |

## Risks and mitigations

| Risk | Mitigation |
| --- | --- |
| Users do not trust the new numbers | Parallel run, publish the tie-out evidence, agree tolerance up front |
| Authors build private models | Certify shared models, grant Build permission on them, require a stated reason for a new model |
| Tableau logic is undocumented | Inventory the calculations during Assess, validate each with the business owner |
| The migration stalls after the workshop | Named owners, a weekly standup, and dated retirement targets |
| Both tools run in parallel indefinitely | Set the Tableau retirement date when the migration starts, not when it finishes |
| Waiting on Fabric approval blocks progress | The NOW rule. Nothing in the first 30 days depends on it |
| Gateway becomes a bottleneck | Stagger refresh schedules, monitor the gateway, use incremental refresh on large facts |
| Momentum depends on one person | Two named owners per domain, and patterns written down rather than held in someone's head |

## Related

- [Workspace governance](workspace-governance.md)
- [Endorsement and certification](endorsement-certification.md)
- [Migration assessment worksheet](migration-assessment-worksheet.md)
- [Migration approaches](../reference/migration-approaches.md)
- [Current state and constraints](../reference/current-state.md)
- [Day 3 showcase](../sessions/day-3-showcase.md)
