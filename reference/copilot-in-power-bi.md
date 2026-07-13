# Copilot in Power BI for insurance report authors

Copilot is most useful when the semantic model is already clean. In this
workshop, that means `sm_insurance` has a star schema, friendly names, governed
measures, and descriptions that explain insurance terms.

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

- Do not demo Copilot against messy duplicate fields.
- Do not accept generated DAX without testing it.
- Do not use synthetic results as proof of production readiness.
- Do show that Copilot is better when the model is governed.
- Do connect Copilot authoring to endorsement and certification.

## Related workshop files

- Model guidance: tableau-to-powerbi.md
- Direct Lake model: direct-lake.md
- Certification: ../governance/endorsement-certification.md
- Adoption plan: ../governance/adoption-roadmap.md
- Source list: sources.md
