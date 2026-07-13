"""Generate the synthetic housing-market dataset for the Schwab Power BI + Fabric workshop.

The workshop teaches a Tableau audience how to move to Power BI and Microsoft
Fabric. Tableau users know the public **Redfin Data Center** housing dataset
well, so this generator produces data shaped like Redfin's market-tracker feed,
plus a small MLS-style listings feed, so the labs feel familiar.

Everything here is SYNTHETIC. No real Redfin data, no real Schwab data. The
numbers are randomly generated around believable ranges so the end-to-end labs
(model, report, Copilot, MCP, Data Agent) run in your own Fabric tenant without
touching any real system. To use the genuine public data instead, see the note
in data/README.md.

It writes two "shapes" on purpose so the migration story lands:

  1. raw/redfin/market_tracker.csv - one wide, denormalized extract, the way a
     Tableau .hyper extract looks today. This is the "before" the labs migrate.
  2. raw/redfin/*.csv normalized dims + fact, and raw/mls/listings.csv, so the
     modeling lab can build a proper star schema (the "after").

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

# ---- reference vocabulary (synthetic, but real US metros so maps work) ------
# (metro display name, state, region_type, base median price, base monthly sales)
METROS = [
    ("Seattle, WA", "WA", 780000, 4200),
    ("Denver, CO", "CO", 610000, 3600),
    ("Austin, TX", "TX", 540000, 3900),
    ("Phoenix, AZ", "AZ", 470000, 5200),
    ("Chicago, IL", "IL", 360000, 6100),
    ("Atlanta, GA", "GA", 410000, 5600),
    ("Boston, MA", "MA", 720000, 3100),
    ("Nashville, TN", "TN", 460000, 3300),
    ("Charlotte, NC", "NC", 400000, 3800),
    ("Miami, FL", "FL", 560000, 4400),
    ("Portland, OR", "OR", 560000, 2600),
    ("Dallas, TX", "TX", 420000, 6400),
]
PROPERTY_TYPES = [
    "All Residential",
    "Single Family Residential",
    "Condo/Co-op",
    "Townhouse",
]
# non-"All" types get a share of the total so the parts sum sensibly
TYPE_SHARE = {
    "Single Family Residential": 0.62,
    "Condo/Co-op": 0.22,
    "Townhouse": 0.16,
}
TYPE_PRICE_FACTOR = {
    "All Residential": 1.00,
    "Single Family Residential": 1.08,
    "Condo/Co-op": 0.78,
    "Townhouse": 0.92,
}


def month_starts(months: int):
    """Return the first-of-month dates for the last `months`, oldest first."""
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


def seasonal_factor(d: date) -> float:
    """Spring/summer selling season bump, winter dip."""
    # peak around May-June (month 5-6), trough Dec-Jan
    return 1.0 + 0.18 * np.sin((d.month - 3) / 12.0 * 2 * np.pi)


def price_trend(i: int, n: int) -> float:
    """Gentle appreciation over the window with a mid-window softening."""
    base = 1.0 + 0.06 * (i / max(1, n - 1))          # ~6% over the window
    dip = -0.03 * np.exp(-(((i - n * 0.55) / (n * 0.16)) ** 2))  # a soft patch
    return base + dip


def main(months: int) -> None:
    random.seed(SEED)
    np.random.seed(SEED)
    periods = month_starts(months)
    n = len(periods)

    # ---- dimensions --------------------------------------------------------
    dim_region_rows = []
    for rid, (metro, st, _p, _s) in enumerate(METROS, start=1):
        dim_region_rows.append({
            "region_id": rid,
            "region": metro,
            "region_type": "metro",
            "state": st,
        })
    dim_region = pd.DataFrame(dim_region_rows)

    dim_date_rows = []
    for did, p in enumerate(periods, start=1):
        dim_date_rows.append({
            "date_id": did,
            "period_begin": p.isoformat(),
            "period_end": month_end(p).isoformat(),
            "year": p.year,
            "month": p.month,
            "month_name": p.strftime("%B"),
            "quarter": f"Q{(p.month - 1)//3 + 1}",
        })
    dim_date = pd.DataFrame(dim_date_rows)

    dim_property = pd.DataFrame(
        [{"property_type_id": i + 1, "property_type": t} for i, t in enumerate(PROPERTY_TYPES)]
    )
    ptype_id = {t: i + 1 for i, t in enumerate(PROPERTY_TYPES)}

    # ---- fact: one row per region x period x property_type ------------------
    fact_rows = []
    wide_rows = []
    for rid, (metro, st, base_price, base_sales) in enumerate(METROS, start=1):
        for i, p in enumerate(periods):
            did = i + 1
            trend = price_trend(i, n)
            seas = seasonal_factor(p)
            # "All Residential" first, then split into the sub-types
            all_price = base_price * trend * (1 + np.random.normal(0, 0.012))
            all_sales = int(base_sales * seas * (1 + np.random.normal(0, 0.05)))
            for t in PROPERTY_TYPES:
                if t == "All Residential":
                    homes_sold = all_sales
                    price_factor = 1.0
                else:
                    homes_sold = int(all_sales * TYPE_SHARE[t] * (1 + np.random.normal(0, 0.04)))
                    price_factor = TYPE_PRICE_FACTOR[t]
                median_price = round(all_price * price_factor / 500) * 500
                new_listings = int(homes_sold * (1.05 + np.random.normal(0, 0.08)))
                inventory = int(homes_sold * (1.6 + np.random.normal(0, 0.12)))
                months_supply = round(inventory / max(1, homes_sold), 1)
                median_dom = max(5, int(28 - 40 * (seas - 1.0) + np.random.normal(0, 4)))
                ppsf = round(median_price / (1650 + np.random.normal(0, 120)), 2)
                sale_to_list = round(0.995 + 0.03 * (seas - 1.0) + np.random.normal(0, 0.006), 4)
                sold_above_list = round(min(0.85, max(0.10,
                    0.42 + 0.6 * (seas - 1.0) + np.random.normal(0, 0.05))), 3)
                new_listings = max(homes_sold, new_listings)

                fact_rows.append({
                    "region_id": rid,
                    "date_id": did,
                    "property_type_id": ptype_id[t],
                    "median_sale_price": median_price,
                    "homes_sold": homes_sold,
                    "new_listings": new_listings,
                    "inventory": inventory,
                    "months_of_supply": months_supply,
                    "median_days_on_market": median_dom,
                    "median_ppsf": ppsf,
                    "avg_sale_to_list": sale_to_list,
                    "sold_above_list_share": sold_above_list,
                })
                wide_rows.append({
                    "region": metro,
                    "state": st,
                    "region_type": "metro",
                    "period_begin": p.isoformat(),
                    "period_end": month_end(p).isoformat(),
                    "year": p.year,
                    "month_name": p.strftime("%B"),
                    "property_type": t,
                    "median_sale_price": median_price,
                    "homes_sold": homes_sold,
                    "new_listings": new_listings,
                    "inventory": inventory,
                    "months_of_supply": months_supply,
                    "median_days_on_market": median_dom,
                    "median_ppsf": ppsf,
                    "avg_sale_to_list": sale_to_list,
                    "sold_above_list_share": sold_above_list,
                })

    fact = pd.DataFrame(fact_rows)
    wide = pd.DataFrame(wide_rows)

    # year-over-year on the wide extract (so a Tableau-style calc exists to replace)
    wide = wide.sort_values(["region", "property_type", "period_begin"]).reset_index(drop=True)
    wide["median_sale_price_yoy"] = (
        wide.groupby(["region", "property_type"])["median_sale_price"].pct_change(12).round(4)
    )
    wide["homes_sold_yoy"] = (
        wide.groupby(["region", "property_type"])["homes_sold"].pct_change(12).round(4)
    )

    # ---- MLS-style listings feed (a second source, for the ingestion lab) --
    agents = [f"Agent {i:03d}" for i in range(1, 61)]
    offices = ["Cascade Realty", "Summit Homes", "Blue Sky Group", "Anchor Properties",
               "Evergreen Realty", "Skyline Partners"]
    listing_rows = []
    lid = 1
    for rid, (metro, st, base_price, base_sales) in enumerate(METROS, start=1):
        # a sample of individual listings in the most recent 6 months
        for p in periods[-6:]:
            for _ in range(max(20, base_sales // 120)):
                t = random.choices(
                    ["Single Family Residential", "Condo/Co-op", "Townhouse"],
                    weights=[62, 22, 16])[0]
                lp = round(base_price * TYPE_PRICE_FACTOR[t] *
                           (1 + np.random.normal(0, 0.22)) / 1000) * 1000
                status = random.choices(["Sold", "Active", "Pending"], weights=[55, 30, 15])[0]
                sp = round(lp * (0.98 + np.random.normal(0, 0.03)) / 1000) * 1000 if status == "Sold" else ""
                listing_rows.append({
                    "listing_id": lid,
                    "region": metro,
                    "state": st,
                    "property_type": t,
                    "list_date": (p + timedelta(days=random.randint(0, 27))).isoformat(),
                    "list_price": int(lp),
                    "status": status,
                    "sale_price": int(sp) if sp != "" else "",
                    "beds": random.choice([2, 3, 3, 4, 4, 5]),
                    "baths": random.choice([1, 2, 2, 3, 3, 4]),
                    "sqft": random.randint(900, 4200),
                    "list_agent": random.choice(agents),
                    "office": random.choice(offices),
                })
                lid += 1
    listings = pd.DataFrame(listing_rows)

    # ---- write -------------------------------------------------------------
    redfin_dir = os.path.join(RAW, "redfin")
    mls_dir = os.path.join(RAW, "mls")
    os.makedirs(redfin_dir, exist_ok=True)
    os.makedirs(mls_dir, exist_ok=True)

    wide.to_csv(os.path.join(redfin_dir, "market_tracker.csv"), index=False)
    dim_region.to_csv(os.path.join(redfin_dir, "dim_region.csv"), index=False)
    dim_date.to_csv(os.path.join(redfin_dir, "dim_date.csv"), index=False)
    dim_property.to_csv(os.path.join(redfin_dir, "dim_property_type.csv"), index=False)
    fact.to_csv(os.path.join(redfin_dir, "fact_home_sales.csv"), index=False)
    listings.to_csv(os.path.join(mls_dir, "listings.csv"), index=False)

    print("Wrote synthetic housing data:")
    print(f"  redfin/market_tracker.csv      {len(wide):>6} rows  (wide 'Tableau extract' shape)")
    print(f"  redfin/fact_home_sales.csv     {len(fact):>6} rows  (star-schema fact)")
    print(f"  redfin/dim_region.csv          {len(dim_region):>6} rows")
    print(f"  redfin/dim_date.csv            {len(dim_date):>6} rows")
    print(f"  redfin/dim_property_type.csv   {len(dim_property):>6} rows")
    print(f"  mls/listings.csv               {len(listings):>6} rows  (second source)")
    print(f"\n  {n} months x {len(METROS)} metros x {len(PROPERTY_TYPES)} property types.")
    print("  Synthetic only. See data/README.md to swap in the real public Redfin feed.")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--months", type=int, default=24, help="months of history (default 24)")
    args = ap.parse_args()
    main(args.months)
