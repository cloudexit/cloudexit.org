---
outputs: [HTML, RSS, print, markdown, LLMSFULL]
title: Cloud Cost Ledger
linkTitle: Ledger
description: A source-backed ledger of compute, block storage, object storage, egress, commitments, break-even points, and long-run bill composition.
weight: 20
type: docs
icon: fa-solid fa-calculator
sidebar_expanded: true
sidebar_root_for: self
sidebar_root_link_self: true
navbar_autohide: false
cascade:
  theme_color: '#724100'
  theme_color_dark: '#e3a15f'
  type: docs
  navbar_autohide: false
  footer_style: slim
  comments: false
  feedback: false
---

Cloud bills are not one price. They are a stack of resource meters, topology,
activity, time commitments, and commercial terms. The ledger makes that stack
visible and then asks where the money actually goes.

> [!IMPORTANT]
> **Price snapshot:** 2026-08-22 · **Research completed:** 2026-08-24 ·
> **Primary regions:** AWS `us-east-1`, Alibaba Cloud `cn-hangzhou` ·
> **FX:** 1 USD = 6.7817 CNY · **Month:** 730 hours. All amounts below are
> dated public-price or scenario values, not live quotes or enterprise net prices.

## The bill in one formula {#formula}

\[
\begin{aligned}
\text{Effective cost} ={}&
\sum(\text{usage} \times \text{unit price} \times \text{topology} \times \text{term}) \\
&+ \text{activity} + \text{network} + \text{support} + \text{tax} \\
&- \text{credits}
\end{aligned}
\]

The denominator matters just as much:

\[
\text{Effective unit cost} = \frac{\text{cash bill}}{\text{useful business output}}
\]

A 50% commitment used at only 60% coverage has an effective price of
`0.50 / 0.60 = 83.3%` of on-demand—not 50%. Discounts can lower the invoice
while raising stranded-value and exit risk.

## Six findings that survive the details {#findings}

| Finding | Audited number | What it establishes | What it does **not** establish |
| --- | ---: | --- | --- |
| Compute scales linearly inside a family | AWS `c7i/m7i/r7i` same-vCPU price factors are about `0.885 / 1 / 1.313`; Alibaba `c9i/g9i/r9i` about `0.779 / 1 / 1.330` | Larger shapes do not automatically buy cheaper cores | Equal vCPU labels mean equal workload performance |
| Elasticity has a visible premium | Alibaba `g9i.large` PAYG at 730 hours is `1.521×` its monthly price; time-only crossing is `65.8%` utilization | PAYG and monthly are different risk products | Monthly is always cheaper after workload and commitment risk |
| Block-storage rankings flip with performance | 200 GiB baseline: gp3 `¥108.51`, AutoPL `¥200`; at 11.8K IOPS / 220 MiB/s: gp3 `¥432.67`, AutoPL `¥200` | Capacity-only comparisons can reverse the answer | Either service is performance-equivalent for every instance or latency profile |
| Object capacity rates have converged | S3 Standard `¥0.156/GB-month`; OSS Standard LRS `¥0.120` | Capacity alone is no longer the whole bill | Requests, retrieval, minimum duration, small objects, or egress are equivalent |
| Reliable topology sets the self-host threshold | Versus OSS one-year package: 8-node single site `199 TB`; dual site `536 TB`; three-site durable crossing `1,223 TB` | Object-storage break-even is a topology question | A single-site pool equals S3's service level |
| Mature bills decline slower than compute | AWS capacity basket 2008→2026: `-63.0%`; Alibaba monthly basket 2016→2026: `-4.8%` | Flat storage/egress meters dilute compute gains | The two baskets are performance- or SLA-equivalent |
{.wide .expand}

## Three bill surfaces {#surfaces}

### Compute: price the useful core {#compute}

Instance size mostly changes the number of objects you operate, not the price
per vCPU inside a family. Architecture, memory ratio, region, generation, and
purchase term change it materially. The [compute ledger](/ledger/compute/)
publishes current reference shapes, regional factors, commitment crossings,
and the discrete self-hosted scale curve.

### Block storage: price capacity and performance together {#block}

For gp3, capacity, IOPS, and throughput are separate meters. For ESSD AutoPL,
capacity carries a rising baseline and performance can add further meters. The
[block-storage ledger](/ledger/block-storage/) shows the same three scenarios
at equal capacity **and** requested performance, plus the instance-channel
ceiling that can make paid IOPS unusable.

### Object storage: price activity and exit, not just TB {#object}

The object bill is storage class + billable object size + minimum duration +
requests + retrieval + replication + transfer. The [object-storage ledger](/ledger/object-storage/)
adds the self-hosted minimum reliable topology, so `100 TB`, `500 TB`, and
`1 PB` are not treated as the same engineering problem.

## The long-run insight {#history}

Cloud prices fell quickly in early competition, then many core marginal rates
plateaued. AWS S3 Standard has stayed at `$0.023/GB-month` since 2016; AWS
internet egress at `$0.09/GB` since 2014; Alibaba ESSD PL1 capacity at
`¥1/GiB-month` and ECS egress at `¥0.8/GB` across the report's 2016–2026
anchors. Compute kept improving, but users usually had to migrate generation,
architecture, or purchase model to capture it.

Read [Cloud price history](/ledger/price-history/) for the full index and bill
baskets.

## Decision rule {#decision}

1. Build a 90–180 day workload fingerprint: hourly compute, capacity, IOPS,
   throughput, object sizes, requests, retrieval, and every network path.
2. Separate stable floor, predictable peak, interruptible work, and stateful data.
3. Match topology and useful performance before comparing prices.
4. Price commitment utilization and stranded value, not the advertised discount.
5. Compare public price, actual invoice, and self-hosted procurement as three
   separate layers.
6. Use a break-even point as permission to start engineering evaluation—not as
   an automatic migration order.

## Released data {#data}

{{< dataset-catalog >}}

Each release contains the full report, source ledger, CSV/JSON tables,
methodology, schema summary, and SHA-256 checksums. The highlighted pages link
directly to their exact source tables.
