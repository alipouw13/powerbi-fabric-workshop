# Schwab environment today (what is available in the room)

This workshop is deliberately tailored to what the attending teams can actually
use today. It comes from the agenda review with the Schwab team: several of the
AI and Fabric capabilities in the original agenda are not enabled for this
audience yet, so those topics are demonstrated by the facilitator instead of
being hands-on, and the time is given back to practical Power BI work.

Read this before you run the workshop, and share the summary with attendees in
the kickoff so nobody spends a lab fighting a locked-down feature.

## Feature availability

| Capability | Status for this audience | How the workshop handles it |
| --- | --- | --- |
| Power BI Desktop and the Power BI Service | Available. | Hands-on for every attendee (Labs 1-4, 8). |
| SQL Server sources through the on-premises data gateway | Available and the standard pattern. | Covered as the primary connectivity path (Lab 5). |
| Import mode semantic models | Available and the standard pattern. | Primary storage mode in the modeling labs. |
| Copilot embedded in Power BI (report authoring, DAX, narratives) | Locked down for most attendees. | Facilitator demo only, with a Microsoft 365 Copilot alternative (Lab 7). |
| Microsoft 365 Copilot | A few attendees have it. | Shown as the practical alternative for summarizing, documenting, and drafting DAX (Lab 7). |
| Copilot Studio | Not available to most attendees. | Not used in any lab. |
| Fabric Data Agent | Not available to most attendees. | Facilitator demo and roadmap discussion only (Lab 10). |
| MCP servers with GitHub Copilot | Not available to most attendees. | Facilitator demo and roadmap discussion only (Lab 9). |
| OneLake, Lakehouse, and Direct Lake | Not fully approved yet. | Presented as the target state and demonstrated, not required for the hands-on path (Labs 5, 6). |

If any of these change before the workshop, tell the facilitator: the labs are
written so a demo section can become hands-on without rewriting the lab.

## Data architecture today

- The estate is **flat**. Reports read wide tables and large Excel files rather
  than a modeled star or a medallion structure.
- Most Power BI reports connect **directly to SQL databases**, using an import
  mode semantic model refreshed through the **on-premises data gateway**.
- A **snowflake pattern** is planned but not implemented.
- **Medallion (Bronze / Silver / Gold)** is not in use today.
- OneLake and Lakehouse options are **not fully approved**, so anything that
  depends on them is target state rather than current practice.

Because of this, the workshop introduces modeling and architecture best
practices **early** (star vs snowflake in Lab 2, medallion and layered
transformation in Lab 5) so teams adopt a preferred pattern now instead of
reworking a flat estate later.

## Audience

- **15 to 18 attendees**, a mix of Austin and Phoenix based staff, with a
  possibility of remote attendance for some Schwab Data team members.
- **Cross-functional**, not a single centralized reporting group. Many sit in the
  infrastructure team.
- **Most attendees have Tableau experience**, so draw the Tableau corollary every
  time a Power BI concept is introduced. See
  [tableau-to-powerbi.md](tableau-to-powerbi.md).
- A goal of the workshop is to seed a **community of practice** and a **center of
  excellence for data visualization**, so the governance and adoption sessions
  matter as much as the build labs.

## Facilitator guidance

- Set the current-state context in the kickoff: what Schwab allows today for
  native tool features, development practices, and gateway connections, so
  attendees can judge what is feasible now versus later.
- Keep the demo-only sections short and clearly labeled as future state, and
  point at the enablement conversation rather than promising dates.
- When a capability is not available, always give the attendee something they can
  do today: Microsoft 365 Copilot instead of embedded Copilot, gateway and import
  instead of Direct Lake, folder and workspace discipline instead of CI/CD.

## Related files

- Agenda and lab list: [../README.md](../README.md)
- Copilot options: [copilot-in-power-bi.md](copilot-in-power-bi.md)
- Target architecture: [architecture.md](architecture.md)
- Adoption plan: [../governance/adoption-roadmap.md](../governance/adoption-roadmap.md)
