---
title: Outage chronology
linkTitle: Outages
description: Material service incidents recorded with event time, scope, source tier, accountability, and uncertainty.
weight: 10
---

> [!NOTE]
> Collection skeleton ready. Incident records have not yet been imported.

## Record contract {#contract}

Each incident stores event start and end, detection time, provider and service,
regions, customer-visible impact, dependency chain, status-page timeline,
provider report, SLA remedy, corrective action, primary and secondary sources,
confidence, dispute state, and revision history.

## Inclusion rule {#inclusion}

Include an incident when it materially affects service availability, integrity,
confidentiality, customer control, or the ability to recover—and when at least
one checkable source exists. Popularity alone is not an inclusion rule.

## What this collection should answer {#questions}

- What failed, for whom, and for how long?
- Which dependency expanded the blast radius?
- What did the provider know and communicate at each point?
- What remedy and corrective action followed?
- Which facts are still unknown or disputed?

