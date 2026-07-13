# Target architecture (housing workshop)

The workshop drives toward a **OneLake-centric** estate: the sources land once in
OneLake, and every workload, Power BI, Copilot, and the Data Agent, reads that
single governed copy. This is the shift from a **Tableau + extracts** world
(many `.hyper` extracts, many refresh schedules, logic trapped in workbooks) to
**land once, model once, serve many**. This renders on GitHub.

```mermaid
flowchart LR
  subgraph SRC[Sources]
    RF[Redfin market feed\nhousing metrics]
    MLS[MLS listings\nlisting-level feed]
    ONP[(On-prem / cloud DBs\nSQL Server, files)]
  end

  subgraph GW[Secure connectivity - managed data gateways]
    direction TB
    OPDG[On-premises data gateway\nfor on-prem sources]
    VNETGW[VNet data gateway\nfor cloud sources]
  end

  subgraph FAB[Microsoft Fabric capacity]
    direction TB
    subgraph OL[OneLake - one logical lake, open Delta]
      B[Bronze\nraw landing]
      S[Silver\nconformed star: dims + fact]
      G[Gold\nmarket summary, region ranking]
      B --> S --> G
    end
    SEM[Housing-Market-Insights\nshared semantic model - Direct Lake]
    G --> SEM
  end

  subgraph SERVE[Serve]
    PBI[Power BI - reports]
    COP[Copilot in Power BI\nbuild + narrate + DAX]
    AGENT[Fabric Data Agent\nnatural-language Q&A]
    MCP[GitHub Copilot + Power BI MCP\nVS Code dev workflow]
  end

  ONP -- via gateway --> OPDG
  RF -- via gateway --> VNETGW
  MLS -- via gateway --> VNETGW
  VNETGW -- Data Factory / Dataflow Gen2 --> B
  OPDG -- Data Factory / Dataflow Gen2 --> B
  SEM --> PBI
  SEM --> COP
  SEM --> AGENT
  SEM --> MCP

  classDef src fill:#E7F0FA,stroke:#2F77C9;
  classDef gw fill:#FBF1E0,stroke:#B5760B;
  classDef lake fill:#E4F1EF,stroke:#117865;
  classDef serve fill:#E8F3EC,stroke:#1EA672;
  class RF,MLS,ONP src;
  class OPDG,VNETGW gw;
  class B,S,G,SEM lake;
  class PBI,COP,AGENT,MCP serve;
```

## How each lab maps onto this picture

| Lab | Part of the diagram it builds |
| --- | --- |
| Day 1 - Lab 0 Setup | Confirms the sandbox and lands the raw data |
| Day 1 - Lab 1 Tableau to Power BI | The mental model: extracts/workbooks -> model + reports |
| Day 1 - Lab 2 Data modeling | The **Silver star** (dims + fact) vs a flat extract |
| Day 1 - Lab 3 Visualization | The **Power BI reports** serve box, viz design |
| Day 1 - Lab 4 Governance foundations | Guardrails around the capacity + workspaces |
| Day 2 - Lab 5 Ingestion | The **source -> Bronze** arrows (Data Factory, gateways) |
| Day 2 - Lab 6 Semantic model | **Gold -> shared semantic model** (Direct Lake) |
| Day 2 - Lab 7 Copilot in reports | The **Copilot in Power BI** serve box |
| Day 2 - Lab 8 Migrate a workbook | A full source-to-report slice, end to end |
| Day 3 - Lab 9 MCP + GitHub Copilot | The **GitHub Copilot + MCP** dev box, PBIP + CI/CD |
| Day 3 - Lab 10 Data Agent | The **Data Agent** serve box |
| Day 3 - Lab 11 Showcase & next steps | The whole picture, plus the adoption roadmap |

## Design choices for a Tableau team

> See also the polished **current-state vs target-state** draw.io diagrams in
> [housing-architecture.md](housing-architecture.md) (editable + PNG).

- **Land once, serve many.** Sources replicate into OneLake; Power BI, Copilot
  and the Data Agent all read the same gold tables. No more one extract per
  workbook.
- **Direct Lake, not Import.** No refresh windows, lower capacity cost, always
  current, the closest thing to a Tableau live connection but on a governed model.
- **Model as a star.** A Tableau extract is often one wide table. Power BI is at
  its best on a [star schema](https://learn.microsoft.com/power-bi/guidance/star-schema);
  Lab 2 makes that switch and it is the single biggest quality lever.
- **Measures defined once.** Business logic (YoY, months of supply) lives in the
  shared model, not copied into every workbook, so numbers agree everywhere.
- **Dev, test, prod are separate** so an experiment cannot disturb the reports
  executives rely on.
