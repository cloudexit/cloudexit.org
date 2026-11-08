# Existing asset → cloudexit.org content map

This file is the intake queue. A source listed here is not automatically a
published claim. It must be normalized under the target page's evidence
contract.

## Research workspaces

| Existing asset in `../cloud/` | Target | Intended use | Intake status |
| --- | --- | --- | --- |
| `research/cloud-build-vs-buy-2026/` | `/ledger/model/`, compute, RDS, object, egress | Assumptions, scale curves, breakpoints, sensitivity, source ledger | Released snapshot `2026-08-24-v1` |
| `research/cloud-pricing-2026/` | `/ledger/*` | AWS/Aliyun compute, RDS, block/object storage, traffic and commitment rates | Released snapshot `2026-08-22-v1` |
| `research/cloud-price-history-2026/` | `/ledger/price-history/` | Long-run price anchors, workload baskets, physical-input context | Released snapshot `2026-08-24-v1` |
| `data/ec2/`, `data/rds/`, `data/ecs/` | `/ledger/data/` | Raw regional price snapshots and catalog inputs | Needs public schema/license review |
| `ui/cloud-cost/` | Future calculator | Existing interactive model behavior and input vocabulary | Reuse model, not code by default |
| `ui/cloud-exit/index.html` | Cases + ledger narrative | Data-first presentation, formulas, break-even and scope | Editorial source, not canonical data |
| `output/pdf/*.pdf` | Future downloads | Rendered research artifacts | Publish only beside source data and verification |

## Existing essays

| Essay | URL | Primary target | Treatment |
| --- | --- | --- | --- |
| 剖析阿里云服务器算力成本 | https://vonng.com/cloud/ecs/ | `/ledger/compute/` | Practitioner anchors; replace historical quotes with dated current data |
| 云盘是不是杀猪盘？ | https://vonng.com/cloud/ebs/ | `/ledger/block-storage/` | Preserve original period; rebuild current comparison |
| 扒皮云对象存储：从降本到杀猪 | https://vonng.com/cloud/s3/ | `/ledger/object-storage/`, C1 | Separate storage, request, retrieval, and exit transfer |
| 云数据库是不是智商税 | https://vonng.com/cloud/rds/ | `/ledger/managed-markup/` | Split resource cost from managed-service value |
| FinOps终点是下云 | https://vonng.com/cloud/finops/ | `/ledger/model/`, `/playbook/negotiation/` | Reframe opinion as testable cost and option-value claims |
| 重新拿回计算机硬件的红利 | https://vonng.com/cloud/bonus/ | `/ledger/compute/`, cases | Hardware and Tantan/DHH anchors with dated scope |
| 数据主权宣言 | https://vonng.com/cloud/data-sovereignty-manifesto/ | Site principles, `/playbook/data-first/` | Values source; not evidence for a provider result |
| 下云数据库自建：从手艺活到工业化 | https://vonng.com/cloud/self-hosting-industrialized/ | `/playbook/staging/`, cases | Operational pattern and conflict disclosure required |

The full [cloud essay index](https://vonng.com/cloud/) provides a large seed
corpus for outages, migration, cost, sovereignty, and lock-in. It is mirrored
in `/blog/` as authored commentary, together with 35 reviewed cross-column
essays on local AI and sovereignty, open data and local-first software,
self-hosted data stacks, infrastructure capability, PostgreSQL platforms, and
Pigsty self-hosting.

The exact snapshot is recorded in `data/blog/imports.json`: 123 Cloud-column
articles plus 35 cross-column articles, with the source commit, source URLs,
language coverage, copied files, byte counts, and SHA-256 digests. The selection
and transformation logic lives in `scripts/import-vonng-blog.py`.

Archive inclusion is not evidence normalization. When an essay supports a
Standard, Ledger, Evidence, Case, or Playbook claim, extract a record, retain
the original URL, add an English abstract where needed, and label observation
versus commentary.

## Initial case candidates

| Candidate | Why useful | Main risk before publication |
| --- | --- | --- |
| DHH / 37signals compute exit | Multiple first-party updates with hardware and savings anchors | Scope changes across posts; preliminary and final numbers must not be mixed |
| DHH / 37signals S3 exit | Clear daily/annual cost pressure and two-site hardware scope | Contract price, billed capacity, logical capacity, and acquired capacity differ |
| Tantan | Locally familiar IDC/compute economics | Need first-party scope, date, and workload confirmation |
| Ahrefs | Large-scale non-cloud infrastructure narrative | Reported savings need applicability and methodology boundaries |
| Partial or reversed exits | Protects the library from success-only bias | Harder sourcing; must not infer motives from absence of public detail |

## Outage intake

Start with incidents that have at least one provider status page, incident
report, contract/SLA artifact, or independently verifiable primary record.
Existing commentary tagged 故障复盘 is a discovery index, not sufficient by
itself for C5.

## Publication order

1. Normalize source ledgers and dates.
2. Publish one dataset family with schema, checksum, and reproducible formula.
3. Publish 3–5 incident records that exercise the revision and uncertainty fields.
4. Calibrate C1–C5 on a small mixed provider set without badges.
5. Publish cases only after reported, modeled, verified, and inferred values are separated.
