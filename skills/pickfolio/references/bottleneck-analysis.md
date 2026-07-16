# Bottleneck Analysis

## Contents

- Demand drivers and complete bottleneck tree
- Positive and counter-evidence transmission
- Node scoring and evidence layers
- Mandate narrowing and required output

## Objective

Turn a broad investment story into a system of demand drivers, binding constraints, investable nodes, observable evidence, and falsification paths. Complete this analysis before defining the final basket roles.

## 1. Start From Demand Drivers

Identify what is changing in the underlying system. For AI infrastructure, useful demand drivers include:

- Training workloads.
- Inference workloads.
- Long-context and multimodal workloads.
- High-frequency agent calls.
- Enterprise application adoption.

For another theme, replace these with its actual demand drivers. Do not start from public-company names.

## 2. Build The Complete Bottleneck Tree

Map all relevant layers before selecting a preferred branch. An AI-infrastructure example contains:

1. Workload drivers.
2. Compute supply.
3. Memory and advanced packaging.
4. Power generation, grid, campus, and facility distribution.
5. Data-center permitting, interconnection, construction, and delivery.
6. Cooling and thermal management.
7. Scale-up, scale-out, switching, and optical networking.
8. Storage, data pipelines, governance, and security.
9. Software efficiency, inference economics, capital, and regulation.

Tag each node as one of:

- `core`: A binding constraint suitable for the current mandate.
- `research`: Plausible but requiring stronger evidence.
- `covered`: Already represented by existing holdings or another role.
- `risk`: A system-wide switch, veto, or counter-evidence factor.

Do not force every tree branch into the final basket.

## 3. Draw Two Transmission Graphs

### Positive transmission

Trace:

```text
demand driver -> capacity pressure -> bottleneck -> supplier demand
-> orders -> revenue conversion -> margin and cash-flow impact
```

### Constraint and counter-evidence transmission

Trace:

```text
weak end demand, poor ROI, policy delay, capacity release, or price decline
-> reduced bottleneck pressure -> delayed or cancelled projects
-> weaker orders or pricing -> lower revenue and profit expectations
```

For AI infrastructure, preserve at least these system checks:

- Compute density -> power and cooling pressure -> design complexity -> delivery time and capex.
- Power shortage -> interconnection delay -> data-center delay -> constrained compute deployment.
- Weak inference revenue or enterprise ROI -> questioned hyperscaler capex -> weaker supplier orders.
- Network constraints -> lower cluster utilization -> weaker compute ROI -> capex pressure.

## 4. Score Nodes Transparently

Score only to structure comparison. Keep raw fields visible and never let a composite score hide a weak critical field.

Recommended fields:

| Field | Question |
| --- | --- |
| Bottleneck strength | Would failure to solve this node constrain system delivery? |
| Data verifiability | Are continuous, public, reproducible signals available? |
| Existing-portfolio gap | Does the node add exposure not already owned? |
| Order strength | Are orders, backlog, RPO, or contracts improving within a compatible definition? |
| Revenue conversion | Is demand becoming recognized revenue? |
| Profit quality | Are margins, cash flow, and returns holding up? |
| Valuation risk | Has the market already priced in the bottleneck story? |
| Market confirmation | Is the direction showing relative strength or breadth? |
| Counter-evidence pressure | Have key falsification signals appeared? |

Use qualitative grades by default. Use a weighted score only when weights, directions, missing-data treatment, and thresholds are explicit. Recalibrate thresholds when the formula changes.

## 5. Require Multiple Evidence Layers

Treat a direction as supported only when at least two of these three layers agree:

- `fact`: Capacity, utilization, lead time, shipment, project, or industry data.
- `financial`: Orders, backlog, RPO, revenue, margin, cash flow, or return data.
- `market`: Relative strength, breadth, valuation position, liquidity, or crowding data.

Market confirmation alone is insufficient. A compelling story without financial or factual validation remains a research hypothesis.

## 6. Define Node Evidence And Falsification

For each important node record:

- Core story.
- What must be true.
- Required fields and preferred sources.
- Positive signals and thresholds, when defensible.
- Counter-evidence and invalidation signals.
- Security roles or industries that map to the node.
- Existing exposure and overlap.
- Current classification and confidence.

Examples of useful node evidence include utility capex, interconnection queues, equipment lead times, rack power density, cooling adoption, network shipments, project megawatts, order conversion, customer concentration, and end-demand capex or ROI.

## 7. Narrow To The Mandate

Select nodes using:

```text
bottleneck importance
+ evidence quality
+ value-capture potential
+ mandate fit
+ existing-portfolio complementarity
- valuation and counter-evidence pressure
```

State why excluded nodes remain comparators or risk switches. The narrowing result defines research directions, not individual stock conclusions.

## 8. Required Output

Include a concise bottleneck section in `selection.md`. Under `standard` or `audit` retention, also keep `evidence/bottleneck-analysis.md` containing:

- Complete tree.
- Positive transmission graph.
- Counter-evidence graph.
- Node scorecard.
- Evidence checklist.
- Mandate-fit classification.
- Narrowing conclusion and unresolved data.
