# 云的价格究竟是怎样炼成的

## AWS 与阿里云基础资源定价体系、折扣机制与 PostgreSQL 数据库经济学

**研究截止：** 2026-08-24  
**价格快照：** 2026-08-22  
**主样本地域：** AWS `us-east-1`，阿里云 `cn-hangzhou`  
**统一口径：** Linux、PostgreSQL、公开价格、730 小时/月；美元兑人民币 6.7817  
**目标读者：** 基础设施负责人、PostgreSQL 架构师、FinOps、采购与企业财务负责人

> 这份报告回答的不是“哪家云更便宜”这种没有配置与边界的问题，而是更基础也更有用的问题：云厂商到底出售哪些计费原子，如何把地域、拓扑、性能、时间承诺和商务合同组合成最终价格，以及怎样把 RDS、Aurora、PolarDB 与自建 PostgreSQL 放在同一个经济模型里比较。

## 执行摘要

### 一句话答案

AWS 与阿里云的价格表看似繁杂，底层却可以归结为同一个六层模型：

`有效成本 = 资源用量 × 地域/代际/架构价格 × 可用性拓扑 × 活动型计费 + 时间承诺 + 商务与财务外层`

其中最容易被忽略的不是实例单价，而是副本数、性能费、跨可用区流量、请求与取回费、承诺浪费、支持费、税与汇率。官网价格只是模型的第一层，不是企业实际成本。

### 最重要的十个结论

1. **主流云服务器实例在同一实例族内基本按 vCPU 线性定价。** 规格变大通常不会带来单位核折扣。真正改变单位价格的是内存配比、CPU 架构、实例代际、地域、操作系统与购买方式。这个规律既存在于用户 2024 年的阿里云研究，也被 2026 年 AWS 和阿里云价格快照再次验证。[用户既有研究](https://vonng.com/cloud/ecs/)

2. **AWS 与阿里云采用相似的 c/g/r 价格骨架。** AWS `c7i/m7i/r7i` 的同核价格系数约为 `0.885/1/1.313`。阿里云 `c9i/g9i/r9i` 的包月同核系数约为 `0.779/1/1.330`。这不是厂商公开的 CPU 与内存拆分价格，而是从打包实例中反推的稳定经验系数。

3. **阿里云“按量价约等于包月价的 1.5 倍”仍然成立。** `ecs.g9i.large` 当前包月 238.60 元，按量 0.4971 元/小时；连续运行 730 小时的按量成本为 362.88 元，是包月的 1.521 倍。因而包月相对按量的纯时间利用率盈亏平衡点约为 `480/730 = 65.8%`。

4. **容量单价不能单独代表块存储成本。** AWS EBS gp3 的容量价只有 0.08 美元/GB/月，但超过 3,000 IOPS 与 125 MiB/s 后分别收费。阿里云 ESSD AutoPL/PL1 包月为 1 元/GiB/月，但 200 GiB 容量自带约 11,800 IOPS 与 220 MB/s。按 200 GiB、11,800 IOPS、220 MB/s 对齐，EBS gp3 约 432.67 元/月，而 ESSD AutoPL 基准容量为 200 元/月。只看每 GB 会得出相反结论。[AWS EBS 定价](https://aws.amazon.com/ebs/pricing/)，[ESSD AutoPL 性能公式](https://help.aliyun.com/zh/ecs/user-guide/essd-autopl-disks)

5. **对象存储的容量价格已经高度趋同，真正拉开账单的是请求、取回、最短存储期与流量。** 按 6.7817 汇率，AWS S3 Standard 约 0.156 元/GB/月，阿里 OSS Standard LRS 为 0.12 元；S3 Deep Archive 约 0.0067 元，OSS 深度冷归档为 0.0075 元。冷存储的表面价格差很小，但访问模型错误会让取回和提前删除费用吞掉全部节省。[AWS S3 定价](https://aws.amazon.com/s3/pricing/)，[阿里云 OSS 当前价目](https://cn.aliyun.com/price/detail/oss)

6. **流量是独立的收费网络，不是服务器附属项。** AWS 全球商业区域每月前 100 GB 聚合公网出流免费，之后前 10 TB 为 0.09 美元/GB；同地域跨 AZ 通常双向各收 0.01 美元/GB。阿里云杭州 ECS 按流量公网出方向为 0.8 元/GB，OSS 忙时 0.5 元/GB、闲时 0.25 元/GB、CDN 回源 0.15 元/GB。NAT、负载均衡、IPv4 与跨区路径还会叠加处理费。[AWS EC2 数据传输](https://aws.amazon.com/ec2/pricing/on-demand/)，[阿里云 ECS 公网带宽](https://help.aliyun.com/zh/ecs/public-bandwidth/)

7. **AWS RDS 的管理溢价必须在同拓扑节点数下计算。** 2026-08-22 快照中，PostgreSQL RDS Single-AZ 对同名 EC2 的计算价格比为 1.77 至 2.23；经典 Multi-AZ 同时把计算和存储乘 2，因此与“两台 EC2 + 两份 EBS”相比，计算溢价仍是 1.77 至 2.23，而不是误导性的 3.5 至 4.5 倍。[AWS RDS Multi-AZ 计费语义](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/USER_OnDemandDBInstances.html)

8. **AWS RDS 的不同计费原子有不同管理系数。** 官方 `us-east-1` Price List 显示，RDS PostgreSQL gp3 相对相同节点数的 EBS gp3，容量系数为 1.4375、额外 IOPS 系数为 4、额外吞吐系数为 2。RDS 不是一个统一的“2 倍价”，而是这些系数按工作负载权重加权后的结果。[AWS RDS 官方地域价目](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonRDS/20260820203529/us-east-1/index.json)

9. **阿里云 RDS 的公开按量价与 ECS 的关系明显不同于 AWS。** 杭州当前独享 4C16G 高可用 RDS 与两台同架构 ECS 对比，计算系数约 1.37 至 1.40；RDS 双节点 ESSD 容量价反而约为两份 ECS ESSD 的 0.81。以倚天独享高可用为例，存储达到约 803 GiB 后，RDS 的“计算 + 容量”公开按量价可低于两台 ECS + 两份 ESSD。通用型 RDS 甚至接近平价，但共享 CPU 与非保证 I/O 不能和独享 ECS 视作性能等价。[阿里云 RDS 规格族](https://help.aliyun.com/zh/rds/apsaradb-rds-for-postgresql/primary-apsaradb-rds-for-postgresql-instance-types/)

10. **折扣不是赠品，而是风险交换。** 厂商用折扣换取需求确定性、现金前置与迁移黏性；客户承担闲置、技术代际、未来降价、错误规格与现金机会成本。任何承诺价格因子 `f` 的最低利用率盈亏平衡点就是 `f`。例如 0.50 的承诺价只有在利用率高于 50% 时才优于按量；利用率 70% 时实际节省只有 `1 - 0.50/0.70 = 28.6%`，不是宣传的 50%。[FinOps Foundation 承诺折扣框架](https://www.finops.org/wg/commitment-based-discounts-overview/)

## 1. 研究边界与口径

### 1.1 比较对象

本报告覆盖：

- 计算：AWS EC2，阿里云 ECS。
- 块存储：AWS EBS gp3/io2，阿里云 ESSD PL0-PL3、AutoPL、PL-X。
- 对象存储：AWS S3，阿里云 OSS。
- 网络：公网出流、同地域跨区、跨地域、NAT、固定带宽与按流量。
- PostgreSQL 托管数据库：Amazon RDS for PostgreSQL、Alibaba Cloud RDS PostgreSQL。
- 云原生数据库：Amazon Aurora PostgreSQL、PolarDB PostgreSQL。
- 折扣与商务：按量、Spot/抢占式、包月、RI、Savings Plans、资源包、企业合同、优惠券、支持费、税与汇率。

不展开 GPU、Windows/商业数据库许可证、专线、CDN 完整产品、云安全产品、Marketplace 软件费与 AWS 中国区。它们可以用相同模型追加，但会把报告的核心关系淹没。

### 1.2 主样本与货币

- AWS 主样本为 `us-east-1`，因为它通常是全球公有云的价格基准地域。
- 阿里云主样本为 `cn-hangzhou`，与用户既有文章和本地 Cloud Cost Lab 一致。
- AWS 金额以美元、不含适用税费；阿里云中国站价格与账单已含税，常见云服务发票税率为 6%。[AWS 税费口径](https://aws.amazon.com/rds/postgresql/pricing/)，[阿里云含税口径](https://help.aliyun.com/zh/user-center/user-guide/request-an-invoice)
- 换算使用 2026-08-21 中国外汇交易中心公布的中间价 `1 USD = 6.7817 CNY`。实际付款汇率、套保与跨境结算成本应作为独立输入。[人民币市场汇价](https://www3.xinhuanet.com/20260821/7332c02bc5dd460ab1007db61330491c/c.html)

### 1.3 证据等级

本报告按以下优先级取证：

1. 云厂商 Price List、官方价格页、计费与架构文档。
2. SEC 年报、公司财报与官方账单字段说明。
3. FinOps Foundation 等透明方法论。
4. 用户文章、公开采购披露与行业经验仅作边界或案例，不冒充当前统一市场价。

本地 2026-08-22 快照覆盖 621 万条 EC2 价格、66 万条 RDS 价格、EBS/S3 官方 meter、阿里云 ECS/ESSD/流量导出、RDS 动态报价与 OSS 官方页面。所有关键结论都保留 SKU、地域、单位与抓取日期。

## 2. 云价格的统一模型

### 2.1 六层计价堆栈

云账单可以拆为六层：

1. **资源层：** vCPU、内存、GPU、容量、IOPS、吞吐、请求、数据取回、流量。
2. **产品层：** 实例族、CPU 架构、代际、存储类型、对象存储等级、数据库引擎。
3. **空间层：** Region、AZ、跨区、跨地域、国内与海外。
4. **拓扑层：** 单节点、主备、三节点、读副本、共享存储、副本数与 SLA。
5. **时间层：** 按秒、按小时、包月、1 年、3 年、5 年、Spot、资源包。
6. **商务财务层：** 企业合同、私有价格、券、Credits、支持计划、税、汇率、资金成本与闲置。

对任意架构，可写成：

`账单成本 = Σ(用量_i × 公共单价_i × 拓扑倍数_i × 时间价格因子_i) + 活动费 + 网络费 + 支持费 + 税费 - 券与 Credits`

但企业真正关心的是：

`有效单位成本 = 账单现金成本 / 有效业务用量`

如果买了 100 单位但只用 60 单位，利用率为 60%，即使账单单价打了 5 折，有效单位成本仍是按量价的 `0.5/0.6 = 83.3%`，实际只节省 16.7%。

### 2.2 三个不能混淆的“价格”

- **目录价：** 标准价目，便于锚定与合同计算。
- **公开成交价：** 官网活动、包年包月、Savings Plans、资源包后的价格。
- **企业有效价：** 合同折扣、券、返佣、Credits、支持费、税、汇率与闲置全部计入后的真实单位成本。

阿里云官方账单术语明确区分“目录价、官网折扣价、企业合同折扣价”。[阿里云费用术语](https://help.aliyun.com/zh/user-center/product-overview/billing-terminology) AWS 也区分 before-discount、after-discount 与带既有合同/承诺的 bill estimate。[AWS 折扣后费率语义](https://docs.aws.amazon.com/cost-management/latest/userguide/pc-rates-discounts.html)

## 3. EC2 与 ECS 算力定价规律

### 3.1 同族线性：规格越大并不自动更便宜

在主流 c/g/r 实例族内，`large`、`xlarge`、`2xlarge` 的价格基本与 vCPU 数成正比。由此得到两个实操结论：

- 垂直扩容不会因“批量采购更多核”获得单位折扣。
- 大规格降低的是实例数量、网络连接和运维对象数，不是核单价。

例外包括 Dedicated Host、带本地盘实例、GPU、突发型 CPU 积分、NUMA/裸金属、商业操作系统与许可证。它们有额外固定项或阶梯项。

### 3.2 内存配比系数

以 AWS 第七代 Intel 实例为例：

| 实例 | 配比 | us-east-1 按量价 | 相对 m7i |
|---|---:|---:|---:|
| c7i.large | 2C4G | $0.08925/h | 0.885 |
| m7i.large | 2C8G | $0.10080/h | 1.000 |
| r7i.large | 2C16G | $0.13230/h | 1.313 |

阿里云第九代 Intel 包月价：

| 实例 | 配比 | 杭州包月价 | 每 vCPU 月价 | 相对 g9i |
|---|---:|---:|---:|---:|
| ecs.c9i.large | 2C4G | ¥185.91 | ¥92.96 | 0.779 |
| ecs.g9i.large | 2C8G | ¥238.60 | ¥119.30 | 1.000 |
| ecs.r9i.large | 2C16G | ¥317.48 | ¥158.74 | 1.330 |

两个厂商的 `r/g` 系数几乎相同，约 1.32 至 1.33；AWS `c/g` 约 0.885，阿里云约 0.779。说明内存较少的计算型实例在阿里云折价更深。

### 3.3 架构与代际系数

AWS 当前样本：

- `m7g.large / m7i.large = 0.810`，第七代 Graviton 价格低约 19%。
- `m8g.large / m8i.large = 0.848`，第八代 Graviton 价格低约 15%。
- `m8i.large / m7i.large = 1.05`，Intel 新一代名义价高约 5%。
- `m8g.large / m7g.large = 1.10`，Graviton 新一代名义价高约 10%。
- `m7a.large / m7i.large = 1.15`。AMD 并不天然更便宜，因为厂商也把性能代际计入价格。

阿里云当前样本中，倚天 `g8y.large` 包月 192 元，Intel `g8i.large` 包月 251.16 元，价格系数约 0.764；最新 `g9i.large` 包月 238.60 元，反而比 `g8i` 低约 5%。但是 `g8i` 的多年公开促销更深，因此长期总价仍可能低于 `g9i`。

**结论：** 架构折扣只表示厂商的定价意愿，不等于单位业务性能折扣。数据库必须用自己的 TPS、P99 延迟、压缩、扩展兼容性和故障恢复基准做价格性能归一化。

### 3.4 地域系数

同一 `m8i.large` 相对 AWS `us-east-1`：

| 地域 | 系数 |
|---|---:|
| us-east-1/us-east-2/us-west-2 | 1.000 |
| eu-west-1 | 1.115 |
| eu-central-1 | 1.198 |
| ap-southeast-1 | 1.250 |
| ap-northeast-1 | 1.292 |
| af-south-1 | 1.323 |
| sa-east-1 | 1.594 |

同一 `ecs.g9i.large` 相对阿里云杭州：

| 地域 | 系数 |
|---|---:|
| 杭州/上海/北京 | 1.000 |
| 乌兰察布 | 0.900 |
| 英国伦敦 | 1.338 |
| 美国弗吉尼亚/硅谷 | 1.384 |
| 新加坡 | 1.770 |
| 日本东京 | 1.798 |
| 中国香港 | 1.929 |

阿里云国内核心地域高度同价，低成本地域约便宜 10%；海外溢价明显大于 AWS 相应海外地域。地域选择同时受数据主权、客户延迟、服务可用性、跨地域流量和灾备拓扑约束，不能只按实例价排序。

### 3.5 跨云的算力单位价

AWS `m8i.large` 为 2C8G，按量每 vCPU 月价约 38.63 美元，即 262.0 元，不含适用税。阿里云 `g9i.large`：

- 包月每 vCPU 119.30 元，含税。
- 按量连续运行 730 小时每 vCPU 181.44 元，含税。

在未做性能与地域等价调整前，AWS `us-east-1` Intel 通用算力现金价约为阿里云杭州包月的 2.20 倍、按量的 1.44 倍。这只是价格面，不是采购结论。

## 4. EBS 与 ESSD：容量价格为何经常误导

### 4.1 两种定价哲学

AWS EBS gp3 和阿里云 ESSD AutoPL 都属于“容量与性能解耦”：

- gp3：容量 0.08 美元/GB/月，含 3,000 IOPS 与 125 MiB/s；额外 IOPS 0.005 美元/IOPS/月，额外吞吐 0.04 美元/MiB/s/月，价格随地域变化。[AWS gp3 计费示例](https://aws.amazon.com/ebs/pricing/)
- AutoPL：容量决定基准性能，另售预配置 IOPS，并可按实际突发 IO 收费。基准 IOPS 为 `max(min(1800 + 50 × GiB, 50000), 3000)`；基准吞吐为 `max(min(120 + 0.5 × GiB, 350), 125)`。[ESSD AutoPL 文档](https://help.aliyun.com/zh/ecs/user-guide/essd-autopl-disks)

传统 ESSD PL0-PL3 属于“容量与性能等级绑定”：

| 等级 | 最小容量 | 最大 IOPS | 最大吞吐 | 杭州包月容量价 |
|---|---:|---:|---:|---:|
| PL0 | 1 GiB | 10K | 180 MB/s | ¥0.5/GiB |
| PL1 | 20 GiB | 50K | 350 MB/s | ¥1/GiB |
| PL2 | 461 GiB | 100K | 750 MB/s | ¥2/GiB |
| PL3 | 1261 GiB | 1M | 4000 MB/s | ¥4/GiB |

PL 等级是上限，不是购买后立即得到的固定性能。实际性能随容量增长，直到碰到等级上限。[ESSD 性能规格](https://help.aliyun.com/zh/ecs/user-guide/essds)

### 4.2 容量价比较

按 6.7817 汇率：

- EBS gp3：0.5425 元/GiB/月。
- ESSD PL0：0.5 元/GiB/月。
- ESSD PL1/AutoPL：1 元/GiB/月。
- ESSD PL2：2 元/GiB/月。
- ESSD PL3：4 元/GiB/月。

只按容量，gp3 与 PL0 相近，约为 PL1/AutoPL 的 54%。但这忽略了 AutoPL 随容量附带的性能。

### 4.3 等性能比较

| 场景 | EBS gp3 月价 | ESSD AutoPL 基准月价 | 结论 |
|---|---:|---:|---|
| 200 GiB, 3K IOPS, 125 MiB/s | ¥108.51 | ¥200.00 | gp3 容量基线便宜 |
| 200 GiB, 11.8K IOPS, 220 MiB/s | ¥432.67 | ¥200.00 | AutoPL 基准更便宜 |
| 2048 GiB, 50K IOPS, 350 MiB/s | ¥2765.85 | ¥2048.00 | AutoPL 更便宜 |

第三行还未考虑实例自身的 EBS/ESSD 带宽与 IOPS 上限。最终性能是 `min(云盘上限, 实例存储通道上限)`，花钱购买超出实例通道的 IOPS 没有价值。

### 4.4 预付费对 ESSD 的影响

杭州常见 ESSD 容量的当前公开折扣：

| 期限 | 相对包月 |
|---|---:|
| 按量连续 730 小时 | 1.533 |
| 1 年 | 0.85 |
| 3 年 | 0.50 |
| 5 年 | 0.50 |

存储 3 年后折扣触顶，而算力可继续降到约 0.30 至 0.32。因此承诺期越长，存储占整机成本的比例越高。用户 2024 年文章指出的规律在当前价目中仍然成立。[用户既有 ESSD 观察](https://vonng.com/cloud/ecs/)

### 4.5 极致性能层

AWS io2 把容量与 IOPS 分开，IOPS 按单卷阶梯降价；阿里 ESSD PL-X 也把容量与预配置 IOPS 分开。它们适合高一致性、低延迟、极高 IOPS 的场景，但单价可能远高于通用盘。例如阿里官方示例中 2048 GiB、200 万 IOPS 的 PL-X 月费为 152,048 元，其中 150,000 元来自性能，而不是容量。[ESSD PL-X 示例](https://help.aliyun.com/zh/ecs/user-guide/essd-pl-x-cloud-disk)

这揭示出块存储的标准规律：低端盘按容量赚钱，高端盘按性能赚钱。

## 5. S3 与 OSS：便宜容量背后的活动费

### 5.1 主流容量价

| 存储等级 | AWS us-east-1 | 折算人民币 | 阿里云中国内地 LRS |
|---|---:|---:|---:|
| 标准 | $0.023/GB/月 | ¥0.156 | ¥0.120 |
| 低频 | $0.0125 | ¥0.0848 | ¥0.080 |
| Glacier Instant / OSS 归档 | $0.004 | ¥0.0271 | ¥0.033 |
| Glacier Flexible / OSS 冷归档 | $0.0036 | ¥0.0244 | ¥0.015 |
| Deep Archive / 深度冷归档 | $0.00099 | ¥0.0067 | ¥0.0075 |

这些类别的取回延迟不同，不能只按同一行横比。S3 Glacier Instant 是毫秒访问，OSS 归档通常需要解冻或支付归档直读；OSS 冷归档与 S3 Glacier Flexible 的恢复模式也不同。

### 5.2 小对象税与最低存储期

AWS：

- Standard-IA、One Zone-IA 与 Glacier Instant 最小计费对象为 128 KB。
- Glacier Flexible 与 Deep Archive 每对象额外保存 40 KB 元数据。
- IA 最短 30 天，Glacier Instant/Flexible 最短 90 天，Deep Archive 最短 180 天。[AWS S3 存储类规则](https://aws.amazon.com/s3/pricing/)

阿里云：

- 低频、归档、冷归档、深度冷归档按至少 64 KB 计费。
- 最短存储期分别为 30、60、180、180 天。
- 提前覆盖、转换或删除会收剩余时长费用。[OSS 存储费用规则](https://help.aliyun.com/zh/oss/storage-fees)

大量 1 KB 至 10 KB 小对象会把名义容量放大 6.4 倍至 128 倍。冷存储前必须先计算对象数量、平均大小和生命周期，而不是只统计 TB。

### 5.3 请求费

AWS S3 Standard 典型价格：

- PUT/COPY/POST/LIST：0.005 美元/千次。
- GET：0.0004 美元/千次。[S3 请求定价](https://aws.amazon.com/s3/pricing/)

阿里云中国内地当前公开价：

- Standard PUT 每月每地域前 500 万次免费，超出后 0.01 元/万次。
- Standard GET 每月每地域前 2000 万次免费，超出后 0.01 元/万次。
- 低频与归档 PUT/GET 通常为 0.1 元/万次。
- 深度冷归档 PUT 为 3.5 元/万次。[OSS 当前价格表](https://cn.aliyun.com/price/detail/oss)

对小对象和高请求率工作负载，阿里云 Standard 当前请求价明显低于 S3；但这项政策时间敏感，必须在采购日重新核验。

### 5.4 取回费

对象进入低频或归档后，读取变成收费活动。当前 OSS LRS 数据取回：低频 0.0325 元/GB、归档 0.06 元/GB、冷归档标准 0.06 元/GB、深度冷归档标准 0.018 元/GB。S3 Standard-IA 典型取回为 0.01 美元/GB，Glacier Instant 为 0.03 美元/GB。[AWS S3 定价](https://aws.amazon.com/s3/pricing/)，[OSS 当前价目](https://cn.aliyun.com/price/detail/oss)

冷存储选择应使用：

`月成本 = 容量费 + 请求费 + 取回 GB × 取回单价 + 提前删除 + 恢复临时副本 + 流量`

### 5.5 资源包与自动阶梯

AWS S3 Standard 采用自动容量阶梯，组织内账户合并后更快进入低价区间。[AWS 合并账单容量阶梯](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/useconsolidatedbilling-effective.html)

阿里 OSS 主要使用预付资源包。Standard LRS 100 GB 包：

- 按量容量价：12 元/月。
- 月包：11 元，约 91.7%。
- 半年：54.78 元，相当于月包再乘约 83%。
- 一年：99 元，相当于月包再乘 75%，对按量总价约 68.8%。

资源包过期未用完即失效，地域、冗余类型和计费项不匹配也无法抵扣。[OSS 资源包规则](https://help.aliyun.com/zh/oss/instructions-for-resource-plans-in-the-chinese-mainland-and-region-specific-resource-plans)

## 6. 流量费：云架构中的收费公路

### 6.1 公网出流

AWS 商业区域：

- 互联网入流通常免费。
- 每月前 100 GB 出流在多个 AWS 服务与地域间聚合免费，不适用于 China 与 GovCloud。
- 之后前 10 TB 为 0.09 美元/GB，后续 40 TB 为 0.085，100 TB 为 0.07，超过 150 TB 为 0.05。[AWS EC2 数据传输表](https://aws.amazon.com/ec2/pricing/on-demand/)

阿里云中国内地：

- ECS 杭州按流量出网 0.8 元/GB，入网免费。
- OSS 00:00 至 08:00 为 0.25 元/GB，08:00 至 24:00 为 0.50 元/GB。
- OSS 到 CDN 回源为 0.15 元/GB。

因此，同一份下载数据从 ECS、OSS、CDN 出口走，成本完全不同。大文件分发应优先做对象存储 + CDN 路径建模，而不是从 ECS 直接出网。

### 6.2 同地域跨 AZ

AWS 中，EC2、RDS、ElastiCache 等跨 AZ 通常入和出方向各 0.01 美元/GB。一个应用请求跨 AZ 往返可能产生两个方向的计费。经典 RDS Multi-AZ 的内部同步复制流量包含在 RDS 价格中，但应用跨 AZ 访问、读副本、NAT 和负载均衡路径仍可能收费。[AWS 同地域传输规则](https://aws.amazon.com/ec2/pricing/on-demand/)

阿里云同地域 VPC 内云产品互访通常不收流量费。[阿里云地域与 VPC 说明](https://help.aliyun.com/zh/ecs/user-guide/regions-and-zones) 但经 NAT、CEN、EIP 或跨地域链路后会进入对应产品计费。

### 6.3 NAT 与公网 IPv4

AWS `us-east-1` 常见 NAT Gateway：0.045 美元/小时 + 0.045 美元/GB 处理费，再叠加正常数据传输；公网 IPv4 为 0.005 美元/地址/小时。[AWS VPC 定价](https://aws.amazon.com/vpc/pricing/)

阿里云杭州跨 AZ 容灾 NAT：0.23 元/小时 + 0.23 元/CU；当前 CU 按每小时处理的总入流量与出流量之和除以 1 GB 计算。[阿里云 NAT 计费](https://help.aliyun.com/zh/nat-gateway/nat-gateway-billing)

这类“处理费”会让表面免费的同地域 S3/OSS 流量重新收费。AWS 访问 S3 应优先使用免费的 Gateway Endpoint，避免绕 NAT。[AWS NAT 优化说明](https://aws.amazon.com/vpc/pricing/)

### 6.4 固定带宽与按流量的盈亏平衡

阿里云杭州 1 Mbps 固定公网带宽包月约 23 元；按流量为 0.8 元/GB。两者在 `23/0.8 = 28.75 GB/月` 相交。1 Mbps 连续满载一月理论可传约 328.5 GB，因此带宽利用率超过约 8.8% 时，固定带宽账面上更便宜。5 Mbps 的结论相近，约 9% 至 10%。

固定带宽提供的是峰值与稳定性承诺，按流量模式中的“带宽峰值”通常只是上限，不是性能承诺。[阿里云公网带宽计费](https://help.aliyun.com/zh/ecs/public-bandwidth/)

## 7. RDS 与 EC2/ECS 的深层换算

### 7.1 正确公式

设：

- `n` 为节点数。
- `Cvm` 为单节点 VM 计算价。
- `G` 为逻辑存储 GiB。
- `Pb` 为自建块存储容量价。
- `mu_c, mu_s, mu_i, mu_t` 分别为托管数据库计算、容量、IOPS、吞吐管理系数。

则同拓扑自建：

`Self = n × Cvm + n × G × Pb + Ops + Backup + Network`

托管 RDS：

`RDS = n × mu_c × Cvm + n × mu_s × G × Pb + n × mu_i × IOPS费 + n × mu_t × 吞吐费 + Add-ons`

忽略后半部分时，RDS 总溢价就是各原子系数按自建成本占比的加权平均：

`Markup = w_c × mu_c + w_s × mu_s + w_i × mu_i + w_t × mu_t`

这解释了为什么不存在适用于所有数据库的“RDS 固定倍数”。

### 7.2 AWS RDS 计算系数

`us-east-1` PostgreSQL 当前按量价：

| 同名家族 | 单节点 RDS / EC2 | Multi-AZ RDS / 两台 EC2 | 错误地除以一台 EC2 |
|---|---:|---:|---:|
| m7i | 1.766 | 1.766 | 3.532 |
| m7g | 2.059 | 2.065 | 4.130 |
| r7i | 1.890 | 1.890 | 3.779 |
| r7g | 2.232 | 2.232 | 4.463 |

经典 Multi-AZ 是主节点 + 不可读热备；Multi-AZ DB cluster 是一个 writer + 两个可读 standby。前者要和两节点自建比，后者要和三节点自建比。[RDS Multi-AZ 架构](https://aws.amazon.com/rds/features/multi-az/)

### 7.3 AWS RDS 存储与性能系数

官方 `us-east-1` 2026-08-20 Price List：

| 拓扑 | RDS gp3 容量 | 额外 IOPS | 额外吞吐 | 相对同节点数 EBS 系数 |
|---|---:|---:|---:|---|
| Single-AZ | $0.115/GiB/月 | $0.02/IOPS/月 | $0.08/MiB/s/月 | 1.4375 / 4 / 2 |
| Multi-AZ 一备 | $0.230 | $0.04 | $0.16 | 1.4375 / 4 / 2 |
| Multi-AZ 两个可读备 | $0.345 | $0.06 | $0.24 | 1.4375 / 4 / 2 |

EBS gp3 对应费率为 0.08、0.005、0.04 美元。三种 RDS 拓扑只是把每节点管理价格按 1、2、3 份展开。[AWS RDS Price List](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonRDS/20260820203529/us-east-1/index.json)

RDS PostgreSQL gp3 在 20 至 399 GiB 时附带 3,000 IOPS/125 MiB/s；达到 400 GiB 后因四卷条带化，基线跳到 12,000 IOPS/500 MiB/s，之后才可购买更多性能。[RDS gp3 性能门槛](https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/CHAP_Storage.html)

### 7.4 AWS RDS 总价曲线

以两台 `m7i.large` + 两份 gp3 对比 RDS Multi-AZ：

| 逻辑容量 | RDS / 自建，按量 | 解释 |
|---:|---:|---|
| 20 GiB | 约 1.76 | 计算主导，接近计算系数 |
| 200 GiB | 约 1.71 | 存储权重上升 |
| 1 TiB | 约 1.59 | 接近容量系数 |
| 无限大 | 1.4375 | 容量系数的理论下限 |

这还没有加入自建运维人力、监控、备份、故障演练，也没有加入 RDS 备份超额、Proxy、Performance Insights、Extended Support、跨区与审计。它回答的是“同样云资源原子”的管理加价，不是完整 TCO。

### 7.5 承诺会扩大 AWS RDS 与 EC2 的差距

AWS EC2 的限制越强，公开折扣通常越深。`m7i.large` 参考：

| 工具 | 期限/付款 | 相对按量因子 |
|---|---|---:|
| Compute Savings Plan | 1 年全预付 | 0.754 |
| Compute Savings Plan | 3 年全预付 | 0.506 |
| EC2 Instance Savings Plan | 3 年全预付 | 0.434 |
| Standard RI | 3 年全预付 | 0.395 |

Database Savings Plans 对最新 provisioned 数据库最高约 20%，Serverless 最高约 35%；RDS RI 折扣因家族而异。[AWS Database Savings Plans](https://aws.amazon.com/blogs/aws/introducing-database-savings-plans-for-aws-databases/)

因为 EC2 承诺通常比 RDS 更深，而 RDS RI 不覆盖存储和 I/O，长期稳定负载下 RDS 相对 EC2 的价格倍数往往比按量场景更高。用按量比值评估三年合同会低估 RDS 溢价。

### 7.6 阿里云 RDS 的节点语义

阿里云 PostgreSQL：

- 基础系列：1 节点，实例价与存储价都是整实例价。
- 高可用系列：默认一主一备，备节点不可读，实例价是整套高可用实例价。
- 集群系列：2 至 9 节点，默认可一主一备或一主二备，计算与存储按单节点价 × 节点数。[RDS 集群系列](https://help.aliyun.com/zh/rds/apsaradb-rds-for-postgresql/rds-cluster-edition/)

本地采集的官方询价响应也逐节点重复列出了集群系列的 `rds_class` 与 `rds_storage` 模块，证明不能再额外乘一次隐含主备系数。

### 7.7 阿里云 RDS 与 ECS 当前按量比值

杭州 4C16G、两节点、20 GiB、ESSD PL1 口径：

| RDS 形态 | 计算 / 两台 ECS | RDS 存储 / 两份 ESSD | 20 GiB 总价比 | 存储盈亏平衡 |
|---|---:|---:|---:|---:|
| x86 独享高可用 | 1.386 | 0.810 | 1.363 | 约 1009 GiB |
| 倚天独享高可用 | 1.401 | 0.810 | 1.372 | 约 803 GiB |
| 倚天通用高可用 | 1.007 | 0.810 | 0.997 | 约 14 GiB |
| 倚天独享集群，2 节点 | 1.200 | 0.810 | 1.181 | 约 400 GiB |
| 倚天通用集群，2 节点 | 1.000 | 0.810 | 0.990 | 0 GiB |

“通用型”会与同宿主机其他实例共享 CPU，最大 IOPS 和带宽不保证；“独享型”才适合和企业级 ECS 做较严肃的资源价格比较。[阿里 RDS 规格表](https://help.aliyun.com/zh/rds/apsaradb-rds-for-postgresql/primary-apsaradb-rds-for-postgresql-instance-types/)

独享倚天高可用的按量曲线：

- 20 GiB：RDS 约为两节点 ECS 自建的 1.37 倍。
- 200 GiB：约 1.20 倍。
- 1 TiB：约 0.97 倍。
- 大容量极限：趋近存储系数 0.81。

这不是说 RDS 的真实成本低于硬件，而是阿里云在当前公开价目中对 RDS 容量与数据库产品做了更激进的定价补贴，同时 ESSD 自建路径的存储价较高。

### 7.8 阿里云 RDS 节省计划

RDS 通用型节省计划公开折扣因子：

| 期限 | 全预付 | 半预付 | 0 预付 |
|---|---:|---:|---:|
| 1 年 | 0.50 | 0.70 | 0.80 |
| 3 年 | 0.30 | 0.43 | 0.50 |

可抵扣多数 RDS 后付费项，包括符合条件的规格、存储、代理、备份与审计；IO 突发、归档 OSS 等有例外。[阿里云 RDS 节省计划](https://help.aliyun.com/zh/rds/product-overview/savings-plan-introduction)

若把当前 RDS 按量费率乘 3 年全预付 0.30，并将两台 `g8y.xlarge` 使用 3 年公开包年价、两份 ESSD 使用 0.50 存储因子，独享高可用 RDS 与自建的容量盈亏平衡约从 803 GiB 降到 630 GiB。该结论依赖所有 RDS 计费项持续可抵扣，合同前必须用真实账单验证。

## 8. Aurora 与 PolarDB：共享存储改变了什么

### 8.1 RDS 与云原生数据库的根本差异

传统 RDS HA 更接近：

`N 个数据库 VM + N 份块存储 + 数据库复制`

Aurora/PolarDB 更接近：

`N 个计算节点 + 一份逻辑共享存储 + 存储层多副本`

增加读节点时，传统 RDS 通常增加一份计算和一份完整存储；共享存储数据库主要增加计算，逻辑存储不按读节点重复计费。这是 Aurora/PolarDB 在大容量、多读副本场景的经济学来源。

### 8.2 Aurora 的存储与高可用

Aurora 一个逻辑 cluster volume 跨三个 AZ 存放六个存储副本，与计算实例数量无关。[Aurora 六副本高可用](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Concepts.AuroraHighAvailability.html) 用户只按实际使用的逻辑容量付费，不需要预先分配固定容量。[Aurora 存储计费](https://docs.aws.amazon.com/AmazonRDS/latest/AuroraUserGuide/Aurora.Overview.StorageReliability.html)

但“数据跨三 AZ”不等于“计算已经高可用”。为了快速实例故障切换，生产集群通常仍需在另一 AZ 配置 Aurora Replica，实例费按 writer 和每个 reader 分别收取。

### 8.3 Aurora Standard 与 I/O-Optimized

`us-east-1`：

- Standard：存储 0.10 美元/GB/月，读写 I/O 0.20 美元/百万次。
- I/O-Optimized：计算约为 Standard 的 1.30 倍，存储 0.225 美元/GB/月，读写 I/O 为 0。[Aurora 价格示例](https://aws.amazon.com/rds/aurora/pricing/)

设 Standard 月计算费为 `C` 美元，逻辑存储为 `G` GB，月 I/O 为 `I` 百万次：

`Standard = C + 0.10G + 0.20I`

`I/O-Optimized = 1.30C + 0.225G`

精确盈亏平衡：

`I > 1.5C + 0.625G`

示例：

| Standard 计算/月 | 存储 | I/O-Optimized 盈亏平衡 | 折算平均 IOPS |
|---:|---:|---:|---:|
| $208.8 | 80 GB | 363.2M I/O/月 | 140 |
| $417.6 | 1 TB | 1.251B I/O/月 | 483 |
| $1000 | 5 TB | 4.625B I/O/月 | 1784 |

AWS 的“当 I/O 支出超过 Aurora 总支出 25% 时可能节省”是便捷经验，不替代上述精确公式。[Aurora I/O-Optimized 说明](https://aws.amazon.com/rds/aurora/pricing/)

### 8.4 Aurora 与经典 RDS 的拐点

以两个 `r6i.large` 计算节点：

- RDS Multi-AZ 计算约 365 美元/月，gp3 0.23 美元/逻辑 GB/月。
- Aurora Standard 两节点计算约 423.4 美元/月，存储 0.10 美元/GB/月，另收 I/O。

忽略 I/O 时，Aurora 在约 449 GiB 后低于经典 RDS；100M I/O/月时约 603 GiB；1B I/O/月时约 1.99 TiB。Aurora 还按实际使用空间而不是预留空间收费，数据稀疏或预留水位高时拐点会提前。

### 8.5 PolarDB 的共享存储

PolarDB PostgreSQL 企业版采用计算存储分离，主节点和只读节点共享一份逻辑数据。[PolarDB 架构](https://help.aliyun.com/zh/polardb/polardb-for-postgresql/polardb-for-postgresql-architecture) 单可用区存储本身使用三副本；双可用区主备存储集群各三副本，共六副本，存储价格更高；若同时启用计算热备，备区计算节点单独收费。[PolarDB 高可用模式](https://help.aliyun.com/en/polardb/polardb-for-postgresql/deploy-a-cluster-across-zones-and-change-the-primary-zone)

中国内地当前按量参考：

- 4C16G 独享计算节点 `polar.pg.x4.large`：2.085 元/节点/小时。
- 集群版默认一主一只读两个节点。[PolarDB 计算节点价格](https://help.aliyun.com/zh/polardb/polardb-for-postgresql/billing-rules-of-pay-as-you-go-compute-nodes/)
- PSL4 单可用区约 0.00158 元/GB/小时，PSL5 约 0.00243 元/GB/小时。[PolarDB Serverless 存储价](https://help.aliyun.com/zh/polardb/polardb-for-postgresql/serverless-cost-description)

### 8.6 PolarDB 与 RDS 集群的拐点

使用当前杭州倚天独享 RDS 集群询价反推，RDS 4C16G 每节点计算约 0.96 元/小时，存储约 0.0017 元/GB/小时/节点。对单可用区 PolarDB：

| 节点数 | PSL4 拐点 | PSL5 拐点 |
|---:|---:|---:|
| 2 | 约 1.21 TiB | 约 2.26 TiB |
| 3 | 约 0.94 TiB | 约 1.23 TiB |
| 4 | 约 0.84 TiB | 约 1.01 TiB |

读节点越多，RDS 重复存储越多，共享存储架构越容易摊薄较高的计算节点价格。以上只比较单可用区公开资源价；PolarDB 双可用区六副本、计算热备、存储包和计算包会改变结果，不能把表中拐点当正式报价。

### 8.7 Serverless 的真实定价单位

- Aurora ACU：约 2 GiB 内存及对应 CPU/网络，按秒计费，Standard 在 us-east-1 示例为 0.12 美元/ACU/小时，I/O-Optimized 为 0.156。[Aurora ACU](https://aws.amazon.com/rds/aurora/pricing/)
- RDS PostgreSQL RCU：约 1 核上限 + 2 GB，杭州 0.333 元/RCU/小时，HA 节点数乘 2；存储仍按节点数与最低容量收费。[阿里 RDS Serverless](https://help.aliyun.com/zh/rds/apsaradb-rds-for-postgresql/pricing-of-serverless-apsaradb-rds-for-sql-server-instances)
- PolarDB PCU：约 1 核 + 2 GB，企业版中国内地约 0.40 元/PCU/小时，标准版约 0.35；计算包约 0.38 元/PCU/小时并按地域系数抵扣。[PolarDB Serverless](https://help.aliyun.com/zh/polardb/polardb-for-postgresql/serverless-cost-description)

Serverless 只有在平均容量显著低于 provisioned 规格时才便宜。应比较 `平均 ACU/RCU/PCU × 单价`，而不是峰值规格；同时纳入最小容量、自动暂停等待、扩容延迟、每个 reader 独立最低容量与存储不缩容。

## 9. 折扣与预付费：厂商出售风险，客户购买确定性

### 9.1 AWS 的折扣梯度

从灵活到限制：

1. On-Demand：最高单价，无长期承诺。
2. Spot：最高可比按量低 90%，但可被中断，AWS 通常只给 2 分钟通知。[EC2 Spot](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-instance-termination-notices.html)
3. Compute Savings Plan：跨家族、地域，覆盖 EC2/Fargate/Lambda，灵活但折扣较浅。
4. EC2 Instance Savings Plan：限定地域与实例族，折扣更深。
5. Convertible RI：可转换，折扣低于 Standard RI。
6. Standard RI：限制最强，通常公开折扣最深。

`m7i.large` 当前本地快照的 3 年全预付因子：Compute SP 0.506，Instance SP 0.434，Standard RI 0.395。限制越强，厂商给出的价格越低。

### 9.2 阿里云的折扣梯度

阿里云并行存在：

- 包年包月：绑定具体资源。
- 预留实例券：匹配地域、家族等属性。
- ECS 计算型 Savings Plan：覆盖实例计算，限制较多，折扣更深。
- 通用型 Savings Plan：可跨更多规格、地域与部分系统盘/带宽，灵活性高。
- SCU 与 OSS 资源包：承诺具体容量或用量。
- 抢占式实例：闲置库存市场价，最低可至按量 1 折，但不适合数据库。[阿里云抢占式实例](https://help.aliyun.com/zh/ecs/spot-instance/)

阿里云官方称 ECS Savings Plan 合理配置后最高可降低 83%，实际折扣由期限、付款、地域、规格和计划类型决定，需要登录折扣查询页核验。[阿里云 ECS Savings Plan](https://help.aliyun.com/zh/ecs/savings-plans/)

### 9.3 承诺利用率公式

设承诺费率为按量价的 `f`，承诺覆盖资源的实际利用率为 `u`：

`有效价格因子 = f / u`

`实际节省率 = 1 - f/u`

只有 `u > f` 才真正省钱。

| 标称因子 f | 盈亏平衡利用率 | u=70% 的实际节省 | u=90% 的实际节省 |
|---:|---:|---:|---:|
| 0.80 | 80% | -14.3% | 11.1% |
| 0.70 | 70% | 0% | 22.2% |
| 0.50 | 50% | 28.6% | 44.4% |
| 0.30 | 30% | 57.1% | 66.7% |

企业不应追求 100% 覆盖率，而应先覆盖长期用量曲线的低谷，再让短期峰值保持按量或 Spot。FinOps 的核心 KPI 是 utilization 与 coverage 的组合，而不是宣传折扣率。[AWS 承诺购买 playbook](https://www.finops.org/wg/purchasing-commitment-discounts-in-aws/)

### 9.4 预付现金的时间价值

阿里 `g9i` 当前公开 1/3/5 年名义因子约 0.70/0.46/0.32。若资本成本为 8%，把未来逐月支付折现后，全预付的经济因子变为约：

| 期限 | 名义因子 | 8% 资本成本后的因子 | 经济折扣 |
|---|---:|---:|---:|
| 1 年 | 0.70 | 0.730 | 27.0% |
| 3 年 | 0.46 | 0.517 | 48.3% |
| 5 年 | 0.32 | 0.387 | 61.3% |

五年“68% 名义折扣”在 8% 资金成本下约为 61% 经济折扣。还未计未来实例降价、代际淘汰和迁移期权，因此越长的承诺越应该使用更高的风险门槛。

### 9.5 支持费会反向吞噬折扣

AWS 当前 Business Support+ 最低 29 美元/账户/月，按月用量阶梯约 9%/7%/5%/3%；Enterprise Support 最低 5000 美元/月，按 10%/7%/5%/3% 阶梯。全预付 Savings Plans、RI 等预付款会在购买当月计入支持费基数，造成现金峰值。[AWS Support 定价](https://aws.amazon.com/premiumsupport/pricing/)

阿里云国际站 Business 支持最低 100 美元/月，Enterprise 最低 8000 美元/月；中国站支持计划文档还说明包年包月按折前价摊销计算服务费，后付费部分需按账户折前消费评估。[Alibaba Cloud 支持价格](https://www.alibabacloud.com/en/pricing)，[中国站支持计费](https://help.aliyun.com/document_detail/73692.html)

企业合同如果要求购买高级支持，必须把支持费增量计入“合同净折扣”，而不是只比较资源折扣百分比。

## 10. 商务成交价与企业真实成本

### 10.1 AWS 私有价格

AWS EDP/PPA 等条款通常受 NDA 约束，没有公开统一折扣表。FinOps Foundation 也明确把组织专属折扣视为私有合同，不建议用一个市场数字代替实际条款。[FinOps Rate Optimization](https://www.finops.org/framework/capabilities/rate-optimization/)

因此本报告不宣称“典型 AWS 商务折扣是 X%”。可复算模型提供 5%、10%、15% 三档敏感性，只用于回答“若合同折扣为 X，结论是否改变”。正式采购必须读自己的 Private Pricing、EDP drawdown、eligible spend、support requirement、MAP credits、Marketplace 是否计入承诺等条款。

AWS 2025 年 10-K 披露，AWS 销售增长被“主要由长期客户合同驱动的价格变化”部分抵消，证明长期合同确实系统性改变实现单价。AWS 2025 年收入 1287.25 亿美元、经营利润 456.06 亿美元，经营利润率约 35.4%。但这个分部利润混合了算力、存储、网络、软件服务、支持、折旧、研发和销售，不能反推某个 EC2 或 EBS SKU 的边际成本。[Amazon 2025 10-K](https://www.sec.gov/Archives/edgar/data/1018724/000101872426000004/amzn-20251231.htm)

### 10.2 阿里云企业合同与渠道价

阿里云账单字段给出更清晰的价格瀑布：

`应付金额 = 目录总价 - Savings Plan 抵扣目录总价 - 优惠金额 - 优惠券抵扣 - 抹零`

核对合同折扣时，应使用 `(官网价 - 优惠金额) / 官网价`，不能用最终应付/目录价，因为后者还混入 Savings Plan 与券。[阿里云账单公式](https://help.aliyun.com/zh/user-center/product-overview/announcement-on-the-updates-of-the-voucher-and-coupon-scheme)

一份历史公开采购披露曾描述特定阿里云渠道项目获得 6 折至 8.5 折、综合约 8 折的供应商政策。这只能证明渠道层存在独立折扣空间，不能推广为 2026 年直客或任何产品的统一价。[特定采购披露](https://qxb-pdf-osscache.qixin.com/AnBaseinfo/32862b42c31e1ad9c3cc5308d388522a.pdf)

### 10.3 企业有效成本瀑布

建议按以下顺序对账：

1. **List cost：** 目录单价 × 实际 meter。
2. **Public rate optimization：** RI/SP/包年包月/资源包覆盖后的摊销成本。
3. **Private pricing：** 合同折扣与产品 PPA。
4. **Credits and coupons：** MAP、迁移金、代金券、折扣券、渠道返佣。
5. **Mandatory adders：** 支持费、税、汇率、支付、专线、安全与第三方软件。
6. **Waste：** 闲置承诺、孤儿磁盘/快照/IP、过配、未使用资源包、跨区路径错误。
7. **Useful unit cost：** 以上现金成本除以有效 CPU 小时、有效 TB 月、有效请求、有效数据库 TPS 或业务交易。

### 10.4 税与现金口径

阿里云中国站价目含税。若一般纳税人取得可抵扣 6% 专票，净经济成本约为含税现金价除以 1.06；不能抵扣时则以含税现金为成本。AWS 公共价通常不含税，实际税由卖方实体、账单地址与地区决定。[阿里云发票说明](https://help.aliyun.com/zh/user-center/user-guide/request-an-invoice)，[AWS 税费说明](https://aws.amazon.com/ebs/pricing/)

跨云比较至少同时给出：

- Cash view：实际付款现金。
- P&L view：承诺摊销、Credits、可抵扣税与汇兑损益。
- Unit economics view：每业务单位的完全成本。

### 10.5 厂商成本不等于客户价格

AWS 分部经营利润率很高，阿里云最新财报中的 Cloud Intelligence adjusted EBITA 率明显更低，且两家都在加大 AI 基础设施投入。[Alibaba FY2026 Cloud 更新](https://www.alibabagroup.com/en-US/document-1991364841188622336) 但会计口径、产品组合和内部成本分摊不同，不能据此宣布某种资源“毛利率等于分部利润率”。

可以确认的是：

- 按量溢价补偿需求不确定性与闲置库存。
- 长约折扣降低销售与容量规划风险并前置现金。
- 存储、网络、请求等高黏性 meter 能回收低价计算入口的利润。
- 商务折扣体现价格歧视与客户迁移弹性，不是硬件成本的直接函数。

## 11. 实操决策框架

### 11.1 先建立工作负载指纹

每个候选架构至少需要：

- 过去 90 至 180 天逐小时 vCPU、内存、IOPS、吞吐、容量与网络。
- CPU/内存 P50、P90、P95、P99 与峰谷时段。
- 对象数、平均/分位对象大小、GET/PUT、取回 GB、生命周期。
- 数据库写 IOPS、读 IOPS、buffer hit、WAL、备份增量、读写比例。
- RTO、RPO、允许的 AZ/Region 故障边界。
- 业务增长、项目结束、迁移、硬件/实例代际计划。

### 11.2 把稳定低谷和弹性峰值分开

- 稳定低谷：RI/SP/包年包月。
- 可预测季节峰值：短期按量、定时扩容、Serverless。
- 可中断批处理：Spot/抢占式。
- 不可中断数据库：不要用 Spot 承载唯一主节点；可把备份校验、分析、ETL、只读离线任务放到 Spot。

### 11.3 数据库比较的最低合格表

必须逐行列出：

| 类别 | 自建 | RDS | Aurora/PolarDB |
|---|---|---|---|
| 计算节点与可读性 | 主/备/读节点 | Single/Multi-AZ/Cluster | writer/reader |
| 存储副本 | 每节点块盘 | 每节点块盘或整实例价 | 共享存储物理副本 |
| 容量 | provisioned | provisioned | actual used 或 provisioned |
| IOPS/吞吐 | 盘 + 实例限制 | RDS 性能费 | request I/O 或共享层能力 |
| 备份 | 快照/对象存储 | 免费额度 + 超额 | 免费额度 + 超额 |
| 网络 | 跨 AZ/公网/NAT | 内部复制与应用流量 | reader/Global/GDN |
| 运维 | 人力、值班、演练 | 服务内含与 Add-ons | 服务内含与 Add-ons |
| 折扣 | EC2/ECS + 存储各自折扣 | RDS RI/SP | DB SP/RI/资源包 |

不满足这张表的“RDS 比 EC2 贵几倍”都只是宣传或情绪，不是核算。

### 11.4 商务谈判清单

- 用过去 12 个月真实 CUR/账单测 eligible spend，不用总账单猜折扣。
- 把资源折扣、支持费、Credits、迁移服务、培训、Marketplace、超承诺价、退出条款分别列出。
- 争取产品级 PPA 的对象应是高占比且缺少公开承诺工具的 meter，例如 S3/OSS、流量、RDS 存储与请求。
- 采购承诺按低谷而不是均值；分批购买，避免一次锁满。
- 用竞争云、自建与托管服务的可迁移方案创造真实谈判杠杆。
- 合同中明确价格下降、新实例代际、组织账号共享、收购拆分、Region 迁移和未用承诺处理。

### 11.5 每月控制面

至少监控：

- Commitment utilization、coverage、effective savings rate。
- 未挂载盘、旧快照、空闲 IP、低利用实例、孤儿负载均衡/NAT。
- 跨 AZ、NAT、互联网出流与对象取回突增。
- RDS 存储水位、IOPS/吞吐基线、备份超额、Extended Support。
- OSS/S3 小对象膨胀、最低时长违约与资源包到期。
- 合同折扣实际命中率与券消耗顺序。

## 12. 最终判断

### AWS 的标准规律

- 公共价结构清晰，Price List 可机器读取，地域与活动型 meter 很细。
- 计算按族线性，公开承诺从灵活 SP 到限制 RI 形成连续梯度。
- gp3 容量便宜，但性能单独收费；RDS 在容量、IOPS、吞吐上设置不同管理系数。
- S3 容量便宜，靠请求、取回、流量、复制与管理功能形成完整收入面。
- RDS PostgreSQL 的核心经济特征是“约两倍计算管理价 + 1.4375 倍容量价 + 更高性能费”；长期 EC2 折扣更深时，RDS 相对溢价扩大。
- Aurora 不是便宜版 RDS，而是用更贵计算和活动 I/O 换共享六副本存储、弹性容量和快速扩展；价值在大容量、多 reader 或高运维要求场景。

### 阿里云的标准规律

- 目录价、官网折扣价、合同价与券层次更多，最终成交价必须从账单字段还原。
- 包月以约 480 小时按量价作为锚，按量连续满月约贵 50%。
- c/g/r 线性与内存配比规律稳定，国内核心地域同价，海外溢价大。
- ESSD 传统 PL 以容量绑定性能，AutoPL 转向容量与性能解耦；算力承诺折扣深于存储。
- OSS 容量价与 S3 已接近，但当前中国内地标准请求免费额度、闲忙时流量价和资源包机制非常不同。
- RDS PostgreSQL 公共价格明显更激进，独享高可用计算管理系数约 1.4，存储可低于两份 ESSD；大容量时 RDS 可比两台 ECS 自建便宜。
- PolarDB 用共享存储消除读节点的重复容量，但计算节点贵；优势随容量和节点数增加而出现，双可用区六副本必须单独报价。

### 对采购者最有用的原则

1. 先统一拓扑，再比较价格。
2. 先统一性能，再比较存储容量价。
3. 先画完整数据路径，再比较流量价。
4. 先算承诺利用率，再看宣传折扣。
5. 先还原账单瀑布，再谈商务折扣。
6. 先定义有效业务单位，再判断云、自建或托管谁更便宜。

云的定价并不神秘。它只是把硬件资源、可靠性、弹性、运维、资金与迁移风险拆成很多 meter，再用折扣重新组合。真正的成本优势来自正确架构和高利用率，而不是一张看上去折扣很大的报价单。

## 限制与待更新项

- 价格随时间、地域、活动与合同变化；所有数值都应带 2026-08-22 快照标签。
- 阿里 RDS 动态报价是 20 GiB、按量付费的受控样本；多年订阅用公开 Savings Plan 因子做情景，不等于正式订单。
- PolarDB 双可用区存储的精确当前倍数需要购买页或正式询价，报告只陈述其六副本与“价格更高”的官方规则。
- AWS/阿里私有合同通常受 NDA 约束，本报告只提供敏感性模型，不提供虚构的统一商务折扣。
- vCPU 价格没有按 SPEC、数据库 TPS 或 P99 性能校正；架构迁移必须用实测替代价格系数。
- 自建 TCO 的机房、电力、网络、硬件、备件、人力、值班、资金与残值没有在本报告固定为单一数字，配套工作簿允许自行输入。
