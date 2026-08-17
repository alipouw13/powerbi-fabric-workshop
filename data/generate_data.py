"""Generate synthetic Banking and Capital Markets I&O data for the
Tableau-to-Power BI workshop.

The workshop teaches a Tableau audience how to move to Power BI, using an
enterprise **Infrastructure & Operations (I&O)** domain. The model follows the star
schema on deck slides 9 and 10: one fact table per domain, all joining the same
conformed dimensions.

Every organization, service, identifier, event, and metric is SYNTHETIC. No real
customer, account, position, trade, or market data is used.

Shapes written, on purpose, so the migration story lands:

  1. raw/tableau_extract/incident_report_extract.csv
     One wide, denormalized table - the way a Tableau .hyper extract looks
     today. This is the "before" that Lab 0 reshapes.

  2. raw/sql/*.csv
     Normalized conformed dimensions plus a fact table per domain - the "after".
     These stand in for the SQL Server views you would reach through the
     on-premises data gateway.

  3. raw/excel/capacity_YYYY_MM.csv
     A folder of monthly extracts, the "large Excel files" pain point. Lab 0
     combines these with a single query and a custom function.

  4. raw/dirty/*.csv
     Deliberately messy exports - junk header rows, cross-tabs, currency stored
     as text, mixed date formats, total rows. Every problem here has a specific
     Power Query fix. See data/power-query-cleanup.md.

Run:  python data/generate_data.py                 # default 24 months
      python data/generate_data.py --months 12
"""
from __future__ import annotations

import argparse
import csv
import os
from datetime import date, timedelta

import numpy as np
import pandas as pd

SEED = 42
HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

# ---- conformed dimension vocabulary (synthetic) -----------------------------

# The two business units are the workshop's explicit reporting scope. Domains
# provide a useful second drill level without introducing a separate dimension.
TARGET_BUSINESS_UNITS = {"Banking", "Capital Markets"}

# (service_name, service_tier, business_unit, business_domain, base incident rate)
# Tier 0 is mission-critical real-time or system-of-record, Tier 1 is customer-facing,
# Tier 2 is important but tolerant of a short outage.
SERVICES = [
    ("Digital Banking Portal", "Tier 1", "Banking", "Digital Banking", 11.0),
    ("Mobile Banking", "Tier 1", "Banking", "Digital Banking", 9.0),
    ("Core Deposits Platform", "Tier 0", "Banking", "Deposits", 7.0),
    ("Payments Gateway", "Tier 0", "Banking", "Payments", 8.0),
    ("Consumer Lending Platform", "Tier 2", "Banking", "Lending", 6.0),
    ("Treasury Management", "Tier 2", "Banking", "Treasury Services", 5.0),
    ("Electronic Trading Platform", "Tier 0", "Capital Markets", "Trading", 14.0),
    ("Order Management System", "Tier 0", "Capital Markets", "Trading", 9.0),
    ("Market Data Distribution", "Tier 0", "Capital Markets", "Market Data", 7.0),
    ("Brokerage Account Platform", "Tier 1", "Capital Markets", "Brokerage", 8.0),
    ("Clearing and Settlement", "Tier 1", "Capital Markets", "Post-Trade", 6.0),
    ("Market Risk Analytics", "Tier 2", "Capital Markets", "Risk Management", 5.0),
]

# (team_name, assignment_group, shift)
TEAMS = [
    ("Platform Engineering", "L3 Engineering", "Follow the Sun"),
    ("Network Operations", "L2 Operations", "24x7"),
    ("Database Administration", "L3 Engineering", "Business Hours"),
    ("Mainframe Operations", "L2 Operations", "24x7"),
    ("Service Desk Tier 1", "L1 Service Desk", "24x7"),
    ("Service Desk Tier 2", "L2 Service Desk", "Extended Hours"),
    ("Security Operations", "L2 Security", "24x7"),
    ("Application Support", "L2 Operations", "Business Hours"),
    ("Cloud Infrastructure", "L3 Engineering", "Follow the Sun"),
    ("Storage & Backup", "L3 Engineering", "Business Hours"),
]

# (site_name, city, state, region, datacenter)
LOCATIONS = [
    ("North Campus", "Dallas", "TX", "Southwest", "DC-DFW-01"),
    ("Central Tech Center", "Fort Worth", "TX", "Southwest", "DC-DFW-01"),
    ("West Operations", "Las Vegas", "NV", "West", "DC-PHX-01"),
    ("Summit Office", "Boulder", "CO", "West", "DC-PHX-01"),
    ("Ridgeview Campus", "Colorado Springs", "CO", "West", "DC-PHX-01"),
    ("Midwest Hub", "Columbus", "OH", "Midwest", "DC-CHI-01"),
    ("Southeast Service Center", "Tampa", "FL", "Southeast", "DC-ATL-01"),
    ("Lakeside Office", "Madison", "WI", "Midwest", "DC-CHI-01"),
]

# (severity_code, severity_name, priority, sla_hours, share of incidents)
SEVERITIES = [
    ("SEV1", "Critical", "P1", 4, 0.03),
    ("SEV2", "High", "P2", 8, 0.12),
    ("SEV3", "Moderate", "P3", 24, 0.45),
    ("SEV4", "Low", "P4", 72, 0.40),
]

CI_TYPES = [
    ("Server", 0.30),
    ("Database", 0.14),
    ("Application", 0.20),
    ("Network Device", 0.12),
    ("Storage Array", 0.08),
    ("Mainframe LPAR", 0.06),
    ("Load Balancer", 0.05),
    ("Virtual Machine", 0.05),
]
ENVIRONMENTS = [("Production", 0.55), ("Non-Production", 0.25), ("DR", 0.10), ("Development", 0.10)]
CRITICALITY = [("Business Critical", 0.20), ("High", 0.30), ("Medium", 0.35), ("Low", 0.15)]

# CI types that carry utilization readings, so fact_capacity has something to measure.
INFRA_CI_TYPES = ["Server", "Database", "Storage Array", "Virtual Machine"]
LPAR_CI_TYPE = "Mainframe LPAR"

# Coverage guarantees, so every fact reaches both business units at any --ci-count.
CI_PER_SERVICE = 1        # one CI per service, so no service is ever orphaned
LPARS_PER_UNIT = 3        # fact_mainframe needs LPARs in both units
INFRA_PER_UNIT = 6        # fact_capacity needs infrastructure CIs in both units

# The support team that owns mainframe LPARs, matched by name against TEAMS.
MAINFRAME_TEAM_NAME = "Mainframe Operations"

# How far back assets were bought, and how long warranties run. Both drive the
# span of dim_date, because fact_asset has to key into it.
ASSET_PURCHASE_MIN_DAYS_AGO = 200
ASSET_PURCHASE_MAX_DAYS_AGO = 2400
ASSET_WARRANTY_TERM_DAYS = [365, 730, 1095, 1825]

# Every foreign key column that may appear on a fact, and the dimension it must
# resolve against. Used by validate_dataset - add a key here and it gets checked.
FOREIGN_KEYS = {
    "date_key": ("dim_date.csv", "date_key"),
    "purchase_date_key": ("dim_date.csv", "date_key"),
    "warranty_end_date_key": ("dim_date.csv", "date_key"),
    "service_key": ("dim_service.csv", "service_key"),
    "ci_key": ("dim_configuration_item.csv", "ci_key"),
    "team_key": ("dim_team.csv", "team_key"),
    "support_team_key": ("dim_team.csv", "team_key"),
    "location_key": ("dim_location.csv", "location_key"),
    "severity_key": ("dim_severity.csv", "severity_key"),
}

# Surrogate primary key per table. Must be unique and non-null.
PRIMARY_KEYS = {
    "dim_date.csv": "date_key",
    "dim_service.csv": "service_key",
    "dim_team.csv": "team_key",
    "dim_location.csv": "location_key",
    "dim_severity.csv": "severity_key",
    "dim_configuration_item.csv": "ci_key",
    "fact_incident.csv": "incident_key",
    "fact_capacity.csv": "capacity_key",
    "fact_mainframe.csv": "mainframe_key",
    "fact_service_desk.csv": "service_desk_key",
    "fact_asset.csv": "asset_key",
}

# The grain of each fact, as column lists. Enforced, not just documented.
FACT_GRAIN = {
    "fact_incident.csv": ["incident_key"],
    "fact_capacity.csv": ["date_key", "ci_key"],
    "fact_mainframe.csv": ["date_key", "ci_key"],
    "fact_service_desk.csv": ["date_key", "service_key", "team_key", "location_key"],
    "fact_asset.csv": ["asset_key"],
}

INCIDENT_CATEGORIES = [
    "Hardware Failure",
    "Software Defect",
    "Capacity Exhaustion",
    "Configuration Error",
    "Network Latency",
    "Access Request",
    "Third Party Outage",
    "Change Induced",
    "Security Event",
    "Data Quality",
]
CONTACT_TYPES = [("Phone", 0.31), ("Self Service", 0.28), ("Email", 0.16), ("Monitoring Alert", 0.20), ("Walk Up", 0.05)]
INCIDENT_STATES = ["Resolved", "Closed", "In Progress", "On Hold"]

LIFECYCLE_STATUS = [("In Service", 0.62), ("In Stock", 0.12), ("Pending Disposal", 0.10), ("Retired", 0.16)]

MONTH_NAMES = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
]


def _weighted(rng: np.random.Generator, items, size):
    """Pick from a list of (value, weight) tuples."""
    values = [v for v, _ in items]
    weights = np.array([w for _, w in items], dtype=float)
    weights = weights / weights.sum()
    return rng.choice(values, size=size, p=weights)


def build_dim_date(start: date, end: date, reporting_start: date, reporting_end: date) -> pd.DataFrame:
    """Full calendar years from start to end, flagged with the reporting window.

    The range has to cover more than the reporting window because fact_asset keys
    into this table on purchase and warranty-end dates, which sit years either
    side. Mark as Date Table also requires contiguous, whole calendar years.
    """
    days = pd.date_range(date(start.year, 1, 1), date(end.year, 12, 31), freq="D")
    df = pd.DataFrame({"date": days})
    df["date_key"] = df["date"].dt.strftime("%Y%m%d").astype(int)
    df["year"] = df["date"].dt.year
    df["quarter"] = "Q" + df["date"].dt.quarter.astype(str)
    df["month"] = df["date"].dt.month
    df["month_name"] = df["month"].map(lambda m: MONTH_NAMES[m - 1])
    df["month_year"] = df["date"].dt.strftime("%Y-%m")
    df["day_of_month"] = df["date"].dt.day
    df["day_of_week"] = df["date"].dt.dayofweek + 1
    df["day_name"] = df["date"].dt.day_name()
    df["is_weekend"] = df["day_of_week"].isin([6, 7])
    df["week_of_year"] = df["date"].dt.isocalendar().week.astype(int)
    # Fiscal year aligned to the calendar year for workshop simplicity.
    df["fiscal_year"] = df["year"]
    df["fiscal_quarter"] = df["quarter"]
    # Marks the window the event facts actually cover. Everything outside it
    # exists so asset purchase and warranty dates have a row to point at.
    df["is_reporting_period"] = (
        (df["date"] >= pd.Timestamp(reporting_start))
        & (df["date"] <= pd.Timestamp(reporting_end))
    )
    return df[[
        "date_key", "date", "year", "quarter", "month", "month_name", "month_year",
        "day_of_month", "day_of_week", "day_name", "is_weekend", "week_of_year",
        "fiscal_year", "fiscal_quarter", "is_reporting_period",
    ]]


def date_to_key(value) -> int:
    """The dim_date surrogate key for a date. Same yyyymmdd rule as build_dim_date."""
    ts = pd.Timestamp(value)
    return int(ts.year * 10000 + ts.month * 100 + ts.day)


def build_dim_service() -> pd.DataFrame:
    rows = []
    for i, (name, tier, bu, domain, rate) in enumerate(SERVICES, start=1):
        rows.append({
            "service_key": i,
            "service_id": f"SVC{i:04d}",
            "service_name": name,
            "service_tier": tier,
            "business_unit": bu,
            "business_domain": domain,
            "base_rate": rate,
        })
    return pd.DataFrame(rows)


def build_dim_team() -> pd.DataFrame:
    rows = []
    for i, (name, group, shift) in enumerate(TEAMS, start=1):
        rows.append({
            "team_key": i,
            "team_id": f"TEAM{i:03d}",
            "team_name": name,
            "assignment_group": group,
            "shift_coverage": shift,
        })
    return pd.DataFrame(rows)


def build_dim_location() -> pd.DataFrame:
    rows = []
    for i, (site, city, state, region, dc) in enumerate(LOCATIONS, start=1):
        rows.append({
            "location_key": i,
            "location_id": f"LOC{i:03d}",
            "site_name": site,
            "city": city,
            "state_province": state,
            "country": "United States",
            "region": region,
            "datacenter": dc,
        })
    return pd.DataFrame(rows)


def build_dim_severity() -> pd.DataFrame:
    rows = []
    for i, (code, name, priority, sla, _share) in enumerate(SEVERITIES, start=1):
        rows.append({
            "severity_key": i,
            "severity_code": code,
            "severity_name": name,
            "priority": priority,
            "sla_target_hours": sla,
            "severity_sort": i,
        })
    return pd.DataFrame(rows)


def _ci_coverage_plan(dim_service) -> list[tuple[int, str | None]]:
    """(service_key, forced_ci_type) pairs that must exist whatever --ci-count is.

    Without this, a small --ci-count can produce zero Mainframe LPARs in one
    business unit and fact_mainframe fails its coverage check. Coverage should
    not depend on the dice.
    """
    plan: list[tuple[int, str | None]] = []
    for svc in dim_service.itertuples(index=False):
        for _ in range(CI_PER_SERVICE):
            plan.append((int(svc.service_key), None))
    for unit in sorted(TARGET_BUSINESS_UNITS):
        unit_services = dim_service.loc[
            dim_service["business_unit"] == unit, "service_key"
        ].tolist()
        for i in range(LPARS_PER_UNIT):
            plan.append((int(unit_services[i % len(unit_services)]), LPAR_CI_TYPE))
        for i in range(INFRA_PER_UNIT):
            plan.append((
                int(unit_services[i % len(unit_services)]),
                INFRA_CI_TYPES[i % len(INFRA_CI_TYPES)],
            ))
    return plan


def min_ci_count(dim_service) -> int:
    return len(_ci_coverage_plan(dim_service))


def build_dim_configuration_item(rng, n_ci, dim_service, dim_location, dim_team) -> pd.DataFrame:
    ci_types = _weighted(rng, CI_TYPES, n_ci)
    envs = _weighted(rng, ENVIRONMENTS, n_ci)
    crits = _weighted(rng, CRITICALITY, n_ci)
    service_keys = rng.integers(1, len(dim_service) + 1, n_ci)
    location_keys = rng.integers(1, len(dim_location) + 1, n_ci)
    team_keys = rng.integers(1, len(dim_team) + 1, n_ci)

    # Front-load the guaranteed CIs, then let the random ones fill the rest.
    plan = _ci_coverage_plan(dim_service)
    for i, (svc_key, forced_type) in enumerate(plan):
        service_keys[i] = svc_key
        if forced_type is not None:
            ci_types[i] = forced_type

    team_by_name = dim_team.set_index("team_name")["team_key"].to_dict()
    assignment_by_key = dim_team.set_index("team_key")["assignment_group"].to_dict()
    mainframe_team_key = int(team_by_name[MAINFRAME_TEAM_NAME])

    prefix = {
        "Server": "SRV", "Database": "DB", "Application": "APP", "Network Device": "NET",
        "Storage Array": "STG", "Mainframe LPAR": "LPAR", "Load Balancer": "LB",
        "Virtual Machine": "VM",
    }
    rows = []
    for i in range(n_ci):
        t = ci_types[i]
        # LPARs are always owned by mainframe ops, which is both realistic and
        # what makes team_key meaningful on fact_mainframe.
        support_team_key = mainframe_team_key if t == LPAR_CI_TYPE else int(team_keys[i])
        rows.append({
            "ci_key": i + 1,
            "ci_id": f"CI{i + 1:05d}",
            "ci_name": f"{prefix[t]}-{envs[i][:3].upper()}-{i + 1:04d}",
            "ci_type": t,
            "environment": envs[i],
            "criticality": crits[i],
            "service_key": int(service_keys[i]),
            "location_key": int(location_keys[i]),
            "support_team_key": support_team_key,
            "support_group": assignment_by_key[support_team_key],
        })
    return pd.DataFrame(rows)


def _stratified_ci_sample(dim_ci, dim_service, ci_types, n):
    """Pick up to n CIs of the given types, balanced across business units.

    A plain random sample can miss a business unit entirely on a small estate,
    which breaks the conformed-dimension promise the whole workshop rests on.
    """
    unit_by_service = dim_service.set_index("service_key")["business_unit"]
    pool = dim_ci[dim_ci["ci_type"].isin(ci_types)].copy()
    if pool.empty:
        pool = dim_ci.copy()
    pool["business_unit"] = pool["service_key"].map(unit_by_service)

    by_unit = {
        unit: group.sort_values("ci_key")["ci_key"].tolist()
        for unit, group in pool.groupby("business_unit")
    }
    picked: list[int] = []
    round_index = 0
    while len(picked) < min(n, len(pool)):
        added = False
        for unit in sorted(by_unit):
            if round_index < len(by_unit[unit]) and len(picked) < n:
                picked.append(by_unit[unit][round_index])
                added = True
        if not added:
            break
        round_index += 1
    return pool[pool["ci_key"].isin(picked)].sort_values("ci_key")


def build_fact_incident(rng, dim_date, dim_service, dim_ci, dim_team, dim_location, dim_severity):
    """One row per incident. This is the primary fact for Labs 0 to 3."""
    sev_codes = [s[0] for s in SEVERITIES]
    sev_shares = np.array([s[4] for s in SEVERITIES])
    sev_shares = sev_shares / sev_shares.sum()
    sev_lookup = dim_severity.set_index("severity_code")["severity_key"].to_dict()
    sla_lookup = dim_severity.set_index("severity_key")["sla_target_hours"].to_dict()

    ci_by_service = {
        k: g["ci_key"].to_numpy() for k, g in dim_ci.groupby("service_key")
    }
    ci_location = dim_ci.set_index("ci_key")["location_key"].to_dict()
    all_ci_keys = dim_ci["ci_key"].to_numpy()
    n_teams = len(dim_team)

    rows = []
    incident_no = 1
    n_days = len(dim_date)

    for day_idx, drow in enumerate(dim_date.itertuples(index=False)):
        # Weekday volume runs higher than weekend; a mild upward trend over time.
        weekday_factor = 0.55 if drow.is_weekend else 1.0
        trend = 1.0 + (day_idx / n_days) * 0.18
        for srow in dim_service.itertuples(index=False):
            lam = srow.base_rate * weekday_factor * trend
            count = rng.poisson(lam)
            if count == 0:
                continue
            candidates = ci_by_service.get(srow.service_key, all_ci_keys)
            for _ in range(int(count)):
                sev_code = rng.choice(sev_codes, p=sev_shares)
                sev_key = sev_lookup[sev_code]
                sla_hours = sla_lookup[sev_key]

                # Resolution time correlates with severity but has a long tail.
                base_minutes = {1: 95, 2: 240, 3: 620, 4: 1500}[sev_key]
                resolve_minutes = max(6, int(rng.lognormal(np.log(base_minutes), 0.75)))

                ci_key = int(rng.choice(candidates))

                opened = pd.Timestamp(drow.date) + pd.Timedelta(
                    hours=int(rng.integers(0, 24)), minutes=int(rng.integers(0, 60))
                )
                resolved = opened + pd.Timedelta(minutes=resolve_minutes)
                state = rng.choice(INCIDENT_STATES, p=[0.42, 0.46, 0.08, 0.04])
                is_open = state in ("In Progress", "On Hold")

                rows.append({
                    "incident_key": incident_no,
                    "incident_number": f"INC{incident_no:07d}",
                    "date_key": int(drow.date_key),
                    "ci_key": ci_key,
                    "service_key": int(srow.service_key),
                    "team_key": int(rng.integers(1, n_teams + 1)),
                    "location_key": int(ci_location[ci_key]),
                    "severity_key": int(sev_key),
                    "opened_at": opened,
                    "resolved_at": pd.NaT if is_open else resolved,
                    "incident_state": state,
                    "category": rng.choice(INCIDENT_CATEGORIES),
                    "contact_type": _weighted(rng, CONTACT_TYPES, 1)[0],
                    "time_to_resolve_minutes": None if is_open else resolve_minutes,
                    "reassignment_count": int(rng.poisson(0.7)),
                    "reopened_flag": bool(rng.random() < 0.05),
                    "sla_met_flag": None if is_open else bool(resolve_minutes <= sla_hours * 60),
                    "major_incident_flag": bool(sev_key == 1 and rng.random() < 0.35),
                    "incident_count": 1,
                })
                incident_no += 1

    return pd.DataFrame(rows)


def build_fact_capacity(rng, dim_date, dim_ci, dim_service):
    """Monthly utilization per infrastructure CI. Capacity & Forecasting domain."""
    infra = _stratified_ci_sample(dim_ci, dim_service, INFRA_CI_TYPES, 120)
    # Monthly grain keeps the file small enough for a workshop laptop.
    month_starts = dim_date[dim_date["day_of_month"] == 1]

    rows = []
    capacity_key = 1
    for ci in infra.itertuples(index=False):
        drift = rng.uniform(0.0, 0.35)
        base_cpu = rng.uniform(28, 72)
        base_mem = rng.uniform(35, 78)
        allocated = float(rng.choice([512, 1024, 2048, 4096, 8192]))
        for i, drow in enumerate(month_starts.itertuples(index=False)):
            growth = 1.0 + (i / max(1, len(month_starts))) * drift
            cpu = min(99.0, base_cpu * growth + rng.normal(0, 4))
            mem = min(99.0, base_mem * growth + rng.normal(0, 4))
            used = min(allocated * 0.98, allocated * (0.45 + 0.4 * (i / max(1, len(month_starts)))) + rng.normal(0, 30))
            rows.append({
                "capacity_key": capacity_key,
                "date_key": int(drow.date_key),
                "ci_key": int(ci.ci_key),
                "service_key": int(ci.service_key),
                "location_key": int(ci.location_key),
                "team_key": int(ci.support_team_key),
                "cpu_utilization_pct": round(max(2.0, cpu), 2),
                "memory_utilization_pct": round(max(4.0, mem), 2),
                "storage_allocated_gb": round(allocated, 2),
                "storage_used_gb": round(max(10.0, used), 2),
                "headroom_pct": round(max(0.0, 100 - max(cpu, mem)), 2),
            })
            capacity_key += 1
    return pd.DataFrame(rows)


def build_fact_mainframe(rng, dim_date, dim_ci, dim_service):
    """Daily MIPS and batch metrics per LPAR. Mainframe Performance domain."""
    lpars = _stratified_ci_sample(dim_ci, dim_service, [LPAR_CI_TYPE], 12)

    rows = []
    mainframe_key = 1
    for lpar in lpars.itertuples(index=False):
        capacity = float(rng.choice([1200, 1800, 2400, 3200]))
        base = capacity * rng.uniform(0.45, 0.70)
        for i, drow in enumerate(dim_date.itertuples(index=False)):
            # Month-end batch peaks are the pattern the Mainframe group looks for.
            month_end_boost = 1.35 if drow.day_of_month >= 27 else 1.0
            weekend_dip = 0.72 if drow.is_weekend else 1.0
            mips = base * month_end_boost * weekend_dip * (1 + i / len(dim_date) * 0.15)
            mips = min(capacity * 0.99, mips + rng.normal(0, capacity * 0.03))
            batch_minutes = int(max(45, rng.normal(320 * month_end_boost, 55)))
            rows.append({
                "mainframe_key": mainframe_key,
                "date_key": int(drow.date_key),
                "ci_key": int(lpar.ci_key),
                "service_key": int(lpar.service_key),
                "location_key": int(lpar.location_key),
                "team_key": int(lpar.support_team_key),
                "mips_consumed": round(max(10.0, mips), 2),
                "mips_capacity": capacity,
                "batch_jobs_completed": int(max(0, rng.normal(880 * month_end_boost, 90))),
                "batch_jobs_failed": int(max(0, rng.poisson(6 * month_end_boost))),
                "batch_window_minutes": batch_minutes,
                "transactions_processed": int(max(0, rng.normal(1_450_000 * month_end_boost, 180_000))),
            })
            mainframe_key += 1
    return pd.DataFrame(rows)


def build_fact_service_desk(rng, dim_date, dim_service, dim_team, dim_location):
    """Daily ticket and staffing metrics. Service Desk & Workforce domain."""
    desk_teams = dim_team[dim_team["assignment_group"].str.contains("Service Desk")]
    if desk_teams.empty:
        desk_teams = dim_team.head(2)

    # Sites that staff the desk, taken from dim_location rather than hardcoded,
    # so the keys are guaranteed to resolve however the dimension is edited.
    desk_location_keys = dim_location["location_key"].tolist()[:3]

    rows = []
    service_desk_key = 1
    mean_service_rate = dim_service["base_rate"].mean()
    for drow in dim_date.itertuples(index=False):
        weekend_factor = 0.35 if drow.is_weekend else 1.0
        for team in desk_teams.itertuples(index=False):
            for loc_key in desk_location_keys:
                for service in dim_service.itertuples(index=False):
                    # Allocate workload by supported business service so every
                    # service-desk metric can roll up to the two focus units.
                    service_factor = service.base_rate / mean_service_rate
                    received = int(max(0, rng.normal(18 * service_factor * weekend_factor, 5)))
                    resolved = int(received * rng.uniform(0.82, 0.98))
                    fcr = int(resolved * rng.uniform(0.55, 0.78))
                    scheduled = int(max(1, rng.normal(2.2 * service_factor * weekend_factor, 0.7)))
                    rows.append({
                        "service_desk_key": service_desk_key,
                        "date_key": int(drow.date_key),
                        "service_key": int(service.service_key),
                        "team_key": int(team.team_key),
                        "location_key": int(loc_key),
                        "tickets_received": received,
                        "tickets_resolved": resolved,
                        "first_contact_resolved": fcr,
                        "calls_abandoned": int(max(0, rng.normal(received * 0.06, 1.5))),
                        "agents_scheduled": scheduled,
                        "agents_available": max(1, scheduled - int(rng.poisson(0.3))),
                        "avg_handle_time_minutes": round(float(max(1, rng.normal(11.5, 2.2))), 2),
                        "avg_speed_to_answer_seconds": round(float(max(5, rng.normal(48, 14))), 1),
                    })
                    service_desk_key += 1
    return pd.DataFrame(rows)


def build_fact_asset(rng, dim_ci, end: date, calendar_start: date, calendar_end: date):
    """One row per asset. Asset & CMDB domain.

    Two date keys, both pointing at dim_date. That makes dim_date a role-playing
    dimension here: only one relationship can be active, the other needs
    USERELATIONSHIP. Both are clamped into the dim_date span so neither lands in
    a blank member.
    """
    rows = []
    for i, ci in enumerate(dim_ci.itertuples(index=False), start=1):
        purchased = end - timedelta(days=int(rng.integers(
            ASSET_PURCHASE_MIN_DAYS_AGO, ASSET_PURCHASE_MAX_DAYS_AGO
        )))
        warranty_end = purchased + timedelta(days=int(rng.choice(ASSET_WARRANTY_TERM_DAYS)))
        purchased = min(max(purchased, calendar_start), calendar_end)
        warranty_end = min(max(warranty_end, calendar_start), calendar_end)
        rows.append({
            "asset_key": i,
            "asset_tag": f"AST{i:06d}",
            "ci_key": int(ci.ci_key),
            "service_key": int(ci.service_key),
            "location_key": int(ci.location_key),
            "team_key": int(ci.support_team_key),
            "purchase_date_key": date_to_key(purchased),
            "warranty_end_date_key": date_to_key(warranty_end),
            "purchase_date": purchased,
            "warranty_end_date": warranty_end,
            "lifecycle_status": _weighted(rng, LIFECYCLE_STATUS, 1)[0],
            "acquisition_cost_usd": round(float(rng.uniform(1200, 48000)), 2),
            "annual_support_cost_usd": round(float(rng.uniform(150, 7200)), 2),
            "is_under_warranty": bool(warranty_end >= end),
            "cmdb_complete_flag": bool(rng.random() < 0.83),
            "asset_count": 1,
        })
    return pd.DataFrame(rows)


def build_tableau_extract(fact_incident, dim_date, dim_service, dim_ci, dim_team, dim_location, dim_severity):
    """The wide, denormalized 'before' table - what a Tableau .hyper looks like."""
    df = (
        fact_incident
        .merge(dim_date[["date_key", "date", "year", "quarter", "month_name", "month_year", "is_weekend"]], on="date_key")
        .merge(dim_service[[
            "service_key", "service_name", "service_tier", "business_unit", "business_domain"
        ]], on="service_key")
        .merge(dim_ci[["ci_key", "ci_name", "ci_type", "environment", "criticality"]], on="ci_key")
        .merge(dim_team[["team_key", "team_name", "assignment_group", "shift_coverage"]], on="team_key")
        .merge(dim_location[["location_key", "site_name", "city", "state_province", "region", "datacenter"]], on="location_key")
        .merge(dim_severity[["severity_key", "severity_code", "severity_name", "priority", "sla_target_hours"]], on="severity_key")
    )
    # Pre-aggregated columns baked into the extract, exactly the habit the labs unwind.
    df["resolve_hours"] = df["time_to_resolve_minutes"] / 60.0
    df["is_breached"] = df["sla_met_flag"].apply(lambda v: None if pd.isna(v) else (not v))
    keep = [
        "incident_number", "date", "year", "quarter", "month_name", "month_year", "is_weekend",
        "service_name", "service_tier", "business_unit", "business_domain",
        "ci_name", "ci_type", "environment", "criticality",
        "team_name", "assignment_group", "shift_coverage",
        "site_name", "city", "state_province", "region", "datacenter",
        "severity_code", "severity_name", "priority", "sla_target_hours",
        "category", "contact_type", "incident_state",
        "opened_at", "resolved_at", "time_to_resolve_minutes", "resolve_hours",
        "reassignment_count", "reopened_flag", "sla_met_flag", "is_breached", "major_incident_flag",
    ]
    return df[keep]


def validate_dataset(outputs) -> None:
    """Fail generation before writing anything, not after someone builds a report.

    Checks, in order:
      1. Focus-unit vocabulary has not drifted.
      2. Every surrogate primary key is unique and non-null.
      3. Every foreign key on every table resolves to a real dimension row.
      4. Every fact carries at least one date key.
      5. Every fact reaches both business units.
      6. Every fact honours its declared grain.
    """
    dim_service = outputs["dim_service.csv"]
    actual_units = set(dim_service["business_unit"])
    if actual_units != TARGET_BUSINESS_UNITS:
        raise ValueError(
            f"Expected business units {sorted(TARGET_BUSINESS_UNITS)}, got {sorted(actual_units)}"
        )

    for name, key in PRIMARY_KEYS.items():
        df = outputs[name]
        if key not in df.columns:
            raise ValueError(f"{name} is missing its primary key {key}")
        if df[key].isna().any():
            raise ValueError(f"{name}.{key} contains nulls")
        if df[key].duplicated().any():
            dupes = df.loc[df[key].duplicated(), key].unique()[:5]
            raise ValueError(f"{name}.{key} is not unique, e.g. {list(dupes)}")

    # Referential integrity. This is the check that catches a fact losing a key.
    for name, df in outputs.items():
        own_key = PRIMARY_KEYS.get(name)
        for column in df.columns:
            if column == own_key or column not in FOREIGN_KEYS:
                continue
            dim_name, dim_key = FOREIGN_KEYS[column]
            valid = set(outputs[dim_name][dim_key])
            orphans = set(df[column].dropna()) - valid
            if orphans:
                raise ValueError(
                    f"{name}.{column} has {len(orphans)} value(s) with no matching row in "
                    f"{dim_name}.{dim_key}, e.g. {sorted(orphans)[:5]}"
                )

    unit_by_service = dim_service.set_index("service_key")["business_unit"]
    for name, df in outputs.items():
        if not name.startswith("fact_"):
            continue

        date_keys = [c for c in df.columns if c.endswith("date_key") or c == "date_key"]
        if not date_keys:
            raise ValueError(f"{name} must carry at least one date key into dim_date")

        if "service_key" not in df.columns:
            raise ValueError(f"{name} must include service_key for business-unit reporting")
        represented_units = set(df["service_key"].map(unit_by_service))
        if represented_units != TARGET_BUSINESS_UNITS:
            raise ValueError(
                f"{name} must cover {sorted(TARGET_BUSINESS_UNITS)}, "
                f"got {sorted(represented_units)}"
            )

        grain = FACT_GRAIN[name]
        missing = [c for c in grain if c not in df.columns]
        if missing:
            raise ValueError(f"{name} is missing grain column(s) {missing}")
        if df.duplicated(subset=grain).any():
            raise ValueError(f"{name} has duplicate rows at its declared grain {grain}")


def write_monthly_excel_style(fact_capacity, dim_date, dim_ci, out_dir):
    """A folder of monthly extracts - the 'large Excel files' pattern for Lab 0.

    Written as CSV so the generator has no Excel dependency. Column names and the
    inconsistencies are what matter: the November file is deliberately different.
    """
    os.makedirs(out_dir, exist_ok=True)
    for name in os.listdir(out_dir):
        if name.startswith("capacity_") and name.endswith(".csv"):
            os.remove(os.path.join(out_dir, name))

    merged = fact_capacity.merge(
        dim_date[["date_key", "month_year"]], on="date_key"
    ).merge(
        dim_ci[["ci_key", "ci_name", "environment"]], on="ci_key"
    )
    november_months = sorted(
        month for month in merged["month_year"].unique() if month.endswith("-11")
    )
    anomaly_month = november_months[-1] if november_months else None
    written = []
    for month_year, grp in merged.groupby("month_year"):
        out = grp[["ci_name", "environment", "cpu_utilization_pct", "memory_utilization_pct",
                   "storage_used_gb", "storage_allocated_gb"]].copy()
        out.columns = ["CI Name", "Environment", "CPU %", "Memory %", "Storage Used GB", "Storage Allocated GB"]
        # One month ships with a renamed column and a stray total row, so Lab 0's
        # schema guard has something real to catch.
        if month_year == anomaly_month:
            out = out.rename(columns={"CPU %": "CPU Utilisation %"})
            total = {c: None for c in out.columns}
            total["CI Name"] = "TOTAL"
            total["CPU Utilisation %"] = round(out["CPU Utilisation %"].mean(), 2)
            out = pd.concat([out, pd.DataFrame([total])], ignore_index=True)
        path = os.path.join(out_dir, f"capacity_{month_year.replace('-', '_')}.csv")
        out.to_csv(path, index=False)
        written.append(path)
    return written


# ---- shape 4: deliberately dirty exports ------------------------------------
#
# Every defect below is one a real export produces, and each maps to a specific
# Power Query transform. The catalogue and the fixes are in raw/dirty/README.md.

NBSP = "\u00a0"

DIRTY_DATE_FORMATS = ["%m/%d/%Y", "%Y-%m-%d", "%d-%b-%Y"]
DIRTY_ASSET_DATE_FORMATS = ["%Y-%m-%d", "%d-%b-%Y", "%B %d, %Y"]
DIRTY_NULL_TOKENS = ["N/A", "-", "", "NULL", "#N/A", "n/a"]
DIRTY_YES_NO = [("Yes", "No"), ("Y", "N"), ("TRUE", "FALSE"), ("1", "0"), ("yes", "no")]
DIRTY_LIFECYCLE_CASE = {
    "In Service": ["In Service", "in service", "IN-SERVICE", "InService", " In Service "],
    "In Stock": ["In Stock", "in stock", "IN STOCK"],
    "Pending Disposal": ["Pending Disposal", "pending disposal", "Pending-Disposal"],
    "Retired": ["Retired", "retired", "RETIRED"],
}


def _thousands(value) -> str:
    """1204 -> '1,204'. The separator is what makes Power Query read it as text."""
    return f"{int(value):,}"


def _money(value: float, style: int) -> str:
    """Currency as text, in the four styles a finance export actually emits."""
    if style == 0:
        return f"${value:,.2f}"
    if style == 1:
        return f"USD {value:,.2f}"
    if style == 2:
        # Accounting negative. Power Query reads the brackets as text, not a minus.
        return f"({value:,.2f})"
    return f"{value:,.2f} "


def _write_csv(path: str, rows) -> None:
    with open(path, "w", newline="", encoding="utf-8-sig") as handle:
        csv.writer(handle).writerows(rows)


def write_dirty_incident_export(out_dir, fact_incident, dim_date, dim_service,
                                dim_location, dim_severity, sample_rows=300):
    """A ServiceNow-style export: junk preamble, mixed formats, dupes, footer."""
    joined = (
        fact_incident
        .merge(dim_date[["date_key", "date"]], on="date_key")
        .merge(dim_service[["service_key", "service_name"]], on="service_key")
        .merge(dim_location[["location_key", "site_name", "state_province"]], on="location_key")
        .merge(dim_severity[["severity_key", "severity_code"]], on="severity_key")
        .sort_values("incident_key")
        .head(sample_rows)
        .reset_index(drop=True)
    )

    rows = [
        ["ServiceNow Incident Export"],
        ["Report run:", "2026-08-17 06:00:12"],
        ["Filter:", "Opened last 90 days | State: All"],
        [],
        # Header row 5. Note the trailing spaces and the shouting.
        ["Incident Number ", " Opened Date", "SERVICE", "Site / State", "SEVERITY",
         "Category", "Resolve Minutes", "SLA Met", "Reassignments", "Notes"],
    ]

    data_rows = []
    for i, inc in enumerate(joined.itertuples(index=False)):
        opened = pd.Timestamp(inc.date).to_pydatetime()
        date_text = opened.strftime(DIRTY_DATE_FORMATS[i % len(DIRTY_DATE_FORMATS)])

        severity_variants = [
            inc.severity_code, inc.severity_code.lower(), inc.severity_code.title(),
            f" {inc.severity_code}", f"{inc.severity_code} ",
        ]

        is_open = pd.isna(inc.time_to_resolve_minutes)
        if is_open:
            minutes_text = DIRTY_NULL_TOKENS[i % 3]
            yes, no = DIRTY_YES_NO[i % len(DIRTY_YES_NO)]
            sla_text = ""
        else:
            minutes_text = _thousands(inc.time_to_resolve_minutes)
            yes, no = DIRTY_YES_NO[i % len(DIRTY_YES_NO)]
            sla_text = yes if inc.sla_met_flag else no

        data_rows.append([
            f"{inc.incident_number} ",
            date_text,
            f"{inc.service_name} " if i % 4 == 0 else inc.service_name,
            f"{inc.site_name} / {inc.state_province}",
            severity_variants[i % len(severity_variants)],
            inc.category,
            minutes_text,
            sla_text,
            str(inc.reassignment_count),
            "",  # Notes is empty on every row. A whole column of nothing.
        ])

    # Blank rows and exact duplicates, scattered the way an append job leaves them.
    padded = []
    for i, row in enumerate(data_rows):
        padded.append(row)
        if i > 0 and i % 47 == 0:
            padded.append([])
        if i > 0 and i % 61 == 0:
            padded.append(list(row))

    rows.extend(padded)

    resolved_total = int(
        joined["time_to_resolve_minutes"].dropna().sum()
    )
    rows.extend([
        [],
        ["TOTAL", "", "", "", "", "", _thousands(resolved_total), "", "", ""],
        ["Generated by ServiceNow export utility v4.2 - do not edit"],
        ["Confidential - Internal Use Only"],
    ])

    path = os.path.join(out_dir, "incident_export_dirty.csv")
    _write_csv(path, rows)
    return path, f"{len(data_rows):,} incidents + preamble, dupes, footer"


def write_dirty_capacity_crosstab(out_dir, fact_capacity, dim_date, dim_service, dim_ci,
                                  max_months=12, max_cis=24):
    """A cross-tab: months across the columns. Needs Unpivot and Fill Down."""
    joined = (
        fact_capacity
        .merge(dim_date[["date_key", "month_year"]], on="date_key")
        .merge(dim_ci[["ci_key", "ci_name"]], on="ci_key")
        .merge(dim_service[["service_key", "service_name", "business_unit"]], on="service_key")
    )
    months = sorted(joined["month_year"].unique())[-max_months:]
    joined = joined[joined["month_year"].isin(months)]

    pivot = joined.pivot_table(
        index=["business_unit", "service_name", "ci_name"],
        columns="month_year",
        values="cpu_utilization_pct",
        aggfunc="mean",
    ).reset_index()
    pivot = pivot.sort_values(["business_unit", "service_name", "ci_name"]).head(max_cis)

    def month_header(month_year: str) -> str:
        stamp = pd.Timestamp(month_year + "-01")
        return stamp.strftime("%b-%Y")

    rows = [
        ["Capacity Utilisation by Month - CPU %"],
        ["Source:", "CapacityIQ nightly export"],
        [],
        ["Business Unit", "Service", "CI Name"] + [month_header(m) for m in months] + ["Total"],
    ]

    last_unit = None
    last_service = None
    for i in range(len(pivot)):
        record = pivot.iloc[i]
        # Reference month columns by name, never by tuple position.
        values = [record[m] for m in months]
        # Repeated group labels are blanked out, the way a report writer emits
        # them. Fill Down is the fix.
        unit_cell = record["business_unit"] if record["business_unit"] != last_unit else ""
        service_cell = record["service_name"] if record["service_name"] != last_service else ""
        last_unit, last_service = record["business_unit"], record["service_name"]

        cells = []
        for j, value in enumerate(values):
            # One gap per handful of rows, so the exercise has a null to handle.
            if (i + j) % 37 == 0 or pd.isna(value):
                cells.append("n/a")
            else:
                cells.append(f"{value:.1f}%")
        present = [v for v in values if not pd.isna(v)]
        average = f"{sum(present) / len(present):.1f}%" if present else "n/a"
        rows.append([unit_cell, service_cell, record["ci_name"]] + cells + [average])

    grand = [f"{float(pivot[m].mean()):.1f}%" for m in months]
    rows.append(["Grand Total", "", ""] + grand + [""])

    path = os.path.join(out_dir, "capacity_by_month_crosstab.csv")
    _write_csv(path, rows)
    return path, f"{len(pivot):,} CIs x {len(months)} month columns, cross-tab"


def write_dirty_asset_inventory(out_dir, fact_asset, dim_ci, dim_location, max_rows=250):
    """An asset register: currency as text, three date formats, split-me location."""
    joined = (
        fact_asset
        .merge(dim_ci[["ci_key", "ci_name"]], on="ci_key")
        .merge(dim_location[["location_key", "city", "state_province", "country"]], on="location_key")
        .sort_values("asset_key")
        .head(max_rows)
        .reset_index(drop=True)
    )

    rows = [[
        "Asset Tag", "CI Name", "Location", "Purchase Date", "Warranty End",
        "Lifecycle Status", "Acquisition Cost", "Annual Support Cost", "Under Warranty",
    ]]

    data_rows = []
    for i, asset in enumerate(joined.itertuples(index=False)):
        purchase_fmt = DIRTY_ASSET_DATE_FORMATS[i % len(DIRTY_ASSET_DATE_FORMATS)]
        warranty_fmt = DIRTY_ASSET_DATE_FORMATS[(i + 1) % len(DIRTY_ASSET_DATE_FORMATS)]

        # Asset tags arrive padded, or with the Excel text-marker apostrophe, or
        # with a non-breaking space that Trim alone will not remove.
        tag_style = i % 4
        if tag_style == 0:
            tag = f" {asset.asset_tag} "
        elif tag_style == 1:
            tag = f"'{asset.asset_tag}"
        elif tag_style == 2:
            tag = f"{asset.asset_tag}{NBSP}"
        else:
            tag = asset.asset_tag

        support_style = i % 4
        support_value = asset.annual_support_cost_usd
        if support_style == 2:
            support_value = -support_value  # a credit note, shown in brackets
        support_text = _money(abs(support_value), support_style)

        yes, no = DIRTY_YES_NO[i % len(DIRTY_YES_NO)]
        warranty_text = yes if asset.is_under_warranty else no

        # A CMDB with holes is the point of the cmdb_complete_flag. Acquisition
        # cost is never a credit, so it never uses the bracketed style.
        acquisition_styles = [0, 1, 3]
        cost_text = (
            _money(asset.acquisition_cost_usd, acquisition_styles[i % len(acquisition_styles)])
            if asset.cmdb_complete_flag
            else DIRTY_NULL_TOKENS[i % len(DIRTY_NULL_TOKENS)]
        )

        variants = DIRTY_LIFECYCLE_CASE[asset.lifecycle_status]
        data_rows.append([
            tag,
            asset.ci_name,
            f"{asset.city}, {asset.state_province}, {asset.country}",
            pd.Timestamp(asset.purchase_date).strftime(purchase_fmt),
            pd.Timestamp(asset.warranty_end_date).strftime(warranty_fmt),
            variants[i % len(variants)],
            cost_text,
            support_text,
            warranty_text,
        ])

    # Six exact duplicates. Remove Duplicates has to run on the full row, because
    # the tag column is inconsistently padded.
    for i in range(0, len(data_rows), max(1, len(data_rows) // 6)):
        data_rows.append(list(data_rows[i]))

    rows.extend(data_rows)
    rows.extend([
        [],
        ["Extracted from AssetCenter on 2026-08-17. Costs in USD unless stated."],
    ])

    path = os.path.join(out_dir, "asset_inventory_dirty.csv")
    _write_csv(path, rows)
    return path, f"{len(data_rows):,} rows, currency + dates as text"


def write_dirty_service_desk(out_dir, fact_service_desk, dim_date, dim_team,
                             dim_location, max_rows=120):
    """A two-row header. Transpose, fill down, merge, transpose back, promote."""
    joined = (
        fact_service_desk
        .merge(dim_date[["date_key", "date"]], on="date_key")
        .merge(dim_team[["team_key", "team_name"]], on="team_key")
        .merge(dim_location[["location_key", "site_name"]], on="location_key")
    )
    daily = (
        joined
        .groupby(["date", "team_name", "site_name"], as_index=False)
        .agg({
            "tickets_received": "sum",
            "tickets_resolved": "sum",
            "first_contact_resolved": "sum",
            "agents_scheduled": "sum",
            "agents_available": "sum",
            "avg_handle_time_minutes": "mean",
        })
        .sort_values(["date", "team_name", "site_name"])
        .tail(max_rows)
        .reset_index(drop=True)
    )

    rows = [
        # Row 1 groups the columns. Row 2 names them. Neither is usable alone.
        ["", "", "", "Tickets", "", "", "Staffing", "", "Quality", ""],
        ["Date", "Team", "Site", "Received", "Resolved", "First Contact",
         "Scheduled", "Available", "Avg Handle (min)", "Notes"],
    ]

    for i, row in enumerate(daily.itertuples(index=False)):
        received = _thousands(row.tickets_received)
        resolved = _thousands(row.tickets_resolved)
        # A dash where a zero belongs. Convert to Whole Number and it errors.
        fcr = "-" if i % 29 == 0 else _thousands(row.first_contact_resolved)
        rows.append([
            pd.Timestamp(row.date).strftime("%d-%b-%Y"),
            row.team_name,
            row.site_name,
            f"{received} " if i % 3 == 0 else received,
            resolved,
            fcr,
            str(row.agents_scheduled),
            str(row.agents_available),
            f"{row.avg_handle_time_minutes:.1f}",
            "",  # Notes. Empty on every row, courtesy of the export template.
        ])

    rows.append([
        "Totals", "", "",
        _thousands(daily["tickets_received"].sum()),
        _thousands(daily["tickets_resolved"].sum()),
        _thousands(daily["first_contact_resolved"].sum()),
        "", "", "", "",
    ])

    path = os.path.join(out_dir, "service_desk_daily_dirty.csv")
    _write_csv(path, rows)
    return path, f"{len(daily):,} rows, two-row header, totals row"


def write_dirty_files(out_dir, fact_incident, fact_capacity, fact_asset,
                      fact_service_desk, dim_date, dim_service, dim_ci, dim_team,
                      dim_location, dim_severity):
    """Shape 4: exports that need cleaning before they can be modelled."""
    os.makedirs(out_dir, exist_ok=True)
    for name in os.listdir(out_dir):
        if name.endswith("_dirty.csv") or name.endswith("_crosstab.csv"):
            os.remove(os.path.join(out_dir, name))

    return [
        write_dirty_incident_export(
            out_dir, fact_incident, dim_date, dim_service, dim_location, dim_severity
        ),
        write_dirty_capacity_crosstab(out_dir, fact_capacity, dim_date, dim_service, dim_ci),
        write_dirty_asset_inventory(out_dir, fact_asset, dim_ci, dim_location),
        write_dirty_service_desk(out_dir, fact_service_desk, dim_date, dim_team, dim_location),
    ]


def main() -> None:
    ap = argparse.ArgumentParser(
        description="Generate synthetic Banking and Capital Markets I&O workshop data."
    )
    ap.add_argument("--months", type=int, default=24, help="Months of history to generate (default 24).")
    ap.add_argument("--ci-count", type=int, default=400, help="Number of configuration items (default 400).")
    args = ap.parse_args()
    if args.months < 1:
        ap.error("--months must be at least 1")
    if args.ci_count < 1:
        ap.error("--ci-count must be at least 1")

    rng = np.random.default_rng(SEED)

    end = date.today().replace(day=1) - timedelta(days=1)
    start_month_index = end.year * 12 + end.month - 1 - (args.months - 1)
    start = date(start_month_index // 12, start_month_index % 12 + 1, 1)

    # dim_date has to span more than the reporting window, because fact_asset
    # keys into it on purchase and warranty-end dates. Whole calendar years,
    # which Mark as Date Table requires anyway.
    calendar_start = date(
        (end - timedelta(days=ASSET_PURCHASE_MAX_DAYS_AGO)).year, 1, 1
    )
    calendar_end = date(
        (end + timedelta(days=max(ASSET_WARRANTY_TERM_DAYS))).year, 12, 31
    )

    sql_dir = os.path.join(RAW, "sql")
    tableau_dir = os.path.join(RAW, "tableau_extract")
    excel_dir = os.path.join(RAW, "excel")
    dirty_dir = os.path.join(RAW, "dirty")
    for d in (sql_dir, tableau_dir, excel_dir, dirty_dir):
        os.makedirs(d, exist_ok=True)

    print(
        f"Generating {args.months} months of synthetic Banking and Capital Markets "
        f"I&O data ({start} to {end})..."
    )

    dim_date = build_dim_date(calendar_start, calendar_end, start, end)
    dim_service = build_dim_service()
    dim_team = build_dim_team()
    dim_location = build_dim_location()
    dim_severity = build_dim_severity()

    required_ci = min_ci_count(dim_service)
    if args.ci_count < required_ci:
        ap.error(
            f"--ci-count must be at least {required_ci} so every service, and the "
            f"mainframe and capacity facts, reach both business units"
        )
    dim_ci = build_dim_configuration_item(
        rng, args.ci_count, dim_service, dim_location, dim_team
    )

    # Event facts only cover the reporting window, not the whole date dimension.
    reporting_days = dim_date[dim_date["is_reporting_period"]].reset_index(drop=True)

    fact_incident = build_fact_incident(
        rng, reporting_days, dim_service, dim_ci, dim_team, dim_location, dim_severity
    )
    fact_capacity = build_fact_capacity(rng, reporting_days, dim_ci, dim_service)
    fact_mainframe = build_fact_mainframe(rng, reporting_days, dim_ci, dim_service)
    fact_service_desk = build_fact_service_desk(
        rng, reporting_days, dim_service, dim_team, dim_location
    )
    fact_asset = build_fact_asset(rng, dim_ci, end, calendar_start, calendar_end)

    dim_service_out = dim_service.drop(columns=["base_rate"])

    outputs = {
        "dim_date.csv": dim_date,
        "dim_service.csv": dim_service_out,
        "dim_team.csv": dim_team,
        "dim_location.csv": dim_location,
        "dim_severity.csv": dim_severity,
        "dim_configuration_item.csv": dim_ci,
        "fact_incident.csv": fact_incident,
        "fact_capacity.csv": fact_capacity,
        "fact_mainframe.csv": fact_mainframe,
        "fact_service_desk.csv": fact_service_desk,
        "fact_asset.csv": fact_asset,
    }
    validate_dataset(outputs)

    for name, df in outputs.items():
        df.to_csv(os.path.join(sql_dir, name), index=False)
        print(f"  raw/sql/{name:<32} {len(df):>8,} rows")

    extract = build_tableau_extract(
        fact_incident, dim_date, dim_service, dim_ci, dim_team, dim_location, dim_severity
    )
    extract_path = os.path.join(tableau_dir, "incident_report_extract.csv")
    extract.to_csv(extract_path, index=False)
    print(f"  raw/tableau_extract/incident_report_extract.csv  {len(extract):>8,} rows "
          f"({len(extract.columns)} columns, denormalized)")

    monthly = write_monthly_excel_style(fact_capacity, dim_date, dim_ci, excel_dir)
    print(f"  raw/excel/capacity_YYYY_MM.csv                   {len(monthly):>8,} monthly files")

    dirty = write_dirty_files(
        dirty_dir, fact_incident, fact_capacity, fact_asset, fact_service_desk,
        dim_date, dim_service, dim_ci, dim_team, dim_location, dim_severity,
    )
    for path, note in dirty:
        print(f"  raw/dirty/{os.path.basename(path):<38} {note}")

    print("\nDone. Next: labs/day-1-setup/README.md")


if __name__ == "__main__":
    main()
