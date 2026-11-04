---
title: 'Object storage: S3, OSS, and owned topology'
linkTitle: Object storage
description: Storage class, small-object tax, minimum duration, requests, retrieval, egress, resource packages, and reliable-topology break-even for object storage.
weight: 40
---

> [!IMPORTANT]
> **Snapshot:** 2026-08-22 · AWS `us-east-1` · Alibaba Cloud China mainland ·
> `1 USD = 6.7817 CNY`. Capacity rates, request policy, free allowances, and
> packages are time-sensitive. Self-hosted crossings exclude labor, software
> licenses, migration, and business-loss risk.

## Direct answer {#answer}

Object-storage capacity is now cheap and surprisingly close across providers.
The bill diverges elsewhere:

\[
\begin{aligned}
\text{monthly object cost} ={}& \text{billable capacity} + \text{requests} \\
&+ \text{retrieval} + \text{minimum-duration penalty} \\
&+ \text{replication} + \text{internet and cross-region transfer} \\
&+ \text{management features}
\end{aligned}
\]

For self-hosting, the corresponding denominator is not raw disk TB:

\[
\begin{aligned}
\text{raw requirement} ={}& \text{logical data} \times \text{EC or replica overhead} \\
&\times \text{free-space reserve} \times \text{site copies} \\
&+ \text{spares} + \text{replication network}
\end{aligned}
\]

That is why object-storage economics do not have one universal “cloud exit
size.” The first question is the minimum reliable topology.

## Current capacity rates {#rates}

| Storage class | AWS `us-east-1` | CNY equivalent | Alibaba OSS LRS |
| --- | ---: | ---: | ---: |
| Standard | `$0.023/GB-month` | `¥0.156` | `¥0.120` |
| Infrequent access | `$0.0125` | `¥0.0848` | `¥0.080` |
| Glacier Instant / Archive | `$0.004` | `¥0.0271` | `¥0.033` |
| Glacier Flexible / Cold Archive | `$0.0036` | `¥0.0244` | `¥0.015` |
| Deep Archive / Deep Cold Archive | `$0.00099` | `¥0.0067` | `¥0.0075` |

The rows are price-adjacent, not service-equivalent. Retrieval latency,
availability, durability topology, restore workflow, and feature semantics
differ.

## The small-object tax {#small-objects}

Cold tiers often bill a minimum object size:

| Service class | Minimum billable object | Minimum storage duration | Extra metadata |
| --- | ---: | ---: | ---: |
| S3 Standard-IA / One Zone-IA | `128 KB` | `30 days` | — |
| S3 Glacier Instant | `128 KB` | `90 days` | — |
| S3 Glacier Flexible / Deep Archive | object bytes | `90 / 180 days` | `40 KB/object` |
| OSS IA / Archive / Cold / Deep Cold | `64 KB` | `30 / 60 / 180 / 180 days` | product-specific |

A 1 KB object can therefore consume 128× or 64× its logical size on the bill;
a 10 KB object consumes 12.8× or 6.4×. Before moving data to a colder tier,
measure object-count distribution, average and percentile size, overwrite/delete
rate, and retention—not just total TB.

## Activity meters {#activity}

### Requests {#requests}

Snapshot reference rates:

- S3 Standard PUT/COPY/POST/LIST: `$0.005 / 1,000 requests`.
- S3 Standard GET: `$0.0004 / 1,000 requests`.
- OSS Standard: first 5 million PUT and 20 million GET per region-month free,
  then `¥0.01 / 10,000`; IA/Archive PUT/GET commonly `¥0.10 / 10,000`.
- OSS Deep Cold PUT: `¥3.50 / 10,000`.

Request policy can change quickly, and console browsing itself can issue GET or
LIST requests. High object count can matter even when capacity is small.

### Retrieval and early deletion {#retrieval}

Snapshot examples:

- S3 Standard-IA retrieval: `$0.01/GB`; Glacier Instant: `$0.03/GB`.
- OSS IA: `¥0.0325/GB`; Archive: `¥0.06/GB`; Cold Archive standard
  retrieval: `¥0.06/GB`; Deep Cold standard: `¥0.018/GB`.

Deleting, overwriting, or transitioning before the minimum duration can charge
the remaining term. An archive restore can also create a temporary hot copy
that is billed while accessible.

### Transfer: the exit and delivery meter {#transfer}

| Path | Snapshot price |
| --- | ---: |
| AWS aggregate internet egress | first 100 GB free; next 10 TB `$0.09/GB` (`¥0.610/GB`) |
| AWS same-region cross-AZ | commonly `$0.01/GB` each direction |
| Alibaba ECS internet egress, Hangzhou | `¥0.80/GB` |
| Alibaba OSS busy / off-peak internet egress | `¥0.50 / ¥0.25 per GB` |
| Alibaba OSS to CDN origin | `¥0.15/GB` |

The same download has a different price from ECS, OSS busy time, OSS off-peak,
or CDN. Draw the full data path before pricing. For provider exit, also check
documented waiver eligibility and operational lead time; a conditional waiver
is not the same as a zero-rate default.

## Packages and commitment risk {#packages}

Alibaba OSS Standard LRS 100 GB illustrates the package ladder:

| Purchase | Total / equivalent | Relative to PAYG |
| --- | ---: | ---: |
| PAYG capacity | `¥12/month` | `100%` |
| Monthly package | `¥11/month` | `91.7%` |
| Six-month package | `¥54.78 total` | about `76.1%` monthly equivalent |
| One-year package | `¥99 total` | `68.8%` monthly equivalent |

Unused capacity expires; region, redundancy type, and meter mismatch can prevent
deduction. A package lowers nominal unit price only when its scope and usage fit.

## Self-hosting begins with topology {#topology}

The released scenario uses 75% erasure-code efficiency, 80% maximum safe fill,
5% spare-drive inventory, 5% monthly data change, and one practical 1 Gbps port
per 100 TB/month of remote replication.

| Topology | Minimum nodes / sites | What it can represent |
| --- | ---: | --- |
| Four-node lower bound | 4 / one site | Historical capacity floor; not a current full production baseline |
| Eight-node single site | 8 / one site | Current production host lower bound; node/disk failure domain |
| Eight-node dual site | 16 / two sites | Complete remote copy plus replication network |
| Eight-node three site | 24 / three sites | Conservative multi-failure-domain approximation |
| Backblaze-style Vault | 20 / 20 racks | 17+3 erasure coding across rack failure domains |
{.wide .expand}

None is automatically equivalent to S3 Standard's service level. Durability,
availability, API semantics, operations, audit, and recovery must be tested
separately.

## Unit cost by topology {#unit-cost}

| Logical capacity | Eight-node single site | Dual site | Three site | 20-rack Vault |
| ---: | ---: | ---: | ---: | ---: |
| 100 TB | `¥0.1786/GB-month` | `¥0.4822` | `¥0.7759` | `¥1.0005` |
| 200 TB | `¥0.0893` | `¥0.2411` | `¥0.3879` | `¥0.5002` |
| 500 TB | `¥0.0357` | `¥0.0964` | `¥0.1552` | `¥0.2001` |
| 1 PB | `¥0.0179` | `¥0.0482` | `¥0.0776` | `¥0.1001` |
| 2 PB | `¥0.0145` | `¥0.0346` | `¥0.0550` | `¥0.0500` |
| 5 PB | `¥0.0113` | `¥0.0301` | `¥0.0481` | `¥0.0254` |
| 10 PB | `¥0.0111` | `¥0.0280` | `¥0.0451` | `¥0.0181` |
{.wide .expand}

At 100 TB the eight-node pool is mostly empty. Around 200 TB it approaches an
OSS one-year package; at 1 PB its single-site capacity cost is about one fifth
of that package. Adding sites changes the answer because hardware and replication
network are duplicated.

## First and durable capacity crossings {#crossings}

| Owned topology | AWS S3 Standard list | Alibaba OSS PAYG | Alibaba OSS one-year package |
| --- | ---: | ---: | ---: |
| Four-node single-site lower bound | `55 TB` | `71 TB` | `95 TB` |
| Eight-node single-site production baseline | `115 TB` | `149 TB` | `199 TB` |
| Eight-node dual site | `310 TB` | `402 TB` | `536 TB` |
| Eight-node three site, first / durable | `498 / 498 TB` | `647 / 647 TB` | `863 / 1,223 TB` |
| 20-node / 20-rack Vault | `642 TB` | `834 TB` | `1,112 TB` |
{.wide .expand}

These are **capacity plus replication-network material crossings**. S3/OSS
requests, retrieval, and small-object overhead are excluded on the cloud side;
commercial software, support, load balancers, security, and internal labor are
excluded on the owned side.

### Sensitivity versus OSS one-year package {#sensitivity}

| Change | Eight-node single | Dual site | Three-site durable |
| --- | ---: | ---: | ---: |
| Baseline | `199 TB` | `536 TB` | `1,223 TB` |
| Hardware -25% | `169 TB` | `476 TB` | `1,047 TB` |
| Hardware +25% | `229 TB` | `597 TB` | `1,399 TB` |
| Safe fill 60% | `199 TB` | `536 TB` | `2,363 TB` |
| Monthly change 20% | `199 TB` | `1,047 TB` | `7,665 TB` |
| High facility price | `224 TB` | `587 TB` | `1,300 TB` |

Single-site capacity is insensitive to write churn; multi-site storage is not.
High-churn data can make network replication dominate and may belong in a
database, block store, or shared filesystem instead.

## Historical insight {#history}

S3 Standard fell from `$0.15/GB-month` in 2006 to `$0.023` in 2016, then stayed
flat through the snapshot. Alibaba OSS Standard directory price reached
`¥0.12` in 2018; a durable public effective rate of `¥0.09` appeared in 2024.
Capacity followed a hardware-like early decline, then became a platform meter.
Egress and activity did not follow the same curve. See [Cloud price history](/ledger/price-history/).

## Decision zones {#decision}

| Workload | Baseline tendency |
| --- | --- |
| `<100–200 TB`, uncertain growth | Cloud object storage avoids the minimum pool |
| `~0.2 PB+`, one-site capacity need | Eight-node owned capacity enters the economic range |
| `~0.5 PB+`, two-site copy | Formal owned comparison becomes worthwhile |
| `~0.9–1.3 PB+`, three-site / rack fault domains | Reliable-topology owned economics can cross normal cloud capacity rates |
| `20–25 TB/month+` stable delivery | Compare fixed transit/CDN path against per-GB egress separately |
| Global edge, DDoS, volatile demand | Keep CDN and elastic edge even if origin capacity is owned |

Cloud exit does not require rejecting CDN, edge, or managed security. A common
efficient design owns stable origin capacity and continues buying statistically
pooled distribution.

## Boundaries {#boundaries}

- Capacity crossings are not SLA or durability certifications.
- Four-node MinIO is retained only as a lower-bound reference.
- Commercial object software and internal operations are excluded from the baseline.
- DHH's observed S3 contract uses billed footprint; primary logical data gives a different denominator.
- Request policy, packages, and prices can change after 2026-08-22.

## Data and sources {#data}

- [Current storage-class rates](/data/cloud-pricing/2026-08-22-v1/tables/object_storage_rates.csv)
- [Current transfer rates](/data/cloud-pricing/2026-08-22-v1/tables/traffic_rates.csv)
- [Object scale curve](/data/build-vs-buy/2026-08-24-v1/tables/object_scale_curve.csv)
- [Object breakpoints](/data/build-vs-buy/2026-08-24-v1/tables/object_breakpoints.csv)
- [Object sensitivity](/data/build-vs-buy/2026-08-24-v1/tables/object_one_way_sensitivity.csv)
- [Full pricing report](/data/cloud-pricing/2026-08-22-v1/report.md)
- [Full build-versus-buy report](/data/build-vs-buy/2026-08-24-v1/report.md)
- [Original Chinese essay](https://vonng.com/cloud/s3/)
