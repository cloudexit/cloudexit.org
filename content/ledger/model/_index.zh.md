---
title: 模型契约
linkTitle: 模型
description: 比较按量服务与自有/托管机房基础设施时统一使用的会计口径。
weight: 10
---

> [!NOTE]
> 模型输出已作为带日期快照发布；它们仍然是情景，不是实时报价。

## 两个成本函数 {#functions}

\[
C_{\mathrm{cloud}}(t) = C_{\mathrm{usage}} + C_{\mathrm{managed}} + C_{\mathrm{commitment}} + C_{\mathrm{exit}}
\]

\[
C_{\mathrm{owned}}(t) = C_{\mathrm{capital}}/t + C_{\mathrm{facility}} + C_{\mathrm{network}} + C_{\mathrm{labor}} + C_{\mathrm{software}} + C_{\mathrm{risk}}
\]

比较周期 \(t\)、汇率日期、税务口径、资金成本与残值必须显式写出。
现金成本与经济成本分开显示，不能混成一个看不出假设的数字。

## 同口径规则 {#like-for-like}

匹配可用容量、可用性、耐久性、备份、恢复目标、运维覆盖、安全控制、地域与需求曲线。
如果无法建立等价条件，就给出两个有边界的情景，而不是一个虚假精确的倍数。

## 必须输出 {#outputs}

- 月度与累计成本曲线。
- 按规模与按时间计算的盈亏平衡点。
- 对利用率、硬件寿命、人力、电力、资金与增长的敏感性。
- 现金成本、经济成本与退出成本三个视角。
- 适用边界与未计入成本。

任何“自建便宜 X 倍”的结论，都必须和让 \(X\) 成立的工作负载与假设一起出现。
