# Lab 0 - Setup, gateway, and your Copilot agents

**When:** Day 1, 3:30 session (`Domain alignment and Day 2 setup`) - **Deck slide 5**

**Scope:** In scope. Power BI Desktop, the sample data, a workspace, the on-premises
data gateway, and M365 Copilot.

This is the only lab that is not a numbered lab on the deck, because it is setup rather
than build. Do it before you leave on Day 1 so Day 2 starts at 10:30 with everyone
building instead of installing.

## What you'll have at the end
- Power BI Desktop installed and signed in
- The synthetic Banking / Capital Markets dataset generated locally
- A workspace you can publish to
- A working gateway connection, or a correctly-worded request for one
- Your domain group and flagship report chosen
- **Four M365 Copilot specialist agents ready to use in Labs 1 to 4**

## Prerequisites
- Power BI Desktop (latest)
- Python 3.10+ with pandas and numpy, to generate the sample data
- Access to a Power BI workspace where you can publish
- M365 Copilot - at minimum one licence per pair
- Reference: [gateway setup](../../reference/gateway-setup.md), [Copilot agents](../../reference/copilot-agents.md)

---

## Steps

### 1. Install and sign in to Power BI Desktop
- Install from the Microsoft Store if you can - it keeps itself updated.
- Sign in with your work account.
- Open **Transform data** once to confirm the Power Query editor launches. You will
  spend more time there on Day 2 than anywhere else.
- Flag any install or sign-in problem now. This is the one blocker that stops the whole
  workshop.

### 2. Generate the sample dataset

```powershell
python data\generate_data.py
```

This writes three shapes on purpose:

| Path | What it is | Used in |
| --- | --- | --- |
| `data\raw\sql\` | Conformed dimensions and one fact table per domain. Stands in for the SQL Server views you would reach through the gateway. | Labs 1, 2, 3 |
| `data\raw\tableau_extract\incident_report_extract.csv` | One wide, denormalized table - what a Tableau `.hyper` extract looks like today | Lab 4 |
| `data\raw\excel\capacity_YYYY_MM.csv` | A folder of monthly extracts, the "large Excel files" problem | Lab 4 |

- Confirm `data\raw\sql\` contains your fact table and the six `dim_*.csv` files.
- Open `dim_service.csv`. Two business units, **Banking** and **Capital Markets**, six
  services each. That split is the business lens for every report you build this week.
- The data is **synthetic**. It is shaped like I&O data for a financial services firm and
  contains nothing real - no customers, accounts, positions, orders or market data.

> **Bringing your own data?** Slide 16 says groups `use their own current-state source
> extracts and SQL data`. Do that where you can - the labs work either way. Keep the
> sample data generated as a fallback so a source access problem cannot stall your table.

### 3. Confirm your workspace
- Open the Power BI service and find a workspace where you can create content.
- **Do not build in My workspace.** Nothing there can be shared, endorsed, or handed over.
- Note the naming convention your platform team uses for dev / test / prod.
- Record the workspace URL in your group's notes.

### 4. Prove the gateway path end to end
Everything you build over the next two days refreshes through the on-premises data
gateway. A model that works beautifully in Desktop and then fails its first scheduled
refresh is the fastest way for a migration to lose credibility in week one. Do not wait
until Day 2 to find out.

**Answer these as a group** - read [gateway-setup.md](../../reference/gateway-setup.md)
sections 1 and 2 if you need to:

- Is there an existing gateway cluster, or does one need to be requested?
- Who are the gateway admins, and which service account do connections use?
- Which Entra security group grants "Can use" on connections?

If nobody in the room knows, that is itself a finding. Capture it as an action with an
owner before Day 3.

**Then create or request the connection.** If you are a gateway admin: service → gear →
**Manage connections and gateways** → **Connections** → **New**. Connection type SQL
Server, authentication Windows with the service account, privacy level
**Organizational**, and grant **Can use** to the security group rather than to
individuals. If you are not an admin, send the request using the template in
[gateway-setup.md section 9](../../reference/gateway-setup.md#9-what-to-ask-for-if-you-cannot-do-this-yourself)
- it contains everything the platform team needs, so it usually comes back in one round
trip instead of four.

**Then prove it.** Connect to one small table, publish it as a throwaway model named
`gw_smoke_test`, map it to the gateway connection under **Settings → Gateway and cloud
connections**, and click **Refresh now**. Green tick means you are unblocked for Day 2;
delete the throwaway. A failure means work the table in
[gateway-setup.md section 7](../../reference/gateway-setup.md#7-troubleshooting-in-the-order-to-check),
where the symptoms are listed in the order worth checking.

> **The mismatch that costs everyone an afternoon.** The server and database strings in
> the gateway connection must match what is in your `.pbix` character for character.
> `SQLPROD01` and `sqlprod01.contoso.com` are different data sources to the gateway even
> though they are the same server. Agree the exact string as a group now, and everyone
> type that one.

### 5. Pick your domain and flagship report
Deck slide 23 splits the room into five groups. Every group builds a different fact
table onto the **same** conformed dimensions, and every group can slice by Banking
versus Capital Markets.

| Group | Domain | Your fact table |
| --- | --- | --- |
| 1 | ITSM & Operational Reporting | `fact_incident` |
| 2 | Capacity & Forecasting | `fact_capacity` |
| 3 | Mainframe Analytics | `fact_mainframe` |
| 4 | Service Desk & Workforce | `fact_service_desk` |
| 5 | Asset & Workplace Services | `fact_asset` |

- Name the **one** Tableau report your group will migrate first.
- Write down the operational question it answers, in one sentence.
- Name the person who owns it today.

### 6. Meet M365 Copilot, then build your four agents
**Budget fifteen minutes. This is the step that pays for itself on Day 2.**

M365 Copilot is the only AI available for this work, and it **cannot see your semantic
model**. Everything good it produces depends on you describing the model first. Rather
than retyping that description in every prompt for two days, you set it up once, now.

**6a. Ask Copilot what it can actually do.** Open M365 Copilot and paste:

> *"I am a Tableau developer moving to Power BI Desktop. I have Microsoft 365 Copilot but
> I do not have Copilot inside Power BI, Copilot Studio, or Fabric. Given only what you
> can actually do in this chat, what are the highest-value ways you can help me build a
> semantic model, write DAX, design report pages, and write Power Query M? Be specific
> about what you cannot do, and tell me what context you need from me to be useful."*

Read the answer as a table. Two things should land, and they set up the whole workshop:
it will ask you for your **schema**, and it will admit it **cannot run DAX or see your
data**. That is why every lab from here ends in a verification step.

**6b. Ask it to turn that into reusable specialists:**

> *"Turn that into four specialist assistants I could reuse: one for semantic modeling,
> one for report design, one for DAX, one for Power Query M. For each, write the
> instructions I would paste at the start of a chat so it behaves that way for the whole
> conversation. Keep each one under 200 words."*

**6c. Compare with the ready-made briefs and set yours up.** Open
[reference/copilot-agents.md](../../reference/copilot-agents.md). The four briefs there
are the same idea as what Copilot just wrote, already loaded with this workshop's model.

Do this now, before you leave:

1. Copy the **model card** from
   [copilot-agents.md step 2](../../reference/copilot-agents.md#step-2-the-model-card)
   into a note you can paste from all week.
2. Fill in the last line: `MY GROUP'S FACT TABLE IS: <your fact>`. Without it, the agent
   hedges across all five domains.
3. Open **four browser tabs**, one per agent, and paste the brief plus the model card
   into each:

| Tab | Agent | You will use it in |
| --- | --- | --- |
| 1 | Model Architect | Lab 1 |
| 2 | Report Designer | Lab 2 |
| 3 | DAX Coach | Lab 3 |
| 4 | Query Engineer | Lab 4 |

4. Test tab 1 with a real question: *"Restate my fact table's grain in one sentence, then
   tell me which of my dimensions I should actually load and which would create an
   ambiguous filter path."* If the answer names your tables correctly, the setup worked.

> **Data handling, non-negotiable.** You paste **schema, code, column names and business
> definitions**. You never paste rows, credentials, connection strings, ticket contents,
> incident descriptions or user names. This is the condition on which the tool is used.

**6d. While you are there, draft your report requirements.** Use the Report Designer tab:

> *"Here are my notes from the report owner: [paste your notes]. Draft a one-page
> requirements summary: the operational question the report answers, the audience, the
> measures needed, the dimensions to slice by, and the open questions I should go back and
> ask."*

Edit it for accuracy and bring it to Lab 2.

### 7. Pair up for Day 2
Not everyone has an M365 Copilot licence. Labs 1 to 4 are designed for pairs: one person
drives Power BI Desktop, the other drives the Copilot tabs and hands code across. Swap
halfway through each lab.

- Agree your pairs now.
- Make sure every pair has at least one licence between them, and note who has one so
  tables can be rebalanced in the morning.

## You'll know it worked when
- Power BI Desktop is installed and signed in for everyone.
- `python data\generate_data.py` completed and `data\raw\sql\` is populated.
- Everyone can reach a shared workspace.
- A gateway test refresh **succeeded** - or a correctly worded request is in flight with a
  named owner and a due date.
- Each group has named its flagship report and the question it answers.
- **Four Copilot tabs are open, primed with the model card, and tab 1 answered a real
  question using your actual table names.**
- Copilot pairs are agreed, and every pair has a licence.

## Next
Day 2 opens with migration methodology, then
[Lab 1 - Build the semantic model](../lab-01-semantic-model/README.md).
