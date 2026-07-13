# Power BI MCP servers

Power BI MCP servers are in Public Preview.
They let AI tools interact with Power BI and Fabric through the Model Context Protocol.
For this workshop, MCP is the bridge between GitHub Copilot in VS Code and governed Power BI artifacts.

Workshop links:

- [Lab 09: MCP and GitHub Copilot](../labs/lab-09-mcp-github-copilot/README.md)
- [PBIP project reference](../src/pbip/README.md)

## MCP roles in plain English

| MCP role | Workshop example | What it does |
| --- | --- | --- |
| Host | VS Code | Runs the AI experience and coordinates tool calls. |
| Client | GitHub Copilot | Sends requests from the user and receives tool results. |
| Server | Power BI MCP server | Exposes Power BI capabilities as tools. |

Microsoft overview: [What are the Power BI MCP servers?](https://learn.microsoft.com/en-us/power-bi/developer/mcp/mcp-servers-overview).

## Remote vs local Power BI MCP server

| Area | Remote Power BI MCP server | Local Power BI MCP server |
| --- | --- | --- |
| Hosting | Fabric-hosted | Runs in VS Code or with Node 20+ through `npx` |
| Install | No local server install | Local setup required |
| Transport | Streamable HTTP | stdio |
| Auth | Microsoft Entra ID user auth or service principal | Local user and configured Power BI project context |
| Best for | Query and insights on existing semantic models and reports | Building or modifying models programmatically |
| Typical user | Analyst, developer, or agent querying governed content | Developer working with PBIP or semantic model metadata |
| Existing model access | Yes | Yes, depending on configuration |
| Metadata read | Yes | Yes |
| Metadata write | Limited to exposed tools | Yes, for supported local modeling operations |
| Query support | DAX query execution | Query support for local development workflows |
| Destructive risk | Lower, mostly query and metadata | Higher, because tools can modify model artifacts |

## Remote server tools

Microsoft details the remote tools in [Remote Power BI MCP server tools](https://learn.microsoft.com/en-us/power-bi/developer/mcp/remote-mcp-server-tools).

| Tool | What it does | Governance note |
| --- | --- | --- |
| Execute Query | Executes DAX against a semantic model | Requires Build permission and enforces RLS under user authentication. |
| Get Semantic Model Schema | Returns tables, columns, measures, relationships, and AI metadata | Use this to ground Copilot responses in the approved model. |
| Get Report Metadata | Returns report pages, visuals, filters, and linked model details | Use this to understand how reports consume the model. |

Setup guidance: [Get started with the remote Power BI MCP server](https://learn.microsoft.com/en-us/power-bi/developer/mcp/remote-mcp-server-get-started).

## Local server use cases

Use the local server when the work is about changing model files, not only asking questions.
Examples:

- Inspect a PBIP semantic model project.
- Read and update tables, measures, relationships, and metadata.
- Generate model changes from a reviewed plan.
- Query the model during local development.
- Support repeatable database or model operations from an agent workflow.

For this workshop, local MCP belongs with the [PBIP project reference](../src/pbip/README.md).

## Security and governance

MCP does not remove the need for Power BI governance.
It makes governance more important because agents can act quickly.

| Control | Required practice |
| --- | --- |
| Fabric RBAC | Grant least privilege at workspace, item, and semantic model levels. |
| Build permission | Give Build only to users and agents that should query or build on a model. |
| RLS | Validate role behavior before allowing broad MCP query access. |
| Service principals | Use only when there is a clear automation requirement and approved lifecycle. |
| Destructive actions | Review local MCP plans before allowing metadata write or delete operations. |
| Auditability | Keep PBIP changes in source control and use pull requests for model updates. |
| Certification | Prefer certified semantic models for agent-assisted analysis. |

## Schwab workshop pattern

1. Build `lh_housing` and gold tables in Fabric.
2. Publish `Housing-Market-Insights (Direct Lake)`.
3. Use the remote MCP server to inspect schema and run governed DAX.
4. Use GitHub Copilot in VS Code to explain results or generate query drafts.
5. Use local MCP only for controlled PBIP modeling workflows.
6. Review all proposed model changes before committing.

## Example remote MCP prompts

- "List the measures in Housing-Market-Insights and identify which ones support YoY analysis."
- "Run a DAX query for Homes Sold by metro for the latest month."
- "Inspect the report metadata and tell me which pages use Inventory."
- "Explain whether the model has the fields needed for a supply pressure page."

## Microsoft Learn anchors

- [What are the Power BI MCP servers?](https://learn.microsoft.com/en-us/power-bi/developer/mcp/mcp-servers-overview)
- [Get started with the remote Power BI MCP server](https://learn.microsoft.com/en-us/power-bi/developer/mcp/remote-mcp-server-get-started)
- [Remote Power BI MCP server tools](https://learn.microsoft.com/en-us/power-bi/developer/mcp/remote-mcp-server-tools)
- [Build permission for shared semantic models](https://learn.microsoft.com/en-us/power-bi/connect-data/service-datasets-build-permissions)
- [Row-level security with Power BI](https://learn.microsoft.com/en-us/fabric/security/service-admin-row-level-security)
