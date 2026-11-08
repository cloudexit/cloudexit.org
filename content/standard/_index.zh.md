---
outputs: [HTML, RSS, print, markdown, LLMSFULL]
title: 下云能力标准
linkTitle: 标准
description: 用五条可证伪判据，检查一项服务是否保留了客户实际离开的能力。
weight: 10
type: docs
icon: fa-solid fa-scale-balanced
sidebar_expanded: true
sidebar_root_for: self
sidebar_root_link_self: true
navbar_autohide: false
cascade:
  theme_color: '#164b63'
  theme_color_dark: '#78c5e6'
  type: docs
  navbar_autohide: false
  footer_style: fat
  comments: false
  feedback: false
---

上云容易下云难。难的从来不是业务代码，而是云厂商精心构筑的专有接口、惩罚性出网流量费与暗度陈仓的商业锁定条款。

**下云能力标准 (Cloud Exit Standard)** 是一套由真实工程实践驱动的可证伪检验体系。它不听公关包装，只验证一个最根本的工程事实：**当你决定离开时，这项服务是否保留了你实际逃生的能力？**

## 五条核心判据 {#criteria}

任何合格的云上架构，都必须经受住以下五项基本检验：

| 判据 | 考察维度 | 核心检验问题 | 需要收集的证据 |
| :--- | :--- | :--- | :--- |
| **[C1 · 无退出罚金](/zh/standard/c1-no-exit-toll/)** | 经济主权 | 离开时是否会被收取惩罚性的出网带宽或数据提取费？ | 完整迁出费用、正常交付成本、豁免与资格；判定阈值尚待校准 |
| **[C2 · 数据整体导出](/zh/standard/c2-whole-data-export/)** | 数据资产 | 能否在有限时间内导出完整、无损且可重建的业务数据？ | 数据与必要元数据、恢复验证、耗时和限速 |
| **[C3 · 接口走公开标准](/zh/standard/c3-standard-interfaces/)** | 架构自由 | 核心数据存取与运维接口，能否用开源协议直接替代？ | 公开规范、独立实现以及所需语义的差异 |
| **[C4 · 无承诺捆绑](/zh/standard/c4-no-commitment-lock/)** | 商业对等 | 长期用量折扣是否沦为了不可解约的人身契？ | 期限、利用率、未履约余额、退款、转移与解约规则 |
| **[C5 · 停机有账可查](/zh/standard/c5-accountable-downtime/)** | 可靠性实证 | 平台重大故障的根因分析、实际停机时长与赔付是否可审计？ | 事故时序、影响、解释、修复措施与合同承诺的救济 |
{.wide .expand}

每条判据遵循同一工程结构：**清晰定义 → 验证命令 → 真实算例 → 边界与反驳**。所有评估只针对具体产品、地域、API 行为与公开复核日期，不代表对任何企业的永久定论。

## 这份标准不是什么 {#not}

- **不是盲目反云的狂热口号**：公共云在业务初创期和高弹性场景依然极具价值；我们反对的是人为制造的迁出壁垒，而不是算力本身。
- **不是安全认证或销售排行**：它不评估厂商的销售规模，也不代替企业评估自身当前的采购决策。
- **不从 Logo 与公司光环推导结论**：无论是巨头还是小厂，只看可复现的技术行为与公开账本。

[评测方法](/zh/standard/method/)定义证据、复核、有效期与申诉流程。[厂商名录](/zh/standard/registry/)在评估通过该流程前保持为空，目前尚未发布任何厂商评级。
