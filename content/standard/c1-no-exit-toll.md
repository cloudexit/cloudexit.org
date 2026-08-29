---
title: C1 · No exit toll
linkTitle: C1 · No exit toll
description: Test whether leaving triggers charges that are disproportionate to delivery cost or ordinary use.
weight: 10
---

> [!CAUTION]
> Draft criterion, version 0.1. No provider result is implied by this page.

## Definition {#definition}

A service passes C1 when a customer can move customer-owned data to another
operator without charges that are disproportionate to ordinary delivery cost
or that make exit economically impractical. The assessed path must be available
at useful bulk-transfer scale, not only as a token free allowance.

## How to verify {#verify}

1. Define the full export volume, request count, retrieval class, region, and deadline.
2. Price every required read, retrieval, API request, transfer, appliance, and support item.
3. Compare exit cost with normal monthly service cost and with an independently procurable transfer path.
4. Record waivers, eligibility limits, notice periods, and whether the customer must negotiate.

## Worked example {#example}

For data volume \(D\), retrieval price \(R\), request cost \(Q\), and transfer
price \(E\):

\[
\text{exit cost} = D(R + E) + Q + \text{required service fees}
\]

The draft method reports the absolute cost, months of ordinary service cost,
and cost per exported unit. A pass/fail threshold will not be fixed until the
first public calibration set has been reviewed.

## Boundaries and objections {#boundaries}

- Network delivery has a real cost; C1 does not require every transfer to be free.
- A documented, automatic exit waiver can count, but a discretionary sales concession cannot.
- Physical transfer appliances can qualify if capacity, lead time, and total cost are practical.
- A low storage price does not offset an exit toll; the two are reported separately.

