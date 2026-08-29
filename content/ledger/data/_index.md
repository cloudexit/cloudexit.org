---
title: Dataset releases
linkTitle: Data
description: Versioned cloud-price, build-versus-buy, and price-history snapshots with reports, source ledgers, full tables, methodology, schemas, and checksums.
weight: 70
---

Every number highlighted in the ledger points to a dated release. A release is
immutable: a correction creates a new version rather than overwriting the old
bytes.

{{< dataset-catalog >}}

## Release contents {#contents}

Each version contains:

```text
README.md             scope, dates, units, and reuse warning
release.json          machine-readable version and status
report.md             complete human-readable analysis
methodology.md        comparison and normalization rules
schema.json           table keys and unit conventions
tables/               all CSV and JSON inputs/outputs plus source ledger
charts/               reproducible report charts where available
checksums.txt          SHA-256 for every released file
```

## Three complementary datasets {#three}

### Cloud pricing · `2026-08-22-v1` {#pricing}

Current-reference AWS and Alibaba Cloud tables for EC2/ECS, EBS/ESSD, S3/OSS,
network, PostgreSQL RDS, commitments, and managed-database curves.

- [Release notes](/data/cloud-pricing/2026-08-22-v1/README.md)
- [Full report](/data/cloud-pricing/2026-08-22-v1/report.md)
- [Source ledger](/data/cloud-pricing/2026-08-22-v1/tables/source_ledger.csv)
- [Checksums](/data/cloud-pricing/2026-08-22-v1/checksums.txt)

### Build versus buy · `2026-08-24-v1` {#build}

Discrete cost curves, first and durable crossings, and sensitivity tables for
compute, PostgreSQL, object storage, and fixed-port egress. Baseline internal
labor and migration cost are deliberately excluded.

- [Release notes](/data/build-vs-buy/2026-08-24-v1/README.md)
- [Assumptions](/data/build-vs-buy/2026-08-24-v1/tables/assumptions.json)
- [Full report](/data/build-vs-buy/2026-08-24-v1/report.md)
- [Source ledger](/data/build-vs-buy/2026-08-24-v1/tables/source_ledger.csv)
- [Checksums](/data/build-vs-buy/2026-08-24-v1/checksums.txt)

### Price history · `2026-08-24-v1` {#history}

Long-run public-price anchors, nominal and real indexes, workload bill baskets,
physical-input context, and historical source records from 2006–2026.

- [Release notes](/data/price-history/2026-08-24-v1/README.md)
- [Full report](/data/price-history/2026-08-24-v1/report.md)
- [Long-run metrics](/data/price-history/2026-08-24-v1/tables/long_run_metrics.csv)
- [Source ledger](/data/price-history/2026-08-24-v1/tables/source_ledger.csv)
- [Checksums](/data/price-history/2026-08-24-v1/checksums.txt)

## Status semantics {#status}

`released-snapshot` means the files ship with the site and pass checksum and
headline-value verification. It does **not** mean the price is current today,
that a provider supplied a formal quote, or that two services are fully
equivalent. Use the snapshot date and applicability note whenever quoting a
value.

The machine-readable release index is at [`/data/index.json`](/data/index.json).

