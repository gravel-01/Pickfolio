# Output Contracts

## Contents

- Run directory and manifest
- Selection and position reports
- Source audit, change, and review reports
- Delivery checks

## Run Directory

Use one immutable directory per run:

```text
runs/YYYY-MM-DD-slug/
├── manifest.json
├── source-audit.csv
├── selection.md          # select/full
├── position.md           # position/full
├── change-report.md      # refresh
├── review.md             # review
├── decision-log.md       # standard/audit
├── evidence/             # standard/audit; includes bottleneck analysis
├── tables/               # standard/audit
├── snapshots/            # standard/audit
├── raw/                  # audit
└── logs/                 # audit
```

Do not reuse a run directory for a later date or changed mandate.

## Manifest

Keep `manifest.json` machine-readable. Include:

- Schema version and run id.
- Creation time and research as-of date.
- Mode, market, language, and retention profile.
- Capital and risk parameters.
- Benchmark, existing holdings, and universe constraints.
- Data policy and snapshot paths.
- Gate statuses and approval records.
- Selected symbols and selection-manifest reference.
- Portfolio weights, cash, caps, and stages when applicable.
- Output paths and unresolved blockers.

Do not mark a status approved merely because a report file exists.

## Selection Report

Use this order:

1. Decision status and one-page conclusion.
2. Mandate, benchmark, horizon, and boundaries.
3. Direction and economic-chain evidence.
4. Complete bottleneck tree, transmission paths, node classification, and narrowing decision.
5. Basket shape and role definitions.
6. Research, watch, and comparator pools.
7. Peer-group hard-data comparisons.
8. Customers, orders, catalysts, and evidence grades.
9. Selected basket and role-duplication review.
10. Alternatives and switch conditions.
11. Data coverage, gaps, invalidation conditions, and next review.

Do not include final portfolio weights in a selection report.

## Position Report

Use this order:

1. Approval status and one-page plan.
2. Frozen selection reference.
3. Capital, cash, maximum loss, and leverage policy.
4. Role budgets and within-role allocation.
5. Final target weights and amounts.
6. Single-name and shared-risk caps.
7. Valuation, volatility, drawdown, liquidity, and overlap review.
8. Stress tests and loss amounts.
9. Staged entry plan and independent evidence gates.
10. Monitoring baselines, pause conditions, and thesis failures.
11. Data dates, limitations, and unresolved approvals.

State explicitly that the report is a plan and does not place orders.

## Source Audit

Always create `source-audit.csv` with at least:

```text
source_id,provider,field_group,symbol_scope,status,as_of_date,
retrieved_at,artifact_path,limitation,error
```

Include failed, restricted, empty, and not-attempted sources when they affect expected coverage.

## Change Report

Separate:

- New disclosures.
- New market observations.
- Recalculations using unchanged fundamentals.
- Source or methodology changes.
- Availability changes.
- Conflicts and unresolved gaps.
- Decisions requiring gate reapproval.

## Review Report

Lead with findings ordered by severity. Cite the affected file, table, field, or report section. Then state open questions, residual risk, and a brief scope summary.

## Delivery Checks

Before delivery:

- Reconcile report values with retained tables.
- Verify dates and units.
- Verify status labels match actual approvals.
- Verify all output links resolve.
- Run `scripts/validate_run.py`.
- Use strict validation only after all template placeholders are resolved.
