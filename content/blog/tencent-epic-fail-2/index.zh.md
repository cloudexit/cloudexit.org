---
title: "【腾讯】云计算史诗级二翻车来了"
date: 2024-04-08
authors: [vonng]
summary: >
  腾讯云管控面大故障，阿里云双十一大故障翻版。疑似 Auth 问题 —— 云计算史诗级二故障来了
categories: [failures-postmortems]
tags:
  - vendor-tencent-cloud
  - service-iam-control-plane
  - topic-reliability
  - topic-architecture
  - form-incident-report
  - tone-cautionary
archive_source: "https://vonng.com/cloud/tencent-epic-fail-2/"
archive_section: "cloud"
---

就在现在，腾讯云管控面挂了。症状几乎和 **[去年双十一阿里云史诗级大故障](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247486452&idx=1&sn=29cff4ee30b90483bd0a4f0963876f28&chksm=fe4b3e2fc93cb739af6ce49cffa4fa3d010781190d99d3052b4dbfa87d28c0386f44667e4908&scene=21#wechat_redirect)**一毛一样：CVM 虚拟机，RDS 数据库还可以正常运行，但是管控面，特别是和 Auth 有关的无一幸免。[**堪称阿里云故障翻版**](/zh/blog/aliyun/)**。**

这篇给阿里云做的的非官方复盘文章《[**我们能从阿里云史诗级故障中学到什么**](/zh/blog/aliyun/)》，把阿里云三个字改成腾讯云，读起来丝毫没有一点儿违和感。也许是[**降本增笑**](/zh/blog/smile/)太狠了，SRE 今年的年终奖又要泡汤了。

![【腾讯】云计算史诗级二翻车来了（图 1）](01.webp)

我自己还有几台 CVM 虚拟机跑 Demo，也用了[**腾讯云的 CDN**](/zh/blog/cdn/) 服务，登陆到控制台上，也访问不了了。看来确实要抓紧[**彻底迁移到 Cloudflare**](/zh/blog/cloudflare/) 上去了。

查看了一下腾讯云健康状态页（https://status.cloud.tencent.com/）发现服务还都是“正常的”，也没有公开通告。不过一些群里已经传出了消息，希望能够尽快恢复吧。

![【腾讯】云计算史诗级二翻车来了（图 2）](02.webp)

![【腾讯】云计算史诗级二翻车来了（图 3）](03.webp)

------------------------------------------------------------------------

今天晚上八点，我在微信直播《[云数据库是不是杀猪盘](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247487249&idx=1&sn=9003873f73089ae603ae1cadd734d3f6&chksm=fe4b3acac93cb3dcabe45ac0965b231f0b6f88dcf85c2ac898ad169bfdc4a23b85c5f69b7aff&scene=21#wechat_redirect)》，嘲讽云服务的质量安全效率成本并不过关，没想到腾讯这么赶趟儿送个大人头。还好，看起来微信还可以正常直播，，不知道是不是没有用自家的云哈哈……欢迎大家预约收看，吐槽云厂商。

## 相关文章

- [云数据库是不是智商税](/zh/blog/rds/)
- [牙膏云？您可别吹捧云厂商了](/zh/blog/toothpaste-cloud/)
- [罗永浩救不了牙膏云](/zh/blog/luo-live/)
- [吊打公有云的赛博佛祖 Cloudflare](/zh/blog/cloudflare/)
- [云计算为啥还没挖沙子赚钱？](/zh/blog/profit/)
- [FinOps 终点是下云](/zh/blog/finops/)
- [卡在政企客户门口的阿里云](/zh/blog/aliyun-enterprise-market/)
- [云厂商眼中的客户：又穷又闲又缺爱](/zh/blog/cloud-customers-poor-bored-lonely/)
- [阿里云降价背后折射出的绝望](/zh/blog/aliyun-price-cut-despair/)
- [迷失在阿里云的年轻人](/zh/blog/lost-youth-at-aliyun/)
- [互联网故障背后的草台班子们](/zh/blog/amateur-internet-outages/)
- [门内的国企如何看门外的云厂商](/zh/blog/state-owned-enterprise-cloud-view/)
- [剖析云算力成本，阿里云真的降价了吗？](/zh/blog/ecs/)
