---
title: 'Compute: EC2, ECS, and owned servers'
linkTitle: Compute
description: Current EC2/ECS reference prices, family and region factors, commitment economics, and the discrete break-even curve for stable owned compute.
weight: 20
---

> [!IMPORTANT]
> **Snapshot:** 2026-08-22 · AWS `us-east-1` prices exclude applicable tax ·
> Alibaba Cloud `cn-hangzhou` public prices include China-site tax ·
> `1 USD = 6.7817 CNY`, 730 hours/month. Prices are not performance benchmarks.

## Direct answer {#answer}

Inside a mainstream instance family, price is almost linear in vCPU. Buying a
larger shape reduces instance count, not unit-core price. The variables that
move unit cost are memory ratio, CPU architecture, generation, region, purchase
term, and—most importantly—useful utilization.

For stable owned compute, the material-cost curve falls rapidly while the first
server fills, jumps when active and spare servers are added, then flattens. The
economic question is not “how large is the company?” but “can this workload keep
the minimum reliable pool usefully full for the asset life?”

## Current 2C8G reference shapes {#reference}

| Offer | Billing | Native price | 730-hour month | CNY / vCPU-month |
| --- | --- | ---: | ---: | ---: |
| AWS `m8i.large`, 2C8G | On-demand | `$0.10584/h` | `$77.26` | `¥261.99` |
| Alibaba `g9i.large`, 2C8G | Monthly | — | `¥238.60` | `¥119.30` |
| Alibaba `g9i.large`, 2C8G | PAYG | `¥0.4971/h` | `¥362.88` | `¥181.44` |
{.wide .expand}

The raw cash-price ratio is not a procurement conclusion. `m8i` and `g9i` differ
in CPU, network, storage channel, regional context, tax, and business
performance. Normalize with application TPS, latency, compile throughput, or
another useful output before choosing.

## The family skeleton {#families}

Same-vCPU prices reveal a repeatable memory-ratio structure:

| Family | Shape | Monthly reference | Relative to general purpose |
| --- | ---: | ---: | ---: |
| AWS `c7i.large` | 2C4G | `$65.15` | `0.885` |
| AWS `m7i.large` | 2C8G | `$73.58` | `1.000` |
| AWS `r7i.large` | 2C16G | `$96.58` | `1.313` |
| Alibaba `c9i.large` | 2C4G | `¥185.91` | `0.779` |
| Alibaba `g9i.large` | 2C8G | `¥238.60` | `1.000` |
| Alibaba `r9i.large` | 2C16G | `¥317.48` | `1.330` |

Moving from `large` to `xlarge` or `2xlarge` inside the same family remains
nearly linear. Exceptions—burstable CPU, local disks, dedicated hosts, bare
metal, GPUs, NUMA, and commercial licenses—carry separate fixed or step meters.

## Architecture, generation, and region {#factors}

The snapshot's price factors are meaningful only as provider pricing intent:

- AWS `m7g/m7i = 0.810`; `m8g/m8i = 0.848`. Graviton is 15–19% cheaper in
  list price, but application compatibility and useful performance decide value.
- Alibaba Yitian `g8y.large` is `¥192/month`, versus Intel `g8i.large` at
  `¥251.16`; current long-term discounts can still change the total ordering.
- AWS `m8i.large` regional factor ranges from `1.000` in core US regions to
  `1.250` Singapore, `1.292` Tokyo, and `1.594` São Paulo.
- Alibaba `g9i.large` is at factor `1.000` in Hangzhou/Shanghai/Beijing,
  `0.900` Ulanqab, `1.770` Singapore, `1.798` Tokyo, and `1.929` Hong Kong.

Region is not a coupon code. Data sovereignty, latency, service coverage,
disaster-recovery topology, and cross-region traffic can dominate the instance
factor.

## Elasticity and commitment {#commitment}

Alibaba `g9i.large` PAYG at 730 hours costs `¥362.88`, or `1.521×` the
`¥238.60` monthly price. The time-only crossing is:

\[
\frac{238.60 / 0.4971}{730} = 65.8\%\text{ of the month}
\]

For any commitment factor \(f\) and realized utilization \(u\):

\[
\text{effective discount} = 1 - \frac{f}{u}
\]

A five-year term and a purchased server both transfer demand risk to the
customer. Compare unused commitment, generation lock, cash opportunity cost,
residual value, failure replacement, and exit terms—not just the discount.

## The owned-compute curve {#owned}

The scenario uses a DHH-class 2U server with 192 vCPU, 384 GiB RAM, fleet-average
19.2 TB local NVMe, purchase price about `¥169,500`, five-year life, and 70%
target fill. A spare is added from the second active server onward. Internal
labor, migration, application changes, and business risk are excluded.

| Stable business vCPU | Total servers | Cash material cost / vCPU-month |
| ---: | ---: | ---: |
| 16 | 1 | `¥220.36` |
| 32 | 1 | `¥110.18` |
| 64 | 1 | `¥55.09` |
| 128 | 1 | `¥27.54` |
| 192 | 3 | `¥55.09` |
| 512 | 5 | `¥40.15` |
| 1,000 | 9 | `¥31.63` |
| 4,000 | 32 | `¥27.56` |
| 64,000 | 501 | `¥22.89` |

The first server filling from 16 to 128 vCPU cuts unit cost eightfold. Expanding
from 4,000 to 64,000 vCPU—16× more scale—cuts it only another 17%. Most scale
economy arrives at the beginning; later results are driven by utilization and
hardware life.

## First and durable crossings {#crossings}

| Cloud comparison | Cloud CNY / vCPU-month | First below cloud | Durable below cloud |
| --- | ---: | ---: | ---: |
| AWS `c7a` on-demand | `¥254.07` | `14 vCPU` | `14 vCPU` |
| AWS `c7a` 3-year Standard RI proxy | `¥100.32` | `36 vCPU` | `36 vCPU` |
| Alibaba `c8i` PAYG | `¥148.81` | `24 vCPU` | `24 vCPU` |
| Alibaba `c8i` 5-year public term | `¥29.35` | `121 vCPU` | `2,972 vCPU` |

“First” means one fill interval becomes cheaper. “Durable” means later server,
spare, rack, and network steps no longer push cost back above the cloud line.
The AWS RI row uses an `m7i` discount factor as a proxy for `c7a`, not a quoted
`c7a` RI offer.

### Sensitivity: why the five-year comparison is fragile {#sensitivity}

| Change | AWS 3-year durable crossing | Alibaba 5-year durable crossing |
| --- | ---: | ---: |
| Baseline | `36 vCPU` | `2,972 vCPU` |
| 50% target utilization | `106 vCPU` | no durable crossing below `200,000 vCPU` |
| 85% target utilization | `36 vCPU` | `984 vCPU` |
| Hardware price -25% | `29 vCPU` | `724 vCPU` |
| Hardware price +25% | `43 vCPU` | `12,634 vCPU` |
| Three-year hardware life | `162 vCPU` | no durable crossing below `200,000 vCPU` |
| Seven-year hardware life | `28 vCPU` | `701 vCPU` |

Against expensive on-demand compute, reasonable scenarios cross early. Against
a deep five-year term near hardware amortization, utilization and asset life can
change the answer by orders of magnitude.

## Decision zones {#decision}

| Stable workload | Baseline reading |
| --- | --- |
| `<16 vCPU` | On-demand cloud usually wins the fixed-cost problem |
| `16–64 vCPU` | Owned material cost can beat PAYG; short commitments may still win |
| `64–134 vCPU` | High-fill single-server sweet spot; still a single failure domain unless designed otherwise |
| `134–600 vCPU` | Expansion sawtooth matters; quote the actual server and spare plan |
| `600–3,000 vCPU` | Owned compute is durable versus 1–3 year terms; five-year outcome depends on fill |
| `3,000+ vCPU` | Under baseline life/fill, owned material cost is durably below all modeled offers |

Cloud remains strongest for unknown duration, high peak/mean ratio, global
small footprints, interruptible work, and rapid release. Owned compute is
strongest for stable, long-lived, standardized workloads with existing
procurement and operations capability.

## Historical context {#history}

AWS ~2C8G advertised-capacity price fell 73.5% from 2007 to 2026, but almost all
list-price decline occurred before 2017. Alibaba 2C8G monthly price fell only
21.0% from 2016 to 2026 while PAYG fell 62.1%, largely by narrowing the
elasticity premium. Mature FinOps therefore means benchmarking and migrating,
not waiting for automatic cuts. See [Cloud price history](/ledger/price-history/).

## Data and sources {#data}

- [Current EC2 reference shapes](/data/cloud-pricing/2026-08-22-v1/tables/aws_ec2_reference.csv)
- [Current ECS reference shapes](/data/cloud-pricing/2026-08-22-v1/tables/aliyun_ecs_reference.csv)
- [Compute scale curve](/data/build-vs-buy/2026-08-24-v1/tables/compute_scale_curve.csv)
- [Compute breakpoints](/data/build-vs-buy/2026-08-24-v1/tables/compute_breakpoints.csv)
- [Compute sensitivity](/data/build-vs-buy/2026-08-24-v1/tables/compute_one_way_sensitivity.csv)
- [Full pricing report](/data/cloud-pricing/2026-08-22-v1/report.md)
- [Full build-versus-buy report](/data/build-vs-buy/2026-08-24-v1/report.md)
