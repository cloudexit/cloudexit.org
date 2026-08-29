---
title: Rating method
linkTitle: Method
description: Scope, evidence hierarchy, scoring states, review cadence, expiry, correction, and appeal for the Cloud Exit Standard.
weight: 60
---

> [!IMPORTANT]
> Method status: **v0.1 draft**. It is suitable for calibration and public
> review, not yet for issuing a badge.

## Unit of assessment {#unit}

The unit is **provider + product + region + commercial plan + review date**.
Company-wide claims are prohibited unless every material product and region in
scope has been tested. A result can therefore differ across regions, storage
classes, or contract types from the same provider.

## Result states {#states}

| State | Meaning |
| --- | --- |
| Pass | Evidence satisfies the criterion in the stated scope. |
| Partial | A practical path exists, but a material limitation remains. |
| Fail | Evidence shows the criterion is not satisfied. |
| Unknown | Evidence is missing, inaccessible, contradictory, or not yet tested. |
| Stale | The review is older than its validity window. |

Unknown is not a failure. Stale is not silently converted into the last known
result.

## Evidence hierarchy {#evidence}

1. Contract, official price page, technical documentation, incident report, or machine-readable provider data.
2. Reproducible measurement with inputs, date, region, account class, and raw output.
3. First-party operating account with a named organization and bounded workload.
4. Independent reporting with links to primary evidence.
5. Editorial analysis, clearly labeled and never sufficient by itself for a rating.

Every citation records a collection date. Screenshots preserve transient price
or policy states but do not replace a stable URL when one exists.

## Review flow {#flow}

1. **Scope** the exact product, region, plan, and features under test.
2. **Collect** primary sources and archive the source window.
3. **Reproduce** export, interface, or price tests where access permits.
4. **Review** every C1–C5 field and record dissent or unknowns.
5. **Notify** the provider or maintainer of the factual draft when a contact is available.
6. **Publish** the result, evidence bundle, review date, and expiry date together.
7. **Revisit** material changes and the scheduled review window.

The dataset target is a quarterly release. Each individual rating expires after
180 days unless its sources are rechecked. This prevents a missed quarterly
release from presenting old information as current.

## Corrections and appeals {#appeals}

Anyone may submit contrary evidence. A valid appeal identifies the exact field,
scope, date, and primary source or reproducible test. Factual corrections are
made promptly with a visible revision note. Method disagreements are recorded
and considered for the next standard version; they do not rewrite an old test
after seeing the result.

## Conflicts of interest {#conflicts}

The initiator, Ruohang Feng, sells commercial support for Pigsty, a self-hosted
PostgreSQL platform, and may benefit from decisions to self-host databases.
Named commercial tools must repeat relevant disclosures on the page that names
them. Reviewers record employment, investment, sponsorship, consulting, and
competitive interests. Disclosure does not make a claim correct; it lets the
reader price the risk while checking the evidence.

## Versioning policy {#versioning}

- Standard changes use semantic document versions: major for incompatible criteria, minor for new fields or thresholds, patch for clarifications.
- Dataset releases use a date plus revision and never overwrite a prior published snapshot.
- Provider results point to the exact standard and dataset versions used.
- The registry shows stale and withdrawn states instead of erasing history.

