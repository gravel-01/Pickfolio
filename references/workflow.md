# Workflow

## Purpose

Run Pickfolio as a gated decision process rather than a single prompt that jumps from a market story to portfolio weights.

## Modes

### Select

1. Confirm the mandate and existing exposure.
2. Prepare a dated data snapshot and coverage audit.
3. Validate the market direction or research thesis.
4. Build the complete bottleneck tree and both positive and counter-evidence transmission paths.
5. Score and classify bottleneck nodes, then narrow the research chain to the mandate.
6. Define portfolio roles before choosing final names.
7. Build research, watch, and comparator pools.
8. Compare hard data within declared peer groups.
9. Validate customers, orders, catalysts, risks, and evidence strength.
10. Remove unintended role duplication and identify replacements.
11. Write the selection report and request approval to freeze it.

Do not assign weights in this mode.

### Position

1. Load a frozen selection manifest and verify its hash or path.
2. Confirm capital, currency, horizon, maximum loss, cash floor, and leverage policy.
3. Allocate budgets to portfolio roles.
4. Allocate each role budget among frozen names.
5. Apply valuation, volatility, drawdown, liquidity, and single-name caps.
6. Apply shared-risk caps for correlated names or common economic drivers.
7. Run portfolio stress tests.
8. Define staged entries, independent evidence gates, and monitoring baselines.
9. Write the position report and request approval.

Do not replace names inside this mode. Return to `select` when a selection thesis fails.

### Full

Run `select`, then stop at the selection-freeze gate. Continue with `position` only after explicit approval. Preserve both approval events in the manifest.

### Refresh

1. Load the prior manifest and snapshot.
2. Collect only the requested or stale fields.
3. Preserve the new snapshot; never overwrite the old snapshot.
4. Compare values, availability, dates, formulas, and source status.
5. Classify changes as factual updates, recalculations, source changes, or unresolved conflicts.
6. Produce `change-report.md` without silently changing a frozen decision.

### Review

Review in this order:

1. Incorrect or unsupported facts.
2. Time-period and security-line mismatches.
3. Invalid cross-group comparisons.
4. Missing-data treatment and proxy misuse.
5. Selection-to-position gate violations.
6. Weight, cash, cap, and stress-test errors.
7. Missing tests, audit trails, or approvals.

## Gates

| Gate | Passing condition | Failure action |
| --- | --- | --- |
| G0 Mandate | Scope, market, horizon, capital context, existing exposure, and authority are known | Ask only for the material missing decision |
| G1 Data | Sources, dates, coverage, missing fields, and formulas are auditable | Mark partial or blocked; narrow conclusions |
| G2 Selection | Peer-group evidence, role logic, alternatives, and invalidation conditions are explicit | Keep as draft or watch-only |
| G3 Freeze | Human explicitly approves the selected basket | Stop before position sizing |
| G4 Risk budget | Maximum loss, cash, leverage, single-name, and shared-risk limits are approved | Keep position blocked |
| G5 Position | Weights reconcile to 100%, respect caps, and pass documented stress tests | Revise weights or reduce exposure |
| G6 Stage | A new independent evidence check passes | Do not advance the next entry stage |

## Completion Criteria

A run is complete only when:

- The required mode outputs exist.
- `manifest.json` reflects the actual gate status.
- `source-audit.csv` records successful, failed, and restricted sources.
- Every key conclusion has a source, date, calculation, or explicit judgment owner.
- Missing fields and unresolved conflicts are visible.
- The validation script passes at the intended draft or strict level.
