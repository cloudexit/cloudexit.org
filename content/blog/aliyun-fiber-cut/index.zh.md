---
title: "阿里云又挂了，这次是光缆被挖断了？"
date: 2024-07-02
authors: [vonng]
summary: >
  上海可用区 N 核心服务受影响半个小时，知情人士透露故障的根因是挖掘机挖断专线。
categories: [failures-postmortems]
tags:
  - vendor-alibaba-cloud
  - service-networking
  - topic-reliability
  - topic-centralization-risk
  - form-incident-report
  - tone-cautionary
archive_source: "https://vonng.com/cloud/aliyun-fiber-cut/"
archive_section: "cloud"
---

根据阿里云健康看板与公告，就在刚刚，上海可用区 N 出现网络访问异常。受到影响的服务包括：OSS，ECS，RDS，K8S，OTS，DTS，KMS，PolarDB，Redis，Mongo，ElasticSearch；从发现故障到解决用时 31 分钟，从发现故障到影响恢复用时 38 分钟。

据知情人士透露，本次故障根因是：**专线被挖掘机挖断了**。（小道消息，请以官网通告为准）

![阿里云又挂了，这次是光缆被挖断了（图 1）](01.webp)

阿里云故障公告地址：https://status.aliyun.com/#/eventDetail?eventId=20

------------------------------------------------------------------------

影响的服务范围看上去”不大“，但要命的核心服务一个都没拉下：对象存储，云服务器，云数据库，K8S……。

![阿里云又挂了，这次是光缆被挖断了（图 2）](02.webp)

------------------------------------------------------------------------

据知情人士透露，本次故障根因是：**专线被挖掘机挖断了**，进而导致其他服务异常。不过，这次故障是单可用区故障，所以一些云数据库服务可以进行主备切换，将流量切换到其他可用区。

![阿里云又挂了，这次是光缆被挖断了（图 3）](03.webp)

有不少使用该可用区的业务受到影响，比如 B 站实时弹幕功、小红书、恋与深空等。。

------------------------------------------------------------------------

### 下云老冯评论

公有云的高可用神话已经在一次又一次频繁发生的故障与响应表现中被打破了。前面有  [**阿里云全球服务不可用**](/zh/blog/aliyun/)  的史诗级故障，后有 [**Google 云删除大基金的整个云账户**](/zh/blog/gcp-unisuper/) 的传说级故障，各种中小故障更是此起彼伏。

尽管这一次故障并没有去年双十一  [**阿里云全球服务不可用**](/zh/blog/aliyun/)  那样惊天动地，但半个小时的单可用区核心服务故障仍然称得上是一次“显著故障”。

公有云并非它们营销所宣称的数字化转型的万灵药，也不是可以买后真的甩手不管的运维外包魔法，希望用户在采购与技术选型时能认识到这一点，并审慎地进行决策。

## 相关文章

- [我们能从阿里云史诗级故障中学到什么](/zh/blog/aliyun/)
- [阿里云周爆：云数据库管控又挂了](/zh/blog/aliyun-weekly-crash/)
- [牙膏云？您可别吹捧云厂商了](/zh/blog/toothpaste-cloud/)
- [从降本增笑到真的降本增效](/zh/blog/smile/)
- [罗永浩救不了牙膏云](/zh/blog/luo-live/)
- [互联网故障背后的草台班子们](/zh/blog/amateur-internet-outages/)
- [迷失在阿里云的年轻人](/zh/blog/lost-youth-at-aliyun/)
- [腾讯云/阿里云故障背后：投入不足](/zh/blog/cloud-outage-underinvestment/)
- [转载：从头到尾复盘腾讯云故障](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247487326&idx=1&sn=a19e6ee548fbe8bd6e899e582c63d31d&chksm=fe4b3a85c93cb393165cf2db37fb9d68dbd56139a5f40c5ac0a69e6aa5b1cd5ef4c057514054&scene=21#wechat_redirect)
- [故障不是腾讯云草台的原因，傲慢才是](http://mp.weixin.qq.com/s?__biz=MzU5ODAyNTM5Ng==&mid=2247487322&idx=1&sn=742491d10ec4f1538d38307fe0f8c625&chksm=fe4b3a81c93cb39701f9fed4e41f658643199848ea82cb28b50daf760e7d3c843d84d0965c71&scene=21#wechat_redirect)
- [腾讯云：颜面尽失的草台班子](/zh/blog/tencent-disgrace/)
- [云上黑暗森林：打爆云账单，只需要 S3 桶名](/zh/blog/s3-scam/)
- [删库：Google 云爆破了大基金的整个云账户](/zh/blog/gcp-unisuper/)
- [为什么我们的云老是故障](/zh/blog/why-cloud-keeps-failing/)
- [你用的公有云都没做过测试](/zh/blog/public-cloud-untested/)
- [赛博菩萨 Cloudflare 圆桌访谈与问答录](/zh/blog/cf-interview/)
- [Ahrefs 不上云，省下四亿美元](/zh/blog/ahrefs-saving/)
