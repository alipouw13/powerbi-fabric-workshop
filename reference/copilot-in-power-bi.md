# Copilot in Power BI for report authors

Copilot in Power BI helps authors move faster when the semantic model is clear, governed, and described.
For Schwab Tableau authors, think of Copilot as an assistant that works best after the data model is organized.

Workshop lab:

- [Lab 07: Copilot reports](../labs/lab-07-copilot-reports/README.md)

## What Copilot can help authors do

Microsoft documents Copilot capabilities in [Copilot for Power BI overview](https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-introduction).

| Author task | Copilot capability | Workshop example |
| --- | --- | --- |
| Create report pages | Generate report pages from a prompt or selected model fields | "Create an executive housing market overview by metro and property type." |
| Edit report pages | Adjust report layout and visuals through prompts | "Add a line chart for median sale price trend by month." |
| Summarize the semantic model | Describe model contents and likely analytical paths | Summarize `Housing-Market-Insights` tables and measures. |
| Create a narrative visual | Add text summaries that update with report context | Explain which metros have the highest inventory pressure. |
| Write DAX queries | Generate or explain DAX queries in DAX query view | Ask for `Homes Sold` by metro and month. |
| Generate measure descriptions | Draft descriptions for model measures | Add business-friendly descriptions for `Homes Sold YoY %`. |

## Authoring surfaces

| Surface | Use it for | Notes |
| --- | --- | --- |
| Copilot pane | Report creation, page edits, summaries, and conversational authoring | Available in supported Power BI experiences when requirements are met. |
| Inline Copilot | Focused assistance inside modeling or report tasks | Useful when generating measure descriptions or DAX. |
| DAX query view | Natural language to DAX query, DAX explanation, and query edits | See [Write DAX queries with Copilot](https://learn.microsoft.com/en-us/dax/dax-copilot). |
| Narrative visual | Context-aware written summary on a report page | See [Create a narrative visual with Copilot](https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-create-narrative). |

## Prerequisites

Copilot availability depends on tenant and capacity settings.
Confirm these before the lab:

1. The workspace is backed by supported Fabric capacity or Power BI Premium capacity.
2. Tenant settings allow users to use Copilot and Azure OpenAI-powered features.
3. Authors have the needed workspace or model permissions.
4. The report or semantic model is in a supported region.
5. The semantic model has clear names, descriptions, and relationships.

Admin settings are documented in [Copilot and Agent admin settings](https://learn.microsoft.com/en-us/fabric/admin/service-admin-portal-copilot).

## Make Copilot good

Copilot quality is model quality multiplied by metadata quality.
Treat the model like a product, not a hidden extract.

| Design choice | Why it helps Copilot |
| --- | --- |
| Star schema | Copilot can infer filter paths and aggregation grain more reliably. |
| Friendly table names | `Region` is clearer than `dim_region` for business prompts if display names are adjusted. |
| Friendly measure names | `Avg Median Sale Price` is easier to prompt than a cryptic workbook calculation. |
| Measure descriptions | Copilot can explain and use calculations with more business context. |
| Hidden technical columns | Authors and Copilot see fewer irrelevant fields. |
| Synonyms and descriptions | Business terms like "metro" and "market" map to the right fields. |
| Certified model | Authors know which model to use and avoid duplicate versions. |

Microsoft guidance: [Prepare your data for AI to improve Copilot results](https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-prepare-data-ai).

## Workshop model setup checklist

Before running Copilot prompts against `Housing-Market-Insights`:

- Confirm relationships from `fact_home_sales` to `dim_date`, `dim_region`, and `dim_property_type`.
- Confirm measures exist for `Homes Sold`, `New Listings`, `Inventory`, and `Homes Sold YoY %`.
- Add descriptions to core measures.
- Hide keys and technical staging fields.
- Use display folders for Market, Supply, Pricing, and Time Intelligence.
- Apply a sensitivity label if the model is used outside the workshop.
- Publish to `Schwab-Analytics-Dev` first, then promote through Test and Prod.

## Example prompts

Use prompts that name the grain and the decision.

| Prompt | Why it works |
| --- | --- |
| "Create a page showing inventory, months of supply, and median days on market by metro for the latest month." | It names metrics, dimensions, and time scope. |
| "Summarize which metros have the fastest year-over-year growth in homes sold." | It points Copilot to the YoY measure and business question. |
| "Write a DAX query that returns Homes Sold and Homes Sold YoY % by month_name for Seattle WA." | It names measures, dimension, and filter. |
| "Add a narrative summary for the selected region and property type." | It connects narrative output to report filters. |

## Guardrails

Copilot accelerates authoring, but authors still own correctness.
Review generated visuals, DAX, and summaries.
Validate totals against known source values.
Do not certify a report because Copilot created it.
Certify it because owners, measures, lineage, and support processes are clear.

## Microsoft Learn anchors

- [Copilot for Power BI overview](https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-introduction)
- [Create and edit Power BI reports with Copilot](https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-create-reports)
- [Write DAX queries with Copilot](https://learn.microsoft.com/en-us/dax/dax-copilot)
- [Use Copilot to create measure descriptions](https://learn.microsoft.com/en-us/power-bi/transform-model/desktop-measure-copilot-descriptions)
- [Prepare your data for AI to improve Copilot results](https://learn.microsoft.com/en-us/power-bi/create-reports/copilot-prepare-data-ai)
