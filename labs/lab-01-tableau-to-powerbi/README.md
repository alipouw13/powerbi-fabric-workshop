# Lab 1 - Tableau to Power BI

**Duration:** ~60 min - **Deck:** "Power BI and Tableau mental model"

You will build the first Contoso Insurance report page from the wide Tableau-style extract. The goal is not a perfect model yet, it is to map familiar Tableau actions to Power BI Desktop and the Power BI Service.

## Schwab context
Many Schwab analysts know how to start from a Tableau extract, drag fields to a sheet, and publish a workbook. In Power BI, the durable asset is the semantic model, while report pages are a presentation layer that can be reused across teams.

## What you'll build
- A Power BI Desktop file connected to contoso/policy_claims_extract.csv
- A first report page with Written Premium cards, product bars, and month trend visuals
- A working mental model for Tableau workbook concepts to Power BI concepts
- A list of fields that should move from a wide extract into a star schema in Lab 2

## Prerequisites
- Completed [Lab 0 - Setup](../lab-00-setup/README.md)
- Power BI Desktop installed and signed in
- data/raw/contoso/policy_claims_extract.csv generated locally
- Access to Schwab-Analytics-Dev in the Power BI Service
- Reference doc: [Tableau to Power BI](../../reference/tableau-to-powerbi.md)

## Steps
### 1. Open the wide extract in Power BI Desktop
- Start Power BI Desktop.
- Select Get data, then Text/CSV.
- Choose data\raw\contoso\policy_claims_extract.csv.
- Preview the file and confirm the columns include policy_number, product, region, channel, period_begin, written_premium, earned_premium, incurred_loss, claim_count, and written_premium_yoy.
- Choose Import for this first lab.
- Load the table without transforming it.

### 2. Compare the authoring surfaces
- In Tableau, you often start with a data source and build sheets.
- In Power BI Desktop, review the three main views: Report, Data, and Model.
- In the Power BI Service, note the distinction between a report and a dashboard.
- A Tableau dashboard usually maps to a Power BI report page.
- A Power BI dashboard is a separate Service feature made from pinned visuals.
- Keep that distinction clear when you talk to report owners.

### 3. Create quick measures for the first page
- Rename the imported table to policy_claims_extract.
- Create a measure named Written Premium.

```DAX
Written Premium = SUM(policy_claims_extract[written_premium])
```

- Create a measure named Earned Premium.

```DAX
Earned Premium = SUM(policy_claims_extract[earned_premium])
```

- Create a measure named Incurred Losses.

```DAX
Incurred Losses = SUM(policy_claims_extract[incurred_loss])
```

- Create a measure named Loss Ratio.

```DAX
Loss Ratio = DIVIDE([Incurred Losses], [Earned Premium])
```

### 4. Build the first insurance report page
- Rename Page 1 to Extract Overview.
- Add a card visual for Written Premium.
- Add a card visual for Loss Ratio.
- Add a clustered bar chart with product on the axis and Written Premium as the value.
- Add a line chart with period_begin on the x-axis and Written Premium as the value.
- Add a slicer for region.
- Add a slicer for channel.
- Format currency, percentages, titles, and labels so the page can be reviewed by an executive audience.

### 5. Contrast the Power BI model-based approach
- In Tableau, each workbook can carry its own extract logic.
- In Power BI, shared semantic models let many reports reuse the same governed definitions.
- The wide extract is fast for a first page, but it mixes policies, agents, customers, dates, premium, and claims in one table.
- Write down three fields that are dimensions: product, region, channel, agent_name, or customer_segment.
- Write down three fields that are facts: written_premium, earned_premium, incurred_loss, claim_count, or annual_premium.
- You will split these into a star schema in Lab 2.

### 6. Publish a draft to the Dev workspace
- Save the file with a local name such as contoso-insurance-extract.pbix.
- Publish to Schwab-Analytics-Dev.
- Open the report in the Power BI Service.
- Confirm the Extract Overview page renders.
- Do not certify or promote this model, because it is only a migration warm-up.

## You'll know it worked when
- policy_claims_extract.csv is loaded in Import mode.
- The Extract Overview page has a Written Premium card, Loss Ratio card, premium by product bar chart, and premium by month line chart.
- Region and channel slicers filter the page.
- You can explain that a Tableau dashboard maps most closely to a Power BI report page.
- You can explain why a shared semantic model is preferred for the production insurance story.

## Next
[Lab 2 - Data modeling](../lab-02-data-modeling/README.md)
