# Day 3 - Showcase, Lessons & Next Steps

**August 20, 2026 · 9:00 to 3:00 · Deck slides 27 to 36**

> **Outcome:** A committed 90-day adoption roadmap.

Day 3 has **no hands-on labs**. Everything built happened on Day 2. Today is
about locking in what worked, being honest about what did not, and leaving with
commitments that have names on them.

Leadership joins the afternoon. The roadmap and next steps are the artifacts we
leave with.

## Run of show

Deck slide 28.

| Time | Session | Lead | Focus |
| --- | --- | --- | --- |
| 9:00 | Group showcases, five domains | All groups | Ten minutes each: the report and how it was built |
| 10:30 | Lessons learned and pitfalls | All groups | What surprised us, what to avoid |
| 11:15 | Reusable patterns library | Microsoft | Templates, measures, and themes to keep |
| 11:45 | Art of the possible: Fabric, once approved | Microsoft | A preview of what is next, clearly future |
| 1:00 | Adoption roadmap: now, next, later | Ricky | Sequence the migration across I&O |
| 2:00 | Community of Practice and next steps | Ricky | Champions, coaching, quarterly reviews |

---

## 9:00 - Group showcases

Ten minutes per group. Structure each one the same way so the room can compare:

1. **The question** your report answers, in one sentence (Lab 2, step 1).
2. **The model** - show the star in Model view. Name your grain.
3. **The report** - walk the page. Do not narrate every visual; answer the question.
4. **One measure** you are proud of, and what `CALCULATE` is doing in it.
5. **One thing that broke**, and how you fixed it.

Point 5 is the most valuable ten seconds of each showcase. Do not let groups skip
it to look polished.

## 10:30 - Lessons learned

Deck slide 30 lists the pitfalls to check yourselves against:

| Pitfall | The fix |
| --- | --- |
| Porting the flat extract | Model the star first |
| Bidirectional everywhere | Default to single direction |
| Calculated columns for everything | Prefer measures for anything aggregated |
| No owner, no endorsement | Certify one and point people to it |
| DirectQuery by reflex | Import by default today |
| Skipping validation | Reconcile against Tableau before you retire it |

Add the ones this room actually hit. Two that usually surface here:

- **The gateway string mismatch.** `SQLPROD01` versus `sqlprod01.schwab.com`.
- **Generated DAX that was right at the total and wrong by month.** Ask which
  groups caught it, and how.

## 11:15 - Reusable patterns library

Deck slide 31. What every group can lift so nobody starts from a blank page:

| Pattern | Where it lives |
| --- | --- |
| Conformed dimensions - Date, CI, Service, Team, Location, Severity | `data/raw/sql/dim_*.csv`, and the model pattern in [Lab 1](../labs/lab-01-semantic-model/README.md) |
| Measure library - totals, running sums, period over period, percent of total | [`src/sql/sample_dax_queries.dax`](../src/sql/sample_dax_queries.dax) |
| Report theme | [`src/theme/schwab-io-theme.json`](../src/theme/schwab-io-theme.json) |
| Page templates - trend, breakdown, KPI | [Lab 2](../labs/lab-02-report-page/README.md) |
| Power Query snippets - staging, reference dimensions, folder combine, schema guard | [`src/powerquery/README.md`](../src/powerquery/README.md) |
| M365 Copilot specialist agents and prompt patterns | [copilot-agents.md](../reference/copilot-agents.md) |
| Gateway request template | [gateway-setup.md](../reference/gateway-setup.md#9-what-to-ask-for-if-you-cannot-do-this-yourself) |
| Q&A synonyms - domain vocabulary | Per model, added in Lab 1 |
| Deployment pipeline - dev to test to prod | [workspace governance](../governance/workspace-governance.md) |

Assign an owner to each pattern. A pattern with no owner is a document nobody
updates.

## 11:45 - Art of the possible: Fabric, once approved

Deck slide 32, with slides 15 and 16 as the callback. **Clearly future. Clearly
approval-dependent.**

The speaker notes on all three slides say the same thing: most attendees do not
have embedded Copilot, Copilot Studio, MCP servers or Data Agent access, and
OneLake and Lakehouse are not approved for this environment. Frame it as a
readiness path, not a capability.

| Slide | Topic | Position it as |
| --- | --- | --- |
| 32 | Governed semantic models: what unlocks AI | The readiness checklist - and note how much of it Day 2 already delivered |
| 15 | Embedded Copilot and natural-language assistance | What becomes possible once licensing and governance are approved |
| 16 | Fabric, OneLake, and governed agents | The broader platform, once OneLake is approved |

Slides 15 and 16 were previewed on Day 1 afternoon. Returning to them here is
deliberate: the room has now built the thing that makes them worth having.

**The point to land:** slide 32's readiness list is almost entirely work this room
did on Day 2. Certified models, documented logic, proven RLS, usage signal. The
missing items are capacity and executive sign-off - and those are asks, not
engineering.

Do not demo anything here. A live demo of an unavailable capability changes the
tone of the session from enablement to sales.

## 1:00 - Adoption roadmap

Deck slide 33. Fill it in with real names and real dates, in the room.

**NOW, 0 to 30 days**
- Finish the five flagship reports
- Certify the shared semantic model per domain
- Stand up dev, test, prod workspaces
- Name an owner per domain

**NEXT, 30 to 90 days**
- Migrate the next tier of Tableau reports
- Roll out the measure and theme library
- Propose Fabric capacity for leadership approval
- Run the first quarterly review

**LATER, 90 days and beyond**
- Retire migrated Tableau workbooks
- Expand to adjacent I&O domains
- Adopt OneLake, Lakehouse, and Copilot once approved
- Scale the Community of Practice

**Test for the 30-day list: nothing on it may be blocked by a capability Schwab
does not have today.** If something is, it belongs in NEXT or LATER.

## 2:00 - Retrospective and Community of Practice

Deck slide 34.

### Retrospective
- **Start** - modeling once, certifying content, reviewing each other's work
- **Stop** - blending private extracts, rebuilding the same calcs
- **Continue** - sharing patterns, coaching across the domains

Prioritize the top improvements together and assign an owner to each.

### Community of Practice
- A champion per domain to mentor their team
- A shared workspace for templates, measures and standards
- Peer review before a report is certified
- A monthly forum to review new reports and patterns

### Proposed next steps
- Stand up a Champion Network across I&O
- Publish modeling and naming standards teams must follow
- Schedule follow-up coaching with Microsoft
- Hold quarterly reviews on adoption and health

**Before anyone leaves the room:** the CoP has a named lead and a recurring
meeting on the calendar. A community of practice that is agreed but not scheduled
does not exist.

## Closing

Deck slide 36. Three commitments:

1. **Pick your flagship** - each domain owns one report to migrate first.
2. **Practice, then scale** - apply the Power Query, modeling and DAX habits from
   this week. Adopt AI features as the organization approves and enables them.
3. **Agree on governance** - one owner, certified content, and Purview from day
   one, not day one hundred.
