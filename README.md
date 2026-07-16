# Pickfolio

[简体中文 SKILL 对照](skills/pickfolio/SKILL-zh.md)

Evidence-first US stock research, selection, and position planning for Codex.

Pickfolio turns a research mandate into two auditable decisions:

1. Which US stocks belong in the selected basket, and why?
2. After that basket is explicitly frozen, how should capital, cash, risk caps, and staged entries be planned?

It also preserves source attempts, coverage gaps, calculations, intermediate evidence, and approval state. It does not place trades.

Before selecting companies, Pickfolio maps the full bottleneck system: demand drivers, positive transmission, counter-evidence paths, node verifiability, existing-portfolio coverage, and the narrowing decision that turns a broad theme into investable research roles.

## Modes

- `select`: Build and freeze a stock-selection report.
- `position`: Size an approved selection into a position plan.
- `full`: Run selection, pause for approval, then plan positions.
- `refresh`: Update data snapshots and report material changes.
- `review`: Audit an existing research or position package.

## Output

```text
runs/YYYY-MM-DD-topic/
├── manifest.json
├── source-audit.csv
├── selection.md
├── position.md
├── decision-log.md
├── evidence/
│   └── bottleneck-analysis.md
├── tables/
└── snapshots/
```

Retention is configurable as `minimal`, `standard`, or `audit`.

## Skill Location

The installable Codex skill is in [`skills/pickfolio`](skills/pickfolio). A complete reader-facing Chinese counterpart is available at [`SKILL-zh.md`](skills/pickfolio/SKILL-zh.md).

Install it locally with:

```bash
cp -R skills/pickfolio "${CODEX_HOME:-$HOME/.codex}/skills/pickfolio"
```

Then invoke it with `$pickfolio`.

## Initialize A Run

```bash
python3 skills/pickfolio/scripts/init_run.py \
  --config skills/pickfolio/assets/project-config.example.json \
  --output-root ./runs \
  --slug ai-infrastructure \
  --mode full \
  --capital 5000000 \
  --currency USD \
  --retain standard
```

Validate a draft package:

```bash
python3 skills/pickfolio/scripts/validate_run.py ./runs/2026-07-16-ai-infrastructure
```

Use `--strict` only after all report placeholders have been resolved.

## Current Scope

Version 1 focuses on US equities, ADR-aware evidence handling, stock selection, position planning, data-source auditing, and reproducible report packages. Broker execution and automatic order placement are intentionally outside the skill.
