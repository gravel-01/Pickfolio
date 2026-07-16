# US Equities

## Scope

Version 1 targets US-listed equities and explicitly identified ADR or OTC lines. Treat an exchange listing, ADR, and foreign primary listing as different security lines even when they represent the same company.

## Benchmark Selection

Use a benchmark that matches the mandate:

- `SPY` or another S&P 500 proxy for broad large-cap comparison.
- `QQQ` for Nasdaq-100 growth exposure.
- `IWM` for US small-cap exposure.
- Sector or theme ETFs only for direction and peer context.

Record whether returns are price-only or total return. Do not use an ETF's performance to assign an individual stock weight directly.

## Primary Company Sources

Prefer:

- SEC submissions and filing archives for 10-K, 10-Q, 8-K, 20-F, 6-K, and proxy filings.
- SEC Company Facts for structured XBRL fields, followed by filing-level verification.
- Company investor-relations filings, earnings releases, and presentations.
- Exchange or regulator datasets for market-structure fields.

Read filing exhibits when an 8-K only points to the substantive disclosure. A filing event does not automatically require a financial-denominator update.

## Fiscal Comparability

US companies may have different fiscal year ends. Record the fiscal period and end date for every annual or quarterly comparison. Do not label a company's fiscal 2026 result as calendar 2026 without explanation.

Keep GAAP, non-GAAP, reported, and adjusted fields separate.

## ADR And Foreign Listings

For each line record:

- Primary exchange and local ticker.
- US ADR or OTC ticker.
- ADR ratio.
- Reporting currency and price currency.
- Whether ownership, volume, shares, and filings refer to the ADR or global company.

Do not combine the primary line's shares with the ADR price without an explicit conversion. Do not use an ADR's 13F coverage as global institutional ownership.

## Ownership And Market Structure

- Treat 13F as a delayed snapshot of reportable US institutional holdings, not complete ownership.
- Preserve holding date and filing date separately.
- Deduplicate original and amended filings by manager and report period.
- Verify current SEC value units before aggregation.
- Keep institutional count, reported value, shares, concentration, and ownership percentage distinct.
- Keep short interest separate from daily short-sale volume.
- Treat option volume, open interest, IV, and put/call as separate observations.

These signals support risk review and disagreement analysis. They do not independently prove company quality or predict price direction.

## Market Dates

Resolve the most recent completed regular trading session rather than assuming the research date is a market date. Record timezone and session. Keep extended-hours data separate unless the mandate explicitly uses it.

## Corporate Actions

Check splits, reverse splits, mergers, spin-offs, ticker changes, special distributions, and listing changes before comparing historical prices, shares, or valuation fields.

## Trading Boundary

Pickfolio produces research and position plans only. Do not call trading endpoints, submit orders, manage broker state, or treat a report as execution authorization.
