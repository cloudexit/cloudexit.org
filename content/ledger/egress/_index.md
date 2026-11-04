---
title: Egress and network paths
linkTitle: Egress
description: Internet transfer, cross-AZ traffic, NAT processing, free allowances, CDN paths, fixed bandwidth, and the per-GB versus port break-even.
weight: 50
---

> [!IMPORTANT]
> **Snapshot:** 2026-08-22. Network prices vary by region, path, direction,
> tier, and contract. A public transit port is not service-equivalent to cloud
> egress; the comparison exposes the different cost curves.

## Direct answer {#answer}

Network is its own bill, not an attachment to compute or storage. The same byte
can be free on ingress, charged twice across an availability-zone round trip,
processed by NAT, and charged again on internet egress.

\[
\begin{aligned}
\text{network bill} ={}& \sum(\text{bytes} \times \text{path rate}) \\
&+ \text{hourly gateways} + \text{processing} + \text{ports and IPs}
\end{aligned}
\]

Draw the path before applying a rate.

## Current reference paths {#rates}

| Provider / service | Path | Snapshot rate |
| --- | --- | ---: |
| AWS aggregate services | First internet egress allowance | `100 GB/month free` outside China/GovCloud |
| AWS aggregate services | Next 10 TB internet egress | `$0.09/GB` (`¥0.610/GB`) |
| AWS EC2/RDS | Same-region cross-AZ | commonly `$0.01/GB` each direction |
| AWS NAT Gateway | Processing | `$0.045/GB` + `$0.045/hour` reference |
| AWS public IPv4 | Address | `$0.005/hour` |
| Alibaba ECS Hangzhou | Internet egress by traffic | `¥0.80/GB` |
| Alibaba OSS | Busy / off-peak internet egress | `¥0.50 / ¥0.25 per GB` |
| Alibaba OSS | CDN origin egress | `¥0.15/GB` |
| Alibaba cross-AZ NAT | Processing CU | `¥0.23/GB-equivalent` + `¥0.23/hour` |

AWS aggregates egress tiers across many services and regions; eligibility and
exceptions matter. Alibaba same-region VPC product communication is often free,
but NAT, CEN, EIP, load balancers, cross-region links, and public paths introduce
their own meters.

## Fixed bandwidth versus per GB {#port}

The self-transit scenario uses a public 1 Gbps line at `¥12,500/month` and a
conservative practical load of `100 TB/month`—about 30% of theoretical line
rate. This is a procurement anchor, not a universal market price.

| Monthly egress | Required 1G ports | Port cost | Effective port ¥/GB | AWS `$0.09` | Alibaba ECS `¥0.8` | Alibaba OSS busy `¥0.5` |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 10 TB | 1 | `¥12,500` | `¥1.250` | `¥6,104` | `¥8,000` | `¥5,000` |
| 20 TB | 1 | `¥12,500` | `¥0.625` | `¥12,207` | `¥16,000` | `¥10,000` |
| 25 TB | 1 | `¥12,500` | `¥0.500` | `¥15,259` | `¥20,000` | `¥12,500` |
| 50 TB | 1 | `¥12,500` | `¥0.250` | `¥30,518` | `¥40,000` | `¥25,000` |
| 100 TB | 1 | `¥12,500` | `¥0.125` | `¥61,035` | `¥80,000` | `¥50,000` |
| 500 TB | 5 | `¥62,500` | `¥0.125` | `¥305,177` | `¥400,000` | `¥250,000` |
{.wide .expand}

Break-even volume is:

\[
V_{break} = \frac{\text{port monthly price}}{\text{cloud egress price per GB}}
\]

| Comparison | Material crossing |
| --- | ---: |
| AWS `$0.09/GB` | `~20.5 TB/month` |
| Alibaba ECS `¥0.8/GB` | `~15.6 TB/month` |
| Alibaba OSS busy `¥0.5/GB` | `25 TB/month` |

The cloud curve starts at zero and scales with bytes. The port curve starts with
a fixed step and then has near-zero marginal bytes until the next port. Bursty,
uncertain, global, or DDoS-exposed traffic may justify the cloud/CDN premium;
stable bulk transfer crosses early.

## Alibaba fixed public bandwidth {#fixed-bandwidth}

The public Hangzhou example prices 1 Mbps fixed bandwidth around `¥23/month`
versus `¥0.8/GB` by traffic. They cross at `23 / 0.8 = 28.75 GB/month`.
One Mbps can theoretically deliver about 328.5 GB/month, so fixed bandwidth
becomes cheaper at roughly 8.8% utilization. Peak entitlement and service
quality remain different from a by-traffic peak cap.

## Architecture consequences {#architecture}

- Use an S3 Gateway Endpoint instead of routing S3 traffic through AWS NAT when applicable.
- Avoid accidental cross-AZ round trips for chatty application/database paths.
- Price ECS, OSS busy/off-peak, and CDN-origin delivery as separate exits.
- Keep stable origin and backup capacity on fixed or private paths; keep global
  edge, CDN, DDoS, and volatile traffic on statistically pooled services.
- Track IPv4, idle NAT, orphan load balancers, and cross-region replication as
  first-class meters.

## Exit capability {#exit}

Provider exit waivers can materially change C1, but only when eligibility,
covered services, destination, notice, transfer window, and approval process are
documented. A negotiated or conditional waiver is recorded separately from the
default meter. The operational export path and time limit remain part of the
test even when the rate is zero.

## Historical insight {#history}

AWS marginal egress fell from `$0.20/GB` in 2006 to `$0.09` in 2014, then
remained flat through the snapshot. Alibaba ECS Hangzhou stayed at `¥0.8/GB`
across the report's 2016–2026 anchors. Silicon and disk gains do not automatically
flow into the network meter. See [Cloud price history](/ledger/price-history/).

## Boundaries {#boundaries}

- Port procurement lacks the cloud platform's global backbone, elasticity,
  routing, DDoS, operations, and zero-startup option.
- The 1 Gbps quote and 100 TB practical load are scenario inputs.
- Taxes, installation, private contracts, and regional fees can move crossings.
- All rates must be refreshed after the snapshot before procurement.

## Data and sources {#data}

- [Cloud transfer rates](/data/cloud-pricing/2026-08-22-v1/tables/traffic_rates.csv)
- [Egress scale curve](/data/build-vs-buy/2026-08-24-v1/tables/egress_scale_curve.csv)
- [Pricing source ledger](/data/cloud-pricing/2026-08-22-v1/tables/source_ledger.csv)
- [Build-versus-buy source ledger](/data/build-vs-buy/2026-08-24-v1/tables/source_ledger.csv)
