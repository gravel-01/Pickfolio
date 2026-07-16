# Parameters

## Resolve Material Inputs

Prefer an existing project configuration or prior manifest. Otherwise resolve only the inputs that can materially change the result.

| Parameter | Default | Required when | Meaning |
| --- | --- | --- | --- |
| `market` | `US` | Always | Version 1 supports US equities |
| `mode` | `full` | Always | `select`, `position`, `full`, `refresh`, or `review` |
| `as_of` | Current local date | Always | Research cutoff, not necessarily last trading date |
| `capital` | Unset | Position/full | Maximum capital budget |
| `currency` | `USD` | Position/full | Budget currency |
| `horizon` | `3-5y` | Select/position/full | Intended holding period |
| `max_loss_pct` | Unset | Position approval | Maximum tolerable portfolio loss |
| `cash_floor_pct` | `15` | Position/full | Minimum strategic cash |
| `leverage_allowed` | `false` | Position/full | Whether gross exposure may exceed capital |
| `benchmark` | `SPY` | Select/full | Primary US equity benchmark |
| `existing_holdings` | Empty | Select/full | Existing names used for overlap checks |
| `candidate_limit` | `25` | Select/full | Target research-universe size, not a hard truth limit |
| `bottleneck_analysis` | `required` | Select/full | Require a complete tree, positive path, and counter-evidence path |
| `bottleneck_scoring` | `qualitative` | Select/full | `qualitative` or an explicitly documented weighted model |
| `data_policy` | `refresh-missing` | Always | `reuse`, `refresh-missing`, or `refresh-all` |
| `retain` | `standard` | Always | `minimal`, `standard`, or `audit` |
| `language` | `zh-CN` | Always | Report language |
| `selection_approval` | `required` | Full/position | Human freeze gate |
| `position_approval` | `required` | Position/full | Human risk and weight approval gate |
| `execution` | `disabled` | Always | Pickfolio never places orders |

## Ask In This Order

When inputs are missing, ask at most the smallest useful set at a time:

1. Clarify the research objective and whether the user wants `select`, `position`, or `full`.
2. For selection, clarify the horizon and existing portfolio overlap when they are not discoverable.
3. For position planning, clarify capital, maximum tolerable loss, minimum cash, and leverage policy.
4. For refresh work, clarify the prior run and the requested as-of date.

Do not block on cosmetic preferences such as report title or chart count; use defaults and record them.

## Retention Profiles

### Minimal

Retain:

- `manifest.json`
- Required reports
- `source-audit.csv`

### Standard

Also retain:

- Normalized source tables
- Candidate and peer-group tables
- Evidence and missing-data matrices
- Position calculations and stress tests
- Key immutable snapshots
- Decision log

### Audit

Also retain:

- Raw API responses and downloaded source files
- Page captures or extracted page text where permitted
- Complete command and collection logs
- Failed and restricted source artifacts
- Formula-level lineage and reconciliation tables

## Configuration Precedence

Resolve conflicts in this order:

1. Explicit instruction in the current request.
2. Explicitly approved current-run decision.
3. Project configuration.
4. Prior frozen manifest, only for fields intended to carry forward.
5. Skill defaults.

Record every override in the manifest decision log.
