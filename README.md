# Pickfolio

[English](README.md) | [简体中文](README.zh-CN.md)

An evidence-first US stock research, selection, and position-planning skill for Codex.

Pickfolio turns a research mandate into two auditable decisions:

1. Which US stocks belong in the selected basket, and why?
2. After that basket is explicitly frozen, how should capital, cash, risk caps, and staged entries be planned?

Before selecting companies, it maps the complete bottleneck system: demand drivers, positive transmission, counter-evidence paths, node verifiability, existing-portfolio coverage, and the narrowing decision that turns a broad theme into investable research roles.

## Core Capabilities

- Build a complete bottleneck tree before choosing stocks.
- Validate a theme with factual, financial, and market evidence.
- Build research, watch, and comparator pools.
- Compare quantitative evidence only within declared peer groups.
- Freeze a selected basket before calculating weights.
- Convert role budgets, cash policy, caps, and stress tests into a staged position plan.
- Audit source attempts, dates, coverage gaps, calculations, and decision lineage.
- Retain intermediate evidence at `minimal`, `standard`, or `audit` level.
- Review existing selection reports, position plans, and data packages.
- Produce plans only; never place, modify, or cancel orders.

## Installation

Install the latest `main` branch:

```bash
mkdir -p "${CODEX_HOME:-$HOME/.codex}/skills"

git clone --depth 1 \
  https://github.com/gravel-01/Pickfolio.git \
  "${CODEX_HOME:-$HOME/.codex}/skills/pickfolio"
```

Reopen Codex or start a new conversation after installation.

## Usage

### Minimal general-purpose invocation

When you do not yet know which mode to choose, describe the outcome and let Pickfolio route the task:

```text
Use $pickfolio to help me complete a US-equity research task.
Choose select, position, full, refresh, or review based on my intended outcome.
Ask only for missing parameters that would materially change the result; use defaults
for the rest and record them in the manifest. Respect the selection-freeze and
position-approval gates. Do not place orders.
```

### General parameter template

Replace the bracketed fields with your own information and remove fields that do not apply:

```text
Use $pickfolio to research [US theme / industry / candidate universe] and perform
[mode or intended outcome].

Research objective: [discover a direction / select stocks / plan positions /
refresh data / review existing work]
Input material: [holdings, candidate list, reports, data directory, or manifest path;
write "none" when unavailable]
Investment horizon: [for example, 1-3y or 3-5y]
Existing holdings or prohibited overlap: [symbols or none]
Benchmark: [for example, SPY; use the default when uncertain]
Capital and currency: [required only for position/full]
Maximum tolerable loss, cash floor, and leverage policy: [position/full only]
Data cutoff: [latest or YYYY-MM-DD]
data_policy: [reuse / refresh-missing / refresh-all]
retain: [minimal / standard / audit]
Output directory: [target path; otherwise create a new immutable run directory]

Ask me before assuming a missing parameter that would materially change the result.
Use documented defaults for the rest and record them explicitly. Produce research
and position plans only; do not execute trades.
```

You may provide an explicit `select`, `position`, `full`, `refresh`, or `review` mode, or describe the desired result and let Pickfolio choose the mode.

### Scenario examples

The following examples show how to add constraints for concrete tasks. They are not fixed industry, capital, or allocation requirements.

#### Run the full workflow

```text
Use $pickfolio to research a US AI-infrastructure basket.
Start with the bottleneck tree and stock-selection report. Preserve standard
intermediate evidence. Stop for my approval before freezing the selection,
then create a position plan for USD 5,000,000 with at least 15% cash.
Do not place orders.
```

#### Create only a stock-selection report

```text
Use $pickfolio in select mode to analyze the US power-grid infrastructure theme.
Build research, watch, and comparator pools; compare names only within peer groups;
and produce selection.md without assigning portfolio weights.
```

#### Create a bottleneck analysis

```text
Use $pickfolio to map the complete AI-infrastructure bottleneck system.
Include demand drivers, positive transmission, counter-evidence transmission,
node scoring, evidence requirements, existing-portfolio overlap, and the final
research-chain narrowing decision.
```

#### Plan positions for an approved selection

```text
Use $pickfolio in position mode. Read the frozen selection manifest at
/path/to/selection/manifest.json, then build a USD 1,000,000 position plan with
20% strategic cash, a 20% maximum-loss budget, single-name caps, shared-risk caps,
stress tests, and staged evidence gates. Do not replace the selected names.
```

#### Refresh sources without changing a frozen decision

```text
Use $pickfolio in refresh mode to update the existing run to the latest completed
US trading session. Preserve a new immutable snapshot, record successful and failed
source attempts, and produce change-report.md. Do not silently change the frozen basket.
```

#### Review an existing package

```text
Use $pickfolio in review mode to audit this selection and position package.
Prioritize unsupported facts, date or security-line mismatches, invalid peer
comparisons, missing-data treatment, gate violations, and weight reconciliation.
```

#### Choose how much intermediate data to retain

Add one of these instructions to any request:

```text
retain=minimal: keep reports, manifest, and source audit only.
retain=standard: also keep evidence matrices, normalized tables, calculations,
and key snapshots. This is the default.
retain=audit: also keep raw responses, page captures, complete logs, and failed attempts.
```

## Workflow

```text
Mandate and parameters
-> source snapshot and coverage audit
-> bottleneck tree and transmission paths
-> research universe and peer-group evidence
-> selected basket
-> explicit selection freeze
-> risk and role budgets
-> target positions and shared-risk caps
-> stress tests and staged evidence gates
-> monitoring and review
```

The skill stops between selection and position planning until a human explicitly freezes the selected basket.

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

`manifest.json` records parameters, dates, gate status, approvals, selected symbols, position state, output paths, and unresolved blockers.

## Optional Run Scaffolding

Create a parameterized run package:

```bash
python3 scripts/init_run.py \
  --config assets/project-config.example.json \
  --output-root ./runs \
  --slug ai-infrastructure \
  --mode full \
  --capital 5000000 \
  --currency USD \
  --retain standard
```

Validate a draft package:

```bash
python3 scripts/validate_run.py ./runs/YYYY-MM-DD-ai-infrastructure
```

Validate a completed package:

```bash
python3 scripts/validate_run.py --strict ./runs/YYYY-MM-DD-ai-infrastructure
```

## Directory Structure

```text
pickfolio/
├── SKILL.md
├── SKILL-zh.md
├── README.md
├── README.zh-CN.md
├── agents/
│   └── openai.yaml
├── assets/
│   ├── project-config.example.json
│   └── *.template.md
├── references/
│   ├── bottleneck-analysis.md
│   ├── data-governance.md
│   ├── output-contracts.md
│   ├── parameters.md
│   ├── position.md
│   ├── selection.md
│   ├── us-equities.md
│   └── workflow.md
└── scripts/
    ├── init_run.py
    └── validate_run.py
```

`SKILL.md` is the executable skill entry. `SKILL-zh.md` is the complete Simplified Chinese reader reference.

## Updating

If installed from `main`:

```bash
git -C "${CODEX_HOME:-$HOME/.codex}/skills/pickfolio" pull --ff-only
```

## Safety Boundaries

- Pickfolio produces research and position plans, not investment guarantees.
- It never places, modifies, or cancels orders.
- A research basket is not a position plan.
- Position sizing requires a frozen selection and an approved risk budget.
- Missing data remains missing and is never silently converted to zero.
- RPO, backlog, bookings, and book-to-bill remain separate metrics.
- Institutional, short, options, and crowding data trigger review; they do not independently dictate trades.
- Secrets, account credentials, and private broker data must not be committed to a run package.

## Chinese

For the full Chinese guide, see [README.zh-CN.md](README.zh-CN.md). For a line-by-line reader counterpart of the skill instructions, see [SKILL-zh.md](SKILL-zh.md).
