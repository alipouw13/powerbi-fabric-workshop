"""Generate the synthetic P&C insurance dataset for the Schwab Power BI + Fabric workshop.

The workshop teaches a Tableau audience how to move to Power BI and Microsoft
Fabric, using a **property & casualty (P&C) insurance** story, "Contoso
Insurance". The schema is aligned to the Contoso Insurance Fabric demo
(github.com/alipouw13/fabric-test) so the lab and the demo tell one story.

Everything here is SYNTHETIC. No real customer data. Contoso Insurance writes
Auto, Home, Renters, Life and Umbrella policies through agents across regions and
channels. The data lets the labs answer the questions a carrier cares about:
written / earned premium, claims, and loss ratio.

It writes two "shapes" on purpose so the Tableau-to-Power-BI migration story
lands:

  1. raw/contoso/policy_claims_extract.csv - one wide, denormalized extract, the
     way a Tableau .hyper extract looks today. This is the "before" the labs
     migrate.
  2. raw/contoso/*.csv normalized dims + facts (the star), and
     raw/ops/claims_intake.csv, a second operational feed (the kind of data a
     Rayfin claims-intake app would land in Fabric).

Run:  python data/generate_data.py                 # default 24 months
      python data/generate_data.py --months 12
"""
from __future__ import annotations

import argparse
import os
import random
from datetime import date, timedelta

import numpy as np
import pandas as pd

SEED = 42
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

# ---- reference vocabulary (synthetic, aligned to Contoso Insurance) ----------
# (product, base monthly new policies, base annual premium, base loss ratio)
PRODUCTS = [
    ("Auto", 280, 1450, 0.68),
    ("Home", 180, 1850, 0.61),
    ("Renters", 140, 280, 0.42),
    ("Life", 100, 1200, 0.35),
    ("Umbrella", 52, 520, 0.30),
]
REGIONS = ["Northeast", "Southeast", "Midwest", "Southwest", "West"]
CHANNELS = ["Independent Agent", "Captive Agent", "Direct", "Online"]
CHANNEL_WEIGHTS = [0.34, 0.28, 0.22, 0.16]
SEGMENTS = ["Personal", "Preferred", "High Net Worth", "Small Business"]
COVERAGES = {
    "Auto": ["Liability", "Collision", "Comprehensive", "Uninsured Motorist"],
    "Home": ["Dwelling", "Personal Property", "Liability", "Loss of Use"],
    "Renters": ["Personal Property", "Liability", "Loss of Use"],
    "Life": ["Term", "Whole"],
    "Umbrella": ["Excess Liability"],
}
LOSS_TYPES = ["Collision", "Theft", "Fire", "Water Damage", "Wind/Hail",
              "Liability", "Medical", "Catastrophe"]
CLAIM_STATUS = ["Open", "In Review", "Approved", "Paid", "Denied", "Closed"]
FIRST = ["Avery", "Jordan", "Riley", "Morgan", "Casey", "Taylor", "Quinn", "Reese",
         "Skyler", "Hayden", "Rowan", "Emerson", "Parker", "Sage", "Dakota", "Finley"]
LAST = ["Nguyen", "Patel", "Garcia", "Smith", "Johnson", "Lee", "Brown", "Martinez",
        "Davis", "Lopez", "Wilson", "Anderson", "Thomas", "Moore", "Clark", "Walker"]
AGENCIES = ["Cascade", "Summit", "Blue Ridge", "Anchor", "Evergreen", "Skyline",
            "Harborview", "Pinnacle", "Meridian", "Crossroads"]


def month_starts(months: int):
    today = date.today().replace(day=1)
    out = []
    y, m = today.year, today.month
    for _ in range(months):
        out.append(date(y, m, 1))
        m -= 1
        if m == 0:
            y -= 1
            m = 12
    return list(reversed(out))


def month_end(d: date) -> date:
    if d.month == 12:
        return date(d.year, 12, 31)
    return date(d.year, d.month + 1, 1) - timedelta(days=1)


def seasonal(d: date) -> float:
    # more auto/home claims in winter and storm season
    return 1.0 + 0.15 * np.sin((d.month - 2) / 12.0 * 2 * np.pi)


def growth(i: int, n: int) -> float:
    return 1.0 + 0.05 * (i / max(1, n - 1))  # ~5% book growth over the window


def main(months: int) -> None:
    random.seed(SEED)
    np.random.seed(SEED)
    periods = month_starts(months)
    n = len(periods)

    # ---- dim_date ----------------------------------------------------------
    dim_date = pd.DataFrame([
        {"date_id": i + 1, "period_begin": p.isoformat(), "period_end": month_end(p).isoformat(),
         "year": p.year, "month": p.month, "month_name": p.strftime("%B"),
         "quarter": f"Q{(p.month - 1)//3 + 1}"}
        for i, p in enumerate(periods)
    ])

    # ---- dim_agent ---------------------------------------------------------
    agents = []
    for aid in range(1, 41):
        agents.append({
            "agent_id": aid,
            "agent_name": f"{random.choice(FIRST)} {random.choice(LAST)}",
            "agency": f"{random.choice(AGENCIES)} Insurance Group",
            "region": random.choice(REGIONS),
            "channel": random.choices(CHANNELS, weights=CHANNEL_WEIGHTS)[0],
        })
    dim_agent = pd.DataFrame(agents)

    # ---- dim_customer ------------------------------------------------------
    customers = []
    for cid in range(1, 1201):
        customers.append({
            "customer_id": cid,
            "customer_name": f"{random.choice(FIRST)} {random.choice(LAST)}",
            "segment": random.choices(SEGMENTS, weights=[0.5, 0.28, 0.10, 0.12])[0],
            "region": random.choice(REGIONS),
            "tenure_years": int(max(0, np.random.gamma(3, 2))),
        })
    dim_customer = pd.DataFrame(customers)

    # ---- dim_coverage ------------------------------------------------------
    cov_rows, cov_id = [], 1
    cov_index = {}
    for prod, covs in COVERAGES.items():
        for c in covs:
            cov_rows.append({"coverage_id": cov_id, "product": prod, "coverage": c})
            cov_index[(prod, c)] = cov_id
            cov_id += 1
    dim_coverage = pd.DataFrame(cov_rows)

    # ---- dim_policy + fact_premium (in-force earned curve) + fact_claim -----
    policy_rows = []
    premium_rows = []
    claim_rows = []
    wide_rows = []
    intake_rows = []
    pid = 1
    clid = 1
    for prod, base_new, base_prem, base_lr in PRODUCTS:
        for i, p in enumerate(periods):        # effective (written) month
            did0 = i + 1
            n_new = int(base_new * growth(i, n) * (1 + np.random.normal(0, 0.05)))
            for _ in range(n_new):
                region = random.choice(REGIONS)
                channel = random.choices(CHANNELS, weights=CHANNEL_WEIGHTS)[0]
                agent = random.randint(1, 40)
                cust = random.randint(1, 1200)
                annual_prem = round(base_prem * (1 + np.random.normal(0, 0.22)) / 10) * 10
                annual_prem = max(120, annual_prem)
                status = random.choices(["In Force", "Lapsed", "Cancelled"],
                                        weights=[0.86, 0.09, 0.05])[0]
                policy_no = f"{prod[:2].upper()}-{p.year}{p.month:02d}-{pid:06d}"
                policy_rows.append({
                    "policy_id": pid, "policy_number": policy_no, "product": prod,
                    "customer_id": cust, "agent_id": agent, "region": region,
                    "channel": channel, "effective_date": p.isoformat(),
                    "annual_premium": annual_prem, "status": status,
                })
                monthly_earned = round(annual_prem / 12, 2)
                policy_incurred = 0
                policy_claims = 0
                # policy earns 1/12 each in-force month (up to 12 months, within window)
                for mi in range(i, min(i + 12, n)):
                    pm = periods[mi]
                    did = mi + 1
                    written = annual_prem if mi == i else 0
                    premium_rows.append({
                        "policy_id": pid, "date_id": did, "product": prod, "region": region,
                        "channel": channel, "agent_id": agent,
                        "written_premium": written, "earned_premium": monthly_earned,
                        "policies_written": 1 if mi == i else 0, "policies_inforce": 1,
                    })
                    # claims tied to that month's EARNED exposure so LR ~ base_lr
                    freq = 0.09
                    nclaims = np.random.poisson(freq * seasonal(pm))
                    base_sev = monthly_earned * base_lr / freq  # E[severity] anchor
                    for _ in range(nclaims):
                        cov = random.choice(COVERAGES[prod])
                        lt = random.choice(LOSS_TYPES)
                        sev = random.choices(["Low", "Medium", "High", "Severe"],
                                             weights=[0.55, 0.28, 0.13, 0.04])[0]
                        sev_mult = {"Low": 0.4, "Medium": 1.0, "High": 2.6, "Severe": 6.5}[sev] / 1.10
                        noise = float(np.random.lognormal(-0.125, 0.5))  # mean ~1
                        incurred = round(base_sev * sev_mult * noise / 10) * 10
                        incurred = max(100, incurred)
                        cstatus = random.choices(CLAIM_STATUS,
                                                 weights=[0.10, 0.10, 0.12, 0.40, 0.10, 0.18])[0]
                        paid = incurred if cstatus in ("Paid", "Closed") else (
                            round(incurred * random.uniform(0.1, 0.7) / 10) * 10
                            if cstatus in ("Approved", "In Review") else 0)
                        fraud = 1 if (random.random() < 0.03) else 0
                        loss_day = random.randint(0, 27)
                        claim_no = f"CLM-{pm.year}{pm.month:02d}-{clid:06d}"
                        claim_rows.append({
                            "claim_id": clid, "claim_number": claim_no, "policy_id": pid,
                            "date_id": did, "product": prod, "region": region,
                            "coverage_id": cov_index[(prod, cov)], "loss_type": lt,
                            "severity": sev, "status": cstatus,
                            "incurred_loss": incurred, "paid_loss": paid,
                            "fraud_flag": fraud,
                        })
                        intake_rows.append({
                            "claim_number": claim_no, "policy_number": policy_no,
                            "product": prod, "region": region, "coverage": cov,
                            "loss_type": lt, "loss_date": (pm + timedelta(days=loss_day)).isoformat(),
                            "reported_date": (pm + timedelta(days=loss_day + random.randint(0, 6))).isoformat(),
                            "status": cstatus, "reserve_amount": incurred, "paid_amount": paid,
                            "severity": sev, "adjuster": f"{random.choice(FIRST)} {random.choice(LAST)}",
                        })
                        policy_incurred += incurred
                        policy_claims += 1
                        clid += 1
                # wide "Tableau extract" row (denormalized, one per policy)
                wide_rows.append({
                    "policy_number": policy_no, "product": prod, "region": region,
                    "channel": channel, "period_begin": p.isoformat(),
                    "year": p.year, "month_name": p.strftime("%B"),
                    "agent_name": dim_agent.loc[agent - 1, "agent_name"],
                    "customer_segment": dim_customer.loc[cust - 1, "segment"],
                    "annual_premium": annual_prem, "written_premium": annual_prem,
                    "earned_premium": monthly_earned, "policy_status": status,
                    "incurred_loss": policy_incurred, "claim_count": policy_claims,
                })
                pid += 1

    dim_policy = pd.DataFrame(policy_rows)
    fact_premium = pd.DataFrame(premium_rows)
    fact_claim = pd.DataFrame(claim_rows)
    wide = pd.DataFrame(wide_rows)
    intake = pd.DataFrame(intake_rows)

    # year-over-year on the wide extract (a Tableau-style table calc to replace)
    wide = wide.sort_values(["product", "region", "period_begin"]).reset_index(drop=True)
    wide["written_premium_yoy"] = (
        wide.groupby(["product", "region"])["written_premium"].pct_change(12).round(4)
    )

    # ---- write -------------------------------------------------------------
    contoso = os.path.join(RAW, "contoso")
    ops = os.path.join(RAW, "ops")
    os.makedirs(contoso, exist_ok=True)
    os.makedirs(ops, exist_ok=True)

    wide.to_csv(os.path.join(contoso, "policy_claims_extract.csv"), index=False)
    dim_date.to_csv(os.path.join(contoso, "dim_date.csv"), index=False)
    dim_agent.to_csv(os.path.join(contoso, "dim_agent.csv"), index=False)
    dim_customer.to_csv(os.path.join(contoso, "dim_customer.csv"), index=False)
    dim_coverage.to_csv(os.path.join(contoso, "dim_coverage.csv"), index=False)
    dim_policy.to_csv(os.path.join(contoso, "dim_policy.csv"), index=False)
    fact_premium.to_csv(os.path.join(contoso, "fact_premium.csv"), index=False)
    fact_claim.to_csv(os.path.join(contoso, "fact_claim.csv"), index=False)
    intake.to_csv(os.path.join(ops, "claims_intake.csv"), index=False)

    lr = fact_claim["incurred_loss"].sum() / max(1, fact_premium["earned_premium"].sum())
    print("Wrote synthetic Contoso Insurance data:")
    print(f"  contoso/policy_claims_extract.csv {len(wide):>7} rows  (wide 'Tableau extract' shape)")
    print(f"  contoso/dim_policy.csv            {len(dim_policy):>7} rows")
    print(f"  contoso/fact_premium.csv          {len(fact_premium):>7} rows")
    print(f"  contoso/fact_claim.csv            {len(fact_claim):>7} rows")
    print(f"  contoso/dim_customer.csv          {len(dim_customer):>7} rows")
    print(f"  contoso/dim_agent.csv             {len(dim_agent):>7} rows")
    print(f"  contoso/dim_coverage.csv          {len(dim_coverage):>7} rows")
    print(f"  contoso/dim_date.csv              {len(dim_date):>7} rows")
    print(f"  ops/claims_intake.csv             {len(intake):>7} rows  (operational feed)")
    print(f"\n  {n} months x {len(PRODUCTS)} products x {len(REGIONS)} regions.")
    print(f"  Portfolio loss ratio ~ {lr:.1%}.  Synthetic only; aligned to the Contoso")
    print("  Insurance Fabric demo (github.com/alipouw13/fabric-test). See data/README.md.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--months", type=int, default=24, help="months of history (default 24)")
    args = ap.parse_args()
    main(args.months)
