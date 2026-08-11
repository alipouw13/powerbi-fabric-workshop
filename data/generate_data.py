"""Generate synthetic Banking and Capital Markets I&O data for the Schwab
Tableau-to-Power BI workshop.

The workshop teaches a Tableau audience how to move to Power BI, using Schwab's
own **Infrastructure & Operations (I&O)** domains. The model follows the star
schema on deck slides 9 and 10: one fact table per domain, all joining the same
conformed dimensions.

Every organization, service, identifier, event, and metric is SYNTHETIC. No real
Schwab, customer, account, position, trade, or market data is used.

Shapes written, on purpose, so the migration story lands:

  1. raw/tableau_extract/incident_report_extract.csv
     One wide, denormalized table - the way a Tableau .hyper extract looks
     today. This is the "before" that Lab 4 reshapes.

  2. raw/sql/*.csv
     Normalized conformed dimensions plus a fact table per domain - the "after".
     These stand in for the SQL Server views you would reach through the
     on-premises data gateway.

  3. raw/excel/capacity_YYYY_MM.csv
     A folder of monthly extracts, the "large Excel files" pain point. Lab 4
     combines these with a single query and a custom function.

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
    ("Westlake Campus", "Westlake", "TX", "Southwest", "DC-DFW-01"),
    ("Austin Tech Center", "Austin", "TX", "Southwest", "DC-DFW-01"),
    ("Phoenix Operations", "Phoenix", "AZ", "West", "DC-PHX-01"),
    ("Denver Office", "Denver", "CO", "West", "DC-PHX-01"),
    ("Lone Tree Campus", "Lone Tree", "CO", "West", "DC-PHX-01"),
    ("Indianapolis Hub", "Indianapolis", "IN", "Midwest", "DC-CHI-01"),
    ("Orlando Service Center", "Orlando", "FL", "Southeast", "DC-ATL-01"),
    ("Richfield Office", "Richfield", "OH", "Midwest", "DC-CHI-01"),
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


def build_dim_date(start: date, end: date) -> pd.DataFrame:
    days = pd.date_range(start, end, freq="D")
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
    # Schwab-style fiscal year aligned to the calendar year for workshop simplicity.
    df["fiscal_year"] = df["year"]
    df["fiscal_quarter"] = df["quarter"]
    return df[[
        "date_key", "date", "year", "quarter", "month", "month_name", "month_year",
        "day_of_month", "day_of_week", "day_name", "is_weekend", "week_of_year",
        "fiscal_year", "fiscal_quarter",
    ]]


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


def build_dim_configuration_item(rng, n_ci, dim_service, dim_location) -> pd.DataFrame:
    ci_types = _weighted(rng, CI_TYPES, n_ci)
    envs = _weighted(rng, ENVIRONMENTS, n_ci)
    crits = _weighted(rng, CRITICALITY, n_ci)
    service_keys = rng.integers(1, len(dim_service) + 1, n_ci)
    location_keys = rng.integers(1, len(dim_location) + 1, n_ci)

    prefix = {
        "Server": "SRV", "Database": "DB", "Application": "APP", "Network Device": "NET",
        "Storage Array": "STG", "Mainframe LPAR": "LPAR", "Load Balancer": "LB",
        "Virtual Machine": "VM",
    }
    rows = []
    for i in range(n_ci):
        t = ci_types[i]
        rows.append({
            "ci_key": i + 1,
            "ci_id": f"CI{i + 1:05d}",
            "ci_name": f"{prefix[t]}-{envs[i][:3].upper()}-{i + 1:04d}",
            "ci_type": t,
            "environment": envs[i],
            "criticality": crits[i],
            "service_key": int(service_keys[i]),
            "location_key": int(location_keys[i]),
            "support_group": random.choice([t[0] for t in TEAMS]),
        })
    return pd.DataFrame(rows)


def build_fact_incident(rng, dim_date, dim_service, dim_ci, dim_team, dim_location, dim_severity):
    """One row per incident. This is the primary fact for Labs 1 to 4."""
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


def build_fact_capacity(rng, dim_date, dim_ci):
    """Daily utilization per infrastructure CI. Capacity & Forecasting domain."""
    infra = dim_ci[dim_ci["ci_type"].isin(["Server", "Storage Array", "Virtual Machine", "Database"])]
    infra = infra.sample(n=min(120, len(infra)), random_state=SEED)
    # Monthly grain keeps the file small enough for a workshop laptop.
    month_starts = dim_date[dim_date["day_of_month"] == 1]

    rows = []
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
                "date_key": int(drow.date_key),
                "ci_key": int(ci.ci_key),
                "service_key": int(ci.service_key),
                "location_key": int(ci.location_key),
                "cpu_utilization_pct": round(max(2.0, cpu), 2),
                "memory_utilization_pct": round(max(4.0, mem), 2),
                "storage_allocated_gb": round(allocated, 2),
                "storage_used_gb": round(max(10.0, used), 2),
                "headroom_pct": round(max(0.0, 100 - max(cpu, mem)), 2),
            })
    return pd.DataFrame(rows)


def build_fact_mainframe(rng, dim_date, dim_ci):
    """Daily MIPS and batch metrics per LPAR. Mainframe Performance domain."""
    lpars = dim_ci[dim_ci["ci_type"] == "Mainframe LPAR"]
    if lpars.empty:
        lpars = dim_ci.head(6)

    rows = []
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
                "date_key": int(drow.date_key),
                "ci_key": int(lpar.ci_key),
                "service_key": int(lpar.service_key),
                "location_key": int(lpar.location_key),
                "mips_consumed": round(max(10.0, mips), 2),
                "mips_capacity": capacity,
                "batch_jobs_completed": int(max(0, rng.normal(880 * month_end_boost, 90))),
                "batch_jobs_failed": int(max(0, rng.poisson(6 * month_end_boost))),
                "batch_window_minutes": batch_minutes,
                "transactions_processed": int(max(0, rng.normal(1_450_000 * month_end_boost, 180_000))),
            })
    return pd.DataFrame(rows)


def build_fact_service_desk(rng, dim_date, dim_service, dim_team, dim_location):
    """Daily ticket and staffing metrics. Service Desk & Workforce domain."""
    desk_teams = dim_team[dim_team["assignment_group"].str.contains("Service Desk")]
    if desk_teams.empty:
        desk_teams = dim_team.head(2)

    rows = []
    mean_service_rate = dim_service["base_rate"].mean()
    for drow in dim_date.itertuples(index=False):
        weekend_factor = 0.35 if drow.is_weekend else 1.0
        for team in desk_teams.itertuples(index=False):
            for loc_key in [1, 3, 6]:  # Westlake, Phoenix, Indianapolis staff the desk
                for service in dim_service.itertuples(index=False):
                    # Allocate workload by supported business service so every
                    # service-desk metric can roll up to the two focus units.
                    service_factor = service.base_rate / mean_service_rate
                    received = int(max(0, rng.normal(18 * service_factor * weekend_factor, 5)))
                    resolved = int(received * rng.uniform(0.82, 0.98))
                    fcr = int(resolved * rng.uniform(0.55, 0.78))
                    scheduled = int(max(1, rng.normal(2.2 * service_factor * weekend_factor, 0.7)))
                    rows.append({
                        "date_key": int(drow.date_key),
                        "service_key": int(service.service_key),
                        "team_key": int(team.team_key),
                        "location_key": loc_key,
                        "tickets_received": received,
                        "tickets_resolved": resolved,
                        "first_contact_resolved": fcr,
                        "calls_abandoned": int(max(0, rng.normal(received * 0.06, 1.5))),
                        "agents_scheduled": scheduled,
                        "agents_available": max(1, scheduled - int(rng.poisson(0.3))),
                        "avg_handle_time_minutes": round(float(max(1, rng.normal(11.5, 2.2))), 2),
                        "avg_speed_to_answer_seconds": round(float(max(5, rng.normal(48, 14))), 1),
                    })
    return pd.DataFrame(rows)


def build_fact_asset(rng, dim_ci, end: date):
    """One row per asset. Asset & CMDB domain."""
    rows = []
    for i, ci in enumerate(dim_ci.itertuples(index=False), start=1):
        purchased = end - timedelta(days=int(rng.integers(200, 2400)))
        warranty_end = purchased + timedelta(days=int(rng.choice([365, 730, 1095, 1825])))
        rows.append({
            "asset_key": i,
            "asset_tag": f"AST{i:06d}",
            "ci_key": int(ci.ci_key),
            "service_key": int(ci.service_key),
            "location_key": int(ci.location_key),
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


def validate_dataset(dim_service, outputs) -> None:
    """Fail generation when focus-unit vocabulary or service relationships drift."""
    actual_units = set(dim_service["business_unit"])
    if actual_units != TARGET_BUSINESS_UNITS:
        raise ValueError(
            f"Expected business units {sorted(TARGET_BUSINESS_UNITS)}, got {sorted(actual_units)}"
        )

    service_keys = set(dim_service["service_key"])
    unit_by_service = dim_service.set_index("service_key")["business_unit"]
    for name, df in outputs.items():
        if not name.startswith("fact_"):
            continue
        if "service_key" not in df.columns:
            raise ValueError(f"{name} must include service_key for business-unit reporting")
        missing = set(df["service_key"].dropna()) - service_keys
        if missing:
            raise ValueError(f"{name} contains unknown service keys: {sorted(missing)}")
        represented_units = set(df["service_key"].map(unit_by_service))
        if represented_units != TARGET_BUSINESS_UNITS:
            raise ValueError(
                f"{name} must cover {sorted(TARGET_BUSINESS_UNITS)}, "
                f"got {sorted(represented_units)}"
            )


def write_monthly_excel_style(fact_capacity, dim_date, dim_ci, out_dir):
    """A folder of monthly extracts - the 'large Excel files' pattern for Lab 4.

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
        # One month ships with a renamed column and a stray total row, so Lab 4's
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

    random.seed(SEED)
    rng = np.random.default_rng(SEED)

    end = date.today().replace(day=1) - timedelta(days=1)
    start_month_index = end.year * 12 + end.month - 1 - (args.months - 1)
    start = date(start_month_index // 12, start_month_index % 12 + 1, 1)

    sql_dir = os.path.join(RAW, "sql")
    tableau_dir = os.path.join(RAW, "tableau_extract")
    excel_dir = os.path.join(RAW, "excel")
    for d in (sql_dir, tableau_dir, excel_dir):
        os.makedirs(d, exist_ok=True)

    print(
        f"Generating {args.months} months of synthetic Banking and Capital Markets "
        f"I&O data ({start} to {end})..."
    )

    dim_date = build_dim_date(start, end)
    dim_service = build_dim_service()
    dim_team = build_dim_team()
    dim_location = build_dim_location()
    dim_severity = build_dim_severity()
    dim_ci = build_dim_configuration_item(rng, args.ci_count, dim_service, dim_location)

    fact_incident = build_fact_incident(rng, dim_date, dim_service, dim_ci, dim_team, dim_location, dim_severity)
    fact_capacity = build_fact_capacity(rng, dim_date, dim_ci)
    fact_mainframe = build_fact_mainframe(rng, dim_date, dim_ci)
    fact_service_desk = build_fact_service_desk(
        rng, dim_date, dim_service, dim_team, dim_location
    )
    fact_asset = build_fact_asset(rng, dim_ci, end)

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
    validate_dataset(dim_service_out, outputs)

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

    print("\nDone. Next: labs/lab-00-setup-and-gateway/README.md")


if __name__ == "__main__":
    main()
