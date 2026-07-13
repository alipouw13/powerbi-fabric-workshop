# Rayfin on Fabric for the Contoso Claims Intake app

Rayfin is a fully managed Backend-as-a-Service that runs on Microsoft Fabric.
You define a data model with TypeScript decorators. Rayfin provisions and
manages Database, Authentication, Data APIs, Storage, and Hosting.

## Workshop connection

- App skeleton: ../rayfin-app/README.md
- Lab: ../labs/lab-11-rayfin-insurance-app/README.md
- Rayfin sources: https://aka.ms/rayfin/docs, https://github.com/microsoft/rayfin, and sources.md#rayfin

## Why Rayfin belongs in a Fabric workshop

| Fabric need | Rayfin answer |
| --- | --- |
| Build an app next to governed data | Rayfin runs on Fabric and inherits Fabric governance, access control, and security. |
| Avoid custom backend plumbing | Rayfin manages database, auth, APIs, storage, and hosting. |
| Keep app data modeled | Entities are defined in TypeScript with decorators. |
| Teach security in app and BI | Rayfin `@role` row-level policy parallels Power BI RLS. |
| Demo Day 3 application patterns | Claims Intake shows how an operational app can sit beside analytics. |

## Services configured by Rayfin

| Service | Workshop meaning |
| --- | --- |
| Database | Stores app entities such as Customer, Policy, and Claim. |
| Authentication | Supports Fabric brokered auth and password auth in configuration. |
| Data APIs | Exposes typed data access through generated APIs. |
| Storage | Supports app file and object scenarios. |
| Hosting | Serves the app from a static build folder. |

## Decorator pattern

Rayfin models use decorators from `@microsoft/rayfin-core`.

| Decorator | Purpose |
| --- | --- |
| `@entity` | Marks a TypeScript class as a persisted entity. |
| `@authenticated('*')` | Requires authenticated access. |
| `@role(...)` | Defines role-based policy, including row-level rules. |
| `@uuid` | Defines an identifier field. |
| `@text({ min, max, optional })` | Defines text constraints. |
| `@int` | Defines an integer field. |
| `@boolean` | Defines a boolean field. |
| `@date` | Defines a date field. |
| `@set(...)` | Defines allowed values. |
| `@one(() => X)` | Defines a one-to-one or many-to-one relationship. |
| `@many(() => X)` | Defines a one-to-many relationship. |

`schema.ts` registers entities so Rayfin can provision and apply the model.

## Policy entity example with row-level security

This example shows the teaching parallel: Rayfin `@role` RLS protects rows in
the app, just as Power BI RLS protects rows in the semantic model.

```ts
import {
  authenticated,
  date,
  entity,
  one,
  role,
  set,
  text,
  uuid,
} from "@microsoft/rayfin-core";
import { Agent } from "./agent";
import { Customer } from "./customer";

@entity
@authenticated("*")
@role("authenticated", "write", {
  policy: (claims, item) => claims.sub.eq(item.agentUserId),
})
export class Policy {
  @uuid id!: string;
  @text({ min: 4, max: 32 }) policyNumber!: string;
  @set("Auto", "Home", "Renters", "Life", "Umbrella") product!: string;
  @set("Northeast", "Southeast", "Midwest", "Southwest", "West") region!: string;
  @text({ min: 1, max: 128 }) agentUserId!: string;
  @date effectiveDate!: Date;
  @one(() => Customer) customer!: Customer;
  @one(() => Agent) agent!: Agent;
}
```

## Configuration pattern

`rayfin.yml` configures the Fabric services that Rayfin manages.

```yaml
auth:
  - fabric
  - password
data:
  dialect: mssql
staticHosting:
  folder: dist
buildCommand: npm run build:fabric
```

## CLI workflow

| Step | Command | Result |
| --- | --- | --- |
| Scaffold | `npm create @microsoft/rayfin@latest` | Creates a starter Rayfin app. |
| Deploy | `npm run rayfin:up` | Runs `rayfin up` to deploy services. |
| Re-apply model | `npm run rayfin:db` | Runs `rayfin up db apply` after model changes. |
| Use client | `RayfinClient<Schema>` | Connects with `baseUrl` and `publishableKey`. |

## Fabricator workflow

The Fabricator is the agent-driven workflow for Rayfin. The presenter describes
the app, and the workflow builds, deploys, and validates the running app in a
Fabric test workspace. There is no local backend or dev server in the loop.
Use Fabricator when the lesson is "describe the business app and let the
platform assemble it." Use the CLI when the lesson is "developers control the
model, deploy, and test changes directly."

## Key npm packages

Core Rayfin packages named in this workshop: `@microsoft/rayfin-core`,
`@microsoft/rayfin-client`, `@microsoft/rayfin-cli`, `@microsoft/rayfin-data`,
`@microsoft/rayfin-auth`, `@microsoft/rayfin-auth-provider-fabric`,
`@microsoft/rayfin-functions`, `@microsoft/rayfin-storage`,
`@microsoft/rayfin-mcp`, and `@microsoft/fabric-embedded-host`.

## Contoso Claims Intake mapping

| Entity | Purpose | BI parallel |
| --- | --- | --- |
| Customer | Claimant or policyholder profile. | `dim_customer` |
| Agent | Producer and agency ownership. | `dim_agent` |
| Policy | Product, region, channel, customer, agent, and book rules. | `dim_policy` |
| Claim | Intake status, severity, reserve, and paid amount. | `fact_claim` and `ops/claims_intake.csv` |

The "my book" policy in Rayfin should mirror the Power BI RLS story: agents see
only the policies and claims they are allowed to service.
