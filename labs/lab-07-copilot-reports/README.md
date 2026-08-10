# Lab 7 - M365 Copilot for DAX and Power Query

**Duration:** ~90 min - **Deck:** "M365 Copilot for Power BI work" - **Day 3**

**Scope:** In scope. M365 Copilot in a browser or Office app, plus Power BI
Desktop. Nothing else.

M365 Copilot is the **only** AI available for this work, and it is not connected
to Power BI. That shapes everything about how you use it: you describe your model
in the prompt, Copilot drafts code, you review it, and you **copy and paste** it
into the DAX editor or the Power Query Advanced Editor. Used well, that loop is
genuinely fast. Used carelessly, it produces confident, wrong DAX.

This lab makes the loop reliable.

## Schwab context
There is no Copilot inside Power BI, no Data Agent, and no Copilot Studio. What
there is, for some of you, is M365 Copilot in another window. That is enough to
meaningfully speed up two things Schwab does constantly: writing DAX measures
that used to be Tableau calculated fields, and writing Power Query M for
transformations that would otherwise be twenty clicks. The catch is that Copilot
cannot see your model, so **the quality of your output is the quality of your
prompt context.** That is a learnable skill, and it is what this lab teaches.

## What you'll build
- A reusable "model context" prompt block your whole team can paste
- Tableau-to-DAX translations you have tested, not just accepted
- A Power Query transformation drafted in Copilot and pasted into Advanced Editor
- Reviewed measure descriptions added to sm_insurance
- A model documentation page for new analysts
- A team standard for reviewing AI-generated code before it ships

## Prerequisites
- Completed [Lab 6 - The shared semantic model](../lab-06-semantic-model-directlake/README.md)
- sm_insurance with core measures and descriptions
- **M365 Copilot access for at least one person per pair.** Pair up before you
  start - unlicensed attendees drive Power BI Desktop while their partner drives
  Copilot. That split is realistic and works well.
- Reference docs: [M365 Copilot for Power BI work](../../reference/copilot-in-power-bi.md)
  and [current state](../../reference/schwab-current-state.md)

> **Data handling.** Never paste real Schwab data, credentials, connection
> strings, or customer information into Copilot. You paste **code, column names,
> and business definitions** - never source records. Everything in this lab uses
> synthetic Contoso Insurance content.

---

## Part A - DAX

Copilot cannot see your model, so you have to hand it one.

### 1. Build your reusable model context block
Write this once, save it, and paste it at the top of every Copilot prompt. This
is the single highest-impact habit in the lab.

```
I am writing DAX for a Power BI model in Import mode. The model is a star schema:

Facts:
  fact_premium(policy_id, agent_id, date_id, written_premium, earned_premium)
  fact_claim(policy_id, coverage_id, date_id, claim_id, incurred_loss, paid_loss)

Dimensions:
  dim_policy(policy_id, policy_number, product, customer_id)
  dim_customer(customer_id, customer_segment)
  dim_agent(agent_id, agent_name, region, channel)
  dim_coverage(coverage_id, coverage, loss_type)
  dim_date(date_id, period_begin, year, quarter, month, month_name)

dim_date is marked as the date table on period_begin.
Relationships are one-to-many, single direction, dimensions filtering facts.

Existing measures:
  Written Premium, Earned Premium, Policies In Force, Policies Written,
  Incurred Losses, Paid Losses, Claim Count, Loss Ratio, Average Premium,
  Written Premium PY, Written Premium YoY %

Always reuse existing measures rather than re-aggregating columns.
```

- Adjust it to match your actual model.
- Save it somewhere the whole team can reach. This block is a community-of-practice
  artifact - it should be standardized, not reinvented per person.

### 2. Explain unfamiliar DAX
- Copy the Loss Ratio measure from your model.
- Prompt: "Explain this Power BI DAX measure to an analyst who knows Tableau but
  not DAX. Explain what filter context is doing here."
- Compare the explanation to what you understood in Lab 6.
- Repeat with Written Premium PY or Written Premium YoY %.
- This is the safest possible use of Copilot: it cannot break anything, and
  understanding filter context is the main conceptual hurdle coming from Tableau.

### 3. Translate a Tableau calculation
- Pick a Tableau calculated field from your own work, or use an LOD example from
  [reference/tableau-to-powerbi.md](../../reference/tableau-to-powerbi.md).
- Paste your context block from step 1, then the Tableau calculation, then:
  "Convert this to a Power BI DAX measure using my model above. Explain how the
  two engines evaluate it differently, and flag anything that will not translate
  cleanly."
- **Copy the result into Power BI Desktop and test it.** Do not accept it on sight.
- Validate at three grains: total, by product, and by month. A measure that is
  right at the total and wrong by month is the classic failure.
- Record which Tableau patterns translate cleanly and which need a rethink. That
  list is directly reusable in the Lab 8 migration.

### 4. Draft a new measure, then break it on purpose
- Ask Copilot for a `Loss Ratio YoY` measure using your context block.
- Review the date logic. Does it use `dim_date`? Does it use `SAMEPERIODLASTYEAR`
  or `DATEADD` appropriately? Does it handle a missing prior period?
- Now run the same prompt **without** the context block and compare. The second
  answer will invent table names.
- That contrast is the lesson: Copilot's usefulness here is almost entirely a
  function of the context you supply.
- Keep the measure only if the numbers tie out. If not, save it as a draft note
  outside the model.

---

## Part B - Power Query M

Because all transformation at Schwab happens in Power Query, this is where
Copilot can save the most clicking - and where a bad paste does the most damage.

### 5. Draft a transformation in M
- Pick a real transformation from Lab 5 - unpivoting a wide monthly Excel sheet,
  splitting a combined name column, or conditionally categorizing severity.
- Prompt Copilot with: the column names, their types, a couple of **synthetic**
  example rows, and what you want the output to look like. Then: "Write the Power
  Query M for this transformation as a single let expression I can paste into the
  Advanced Editor."
- In Power BI Desktop, open Power Query, select the query, and open **Advanced
  Editor**.
- Paste the M and apply.
- Read the error if it fails. M errors are terse but specific - and pasting the
  error back into Copilot with the M is an effective debugging loop.

### 6. Verify what the paste actually did
This is the step people skip. Do not skip it.

- Check the row count before and after. Did the transformation silently drop rows?
- Check for new `null` values. A type mismatch often produces nulls rather than
  an error.
- Check data types on every affected column. Copilot frequently omits explicit
  typing.
- Check whether **query folding still works**. Right-click the last step and look
  for View Native Query. Generated M often breaks folding, which can turn a
  two-minute refresh into a twenty-minute one.
- Check the step names. Rename generated steps to something a colleague can read.
- If the M is longer than the click-path would have been, use the click-path.
  Generated code you do not understand is a maintenance liability.

### 7. Build the team's M reuse library
- Save the M snippets that worked, with a one-line description of what each does.
- Add them to `src/powerquery/` or wherever your community of practice decides.
- Standardize the prompt patterns that produced good output.
- Without Dataflows, a shared snippet library is how Schwab gets transformation
  reuse. It is low-tech and it works.

---

## Part C - Documentation and review

### 8. Draft measure descriptions
- Prompt: "Write one-sentence business descriptions for these P&C insurance
  measures for a Power BI model: Written Premium, Earned Premium, Incurred
  Losses, Paid Losses, Claim Count, Loss Ratio, Average Premium."
- Review every description for insurance accuracy.
- Avoid any description that implies data lineage you have not validated.
- Add the approved descriptions to sm_insurance.
- Descriptions are the cheapest trust-building work available to you, and Copilot
  makes them nearly free.

### 9. Document the model for a new analyst
- Copy your table and measure list out of the model.
- Prompt: "Turn this into a one-page semantic model guide for a new report author
  migrating from Tableau. Include which fields to use for time, and which fields
  to avoid."
- Edit for accuracy, then save it with your team notes.
- This becomes a starter template for the community of practice in Lab 12.

### 10. Agree the review standard
Generated code that nobody reviewed is how a shared model loses credibility.
Write the rule down as a group:

- Generated DAX is tested at three grains before it enters the model.
- Generated M is checked for row count, nulls, types, and folding.
- Nobody commits code they cannot explain to a colleague.
- Anything added to sm_insurance goes through the model owner from Lab 6.
- No real data goes into any AI tool, ever.

### 11. Know the limits
Fill this in as a group, from what you actually experienced:

| Task | M365 Copilot |
| --- | --- |
| Explain DAX you paste in | Yes - and it is good at it |
| Translate a Tableau calculation | Yes, with a context block |
| Draft a DAX measure | Yes, then you test it |
| Draft Power Query M | Yes, then you verify folding and types |
| Draft descriptions and documentation | Yes |
| See your model schema | **No** - you describe it every time |
| Run DAX and return real numbers | **No** |
| Generate a report page | **No** |
| Read your data | **No** - and it must not |

## You'll know it worked when
- Your team has a saved model context block that everyone uses.
- You translated at least one Tableau calculation to DAX and validated it at
  three grains.
- You pasted generated M into Advanced Editor, and you checked row count, nulls,
  types, and folding afterwards.
- You can show one case where Copilot was wrong and explain how you caught it.
- Measure descriptions are reviewed and added to sm_insurance.
- The review standard is written down and agreed.
- Nobody pasted real data into an AI tool.

## Next
[Lab 12 - Community of practice and next steps](../lab-12-showcase-next-steps/README.md)
