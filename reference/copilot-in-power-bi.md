# Copilot options for insurance report authors

Copilot is most useful when the semantic model is already clean. In this
workshop, that means `sm_insurance` has a star schema, friendly names, governed
measures, and descriptions that explain insurance terms.

> **Availability for this audience:** Copilot embedded in Power BI is locked down
> for most attendees and Copilot Studio is not available, so the embedded
> experience is a facilitator demo. **Microsoft 365 Copilot** is the option some
> attendees have today, and the section below covers what it can do for a report
> author. See [schwab-environment-today.md](schwab-environment-today.md).

## Lab connection

- Lab: ../labs/lab-07-copilot-reports/README.md
- Semantic model: `sm_insurance`
- Report: `rpt_insurance_executive`
- Sources: [Copilot for Power BI overview](sources.md#copilot-for-power-bi)

## What Copilot can help authors do

| Author task | Copilot use | Insurance prompt example |
| --- | --- | --- |
| Create a report page | Generate a first layout from a model prompt. | "Create an executive page showing Written Premium, Loss Ratio, Claim Count, and Policies In Force." |
| Edit a page | Add or change visuals using natural language. | "Add a line chart for Written Premium by month and Product." |
| Summarize a model | Explain tables, fields, and measures. | "Summarize the insurance semantic model for a new analyst." |
| Add a narrative visual | Generate explanatory text from report context. | "Explain why Loss Ratio changed by region this quarter." |
| Write or refine DAX | Use Copilot in DAX query view for DAX queries and explanations. | "Show DAX to compare Written Premium to prior year by Product." |
| Improve descriptions | Draft measure descriptions for model maintainers. | "Describe Loss Ratio for report authors in one sentence." |

## Microsoft 365 Copilot as the alternative

Microsoft 365 Copilot does not see your semantic model, so you give it the
context. That still covers a lot of the author workload while embedded Copilot
is unavailable.

| Author task | How to do it with Microsoft 365 Copilot | Watch out for |
| --- | --- | --- |
| Understand a model | Paste the table, column, and measure list and ask for a plain-language summary. | It only knows what you paste; it cannot read `sm_insurance`. |
| Document measures | Ask for one-sentence descriptions of Loss Ratio, Earned Premium, and Written Premium YoY %. | Review every description for insurance accuracy before adding it to the model. |
| Draft DAX | Give the existing measure definitions as context and ask for a new measure, then test it in Power BI Desktop. | Generated DAX is a draft. Tie the numbers out before keeping it. |
| Translate Tableau logic | Paste a Tableau calculated field or LOD expression and ask for the DAX equivalent. | Confirm the filter context matches what the workbook actually did. |
| Plan a migration | Ask it to turn workbook notes into a page-by-page migration checklist. | Keep the checklist in the governed migration worksheet, not only in chat. |
| Write the comms | Draft release notes, training summaries, or a community-of-practice update. | Do not paste real Schwab data, credentials, or restricted content into any prompt. |

What Microsoft 365 Copilot cannot do: generate report pages on the canvas, add
visuals from a prompt, produce a narrative visual, or query the semantic model.
Those need Copilot in Power BI, which is why the demo is worth watching even
though it is not enabled yet.

## Prerequisites to confirm

Use current tenant guidance and the sources in sources.md. For workshop
planning, confirm:

- The workspace is on supported Fabric or Power BI capacity.
- Copilot is enabled by tenant and capacity settings.
- Authors have permission to the workspace and semantic model.
- Data is appropriate for Copilot use under company policy.
- The semantic model has understandable table, column, and measure names.
- The report author is working from the governed model, not a private copy.

## Make Copilot good

Copilot quality depends on model quality. Do this before the demo:

| Model preparation | Why it matters |
| --- | --- |
| Use a star schema | Copilot can reason over clear facts and dimensions. |
| Hide technical columns | Users should not see `policy_id`, `date_id`, or surrogate keys. |
| Use friendly names | "Written Premium" is better than `written_premium`. |
| Add measure descriptions | Copilot can use descriptions to explain intent. |
| Define measures once | Reuse reduces conflicting answers. |
| Set data categories | Dates, geography, and URLs behave better in visuals. |
| Remove ambiguous duplicates | Do not expose two fields with the same business meaning. |

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

## Prompt patterns

| Pattern | Example |
| --- | --- |
| Start with business question | "Which product has the highest Loss Ratio in the West region?" |
| Specify visual type | "Create a matrix with Product rows, Region columns, and Loss Ratio values." |
| Name the measures | "Use Written Premium, Earned Premium, and Claim Count." |
| Ask for explanation | "Explain the drivers of Loss Ratio for Auto in the Northeast." |
| Ask for validation help | "List DAX queries I can use to tie out Written Premium by month." |

## DAX Copilot examples

Use DAX Copilot to generate queries for exploration and validation, not as a
substitute for model owner review.

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

Ask Copilot to explain the query, then have the model owner approve the final
measure or validation query.

## Guardrails for workshop presenters

- Be explicit about which Copilot you are showing, embedded or Microsoft 365.
- Do not imply an enablement date for restricted features; route that to the
  enablement conversation instead.
- Do not demo Copilot against messy duplicate fields.
- Do not accept generated DAX without testing it.
- Do not use synthetic results as proof of production readiness.
- Do show that Copilot is better when the model is governed.
- Do connect Copilot authoring to endorsement and certification.

## Related workshop files

- Environment and availability: schwab-environment-today.md
- Model guidance: tableau-to-powerbi.md
- Direct Lake model: direct-lake.md
- Certification: ../governance/endorsement-certification.md
- Adoption plan: ../governance/adoption-roadmap.md
- Source list: sources.md
