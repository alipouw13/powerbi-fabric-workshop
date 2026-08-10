# M365 Copilot for Power BI work

> **Scope.** Copilot **embedded in Power BI** is not available to this audience,
> and neither are Copilot Studio or Fabric Data Agents. The only AI in this
> workshop is **M365 Copilot**, used in a separate window as a drafting tool with
> a copy-and-paste handoff into Power BI Desktop. See
> [schwab-current-state.md](schwab-current-state.md) and
> [Lab 7](../labs/lab-07-copilot-reports/README.md).

M365 Copilot cannot see your semantic model, your data, or your queries. Treat it
as a fast colleague who knows DAX and M well but has never seen your work. That
single fact drives everything below: **the quality of the output is the quality of
the context you supply.**

## What it can and cannot do

| Task | M365 Copilot | Notes |
| --- | --- | --- |
| Explain a DAX measure you paste in | Yes | The best entry point. Excellent for teaching filter context to Tableau users. |
| Convert a Tableau calculated field to DAX | Yes | Supply your table and column names or it will invent them |
| Draft a new DAX measure | Yes | Then test it at three grains before keeping it |
| Draft Power Query M | Yes | Then verify row counts, nulls, types, and folding |
| Debug an M or DAX error | Yes | Paste the code and the exact error text together |
| Draft measure and column descriptions | Yes | Review every one for insurance accuracy |
| Write model documentation | Yes | Feed it your table and measure list |
| See your model schema | **No** | You describe it in every prompt |
| Run DAX and return real numbers | **No** | |
| Generate a report page | **No** | |
| Read your data | **No** | And it must not - see below |

**Data handling.** Never paste real Schwab data, credentials, connection strings,
or customer information into Copilot. You paste **code, column names, and business
definitions** - never source records. Synthetic example rows are fine.

## The model context block

Write this once, save it where the team can reach it, and paste it at the top of
every prompt. It is the difference between usable output and invented table names.

```
I am writing DAX for a Power BI model in Import mode. The model is a star schema:

Facts:
  fact_premium(policy_id, agent_id, date_id, written_premium, earned_premium)
  fact_claim(policy_id, coverage_id, date_id, claim_id, incurred_loss, paid_loss)

Dimensions:
  dim_policy(policy_id, policy_number, product, customer_id)
  dim_customer(customer_id, customer_segment)
  dim_agent(agent_id, agent_name, region, channel)
  dim_coverage(coverage_id, coverage, loss_type)
  dim_date(date_id, period_begin, year, quarter, month, month_name)

dim_date is marked as the date table on period_begin.
Relationships are one-to-many, single direction, dimensions filtering facts.

Existing measures:
  Written Premium, Earned Premium, Policies In Force, Policies Written,
  Incurred Losses, Paid Losses, Claim Count, Loss Ratio, Average Premium,
  Written Premium PY, Written Premium YoY %

Always reuse existing measures rather than re-aggregating columns.
```

## The copy-paste loop

1. **Context** - paste the model context block.
2. **Ask** - state the business question and the output you want.
3. **Review** - read the generated code. If you cannot explain it, do not use it.
4. **Paste** - DAX into the measure editor or DAX query view; M into the Power
   Query **Advanced Editor**.
5. **Verify** - for DAX, check the total, by product, and by month. For M, check
   row count, nulls, data types, and whether query folding survived.
6. **Name it** - rename generated Power Query steps so a colleague can read them.

Step 5 is the one people skip, and it is the one that catches the errors.

## Lab connection

- Lab: ../labs/lab-07-copilot-reports/README.md
- Semantic model: `sm_insurance`
- Report: `rpt_insurance_executive`

## Why model quality still matters

Even without Copilot inside Power BI, everything below makes your work faster and
your model more trustworthy - and it is what you would paste into a prompt anyway.

## Prerequisites to confirm

Use current tenant guidance and the sources in sources.md. For workshop
planning, confirm:

- The workspace is on supported Fabric or Power BI capacity.
- Copilot is enabled by tenant and capacity settings.
- Authors have permission to the workspace and semantic model.
- Data is appropriate for Copilot use under company policy.
- The semantic model has understandable table, column, and measure names.
- The report author is working from the governed model, not a private copy.

## Make Copilot useful

Copilot output quality depends on how well you can describe your model. Every item
below makes the description easier to write - and makes the model better anyway.

| Model preparation | Why it matters |
| --- | --- |
| Use a star schema | A star is describable in a paragraph. A wide extract is not. |
| Hide technical columns | Users should not see `policy_id`, `date_id`, or surrogate keys. |
| Use friendly names | "Written Premium" is better than `written_premium`. |
| Add measure descriptions | They become the definitions you paste into prompts. |
| Define measures once | Reuse means Copilot has one right answer to reference. |
| Set data categories | Dates, geography, and URLs behave better in visuals. |
| Remove ambiguous duplicates | Two fields with the same meaning produce two wrong answers. |

## Core insurance measures

| Measure | Description for authors |
| --- | --- |
| Written Premium | Premium written during the selected period. |
| Earned Premium | Premium earned during the selected coverage period. |
| Policies In Force | Count of active policies in force for the selected context. |
| Policies Written | Count of policies written during the selected period. |
| Incurred Losses | Loss amount incurred for claims in the selected context. |
| Paid Losses | Claim payments made in the selected context. |
| Claim Count | Count of claims in the selected context. |
| Loss Ratio | Incurred Losses divided by Earned Premium. |
| Average Premium | Written Premium divided by Policies Written. |
| Written Premium YoY % | Year-over-year change in Written Premium. |

## Prompt patterns that work

| Pattern | Example |
| --- | --- |
| Lead with the model context block | Paste it first, every time |
| Explain before generate | "Explain what filter context is doing in this measure." |
| Name the measures to reuse | "Use the existing Written Premium and Earned Premium measures - do not re-aggregate the columns." |
| Give the Tableau original | "Here is the Tableau LOD calculation. Convert it and flag what will not translate cleanly." |
| Ask for one artifact | "Return a single DAX measure" or "Return one let expression I can paste into Advanced Editor." |
| Supply synthetic sample rows for M | Three fake rows tell Copilot more about shape than a paragraph does |
| Debug with the exact error | Paste the code and the full error text together |
| Ask for the validation | "Give me a DAX query I can run to tie this out by month." |

## Validating what comes back

**For DAX** - paste it in, then check the number at three grains:

```DAX
EVALUATE
SUMMARIZECOLUMNS(
    'dim_date'[year],
    'dim_date'[month_name],
    'dim_policy'[product],
    "Written Premium", [Written Premium],
    "Loss Ratio", [Loss Ratio]
)
```

A measure that is right at the total and wrong by month is the classic failure,
and it is invisible unless you look.

**For Power Query M** - after pasting into Advanced Editor, check:

- Row count before and after. Did it silently drop rows?
- New nulls. A type mismatch often produces nulls rather than an error.
- Explicit data types on every affected column. Generated M frequently omits them.
- **Query folding.** Right-click the last step and look for View Native Query.
  Generated M often breaks folding and turns a fast refresh into a slow one.
- Step names. Rename them so a colleague can read the query.

## Guardrails

- Do not paste real data, credentials, or customer information. Ever.
- Do not accept generated DAX without testing it at three grains.
- Do not accept generated M without checking rows, nulls, types, and folding.
- Do not commit code you cannot explain to a colleague.
- Route anything that enters `sm_insurance` through the model owner.
- If the generated M is longer than the click-path would have been, use the
  click-path.

## Related workshop files

- Current state and constraints: schwab-current-state.md
- Model guidance: tableau-to-powerbi.md
- Power Query snippets: ../src/powerquery/README.md
- Certification: ../governance/endorsement-certification.md
- Adoption plan: ../governance/adoption-roadmap.md
- Source list: sources.md
