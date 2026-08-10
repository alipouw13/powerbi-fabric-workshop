# Lab 11 - Rayfin insurance app (appendix)

**Deck:** "Build a data app on Fabric with Rayfin" - **Appendix reading, not run**

> **Not in scope for this workshop.** Rayfin runs on Microsoft Fabric, which is
> not available to this audience. This page is kept as reference only. It is
> **not demoed and not a prerequisite for anything**. See
> [reference/schwab-current-state.md](../../reference/schwab-current-state.md).
>
> **The part you can act on today:** the idea worth taking from this page is that
> a business rule - "an agent sees only their own book" - should be designed once
> and applied consistently everywhere. You implement that rule as Power BI RLS in
> [Lab 4](../lab-04-governance-foundations/README.md).

Rayfin is a Backend-as-a-Service on Fabric for building operational apps that
capture data at the source, with row-level policies enforced in the app the same
way RLS enforces them in analytics.

## What it would look like
- A running Rayfin app from the rayfin-app/ skeleton
- A TypeScript data model with Customer, Agent, Policy, and Claim entities
- A Fabric-backed data service configured through rayfin.yml
- A security comparison between Rayfin @role and Power BI RLS

## Reference docs
[Rayfin](../../reference/rayfin.md), [rayfin-app/README.md](../../rayfin-app/README.md)

## Steps
### 1. Review what Rayfin provides
- Rayfin is a Backend-as-a-Service that runs on Microsoft Fabric.
- You define the application model in TypeScript.
- Decorators such as @entity, @authenticated('*'), @role(...), @uuid, @text({max}), @int, @boolean, @date, @set(...), @one(() => X), and @many(() => X) describe the schema and access rules.
- schema.ts registers the entities.
- rayfin.yml configures services such as auth.fabric, data.dialect mssql, and staticHosting.
- The client uses RayfinClient<Schema> to call the generated service.
- The Fabricator workflow can build, deploy, and validate the app from a description.

### 2. Open the Contoso Claims Intake skeleton
- Open the workshop repository in VS Code.
- Navigate to rayfin-app/.
- Read [rayfin-app/README.md](../../rayfin-app/README.md).
- Find the Customer entity.
- Find the Agent entity.
- Find the Policy entity.
- Find the Claim entity.
- Notice that Policy connects customers, agents, and claims.
- Notice that Claim lines up with ops/claims_intake.csv from Lab 5 and Lab 8.

### 3. Inspect the row-level policy
- Open the model files described by rayfin-app/README.md.
- Find the @role policy on Policy or the related book-of-business access rule.
- Read the rule as a business statement: an agent sees only their own book.
- Compare that to the Agent Book Power BI RLS role from Lab 4.
- Power BI RLS protects analytics queries and reports.
- Rayfin @role protects operational app reads and writes.
- The business rule should be designed once, then implemented consistently across both surfaces.

### 4. Build with the CLI path
- Open a terminal in rayfin-app/.
- Install dependencies.

```powershell
npm install
```

- Deploy the app services.

```powershell
npm run rayfin:up
```

- Re-apply the data model if the scaffold or facilitator asks you to update the database.

```powershell
npm run rayfin:db
```

- These scripts map to rayfin up and rayfin up db apply.
- Sign in with your Microsoft account when prompted.
- Use the Fabric test workspace assigned by the facilitator.

### 5. Build with the Fabricator path
- If your facilitator uses Fabricator, describe the app in plain language.
- Use this prompt as a starting point: Build an agent portal to file and track Contoso Insurance claims on Fabric.
- Include the entities Customer, Agent, Policy, and Claim.
- Include the rule that an agent can see only their own book.
- Ask the Fabricator to build, deploy, and validate the running app in a Fabric test workspace.
- Review the generated changes before keeping them.
- Keep the rayfin-app/README.md contract as the source of truth.

### 6. Enter a policy and claim
- Open the deployed Rayfin app URL.
- Sign in with Fabric authentication.
- Add or select a Customer.
- Add or select an Agent.
- Create a Policy with product, region, channel, effective date, annual premium, and status.
- Create a Claim tied to the Policy.
- Include fields that map to claims_intake.csv, such as coverage, loss_type, loss_date, reported_date, status, reserve_amount, paid_amount, severity, and adjuster.
- Save the claim.

### 7. Confirm data persistence in Fabric
- Return to Fabric.
- Locate the data service or database target configured by rayfin.yml.
- Confirm the Customer, Agent, Policy, and Claim records persist.
- Compare the Claim shape to Files/raw/ops/claims_intake.csv.
- Explain how a production app could feed Bronze tables instead of a static CSV.
- Connect this back to lh_insurance, bronze_claims_intake, and sm_insurance.
- The operational app and analytics model are part of the same Fabric estate.

### 8. Discuss security and ALM
- Confirm that @authenticated('*') requires sign-in.
- Confirm that @role limits book-of-business access.
- Discuss how this aligns with Power BI RLS and least-privilege workspace roles.
- Discuss which workspace should host dev, test, and prod versions of the app.
- Discuss how @microsoft/rayfin-mcp could help GitHub Copilot assist app changes.
- Capture follow-up owners for app security, data ownership, and deployment.

## You'll know it worked when
- rayfin-app/ installs with npm install.
- npm run rayfin:up completes or the Fabricator deploys the app successfully.
- npm run rayfin:db applies the model when needed.
- You can sign in to the app.
- You can create a Policy and Claim.
- You can show that the Claim shape matches ops/claims_intake.csv.
- You can explain the Rayfin @role and Power BI RLS parallel.

## Back to the workshop
[Lab 12 - Community of practice and next steps](../lab-12-showcase-next-steps/README.md)
