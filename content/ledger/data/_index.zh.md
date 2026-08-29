---
title: 数据版本
linkTitle: 数据
description: 带完整报告、来源账、全量表、方法、schema 与校验和的版本化云定价、自建对比和价格历史快照。
weight: 70
---

账本中的每个醒目数字都指向一份带日期的数据版本。版本不可变；纠错会产生新修订，
不会覆盖旧字节。

{{< dataset-catalog >}}

## 每个版本包含什么 {#contents}

```text
README.md             范围、日期、单位与复用提醒
release.json          机器可读版本与状态
report.md             完整人类可读分析
methodology.md        比较与归一化规则
schema.json           表主键与单位约定
tables/               全部 CSV/JSON 输入输出与来源账
charts/               已有的可复现报告图表
checksums.txt          每个发布文件的 SHA-256
```

## 三份互补数据集 {#three}

### 云定价 · `2026-08-22-v1` {#pricing}

AWS 与阿里云 EC2/ECS、EBS/ESSD、S3/OSS、网络、PostgreSQL RDS、承诺和托管数据库曲线。

- [版本说明](/data/cloud-pricing/2026-08-22-v1/README.md)
- [完整报告](/data/cloud-pricing/2026-08-22-v1/report.md)
- [来源账](/data/cloud-pricing/2026-08-22-v1/tables/source_ledger.csv)
- [校验和](/data/cloud-pricing/2026-08-22-v1/checksums.txt)

### 自建与购买 · `2026-08-24-v1` {#build}

计算、PostgreSQL、对象存储与固定端口流量的离散成本曲线、第一次/稳定交点与敏感性。
基准刻意不计内部人力与迁移项目成本。

- [版本说明](/data/build-vs-buy/2026-08-24-v1/README.md)
- [假设](/data/build-vs-buy/2026-08-24-v1/tables/assumptions.json)
- [完整报告](/data/build-vs-buy/2026-08-24-v1/report.md)
- [来源账](/data/build-vs-buy/2026-08-24-v1/tables/source_ledger.csv)
- [校验和](/data/build-vs-buy/2026-08-24-v1/checksums.txt)

### 云价历史 · `2026-08-24-v1` {#history}

2006–2026 长期公开价格锚点、名义与实际指数、工作负载账单篮子、物理投入背景和历史来源。

- [版本说明](/data/price-history/2026-08-24-v1/README.md)
- [完整报告](/data/price-history/2026-08-24-v1/report.md)
- [长期指标](/data/price-history/2026-08-24-v1/tables/long_run_metrics.csv)
- [来源账](/data/price-history/2026-08-24-v1/tables/source_ledger.csv)
- [校验和](/data/price-history/2026-08-24-v1/checksums.txt)

## 状态语义 {#status}

`released-snapshot` 表示文件已经进入站点构建，并通过校验和与关键值复算；
它**不**代表今天的当前价格，不代表厂商正式报价，也不代表两项服务完全等价。
引用数字时必须同时带快照日期与适用边界。

机器可读版本索引见 [`/data/index.json`](/data/index.json)。

