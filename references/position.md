# Position Planning

## Contents

- Objective and preconditions
- Risk and role budgets
- Within-role allocation and caps
- Stress tests and staged entry gates
- Monitoring and reconciliation

## Objective

Translate a frozen stock-selection decision into a cash-aware, capped, stress-tested, and staged position plan. Do not reopen stock selection inside this workflow.

## 1. Verify Preconditions

Require:

- Frozen selection manifest and selected symbols.
- Capital and currency.
- Holding horizon.
- Maximum tolerable loss or an explicit unresolved-risk status.
- Strategic cash floor.
- Leverage policy.
- Existing positions and account constraints.

Keep the position status `blocked` while material risk inputs are unresolved.

## 2. Set The Risk Budget

Define:

- Gross equity target.
- Strategic cash floor.
- Single-name maximum.
- Shared-risk-group maximums.
- Maximum tolerable drawdown or loss amount.
- Stress scenarios and the action each threshold triggers.

Treat capital as a ceiling, not an instruction to invest everything immediately.

## 3. Allocate Role Budgets

Budget portfolio roles before individual names. Judge each role by:

- Importance to the thesis.
- Ability to capture revenue and profit.
- Durability across the holding horizon.
- Evidence quality and observability.
- Distinctiveness from other roles.

Role importance does not automatically imply the largest weight.

## 4. Allocate Within Roles

Use company quality, cash generation, order visibility, customer quality, cycle sensitivity, and role fit to divide a role budget among frozen names.

When roles overlap, define a shared-risk group even if the companies operate in different subsegments.

## 5. Apply Caps And Feasibility Checks

Apply:

- Valuation cap.
- Volatility and drawdown cap.
- Single-name cap.
- Shared-risk cap.
- Liquidity and estimated market-impact check.
- Event and reporting-calendar constraints.
- Existing-portfolio overlap cap.

Use institutional ownership, short data, options, and crowding to form review questions. Do not let these fields silently override the approved weight logic.

## 6. Stress Test The Portfolio

At minimum show:

- Historical-window volatility and drawdown with dates.
- A mechanical simultaneous drawdown scenario.
- Shared-factor or correlated-group stress.
- Thesis-specific revenue, margin, order, or valuation compression scenarios.
- Loss amounts in portfolio currency.

Historical outcomes are examples, not future loss bounds.

## 7. Define Staged Entry Gates

Each stage must add independent evidence. For every stage record:

- Target completion percentage and amount.
- Fundamental gate.
- Valuation or price-risk gate.
- Event/calendar constraint.
- Cap reconciliation after the stage.
- Pause, downgrade, and thesis-failure conditions.

Do not use vague gates such as "stabilized" without a measurable definition. Do not treat a price decline as evidence that fundamentals improved.

## 8. Establish Monitoring Baselines

For each name and risk group, record:

- Baseline value and date.
- Review threshold.
- Required corroborating evidence.
- Review action.
- What the signal cannot prove.

Price thresholds should trigger review unless the mandate explicitly defines a tested execution rule.

## 9. Reconcile The Plan

Before approval verify:

```text
sum(name weights) + cash weight = 100%
each name <= single-name cap
each risk group <= shared-risk cap
stage amounts sum to each final name amount
stress loss <= approved loss budget, or the exception is explicit
```

Mark the plan `approved` only after explicit human approval. Pickfolio stops at the plan and never submits orders.
