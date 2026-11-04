---
title: 'Block storage: EBS and ESSD'
linkTitle: Block storage
description: Capacity, IOPS, throughput, commitment, snapshots, and instance-channel limits for AWS EBS gp3 and Alibaba ESSD.
weight: 30
---

> [!IMPORTANT]
> **Snapshot:** 2026-08-22 · AWS `us-east-1` · Alibaba Cloud `cn-hangzhou` ·
> `1 USD = 6.7817 CNY`. Exact rates vary by region. The comparison aligns
> provisioned capacity and requested IOPS/throughput, not latency or service level.

## Direct answer {#answer}

“Price per GB” is not a valid block-storage comparison by itself. It can rank
gp3 as cheaper at baseline and then reverse the answer once performance is
matched. A usable bill must price at least four things:

\[
\begin{aligned}
\text{monthly block cost} ={}& \text{capacity} + \text{IOPS} + \text{throughput} \\
&+ \text{snapshots and recovery} + \text{network path}
\end{aligned}
\]

The final usable performance is also bounded by the instance:

\[
\text{usable I/O} = \min(\text{volume limit}, \text{instance storage-channel limit})
\]

Paying for IOPS that the attached instance cannot deliver creates cost without
performance.

## Two pricing philosophies {#philosophies}

### AWS EBS gp3: capacity and performance are explicit meters {#gp3}

The snapshot uses:

- Capacity: `$0.08/GB-month` (`¥0.5425`).
- Included: `3,000 IOPS` and `125 MiB/s`.
- Extra IOPS: `$0.005/IOPS-month`.
- Extra throughput: `$0.04/MiB/s-month` in the exact `us-east-1` snapshot.

So:

\[
\begin{aligned}
C_{gp3} ={}& 0.08G + 0.005\max(I-3000,0) \\
&+ 0.04\max(T-125,0)
\end{aligned}
\]

All three are provisioned meters. Actual low usage does not refund unused
provisioned IOPS or throughput.

### Alibaba ESSD: capacity often carries a performance curve {#essd}

Traditional PL0–PL3 bind capacity to a product level. AutoPL separates capacity
from optional provisioned and burst performance, but capacity still includes a
rising baseline:

\[
I_{base}=\max(\min(1800 + 50G, 50000), 3000)
\]

\[
T_{base}=\max(\min(120 + 0.5G, 350), 125)
\]

At 200 GiB this yields 11,800 IOPS and 220 MB/s; at 2,048 GiB the baseline
reaches 50,000 IOPS and 350 MB/s. Alibaba's documentation also notes that the
attached instance can impose the lower I/O ceiling.

## Capacity meter alone {#capacity}

| Product | Capacity price | Included/baseline performance | PAYG-equivalent | 1 year | 3 years | 5 years |
| --- | ---: | --- | ---: | ---: | ---: | ---: |
| EBS gp3 | `¥0.5425/GiB-month` | 3K IOPS, 125 MiB/s | same list meter | contract-specific | contract-specific | contract-specific |
| ESSD PL0 | `¥0.50/GiB-month` | capacity-coupled | `¥0.7665` | `¥0.425` | `¥0.25` | `¥0.25` |
| ESSD PL1 / AutoPL | `¥1.00/GiB-month` | capacity-coupled to 50K / 350 | `¥1.533` | `¥0.85` | `¥0.50` | `¥0.50` |
| ESSD PL2 | `¥2.00/GiB-month` | higher level; minimum 461 GiB | `¥3.066` | `¥1.70` | `¥1.00` | `¥1.00` |
| ESSD PL3 | `¥4.00/GiB-month` | higher level; minimum 1,261 GiB | `¥6.132` | `¥3.40` | `¥2.00` | `¥2.00` |
{.wide .expand}

At this layer, gp3 is near PL0 and about 54% of PL1/AutoPL. That statement is
true but incomplete.

## Performance-matched scenarios {#matched}

| Capacity and target | EBS gp3 | ESSD AutoPL baseline | gp3 / AutoPL | Reading |
| --- | ---: | ---: | ---: | --- |
| 200 GiB · 3K IOPS · 125 MiB/s | `¥108.51/month` | `¥200.00/month` | `0.54×` | gp3 baseline is cheaper |
| 200 GiB · 11.8K IOPS · 220 MiB/s | `¥432.67/month` | `¥200.00/month` | `2.16×` | AutoPL capacity baseline is cheaper |
| 2,048 GiB · 50K IOPS · 350 MiB/s | `¥2,765.85/month` | `¥2,048.00/month` | `1.35×` | AutoPL remains cheaper at its baseline ceiling |
{.wide .expand}

This is the core block-storage insight: **the answer flips because one product
charges extra performance separately while the other bundles a capacity-driven
baseline.** It does not prove equal latency, durability, burst behavior, or
instance delivery.

The exact rows are in
[`block_storage_scenarios.csv`](/data/cloud-pricing/2026-08-22-v1/tables/block_storage_scenarios.csv).

## What the price table still hides {#hidden}

### Snapshots and recovery {#snapshots}

EBS snapshots bill changed blocks in S3-backed storage; cross-region copy,
archive retrieval, fast snapshot restore, time-bounded copy, and provisioned
initialization can add separate meters. ESSD snapshots, backup products, and
cross-region recovery have their own lifecycle and transfer costs. A recovery
budget needs restore time and restore throughput, not just snapshot GB-month.

### Topology and network {#topology}

A single cloud disk is an availability-zone resource. Cross-AZ database or
application topologies may duplicate volumes and add network charges. Managed
database storage can price capacity, IOPS, and throughput at different markup
factors from raw block storage.

### Provisioned versus consumed {#provisioned}

Both capacity and performance can be paid before they are used. Track:

- provisioned vs used GiB;
- provisioned vs observed P95/P99 IOPS;
- provisioned vs observed throughput;
- instance channel utilization;
- snapshot growth and orphan retention;
- commitment coverage and unused term value.

## Extreme-performance layers {#extreme}

At the high end, capacity is no longer the dominant meter. AWS io2 prices
provisioned IOPS by volume-level tiers. Alibaba ESSD PL-X similarly separates
capacity and IOPS; an official example for 2,048 GiB and two million IOPS totals
`¥152,048/month`, of which `¥150,000` is performance. Low-end disks monetize
capacity; high-end disks monetize performance.

## Historical insight {#history}

AWS gp2 to gp3 reduced capacity price only 20%, from `$0.10` to `$0.08/GB-month`.
For a 200 GiB volume, however, included baseline IOPS rose from 600 to 3,000,
cutting price per baseline IOPS by 84%. Alibaba's 2016 SSD and 2026 ESSD PL1
both anchor at `¥1/GB-month`; performance, reliability, and product semantics
improved while the capacity meter stayed flat.

This is why “storage prices did not fall” and “storage price-performance
improved sharply” can both be true. See [Cloud price history](/ledger/price-history/).

## A minimum bill worksheet {#worksheet}

Before comparing disks, fill one row per volume:

| Field | Required value |
| --- | --- |
| Region / AZ | Exact deployment path |
| Provisioned and used capacity | GiB, both values |
| IOPS | baseline, provisioned, P95/P99 observed |
| Throughput | baseline, provisioned, P95/P99 observed |
| Latency requirement | P50/P99 and block size |
| Instance channel | max IOPS and throughput |
| Snapshot and restore | changed GB, retention, RTO, copy path |
| Topology | number of volumes, replicas, AZs |
| Term | PAYG, monthly, 1/3/5 year, residual commitment |

If any of these is missing, a capacity-price ratio is a lead, not a conclusion.

## Boundaries {#boundaries}

- GB and GiB are retained exactly as providers publish them.
- AutoPL baseline does not imply the attached instance can deliver it.
- This comparison does not equalize latency, durability, burst, or SLA.
- AWS rates are regional and tax-exclusive; Alibaba China-site rates are tax-inclusive.
- Prices may have changed after 2026-08-22; refresh before purchase.

## Data and sources {#data}

- [Block-storage rates](/data/cloud-pricing/2026-08-22-v1/tables/block_storage_rates.csv)
- [Performance-matched scenarios](/data/cloud-pricing/2026-08-22-v1/tables/block_storage_scenarios.csv)
- [Full pricing report](/data/cloud-pricing/2026-08-22-v1/report.md)
- [Pricing source ledger](/data/cloud-pricing/2026-08-22-v1/tables/source_ledger.csv)
- [Checksums](/data/cloud-pricing/2026-08-22-v1/checksums.txt)
- [Original Chinese essay](https://vonng.com/cloud/ebs/)
