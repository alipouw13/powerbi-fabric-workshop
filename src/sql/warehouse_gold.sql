-- Warehouse gold (Contoso Insurance workshop) - the SQL alternative to the
-- Lakehouse notebooks. If your team prefers T-SQL over Spark, build the same
-- gold layer in the Fabric Warehouse `wh_insurance`. Direct Lake works over
-- either. Run in wh_insurance whose Lakehouse (lh_insurance) silver tables are
-- shortcutted in, or adapt schema names to your environment.

-- Premium production: product x region x channel x month
CREATE VIEW gold_premium_summary AS
SELECT
    d.[year],
    d.[month],
    d.month_name,
    d.period_begin,
    p.product,
    p.region,
    p.channel,
    SUM(p.written_premium)  AS written_premium,
    SUM(p.earned_premium)   AS earned_premium,
    SUM(p.policies_written) AS policies_written,
    SUM(p.policies_inforce) AS policies_inforce
FROM fact_premium p
JOIN dim_date     d ON d.date_id = p.date_id
GROUP BY d.[year], d.[month], d.month_name, d.period_begin, p.product, p.region, p.channel;
GO

-- Loss ratio: earned premium vs incurred losses by product x region x month
CREATE VIEW gold_loss_ratio AS
WITH prem AS (
    SELECT d.[year], d.[month], d.period_begin, p.product, p.region,
           SUM(p.earned_premium) AS earned_premium
    FROM fact_premium p JOIN dim_date d ON d.date_id = p.date_id
    GROUP BY d.[year], d.[month], d.period_begin, p.product, p.region
),
loss AS (
    SELECT d.[year], d.[month], c.product, c.region,
           SUM(c.incurred_loss) AS incurred_loss,
           SUM(c.paid_loss)     AS paid_loss,
           COUNT(*)             AS claim_count
    FROM fact_claim c JOIN dim_date d ON d.date_id = c.date_id
    GROUP BY d.[year], d.[month], c.product, c.region
)
SELECT
    prem.[year], prem.[month], prem.period_begin, prem.product, prem.region,
    prem.earned_premium,
    COALESCE(loss.incurred_loss, 0) AS incurred_loss,
    COALESCE(loss.paid_loss, 0)     AS paid_loss,
    COALESCE(loss.claim_count, 0)   AS claim_count,
    CASE WHEN prem.earned_premium > 0
         THEN COALESCE(loss.incurred_loss, 0) / prem.earned_premium ELSE 0 END AS loss_ratio
FROM prem
LEFT JOIN loss
  ON loss.[year] = prem.[year] AND loss.[month] = prem.[month]
 AND loss.product = prem.product AND loss.region = prem.region;
GO

-- Agent scorecard: written premium, loss ratio and policy count per agent
CREATE VIEW gold_agent_scorecard AS
WITH prem AS (
    SELECT agent_id,
           SUM(written_premium) AS written_premium,
           SUM(earned_premium)  AS earned_premium,
           SUM(policies_written) AS policies_written
    FROM fact_premium GROUP BY agent_id
),
loss AS (
    SELECT fp.agent_id, SUM(c.incurred_loss) AS incurred_loss
    FROM fact_claim c
    JOIN (SELECT DISTINCT policy_id, agent_id FROM fact_premium) fp
      ON fp.policy_id = c.policy_id
    GROUP BY fp.agent_id
)
SELECT
    a.agent_id, a.agent_name, a.agency, a.region, a.channel,
    prem.written_premium, prem.policies_written,
    COALESCE(loss.incurred_loss, 0) AS incurred_loss,
    CASE WHEN prem.earned_premium > 0
         THEN COALESCE(loss.incurred_loss, 0) / prem.earned_premium ELSE 0 END AS loss_ratio
FROM prem
JOIN dim_agent a ON a.agent_id = prem.agent_id
LEFT JOIN loss ON loss.agent_id = prem.agent_id;
GO
