# On-premises data gateway: install, configure, and operate

The gateway is the bridge between Power BI in the cloud and Schwab's SQL Server
sources on-premises. Deck slide 7 puts it in the **Now** column, and slide 8 says
`Import-mode refresh runs through the on-premises data gateway`. Every scheduled
refresh in this workshop depends on it working.

This page is the detail behind [Lab 0](../labs/lab-00-setup-and-gateway/README.md).

> **Who does what.** At Schwab the gateway is centrally managed. Most attendees
> will **not** install a gateway or create a data source themselves - they will
> request one. Read this anyway: the fastest way to get an unblocked refresh is
> to arrive at the conversation knowing exactly what to ask for.

---

## 1. Which gateway do you need

| | **Standard mode** (on-premises data gateway) | **Personal mode** |
| --- | --- | --- |
| Who can use it | Shared across users and reports | The installing user only |
| Runs as | A Windows service, survives sign-out | The user's session |
| Supports | Power BI, Power Apps, Power Automate, Logic Apps, Analysis Services | Power BI only |
| DirectQuery | Yes | **No - Import refresh only** |
| Right answer for Schwab | **Yes, this one** | Never, for shared content |

There is also a **virtual network (VNet) data gateway** - a managed gateway for
Azure sources reachable over a VNet. It needs no installed machine, but it does
not reach on-premises SQL Server, so it is not the option here.

**Decision for this workshop: standard mode, installed on a server, managed by
the platform team.**

---

## 2. Where to install it

Get this wrong and every refresh is slow for the life of the model.

| Requirement | Guidance |
| --- | --- |
| Machine | A dedicated server, not a laptop. It must be on and connected 24/7. |
| OS | Windows Server 2019 or later, 64-bit |
| Spec | 8 cores / 8 GB RAM minimum for real workloads. Refresh is memory-hungry. |
| Placement | **Physically close to the data source.** The gateway-to-SQL hop is where refresh time is won or lost. |
| Domain | Joined to the same domain as the SQL sources, so Windows auth works |
| Not on | A domain controller, or the same box as SQL Server under memory pressure |

Outbound connectivity: the gateway needs outbound HTTPS (443) to Azure Service
Bus. It does **not** need any inbound firewall rule opened, which is usually the
detail that unblocks a security review.

---

## 3. Install and register

1. Download the standard gateway installer from
   `https://powerbi.microsoft.com/gateway/`.
2. Run it on the target server. Accept the path, choose **On-premises data
   gateway (recommended)**, not personal mode.
3. Sign in with a **service account**, not a personal account. When the person
   who registered the gateway leaves, a personally-registered gateway leaves with
   them.
4. Choose **Register a new gateway on this computer**.
5. Name it to a convention: `SCHWAB-IO-GW-PROD-01`. The name appears in every
   dataset's settings, so make it say something.
6. Set a **recovery key**. Store it in the team's secrets vault immediately.
   - You cannot recover it later.
   - You need it to restore the gateway on another machine, or to add a second
     gateway to the same cluster.
7. Add the gateway to a **cluster** (or create one). A single-member cluster is
   fine on day one, but the option only exists at registration - retro-fitting it
   means re-registering.

**High availability:** install a second gateway on a second server and join it to
the same cluster with the recovery key. Traffic distributes across online
members. Do this before the first production model, not after the first outage.

---

## 4. Create the data source

Done once per source, in the Power BI service, by a gateway admin.

1. **Settings** (gear) → **Manage connections and gateways**.
2. **Connections** tab → **New**.
3. Fill in:

| Field | Value for this workshop |
| --- | --- |
| Gateway cluster | `SCHWAB-IO-GW-PROD-01` |
| Connection name | `SQL-IO-ITSM-PROD` - name the source, not the report |
| Connection type | SQL Server |
| Server | The SQL instance, exactly as typed in Power BI Desktop |
| Database | The database, exactly as typed in Power BI Desktop |
| Authentication | Windows (a service account) or Basic |
| Privacy level | **Organizational** for internal sources |

4. **Create**, and confirm it tests successfully.

> **The single most common failure.** The server and database strings must match
> what is in the .pbix **character for character**. `SQLPROD01` and
> `sqlprod01.schwab.com` are different data sources to the gateway, even though
> they resolve to the same box. If the model says "you don't have access to this
> gateway", check this first.

**Privacy levels** matter more than they look. If one query combines an
Organizational source with a Public one, the mashup engine may refuse to fold and
will buffer data in memory instead - turning a two-minute refresh into a twenty-
minute one. Keep sources at consistent, deliberate levels.

---

## 5. Grant access

Two separate permissions, and people routinely confuse them:

- **Gateway admin** - can create data sources and manage the cluster. Keep this
  to the platform team.
- **Connection user** - can bind a semantic model to this data source. This is
  what a report author needs.

Grant connection access to an **Entra security group**, never to individuals.
Individual grants are how gateway permissions rot.

On the connection → **Manage users** → add the group → role **Can use**.

---

## 6. Bind the semantic model and schedule refresh

Done by the report author, after publishing.

1. Workspace → the semantic model → **Settings**.
2. Expand **Gateway and cloud connections**.
3. The gateway cluster should appear with a green tick. Map each data source in
   the model to its gateway connection.
   - No green tick means step 4's string mismatch, or missing connection access.
4. Expand **Refresh** → **Configure a refresh schedule**:
   - Time zone first, before you pick times.
   - Up to 8 refreshes per day on Pro; 48 on a Fabric/Premium capacity.
   - Schedule **after** the source ETL lands, not on the hour out of habit.
   - Set **failure notifications** to a group mailbox, not one person.
5. Run **Refresh now** once and confirm it succeeds before you tell anyone the
   report is ready.

---

## 7. Troubleshooting, in the order to check

| Symptom | Check first |
| --- | --- |
| "You don't have access to this gateway" | Server/database string mismatch between .pbix and connection |
| Gateway shows offline | Windows service `PBIEgwService` running? Outbound 443 open? |
| Credentials failed after working for months | Service account password rotated or expired |
| Refresh times out | Query folding broken - see below. Then source indexes, then gateway RAM |
| Refresh slow only at month end | Source contention, not the gateway. Move the schedule |
| Works in Desktop, fails on refresh | Desktop uses your credentials; the gateway uses the service account. Grant the service account access to the source |
| One query in the model fails | Mixed privacy levels forcing a buffer |

**Folding is a gateway problem.** If a step breaks query folding, the gateway
pulls the whole table across the wire and processes it in memory on the gateway
server. That is the difference between a refresh that takes two minutes and one
that takes an hour. Check **View Native Query** in Power Query before blaming the
gateway - see [Lab 4](../labs/lab-04-power-query/README.md).

**Logs:** gateway app → **Diagnostics** → **Export logs**. Enable additional
logging only while investigating; it is verbose and it costs performance.

---

## 8. Operate it

- **Update monthly.** Microsoft ships a gateway update roughly monthly and
  supports only the last six versions. An unpatched gateway eventually stops
  working, always at an inconvenient moment.
- **Monitor the service account expiry** the way you would any other credential.
- **Watch the recovery key.** Losing it means rebuilding the cluster.
- **Review the connection list quarterly** and delete what nothing uses.
- **Alert on refresh failure**, do not rely on someone noticing a stale report.

---

## 9. What to ask for, if you cannot do this yourself

Most attendees will send a request rather than click these screens. Send this and
you will usually get it back in one round trip:

> Please create an on-premises data gateway connection with:
> - **Gateway cluster:** `<existing I&O cluster>`
> - **Connection name:** `SQL-IO-<domain>-<env>`
> - **Server:** `<exact string from my .pbix>`
> - **Database:** `<exact string from my .pbix>`
> - **Authentication:** Windows, service account `<account>`
> - **Privacy level:** Organizational
> - **Grant "Can use" to:** `<Entra security group>`
>
> Semantic model that will bind to it: `<workspace> / <model name>`.
> Refresh window requested: `<time and time zone>`, after `<upstream job>` completes.

---

## Related

- [Lab 0 - Setup and gateway](../labs/lab-00-setup-and-gateway/README.md)
- [Lab 4 - Power Query](../labs/lab-04-power-query/README.md) - folding, and why it decides refresh time
- [Current state and constraints](schwab-current-state.md)
- Microsoft Learn: `learn.microsoft.com/power-bi/connect-data/service-gateway-onprem`
