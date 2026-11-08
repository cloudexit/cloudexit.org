---
outputs: [HTML, RSS, print, markdown, LLMSFULL]
title: Evidence Archive
linkTitle: Evidence
description: A dated, source-ranked record of outages, lock-in mechanisms, and public claims.
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
> The collection templates are ready. Structured incident, lock-in, and claim records have not yet been published. Source commentary is available in the [essay archive](/blog/).

Outages are not anomalies; they are the unavoidable physics of centralized infrastructure.

When thousands of mission-critical systems depend on a shared, proprietary control plane, "five-nines availability" often shrinks into SLA credit coupons when disaster strikes. A token discount on next month's invoice cannot offset catastrophic downtime, corrupted data, or eroded customer trust.

The **Evidence Archive** maintains a timestamped, peer-verifiable record of public cloud failure modes, proprietary lock-in mechanisms, and marketing claims contrasted directly against observable production reality.

## Three Core Collections {#collections}

{{< cards >}}
  {{< card title="Outage Chronology" link="/evidence/outages/" icon="fa-solid fa-triangle-exclamation" badge="Incidents" >}}
Timestamped records of major cloud outages, cascading blast radiuses, first-party RCA audits, and long-term remediation tracking.
  {{< /card >}}
  {{< card title="Lock-in Map" link="/evidence/lock-in/" icon="fa-solid fa-link" badge="Architecture" >}}
Technical deconstruction of proprietary storage formats, message queues, bespoke control planes, and IAM dependency traps.
  {{< /card >}}
  {{< card title="Claims vs Reality" link="/evidence/claims/" icon="fa-solid fa-quote-right" badge="Audit" >}}
Juxtaposing vendor marketing promises of infinite elasticity directly alongside observable production downtime and throttle limits.
  {{< /card >}}
{{< /cards >}}

## Evidence Discipline {#discipline}

- **Primary Sources First**: Every entry distinguishes observed timestamps, verified first-party postmortems, and community audits from speculative commentary.
- **Auditable & Dynamic**: Disputed or unverified details remain transparently noted; as cloud providers release technical fixes or reduce egress tolls, records are updated with public changelogs.
- **Curated Foundations**: Structured and synthesized from the extensive research archive at [vonng.com/cloud](https://vonng.com/cloud/) and global infrastructure postmortems.

