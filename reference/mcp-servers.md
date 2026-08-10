# Power BI MCP servers (appendix - not in scope)

> **Not available at Schwab today.** MCP servers, GitHub Copilot in VS Code, and
> PBIP-based CI/CD are not part of this audience's tooling. The only AI in this
> workshop is M365 Copilot, used as a drafting tool with a copy-and-paste handoff
> - see [Lab 7](../labs/lab-07-copilot-reports/README.md) and
> [schwab-current-state.md](schwab-current-state.md). This page is background
> reading only.

Model Context Protocol, or MCP, gives an AI client a structured way to call a
server that exposes tools. In the Power BI scenario, the host is VS Code, the
client is GitHub Copilot, and the server is Power BI.

## Lab connection

- Lab: ../labs/lab-09-mcp-github-copilot/README.md
- PBIP reference: ../src/pbip/README.md
- Source: [Overview of the Power BI MCP servers](sources.md#mcp-and-agent-tooling)

## Mental model

| MCP part | Workshop example | What it does |
| --- | --- | --- |
| Host | VS Code | Runs the AI-assisted development environment. |
| Client | GitHub Copilot | Receives user intent and calls tools through MCP. |
| Server | Power BI MCP server | Exposes Power BI model, report, and query tools. |
| Resource | `sm_insurance` or report metadata | The object the tool reads or modifies. |
| Tool call | Execute Query or Get Semantic Model Schema | The structured action the client invokes. |

## Remote vs local Power BI MCP server

| Topic | Remote Power BI MCP server | Local Power BI MCP server |
| --- | --- | --- |
| Status | Public Preview | Public Preview |
| Runtime | Fabric-hosted | VS Code extension or Node 20+ with `npx` |
| Transport | Streamable HTTP | stdio |
| Install | No local server install | Local setup required |
| Auth | Microsoft Entra ID or Service Principal | Local developer auth context |
| Best fit | Query and inspect published Fabric artifacts | Build or modify models programmatically |
| Workshop use | Ask questions of `sm_insurance` and report metadata | Inspect or edit PBIP model files |

## Remote server tools

The remote server tools listed in Microsoft Learn include:

| Tool | What it does | Governance note |
| --- | --- | --- |
| Execute Query | Runs a DAX query against a semantic model. | Under user auth, RLS is enforced and Build permission is required. |
| Get Semantic Model Schema | Returns tables, columns, measures, and relationships. | Limit access to models users are allowed to inspect. |
| Get Report Metadata | Returns report structure and metadata. | Treat report metadata as workspace content. |

## Local server workflow

Use the local server when the goal is development work against model files.

1. Open the PBIP project in VS Code.
2. Connect Copilot to the local Power BI MCP server.
3. Ask Copilot to inspect tables, relationships, and measures.
4. Apply model changes through supported tooling.
5. Validate with DAX queries and source control diff.

In this workshop, local work maps to the PBIP assets documented in
../src/pbip/README.md.

## Remote server workflow

Use the remote server when the model already lives in Fabric.

1. Confirm the user has workspace access and Build permission.
2. Connect Copilot to the remote Power BI MCP endpoint.
3. Ask for the schema of `sm_insurance`.
4. Run validation DAX, for example Written Premium by month.
5. Ask for report metadata from `rpt_insurance_executive`.
6. Use findings to improve docs, tests, and migration decisions.

## Security guidance

| Control | Practical rule |
| --- | --- |
| Fabric RBAC | Grant the least workspace role needed for the task. |
| Build permission | Grant only to users who should query or build on a semantic model. |
| RLS | Test with user identities that match real access patterns. |
| Service principals | Use scoped identities and governed workspace access. |
| Auditability | Keep model changes in source control when using PBIP workflows. |
| Data sensitivity | Use sensitivity labels for regulated insurance data. |

## Insurance examples

| Question | MCP path |
| --- | --- |
| "What measures exist for claims?" | Get Semantic Model Schema on `sm_insurance`. |
| "Does Loss Ratio tie out by Product?" | Execute Query with Product and `[Loss Ratio]`. |
| "Which pages are in the executive report?" | Get Report Metadata on `rpt_insurance_executive`. |
| "Can an agent see only my book?" | Execute Query as a user with RLS applied. |

## Rayfin parallel

Power BI MCP helps agents inspect and query BI artifacts. Rayfin has an
application-building counterpart through the `@microsoft/rayfin-mcp` package.
Use Power BI MCP for semantic models and reports. Use Rayfin MCP tooling when
the agent is helping build Fabric-native apps.

See rayfin.md for the Rayfin app pattern used in the Day 3 insurance app lab.

## Presenter cautions

- MCP does not bypass Fabric permissions.
- DAX results are only as trustworthy as the model and filters.
- Public Preview features can change, so verify setup before delivery.
- Keep production write access separate from workshop demo access.

## Related workshop files

- Rayfin reference: rayfin.md
- Direct Lake model: direct-lake.md
- Governance: ../governance/workspace-governance.md
- Source list: sources.md
