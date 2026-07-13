# Contoso Insurance synthetic data

This folder documents the synthetic P&C insurance data used by the Schwab Power
BI and Fabric workshop. The data is generated for training only and aligns to
the Fabric demo at https://github.com/alipouw13/fabric-test.

## Synthetic data notice

All names, policy numbers, claims, premiums, losses, regions, and operational
records are synthetic. Do not treat this data as Charles Schwab data, customer
data, production insurance data, or regulated data.

## Generation command

Generate the raw files with:

```powershell
python data\generate_data.py --months N
```

The default workshop shape is 24 months x 5 products x 5 regions.

## Business dimensions

| Domain | Values |
| --- | --- |
| Products | Auto, Home, Renters, Life, Umbrella |
| Regions | Northeast, Southeast, Midwest, Southwest, West |
| Channels | Independent Agent, Captive Agent, Direct, Online |

The generated portfolio loss ratio is approximately 61 percent. Use that as a
quick reasonableness check, not as an exact test assertion.

## Folder layout

| Path | Purpose |
| --- | --- |
| `data/raw/contoso/policy_claims_extract.csv` | Wide Tableau-style extract. |
| `data/raw/contoso/dim_policy.csv` | Policy dimension. |
| `data/raw/contoso/dim_customer.csv` | Customer dimension. |
| `data/raw/contoso/dim_agent.csv` | Agent dimension. |
| `data/raw/contoso/dim_coverage.csv` | Coverage dimension. |
| `data/raw/contoso/dim_date.csv` | Date dimension. |
| `data/raw/contoso/fact_premium.csv` | Premium and policy count fact. |
| `data/raw/contoso/fact_claim.csv` | Claim and loss fact. |
| `data/raw/ops/claims_intake.csv` | Operational claims intake feed. |

## Wide extract

`policy_claims_extract.csv` is the flat "Tableau extract" used for migration
discussion.

| File | Columns |
| --- | --- |
| `contoso/policy_claims_extract.csv` | `policy_number`, `product`, `region`, `channel`, `period_begin`, `year`, `month_name`, `agent_name`, `customer_segment`, `annual_premium`, `written_premium`, `earned_premium`, `policy_status`, `incurred_loss`, `claim_count`, `written_premium_yoy` |

Use this file to show why workbook-level calculations and extracts become hard
to govern as reporting grows.

## Star schema dimensions

| File | Grain | Columns |
| --- | --- | --- |
| `contoso/dim_customer.csv` | One row per customer | `customer_id`, `customer_name`, `segment`, `region`, `tenure_years` |
| `contoso/dim_agent.csv` | One row per agent | `agent_id`, `agent_name`, `agency`, `region`, `channel` |
| `contoso/dim_coverage.csv` | One row per coverage | `coverage_id`, `product`, `coverage` |
| `contoso/dim_date.csv` | One row per month or period | `date_id`, `period_begin`, `period_end`, `year`, `month`, `month_name`, `quarter` |
| `contoso/dim_policy.csv` | One row per policy | `policy_id`, `policy_number`, `product`, `customer_id`, `agent_id`, `region`, `channel`, `effective_date`, `annual_premium`, `status` |

## Star schema facts

| File | Grain | Columns |
| --- | --- | --- |
| `contoso/fact_premium.csv` | Policy and date period | `policy_id`, `date_id`, `product`, `region`, `channel`, `agent_id`, `written_premium`, `earned_premium`, `policies_written`, `policies_inforce` |
| `contoso/fact_claim.csv` | One row per claim | `claim_id`, `claim_number`, `policy_id`, `date_id`, `product`, `region`, `coverage_id`, `loss_type`, `severity`, `status`, `incurred_loss`, `paid_loss`, `fraud_flag` |

## Operational feed

| File | Grain | Columns |
| --- | --- | --- |
| `ops/claims_intake.csv` | One row per claim intake event | `claim_number`, `policy_number`, `product`, `region`, `coverage`, `loss_type`, `loss_date`, `reported_date`, `status`, `reserve_amount`, `paid_amount`, `severity`, `adjuster` |

Use this file for the Rayfin Claims Intake story and for discussing how
operational app data can complement analytics data in Fabric.

## Wide vs star explanation

| Pattern | What it represents | Tradeoff |
| --- | --- | --- |
| Wide extract | `policy_claims_extract.csv` combines policy, date, agent, premium, and claim fields. | Fast to start, but logic is duplicated and hard to certify. |
| Star schema | `dim_*` and `fact_*` files separate descriptive attributes from measurable events. | Requires modeling discipline, but supports reuse, RLS, and certified measures. |

The wide extract is useful for Tableau migration assessment. The star schema is
the target pattern for Power BI and Fabric.

## Fabric target alignment

| Fabric object | Data mapping |
| --- | --- |
| Lakehouse `lh_insurance` Bronze | `bronze_policy_claims`, `bronze_claims_intake` |
| Lakehouse `lh_insurance` Silver | `dim_*`, `fact_premium`, `fact_claim` |
| Lakehouse `lh_insurance` Gold | `gold_premium_summary`, `gold_loss_ratio`, `gold_agent_scorecard` |
| Warehouse `wh_insurance` | Curated relational serving layer. |
| Semantic model `sm_insurance` | Direct Lake model on Gold tables. |
| Report `rpt_insurance_executive` | Executive reporting experience. |

## Core measures supported

- Written Premium.
- Earned Premium.
- Policies In Force.
- Policies Written.
- Incurred Losses.
- Paid Losses.
- Claim Count.
- Loss Ratio, calculated as Incurred Losses divided by Earned Premium.
- Average Premium.
- Written Premium PY.
- Written Premium YoY %.

## Related workshop files

- Tableau translation: ../reference/tableau-to-powerbi.md
- Direct Lake reference: ../reference/direct-lake.md
- Rayfin reference: ../reference/rayfin.md
- Migration worksheet: ../governance/migration-assessment-worksheet.md
