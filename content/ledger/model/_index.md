---
title: Model contract
linkTitle: Model
description: The common accounting frame for comparing metered services with owned or colocated infrastructure.
weight: 10
---

> [!NOTE]
> Model outputs are released as dated snapshots. They remain scenarios, not live quotes.

## Two cost functions {#functions}

\[
C_{\mathrm{cloud}}(t) = C_{\mathrm{usage}} + C_{\mathrm{managed}} + C_{\mathrm{commitment}} + C_{\mathrm{exit}}
\]

\[
C_{\mathrm{owned}}(t) = C_{\mathrm{capital}}/t + C_{\mathrm{facility}} + C_{\mathrm{network}} + C_{\mathrm{labor}} + C_{\mathrm{software}} + C_{\mathrm{risk}}
\]

The comparison period \(t\), currency date, tax treatment, financing cost, and
residual value must be explicit. Cash cost and economic cost are shown
separately rather than blended.

## Like-for-like rule {#like-for-like}

Match usable capacity, required availability, durability, backup, recovery
objective, operations coverage, security controls, region, and demand shape.
When parity cannot be established, publish two bounded scenarios rather than
one false-precision ratio.

## Required outputs {#outputs}

- Monthly and cumulative cost curves.
- Break-even scale and break-even time.
- Sensitivity to utilization, hardware life, labor, power, financing, and growth.
- Cash, economic, and exit-cost views.
- Applicability boundaries and omitted costs.

The claim is never “self-hosting is X times cheaper” without the workload and
assumptions that make \(X\) true.
