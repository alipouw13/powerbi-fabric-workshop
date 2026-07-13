-- Warehouse gold (housing workshop) - the SQL alternative to the Lakehouse
-- notebooks. If your team prefers T-SQL over Spark, build the same gold layer
-- in a Fabric Warehouse. Direct Lake works over either.
--
-- Run in a Fabric Warehouse whose Lakehouse (lh_housing) is shortcutted in, or
-- adapt schema names to your environment.

-- Headline grid: metro x month x property type
CREATE VIEW gold_market_summary AS
SELECT
    r.region,
    r.state,
    d.period_begin,
    d.[year],
    d.month_name,
    p.property_type,
    f.median_sale_price,
    f.homes_sold,
    f.new_listings,
    f.inventory,
    f.months_of_supply,
    f.median_days_on_market,
    f.avg_sale_to_list,
    f.sold_above_list_share
FROM fact_home_sales   f
JOIN dim_region        r ON r.region_id = f.region_id
JOIN dim_date          d ON d.date_id = f.date_id
JOIN dim_property_type p ON p.property_type_id = f.property_type_id;
GO

-- Latest month per metro (All Residential) for ranking visuals
CREATE VIEW gold_region_latest AS
WITH latest AS (
    SELECT MAX(d.period_begin) AS max_period
    FROM fact_home_sales f
    JOIN dim_date d ON d.date_id = f.date_id
)
SELECT
    r.region,
    r.state,
    f.median_sale_price,
    f.homes_sold,
    f.months_of_supply,
    f.median_days_on_market,
    f.sold_above_list_share
FROM fact_home_sales   f
JOIN dim_region        r ON r.region_id = f.region_id
JOIN dim_date          d ON d.date_id = f.date_id
JOIN dim_property_type p ON p.property_type_id = f.property_type_id
CROSS JOIN latest l
WHERE p.property_type = 'All Residential'
  AND d.period_begin = l.max_period;
GO
