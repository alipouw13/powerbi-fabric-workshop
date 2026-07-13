# Contoso Claims Intake - a Rayfin app for the workshop

A small **Contoso Insurance** claims-intake / agent portal built on
[Rayfin](https://github.com/microsoft/rayfin), the Backend-as-a-Service that runs
on Microsoft Fabric. You define the data model with TypeScript decorators; Rayfin
provisions and manages the **database, authentication, and data APIs** for you,
and deploys the app to a Fabric test workspace.

> This is the hands-on "build a data app on Fabric" artifact for the workshop.
> It complements the analytics labs: the operational data this app captures
> (policies, claims) lands in Fabric, exactly the kind of source the BI labs then
> model and report on. See [Lab 11](../labs/lab-11-rayfin-insurance-app/README.md).

## What's here

```text
rayfin-app/
  rayfin/
    rayfin.yml            Fabric service config (auth: Fabric, data: mssql, static hosting)
    data/
      schema.ts           Registers the four entities
      Customer.ts         Policyholder
      Agent.ts            Selling agent (userId links to a signed-in identity)
      Policy.ts           Written policy, with @role row-level security to "my book"
      Claim.ts            First-notice-of-loss claim against a policy
  package.json            Scripts: rayfin:up (deploy), rayfin:db (apply model)
  .env.example            Client config placeholders (filled by rayfin up)
```

The React front end is intentionally omitted: in the **Rayfin Fabricator** you
describe the UI you want ("an agent portal to file and track claims") and the
Fabricator agent generates it, deploys the app, and validates it in its built-in
browser. This folder gives you the **insurance data model** to start from.

## The data model (TypeScript decorators)

```typescript
@entity()
@authenticated('*')
@role('authenticated', 'write', {
  policy: (claims, item) => claims.sub.eq(item.agentUserId),   // "my book" RLS
})
export class Policy {
  @uuid() id!: string;
  @text({ max: 40 }) policyNumber!: string;
  @set('Auto', 'Home', 'Renters', 'Life', 'Umbrella') product!: ...;
  @int() annualPremium!: number;
  @one(() => Customer) customer!: Customer;
  @one(() => Agent) agent!: Agent;
  @many(() => Claim) claims?: Claim[];
}
```

Note the `@role` policy: an agent can only write policies in their own book. That
is the Rayfin equivalent of **Power BI row-level security**, a deliberate parallel
we call out in the workshop.

## Prerequisites

- Node.js 20+ and npm.
- A Microsoft Fabric capacity and a **test workspace** you can deploy into.
- Signed in with your Microsoft (Entra) account.

## Deploy it

Either use the **Fabricator** (describe the app and let the agent build + deploy),
or from the CLI:

```bash
npm install
npm run rayfin:up        # provisions DB + auth + data APIs, deploys to Fabric
npm run rayfin:db        # re-apply after you change the data model
```

`rayfin up` writes the client `baseUrl` and `publishableKey` into your env; a
front end then talks to the data via the typed `RayfinClient<InsuranceSchema>`.

## How this connects to the analytics labs

The policies and claims captured here are **operational data in Fabric**. In the
BI labs you land the provided `ops/claims_intake.csv` (the same shape as this
app's `Claim` entity) into the `lh_insurance` Lakehouse and model it alongside the
Contoso Insurance star. The message for the customer: **one Fabric estate serves
both the app that writes the data and the analytics that read it.**

## Safety

Synthetic workshop artifact. Do not commit real customer data, workspace GUIDs,
or `rayfin up` secrets. `.env` / `.env.local` are gitignored.
