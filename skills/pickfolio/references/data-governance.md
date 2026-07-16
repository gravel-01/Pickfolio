# Data Governance

## Contents

- Four data layers
- Source reliability
- Time semantics and snapshots
- Conflicts and metric boundaries
- Refresh behavior

## Separate Four Data Layers

### 1. Source Catalog

Maintain stable source capabilities:

```text
source_id, provider, entrypoint, fields, security_scope, auth,
update_frequency, method, reliability_tier, known_boundaries
```

Do not store a past run's success state as a permanent source capability.

### 2. Attempt Log

Record every actual collection attempt:

```text
run_id, attempted_at, source_id, symbol, field_group, request_ref,
status, error, retry_method, artifact_path
```

Use statuses such as `success`, `partial`, `empty`, `restricted`, `blocked`, and `error`. Preserve real errors; never claim a fallback was attempted when it was not.

### 3. Coverage Matrix

Record the current run's field coverage by security:

```text
symbol, security_line, field, value_status, source_id, as_of_date,
retrieved_at, period_type, fiscal_period, artifact_path, limitation
```

Keep `missing`, `not_applicable`, `restricted`, and `not_attempted` distinct.

### 4. Lineage

Trace every report metric:

```text
metric_id, symbol, output_file, output_location, source_artifact,
source_fields, formula, as_of_date, calculated_at, boundary
```

## Rank Source Reliability

Prefer sources in this order when the field is genuinely covered:

1. Regulatory filing, exchange, regulator, or official dataset.
2. Company investor-relations filing, presentation, or release.
3. Established market-data vendor with a documented field definition.
4. Reputable aggregator or authenticated visible page.
5. Calculated proxy from traceable inputs.
6. Search snippet, commentary, or unverified secondary claim.

Higher-tier does not mean comparable. A primary-source backlog and primary-source RPO can still use incompatible definitions.

## Preserve Time Semantics

Store separately:

- `market_as_of`: Latest market observation used.
- `retrieved_at`: When the data was fetched.
- `period_end`: Fiscal or measurement period end.
- `filed_at`: Regulatory filing date.
- `holding_date`: Ownership snapshot date.
- `effective_at`: Date a decision or configuration became active.

Never relabel a value with a newer market date when its underlying financial denominator or filing period did not change.

## Preserve Snapshots

- Write each refresh to a new dated or run-id directory.
- Never overwrite a frozen run's raw or normalized data.
- Save source URLs, request parameters with secrets redacted, raw artifacts when retention permits, and checksums for critical inputs.
- Keep prior values when comparing changes, but never present stale values as newly fetched.

## Resolve Conflicts

When sources disagree:

1. Check security line, currency, units, split adjustment, fiscal period, and retrieval date.
2. Prefer the source closest to the original disclosure for factual fields.
3. Keep vendor-specific estimates separate rather than averaging them silently.
4. Record the conflict and its effect on the decision.
5. Block the dependent conclusion when the conflict is material and unresolved.

## Apply Metric Boundaries

- Price return is not total return unless distributions are included.
- Price position and maximum drawdown are historical risk proxies.
- Current valuation and historical percentile are different fields.
- A five-year average is not a historical percentile.
- TTM price/cash-flow is not automatically P/FCF.
- Short interest is not daily short-sale volume.
- Put/call, open interest, and implied volatility do not reveal net dealer gamma without position-level data and assumptions.
- Institutional ownership counts, concentration, and ownership percentage are different fields.
- 13F does not cover all investors or all global security lines.
- A customer or industry label is not a quantified revenue share.

## Refresh Without Decision Drift

A refresh may update facts and calculations. It must not silently alter a frozen basket, approved weight, or stage authorization. Produce a change report and route material changes back through the appropriate gate.
