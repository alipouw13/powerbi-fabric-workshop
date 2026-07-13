# Workshop data

The workshop data is synthetic.
It is generated for a 3-day Microsoft Power BI and Fabric workshop for Charles Schwab.
It is safe for hands-on labs because it does not contain client, employee, or proprietary Schwab data.

## Generate the data

From the workshop root:

```powershell
python data\generate_data.py --months 24
```

You can change the month count:

```powershell
python data\generate_data.py --months N
```

The default contract is 24 months x 12 metros x 4 property types.

## Metros

The generated metros are:

Seattle WA, Denver CO, Austin TX, Phoenix AZ, Chicago IL, Atlanta GA, Boston MA, Nashville TN, Charlotte NC, Miami FL, Portland OR, and Dallas TX.

## Property types

The generated property types are:

All Residential, Single Family Residential, Condo/Co-op, and Townhouse.

## Files under raw

| File | Purpose |
| --- | --- |
| `raw/redfin/market_tracker.csv` | Wide "Tableau extract" shape for workbook migration exercises. |
| `raw/redfin/fact_home_sales.csv` | Fact table for modeled Power BI and Fabric exercises. |
| `raw/redfin/dim_region.csv` | Region dimension. |
| `raw/redfin/dim_date.csv` | Date dimension. |
| `raw/redfin/dim_property_type.csv` | Property type dimension. |
| `raw/mls/listings.csv` | Synthetic listing-level MLS-style data. |

## `market_tracker.csv` columns

This file is the flat extract shape Tableau authors will recognize.

- `region`
- `state`
- `region_type`
- `period_begin`
- `period_end`
- `year`
- `month_name`
- `property_type`
- `median_sale_price`
- `homes_sold`
- `new_listings`
- `inventory`
- `months_of_supply`
- `median_days_on_market`
- `median_ppsf`
- `avg_sale_to_list`
- `sold_above_list_share`
- `median_sale_price_yoy`
- `homes_sold_yoy`

## Star schema files

Use these files for the modeled Power BI path.

| File | Columns |
| --- | --- |
| `raw/redfin/fact_home_sales.csv` | `region_id`, `date_id`, `property_type_id`, `median_sale_price`, `homes_sold`, `new_listings`, `inventory`, `months_of_supply`, `median_days_on_market`, `median_ppsf`, `avg_sale_to_list`, `sold_above_list_share` |
| `raw/redfin/dim_region.csv` | `region_id`, `region`, `region_type`, `state` |
| `raw/redfin/dim_date.csv` | `date_id`, `period_begin`, `period_end`, `year`, `month`, `month_name`, `quarter` |
| `raw/redfin/dim_property_type.csv` | `property_type_id`, `property_type` |

## `listings.csv` columns

The MLS-style file has listing-level rows:

- `listing_id`
- `region`
- `state`
- `property_type`
- `list_date`
- `list_price`
- `status`
- `sale_price`
- `beds`
- `baths`
- `sqft`
- `list_agent`
- `office`

## Wide vs star explanation

`market_tracker.csv` is intentionally wide.
It behaves like a Tableau extract where most attributes and metrics are in one file.
That makes it easy to migrate a workbook quickly, but it can duplicate logic across reports.

The `dim_` and `fact_` files are the modeled star schema.
Dimensions hold descriptive filters.
The fact table holds numeric measures at the date, region, and property type grain.
This is the preferred path for `Housing-Market-Insights`.

## Fabric object mapping

| Layer | Workshop object |
| --- | --- |
| Workspace | `Schwab-Analytics-Dev`, `Schwab-Analytics-Test`, `Schwab-Analytics-Prod` |
| Lakehouse | `lh_housing` |
| Raw files | `Files/raw` |
| Bronze | `bronze_market_tracker`, `bronze_listings` |
| Silver | `dim_region`, `dim_date`, `dim_property_type`, `fact_home_sales` |
| Gold | `gold_market_summary`, `gold_region_latest` |
| Semantic model | `Housing-Market-Insights (Direct Lake)` |

Core measures expected in the model:

`Homes Sold`, `New Listings`, `Inventory`, `Avg Median Sale Price`, `Median Days on Market`, `Avg Sale to List %`, `Sold Above List %`, `Months of Supply`, `Homes Sold PY`, and `Homes Sold YoY %`.

## Using real Redfin data

The workshop data is synthetic and generated locally.
If you want to replace it with real public market data, start with the Redfin Data Center:

https://www.redfin.com/news/data-center/

When swapping in real data, re-check schema, licensing, privacy, refresh cadence, and metric definitions before using the workshop labs.
