---
name: pickfolio
description: Evidence-first US-equity research and portfolio-positioning workflow. Use when Codex must discover or validate a US stock theme, build or review a candidate universe, create a stock-selection report, size a frozen selection into a cash-aware staged position plan, refresh or audit investment data sources, retain intermediate evidence, or review an existing research package. Supports select, position, full, refresh, and review modes; does not place trades.
---

# Pickfolio

Turn US-equity data into an auditable stock-selection decision and, after explicit selection approval, a risk-bounded position plan. Preserve the distinction between evidence, calculated proxies, human judgment, and execution authority.

## Route The Request

Choose exactly one primary mode:

| Mode | Use it for | Required result |
| --- | --- | --- |
| `select` | Discover a theme, build a universe, compare candidates, or freeze a basket | `selection.md` |
| `position` | Size an already frozen basket | `position.md`; require an approved selection manifest |
| `full` | Run selection first and position planning second | Both reports; stop for approval between them |
| `refresh` | Refresh sources or compare a new snapshot with an old one | `change-report.md` and source audit |
| `review` | Audit existing data, selection logic, or position logic | `review.md` with findings first |

Do not silently expand a request from research into position planning, or from position planning into order placement.

## Load The Right References

Read [workflow.md](references/workflow.md), [parameters.md](references/parameters.md), and [output-contracts.md](references/output-contracts.md) for every new run.

Read the remaining files only when applicable:

- For selection work, read [selection.md](references/selection.md).
- For bottleneck trees, transmission paths, node scoring, or research-chain narrowing, read [bottleneck-analysis.md](references/bottleneck-analysis.md).
- For position sizing or staged entry planning, read [position.md](references/position.md).
- For source collection, refreshes, or evidence review, read [data-governance.md](references/data-governance.md).
- For US listings, SEC filings, ADRs, 13F, short data, options, or benchmark choices, read [us-equities.md](references/us-equities.md).

## Start A Run

1. Resolve the run parameters. Ask only for material missing decisions; use documented defaults for the rest.
2. Create a run package with `scripts/init_run.py`. Never write a new run over an existing directory.
3. Record resolved inputs in `manifest.json` before analysis.
4. Collect or reuse data according to `data_policy`; record every source attempt and its as-of date.
5. Follow the mode-specific workflow and update statuses as gates are completed.
6. Validate the package with `scripts/validate_run.py` before delivery.

Example:

```bash
python3 scripts/init_run.py \
  --output-root /path/to/project/runs \
  --slug ai-infrastructure \
  --mode full \
  --capital 5000000 \
  --currency USD \
  --retain standard
```

## Enforce The Decision Gates

Use these statuses in `manifest.json`:

```text
mandate: draft -> confirmed
data: pending -> ready | partial | blocked
selection: draft -> reviewed -> frozen
position: blocked -> draft -> reviewed -> approved
```

Require explicit human approval before changing `selection` to `frozen`, before approving the risk budget, and before changing `position` to `approved`. In `full` mode, stop after the selection report when approval is missing.

Treat `partial` data as usable only when the missing fields and affected conclusions are explicit. Treat `blocked` data as a hard stop for any conclusion that depends on it.

## Apply The Core Rules

- Compare quantitative results only within comparable business models or declared peer groups.
- Treat missing data as missing, never as zero or an automatic penalty.
- Keep raw facts, normalized fields, calculated metrics, proxies, and judgments separately labeled.
- Keep market as-of date, retrieval date, fiscal period, filing date, and holding date separate.
- Map the complete bottleneck system before narrowing to investable nodes; include both positive transmission and counter-evidence paths.
- Keep TTM and forward estimates separate; keep annual and quarterly financials separate.
- Do not merge RPO, backlog, bookings, and book-to-bill into one directly comparable metric.
- Do not equate orders with revenue, revenue with profit, customer labels with AI revenue, or price action with fundamental validation.
- Use institutional ownership, short interest, short-sale volume, options, and crowding as review signals unless the mandate explicitly defines a tested rule.
- Require a frozen selection before calculating position weights.
- Derive position weights from role budgets, within-role allocation, cash policy, single-name caps, shared-risk caps, and stress tests. Do not average unrelated rankings into weights.
- Require new independent evidence before each staged increase. A lower price alone is not new evidence.
- Never place, modify, or cancel orders. Hand execution to a separate explicitly authorized trading workflow.

## Use Retention Deliberately

Set `retain` to:

- `minimal`: reports, manifest, and source audit only.
- `standard`: also retain evidence matrices, normalized tables, calculations, and key snapshots. Use this default.
- `audit`: also retain raw responses, page captures, complete logs, and failed-attempt artifacts.

Never omit `manifest.json` or `source-audit.csv`.

## Finish The Run

Run:

```bash
python3 scripts/validate_run.py /path/to/run
```

Use `--strict` only for a completed delivery; drafts may contain template placeholders. Report validation errors, unresolved data gaps, approval status, and the exact output paths.
