# Migration assessment worksheet

Fill this in before rebuilding any Tableau content in Power BI. The purpose is to
decide what to rebuild, what to consolidate, what to retire, and which semantic
model each survivor should point at.

This is the **Assess** and **Rationalize** work from
[migration-approaches.md](../reference/migration-approaches.md). Do it before you
open Power BI Desktop.

## Worksheet

| Workbook | Domain | Owner | Sheets | Data sources | Extract or Live | Complexity 1-5 | Business value 1-5 | 90-day views | Priority | Target semantic model | Approach | Notes |
| --- | --- | --- | ---: | --- | --- | ---: | ---: | ---: | --- | --- | --- | --- |
| Incident SLA Dashboard | ITSM | ITSM reporting owner | 12 | ServiceNow incident extract | Extract | 4 | 5 | 840 | P1 | `sm_io_itsm` | Rebuild | Tie out Total Incidents, SLA Met %, Avg Resolve Minutes by month, service and severity |
| Capacity Utilization | Capacity | Capacity planning owner | 6 | Monthly Excel folder | Extract | 3 | 4 | 210 | P1 | `sm_io_capacity` | Rebuild | Nov file renames CPU %, and carries a TOTAL row. Needs a schema guard |
| MIPS Trend | Mainframe | Mainframe ops owner | 4 | SMF summary table | Live | 3 | 4 |  | P2 | `sm_io_mainframe` | Rebuild | Confirm whether Live is a real requirement or a habit |
|  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |
|  |  |  |  |  |  |  |  |  |  |  |  |  |

Copy the empty rows. One row per Tableau workbook, no exceptions, including the
ones you already know you will retire. The retirement list is half the value of
this exercise.

## Complexity rubric

| Score | Description | Examples |
| --- | --- | --- |
| 1 | Simple | Few visuals, one clean source, almost no calculated fields |
| 2 | Low | Several sheets, basic filters, standard aggregations |
| 3 | Moderate | Multiple sources, calculated fields, moderate interactivity |
| 4 | High | LOD expressions, table calculations, RLS, complex layout |
| 5 | Very high | Many sources, custom extensions, heavy prep, daily operational dependence |

## Business value rubric

| Score | Description | Examples |
| --- | --- | --- |
| 1 | Low | Rarely opened, no clear owner, no decision attached |
| 2 | Limited | One small team, non-critical monitoring |
| 3 | Moderate | Monthly, or a single department lead |
| 4 | High | Weekly operational reviews, or drives a staffing or capacity decision |
| 5 | Critical | Executive, audit, incident bridge, or daily operational decision support |

Score value from usage and decision impact, not from how much effort went into
building it. Sunk cost is not business value.

## Priority rules

| Priority | Use when | Path |
| --- | --- | --- |
| P1 | High value and feasible in this wave | Rebuild, validate, certify |
| P2 | Important but blocked on model or data readiness | Sequence after the shared model gap closes |
| P3 | Low value, or duplicates something else | Consolidate or retire |
| Hold | Owner, source or requirement unclear | Resolve before any build starts |

## Approach options

| Approach | Definition | Use for |
| --- | --- | --- |
| Rebuild | Model in a star schema, then build the report | High-value workbooks carrying duplicated Tableau logic. The default |
| Re-platform | Recreate the report experience with minimal logic change | Simple workbooks already sitting on a governed, clean source |
| Consolidate | Replace several workbooks with one report or app | Duplicate service, site or team views |
| Retire | Archive and remove from navigation | Low use, no owner, or superseded |

**Do not port a bad model.** If the Tableau workbook is a wide extract with forty
calculated fields, rebuilding the model is faster than translating the
calculations, and the result is something you can certify.

## Data source assessment

For each source behind each workbook, capture:

- Source system, view or file path
- Refresh cadence, and the actual business need for that cadence
- Extract size and row count
- Live connection dependency, and whether it is a real requirement
- Credential owner
- Gateway requirement, and whether the data source already exists on the gateway
- Data classification and the sensitivity label it will need
- Known quality issues, including schema drift like the November capacity file
- Target: which `sm_io_<domain>` model will serve it

Two things that come up constantly in I&O:

- **Monthly file folders.** Confirm whether column names are stable across
  months. They usually are not. Plan for a schema guard.
- **"Live" that does not need to be live.** Most Tableau live connections in
  operational reporting exist because someone once wanted intraday data. Confirm
  the requirement before you carry DirectQuery into the new estate.

## Calculation assessment

For each workbook, list:

- Calculated fields
- LOD expressions (`FIXED`, `INCLUDE`, `EXCLUDE`)
- Table calculations (running sum, percent of total, lookup)
- Parameters
- Sets and groups
- Custom fiscal calendars
- Security filters
- Anything used by more than one workbook

**Anything used by more than one workbook is a shared DAX measure, not a
report-level calculation.** That list is the starting backlog for
[the measure library](../src/pbip/README.md).

Translation patterns are in
[tableau-to-powerbi.md](../reference/tableau-to-powerbi.md).

## Validation grain

Agree the tie-out grain with the business owner before you build, not after. A
number that matches at the total and not by month will be found by a stakeholder,
not by you.

| Measure | Tie-out grain | Compare against |
| --- | --- | --- |
| Total Incidents | Month, service, severity | Tableau extract and `fact_incident` |
| SLA Met % | Month, severity | Tableau workbook and the DAX measure |
| Avg Resolve Minutes | Severity, team | Tableau workbook and `fact_incident` |
| Avg CPU Utilization | Month, environment | Monthly Excel folder and `fact_capacity` |
| MIPS Utilization % | Month, LPAR | SMF summary and `fact_mainframe` |
| Tickets Received | Month, team, location | Service desk report and `fact_service_desk` |
| Total Assets | Site, lifecycle status | CMDB export and `fact_asset` |

Agree the tolerance too. "Within 0.5 percent, explained" is a workable standard.
"Exact" usually is not, because the Tableau extract and the source have different
cut-off times.

## Exit criteria for a workbook

Do not start building until every one of these is true:

- [ ] Owner has confirmed the replacement scope.
- [ ] Target `sm_io_<domain>` model is named.
- [ ] Priority and approach are assigned.
- [ ] Required calculations are mapped to DAX measures.
- [ ] Source, gateway and credential path are confirmed.
- [ ] RLS and sensitivity label needs are documented.
- [ ] Validation grain and tolerance are agreed with the owner.
- [ ] Cutover date and the Tableau retirement date are written down.

The last one is the one people skip, and it is why organizations end up running
both tools for three years.

## Related

- [Migration approaches](../reference/migration-approaches.md)
- [Tableau to Power BI](../reference/tableau-to-powerbi.md)
- [Endorsement and certification](endorsement-certification.md)
- [Workspace governance](workspace-governance.md)
- [Adoption roadmap](adoption-roadmap.md)
- [Dataset documentation](../data/README.md)
