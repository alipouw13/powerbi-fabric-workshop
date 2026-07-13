# Lab 9 - MCP + GitHub Copilot

**Duration:** ~75 min - **Deck:** "Developer workflow: GitHub Copilot + MCP"

You will connect GitHub Copilot in VS Code to Power BI MCP servers and use the model from prior labs as the working target. You will query an existing semantic model with the remote server, then discuss how the local server can build and modify models programmatically.

## Schwab context
Analysts and BI developers increasingly work in both visual tools and code. For Schwab teams, MCP creates a governed bridge where GitHub Copilot can inspect semantic models, run approved queries, and help manage PBIP assets without bypassing Fabric RBAC.

In MCP terms, the host is VS Code, the client is GitHub Copilot, and the server is Power BI. Use least-privilege Fabric RBAC for every connection.

## What you'll build
- A VS Code MCP configuration file named mcp.json.
- A GitHub Copilot chat session that calls Get Semantic Model Schema.
- A DAX query run through Execute Query against Housing-Market-Insights.
- A review of Get Report Metadata output.
- A local MCP workflow discussion for building or modifying semantic models.
- A PBIP and CI/CD handoff using [src/pbip/README.md](../../src/pbip/README.md) and [src/cicd](../../src/cicd/).

## Prerequisites
- Completed [Lab 8 - Migrate a Workbook](../lab-08-migrate-a-workbook/README.md).
- VS Code with the GitHub Copilot extension installed and signed in.
- Build permission on Housing-Market-Insights.
- Power BI MCP server details from [reference/mcp-servers.md](../../reference/mcp-servers.md).
- Node.js 20+ available if you test the local MCP server.
- Sample DAX in [src/sql/sample_dax_queries.dax](../../src/sql/sample_dax_queries.dax).

## Steps
### 1. Open the workshop repo in VS Code
Open the workshop repository folder in VS Code.

Confirm GitHub Copilot Chat is available. Keep the Fabric portal open so you can compare MCP responses to the actual semantic model.

### 2. Configure the remote MCP server
Create or update an mcp.json file using the facilitator-provided remote Power BI MCP server endpoint.

The remote MCP server is Fabric-hosted, requires no local install, uses Streamable HTTP, and supports Microsoft Entra ID OAuth or Service Principal auth. Do not paste secrets into source-controlled files.

### 3. Confirm the remote server tools
In GitHub Copilot Chat, ask which Power BI MCP tools are available.

The remote server is for querying data and generating insights from existing models. It exposes Execute Query, Get Semantic Model Schema, and Get Report Metadata.

### 4. Get the semantic model schema
Ask Copilot to use Get Semantic Model Schema for Housing-Market-Insights.

Review tables, columns, measures, relationships, and AI metadata. Confirm that the core measures from Lab 6 appear with the exact names.

### 5. Execute a governed DAX query
Open [src/sql/sample_dax_queries.dax](../../src/sql/sample_dax_queries.dax) and choose a query.

Ask Copilot to run Execute Query against Housing-Market-Insights. Under user auth, Row-Level Security is enforced, and the user needs Build permission on the semantic model.

### 6. Inspect report metadata
Ask Copilot to use Get Report Metadata for the report created in Lab 7 or Lab 8.

Review pages, visuals, fields, and model references. Use this to understand how report structure can be reviewed without manually clicking through every page.

### 7. Configure the local MCP server
Review the local server setup in [reference/mcp-servers.md](../../reference/mcp-servers.md).

The local MCP server runs locally in VS Code or through Node.js 20+ with npx and uses stdio transport. It is intended for building and modifying semantic models programmatically, including metadata read and write, query, and database operations.

### 8. Save the model as PBIP
Review [src/pbip/README.md](../../src/pbip/README.md).

Save or export the model and report as a Power BI Project where possible. PBIP makes semantic model metadata reviewable in Git and easier to automate in a developer workflow.

### 9. Commit and prepare CI/CD
Review [src/cicd/parameter.yml](../../src/cicd/parameter.yml) and [src/cicd/.github/workflows/fabric-cicd.yml](../../src/cicd/.github/workflows/fabric-cicd.yml).

Use Git to commit only approved PBIP and configuration changes. The CI/CD pattern promotes content through Schwab-Analytics-Dev, Schwab-Analytics-Test, and Schwab-Analytics-Prod.

### 10. Apply least privilege
Review who has access to the model, the workspace, and the MCP connection.

Use least-privilege Fabric RBAC. Give Build permission only to users who should query the semantic model through tools such as Execute Query.

## You'll know it worked when
- VS Code can connect GitHub Copilot to the Power BI remote MCP server.
- Get Semantic Model Schema returns tables, measures, relationships, and AI metadata for Housing-Market-Insights.
- Execute Query runs a DAX query from sample_dax_queries.dax.
- You can explain the difference between the remote MCP server and local MCP server.
- You know where PBIP and CI/CD assets live in src/pbip and src/cicd.

## Next
Previous: [Lab 8 - Migrate a Workbook](../lab-08-migrate-a-workbook/README.md). Continue to [Lab 10 - Data Agent Showcase](../lab-10-data-agent-showcase/README.md).
