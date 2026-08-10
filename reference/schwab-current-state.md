# Schwab current state, constraints, and what that means for this workshop

This page captures what the Schwab team told us in the pre-workshop agenda
review. Every lab is written against these facts. Read this before facilitating,
and cover it in the Day 1 kickoff so attendees know what is feasible **today**
versus what is on the roadmap.

> Treat this as a living document. Confirm each row with Anthony and Richard the
> week of the workshop, because tenant settings and approvals can change.

## Audience

| Item | What we know |
| --- | --- |
| Size | 15-18 attendees |
| Locations | Mix of Austin and Phoenix; some Schwab Data team members may join virtually |
| Background | Cross-functional. Most have **Tableau** experience. Not a centralized reporting group. |
| Power BI experience | Assume none |
| Goal | Form a **community of practice** and stand up a center of excellence for data visualization inside the infrastructure team |

Implication: draw explicit Tableau corollaries in every teaching block. Do not
assume attendees share a common toolchain, naming standard, or release process.

## Tooling and feature access

| Capability | Status today | How the workshop handles it |
| --- | --- | --- |
| Power BI Desktop, Power Query, DAX | Available | Every hands-on lab |
| Import and DirectQuery storage modes | Available - **the only two options** | [Lab 5](../labs/lab-05-ingestion-onelake/README.md), [Lab 6](../labs/lab-06-semantic-model-directlake/README.md) |
| On-premises data gateway | Available, centrally managed | [Lab 5](../labs/lab-05-ingestion-onelake/README.md) |
| Power BI Service: workspaces, RLS, endorsement, apps | Available | [Lab 4](../labs/lab-04-governance-foundations/README.md) |
| **M365 Copilot** | Available to some attendees | [Lab 7](../labs/lab-07-copilot-reports/README.md). Draft in Copilot, review, **copy and paste** into Power Query or the DAX editor. Pair licensed and unlicensed attendees. |
| Copilot **embedded in Power BI** | **Not available** | Not covered. Do not demo. |
| **Copilot Studio** | **Not available** | Not covered |
| **Fabric Data Agent** | **Not available** | Not covered. [Lab 10](../labs/lab-10-data-agent-showcase/README.md) is appendix reading only. |
| **Lakehouse / OneLake / Direct Lake** | **Not available** | Not covered hands-on. Appendix reading only. |
| **Dataflows Gen2, Data Factory pipelines, notebooks** | **Not available** | Not covered. All transformation is manual Power Query. |
| **MCP servers** | **Not available** | [Lab 9](../labs/lab-09-mcp-github-copilot/README.md) is appendix reading only |
| **GitHub Copilot / VS Code / PBIP / CI-CD** | Not part of current practice | Appendix reading only |
| **Rayfin** | **Not available** - requires Fabric | [Lab 11](../labs/lab-11-rayfin-insurance-app/README.md) is appendix reading only |

**The practical consequence:** every transformation in this workshop is done by
hand in **Power Query**, and every calculation is written in **DAX**. There is no
lake layer to push work into, and no AI inside Power BI to generate it. The only
AI assist available is M365 Copilot in a separate window, used as a drafting tool
with a copy-and-paste handoff.

Escalation path for enabling any of the above later: Hilary, Jeremy, Tim, and
Richard coordinate. Keep that out of the workshop content itself, and capture
requests in the Day 3 roadmap instead.

## Data architecture today

- The architecture is **very flat**. There is no medallion layering and no
  normalized dimensional structure in place.
- Large **Excel files** are a common source and a common pain point.
- Most Power BI reports connect **directly to SQL databases** through a semantic
  model in **Import** mode. **DirectQuery** is the only other option.
- The **on-premises data gateway** brokers those connections.
- A move to a **snowflake pattern** is planned but not implemented.
- OneLake and Lakehouse are **not available**, so there is no lake layer to push
  transformation work into.
- **All transformation happens in Power Query**, by hand, in the model.

Implication: the workshop must be useful to someone who will go back to a
gateway-brokered Import model on Monday. Power Query skill is therefore the
highest-leverage thing we can teach, alongside star-schema modeling. Introduce
the architecture vocabulary so the team avoids rework as it modernizes, but do
not teach a workflow that depends on tooling they cannot use.

## The three modeling patterns we teach, and when each applies

| Pattern | What it is | Where Schwab is | Where we teach it |
| --- | --- | --- | --- |
| **Flat / wide extract** | One wide table per workbook, logic baked into the extract | Current state | [Lab 1](../labs/lab-01-tableau-to-powerbi/README.md) - built deliberately, then critiqued |
| **Star schema** | Facts plus conformed dimensions, single-direction filters | The first move, and the highest-value one | [Lab 2](../labs/lab-02-data-modeling/README.md), shaped in Power Query in [Lab 5](../labs/lab-05-ingestion-onelake/README.md) |
| **Snowflake** | Dimensions normalized into related sub-dimensions | Stated plan | [Lab 2](../labs/lab-02-data-modeling/README.md), with the tradeoffs called out |

**Medallion (Bronze/Silver/Gold)** is mentioned once, as vocabulary, so the term
does not cause confusion later. It is **not taught or built**, because it requires
a lake layer Schwab does not have. Be explicit that medallion and star are not
competing choices: medallion describes how data is refined on the way in, star
describes how the model is shaped for analysis. A team can - and here, must -
adopt a star schema with nothing but Power Query and gateway-brokered SQL.

## Storage mode: the only two choices

| | Import | DirectQuery |
| --- | --- | --- |
| Where data lives | Cached in the model | Stays in the source |
| Query speed | Fast | Depends on the source |
| Data freshness | As of last refresh | Live |
| Refresh needed | Yes, scheduled | No |
| Power Query transformations | Full library available | Only folding steps allowed |
| Model size limits | Applies | Not applicable |
| Best for | Most reporting at Schwab today | Large or highly volatile sources, or where caching is not permitted |

This tradeoff is taught in [Lab 5](../labs/lab-05-ingestion-onelake/README.md) and
decided per model in [Lab 6](../labs/lab-06-semantic-model-directlake/README.md).

## Development practice constraints to acknowledge

- Gateway connections are centrally managed. Assume attendees cannot create or
  repoint a gateway data source themselves.
- Native tool features are enabled selectively at tenant and capacity level.
  Do not demo anything outside the **In scope** list above - a demo of something
  the team cannot use reads as a sales pitch, not enablement.
- There is no shared source-control or CI/CD practice for Power BI content, and
  PBIP is not in use. Standards and review discipline are the substitute, and
  they are set by the community of practice in [Lab 12](../labs/lab-12-showcase-next-steps/README.md).
- Report development is decentralized. Naming, certification, and workspace
  standards are part of what the community of practice needs to define.
- No AI tool may receive real Schwab data, credentials, or customer information.
  M365 Copilot is used for **code and prose only**, never source records.

## Facilitator labeling convention

Every lab uses one of two badges so attendees always know what applies to them:

- **In scope** - attendees do this hands-on with the tools they have today.
- **Appendix** - reference reading about a capability Schwab does not have.
  Not run, not demoed, not a prerequisite for anything.

If a question comes up about an appendix capability, answer it briefly and route
the request to the Day 3 roadmap. Do not detour into a live demo.

## Related

- [Tableau to Power BI](tableau-to-powerbi.md)
- [M365 Copilot for Power BI work](copilot-in-power-bi.md)
- [Migration approaches](migration-approaches.md)
- [Workspace governance](../governance/workspace-governance.md)
- [Adoption roadmap](../governance/adoption-roadmap.md)
- [Architecture](architecture.md) - appendix, future state
