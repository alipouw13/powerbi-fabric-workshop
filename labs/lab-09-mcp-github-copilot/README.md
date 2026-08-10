# Lab 9 - MCP and GitHub Copilot (appendix)

**Deck:** "MCP + GitHub Copilot" - **Appendix reading, not run**

> **Not in scope for this workshop.** MCP servers, GitHub Copilot in VS Code, and
> PBIP-based CI/CD are not available to this audience. This page is kept as
> reference so the team can see what a code-first Power BI practice looks like and
> make an informed request later. It is **not demoed and not a prerequisite for
> anything**. See [reference/schwab-current-state.md](../../reference/schwab-current-state.md).
>
> **The part you can act on today:** the underlying problem this addresses is that
> Power BI development at Schwab is decentralized with no shared review or release
> practice. You do not need MCP to fix that - you need the standards the community
> of practice sets in [Lab 12](../lab-12-showcase-next-steps/README.md).

GitHub Copilot in VS Code can connect to Power BI MCP servers to inspect models,
run DAX, and modify artifacts, with PBIP and Fabric CI/CD providing the source
control and deployment loop.

## What it would look like
- A VS Code MCP configuration for the Power BI remote MCP server
- A schema inspection of sm_insurance
- A DAX query against sm_insurance using src/sql/sample_dax_queries.dax
- A local MCP workflow for build or model modification tasks
- A PBIP source-control checkpoint tied to src/pbip/README.md and src/cicd/

## Reference docs
[MCP servers](../../reference/mcp-servers.md), [PBIP](../../src/pbip/README.md),
[current state](../../reference/schwab-current-state.md)

## Steps
### 1. Review the MCP architecture
- Host: VS Code.
- Client: GitHub Copilot.
- Server: Power BI.
- The Power BI remote MCP server is Fabric-hosted and requires no local install.
- The remote server uses Streamable HTTP and Entra ID or Service Principal authentication.
- The remote tools include Execute Query, Get Semantic Model Schema, and Get Report Metadata.
- Execute Query runs DAX, enforces RLS, and requires Build permission on the semantic model.
- The local MCP server uses Node 20+, npx, and stdio for build and modification workflows.

### 2. Add the remote MCP server to VS Code
- Open this workshop repository in VS Code.
- Open or create your user-level mcp.json according to your VS Code and GitHub Copilot setup.
- Add the Power BI remote MCP server using the URL and authentication pattern from [reference/mcp-servers.md](../../reference/mcp-servers.md).
- Do not paste secrets into the repository.
- Keep tenant-specific values in user settings or approved secret storage.
- Restart the MCP session if VS Code prompts you.
- Confirm GitHub Copilot shows the Power BI tools.

### 3. Inspect sm_insurance schema
- In GitHub Copilot chat, ask for the schema of sm_insurance in Schwab-Analytics-Dev.
- Use the Get Semantic Model Schema tool.
- Confirm the model includes fact_premium, fact_claim, dim_customer, dim_agent, dim_policy, dim_coverage, and dim_date.
- Confirm the core measures appear with expected names.
- Ask Copilot to summarize the model in insurance business terms.
- Check the answer against the fields and descriptions you added in Lab 6.

### 4. Execute DAX through MCP
- Open [src/sql/sample_dax_queries.dax](../../src/sql/sample_dax_queries.dax).
- Copy a query that returns Written Premium, Earned Premium, or Loss Ratio by product or region.
- Ask GitHub Copilot to run the query against sm_insurance with the Execute Query tool.
- Confirm the result respects your permissions and RLS.
- If a query fails, check Build permission, workspace access, model name, and DAX syntax.
- Compare the result to the Lab 6 validation output.

### 5. Review report metadata
- Ask Copilot to get metadata for rpt_insurance_executive.
- Confirm report pages such as Insurance Executive Overview, Premium Production, Loss Ratio Trend, or Agent Scorecard are visible if they exist.
- Ask Copilot to identify which semantic model the report uses.
- Confirm it points to sm_insurance.
- Use this step to discuss inventory, documentation, and migration assessment at scale.

### 6. Try the local MCP workflow
- Configure the local Power BI MCP server according to [reference/mcp-servers.md](../../reference/mcp-servers.md).
- Confirm Node 20+ is active.
- Use npx only as documented by the server instructions.
- Ask Copilot to inspect or modify a local PBIP artifact.
- Use [src/pbip/README.md](../../src/pbip/README.md) as the PBIP contract.
- Keep generated changes small and reviewable.
- Do not let local edits bypass semantic model governance.

### 7. Commit and deploy the governed pattern
- Review src/cicd/parameter.yml.
- Review src/cicd/.github/workflows/fabric-cicd.yml.
- Commit PBIP or metadata changes only after validation.
- Use a focused commit message.
- Let the Fabric CI/CD workflow deploy to the right workspace when configured.
- Keep environment-specific values in parameter.yml or approved secret storage.
- Confirm Dev, Test, and Prod remain aligned with Lab 4 governance.

### 8. Connect the Rayfin MCP parallel
- Rayfin ships an MCP package named @microsoft/rayfin-mcp.
- Power BI MCP helps Copilot inspect and work with semantic models and reports.
- Rayfin MCP is the app-building parallel for Fabric-backed operational apps.
- Both patterns put Copilot in a tool-enabled workflow with least-privilege access.
- You will use the Rayfin app skeleton directly in Lab 11.

## You'll know it worked when
- GitHub Copilot can access the Power BI remote MCP tools in VS Code.
- Get Semantic Model Schema returns sm_insurance tables and measures.
- Execute Query runs a DAX query from src/sql/sample_dax_queries.dax and enforces RLS.
- You understand when to use the remote MCP server and when to use the local MCP server.
- You can explain how @microsoft/rayfin-mcp is analogous for Rayfin app development.

## Back to the workshop
[Lab 12 - Community of practice and next steps](../lab-12-showcase-next-steps/README.md)
