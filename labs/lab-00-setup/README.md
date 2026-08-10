# Lab 0 - Setup and kickoff

**Duration:** ~40 min - **Deck:** "Kickoff + goals" - **Day 1**

**Scope:** In scope.

You will agree on where Schwab is today, what this workshop will and will not
cover, and get Power BI Desktop and the sample data ready.

## Schwab context
This room is cross-functional, not a centralized reporting group, and most people
come from Tableau. So the first thing to build is not a workspace - it is shared
vocabulary and a shared understanding of the constraints. Schwab connects to SQL
through the on-premises data gateway using Import or DirectQuery, works with
large Excel files, and has a flat architecture with a snowflake pattern planned.
There is no Lakehouse, no Direct Lake, no Copilot inside Power BI, and no Data
Agent - so **every transformation in this workshop is done by hand in Power
Query**, and the only AI available is M365 Copilot in a separate window.

That is not a limitation to apologize for. It is the actual job, and doing it
well is what the next three days are about.

## What you'll build
- A shared picture of the current state and its constraints
- A working Power BI Desktop setup
- The synthetic Contoso Insurance dataset on your workstation
- A workspace you can publish to
- The start of a community-of-practice roster: who does what, and where

## Prerequisites
- **Power BI Desktop** installed
- Access to a Power BI workspace you can publish to
- Python 3.10 or later available on your workstation
- **M365 Copilot** for Lab 7 on Day 3, for at least one person per pair
- Reference docs: [current state](../../reference/schwab-current-state.md) and [sources](../../reference/sources.md)

**Not required:** Fabric capacity, Lakehouse access, Node.js, VS Code, or GitHub
Copilot. Nothing in this workshop uses them.

## Steps
### 1. Set the current state and the constraints
- Walk through [reference/schwab-current-state.md](../../reference/schwab-current-state.md) as a group.
- Confirm or correct each row. Anything that has changed since the planning call
  should be captured now, not discovered mid-lab.
- Be explicit about what is **out of scope**: Lakehouse, OneLake, Direct Lake,
  Dataflows Gen2, Copilot in Power BI, Copilot Studio, and Fabric Data Agents.
  None of these will be demoed, so nobody spends three days wanting something
  they cannot have.
- Be equally explicit about what **is** in scope: Power BI Desktop, Power Query,
  Import and DirectQuery, the gateway, the Power BI Service, and M365 Copilot.
- Agree on the two badges used throughout: **In scope** and **Appendix**.

### 2. Introduce yourselves and map the room
- Go around: name, team, what you build in Tableau today, and what you want to
  stop doing manually.
- Note who owns which reports and which data sources. This is the seed of the
  community of practice you charter in Lab 12.
- **Note who has M365 Copilot.** Form Day 3 pairs now so Lab 7 does not stall.
- Form tables of three or four, mixing Tableau depth across each table.

### 3. Confirm your Power BI workspace
- Open the Power BI Service and confirm you can see a workspace where you can
  create content.
- Do not build the labs in My workspace.
- The workshop uses the naming pattern Schwab-Analytics-Dev, Schwab-Analytics-Test,
  and Schwab-Analytics-Prod. Use whichever of these your facilitator provisioned,
  or map the pattern onto the workspaces you already have.
- Record the workspace URL in your team notes.

### 4. Generate the Contoso Insurance files
- From the workshop root, run the synthetic data generator.

```powershell
python data\generate_data.py
```

- Confirm the generator created data\raw\contoso\policy_claims_extract.csv.
- Confirm it also created the star schema files dim_policy.csv, dim_customer.csv, dim_agent.csv, dim_coverage.csv, dim_date.csv, fact_premium.csv, and fact_claim.csv.
- Do not rename columns, because later labs depend on the exact names.
- These files stand in for the SQL source you would reach through the gateway.
- The data is **synthetic and fictional**. No real Schwab data is used anywhere in
  this workshop, and none should be introduced - especially not in Lab 7.

### 5. Confirm Power BI Desktop
- Open Power BI Desktop and sign in.
- Confirm you can reach the workspace from step 3.
- Note the three views you will use constantly: Report, Data, and Model.
- Open **Transform data** to see the Power Query editor. You will spend more time
  here than anywhere else on Day 2.
- If Power BI Desktop is not installed or cannot sign in, flag it now. This is the
  one blocker that stops the whole workshop.

## You'll know it worked when
- The group can state what is in scope and what is not, without looking.
- Everyone has Power BI Desktop open and signed in.
- Everyone can reach a workspace they can publish to.
- `python data\generate_data.py` completes without errors.
- data\raw\contoso\ contains the expected CSVs.
- Tables are formed, and Day 3 Copilot pairs are assigned.

## Next
[Lab 1 - Tableau to Power BI](../lab-01-tableau-to-powerbi/README.md)
