---
outputs: [HTML, RSS, print, markdown, LLMSFULL]
title: 证据档案
linkTitle: 档案
description: 按日期与证据等级整理故障、锁定机制与公开说法。
weight: 30
type: docs
icon: fa-solid fa-box-archive
sidebar_expanded: true
sidebar_root_for: self
sidebar_root_link_self: true
navbar_autohide: false
cascade:
  theme_color: '#7a2b3a'
  theme_color_dark: '#ef9aaa'
  type: docs
  navbar_autohide: false
  footer_style: fat
  comments: false
  feedback: false
---

> [!NOTE]
> 记录模板已经就绪，结构化的事故、锁定与声明记录尚未发布。来源评论可在[文章归档](/zh/blog/)阅读。

故障不是意外，而是中心化架构必然服从的物理定律。

当成千上万家企业的生产系统同时押注在同一套控制平面上，所谓的「五个九可用性」往往只停留在 SLA 赔付条款里——而在业务因云平台级故障中断数小时后，几张轻飘飘的代金券根本抵不上真实的商业信誉与业务停摆损失。

**实证风险档案**以可溯源的一手 RCA 事故报告、公开技术事实与时间戳为依据，真实记录公共云的单点集中风险与人为锁定机制：

## 三类核心档案 {#collections}

{{< cards >}}
  {{< card title="故障编年" link="/zh/evidence/outages/" icon="fa-solid fa-triangle-exclamation" badge="实证记录" >}}
重大云服务事故的完整时间线、影响范围、官方 RCA 根因追溯与后续技术整改跟踪。
  {{< /card >}}
  {{< card title="锁定图鉴" link="/zh/evidence/lock-in/" icon="fa-solid fa-link" badge="机制解构" >}}
剖析专有存储格式、消息队列、私有控制面与 IAM 权限网中常见的人为锁定套路与逃生解法。
  {{< /card >}}
  {{< card title="通稿核对" link="/zh/evidence/claims/" icon="fa-solid fa-quote-right" badge="真伪对照" >}}
将厂商销售公关宣传中的「无限弹性」与生产环境可观测到的真实故障数据并排对照。
  {{< /card >}}
{{< /cards >}}

## 证据纪律 {#discipline}

- **一手事实优先**：每条记录严格区分发生时间、一手官方报告与社区工程复核，拒绝道听途说。
- **留白与动态修正**：存在争议或厂商尚未彻底披露的细节如实保留，并附上跟进追踪；一旦厂商完成技术修复，同步更新状态。
- **去伪存真**：结构化提炼自 [vonng.com 云计算专栏](https://vonng.com/cloud/) 种子库与全球一线运维实践，中英双语对齐归档。

