# Lab 0 - Setup and the data gateway

**When:** Day 1, 3:30 session (`Domain alignment and Day 2 setup`) - **Deck slide 5**

**Scope:** In scope. Power BI Desktop, the sample data, a workspace, and the
on-premises data gateway.

This is the only lab that does not appear as a numbered lab on the deck, because
it is setup rather than build. Do it before you leave on Day 1 so Day 2 starts at
10:30 with everyone building instead of installing.

## Why the gateway matters here
Deck slide 7 puts the **on-premises data gateway** in the *Now* column, and slide
8 says `Import-mode refresh runs through the on-premises data gateway`. Everything
you build over the next two days refreshes through it. A model that works
beautifully in Power BI Desktop and then fails its first scheduled refresh is the
single most common way a migration loses credibility in week one.

## What you'll have at the end
- Power BI Desktop installed and signed in
- The synthetic I&O dataset generated locally
- A workspace you can publish to
- A working gateway connection, or a correctly-worded request for one
- Your domain breakout group and flagship report chosen
- Your Day 2 M365 Copilot pair agreed

## Prerequisites
- Power BI Desktop (latest)
- Python 3.10+ with pandas and numpy, to generate the sample data
- Access to a Power BI workspace where you can publish
- Reference: [gateway setup](../../reference/gateway-setup.md), [current state](../../reference/schwab-current-state.md)

---

## Steps

### 1. Install and sign in to Power BI Desktop
- Install from the Microsoft Store if you can - it keeps itself updated.
- Sign in with your Schwab account.
- Open **Transform data** once to confirm the Power Query editor launches. You
  will spend more time there on Day 2 than anywhere else.
- Flag any install or sign-in problem now. This is the one blocker that stops the
  whole workshop.

### 2. Generate the sample dataset

```powershell
python data\generate_data.py
```

This writes three shapes on purpose:

| Path | What it is | Used in |
| --- | --- | --- |
| `data\raw\sql\` | Conformed dimensions and a fact table per I&O domain. Stands in for the SQL Server views you would reach through the gateway. | Labs 1, 2, 3 |
| `data\raw\tableau_extract\incident_report_extract.csv` | One wide, denormalized table - what a Tableau `.hyper` extract looks like today | Lab 4 |
| `data\raw\excel\capacity_YYYY_MM.csv` | A folder of monthly extracts, the "large Excel files" problem | Lab 4 |

- Confirm `data\raw\sql\fact_incident.csv` and the six `dim_*.csv` files exist.
- The data is **synthetic**. It is shaped like I&O data but contains nothing real.

> **Bringing your own data?** Slide 16 says groups `use their own current-state
> source extracts and SQL data`. Do that where you can - the labs work either way.
> Keep the sample data generated as a fallback so a source access problem cannot
> stall your table.

### 3. Confirm your workspace
- Open the Power BI service and find a workspace where you can create content.
- **Do not build in My workspace.** Nothing there can be shared, endorsed, or
  handed over.
- Note the naming convention your platform team uses for dev / test / prod.
- Record the workspace URL in your group's notes.

### 4. Understand the gateway before you need it
Read [reference/gateway-setup.md](../../reference/gateway-setup.md) sections 1
and 2, then answer these as a group:

- Is there an existing I&O gateway cluster, or does one need to be requested?
- Who are the gateway admins?
- Which service account do connections authenticate with?
- Which Entra security group grants "Can use" on connections?
- Where is the gateway installed relative to the SQL sources?

If nobody in the room knows, that is itself a finding. Capture it as an action
with an owner before Day 3.

### 5. Create or request the data source
**If you are a gateway admin**, create the connection now:
- Power BI service → gear → **Manage connections and gateways** → **Connections**
  → **New**.
- Connection type SQL Server, server and database strings **exactly** as you type
  them in Power BI Desktop, authentication Windows with the service account,
  privacy level **Organizational**.
- Grant **Can use** to the security group, not to individuals.
- Test the connection before moving on.

**If you are not**, send the request. Use the template in
[gateway-setup.md section 9](../../reference/gateway-setup.md#9-what-to-ask-for-if-you-cannot-do-this-yourself)
- it contains everything the platform team needs, so it usually comes back in one
round trip instead of four.

> **The mismatch that costs everyone an afternoon.** The server and database
> strings in the gateway connection must match what is in your `.pbix`
> character for character. `SQLPROD01` and `sqlprod01.schwab.com` are different
> data sources to the gateway even though they are the same server. Agree the
> exact string as a group now, and everyone type that one.

### 6. Prove the refresh path end to end
Do not wait until Day 2 to discover the gateway does not work.

- In Power BI Desktop, connect to one small table from the real source.
- Publish it to your workspace as a throwaway model named `gw_smoke_test`.
- Semantic model → **Settings** → **Gateway and cloud connections** → map the
  data source to the gateway connection. Look for the green tick.
- Click **Refresh now**.
- If it succeeds, you are unblocked for Day 2. Delete the throwaway model.
- If it fails, work the table in
  [gateway-setup.md section 7](../../reference/gateway-setup.md#7-troubleshooting-in-the-order-to-check)
  - the symptoms are listed in the order worth checking.

### 7. Pick your domain and flagship report
Deck slide 23 splits the room into five groups. Choose yours:

| Group | Domain | Primary fact table |
| --- | --- | --- |
| 1 | ITSM & Operational Reporting | `fact_incident` |
| 2 | Capacity & Forecasting | `fact_capacity` |
| 3 | Mainframe Analytics | `fact_mainframe` |
| 4 | Service Desk & Workforce | `fact_service_desk` |
| 5 | Asset & Workplace Services | `fact_asset` |

- Name the **one** Tableau report your group will migrate first.
- Write down the operational question it answers, in one sentence.
- Name the person who owns it today.

> **M365 Copilot assist.** Before you leave, draft the requirements for your
> flagship report. This is exactly the use deck slide 24 describes:
>
> *"I am migrating a Tableau report to Power BI. Here are my notes from the
> stakeholder conversation: [paste notes]. Draft a one-page requirements summary
> with: the operational question the report answers, the audience, the measures
> needed, the dimensions to slice by, and any open questions I should go back
> and ask."*
>
> Edit it for accuracy, then bring it to Lab 2.

### 8. Pair up for Day 2
Not everyone has an M365 Copilot licence. Labs 3 and 4 are designed for pairs:
one person drives Power BI Desktop, the other drives Copilot and hands code
across.

- Agree your pairs now.
- Make sure every pair has at least one licence between them.
- Note who has one, so tables can be rebalanced in the morning.

## You'll know it worked when
- Power BI Desktop is installed and signed in for everyone.
- `python data\generate_data.py` completed and `data\raw\sql\` is populated.
- Everyone can reach a shared workspace.
- A gateway connection exists and a test refresh **succeeded** - or a correctly
  worded request is in flight with a named owner and a due date.
- Each group has named its flagship report and the question it answers.
- Copilot pairs are agreed, and every pair has a licence.

## Next
Day 2 opens with migration methodology, then
[Lab 1 - Build the semantic model](../lab-01-semantic-model/README.md).
