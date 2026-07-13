# Lab 0 - Setup

**Duration:** ~40 min - **Deck:** "Kickoff + goals"

You will prepare the Fabric, Power BI, GitHub Copilot, and Rayfin toolchains used across the workshop. By the end, your team has the Contoso Insurance data landed in OneLake and the Rayfin prerequisite checked before Day 3.

## Schwab context
Schwab teams moving from Tableau to Power BI need a consistent Fabric estate before any report migration starts. This setup lab gives every team the same P&C insurance data, the same workspace pattern, and the same Rayfin app foundation for operational claims intake.

## What you'll build
- Three Fabric workspaces: Schwab-Analytics-Dev, Schwab-Analytics-Test, Schwab-Analytics-Prod
- A Lakehouse named lh_insurance in Schwab-Analytics-Dev
- Raw Contoso Insurance files under Files/raw with the contoso/ and ops/ folders preserved
- A verified Rayfin toolchain or a reviewed rayfin-app/ skeleton
- A local authoring setup for Power BI, VS Code, and GitHub Copilot

## Prerequisites
- Access to a Microsoft Fabric tenant with an available Fabric capacity
- Permission to create workspaces and Lakehouses in Fabric
- Power BI Desktop installed for Day 1 report authoring
- Python 3.10 or later available on your workstation
- Node 20+ available for the Rayfin prerequisite
- Git installed so you can work with the workshop repository
- Reference docs: [architecture](../../reference/architecture.md), [Rayfin](../../reference/rayfin.md), and [sources](../../reference/sources.md)

## Steps
### 1. Confirm Fabric capacity
- Open the Fabric portal and confirm you can see a capacity assigned to your tenant.
- If your administrator already created a workspace, verify it is backed by capacity.
- If you do not see capacity, capture the issue for the facilitator before continuing.
- Do not build the labs in My workspace.
- Keep capacity, workspace, and deployment pipeline names consistent with this guide.

### 2. Create the workshop workspaces
- Create Schwab-Analytics-Dev for hands-on build work.
- Create Schwab-Analytics-Test for deployment pipeline validation.
- Create Schwab-Analytics-Prod for the final shared model and report pattern.
- Assign contributors only to the people who need to build content.
- Leave viewer access for consumers until Lab 4, when you apply governance rules.
- Record the workspace URLs in your team notes.

### 3. Generate the Contoso Insurance files
- From the workshop root, run the synthetic data generator.

```powershell
python data\generate_data.py
```

- Confirm the generator created data\raw\contoso\policy_claims_extract.csv.
- Confirm it also created the star schema files dim_policy.csv, dim_customer.csv, dim_agent.csv, dim_coverage.csv, dim_date.csv, fact_premium.csv, and fact_claim.csv.
- Confirm data\raw\ops\claims_intake.csv exists.
- Do not rename columns, because later labs depend on the exact names.

### 4. Create lh_insurance and land raw files
- In Schwab-Analytics-Dev, create a Lakehouse named lh_insurance.
- Open Files and create a raw folder if it is not already present.
- Upload data/raw/** into Files/raw.
- Keep Files/raw/contoso/ for the analytics extracts.
- Keep Files/raw/ops/ for the operational claims feed.
- Spot-check policy_claims_extract.csv and claims_intake.csv in the Lakehouse file explorer.

### 5. Prepare the Rayfin prerequisite
- Rayfin is a Backend-as-a-Service that runs on Microsoft Fabric.
- Confirm Node 20+ is active.

```powershell
node --version
npm --version
```

- Run the scaffold command to verify the toolchain, or open the provided app if the facilitator has already prepared it.

```powershell
npm create @microsoft/rayfin@latest
```

- Sign in with your Microsoft account when the Rayfin CLI prompts you.
- Skim [rayfin-app/README.md](../../rayfin-app/README.md) and [reference/rayfin.md](../../reference/rayfin.md).
- Notice the entities Customer, Agent, Policy, and Claim.
- Notice that Policy uses @role row-level security for an agent's book of business.

### 6. Prepare Day 3 developer tools
- Install VS Code if it is not already installed.
- Sign in to GitHub Copilot in VS Code.
- Confirm you can open this workshop repository in VS Code.
- You will use these tools in Lab 9 for Power BI MCP and Lab 11 for Rayfin.
- Skim [reference/architecture.md](../../reference/architecture.md) to see how OneLake, Direct Lake, Power BI, MCP, and Rayfin fit together.

## You'll know it worked when
- Schwab-Analytics-Dev, Schwab-Analytics-Test, and Schwab-Analytics-Prod exist.
- lh_insurance exists in Schwab-Analytics-Dev.
- Files/raw/contoso/ contains the Contoso Insurance CSVs.
- Files/raw/ops/claims_intake.csv is uploaded.
- `python data\generate_data.py` completes without errors.
- `node --version` shows Node 20 or later.
- You can explain why Rayfin's Claim entity and ops/claims_intake.csv share the same operational shape.

## Next
[Lab 1 - Tableau to Power BI](../lab-01-tableau-to-powerbi/README.md)
