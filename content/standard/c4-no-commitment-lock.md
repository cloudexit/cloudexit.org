---
title: C4 · No commitment lock
linkTitle: C4 · No commitment lock
description: Test whether discounts, credits, and term contracts preserve a practical economic path out.
weight: 40
---

> [!CAUTION]
> Draft criterion, version 0.1. No provider result is implied by this page.

## Definition {#definition}

A service passes C4 when commercial commitments do not turn an otherwise
portable workload into an economically stranded one. Commitments are not a
failure by themselves; the test measures term, unused balance, scope,
transferability, cancellation, and the penalty created by leaving early.

## How to verify {#verify}

Record contract duration, committed spend, eligible products, utilization
assumption, prepayment, refund and transfer rules, renewal behavior, and the
unused obligation at each plausible exit date. Compare the committed effective
price with both on-demand cost and the cost of leaving.

## Worked example {#example}

A three-year discount can lower unit price while increasing total exit cost.
The ledger therefore shows at least two values: effective unit cost while the
commitment is fully used, and stranded value if the workload exits at month 6,
12, 18, or 24.

## Boundaries and objections {#boundaries}

- Voluntary commitments can be rational financing choices; the standard does not forbid them.
- Credits tied to one product family are reported differently from credits transferable across the portfolio.
- A nominal cancellation path is not practical if it requires discretionary approval or forfeits most remaining value.

